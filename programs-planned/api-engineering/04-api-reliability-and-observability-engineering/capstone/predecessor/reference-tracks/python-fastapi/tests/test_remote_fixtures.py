from __future__ import annotations

from pathlib import Path

import pytest

from analysis_service.remote_fixtures import (
    RemoteFixtureError,
    resolve_remote_fixture,
)


def test_resolves_regular_file_under_approved_origin(tmp_path: Path) -> None:
    target = tmp_path / "cohort" / "reads.csv"
    target.parent.mkdir()
    target.write_text("sample,value\na,1\n", encoding="utf-8")

    resolved = resolve_remote_fixture(
        tmp_path,
        "https://objects.example.test/cohort/reads.csv",
    )

    assert resolved == target.resolve()


@pytest.mark.parametrize(
    "uri",
    [
        "http://objects.example.test/cohort/reads.csv",
        "https://evil.example.test/cohort/reads.csv",
        "https://user@objects.example.test/cohort/reads.csv",
        "https://objects.example.test:444/cohort/reads.csv",
        "https://objects.example.test/cohort/reads.csv?version=1",
        "https://objects.example.test/cohort/reads.csv#part",
        "https://objects.example.test/%2e%2e/secret.txt",
        "https://objects.example.test/cohort/../secret.txt",
    ],
)
def test_rejects_untrusted_or_traversing_uri(
    tmp_path: Path,
    uri: str,
) -> None:
    tmp_path.mkdir(exist_ok=True)
    with pytest.raises(RemoteFixtureError):
        resolve_remote_fixture(tmp_path, uri)


def test_rejects_final_symbolic_link(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside.txt"
    outside.write_text("secret", encoding="utf-8")
    link = tmp_path / "link.txt"
    try:
        link.symlink_to(outside)
    except OSError as exc:  # pragma: no cover - platform permission boundary
        pytest.skip(f"symbolic links are unavailable: {exc}")

    with pytest.raises(RemoteFixtureError, match="symbolic link"):
        resolve_remote_fixture(
            tmp_path,
            "https://objects.example.test/link.txt",
        )


def test_rejects_symbolic_link_in_parent_component(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside-directory"
    outside.mkdir()
    (outside / "reads.csv").write_text("secret", encoding="utf-8")
    link = tmp_path / "cohort"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError as exc:  # pragma: no cover - platform permission boundary
        pytest.skip(f"symbolic links are unavailable: {exc}")

    with pytest.raises(RemoteFixtureError, match="symbolic link"):
        resolve_remote_fixture(
            tmp_path,
            "https://objects.example.test/cohort/reads.csv",
        )
