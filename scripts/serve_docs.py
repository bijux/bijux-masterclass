#!/usr/bin/env python3
"""Serve MkDocs on the first available local address."""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
from pathlib import Path

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_PORT_SEARCH_LIMIT = 25


def positive_int(raw: str, option_name: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"{option_name} must be an integer, got {raw!r}"
        ) from exc
    if value < 1:
        raise argparse.ArgumentTypeError(f"{option_name} must be greater than zero")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Serve a MkDocs site on the first available port starting from the "
            "requested value."
        )
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to the MkDocs configuration file.",
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Host interface for the live-reload server. Default: {DEFAULT_HOST}.",
    )
    parser.add_argument(
        "--port",
        default=DEFAULT_PORT,
        type=lambda raw: positive_int(raw, "--port"),
        help=f"Preferred starting port. Default: {DEFAULT_PORT}.",
    )
    parser.add_argument(
        "--port-search-limit",
        default=DEFAULT_PORT_SEARCH_LIMIT,
        type=lambda raw: positive_int(raw, "--port-search-limit"),
        help=(
            "Number of consecutive ports to probe before failing. "
            f"Default: {DEFAULT_PORT_SEARCH_LIMIT}."
        ),
    )
    return parser.parse_args()


def port_is_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def pick_port(host: str, start_port: int, search_limit: int) -> int:
    for port in range(start_port, start_port + search_limit):
        if port_is_available(host, port):
            return port
    last_port = start_port + search_limit - 1
    raise RuntimeError(
        f"no available port found on {host} between {start_port} and {last_port}"
    )


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    if not config_path.is_file():
        raise FileNotFoundError(f"missing MkDocs config: {config_path}")

    selected_port = pick_port(args.host, args.port, args.port_search_limit)
    if selected_port != args.port:
        print(
            (
                f"Port {args.port} is already in use on {args.host}; "
                f"serving on {selected_port} instead."
            ),
            file=sys.stderr,
        )
    print(
        f"Serving docs at http://{args.host}:{selected_port}/",
        file=sys.stderr,
    )

    env = os.environ.copy()
    env["SITE_URL"] = f"http://{args.host}:{selected_port}/"

    command = [
        sys.executable,
        "-m",
        "mkdocs",
        "serve",
        "-f",
        str(config_path),
        "-a",
        f"{args.host}:{selected_port}",
    ]
    try:
        return subprocess.call(command, env=env)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
