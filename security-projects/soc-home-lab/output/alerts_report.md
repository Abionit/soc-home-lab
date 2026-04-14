# SOC Alerts Report

Generated at: 2026-04-14T17:51:39.461562+00:00

## Summary
- Total events analyzed: 259
- Total alerts generated: 5
- Event distribution: {'login_success': 178, 'file_access': 14, 'password_reset': 26, 'login_failed': 23, 'privilege_change': 18}
- Severity distribution: {'high': 1, 'critical': 4}

## Alerts
### R001 | HIGH | user=alice
- Source IP: 77.91.72.10
- First seen: 2026-04-14T16:21:39.037912+00:00
- Last seen: 2026-04-14T17:48:59.037912+00:00
- Details: 8 failed logins in <= 10 minutes

### R002 | CRITICAL | user=alice
- Source IP: 77.91.72.10
- First seen: 2026-04-14T14:13:39.037912+00:00
- Last seen: 2026-04-14T14:13:39.037912+00:00
- Details: Privilege change detected from external geography

### R002 | CRITICAL | user=bob
- Source IP: 77.91.72.10
- First seen: 2026-04-14T15:51:39.037912+00:00
- Last seen: 2026-04-14T15:51:39.037912+00:00
- Details: Privilege change detected from external geography

### R002 | CRITICAL | user=eve
- Source IP: 77.91.72.10
- First seen: 2026-04-14T16:30:39.037912+00:00
- Last seen: 2026-04-14T16:30:39.037912+00:00
- Details: Privilege change detected from external geography

### R002 | CRITICAL | user=bob
- Source IP: 77.91.72.10
- First seen: 2026-04-14T17:49:39.037912+00:00
- Last seen: 2026-04-14T17:49:39.037912+00:00
- Details: Privilege change detected from external geography
