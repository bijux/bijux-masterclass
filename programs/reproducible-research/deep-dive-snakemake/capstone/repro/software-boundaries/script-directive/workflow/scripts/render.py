from pathlib import Path

SOFTWARE_MARKER = "script-directive-v1"

source = Path(snakemake.input.source)  # type: ignore[name-defined]  # noqa: F821
artifact = Path(snakemake.output.artifact)  # type: ignore[name-defined]  # noqa: F821
artifact.parent.mkdir(parents=True, exist_ok=True)
artifact.write_text(
    f"{SOFTWARE_MARKER}\n{source.read_text(encoding='utf-8')}",
    encoding="utf-8",
)
