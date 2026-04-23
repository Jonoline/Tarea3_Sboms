# Tarea 3 - SBOMs y Análisis de Vulnerabilidades

Pipeline DevSecOps para generar inventarios de software (SBOMs) y analizar vulnerabilidades en repositorios de GitHub.

## Objetivo

Analizar todos los repositorios de una organización de código abierto, generando:
- **SBOM**: Inventario de paquetes mediante Syft
- **SCA**: Análisis de vulnerabilidades en dependencias mediante Grype
- **SAST**: Análisis de código estático mediante Semgrep
- **Análisis Cuantitativo**: Notebook Jupyter con visualizaciones

## Organización Objetivo

**EbookFoundation** - 38 repositorios (proyectos Python/JS y archivos de texto)

## Estructura del Proyecto

```
Tarea3_Sboms/
├── pipeline/                   # Pipeline de extracción y escaneo
│   ├── src/
│   │   ├── main.py            # Orquestador del pipeline
│   │   ├── scanners.py       # Funciones Syft/Grype/Semgrep
│   │   └── github_client.py # API GitHub y clonador
│   └── data/
│       └── raw/              # JSONs crudos (sbom_*, sca_*, sast_*.json)
├── analysis/
│   ├── SBOM_Analysis.ipynb   # Notebook de análisis
│   └── requirements.txt   # Dependencias
├── docs/
│   └── README.md           # Este archivo
├── Dockerfile             # Imagen del contenedor
└── docker-compose.yml    # Orquestación
```

## Requisitos

- Docker
- Docker Compose
- GitHub Token (con permisos de lectura)

## Uso

### 1. Configurar Token de GitHub

Crear archivo `.env`:
```bash
GITHUB_TOKEN=tu_token_aqui
```

O.exportar variable:
```bash
export GITHUB_TOKEN=tu_token
```

### 2. Ejecutar el Pipeline

```bash
docker-compose up --build
```

Esto clonará los 38 repositorios de EbookFoundation y ejecutará:
- Syft (SBOM)
- Grype (vulnerabilidades)
- Semgrep (código estático)

Los resultados se guardan en `pipeline/data/raw/`.

### 3. Ejecutar el Notebook de Análisis

```bash
cd analysis
jupyter notebook SBOM_Analysis.ipynb
```

O desde Docker:
```bash
docker run --rm -v $(pwd)/../pipeline/data:/app/data -p 8888:8888 sbom-pipeline jupyter notebook --ip=0.0.0.0
```

## Herramientas Utilizadas

| Herramienta | Propósito |
|-------------|-----------|
| Syft        | Generación de SBOM |
| Grype       | Análisis de vulnerabilidades (SCA) |
| Semgrep     | Análisis de código estático (SAST) |
| Pandas     | Análisis de datos |
| Matplotlib | Visualizaciones |

## Notas

- El pipeline usa `--depth 1` para clonar solo el último commit
- Los escaneos se cachean para evitar re-procesamiento
- Límite de tiempo: 3 horas

## Estructura de Datos

### SBOM (sbom_*.json)
```json
{
  "artifacts": [
    {"name": "requests", "version": "2.28.0", "type": "npm", "language": "Python"}
  ]
}
```

### SCA (sca_*.json)
```json
{
  "matches": [
    {"vulnerability": {"id": "CVE-2023-1234", "severity": "High"}, "artifact": {...}}
  ]
}
```

### SAST (sast_*.json)
```json
{
  "results": [
    {"check_id": "python.lang.security.bad-deserialization", "path": "main.py", "line": 42}
  ]
}
```