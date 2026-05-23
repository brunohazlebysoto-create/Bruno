"""CrossRef API integration — metadata + clinical trial detection."""
import requests

BASE = "https://api.crossref.org/works"
MAILTO = "brunohazlebysoto@gmail.com"


def search(query: str, max_results: int = 15) -> list[dict]:
    params = {
        "query": query,
        "rows": max_results,
        "filter": "type:journal-article",
        "select": "DOI,title,author,published,abstract,container-title,is-referenced-by-count,type",
        "mailto": MAILTO,
        "sort": "relevance",
    }
    try:
        r = requests.get(BASE, params=params, timeout=15)
    except Exception:
        return []
    if r.status_code != 200:
        return []

    papers = []
    for item in r.json().get("message", {}).get("items", []):
        title_list = item.get("title", [])
        authors = [
            f"{a.get('given', '')} {a.get('family', '')}".strip()
            for a in item.get("author", [])
        ]
        pub = item.get("published", {}).get("date-parts", [[""]])[0]
        year = str(pub[0]) if pub else ""
        abstract = item.get("abstract", "")
        # Strip JATS XML tags if present
        if abstract:
            import re
            abstract = re.sub(r"<[^>]+>", " ", abstract).strip()

        papers.append({
            "pmid": "",
            "title": title_list[0] if title_list else "",
            "authors": authors,
            "journal": (item.get("container-title") or [""])[0],
            "year": year,
            "abstract": abstract,
            "doi": item.get("DOI", ""),
            "citations": item.get("is-referenced-by-count", 0),
            "source": "CrossRef",
            "url": f"https://doi.org/{item.get('DOI', '')}",
        })
    return papers
