"""Executable learning proof for Module 01's CSV and JSONL shell boundary."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

import pytest
from funcpipe_rag import RagEnv, RawDoc, full_rag, rag_shell


def _json_value(value: object) -> object:
    return json.loads(json.dumps(value))


def test_shell_serializes_the_same_chunks_as_the_pure_core(tmp_path: Path) -> None:
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
    env = RagEnv(chunk_size=5)

    rag_shell(env, str(source), str(output))

    actual = [
        json.loads(line)
        for line in output.read_text(encoding="utf-8").splitlines()
    ]
    expected = [_json_value(asdict(chunk)) for chunk in full_rag(docs, env)]
    assert actual == expected
    assert source.read_text(encoding="utf-8") == csv_text


def test_shell_writes_empty_output_for_header_only_csv(tmp_path: Path) -> None:
    source = tmp_path / "empty.csv"
    output = tmp_path / "chunks.jsonl"
    source.write_text(
        "doc_id,title,abstract,categories\n",
        encoding="utf-8",
    )

    rag_shell(RagEnv(chunk_size=5), str(source), str(output))

    assert output.read_text(encoding="utf-8") == ""


def test_shell_translates_invalid_row_shape_before_writing(tmp_path: Path) -> None:
    source = tmp_path / "invalid.csv"
    output = tmp_path / "chunks.jsonl"
    source.write_text(
        "doc_id,title,abstract\n"
        "a,A,Pure values\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=str(source)):
        rag_shell(RagEnv(chunk_size=5), str(source), str(output))

    assert not output.exists()


def test_shell_propagates_missing_input_path(tmp_path: Path) -> None:
    source = tmp_path / "missing.csv"
    output = tmp_path / "chunks.jsonl"

    with pytest.raises(FileNotFoundError):
        rag_shell(RagEnv(chunk_size=5), str(source), str(output))

    assert not output.exists()
