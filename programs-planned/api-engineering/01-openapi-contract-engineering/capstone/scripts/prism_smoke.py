#!/usr/bin/env python3
from __future__ import annotations

import argparse

import httpx


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4010")
    args = parser.parse_args()
    with httpx.Client(base_url=args.base_url, timeout=5.0) as client:
        health = client.get("/health", headers={"Prefer": "example=healthy"})
        if health.status_code != 200:
            raise SystemExit(f"Prism health smoke failed: {health.status_code} {health.text}")
        invalid = client.post(
            "/projects",
            headers={"Authorization": "Bearer learner-write", "Content-Type": "application/json"},
            json={"name": ""},
        )
        if invalid.status_code < 400:
            raise SystemExit(f"Prism accepted invalid project: {invalid.status_code} {invalid.text}")
    print("PASS Prism mock and request validation smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
