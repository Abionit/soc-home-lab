# Detection Catalog

| Rule ID | Detection | Severity | Log Source | MITRE | Analyst Notes |
| --- | --- | --- | --- | --- | --- |
| 100100 | SSH brute force | High | Linux auth/syslog | T1110 | Review source IP, target account, failed count, and geo context. |
| 100110 | RDP brute force | High | Windows Security | T1110 | Review target host, user, source IP, and prior successful logons. |
| 100120 | Suspicious encoded PowerShell | Critical | Windows Sysmon/PowerShell | T1059.001 | Review command line, parent process, user, and script origin. |
| 100130 | Local administrator account created | High | Windows Security | T1136.001 | Confirm whether the account creation was approved. |
| 100140 | Sensitive file modified | Medium | File Integrity Monitoring | T1565.001 | Review file path, user, process, and change window. |
| 100150 | Malware test artifact observed | High | Endpoint security | T1204 | Validate whether this was a controlled test or an actual suspicious file. |
| 100160 | Web path traversal attempt | High | Web access logs | T1190 | Review requested URI, source IP, user agent, and response code. |
| 100170 | Suspicious sudo escalation | High | Linux auth/syslog | T1548 | Review user, command, host, and business justification. |
| 100180 | Credential access tool indicator | Critical | Endpoint/Sysmon | T1003 | Treat as high priority; review process tree and host containment needs. |

## Detection Philosophy

The detections are intentionally practical:

- simple enough to validate in a lab
- mapped to realistic SOC scenarios
- connected to triage questions
- useful for security analytics reporting
