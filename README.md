# 🏥 Sistema Multi-Agente de Investigación Médica

Pipeline automático que orquesta **5 agentes especializados** para generar desde cero una revisión médica completa: búsqueda en bases de datos, análisis crítico, meta-análisis, apunte clínico y presentación PowerPoint.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                     ORQUESTADOR (main.py)                       │
└──────────┬──────────────────────────────────────────────────────┘
           │
    ┌──────▼──────┐
    │ 1. BUSCADOR │  PubMed + Semantic Scholar + CrossRef (paralelo)
    └──────┬──────┘
           │  N artículos únicos
    ┌──────▼──────────┐
    │ 2. ANALIZADOR   │  PICO · Nivel evidencia · Calidad metodológica
    └──────┬──────────┘  (Claude por cada paper)
           │  Papers + análisis estructurado
    ┌──────▼────────────┐
    │ 3. META-ANALISTA  │  Síntesis · GRADE · Consenso · Gaps
    └──────┬────────────┘  (Claude, visión global)
           │  meta-análisis JSON
    ┌──────▼──────────────┐
    │ 4. REDACTOR APUNTE  │  Apunte clínico completo en Markdown
    └──────┬──────────────┘  (Claude, ~2000 palabras)
           │
    ┌──────▼───────────┐
    │ 5. PRESENTADOR   │  PowerPoint académico (15+ slides)
    └──────────────────┘  (Claude + python-pptx)
```

## Agentes

| Agente | Rol | Herramientas |
|--------|-----|--------------|
| **SearchAgent** | Búsqueda bibliográfica paralela | PubMed API, Semantic Scholar, CrossRef |
| **AnalysisAgent** | Análisis crítico individual | Claude + criterios CEBM/GRADE |
| **MetaAnalysisAgent** | Síntesis de evidencia | Claude + bioestadística narrativa |
| **NotesAgent** | Redacción de apunte médico | Claude (8K tokens) |
| **PPTAgent** | Presentación PowerPoint | Claude + python-pptx |

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
# Forma básica
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py "diabetes tipo 2 tratamiento farmacológico"

# Con opciones
python main.py \
  --topic "hipertensión arterial" \
  --max-papers 30 \
  --output ./resultados \
  --pubmed-key "TU_NCBI_KEY"   # opcional, aumenta límite de velocidad

# Solo apunte, sin PowerPoint
python main.py "sepsis tratamiento" --no-ppt
```

## Salidas generadas

```
output/diabetes_tipo_2_20241201_143022/
├── 01_papers_raw.json          # Artículos crudos de todas las bases de datos
├── 02_papers_analyzed.json     # Artículos + análisis estructurado por Claude
├── 03_meta_analysis.json       # Meta-análisis completo con GRADE
├── 04_apunte_medico.md         # Apunte clínico completo (~2000 palabras)
└── 05_presentacion.pptx        # Presentación PowerPoint profesional
```

## Variables de entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `ANTHROPIC_API_KEY` | Clave API de Anthropic | ✅ Sí |
| `PUBMED_API_KEY` | NCBI API key (10 req/s vs 3/s) | No |
| `SS_API_KEY` | Semantic Scholar API key | No |

## Bases de datos consultadas

- **PubMed/MEDLINE** — mayor base biomédica mundial (NCBI)
- **Semantic Scholar** — AI-powered academic search (Allen Institute)
- **CrossRef** — metadatos de 150M+ publicaciones científicas

## Criterios de análisis

- **Nivel de evidencia**: Oxford CEBM (1a–5)
- **Grado de recomendación**: A–D
- **Sesgo**: bajo / moderado / alto
- **PICO**: Población, Intervención, Comparador, Outcome
- **Calidad**: escala 1–5

## Diseño de la presentación

Tema visual médico profesional con:
- Paleta navy/azul/cyan
- Slides de título, objetivos, contenido, tablas, evidencia, conclusiones
- Tipografía académica limpia
