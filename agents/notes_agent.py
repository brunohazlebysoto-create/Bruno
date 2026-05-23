"""Notes Agent — generates comprehensive structured medical notes."""
import os
import anthropic
from rich.console import Console

console = Console()

SYSTEM = """Eres un médico docente experto en redacción de apuntes médicos académicos.
Escribes en español, con rigor científico, claridad didáctica y estructura impecable.
Incluyes tablas, listas, esquemas y referencias cuando corresponde."""

NOTES_PROMPT = """Con base en el siguiente meta-análisis y los artículos analizados,
redacta un APUNTE MÉDICO COMPLETO Y ACADÉMICO sobre el tema: "{topic}"

META-ANÁLISIS:
{meta_json}

Estructura el apunte con las siguientes secciones en Markdown:

# {topic} — Apunte Clínico Completo

## 1. Introducción y Epidemiología
- Definición, prevalencia, incidencia
- Factores de riesgo
- Importancia clínica

## 2. Fisiopatología
- Mecanismos moleculares/celulares
- Cascada de eventos
- Esquema conceptual (describir)

## 3. Manifestaciones Clínicas
- Síntomas y signos (tabla si aplica)
- Presentaciones típicas y atípicas
- Cronología

## 4. Diagnóstico
- Criterios diagnósticos
- Estudios de laboratorio
- Imágenes y procedimientos
- Diagnóstico diferencial (tabla)

## 5. Tratamiento
### 5.1 Medidas Generales
### 5.2 Tratamiento Farmacológico
- Fármacos de primera línea (con dosis, nivel evidencia)
- Alternativas
- Casos especiales

### 5.3 Tratamiento No Farmacológico

### 5.4 Indicaciones de Derivación / Hospitalización

## 6. Síntesis de la Evidencia (basado en el meta-análisis)
- Hallazgos principales
- Nivel de evidencia global
- Áreas de consenso y controversia
- Tabla resumen de evidencia

## 7. Puntos Clave (10 bullet points para el resumen)

## 8. Referencias Principales
- Lista las fuentes más relevantes del análisis

Sé exhaustivo, usa negrita para conceptos clave, y tablas Markdown donde sea útil.
Mínimo 1500 palabras.
"""


class NotesAgent:
    """Generates comprehensive academic medical notes."""

    name = "Agente Redactor de Apuntes"
    description = (
        "Docente médico experto en elaboración de material educativo. "
        "Redacta apuntes clínicos completos, estructurados y basados en evidencia."
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

        with console.status("  Generando apunte médico completo..."):
            msg = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8096,
                system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
        notes = msg.content[0].text.strip()
        console.print("  [bold]✓ Apunte generado[/bold]\n")
        return notes
