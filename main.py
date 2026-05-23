#!/usr/bin/env python3
"""
Sistema Multi-Agente de Investigación en Cirugía Infantil
==========================================================
Orquestador de 5 agentes expertos en cirugía pediátrica que:
  1. Buscan papers en PubMed, Semantic Scholar y CrossRef (con filtros pediátricos)
  2. Analizan cada artículo con criterios de MBE quirúrgica pediátrica
  3. Realizan meta-análisis con perspectiva de cirugía infantil
  4. Generan apunte clínico completo con técnica quirúrgica y cuidados pediátricos
  5. Crean presentación PowerPoint académica de cirugía infantil

Temas de ejemplo:
    python main.py "apendicitis aguda laparoscopia pediátrica"
    python main.py "invaginación intestinal reducción neumática"
    python main.py "estenosis hipertrófica del píloro piloromiotomía"
    python main.py "enfermedad de Hirschsprung pull-through"
    python main.py "hernia inguinal lactantes reparación laparoscópica"
    python main.py "atresia esofágica reparación toracoscópica"
    python main.py "gastrosquisis cierre primario"
    python main.py "malrotación intestinal procedimiento de Ladd"
    python main.py "criptorquidia orquiopexia"
    python main.py --topic "estenosis ureteropélvica pieloplastia" --max-papers 25
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

# ── Agents ──────────────────────────────────────────────────────────────────── #
from agents.search_agent      import SearchAgent
from agents.analysis_agent    import AnalysisAgent
from agents.meta_analysis_agent import MetaAnalysisAgent
from agents.notes_agent       import NotesAgent
from agents.ppt_agent         import PPTAgent

console = Console()


def banner():
    console.print()
    console.print(Panel(
        Text.from_markup(
            "[bold cyan]🔪 Sistema Multi-Agente de Investigación en Cirugía Infantil[/bold cyan]\n"
            "[dim]PubMed · Semantic Scholar · CrossRef · Análisis PICO · Meta-análisis · Apuntes · PowerPoint[/dim]\n"
            "[dim]Apendicitis · Invaginación · Píloro · Hirschsprung · Hernia inguinal · Atresia esofágica · y más[/dim]"
        ),
        border_style="cyan",
        padding=(1, 4),
    ))
    console.print()


def save_json(data, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(text: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_pipeline(
    topic: str,
    max_papers: int = 20,
    output_dir: str = "./output",
    api_key: str = "",
    pubmed_key: str = "",
    ss_key: str = "",
    skip_ppt: bool = False,
):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = topic[:40].lower().replace(" ", "_").replace("/", "-")
    out = Path(output_dir) / f"{slug}_{ts}"
    out.mkdir(parents=True, exist_ok=True)

    anthropic_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not anthropic_key:
        console.print(
            "[red]ERROR:[/red] Se requiere ANTHROPIC_API_KEY. "
            "Exporta la variable o pasa --api-key."
        )
        sys.exit(1)

    # ── 1. Search ───────────────────────────────────────────────────────────── #
    console.print(Rule("[bold]Fase 1: Búsqueda Bibliográfica[/bold]", style="cyan"))
    searcher = SearchAgent(pubmed_api_key=pubmed_key, ss_api_key=ss_key)
    papers = searcher.run(topic, max_per_db=max_papers // 3 + 5)
    save_json(papers, out / "01_papers_raw.json")
    console.print(f"  → Guardado: [dim]{out}/01_papers_raw.json[/dim]")

    if not papers:
        console.print("[yellow]No se encontraron artículos. Verifica el tema o la conexión.[/yellow]")
        sys.exit(0)

    # ── 2. Analysis ─────────────────────────────────────────────────────────── #
    console.print(Rule("[bold]Fase 2: Análisis Individual de Artículos[/bold]", style="cyan"))
    analyzer = AnalysisAgent(api_key=anthropic_key)
    analyzed = analyzer.run(papers[:max_papers])
    save_json(analyzed, out / "02_papers_analyzed.json")
    console.print(f"  → Guardado: [dim]{out}/02_papers_analyzed.json[/dim]")

    # ── 3. Meta-analysis ────────────────────────────────────────────────────── #
    console.print(Rule("[bold]Fase 3: Meta-Análisis[/bold]", style="cyan"))
    meta_agent = MetaAnalysisAgent(api_key=anthropic_key)
    meta = meta_agent.run(analyzed, topic)
    save_json(meta, out / "03_meta_analysis.json")
    console.print(f"  → Guardado: [dim]{out}/03_meta_analysis.json[/dim]")

    # ── 4. Notes ────────────────────────────────────────────────────────────── #
    console.print(Rule("[bold]Fase 4: Generación de Apunte Médico[/bold]", style="cyan"))
    notes_agent = NotesAgent(api_key=anthropic_key)
    notes_md = notes_agent.run(topic, meta, analyzed)
    notes_path = out / "04_apunte_medico.md"
    save_text(notes_md, notes_path)
    console.print(f"  → Guardado: [dim]{notes_path}[/dim]")

    # ── 5. PowerPoint ───────────────────────────────────────────────────────── #
    ppt_path = None
    if not skip_ppt:
        console.print(Rule("[bold]Fase 5: Generación de Presentación PowerPoint[/bold]", style="cyan"))
        ppt_agent = PPTAgent(api_key=anthropic_key)
        ppt_file = str(out / "05_presentacion.pptx")
        ppt_path = ppt_agent.run(topic, meta, ppt_file)

    # ── Summary ─────────────────────────────────────────────────────────────── #
    console.print()
    console.print(Panel(
        Text.from_markup(
            f"[bold green]✅ Pipeline completado exitosamente[/bold green]\n\n"
            f"[bold]Tema:[/bold] {topic}\n"
            f"[bold]Artículos encontrados:[/bold] {len(papers)}\n"
            f"[bold]Artículos analizados:[/bold] {len(analyzed)}\n"
            f"[bold]Nivel de evidencia global:[/bold] {meta.get('nivel_evidencia_global', 'N/A')}\n"
            f"[bold]Grado de recomendación:[/bold] {meta.get('grado_recomendacion_global', 'N/A')}\n\n"
            f"[bold]Archivos generados:[/bold]\n"
            f"  📄 {out}/01_papers_raw.json\n"
            f"  🔬 {out}/02_papers_analyzed.json\n"
            f"  📊 {out}/03_meta_analysis.json\n"
            f"  📝 {out}/04_apunte_medico.md\n"
            + (f"  🎨 {ppt_path}\n" if ppt_path else "")
        ),
        title="[bold cyan]Resumen[/bold cyan]",
        border_style="green",
        padding=(1, 3),
    ))
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Sistema Multi-Agente de Investigación Médica",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "topic", nargs="?",
        help="Tema médico a investigar (entre comillas si tiene espacios)"
    )
    parser.add_argument("--topic", "-t", dest="topic_flag", help="Alternativa: tema médico")
    parser.add_argument("--max-papers", "-n", type=int, default=20,
                        help="Máximo de artículos a procesar (default: 20)")
    parser.add_argument("--output", "-o", default="./output",
                        help="Directorio de salida (default: ./output)")
    parser.add_argument("--api-key", help="Anthropic API key (o env ANTHROPIC_API_KEY)")
    parser.add_argument("--pubmed-key", default="", help="NCBI API key (opcional)")
    parser.add_argument("--ss-key", default="", help="Semantic Scholar API key (opcional)")
    parser.add_argument("--no-ppt", action="store_true", help="Omitir generación de PowerPoint")

    args = parser.parse_args()
    topic = args.topic or args.topic_flag

    banner()

    if not topic:
        console.print("[yellow]Ingresa el tema de cirugía infantil a investigar:[/yellow]")
        console.print(
            "[dim]Ejemplos: 'apendicitis aguda pediátrica', 'invaginación intestinal', "
            "'estenosis hipertrófica del píloro', 'hernia inguinal', "
            "'enfermedad de Hirschsprung'[/dim]"
        )
        topic = input("→ ").strip()
        if not topic:
            console.print("[red]Tema vacío. Saliendo.[/red]")
            sys.exit(1)

    run_pipeline(
        topic=topic,
        max_papers=args.max_papers,
        output_dir=args.output,
        api_key=args.api_key or "",
        pubmed_key=args.pubmed_key,
        ss_key=args.ss_key,
        skip_ppt=args.no_ppt,
    )


if __name__ == "__main__":
    main()
