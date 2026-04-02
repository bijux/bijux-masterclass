from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()

    if not args.config.is_file():
        raise FileNotFoundError(f"missing config file: {args.config}")
    if not args.schema.is_file():
        raise FileNotFoundError(f"missing schema file: {args.schema}")

    try:
        import jsonschema
    except ImportError:
        print("SKIP: jsonschema not installed")
        return 0

    try:
        import yaml
    except ImportError:
        print("SKIP: pyyaml not installed")
        return 0

    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    schema = yaml.safe_load(args.schema.read_text(encoding="utf-8"))
    jsonschema.validate(config, schema)
    print("PASS: config validates against schema")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
