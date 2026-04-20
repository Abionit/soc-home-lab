# SOC Home Lab v2 - Pipeline de Deteccion, Analitica y Triage

Proyecto practico para demostrar habilidades SOC con un flujo reproducible de deteccion, analitica SQL y visualizacion operativa.

## Problema que resuelve

En un SOC no basta con leer logs crudos. Un analista tambien necesita contexto, priorizacion y metricas operativas para saber que investigar primero y como comunicar el estado del trabajo.

Este laboratorio construye un mini pipeline que:

1. genera telemetria de seguridad,
2. aplica reglas de deteccion,
3. enriquece las alertas con contexto de triage,
4. exporta metricas reutilizables en SQL,
5. presenta resultados en un dashboard operativo.

## Habilidades que demuestra

- Python para procesamiento y orquestacion
- Deteccion basada en reglas
- SQL con SQLite para reporting
- Dashboarding con Streamlit
- Analitica operativa: backlog, SLA, tiempo de triage y tiempo de resolucion
- Documentacion tecnica y salidas revisables

## Documentacion y Referencias

- Version en ingles: [README.en.md](README.en.md)
- Guia de versiones: [CHANGELOG.md](CHANGELOG.md)
- Indice de evidencias: [evidence/v2/README.md](evidence/v2/README.md)
- Logica de deteccion: [src/detect_alerts.py](src/detect_alerts.py)
- Consultas SQL del portafolio: [sql/portfolio_queries.sql](sql/portfolio_queries.sql)
- Reporte de ejemplo: [output/alerts_report.md](output/alerts_report.md)

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

## Resumen de Versiones

- `v1` estaba orientada a una demo compacta de deteccion y dashboard con dos reglas y salidas basicas.
- `v2` agrega telemetria enriquecida, una tercera regla, capa SQL, exportacion de KPIs, mejor dashboard y documentacion mas completa.

## Setup

```bash
python -m venv .venv
```

Activa el entorno virtual:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instala dependencias:

```bash
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

## Vistas de Referencia

La version actual incluye referencias visuales y exportaciones indexadas en [evidence/v2/README.md](evidence/v2/README.md), entre ellas:

1. ejecucion del pipeline
2. tarjetas KPI del dashboard
3. tendencia y distribucion por severidad
4. distribucion por estado y por regla
5. tabla enriquecida de alertas
6. vista previa del reporte SQL

## Temas de Discusion Tecnica

1. por que cada regla puede representar riesgo real
2. que alertas podrian ser falsos positivos y como afinarlas
3. como las metricas de triage ayudan a medir carga operativa
4. por que SQL tambien aporta valor dentro de un SOC