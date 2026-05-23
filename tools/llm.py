"""LLM wrapper — Groq (free) and Google Gemini via REST API.

Gemini modes
------------
  free  → gemini-2.5-flash   cuota gratuita, 15 RPM; pausa 5 s entre llamadas
  pro   → gemini-1.5-pro     sin pausas, cobra tokens (~$1.25/M input tokens)

Groq mode
---------
  groq  → llama-3.3-70b-versatile  gratis con registro, sin tarjeta
"""
import re
import time
import requests

_FENCE = re.compile(r'^```(?:json)?\s*|\s*```$', re.MULTILINE)

# ── Gemini model map ──────────────────────────────────────────────────────── #
GEMINI_MODELS = {
    "free": "gemini-2.5-flash",   # cuota gratuita, sin cobro de tokens
    "pro":  "gemini-1.5-pro",     # cobra tokens
}
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Pausa entre llamadas en modo free para mantenerse bajo los 15 RPM de Google
FREE_RATE_PAUSE = 5  # segundos

# ── Groq ──────────────────────────────────────────────────────────────────── #
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

# ── Cerebras (gratis, muy rápido) ─────────────────────────────────────────── #
CEREBRAS_URL   = "https://api.cerebras.ai/v1/chat/completions"
CEREBRAS_MODEL = "llama3.1-70b"


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
    result = _strip(r.json()["candidates"][0]["content"]["parts"][0]["text"])
    # Pausa estratégica en modo free para respetar el límite de 15 RPM
    if mode == "free":
        time.sleep(FREE_RATE_PAUSE)
    return result


def _call_openai_compat(url: str, model: str, system: str, prompt: str,
                        api_key: str, max_tokens: int,
                        temperature: float, name: str) -> str:
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user",   "content": prompt}],
            "max_tokens":  max_tokens,
            "temperature": temperature,
        },
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(f"{name} error {r.status_code}: {r.text[:300]}")
    return _strip(r.json()["choices"][0]["message"]["content"])


def _call_groq(system: str, prompt: str, api_key: str,
               max_tokens: int, temperature: float) -> str:
    return _call_openai_compat(GROQ_URL, GROQ_MODEL, system, prompt,
                               api_key, max_tokens, temperature, "Groq")


def _call_cerebras(system: str, prompt: str, api_key: str,
                   max_tokens: int, temperature: float) -> str:
    return _call_openai_compat(CEREBRAS_URL, CEREBRAS_MODEL, system, prompt,
                               api_key, max_tokens, temperature, "Cerebras")


def call_llm(system: str, prompt: str, api_key: str,
             max_tokens: int = 2048, temperature: float = 0.3,
             provider: str = "gemini", mode: str = "free") -> str:
    """
    provider: "gemini" | "groq"
    mode:     "free"  → gemini-2.5-flash, pausa 5 s (100% gratis)
              "pro"   → gemini-1.5-pro,   sin pausas (cobra tokens)
              (ignorado cuando provider="groq")
    """
    if provider == "groq":
        return _call_groq(system, prompt, api_key, max_tokens, temperature)
    if provider == "cerebras":
        return _call_cerebras(system, prompt, api_key, max_tokens, temperature)
    return _call_gemini(system, prompt, api_key, max_tokens, temperature, mode)


def model_label(provider: str, mode: str) -> str:
    """Human-readable model name for UI display."""
    if provider == "groq":
        return f"Groq · {GROQ_MODEL}"
    if provider == "cerebras":
        return f"Cerebras · {CEREBRAS_MODEL}"
    return f"Gemini · {GEMINI_MODELS.get(mode, 'gemini-2.5-flash')}"
