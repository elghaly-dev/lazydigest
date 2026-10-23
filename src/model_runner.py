import json
import logging
import re

import ollama

from src.config import GEMMA_MODEL

logging.basicConfig(level=logging.INFO)

SYSTEM_PROMPT = """You are a lazy personal note summarizer.
Analyze the provided notes and return a concise JSON summary containing:
1. "category": A single short category name.
2. "key_takeaway": One sentence summarizing the core idea.
3. "action_item": One optional actionable task, or "None".

Strictly respond with valid JSON only."""

_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def _fallback(note_content: str) -> dict:
    lines = note_content.strip().splitlines()
    first = lines[0][:100] if lines else "(empty note)"
    return {"category": "General", "key_takeaway": first, "action_item": "None"}


def parse_model_output(raw_text: str, note_content: str) -> dict:
    """Strip optional code fences, parse JSON, and fill any missing keys."""
    text = _FENCE.sub("", (raw_text or "").strip()).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("model output is not a JSON object")
    fb = _fallback(note_content)
    return {
        "category": str(data.get("category") or fb["category"]),
        "key_takeaway": str(data.get("key_takeaway") or fb["key_takeaway"]),
        "action_item": str(data.get("action_item") or "None"),
    }


def analyze_note_with_gemma(note_content: str) -> dict:
    """Passes note content to the local Gemma model via Ollama."""
    try:
        response = ollama.generate(
            model=GEMMA_MODEL,
            prompt=f"{SYSTEM_PROMPT}\n\nNote:\n{note_content}",
            options={"temperature": 0.1, "top_p": 0.9},
        )
        return parse_model_output(response.get("response", ""), note_content)
    except Exception as e:
        logging.warning("Local Gemma run failed or returned invalid JSON: %s", e)
        return _fallback(note_content)
