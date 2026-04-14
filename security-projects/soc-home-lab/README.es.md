# SOC Home Lab - Pipeline de Deteccion y Triage

Proyecto de portafolio para demostrar habilidades SOC junior con un flujo practico de deteccion.

## Problema que resuelve

En un SOC no basta con leer logs crudos. Este laboratorio construye un mini pipeline que:

1. genera eventos de seguridad,
2. aplica reglas de deteccion,
3. prioriza alertas,
4. produce evidencia para investigacion.

## Arquitectura

1. Generacion de eventos: src/generate_sample_logs.py
2. Motor de deteccion: src/detect_alerts.py
3. Orquestacion: src/run_pipeline.py
4. Dashboard visual: src/dashboard.py
5. Salidas:
   - data/raw_events.jsonl
   - output/alerts.csv
   - output/alerts_report.md

## Reglas de deteccion (v1)

- R001 (high): rafaga de logins fallidos para mismo usuario + IP.
- R002 (critical): cambio de privilegios desde geografia no confiable.

## Setup

```bash
cd security-projects/soc-home-lab
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar pipeline

```bash
python src/run_pipeline.py
```

## Ejecutar dashboard visual

```bash
streamlit run src/dashboard.py
```

## Capturas que debes incluir en tu portafolio

Toma las capturas en este orden exacto y guardalas en la carpeta `evidence/`:

1. `01_pipeline_success.png` - terminal ejecutando el pipeline correctamente.
2. `02_dashboard_metrics.png` - tarjetas de metricas del dashboard.
3. `03_dashboard_severity.png` - grafico de severidad.
4. `04_dashboard_rules.png` - grafico por reglas.
5. `05_dashboard_table.png` - tabla de alertas con al menos una alerta critical.
6. `06_dashboard_report_preview.png` - vista previa del reporte.

Extras opcionales:
- `07_alerts_csv_preview.png`
- `08_alerts_report_md.png`

## Como explicarlo en entrevista

1. Explica por que cada regla puede representar un riesgo.
2. Explica posibles falsos positivos.
3. Explica mejoras para una version 2.

## Mejoras v2

1. Mapeo MITRE ATT&CK por regla.
2. Whitelist y umbrales adaptativos.
3. Enriquecimiento de contexto por IP.
4. Dashboard de tendencia y tiempo de triage.
