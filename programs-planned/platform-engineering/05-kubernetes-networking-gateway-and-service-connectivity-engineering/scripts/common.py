from __future__ import annotations
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]

def fail(message:str)->None:
    print(f"FAIL {message}"); raise SystemExit(1)

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()

def markdown_headings(path:Path,prefix:str='## ')->list[str]:
    return [line[len(prefix):].strip() for line in path.read_text().splitlines() if line.startswith(prefix)]

def json_load(path:Path): return json.loads(path.read_text())
