#!/usr/bin/env python3
from __future__ import annotations
import subprocess,tempfile
from pathlib import Path
from atlas_delivery.gitrepo import commit, run_git
with tempfile.TemporaryDirectory() as d:
    repo=Path(d); subprocess.run(['git','init','-q',repo],check=True)
    run_git(repo,'config','user.email','course@example.invalid'); run_git(repo,'config','user.name','Course')
    (repo/'environment.yaml').write_text('release: one\n'); first=commit(repo,'release one')
    (repo/'environment.yaml').write_text('release: two\n'); second=commit(repo,'release two')
    if first==second: raise SystemExit('FAIL commits not unique')
    run_git(repo,'revert','--no-edit',second)
    if (repo/'environment.yaml').read_text()!='release: one\n': raise SystemExit('FAIL revert did not restore content')
print('PASS local Git lineage, immutable commits, and explicit revert')
