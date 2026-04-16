# SOC Home Lab - Pipeline de Deteccion, Analitica y Triage

Proyecto de portafolio para demostrar habilidades SOC con un flujo reproducible de deteccion, analitica SQL y visualizacion operativa.

## Problema que resuelve

En un SOC no basta con leer logs crudos. Un analista tambien necesita contexto, priorizacion y metricas operativas para saber que investigar primero y como comunicar el estado del trabajo.

Este laboratorio construye un mini pipeline que:

1. genera telemetria de seguridad,
2. aplica reglas de deteccion,
3. enriquece las alertas con contexto de triage,
4. exporta metricas reutilizables en SQL,
5. presenta resultados en un dashboard listo para portafolio.

## Habilidades que demuestra

- Python para procesamiento y orquestacion
- Deteccion basada en reglas
- SQL con SQLite para reporting
- Dashboarding con Streamlit
- Analitica operativa: backlog, SLA, tiempo de triage y tiempo de resolucion
- Documentacion tecnica para GitHub e entrevistas

## Arquitectura

1. Generacion de eventos: `src/generate_sample_logs.py`
2. Motor de deteccion: `src/detect_alerts.py`
3. Capa analitica SQL: `src/build_analytics.py`
4. Orquestacion: `src/run_pipeline.py`
5. Dashboard visual: `src/dashboard.py`
6. Salidas:
   - `data/raw_events.jsonl`
   - `output/alerts.csv`
   - `output/alerts_report.md`
   - `output/alert_kpis.csv`
   - `output/alert_trend.csv`
   - `output/rule_summary.csv`
   - `analytics/soc_home_lab.db`
   - `sql/portfolio_queries.sql`

## Reglas de deteccion (v2)

- `R001` (`high`): rafaga de logins fallidos desde la misma IP hacia el mismo usuario en una ventana de 10 minutos
- `R002` (`critical`): cambio de privilegios desde una geografia no confiable
- `R003` (`high`): password reset seguido por login exitoso desde una geografia no confiable

Cada alerta ahora incluye:

- contexto tipo MITRE ATT&CK
- metadata del host y fuente de logs
- analista o equipo asignado
- estado de la alerta
- tiempo de triage y de resolucion
- bandera de incumplimiento de SLA

## Setup

```bash
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
python -m streamlit run src/dashboard.py
```

## Ejecutar prueba de regresion

```bash
python -m unittest discover -s tests
```

## Por que esta capa SQL suma valor

Muchos puestos asociados piden mas que solo revisar alertas. Tambien esperan manejo de metricas, reporting y consultas reutilizables. Por eso este proyecto incluye:

- una base SQLite local
- exportacion de KPIs en CSV
- consultas reutilizables en `sql/portfolio_queries.sql`

Eso hace que el repositorio funcione bien tanto para roles SOC como para perfiles de analitica orientados a operaciones y seguridad.

## Capturas que debes incluir en tu portafolio

1. Ejecucion exitosa del pipeline en terminal
2. Tarjetas KPI del dashboard
3. Tendencia de alertas y distribucion por severidad
4. Distribucion por estado y por regla
5. Tabla enriquecida de alertas
6. Fragmento SQL y vista previa del reporte

## Como explicarlo en entrevista

1. Explica por que cada regla puede representar riesgo real
2. Explica que alertas podrian ser falsos positivos y como afinarlas
3. Explica como las metricas de triage ayudan a medir carga operativa
4. Explica por que SQL tambien aporta valor dentro de un SOC
