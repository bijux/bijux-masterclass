#!/usr/bin/env python3
"""Create a deterministic repository-ready ZIP from the exact course manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

FIXED_TIME=(2026,8,8,0,0,0)


def build(root: Path, output: Path) -> None:
    manifest=json.loads((root/'MANIFEST.json').read_text())
    paths=[item['path'] for item in manifest['files']]+['MANIFEST.json','MANIFEST.sha256']
    prefix=PurePosixPath('programs')/'api-engineering'/root.name
    names=[]
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for rel in sorted(paths):
            source=root/rel
            if not source.is_file(): raise SystemExit(f'missing release file: {rel}')
            name=(prefix/PurePosixPath(rel)).as_posix()
            pure=PurePosixPath(name)
            if pure.is_absolute() or '..' in pure.parts: raise SystemExit(f'unsafe ZIP path: {name}')
            info=zipfile.ZipInfo(name,FIXED_TIME)
            info.compress_type=zipfile.ZIP_DEFLATED
            mode=source.stat().st_mode
            info.external_attr=((stat.S_IFREG | (mode & 0o777)) << 16)
            info.create_system=3
            archive.writestr(info,source.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
            names.append(name)
    if len(names)!=len(set(names)): raise SystemExit('duplicate ZIP member')
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None: raise SystemExit('ZIP CRC failure')
    print(f'wrote {output} — {len(names)} files')


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('output')
    parser.add_argument('--root',default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    build(Path(args.root).resolve(),Path(args.output).resolve())

if __name__=='__main__': main()
