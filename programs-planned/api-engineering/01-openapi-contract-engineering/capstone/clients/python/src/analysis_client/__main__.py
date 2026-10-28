from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from .client import AnalysisClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Analysis Runs API example workflow")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    credentials = parser.add_mutually_exclusive_group(required=True)
    credentials.add_argument("--token")
    credentials.add_argument("--api-key")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "dataset.csv"
        path.write_text("sample,value\nA,1\n", encoding="utf-8")
        with AnalysisClient(
            args.base_url,
            bearer_token=args.token,
            api_key=args.api_key,
        ) as client:
            result = client.complete_workflow(
                project_name="Python client demo",
                dataset_path=path,
                idempotency_key="python-client-demo-0001",
            )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
