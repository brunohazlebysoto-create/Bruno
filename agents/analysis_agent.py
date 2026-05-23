"""Analysis Agent — evaluates each paper with Claude using structured criteria."""
import json
import os
import anthropic
from rich.console import Console
from rich.progress import track

console = Console()

SYSTEM = """Eres un cirujano pediatra e investigador clínico experto en medicina basada en evidencia (MBE).
Tienes amplio conocimiento de cirugía infantil, anestesia pediátrica, neonatología quirúrgica
y epidemiología clínica pediátrica. Analizas artículos con rigor metodológico considerando
las particularidades fisiológicas, farmacológicas y éticas de la población pediátrica.
Siempre responde en español con formato JSON válido."""

ANALYSIS_PROMPT = """Analiza el siguiente artículo de CIRUGÍA INFANTIL y devuelve SOLO un JSON con esta estructura exacta:

{{
  "titulo_resumido": "<título corto ≤60 chars>",
  "tipo_estudio": "<RCT | Cohorte | Caso-Control | Transversal | Revisión Sistemática | Meta-análisis | Reporte de Caso | Serie de Casos | Otro>",
  "nivel_evidencia": "<1a | 1b | 2a | 2b | 3 | 4 | 5>",
  "grado_recomendacion": "<A | B | C | D>",
  "grupo_etario": "<neonato | lactante | preescolar | escolar | adolescente | mixto>",
  "rango_edad": "<p.ej. 0–14 años>",
  "poblacion": "<descripción de la población pediátrica estudiada>",
  "patologia_quirurgica": "<diagnóstico quirúrgico principal>",
  "intervencion": "<técnica quirúrgica o manejo principal>",
  "comparador": "<técnica alternativa o grupo control>",
  "desenlace_principal": "<outcome quirúrgico primario>",
  "n_muestra": <número entero o null>,
  "seguimiento": "<duración del seguimiento>",
  "resultado_clave": "<resultado numérico principal con IC95% si disponible>",
  "complicaciones_reportadas": ["<complicación 1>", "<complicación 2>"],
  "mortalidad": "<tasa de mortalidad si reportada, o 'no reportada'>",
  "consideraciones_anestesia": "<aspectos anestésicos o perioperatorios relevantes o 'no aplica'>",
  "consideraciones_neonatales": "<aspectos neonatales relevantes o 'no aplica'>",
  "conclusion_autores": "<conclusión principal en 1-2 oraciones>",
  "fortalezas": ["<fortaleza 1>", "<fortaleza 2>"],
  "limitaciones": ["<limitación 1>", "<limitación 2>"],
  "sesgo_riesgo": "<bajo | moderado | alto | no evaluable>",
  "relevancia_clinica": <1-5>,
  "calidad_metodologica": <1-5>,
  "aplicabilidad_pediatrica": "<directa | parcial | limitada>",
  "palabras_clave": ["<kw1>", "<kw2>", "<kw3>"]
}}

ARTÍCULO:
Título: {title}
Autores: {authors}
Revista: {journal} ({year})
Resumen: {abstract}
"""


class AnalysisAgent:
    """Evaluates paper quality and extracts structured data using Claude."""

    name = "Agente Analizador"
    description = (
        "Experto en epidemiología clínica. Evalúa calidad metodológica, "
        "nivel de evidencia (Oxford CEBM), PICO y aplicabilidad clínica."
    )

    def __init__(self, api_key: str = ""):
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        )

    def _analyze_one(self, paper: dict) -> dict:
        prompt = ANALYSIS_PROMPT.format(
            title=paper.get("title", "Sin título"),
            authors=", ".join(paper.get("authors", [])[:5]),
            journal=paper.get("journal", ""),
            year=paper.get("year", ""),
            abstract=paper.get("abstract", "Sin resumen disponible")[:3000],
        )
        try:
            msg = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            text = msg.content[0].text.strip()
            # Strip markdown code fences if present
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            analysis = json.loads(text)
        except (json.JSONDecodeError, Exception) as e:
            analysis = {
                "titulo_resumido": paper.get("title", "")[:60],
                "tipo_estudio": "No evaluable",
                "nivel_evidencia": "N/A",
                "grado_recomendacion": "N/A",
                "resultado_clave": "No disponible",
                "conclusion_autores": "No disponible",
                "sesgo_riesgo": "no evaluable",
                "relevancia_clinica": 0,
                "calidad_metodologica": 0,
                "error": str(e),
            }
        return {**paper, "analysis": analysis}

    def run(self, papers: list[dict]) -> list[dict]:
        console.print(
            f"\n[bold cyan]🔬 {self.name}[/bold cyan] — analizando {len(papers)} artículos con Claude\n"
        )
        analyzed = []
        for paper in track(papers, description="  Analizando artículos..."):
            result = self._analyze_one(paper)
            analyzed.append(result)
        console.print(
            f"  [bold]✓ Análisis completado:[/bold] {len(analyzed)} artículos evaluados\n"
        )
        return analyzed
