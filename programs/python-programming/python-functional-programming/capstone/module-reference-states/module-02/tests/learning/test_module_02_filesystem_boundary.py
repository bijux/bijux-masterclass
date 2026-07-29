"""Executable learning proof for Module 02's Result-bearing filesystem shell."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from funcpipe_rag import (
    Err,
    Ok,
    RagConfig,
    RagEnv,
    RawDoc,
    full_rag_api_docs,
    get_deps,
)
from funcpipe_rag.shells.rag_api_shell import run
from funcpipe_rag.shells.rag_main import boundary_app_config


def _json_value(value: object) -> object:
    return json.loads(json.dumps(value))


def test_filesystem_shell_preserves_the_configured_core_values(tmp_path: Path) -> None:
    source = tmp_path / "docs.csv"
    output = tmp_path / "chunks.jsonl"
    csv_text = (
        "doc_id,title,abstract,categories\n"
        "b,B,Local reasoning,cs.PL\n"
        "a,A,Pure values,cs.PL\n"
    )
    source.write_text(csv_text, encoding="utf-8")
    docs = [
        RawDoc("b", "B", "Local reasoning", "cs.PL"),
        RawDoc("a", "A", "Pure values", "cs.PL"),
    ]
    config = RagConfig(env=RagEnv(chunk_size=5))

    result = run(str(source), str(output), config=config)

    assert isinstance(result, Ok)
    expected_chunks, expected_observations = full_rag_api_docs(
        docs,
        config,
        get_deps(config),
    )
    actual_chunks = [
        json.loads(line)
        for line in output.read_text(encoding="utf-8").splitlines()
    ]
    assert actual_chunks == [
        _json_value(asdict(chunk))
        for chunk in expected_chunks
    ]
    assert result.value == expected_observations
    assert source.read_text(encoding="utf-8") == csv_text


def test_filesystem_shell_writes_empty_output_for_header_only_csv(
    tmp_path: Path,
) -> None:
    source = tmp_path / "empty.csv"
    output = tmp_path / "chunks.jsonl"
    source.write_text(
        "doc_id,title,abstract,categories\n",
        encoding="utf-8",
    )

    result = run(
        str(source),
        str(output),
        config=RagConfig(env=RagEnv(chunk_size=5)),
    )

    assert isinstance(result, Ok)
    assert result.value.total_docs == 0
    assert result.value.total_chunks == 0
    assert output.read_text(encoding="utf-8") == ""


def test_filesystem_shell_returns_parse_failure_before_writing(
    tmp_path: Path,
) -> None:
    source = tmp_path / "invalid.csv"
    output = tmp_path / "chunks.jsonl"
    source.write_text(
        "doc_id,title,abstract\n"
        "a,A,Pure values\n",
        encoding="utf-8",
    )

    result = run(
        str(source),
        str(output),
        config=RagConfig(env=RagEnv(chunk_size=5)),
    )

    assert isinstance(result, Err)
    assert result.error.startswith("Load failed:")
    assert not output.exists()


def test_filesystem_shell_returns_missing_input_failure(tmp_path: Path) -> None:
    source = tmp_path / "missing.csv"
    output = tmp_path / "chunks.jsonl"

    result = run(
        str(source),
        str(output),
        config=RagConfig(env=RagEnv(chunk_size=5)),
    )

    assert isinstance(result, Err)
    assert result.error.startswith("Load failed:")
    assert not output.exists()


def test_filesystem_shell_returns_output_failure_after_core_work(
    tmp_path: Path,
) -> None:
    source = tmp_path / "docs.csv"
    output = tmp_path / "missing-parent" / "chunks.jsonl"
    source.write_text(
        "doc_id,title,abstract,categories\n"
        "a,A,Pure values,cs.PL\n",
        encoding="utf-8",
    )

    result = run(
        str(source),
        str(output),
        config=RagConfig(env=RagEnv(chunk_size=5)),
    )

    assert isinstance(result, Err)
    assert result.error.startswith("Write failed:")
    assert not output.exists()


def test_app_config_rejects_unknown_clean_rule_before_execution() -> None:
    result = boundary_app_config(
        [
            "--input",
            "docs.csv",
            "--output",
            "chunks.jsonl",
            "--clean_rules",
            "strip,unknown",
        ]
    )

    assert isinstance(result, Err)
    assert "unknown clean rule" in result.error
