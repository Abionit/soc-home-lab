# Runbook

## Prerequisites

The Wazuh Docker single-node stack requires:

- Docker Desktop or Docker Engine
- Docker Compose
- 4 CPU cores
- 8 GB RAM minimum
- 50 GB available disk space

Official reference: https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html

## Start Docker

On Windows, open Docker Desktop and wait until the Docker engine is running.

Validate:

```bash
docker ps
docker compose version
```

## Prepare Wazuh Docker

Use the helper script:

```powershell
.\scripts\setup_wazuh_docker.ps1
```

The script downloads the official Wazuh Docker deployment archive if it is not already present.

## Deploy Wazuh Single Node

From the downloaded Wazuh Docker `single-node` directory:

```bash
docker compose -f generate-indexer-certs.yml run --rm generator
docker compose up -d
```

Expected exposed services:

| Port | Service |
| --- | --- |
| 443 | Wazuh dashboard |
| 1514 | Wazuh agent events |
| 1515 | Wazuh agent enrollment |
| 514/udp | Syslog input |
| 55000 | Wazuh API |
| 9200 | Wazuh indexer API |

## Add Custom Rules

Copy the custom rules into the Wazuh manager container:

```bash
docker cp config/wazuh/rules/local_soc_rules.xml single-node-wazuh.manager-1:/var/ossec/etc/rules/local_soc_rules.xml
docker restart single-node-wazuh.manager-1
```

If the container name differs, list containers first:

```bash
docker ps
```

## Generate Test Events

Create representative local events:

```bash
python scripts/generate_lab_events.py
```

Send events to the Wazuh syslog listener:

```powershell
.\scripts\send_syslog_events.ps1 -InputFile .\output\generated_lab_events.log -Server 127.0.0.1 -Port 514
```

## Build Reports

```bash
python scripts/build_alert_analytics.py
```

Generated outputs:

- `output/alert_metrics.csv`
- `output/detection_summary.csv`
- `output/triage_queue.csv`
- `output/executive_report.md`
- `output/wazuh_soc_lab.db`

## Review Checklist

- Confirm Wazuh dashboard is reachable.
- Confirm custom rules are loaded.
- Confirm lab events are generated.
- Confirm alerts appear in Wazuh.
- Confirm analytics reports are generated.
- Capture evidence in the `evidence/` folder if using the project in a portfolio.
