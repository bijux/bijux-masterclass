"""Module 09 Core 6: optional Typer CLI seam (end-of-Module-09).

The stdlib argparse shell is the canonical learner route in this repository.
This file exists only to show where a richer framework shell could attach
without changing the pure helper split or the default proof surface.
"""

# mypy: ignore-errors

from __future__ import annotations

import importlib
from typing import Any


def build_app() -> Any:
    typer = importlib.import_module("typer")
    app = typer.Typer()

    @app.command()
    def hello(name: str = "world") -> None:
        typer.echo(f"hello {name}")

    return app


__all__ = ["build_app"]
