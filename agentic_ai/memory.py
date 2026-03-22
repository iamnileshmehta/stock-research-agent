import json
from pathlib import Path
from typing import Any


class JsonMemoryStore:
    def __init__(self, path: str = ".agentic_memory/memory.json"):
        self.path = Path(path)

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"runs": []}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"runs": []}

    def _save(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def append_run(self, run: dict[str, Any]) -> None:
        data = self._load()
        data.setdefault("runs", []).append(run)
        self._save(data)

    def recent_for_symbol(self, symbol: str, limit: int = 3) -> list[dict[str, Any]]:
        data = self._load()
        runs = data.get("runs", [])
        filtered = [r for r in runs if str(r.get("symbol", "")).upper() == symbol.upper()]
        return filtered[-limit:]
