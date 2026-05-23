"""Meta-analysis Agent — synthesizes evidence using Gemini 1.5 Flash."""
import json
import os
from rich.console import Console
from tools.llm import call_llm

console = Console()

SYSTEM = """Eres un cirujano pediatra y bioestadístico especialista en meta-análisis en cirugía infantil.
Conoces profundamente las particularidades metodológicas de la investigación quirúrgica pediátrica:
escasez de RCTs, heterogeneidad de grupos etarios, diferencias fisiológicas entre neonatos,
lactantes y niños mayores, y los retos éticos de la investigación en menores de edad.
Realizas síntesis cuantitativa y cualitativa rigurosa con criterios GRADE adaptados al contexto quirúrgico pediátrico.
Responde siempre en español con formato JSON válido."""

META_PROMPT = """Realiza un meta-análisis completo en cirugía infantil de los siguientes artículos analizados.
Devuelve SOLO un JSON con esta estructura exacta:

{{
  "pregunta_clinica": "<pregunta PICO-S pediátrica derivada de la evidencia>",
  "total_estudios": <número>,
  "total_pacientes_estimado": <número o null>,
  "distribucion_tipos": {{
    "RCT": <n>,
    "Cohorte": <n>,
    "Revision_Sistematica": <n>,
    "Meta_analisis": <n>,
    "Serie_de_Casos": <n>,
    "Otros": <n>
  }},
  "distribucion_etaria": {{
    "neonatos": "<% o descripción>",
    "lactantes": "<% o descripción>",
    "preescolares_escolares": "<% o descripción>",
    "adolescentes": "<% o descripción>"
  }},
  "nivel_evidencia_global": "<1a | 1b | 2a | 2b | 3 | 4 | 5>",
  "grado_recomendacion_global": "<A | B | C | D>",
  "heterogeneidad": "<baja | moderada | alta | no evaluable>",
  "sesgo_publicacion": "<probable | improbable | no evaluable>",
  "hallazgos_principales": [
    {{"hallazgo": "<descripción>", "nivel_evidencia": "<nivel>", "consenso": "<alto|moderado|bajo>"}},
    {{"hallazgo": "<descripción>", "nivel_evidencia": "<nivel>", "consenso": "<alto|moderado|bajo>"}}
  ],
  "tecnicas_quirurgicas_comparadas": ["<técnica 1>", "<técnica 2>"],
  "complicaciones_mas_frecuentes": ["<complicación 1>", "<complicación 2>", "<complicación 3>"],
  "mortalidad_global": "<tasa estimada o 'no evaluable'>",
  "consideraciones_anestesia_periop": "<aspectos anestésicos/perioperatorios clave>",
  "areas_controversia": ["<área 1>", "<área 2>"],
  "areas_consenso": ["<área 1>", "<área 2>"],
  "gaps_conocimiento": ["<gap 1>", "<gap 2>"],
  "implicaciones_clinicas": ["<implicación 1>", "<implicación 2>", "<implicación 3>"],
  "implicaciones_investigacion": ["<línea futura 1>", "<línea futura 2>"],
  "recomendaciones_tecnica": "<recomendación sobre técnica quirúrgica preferida basada en la evidencia>",
  "conclusion_sintetica": "<conclusión global en 3-5 oraciones>",
  "resumen_ejecutivo": "<párrafo ejecutivo de 100-150 palabras para cirujanos pediatras>",
  "tabla_evidencia": [
    {{
      "referencia": "<Autor et al., Año>",
      "tipo": "<tipo estudio>",
      "n": <n o null>,
      "grupo_etario": "<grupo etario>",
      "resultado_clave": "<resultado quirúrgico>",
      "nivel_evidencia": "<nivel>",
      "calidad": <1-5>
    }}
  ]
}}

ARTÍCULOS ANALIZADOS:
{articles_json}

TEMA (CIRUGÍA INFANTIL): {topic}
"""


class MetaAnalysisAgent:
    """Synthesizes evidence across all analyzed papers."""

    name = "Agente Meta-Analista"
    description = (
        "Bioestadístico en cirugía infantil · Síntesis GRADE · "
        "Distribución etaria · Técnicas quirúrgicas comparadas"
    )

    def __init__(self, api_key: str = "", provider: str = "gemini", mode: str = "free"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
        self.provider = provider
        self.mode = mode

    def _summarize_for_prompt(self, papers: list[dict]) -> str:
        summaries = []
        for p in papers:
            a = p.get("analysis", {})
            summaries.append({
                "titulo": a.get("titulo_resumido", p.get("title", "")[:60]),
                "autores": p.get("authors", [])[:3],
                "año": p.get("year", ""),
                "tipo_estudio": a.get("tipo_estudio", ""),
                "grupo_etario": a.get("grupo_etario", ""),
                "patologia_quirurgica": a.get("patologia_quirurgica", ""),
                "intervencion": a.get("intervencion", ""),
                "nivel_evidencia": a.get("nivel_evidencia", ""),
                "n_muestra": a.get("n_muestra"),
                "resultado_clave": a.get("resultado_clave", ""),
                "complicaciones": a.get("complicaciones_reportadas", []),
                "mortalidad": a.get("mortalidad", ""),
                "conclusion": a.get("conclusion_autores", ""),
                "calidad_metodologica": a.get("calidad_metodologica", 0),
                "sesgo_riesgo": a.get("sesgo_riesgo", ""),
                "relevancia_clinica": a.get("relevancia_clinica", 0),
            })
        return json.dumps(summaries, ensure_ascii=False, indent=2)

    def run(self, papers: list[dict], topic: str) -> dict:
        console.print(
            f"\n[bold cyan]📊 {self.name}[/bold cyan] — "
            f"sintetizando {len(papers)} artículos\n"
        )
        articles_json = self._summarize_for_prompt(papers)
        prompt = META_PROMPT.format(articles_json=articles_json, topic=topic)

        try:
            text = call_llm(SYSTEM, prompt, self.api_key, max_tokens=4096, provider=self.provider, mode=self.mode)
            meta = json.loads(text)
        except Exception as e:
            console.print(f"  [red]Error en meta-análisis:[/red] {e}")
            meta = {"error": str(e), "conclusion_sintetica": "No disponible"}

        console.print("  [bold]✓ Meta-análisis completado[/bold]\n")
        return meta
