# SOC Home Lab

[Read in English](README.md)

Este repositorio hace parte de mi portafolio publico. Lo construyi para practicar un flujo SOC pequeno de punta a punta: generar eventos, detectar comportamiento sospechoso y convertirlo en salidas que se puedan revisar con rapidez durante el triage.

Lo mantuve compacto a proposito. Queria un proyecto que alguien pudiera entender en pocos minutos y que al mismo tiempo sirviera para conversar sobre mi forma de trabajar en una entrevista.

## Que hace este proyecto

1. Genera eventos de seguridad de ejemplo
2. Aplica dos reglas de deteccion
3. Escribe alertas en CSV y Markdown
4. Muestra los resultados en un dashboard sencillo con Streamlit

## Archivos que vale la pena abrir primero

- `src/detect_alerts.py` para ver la logica de deteccion
- `output/alerts_report.md` para ver el reporte generado con la muestra actual
- `src/dashboard.py` para la capa visual de revision
- `data/raw_events.jsonl` para ver la telemetria de ejemplo

## Reglas actuales

- `R001` `high`: varios logins fallidos del mismo usuario y la misma IP dentro de una ventana de 10 minutos
- `R002` `critical`: cambio de privilegios desde una geografia no confiable

## Estructura del repo

```text
soc-home-lab/
|-- data/
|   `-- raw_events.jsonl
|-- evidence/
|   `-- README.md
|-- output/
|   |-- alerts.csv
|   `-- alerts_report.md
|-- src/
|   |-- dashboard.py
|   |-- detect_alerts.py
|   |-- generate_sample_logs.py
|   `-- run_pipeline.py
|-- requirements.txt
|-- README.md
`-- README.es.md
```

## Como ejecutarlo

### macOS o Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_pipeline.py
streamlit run src/dashboard.py
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/run_pipeline.py
streamlit run src/dashboard.py
```

## Por que lo dejo publico

Este repo me sirve para mostrar como pienso un problema de deteccion y triage en un formato pequeno pero facil de revisar. En lugar de solo listar herramientas, enseña un flujo con generacion de datos, logica de alertas, salidas para analista y una capa visual basica.

## Siguientes mejoras

- agregar mapeo MITRE ATT&CK por regla
- agregar allowlists y umbrales adaptativos
- enriquecer alertas con mejor contexto de origen
- sumar mas detecciones como impossible travel y password spray
