from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def main() -> int:
    cap = Path(__file__).resolve().parents[1]
    nginx = shutil.which("nginx")
    if nginx is None:
        raise SystemExit("nginx is not available")
    snippet = (cap / "nginx" / "atlas.conf").read_text(encoding="utf-8")
    snippet = snippet.replace("listen 443 ssl;", "listen 127.0.0.1:18444 ssl;")
    snippet = snippet.replace("listen [::]:443 ssl;", "listen [::1]:18444 ssl;")
    snippet = snippet.replace("server_name atlas.example.invalid;", "server_name atlas.test;")
    snippet = snippet.replace("/etc/atlas/tls/atlas.crt", str(cap / "pki" / "atlas.crt"))
    snippet = snippet.replace("/etc/atlas/tls/atlas.key", str(cap / "pki" / "atlas.key"))

    with tempfile.TemporaryDirectory(prefix="atlas-nginx-") as raw:
        root = Path(raw)
        (root / "logs").mkdir()
        config = root / "nginx.conf"
        config.write_text(
            "worker_processes 1;\n"
            "error_log stderr notice;\n"
            "pid logs/nginx.pid;\n"
            "events { worker_connections 64; }\n"
            "http {\n" + snippet + "\n}\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [nginx, "-t", "-p", str(root), "-c", str(config)],
            text=True,
            capture_output=True,
        )
        report = {
            "command": result.args,
            "returnCode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        target = cap / "reports" / "nginx.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        if result.returncode != 0:
            raise SystemExit(result.stderr or result.stdout)
    print("PASS Nginx reference syntax")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
