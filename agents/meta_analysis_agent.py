"""Meta-analysis Agent — synthesizes evidence across papers using Claude."""
import json
import os
import anthropic
from rich.console import Console

console = Console()

SYSTEM = """Eres un bioestadístico y epidemiólogo clínico con expertise en meta-análisis.
Realizas síntesis cuantitativa y cualitativa de la evidencia científica.
Responde siempre en español con formato JSON válido y riguroso."""

META_PROMPT = """Realiza un meta-análisis narrativo y cuantitativo de los siguientes artículos analizados.
Devuelve SOLO un JSON con esta estructura exacta:

{{
  "pregunta_clinica": "<pregunta PICO derivada del conjunto de evidencia>",
  "total_estudios": <número>,
  "total_pacientes_estimado": <número o null>,
  "distribucion_tipos": {{
    "RCT": <n>,
    "Cohorte": <n>,
    "Revision_Sistematica": <n>,
    "Meta_analisis": <n>,
    "Otros": <n>
  }},
  "nivel_evidencia_global": "<1a | 1b | 2a | 2b | 3 | 4 | 5>",
  "grado_recomendacion_global": "<A | B | C | D>",
  "heterogeneidad": "<baja | moderada | alta | no evaluable>",
  "sesgo_publicacion": "<probable | improbable | no evaluable>",
  "hallazgos_principales": [
    {{"hallazgo": "<descripción>", "nivel_evidencia": "<nivel>", "consenso": "<alto|moderado|bajo>"}},
    {{"hallazgo": "<descripción>", "nivel_evidencia": "<nivel>", "consenso": "<alto|moderado|bajo>"}}
  ],
  "areas_controversia": ["<área 1>", "<área 2>"],
  "areas_consenso": ["<área 1>", "<área 2>"],
  "gaps_conocimiento": ["<gap 1>", "<gap 2>"],
  "implicaciones_clinicas": ["<implicación 1>", "<implicación 2>", "<implicación 3>"],
  "implicaciones_investigacion": ["<línea futura 1>", "<línea futura 2>"],
  "conclusion_sintetica": "<conclusión global en 3-5 oraciones>",
  "resumen_ejecutivo": "<párrafo ejecutivo de 100-150 palabras para clínicos>",
  "tabla_evidencia": [
    {{
      "referencia": "<Autor et al., Año>",
      "tipo": "<tipo estudio>",
      "n": <n o null>,
      "resultado_clave": "<resultado>",
      "nivel_evidencia": "<nivel>",
      "calidad": <1-5>
    }}
  ]
}}

ARTÍCULOS ANALIZADOS:
{articles_json}

TEMA: {topic}
"""


class MetaAnalysisAgent:
    """Synthesizes evidence across all analyzed papers."""

    name = "Agente Meta-Analista"
    description = (
        "Bioestadístico clínico experto en síntesis de evidencia. "
        "Evalúa heterogeneidad, sesgos y produce conclusiones GRADE."
    )

    def __init__(self, api_key: str = ""):
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        )

    def _summarize_for_prompt(self, papers: list[dict]) -> str:
        summaries = []
        for p in papers:
            a = p.get("analysis", {})
            summaries.append({
                "titulo": a.get("titulo_resumido", p.get("title", "")[:60]),
                "autores": p.get("authors", [])[:3],
                "año": p.get("year", ""),
                "tipo_estudio": a.get("tipo_estudio", ""),
                "nivel_evidencia": a.get("nivel_evidencia", ""),
                "n_muestra": a.get("n_muestra"),
                "resultado_clave": a.get("resultado_clave", ""),
                "conclusion": a.get("conclusion_autores", ""),
                "calidad_metodologica": a.get("calidad_metodologica", 0),
                "sesgo_riesgo": a.get("sesgo_riesgo", ""),
                "relevancia_clinica": a.get("relevancia_clinica", 0),
            })
        return json.dumps(summaries, ensure_ascii=False, indent=2)

    def run(self, papers: list[dict], topic: str) -> dict:
        console.print(
            f"\n[bold cyan]📊 {self.name}[/bold cyan] — sintetizando {len(papers)} artículos\n"
        )
        articles_json = self._summarize_for_prompt(papers)
        prompt = META_PROMPT.format(articles_json=articles_json, topic=topic)

        try:
            msg = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            text = msg.content[0].text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            meta = json.loads(text)
        except Exception as e:
            console.print(f"  [red]Error en meta-análisis:[/red] {e}")
            meta = {"error": str(e), "conclusion_sintetica": "No disponible"}

        console.print("  [bold]✓ Meta-análisis completado[/bold]\n")
        return meta
