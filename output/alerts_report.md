# SOC Alerts Report

Generated at: 2026-04-16T03:14:13.223726+00:00

## Summary
- Total events analyzed: 332
- Total alerts generated: 5
- Event distribution: {'login_success': 187, 'file_access': 53, 'login_failed': 53, 'privilege_change': 12, 'password_reset': 27}
- Severity distribution: {'high': 3, 'critical': 2}
- Status distribution: {'closed': 4, 'investigating': 1}
- Rule distribution: {'R003': 2, 'R002': 2, 'R001': 1}

## Alerts
### R003 | HIGH | user=carol | status=closed
- Source IP: 45.178.1.92 (US)
- Hostname: mail-01 | Asset criticality: high
- MITRE ATT&CK: Initial Access / Defense Evasion / T1078 Valid Accounts
- First seen: 2026-04-15T23:23:00+00:00
- Last seen: 2026-04-15T23:33:00+00:00
- Assigned to: Tier1 SOC
- Triage minutes: 24
- Resolution minutes: 240
- SLA breached: no
- Details: Password reset was followed by a successful login from a non-trusted geography within 15 minutes

### R003 | HIGH | user=carol | status=investigating
- Source IP: 45.178.1.92 (US)
- Hostname: mail-01 | Asset criticality: high
- MITRE ATT&CK: Initial Access / Defense Evasion / T1078 Valid Accounts
- First seen: 2026-04-16T02:30:00+00:00
- Last seen: 2026-04-16T02:37:00+00:00
- Assigned to: Threat Hunter
- Triage minutes: 30
- Resolution minutes: pending
- SLA breached: no
- Details: Password reset was followed by a successful login from a non-trusted geography within 15 minutes

### R002 | CRITICAL | user=bob | status=closed
- Source IP: 77.91.72.10 (RU)
- Hostname: jumpbox-01 | Asset criticality: critical
- MITRE ATT&CK: Persistence / Privilege Escalation / T1098 Account Manipulation
- First seen: 2026-04-16T02:58:00+00:00
- Last seen: 2026-04-16T02:58:00+00:00
- Assigned to: Tier2 SOC
- Triage minutes: 25
- Resolution minutes: 185
- SLA breached: yes
- Details: Privilege change detected from a non-trusted geography

### R001 | HIGH | user=alice | status=closed
- Source IP: 77.91.72.10 (RU)
- Hostname: vpn-gateway-01 | Asset criticality: high
- MITRE ATT&CK: Credential Access / T1110 Brute Force
- First seen: 2026-04-16T02:54:00+00:00
- Last seen: 2026-04-16T02:58:05+00:00
- Assigned to: Threat Hunter
- Triage minutes: 42
- Resolution minutes: 240
- SLA breached: yes
- Details: 8 failed logins from the same IP in <= 10 minutes

### R002 | CRITICAL | user=eve | status=closed
- Source IP: 77.91.72.10 (RU)
- Hostname: jumpbox-01 | Asset criticality: critical
- MITRE ATT&CK: Persistence / Privilege Escalation / T1098 Account Manipulation
- First seen: 2026-04-16T03:06:00+00:00
- Last seen: 2026-04-16T03:06:00+00:00
- Assigned to: Tier2 SOC
- Triage minutes: 13
- Resolution minutes: 160
- SLA breached: yes
- Details: Privilege change detected from a non-trusted geography
