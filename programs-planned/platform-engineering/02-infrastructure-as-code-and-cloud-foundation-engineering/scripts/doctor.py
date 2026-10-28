from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys


def version(command: list[str]) -> str | None:
    if shutil.which(command[0]) is None:
        return None
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=10, check=False)
    except Exception:
        return "present-version-unavailable"
    text = (result.stdout or result.stderr).strip().splitlines()
    return text[0] if text else "present"


def main() -> int:
    tools = {
        "python": platform.python_version(),
        "pytest": version([sys.executable, "-m", "pytest", "--version"]),
        "openssl": version(["openssl", "version"]),
        "node": version(["node", "--version"]),
        "opentofu": version(["tofu", "version"]),
        "aws": version(["aws", "--version"]),
        "mkdocs": version(["mkdocs", "--version"]),
        "shellcheck": version(["shellcheck", "--version"]),
    }
    report = {
        "platform": platform.platform(),
        "tools": tools,
        "dependencyLightReady": sys.version_info >= (3, 12) and tools["pytest"] is not None,
        "opentofuReady": tools["opentofu"] is not None,
        "awsReady": tools["aws"] is not None,
        "docsReady": tools["mkdocs"] is not None,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["dependencyLightReady"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
