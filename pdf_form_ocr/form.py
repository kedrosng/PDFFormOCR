from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple


Field = Tuple[int, int, int, int]


class FormLayout:
    """Represents layout mapping of field names to bounding boxes."""

    def __init__(self, mapping: Dict[str, Field] | None = None):
        self.mapping: Dict[str, Field] = mapping or {}

    def save(self, path: str | Path) -> None:
        data = {k: list(v) for k, v in self.mapping.items()}
        Path(path).write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "FormLayout":
        p = Path(path)
        if not p.exists():
            return cls()
        data = json.loads(p.read_text())
        mapping = {k: tuple(v) for k, v in data.items()}
        return cls(mapping)
