# Wazuh SOC Detection Engineering Report

Generated from representative lab alert data.

## Executive Summary

- Total alerts reviewed: 9
- Critical alerts: 2
- High severity alerts: 6
- Active alerts requiring review: 4
- Average triage time: 20.0 minutes
- Average resolution time: 127.2 minutes
- Unique hosts involved: 9
- MITRE techniques represented: 8

## Highest Priority Alert

- Detection: credential_access_indicator
- Severity: critical
- Host: win-admin-01
- User: admin
- Source IP: 10.10.60.12
- MITRE: T1003
- Recommended action: contain

## Most Active Detection

- Rule ID: 100120
- Detection: suspicious_powershell_encoded
- Severity: critical
- Alert count: 1
- MITRE: T1059.001

## Analyst Notes

The lab demonstrates how Wazuh detections can be converted into structured SOC reporting. The analytics layer supports alert prioritization, severity review, MITRE coverage, and operational metrics that can be discussed in technical interviews.
