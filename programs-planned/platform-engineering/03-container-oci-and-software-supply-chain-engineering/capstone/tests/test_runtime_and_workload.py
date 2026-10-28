from __future__ import annotations

import json
import subprocess
from pathlib import Path

from atlas_container.runtime_config import atlas_runtime_config, validate_runtime_config

CAPSTONE = Path(__file__).resolve().parents[1]
WORKLOAD = CAPSTONE / "workload"


def test_runtime_profile_is_nonroot_readonly_namespaced_and_bounded() -> None:
    config = atlas_runtime_config()
    assert validate_runtime_config(config) == []
    namespaces = {item["type"] for item in config["linux"]["namespaces"]}
    assert {"pid", "mount", "uts", "ipc", "network", "user"}.issubset(namespaces)
    assert config["root"]["readonly"] is True
    assert config["process"]["user"] == {"uid": 65532, "gid": 65532}
    assert all(not values for values in config["process"]["capabilities"].values())


def test_root_writable_root_and_docker_socket_are_rejected() -> None:
    config = atlas_runtime_config()
    config["process"]["user"]["uid"] = 0
    config["root"]["readonly"] = False
    config["mounts"].append(
        {
            "destination": "/var/run/docker.sock",
            "source": "/var/run/docker.sock",
            "type": "bind",
        }
    )
    errors = validate_runtime_config(config)
    assert any("UID 0" in error for error in errors)
    assert any("read-only" in error for error in errors)
    assert any("forbidden mount" in error for error in errors)


def test_containerfiles_have_explicit_frontend_builder_input_and_minimal_runtime() -> None:
    for path in sorted(WORKLOAD.glob("Containerfile.*")):
        text = path.read_text()
        assert text.startswith("# syntax=docker.io/docker/dockerfile-upstream:1.26.0")
        assert "ARG GO_BASE=" in text
        assert "FROM --platform=$BUILDPLATFORM ${GO_BASE} AS build" in text
        assert "FROM scratch" in text
        runtime = text.split("FROM scratch", 1)[1]
        assert "USER 65532:65532" in runtime
        assert "ENTRYPOINT [" in runtime
        assert "RUN " not in runtime


def test_context_excludes_private_material() -> None:
    ignore = (WORKLOAD / ".containerignore").read_text()
    for pattern in ("*.key", "*.pem", ".git", "reports"):
        assert pattern in ignore
    for path in WORKLOAD.rglob("*"):
        if path.is_file():
            assert "BEGIN PRIVATE KEY" not in path.read_text(errors="ignore")


def test_go_programs_compile_for_both_declared_architectures(tmp_path: Path) -> None:
    targets = ("atlas-api", "atlas-worker", "atlas-probe")
    for arch in ("amd64", "arm64"):
        for target in targets:
            output = tmp_path / f"{target}-{arch}"
            result = subprocess.run(
                [
                    "go",
                    "build",
                    "-trimpath",
                    "-ldflags=-s -w -buildid=",
                    "-o",
                    str(output),
                    f"./cmd/{target}",
                ],
                cwd=WORKLOAD,
                env={
                    **__import__("os").environ,
                    "CGO_ENABLED": "0",
                    "GOOS": "linux",
                    "GOARCH": arch,
                },
                text=True,
                capture_output=True,
            )
            assert result.returncode == 0, result.stderr
            assert output.read_bytes().startswith(b"\x7fELF")
