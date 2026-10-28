#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from common import ROOT, excluded
files=[]
for p in sorted(x for x in ROOT.rglob('*') if x.is_file() and not excluded(x)):
    files.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':oct(p.stat().st_mode&0o777)})
manifest={'schemaVersion':'1.0','course':'platform-engineering-course-07','files':files}
raw=json.dumps(manifest,indent=2,sort_keys=True)+'\n'; (ROOT/'MANIFEST.json').write_text(raw)
(ROOT/'MANIFEST.sha256').write_text(hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest()+'  MANIFEST.json\n')
print(f"PASS course manifest — {len(files)} files")
