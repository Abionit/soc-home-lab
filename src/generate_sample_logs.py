from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

SEED = 42

USERS = [
    {"user": "alice", "department": "Finance", "role": "finance-analyst"},
    {"user": "bob", "department": "IT", "role": "system-administrator"},
    {"user": "carol", "department": "HR", "role": "hr-specialist"},
    {"user": "dave", "department": "Sales", "role": "sales-manager"},
    {"user": "eve", "department": "Security", "role": "soc-analyst"},
]

HOSTS = [
    {"hostname": "vpn-gateway-01", "asset_group": "identity", "asset_criticality": "high", "log_source": "vpn"},
    {
        "hostname": "dc01",
        "asset_group": "identity",
        "asset_criticality": "critical",
        "log_source": "windows-security",
    },
    {"hostname": "mail-01", "asset_group": "messaging", "asset_criticality": "high", "log_source": "m365-audit"},
    {
        "hostname": "filesrv-01",
        "asset_group": "collaboration",
        "asset_criticality": "medium",
        "log_source": "file-audit",
    },
    {"hostname": "hr-app-01", "asset_group": "business-app", "asset_criticality": "high", "log_source": "app-audit"},
    {
        "hostname": "jumpbox-01",
        "asset_group": "admin",
        "asset_criticality": "critical",
        "log_source": "windows-security",
    },
]

SOURCES = [
    {"source_ip": "181.49.10.12", "geo": "CO", "network_zone": "corp-wan"},
    {"source_ip": "45.227.80.3", "geo": "CO", "network_zone": "corp-wan"},
    {"source_ip": "190.145.200.18", "geo": "CO", "network_zone": "branch-office"},
    {"source_ip": "10.0.2.15", "geo": "INTERNAL", "network_zone": "server-lan"},
    {"source_ip": "192.168.1.22", "geo": "INTERNAL", "network_zone": "user-lan"},
    {"source_ip": "77.91.72.10", "geo": "RU", "network_zone": "internet"},
    {"source_ip": "45.178.1.92", "geo": "US", "network_zone": "internet"},
]


def build_event(ts: datetime, user: dict, source: dict, host: dict, event_type: str, success: bool) -> dict:
    return {
        "timestamp": ts.isoformat(),
        "user": user["user"],
        "department": user["department"],
        "role": user["role"],
        "source_ip": source["source_ip"],
        "geo": source["geo"],
        "network_zone": source["network_zone"],
        "hostname": host["hostname"],
        "asset_group": host["asset_group"],
        "asset_criticality": host["asset_criticality"],
        "log_source": host["log_source"],
        "event_type": event_type,
        "success": success,
    }


def choose_event_type(rng: random.Random) -> str:
    roll = rng.random()
    if roll < 0.56:
        return "login_success"
    if roll < 0.74:
        return "file_access"
    if roll < 0.86:
        return "login_failed"
    if roll < 0.94:
        return "password_reset"
    return "privilege_change"


def choose_host(rng: random.Random, event_type: str) -> dict:
    if event_type == "privilege_change":
        privileged_hosts = [host for host in HOSTS if host["hostname"] in {"dc01", "jumpbox-01"}]
        return rng.choice(privileged_hosts)
    if event_type == "password_reset":
        identity_hosts = [host for host in HOSTS if host["asset_group"] in {"identity", "messaging"}]
        return rng.choice(identity_hosts)
    return rng.choice(HOSTS)


def generate_events(total: int = 320) -> list[dict]:
    rng = random.Random(SEED)
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    events: list[dict] = []

    for idx in range(total):
        ts = now - timedelta(minutes=total - idx)
        user = rng.choice(USERS)
        source = rng.choices(SOURCES, weights=[18, 16, 12, 20, 18, 5, 6], k=1)[0]
        event_type = choose_event_type(rng)
        host = choose_host(rng, event_type)
        success = event_type != "login_failed"
        events.append(build_event(ts, user, source, host, event_type, success))

    suspicious_source = next(source for source in SOURCES if source["source_ip"] == "77.91.72.10")
    suspect_user = next(user for user in USERS if user["user"] == "alice")
    vpn_host = next(host for host in HOSTS if host["hostname"] == "vpn-gateway-01")
    burst_start = now - timedelta(minutes=18)
    for index in range(8):
        events.append(
            build_event(
                burst_start + timedelta(seconds=index * 35),
                suspect_user,
                suspicious_source,
                vpn_host,
                "login_failed",
                False,
            )
        )

    admin_host = next(host for host in HOSTS if host["hostname"] == "jumpbox-01")
    for user_name, offset in [("bob", 14), ("eve", 6)]:
        matching_user = next(user for user in USERS if user["user"] == user_name)
        events.append(
            build_event(
                now - timedelta(minutes=offset),
                matching_user,
                suspicious_source,
                admin_host,
                "privilege_change",
                True,
            )
        )

    external_source = next(source for source in SOURCES if source["source_ip"] == "45.178.1.92")
    target_user = next(user for user in USERS if user["user"] == "carol")
    mail_host = next(host for host in HOSTS if host["hostname"] == "mail-01")
    reset_time = now - timedelta(minutes=42)
    events.append(build_event(reset_time, target_user, external_source, mail_host, "password_reset", True))
    events.append(
        build_event(
            reset_time + timedelta(minutes=7),
            target_user,
            external_source,
            mail_host,
            "login_success",
            True,
        )
    )

    return sorted(events, key=lambda event: event["timestamp"])


def main() -> None:
    output_path = Path("data/raw_events.jsonl")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    events = generate_events()
    with output_path.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")

    print(f"Generated {len(events)} events at {output_path}")
    print(f"Seed used for reproducibility: {SEED}")


if __name__ == "__main__":
    main()
