# 🔪 Sistema Multi-Agente de Investigación en Cirugía Infantil

Pipeline automático que orquesta **5 agentes especializados** para generar desde cero una revisión clínica completa de cualquier tema de cirugía pediátrica: búsqueda bibliográfica con filtros pediátricos, análisis crítico quirúrgico, meta-análisis, apunte de cirugía infantil y presentación PowerPoint académica.

## Arquitectura

```
┌───────────────────────────────────────────────────────────────────────┐
│                    ORQUESTADOR (main.py)                              │
└──────────┬────────────────────────────────────────────────────────────┘
           │
    ┌──────▼──────┐
    │ 1. BUSCADOR │  PubMed (MeSH pediátrico) + Semantic Scholar + CrossRef
    └──────┬──────┘  — búsqueda paralela con filtros: child/infant/neonate/pediatric
           │  N artículos únicos de cirugía infantil
    ┌──────▼──────────┐
    │ 2. ANALIZADOR   │  PICO-S · Grupo etario · Técnica quirúrgica
    └──────┬──────────┘  Anestesia · Complicaciones · Nivel evidencia CEBM
           │  Papers + análisis estructurado pediátrico
    ┌──────▼────────────┐
    │ 3. META-ANALISTA  │  Síntesis quirúrgica · Distribución etaria
    └──────┬────────────┘  Técnicas comparadas · GRADE pediátrico
           │  meta-análisis JSON
    ┌──────▼──────────────┐
    │ 4. REDACTOR APUNTE  │  Técnica quirúrgica paso a paso
    └──────┬──────────────┘  Dosis mg/kg · Cuidados perioperatorios pediátricos
           │
    ┌──────▼───────────┐
    │ 5. PRESENTADOR   │  PowerPoint 18+ slides con tablas etarias,
    └──────────────────┘  técnica quirúrgica, complicaciones, evidencia
```

## Agentes

| Agente | Especialidad | Herramientas |
|--------|-------------|--------------|
| **SearchAgent** | Búsqueda bibliográfica pediátrica | PubMed (MeSH child/infant/neonate) + SS + CrossRef |
| **AnalysisAgent** | Cirujano pediatra / epidemiólogo | Claude + PICO-S + grupo etario + anestesia |
| **MetaAnalysisAgent** | Bioestadístico en cirugía infantil | Claude + distribución etaria + técnicas quirúrgicas |
| **NotesAgent** | Cirujano pediatra docente | Claude 8K — técnica, dosis mg/kg, periop |
| **PPTAgent** | Docente cirugía infantil | Claude + python-pptx — 18+ slides académicos |

## Temas soportados (con papers demo)

| Tema | Demo papers disponibles |
|------|------------------------|
| Apendicitis aguda pediátrica | Laparoscopia vs abierta, NOM antibióticos, scores PAS/AIR, ERAS |
| Invaginación intestinal | Reducción neumática vs hidrostática, enema eco-guiado, cirugía |
| Estenosis hipertrófica del píloro | Piloromiotomía Ramstedt lap vs abierta, umbral bicarbonato, ecografía |
| Enfermedad de Hirschsprung | Pull-through transanal, HAEC, timing neonatal |
| Hernia inguinal pediátrica | PIRS vs herniotomía abierta, prematuros, timing |
| Atresia esofágica | Toracoscopia vs toracotomía, long-gap EA, Foker |
| Gastrosquisis / Onfalocele | Cierre primario vs silo, gastrosquisis compleja |
| Criptorquidia | Orquiopexia: timing, fertilidad, riesgo neoplásico |
| Malrotación / Vólvulo | Procedimiento de Ladd laparoscópico vs abierto |
| Estenosis ureteropélvica | Pieloplastia robótica vs laparoscópica |
| Colecistitis/Colelitiasis | Colecistectomía laparoscópica pediátrica |
| **Cualquier otro tema** | Busca en PubMed/SS/CrossRef en tiempo real |

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

# Temas frecuentes en cirugía infantil
python main.py "apendicitis aguda laparoscopia pediátrica"
python main.py "invaginación intestinal reducción neumática"
python main.py "estenosis hipertrófica del píloro piloromiotomía"
python main.py "enfermedad de Hirschsprung pull-through"
python main.py "hernia inguinal lactantes reparación laparoscópica"
python main.py "atresia esofágica reparación toracoscópica"
python main.py "gastrosquisis cierre primario versus silo"
python main.py "malrotación intestinal procedimiento de Ladd"
python main.py "criptorquidia orquiopexia timing"

# Con opciones
python main.py \
  --topic "obstrucción intestinal neonatal" \
  --max-papers 30 \
  --output ./clases \
  --pubmed-key "TU_NCBI_KEY"

# Solo apunte, sin PowerPoint
python main.py "onfalocele tratamiento quirúrgico" --no-ppt
```

## Salidas generadas

```
output/apendicitis_aguda_20241201_143022/
├── 01_papers_raw.json          # Artículos de PubMed/SS/CrossRef con filtros pediátricos
├── 02_papers_analyzed.json     # Análisis: grupo etario, técnica, complicaciones, PICO-S
├── 03_meta_analysis.json       # Meta-análisis: dist. etaria, técnicas, GRADE pediátrico
├── 04_apunte_medico.md         # Apunte completo: técnica quirúrgica, dosis mg/kg, periop
└── 05_presentacion.pptx        # Clase PowerPoint 18+ slides con tablas etarias
```

## Variables de entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `ANTHROPIC_API_KEY` | Clave API de Anthropic (Claude) | ✅ Sí |
| `PUBMED_API_KEY` | NCBI API key (10 req/s vs 3/s) | No |
| `SS_API_KEY` | Semantic Scholar API key | No |

## Particularidades del análisis pediátrico

El sistema está optimizado para cirugía infantil:

- **Búsqueda**: MeSH terms `infant`, `child`, `adolescent`, `newborn` + filtros quirúrgicos
- **Análisis**: Grupo etario, anestesia pediátrica, consideraciones neonatales
- **Meta-análisis**: Distribución etaria, técnicas laparoscópicas vs abiertas
- **Apunte**: Manifestaciones por edad, dosis mg/kg, ayuno 6-4-2-1, bloqueos regionales
- **PowerPoint**: Tabla clínica por grupo etario, técnica quirúrgica paso a paso
