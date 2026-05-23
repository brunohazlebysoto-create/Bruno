"""PubMed/NCBI Entrez API integration."""
import time
import requests
from typing import Optional

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search(query: str, max_results: int = 20, api_key: Optional[str] = None) -> list[dict]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
    }
    if api_key:
        params["api_key"] = api_key

    try:
        r = requests.get(f"{BASE}/esearch.fcgi", params=params, timeout=15)
        r.raise_for_status()
    except Exception:
        return []
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []
    return fetch_details(ids, api_key)


def fetch_details(pmids: list[str], api_key: Optional[str] = None) -> list[dict]:
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json",
        "rettype": "abstract",
    }
    if api_key:
        params["api_key"] = api_key

    time.sleep(0.4)  # NCBI rate limit: max 3 req/s without key, 10/s with key
    r = requests.get(f"{BASE}/efetch.fcgi", params=params, timeout=20)

    # efetch with json+abstract returns PubmedArticleSet in XML; use summary instead
    params["rettype"] = "docsum"
    r = requests.get(f"{BASE}/esummary.fcgi", params=params, timeout=20)
    r.raise_for_status()

    articles = []
    result = r.json().get("result", {})
    for pmid in pmids:
        art = result.get(pmid, {})
        if not art:
            continue
        articles.append({
            "pmid": pmid,
            "title": art.get("title", ""),
            "authors": [a.get("name", "") for a in art.get("authors", [])],
            "journal": art.get("fulljournalname", art.get("source", "")),
            "year": art.get("pubdate", "")[:4],
            "abstract": art.get("summary", ""),
            "doi": next(
                (i.get("value", "") for i in art.get("articleids", []) if i.get("idtype") == "doi"),
                "",
            ),
            "source": "PubMed",
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        })
    return articles
