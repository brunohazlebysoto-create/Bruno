"""Unified LLM wrapper — Google Gemini 1.5 Flash via REST API (no SDK needed)."""
import re
import requests

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models"
    "/gemini-1.5-flash:generateContent"
)

_FENCE = re.compile(r'^```(?:json)?\s*|\s*```$', re.MULTILINE)


def call_llm(system: str, prompt: str, api_key: str,
             max_tokens: int = 2048, temperature: float = 0.3) -> str:
    """Call Gemini 1.5 Flash and return plain text (code fences stripped)."""
    payload = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": temperature,
        },
    }
    r = requests.post(
        GEMINI_URL,
        params={"key": api_key},
        json=payload,
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(
            f"Gemini API error {r.status_code}: {r.text[:300]}"
        )
    text = (
        r.json()
        ["candidates"][0]["content"]["parts"][0]["text"]
        .strip()
    )
    return _FENCE.sub("", text).strip()
