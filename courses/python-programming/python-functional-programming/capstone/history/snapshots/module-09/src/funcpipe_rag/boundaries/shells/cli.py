"""Module 09 Core 6: minimal stdlib CLI shell (end-of-Module-09).

This CLI is intentionally small and dependency-free (argparse). It demonstrates:
- thin shell adapter
- config-as-data loading (JSON)
- override parsing (dotted `a.b=1` strings)
- delegation to pure pipeline builders in `funcpipe_rag.pipelines`
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast

from funcpipe_rag.core.rag_types import RawDoc
from funcpipe_rag.infra.adapters.file_storage import FileStorage
from funcpipe_rag.pipelines.cli import deep_merge, parse_override
from funcpipe_rag.pipelines.configured import PipelineConfig, StepConfig, build_rag_pipeline
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result


def _load_config(path: Path) -> PipelineConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "steps" not in data:
        raise ValueError("config must be an object with a 'steps' field")
    steps_raw = data["steps"]
    if not isinstance(steps_raw, list):
        raise ValueError("config.steps must be a list")
    steps: list[StepConfig] = []
    for s in steps_raw:
        if not isinstance(s, dict) or "name" not in s:
            raise ValueError("each step must be an object with a 'name'")
        name = s["name"]
        params = s.get("params", {})
        if not isinstance(name, str) or not isinstance(params, dict):
            raise ValueError("step.name must be str and step.params must be object")
        steps.append(StepConfig(name=name, params=params))
    return PipelineConfig(steps=tuple(steps))


def _render(result: Result[Any, ErrInfo]) -> int:
    if isinstance(result, Ok):
        return 0
    err = result.error
    print(json.dumps({"error": {"code": err.code, "msg": err.msg, "stage": err.stage}}, ensure_ascii=False))
    return 2 if err.code.startswith("PARSE") else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="funcpipe-rag")
    p.add_argument("input_csv", type=Path)
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--set", dest="overrides", action="append", default=[], help="Override a.b.c=value")
    args = p.parse_args(argv)

    cfg = _load_config(args.config)
    overrides: dict[str, Any] = {}
    for ov in cast(list[str], args.overrides):
        overrides = deep_merge(overrides, parse_override(ov))

    if overrides:
        steps: list[StepConfig] = []
        for step in cfg.steps:
            step_over = overrides.get(step.name, {})
            if isinstance(step_over, dict):
                steps.append(StepConfig(name=step.name, params=deep_merge(dict(step.params), step_over)))
            else:
                steps.append(step)
        cfg = PipelineConfig(steps=tuple(steps))

    storage = FileStorage()
    docs = storage.read_docs(str(args.input_csv))

    ok_docs: list[RawDoc] = []
    for doc_res in docs:
        if isinstance(doc_res, Ok):
            ok_docs.append(doc_res.value)
        else:
            return _render(Err(doc_res.error))

    pipe = build_rag_pipeline(cfg)
    results = pipe(iter(ok_docs))
    # minimal sink: force execution and report first error if any
    for out_res in results:
        if isinstance(out_res, Err):
            return _render(out_res)
    return 0


__all__ = ["main"]
