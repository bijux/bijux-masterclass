#!/usr/bin/env python3
"""Wait until an HTTP endpoint returns a non-5xx status."""
from __future__ import annotations

import argparse
import time
import urllib.error
import urllib.request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--seconds", type=float, default=60)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    deadline = time.monotonic() + args.seconds
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(args.url, timeout=2) as response:
                if response.status < 500:
                    print(args.url)
                    return
                last_error = RuntimeError(
                    f"endpoint returned HTTP {response.status}"
                )
        except (OSError, urllib.error.URLError) as exc:
            last_error = exc
        time.sleep(0.25)

    detail = f": {last_error}" if last_error is not None else ""
    raise SystemExit(f"timed out waiting for {args.url}{detail}")


if __name__ == "__main__":
    main()
