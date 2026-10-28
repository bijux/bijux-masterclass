#!/usr/bin/env python3
"""Controlled telemetry-loss stage from the Course 4 game day.

The script requires ALLOW_GAME_DAY=1 and Docker. It proves one bounded claim:
collector loss must not make either API fail liveness or readiness. Worker-loss
and webhook-degradation stages remain separate labs because they require a
prepared durable run and explicit operator roles.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import time
from urllib.request import urlopen


def health(base: str, route: str) -> dict[str, object]:
    with urlopen(base + route, timeout=5) as response:
        if response.status != 200:
            raise RuntimeError(f"{base}{route} returned {response.status}")
        return json.loads(response.read())


def compose(course: Path, *args: str) -> None:
    command = [
        "docker",
        "compose",
        "-f",
        str(course / "capstone" / "observability" / "compose.yaml"),
        *args,
    ]
    result = subprocess.run(command, text=True)
    if result.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(command)}")


def main() -> None:
    if os.environ.get("ALLOW_GAME_DAY") != "1":
        raise SystemExit("set ALLOW_GAME_DAY=1 to authorize the controlled fault")
    course = Path(__file__).resolve().parents[3]
    bases = [
        os.environ.get("PYTHON_API_URL", "http://127.0.0.1:58000"),
        os.environ.get("TYPESCRIPT_API_URL", "http://127.0.0.1:58001"),
    ]
    before = [(health(base, "/internal/health/live"), health(base, "/internal/health/ready")) for base in bases]
    if any(item[0].get("live") is not True or item[1].get("ready") is not True for item in before):
        raise SystemExit("steady state is not healthy; aborting fault injection")

    try:
        compose(course, "stop", "otel-collector")
        time.sleep(3)
        during = [(health(base, "/internal/health/live"), health(base, "/internal/health/ready")) for base in bases]
        if any(item[0].get("live") is not True or item[1].get("ready") is not True for item in during):
            raise SystemExit("collector loss changed API liveness/readiness")
    finally:
        compose(course, "start", "otel-collector")

    print(
        "PASS controlled game-day stage — telemetry collector loss did not gate "
        "customer-serving liveness or readiness; collector restored"
    )


if __name__ == "__main__":
    main()
