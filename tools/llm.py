"""LLM wrapper — Groq (free) and Google Gemini via REST API."""
import re
import requests

_FENCE = re.compile(r'^```(?:json)?\s*|\s*```$', re.MULTILINE)

# ── Groq ─────────────────────────────────────────────────────────────────── #
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

# ── Gemini ───────────────────────────────────────────────────────────────── #
GEMINI_URL   = ("https://generativelanguage.googleapis.com/v1beta/models"
                "/gemini-1.5-flash:generateContent")


def _strip(text: str) -> str:
    return _FENCE.sub("", text).strip()


def _call_groq(system: str, prompt: str, api_key: str,
               max_tokens: int, temperature: float) -> str:
    r = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "system", "content": system},
                         {"role": "user",   "content": prompt}],
            "max_tokens":  max_tokens,
            "temperature": temperature,
        },
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Groq error {r.status_code}: {r.text[:300]}")
    return _strip(r.json()["choices"][0]["message"]["content"])


def _call_gemini(system: str, prompt: str, api_key: str,
                 max_tokens: int, temperature: float) -> str:
    r = requests.post(
        GEMINI_URL,
        params={"key": api_key},
        json={
            "system_instruction": {"parts": [{"text": system}]},
            "contents":           [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature":     temperature,
            },
        },
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Gemini error {r.status_code}: {r.text[:300]}")
    return _strip(r.json()["candidates"][0]["content"]["parts"][0]["text"])


def call_llm(system: str, prompt: str, api_key: str,
             max_tokens: int = 2048, temperature: float = 0.3,
             provider: str = "groq") -> str:
    """Call Groq or Gemini and return plain text (code fences stripped)."""
    if provider == "gemini":
        return _call_gemini(system, prompt, api_key, max_tokens, temperature)
    return _call_groq(system, prompt, api_key, max_tokens, temperature)
