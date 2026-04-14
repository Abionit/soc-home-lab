from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EVENT_TYPES = [
    "login_success",
    "login_failed",
    "password_reset",
    "privilege_change",
    "file_access",
]

USERS = [
    "alice",
    "bob",
    "carol",
    "dave",
    "eve",
]

SOURCE_IPS = [
    "181.49.10.12",
    "45.227.80.3",
    "190.145.200.18",
    "10.0.2.15",
    "192.168.1.22",
    "77.91.72.10",
]

GEO = {
    "181.49.10.12": "CO",
    "45.227.80.3": "CO",
    "190.145.200.18": "CO",
    "10.0.2.15": "INTERNAL",
    "192.168.1.22": "INTERNAL",
    "77.91.72.10": "RU",
}


def build_event(ts: datetime, user: str, source_ip: str, event_type: str, success: bool) -> dict:
    return {
        "timestamp": ts.isoformat(),
        "user": user,
        "source_ip": source_ip,
        "geo": GEO.get(source_ip, "UNKNOWN"),
        "event_type": event_type,
        "success": success,
    }


def generate_events(total: int = 250) -> list[dict]:
    now = datetime.now(timezone.utc)
    events: list[dict] = []

    for idx in range(total):
        ts = now - timedelta(minutes=total - idx)
        user = random.choice(USERS)
        source_ip = random.choice(SOURCE_IPS)

        if random.random() < 0.65:
            event_type = "login_success"
            success = True
        else:
            event_type = random.choice(EVENT_TYPES)
            success = event_type != "login_failed"

        events.append(build_event(ts, user, source_ip, event_type, success))

    # Inject suspicious behavior for rule validation.
    suspicious_ip = "77.91.72.10"
    suspect_user = "alice"
    burst_start = now - timedelta(minutes=5)
    for i in range(8):
        events.append(
            build_event(
                burst_start + timedelta(seconds=i * 20),
                suspect_user,
                suspicious_ip,
                "login_failed",
                False,
            )
        )

    events.append(
        build_event(
            now - timedelta(minutes=2),
            "bob",
            "77.91.72.10",
            "privilege_change",
            True,
        )
    )

    return sorted(events, key=lambda x: x["timestamp"])


def main() -> None:
    output_path = ROOT / "data" / "raw_events.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    events = generate_events()
    with output_path.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")

    print(f"Generated {len(events)} events at {output_path}")


if __name__ == "__main__":
    main()
