"""Semantic Scholar API integration."""
import requests
from typing import Optional

BASE = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,authors,year,abstract,journal,externalIds,citationCount,openAccessPdf,publicationTypes"


def search(query: str, max_results: int = 15, api_key: Optional[str] = None) -> list[dict]:
    headers = {"x-api-key": api_key} if api_key else {}
    params = {
        "query": query,
        "limit": max_results,
        "fields": FIELDS,
    }
    try:
        r = requests.get(f"{BASE}/paper/search", params=params, headers=headers, timeout=15)
    except Exception:
        return []
    if r.status_code in (429, 403):
        return []
    if not r.ok:
        return []

    papers = []
    for p in r.json().get("data", []):
        papers.append({
            "pmid": p.get("externalIds", {}).get("PubMed", ""),
            "title": p.get("title", ""),
            "authors": [a.get("name", "") for a in p.get("authors", [])],
            "journal": (p.get("journal") or {}).get("name", ""),
            "year": str(p.get("year", "")),
            "abstract": p.get("abstract", ""),
            "doi": p.get("externalIds", {}).get("DOI", ""),
            "citations": p.get("citationCount", 0),
            "open_access_pdf": (p.get("openAccessPdf") or {}).get("url", ""),
            "publication_types": p.get("publicationTypes", []),
            "source": "Semantic Scholar",
            "url": f"https://www.semanticscholar.org/paper/{p.get('paperId', '')}",
        })
    return papers
