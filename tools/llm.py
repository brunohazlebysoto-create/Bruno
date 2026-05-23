"""LLM wrapper — Groq (free) and Google Gemini via REST API.

Gemini modes
------------
  free  → gemini-2.5-flash       gratis, cuota gratuita, sin cobro de tokens
  pro   → gemini-1.5-pro         cobra tokens (~$1.25/M input tokens)

Groq mode
---------
  groq  → llama-3.3-70b-versatile  gratis con registro, sin tarjeta
"""
import re
import requests

_FENCE = re.compile(r'^```(?:json)?\s*|\s*```$', re.MULTILINE)

# ── Gemini model map ──────────────────────────────────────────────────────── #
GEMINI_MODELS = {
    "free": "gemini-2.5-flash",       # cuota gratuita, sin cobro de tokens
    "pro":  "gemini-1.5-pro",         # cobra tokens
}
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# ── Groq ──────────────────────────────────────────────────────────────────── #
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"


def _strip(text: str) -> str:
    return _FENCE.sub("", text).strip()


def _call_gemini(system: str, prompt: str, api_key: str,
                 max_tokens: int, temperature: float, mode: str) -> str:
    model = GEMINI_MODELS.get(mode, GEMINI_MODELS["free"])
    url   = GEMINI_BASE.format(model=model)
    r = requests.post(
        url,
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


def call_llm(system: str, prompt: str, api_key: str,
             max_tokens: int = 2048, temperature: float = 0.3,
             provider: str = "gemini", mode: str = "free") -> str:
    """
    provider: "gemini" | "groq"
    mode:     "free"   → gemini-2.0-flash (sin costo)
              "pro"    → gemini-1.5-pro    (cobra tokens)
              (ignorado cuando provider="groq")
    """
    if provider == "groq":
        return _call_groq(system, prompt, api_key, max_tokens, temperature)
    return _call_gemini(system, prompt, api_key, max_tokens, temperature, mode)


def model_label(provider: str, mode: str) -> str:
    """Human-readable model name for UI display."""
    if provider == "groq":
        return f"Groq · {GROQ_MODEL}"
    return f"Gemini · {GEMINI_MODELS.get(mode, 'gemini-2.0-flash')}"
