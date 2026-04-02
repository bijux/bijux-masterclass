from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def load_provenance_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "workflow" / "scripts" / "provenance.py"
    )
    spec = importlib.util.spec_from_file_location("snakemake_provenance", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_resolve_snakemake_version_prefers_import(monkeypatch) -> None:
    module = load_provenance_module()
    monkeypatch.setattr(
        module.importlib,
        "import_module",
        lambda name: SimpleNamespace(__version__="9.14.3"),
    )

    version = module.resolve_snakemake_version("python3")

    assert version == "9.14.3"


def test_resolve_snakemake_version_falls_back_to_subprocess(monkeypatch) -> None:
    module = load_provenance_module()

    def raise_import_error(name: str):
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(module.importlib, "import_module", raise_import_error)
    monkeypatch.setattr(
        module.subprocess,
        "check_output",
        lambda command, text=True: "9.14.4\n",
    )

    version = module.resolve_snakemake_version("python3")

    assert version == "9.14.4"
