"""Notes Agent — generates comprehensive pediatric surgery clinical notes."""
import os
import anthropic
from rich.console import Console

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
- Anamnesis (preguntar a los padres: duración, síntomas asociados)
- Exploración física específica
- Scores y criterios diagnósticos validados en pediatría

### 4.2 Laboratorio
- Estudios básicos y específicos (con valores de referencia pediátricos)
- Marcadores relevantes

### 4.3 Imagen
- Técnica de elección (justificar preferencia sin radiación en pediatría)
- Hallazgos característicos
- Criterios diagnósticos por imagen

### 4.4 Diagnóstico Diferencial (tabla)
| Diagnóstico | Características diferenciadores | Estudio clave |
|-------------|--------------------------------|---------------|

## 5. Tratamiento
### 5.1 Preparación Preoperatoria
- Resucitación y estabilización (específica por grupo etario)
- Corrección de desequilibrios metabólicos (con metas numéricas)
- Ayuno preoperatorio (guías pediátricas actuales: regla 6-4-2-1)
- Profilaxis antibiótica (fármaco + dosis mg/kg)

### 5.2 Consideraciones Anestésicas
- Tipo de anestesia preferida
- Premedicación y técnicas de inducción en niños
- Manejo de la vía aérea pediátrica
- Analgesia regional (bloqueos específicos)
- Temperatura y fluidoterapia perioperatoria

### 5.3 Técnica Quirúrgica
#### Abordaje preferido (según evidencia)
- Paso a paso de la técnica principal
- Variantes técnicas y cuándo usarlas
- Puntos críticos y errores a evitar

#### Técnica alternativa
- Indicaciones específicas
- Descripción breve

### 5.4 Cuidados Postoperatorios
- Monitorización específica (incluir apnea en prematuros si aplica)
- Manejo del dolor (analgesia multimodal pediátrica con dosis)
- Realimentación (esquema progresivo)
- Criterios de alta

### 5.5 Tratamiento No Quirúrgico
- Indicaciones del manejo conservador (si existe)
- Protocolo y fármacos (con dosis pediátricas mg/kg)

## 6. Complicaciones
### 6.1 Intraoperatorias
### 6.2 Postoperatorias Tempranas (< 30 días)
### 6.3 Tardías y Seguimiento a Largo Plazo
- Impacto en crecimiento y desarrollo
- Calidad de vida

## 7. Síntesis de la Evidencia (basado en el meta-análisis)
- Nivel de evidencia global y grado de recomendación
- Técnica quirúrgica recomendada con base en la evidencia
- Áreas de consenso y controversia en cirugía infantil
- Tabla resumen de estudios clave

## 8. Perlas Clínicas y Puntos Clave
> 10 bullet points esenciales para el cirujano pediatra

## 9. Referencias Principales
- Lista las fuentes más relevantes del análisis con año y revista

Sé exhaustivo y didáctico. Usa **negrita** para conceptos clave, tablas Markdown donde sea útil,
y siempre especifica dosis en mg/kg para medicamentos pediátricos.
Mínimo 2000 palabras.
"""


class NotesAgent:
    """Generates comprehensive pediatric surgery clinical notes."""

    name = "Agente Redactor de Apuntes"
    description = (
        "Cirujano pediatra docente experto en elaboración de apuntes quirúrgicos pediátricos. "
        "Redacta apuntes clínicos completos con técnica quirúrgica, "
        "cuidados perioperatorios y dosificación pediátrica."
    )

    def __init__(self, api_key: str = ""):
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        )

    def run(self, topic: str, meta: dict, papers: list[dict]) -> str:
        import json
        console.print(
            f"\n[bold cyan]📝 {self.name}[/bold cyan] — redactando apunte sobre: [italic]{topic}[/italic]\n"
        )
        meta_json = json.dumps(meta, ensure_ascii=False, indent=2)[:8000]
        prompt = NOTES_PROMPT.format(topic=topic, meta_json=meta_json)

        with console.status("  Generando apunte de cirugía infantil..."):
            msg = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8096,
                system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
        notes = msg.content[0].text.strip()
        console.print("  [bold]✓ Apunte generado[/bold]\n")
        return notes
