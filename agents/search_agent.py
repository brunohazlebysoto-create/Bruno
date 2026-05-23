"""Search Agent — queries PubMed, Semantic Scholar and CrossRef in parallel."""
import json
import os
import threading
from rich.console import Console
from tools import pubmed, semantic_scholar, crossref
from tools.demo_papers import get_demo_papers

console = Console()


def deduplicate(papers: list[dict]) -> list[dict]:
    seen_titles, seen_dois, unique = set(), set(), []
    for p in papers:
        title_key = p.get("title", "").lower().strip()[:80]
        doi_key = p.get("doi", "").lower().strip()
        if doi_key and doi_key in seen_dois:
            continue
        if title_key and title_key in seen_titles:
            continue
        if doi_key:
            seen_dois.add(doi_key)
        if title_key:
            seen_titles.add(title_key)
        unique.append(p)
    return unique


class SearchAgent:
    """Multi-database parallel literature search."""

    name = "Agente Buscador"
    description = (
        "Experto en búsqueda bibliográfica médica. "
        "Consulta PubMed, Semantic Scholar y CrossRef simultáneamente."
    )

    def __init__(self, pubmed_api_key: str = "", ss_api_key: str = ""):
        self.pubmed_key = pubmed_api_key or os.getenv("PUBMED_API_KEY", "")
        self.ss_key = ss_api_key or os.getenv("SS_API_KEY", "")

    # ------------------------------------------------------------------ #

    def _build_queries(self, topic: str) -> dict[str, str]:
        """Generate database-specific search strings from the topic."""
        base = topic.strip()
        return {
            "pubmed": f'({base})[Title/Abstract] AND ("last 10 years"[PDat])',
            "ss": base,
            "crossref": base,
        }

    def run(self, topic: str, max_per_db: int = 15) -> list[dict]:
        queries = self._build_queries(topic)
        results: dict[str, list] = {"pubmed": [], "ss": [], "crossref": []}
        errors: list[str] = []

        def fetch_pubmed():
            try:
                results["pubmed"] = pubmed.search(
                    queries["pubmed"], max_per_db, self.pubmed_key
                )
                console.print(
                    f"  [green]✓ PubMed[/green]: {len(results['pubmed'])} artículos"
                )
            except Exception as e:
                errors.append(f"PubMed: {e}")
                console.print(f"  [yellow]! PubMed error[/yellow]: {e}")

        def fetch_ss():
            try:
                results["ss"] = semantic_scholar.search(
                    queries["ss"], max_per_db, self.ss_key
                )
                console.print(
                    f"  [green]✓ Semantic Scholar[/green]: {len(results['ss'])} artículos"
                )
            except Exception as e:
                errors.append(f"SemanticScholar: {e}")
                console.print(f"  [yellow]! Semantic Scholar error[/yellow]: {e}")

        def fetch_crossref():
            try:
                results["crossref"] = crossref.search(queries["crossref"], max_per_db)
                console.print(
                    f"  [green]✓ CrossRef[/green]: {len(results['crossref'])} artículos"
                )
            except Exception as e:
                errors.append(f"CrossRef: {e}")
                console.print(f"  [yellow]! CrossRef error[/yellow]: {e}")

        console.print(f"\n[bold cyan]🔍 {self.name}[/bold cyan] — buscando: [italic]{topic}[/italic]")
        threads = [
            threading.Thread(target=fetch_pubmed),
            threading.Thread(target=fetch_ss),
            threading.Thread(target=fetch_crossref),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        all_papers = results["pubmed"] + results["ss"] + results["crossref"]
        unique = deduplicate(all_papers)
        if not unique:
            console.print(
                "  [yellow]⚠ No se encontraron artículos en bases externas. "
                "Usando datos de demostración.[/yellow]"
            )
            unique = get_demo_papers(topic)
            for p in unique:
                p["demo"] = True
            console.print(f"  [dim]→ {len(unique)} artículos demo cargados[/dim]")
        else:
            console.print(
                f"  [bold]Total únicos:[/bold] {len(unique)} artículos tras deduplicación"
            )
        console.print()
        return unique
