from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from src.detect_alerts import detect_failed_login_burst


class DetectAlertsTests(unittest.TestCase):
    def test_failed_login_burst_uses_best_window_instead_of_full_history(self) -> None:
        base_time = datetime(2026, 4, 15, 12, 0, tzinfo=timezone.utc)
        template = {
            "user": "alice",
            "department": "Finance",
            "source_ip": "77.91.72.10",
            "geo": "RU",
            "hostname": "vpn-gateway-01",
            "asset_group": "identity",
            "asset_criticality": "high",
            "log_source": "vpn",
            "event_type": "login_failed",
        }

        events = []
        for minutes in [0, 1, 2]:
            events.append({**template, "timestamp": base_time + timedelta(minutes=minutes)})
        for minutes in [30, 31, 32, 33, 34]:
            events.append({**template, "timestamp": base_time + timedelta(minutes=minutes)})

        alerts = detect_failed_login_burst(events, window_minutes=10, threshold=5)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].first_seen, (base_time + timedelta(minutes=30)).isoformat())
        self.assertEqual(alerts[0].last_seen, (base_time + timedelta(minutes=34)).isoformat())


if __name__ == "__main__":
    unittest.main()
