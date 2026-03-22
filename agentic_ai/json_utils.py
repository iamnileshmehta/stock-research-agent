import json
import re
from typing import Any


def extract_first_json_block(text: str) -> str | None:
    if not text:
        return None

    fenced = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
    if fenced:
        return fenced.group(1)

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return text[start : end + 1]


def safe_json_loads(text: str, fallback: Any) -> Any:
    block = extract_first_json_block(text)
    if not block:
        return fallback
    try:
        return json.loads(block)
    except json.JSONDecodeError:
        return fallback
