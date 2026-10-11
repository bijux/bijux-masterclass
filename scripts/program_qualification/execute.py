"""Execute a named program profile, or reuse an exact trusted qualification."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from .github import find_saved_qualification
from .inputs import fingerprint, program_inputs, runtime_inputs
from .profiles import FAST_TESTS, FULL_COMMANDS
from .provenance import REPOSITORY

ROOT = Path(__file__).resolve().parents[2]


def run(command: list[str], *, cwd: Path, env: dict[str, str], log: Path) -> None:
    print("Executing:", " ".join(command), flush=True)
    with log.open("w") as output:
        child = subprocess.run(
            command,
            check=False,
            cwd=cwd,
            env=env,
            stdout=output,
            stderr=subprocess.STDOUT,
        )
    print(log.read_text(errors="replace"), end="", flush=True)
    if child.returncode:
        raise subprocess.CalledProcessError(child.returncode, command)


def prepare(program: str, venv: Path, artifacts: Path, env: dict[str, str]) -> Path:
    capstone = ROOT / "programs" / program / "capstone"
    if program == "reproducible-research/deep-dive-snakemake":
        command = [
            "make",
            "bootstrap",
            f"TOOLS_VENV_DIR={venv}",
            f"SYSTEM_PYTHON={sys.executable}",
        ]
    else:
        variable = (
            "VENV_DIR" if program == "reproducible-research/deep-dive-dvc" else "VENV"
        )
        command = ["make", "install", f"{variable}={venv}", f"PYTHON={sys.executable}"]
    run(command, cwd=capstone, env=env, log=artifacts / "prepare.log")
    python = venv / "bin/python"
    if not python.is_file():
        raise ValueError("program preparation did not produce its admitted interpreter")
    return python


def dvc_smoke(program: str, python: Path, artifacts: Path, env: dict[str, str]) -> None:
    workspace_root = Path(tempfile.mkdtemp(prefix="pipeline-", dir=artifacts))
    prefix = f"programs/{program}/capstone/"
    workspace = workspace_root / prefix
    workspace.mkdir(parents=True)
    # Keep the published relative interpreter contract unchanged in the isolated
    # fixture. Both the link and its admitted target are repository artifacts.
    published_environment = workspace_root / "artifacts/venv" / program / "capstone"
    published_environment.parent.mkdir(parents=True)
    published_environment.symlink_to(python.parent.parent, target_is_directory=True)
    tracked = (
        subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        .decode()
        .split("\0")
    )
    for relative in filter(lambda value: value.startswith(prefix), tracked):
        source = ROOT / relative
        destination = workspace / relative.removeprefix(prefix)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            raise ValueError("pipeline fixture cannot borrow external symlink inputs")
        shutil.copyfile(source, destination)
    subprocess.run(["git", "init", "--quiet", str(workspace)], check=True)
    if not (workspace / ".dvc").is_dir():
        run(
            [str(python), "-m", "dvc", "init", "--quiet"],
            cwd=workspace,
            env=env,
            log=artifacts / "smoke-init.log",
        )
    run(
        [str(python), "-m", "dvc", "repro"],
        cwd=workspace,
        env=env,
        log=artifacts / "smoke-pipeline.log",
    )
    run(
        [
            str(python),
            "-m",
            "incident_escalation_capstone.verify",
            "--publish",
            "publish/v1",
        ],
        cwd=workspace,
        env=env,
        log=artifacts / "smoke-verification.log",
    )


def execute(program: str, profile: str, output: Path, venv: Path | None = None) -> dict:
    if profile not in {"fast", "full"} or program not in FAST_TESTS:
        raise ValueError("unsupported program qualification profile")
    if not output.is_absolute():
        output = ROOT / output
    output.resolve().relative_to((ROOT / "artifacts").resolve())
    artifacts = output.parent
    artifacts.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)
    started = time.monotonic()
    sources = program_inputs(ROOT, program)
    (artifacts / "inputs-before.json").write_text(
        json.dumps(sources, indent=2, sort_keys=True) + "\n"
    )
    timings = {}
    checkpoint = started
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    for overlay in ("PYTEST_ADDOPTS", "PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP"):
        env.pop(overlay, None)
    env["PYTHONNOUSERSITE"] = "1"
    env["TMPDIR"] = str(artifacts / "tmp")
    Path(env["TMPDIR"]).mkdir(exist_ok=True)
    venv = venv or artifacts / "venv"
    python = prepare(program, venv, artifacts, env)
    timings["preparation_seconds"] = round(time.monotonic() - checkpoint, 3)
    checkpoint = time.monotonic()
    env["PATH"] = str(venv / "bin") + os.pathsep + env["PATH"]
    tests = FAST_TESTS[program]
    lock = ROOT / "programs" / program / "capstone/requirements-tools.lock"
    identity = {
        "program": program,
        "profile": profile,
        "sources": sources,
        "runtime": runtime_inputs(python, env),
        "tests": tests if profile == "fast" else "published confirmation",
        "dependencies_locked": program == "reproducible-research/deep-dive-snakemake"
        and lock.is_file(),
        "environment_policy": {
            "PYTHONHASHSEED": "0",
            "PYTHONNOUSERSITE": "1",
            "import_overlays": "cleared",
            "PYTEST_ADDOPTS": "cleared",
        },
    }
    if any(
        not package["installed_record"] for package in identity["runtime"]["packages"]
    ):
        identity["dependencies_locked"] = False
    timings["runtime_admission_seconds"] = round(time.monotonic() - checkpoint, 3)
    checkpoint = time.monotonic()
    saved = None
    name = program.split("/")[-1] + "-" + profile
    if os.environ.get("GITHUB_REPOSITORY") == REPOSITORY:
        saved = find_saved_qualification(
            ROOT, identity, "program-qualification-" + name
        )
    timings["trusted_lookup_seconds"] = round(time.monotonic() - checkpoint, 3)
    checkpoint = time.monotonic()
    if saved is None:
        if profile == "full":
            # Complete confirmation is an explicit manual route. Its published
            # selftests and output checks retain their original command identity.
            command = FULL_COMMANDS.get(program, ["make", f"PROGRAM={program}", "test"])
            if program == "reproducible-research/deep-dive-snakemake":
                full_venv = artifacts / "clean-room-venv"
                command = [
                    *command,
                    f"TOOLS_VENV_DIR={full_venv}",
                    f"SYSTEM_PYTHON={sys.executable}",
                ]
            else:
                variable = (
                    "VENV_DIR"
                    if program == "reproducible-research/deep-dive-dvc"
                    else "VENV"
                )
                command = [*command, f"{variable}={venv}", f"PYTHON={sys.executable}"]
            run(command, cwd=ROOT, env=env, log=artifacts / "full-confirmation.log")
            if program == "reproducible-research/deep-dive-snakemake":
                python = full_venv / "bin/python"
                identity["runtime"] = runtime_inputs(python, env)
        else:
            for test in tests:
                if not (
                    ROOT / "programs" / program / "capstone" / test.split("::")[0]
                ).exists():
                    raise ValueError(
                        f"required representative contract is missing: {test}"
                    )
            junit = artifacts / "tests.xml"
            command = [
                str(python),
                "-m",
                "pytest",
                "-q",
                "--strict-markers",
                "--durations=0",
                "-o",
                f"cache_dir={artifacts / 'pytest-cache'}",
                f"--basetemp={artifacts / 'pytest-tmp'}",
                f"--junitxml={junit}",
                *tests,
            ]
            run(
                command,
                cwd=ROOT / "programs" / program / "capstone",
                env=env,
                log=artifacts / "tests.log",
            )
            import xml.etree.ElementTree as ET

            cases = ET.parse(junit).getroot().findall(".//testcase")
            if not cases or any(case.find("skipped") is not None for case in cases):
                raise ValueError(
                    "representative PR contracts must execute without skipped cases"
                )
            if program == "reproducible-research/deep-dive-dvc":
                dvc_smoke(program, python, artifacts, env)
    timings["validation_seconds"] = round(time.monotonic() - checkpoint, 3)
    if identity["runtime"] != runtime_inputs(python, env):
        raise ValueError("program execution changed admitted runtime payloads")
    observed = program_inputs(ROOT, program)
    (artifacts / "inputs-after.json").write_text(
        json.dumps(observed, indent=2, sort_keys=True) + "\n"
    )
    timings["elapsed_seconds"] = round(time.monotonic() - started, 3)
    (artifacts / "timings.json").write_text(
        json.dumps(timings, indent=2, sort_keys=True) + "\n"
    )
    if sources != observed:
        changed = sorted(
            path
            for path in sources.keys() | observed.keys()
            if sources.get(path) != observed.get(path)
        )
        (artifacts / "input-refusal.json").write_text(
            json.dumps({"changed_paths": changed, "result": "refused"}, indent=2) + "\n"
        )
        raise ValueError(
            "program execution changed qualification inputs: " + ", ".join(changed)
        )
    clean = not subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=normal"],
        cwd=ROOT,
        text=True,
    ).strip()
    receipt = {
        "schema_version": 1,
        "worktree_clean": clean,
        "execution_context": "committed tree" if clean else "local input snapshot",
        "timings": timings,
        "result": "success",
        "identity": identity,
        "input_digest": fingerprint(identity),
        "execution": "executed" if saved is None else "reused",
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "run_id": int(os.environ.get("GITHUB_RUN_ID", "0")),
        "run_attempt": int(os.environ.get("GITHUB_RUN_ATTEMPT", "0")),
        "job_name": name,
        "execution_tree": subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True
        ).strip(),
        "execution_sha": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "reused_from": saved,
        "scientific_scope": "representative PR contracts"
        if profile == "fast"
        else "complete published confirmation",
    }
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "profile": profile,
                "input_digest": receipt["input_digest"],
                "execution": receipt["execution"],
                "elapsed_seconds": receipt["elapsed_seconds"],
            }
        )
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--program", choices=sorted(FAST_TESTS), required=True)
    parser.add_argument("--profile", choices=["fast", "full"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--venv", type=Path)
    args = parser.parse_args()
    execute(args.program, args.profile, args.output, args.venv)


if __name__ == "__main__":
    main()
