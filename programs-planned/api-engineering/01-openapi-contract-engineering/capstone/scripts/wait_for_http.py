#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

import httpx


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--attempts", type=int, default=60)
    parser.add_argument("--interval", type=float, default=0.1)
    args = parser.parse_args()
    for _ in range(args.attempts):
        try:
            response = httpx.get(args.url, timeout=1.0)
            if response.status_code < 500:
                return 0
        except httpx.HTTPError:
            pass
        time.sleep(args.interval)
    raise SystemExit(f"service did not become ready: {args.url}")


if __name__ == "__main__":
    raise SystemExit(main())
