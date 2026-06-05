# SOC Home Lab v2 - Pipeline de Deteccion, Analitica y Triage

Flujo reproducible para deteccion, enriquecimiento de alertas, reporting SQL y monitoreo operativo de seguridad.

## Problema

Un SOC necesita mas que logs crudos. Requiere un proceso repetible para ingerir telemetria, detectar actividad sospechosa, agregar contexto de triage, medir carga operativa y comunicar el estado de las alertas.

## Arquitectura

1. Generacion de eventos: `src/generate_sample_logs.py`
2. Motor de deteccion: `src/detect_alerts.py`
3. Construccion analitica: `src/build_analytics.py`
4. Orquestacion: `src/run_pipeline.py`
5. Dashboard operativo: `src/dashboard.py`
6. Reporting en SQLite y CSV

## Reglas de Deteccion

- `R001` high: rafaga de intentos fallidos desde la misma IP al mismo usuario
- `R002` critical: cambio de privilegios desde una geografia no confiable
- `R003` high: restablecimiento de clave seguido por login desde una geografia no confiable

Cada alerta incluye contexto tipo ATT&CK, metadata del activo y fuente, ownership, estado, tiempo de triage, tiempo de resolucion y bandera SLA.

## Salidas Operativas

- cola de alertas enriquecidas
- KPI de alertas y severidad
- metricas de backlog activo
- tiempos de triage y resolucion
- resumen de rendimiento por regla
- consultas SQL reutilizables
- dashboard operacional en Streamlit

## Ejecucion

```bash
python -m venv .venv
pip install -r requirements.txt
python src/run_pipeline.py
python -m unittest discover -s tests
python -m streamlit run src/dashboard.py
```

## Referencias

- English: [README.en.md](README.en.md)
- Evidencia: [evidence/v2/README.md](evidence/v2/README.md)
- Logica de deteccion: [src/detect_alerts.py](src/detect_alerts.py)
- SQL: [sql/portfolio_queries.sql](sql/portfolio_queries.sql)
- Reporte: [output/alerts_report.md](output/alerts_report.md)
