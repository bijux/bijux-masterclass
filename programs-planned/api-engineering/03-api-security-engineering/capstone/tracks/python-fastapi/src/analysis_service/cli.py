from __future__ import annotations
import argparse
from pathlib import Path
from .config import Settings
from .migrations import apply_migrations

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['migrate'])
    p.add_argument('--migrations', type=Path, default=Path(__file__).parents[2] / 'migrations')
    p.add_argument('--target')
    a = p.parse_args()
    s = Settings.from_env()
    for version in apply_migrations(s.database_url, a.migrations, a.target):
        print(version)
if __name__ == '__main__':
    main()
