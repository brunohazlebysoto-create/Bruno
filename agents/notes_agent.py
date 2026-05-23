"""Notes Agent — generates pediatric surgery notes using Gemini 1.5 Flash."""
import json
import os
from rich.console import Console
from tools.llm import call_llm

console = Console()

SYSTEM = """Eres un cirujano pediatra docente con experiencia en cirugía neonatal y pediátrica.
Redactas apuntes médicos académicos de cirugía infantil en español, con rigor científico,
claridad didáctica y estructura impecable. Incluyes: anatomía quirúrgica, técnica operatoria,
cuidados perioperatorios pediátricos, consideraciones anestésicas, dosificación por peso,
complicaciones y seguimiento a largo plazo. Usas tablas, listas y esquemas cuando corresponde."""

NOTES_PROMPT = """Con base en el siguiente meta-análisis y los artículos analizados,
redacta un APUNTE CLÍNICO COMPLETO DE CIRUGÍA INFANTIL sobre el tema: "{topic}"

META-ANÁLISIS:
{meta_json}

Estructura el apunte con las siguientes secciones en Markdown:

# {topic} — Apunte de Cirugía Infantil

## 1. Introducción y Epidemiología
- Definición y clasificación
- Incidencia, prevalencia y grupos de edad más afectados
- Factores de riesgo (incluyendo factores congénitos y genéticos si aplica)
- Importancia clínica y morbimortalidad

## 2. Embriología y Fisiopatología
- Bases embriológicas/anatómicas relevantes
- Mecanismo fisiopatológico
- Clasificaciones anatómicas o clínicas (tabla si aplica)

## 3. Manifestaciones Clínicas según Grupo Etario
| Edad | Síntomas principales | Signos clave | Presentación típica |
|------|---------------------|--------------|---------------------|
| Neonato | ... | ... | ... |
| Lactante | ... | ... | ... |
| Preescolar | ... | ... | ... |
| Escolar/Adolescente | ... | ... | ... |

## 4. Diagnóstico
### 4.1 Clínico
- Anamnesis y exploración física específica
- Scores y criterios diagnósticos validados en pediatría

### 4.2 Laboratorio
- Estudios básicos y específicos (con valores de referencia pediátricos)

### 4.3 Imagen
- Técnica de elección (preferencia sin radiación en pediatría)
- Hallazgos característicos y criterios diagnósticos por imagen

### 4.4 Diagnóstico Diferencial (tabla)
| Diagnóstico | Características diferenciadores | Estudio clave |
|-------------|--------------------------------|---------------|

## 5. Tratamiento
### 5.1 Preparación Preoperatoria
- Resucitación y estabilización (específica por grupo etario)
- Corrección de desequilibrios metabólicos (con metas numéricas)
- Ayuno preoperatorio (guías pediátricas: regla 6-4-2-1)
- Profilaxis antibiótica (fármaco + dosis mg/kg)

### 5.2 Consideraciones Anestésicas
- Tipo de anestesia preferida y manejo de la vía aérea pediátrica
- Analgesia regional (bloqueos específicos) y fluidoterapia perioperatoria

### 5.3 Técnica Quirúrgica
#### Abordaje preferido (según evidencia)
- Paso a paso de la técnica principal
- Puntos críticos y errores a evitar

#### Técnica alternativa
- Indicaciones específicas y descripción breve

### 5.4 Cuidados Postoperatorios
- Monitorización específica (apnea en prematuros si aplica)
- Manejo del dolor (analgesia multimodal pediátrica con dosis mg/kg)
- Realimentación (esquema progresivo) y criterios de alta

### 5.5 Tratamiento No Quirúrgico
- Indicaciones del manejo conservador y protocolo (dosis pediátricas mg/kg)

## 6. Complicaciones
### 6.1 Intraoperatorias
### 6.2 Postoperatorias Tempranas (< 30 días)
### 6.3 Tardías y Seguimiento a Largo Plazo

## 7. Síntesis de la Evidencia
- Nivel de evidencia global y grado de recomendación
- Técnica quirúrgica recomendada basada en la evidencia
- Áreas de consenso y controversia
- Tabla resumen de estudios clave

## 8. Perlas Clínicas — 10 Puntos Clave

## 9. Referencias Principales

Sé exhaustivo. Usa **negrita** para conceptos clave, tablas Markdown y siempre
especifica dosis en mg/kg. Mínimo 2000 palabras.
"""


class NotesAgent:
    """Generates comprehensive pediatric surgery notes with Gemini."""

    name = "Agente Redactor de Apuntes"
    description = (
        "Cirujano pediatra docente · Técnica quirúrgica paso a paso · "
        "Dosis mg/kg · Cuidados perioperatorios pediátricos"
    )

    def __init__(self, api_key: str = "", provider: str = "gemini", mode: str = "free"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
        self.provider = provider
        self.mode = mode

    def run(self, topic: str, meta: dict, papers: list[dict]) -> str:
        console.print(
            f"\n[bold cyan]📝 {self.name}[/bold cyan] — "
            f"redactando apunte: [italic]{topic}[/italic]\n"
        )
        meta_json = json.dumps(meta, ensure_ascii=False, indent=2)[:8000]
        prompt = NOTES_PROMPT.format(topic=topic, meta_json=meta_json)

        with console.status("  Generando apunte de cirugía infantil..."):
            notes = call_llm(SYSTEM, prompt, self.api_key, max_tokens=8192, temperature=0.4, provider=self.provider, mode=self.mode)

        console.print("  [bold]✓ Apunte generado[/bold]\n")
        return notes
