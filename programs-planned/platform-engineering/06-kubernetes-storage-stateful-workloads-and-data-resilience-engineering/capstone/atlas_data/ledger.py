from __future__ import annotations

import json
from pathlib import Path

from .durability import write_atomic
from .fencing import FenceToken


class DurableLedger:
    """A tiny durable ledger used to make fencing visible in local tests.

    The ledger is not a database. It intentionally exposes only one atomic
    document so the learner can inspect when a generation becomes durable.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.state_file = self.root / "ledger.json"
        if not self.state_file.exists():
            write_atomic(self.state_file, b'{"generation":0,"records":{}}\n')

    def _load(self) -> dict[str, object]:
        document = json.loads(self.state_file.read_text(encoding="utf-8"))
        if not isinstance(document.get("records"), dict):
            raise ValueError("ledger records must be an object")
        return document

    def commit(self, token: FenceToken, key: str, value: str) -> int:
        state = self._load()
        current = int(state["generation"])
        if token.generation < current:
            raise PermissionError("stale ledger writer")
        if token.generation > current:
            state["generation"] = token.generation
        records = dict(state["records"])
        records[key] = value
        state["records"] = records
        payload = json.dumps(
            state,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8") + b"\n"
        write_atomic(self.state_file, payload)
        return int(state["generation"])

    def read(self, key: str) -> str | None:
        return dict(self._load()["records"]).get(key)

    def generation(self) -> int:
        return int(self._load()["generation"])
