#!/usr/bin/env python3
from common import COURSE, CAPSTONE, run, passed
import os, sys
python=sys.executable
env={"PYTHONPATH":str(CAPSTONE)}
steps=[
 [python,"scripts/verify_predecessor.py"],
 [python,"scripts/verify_structure.py"],
 [python,"scripts/verify_educational_quality.py"],
 [python,"scripts/verify_documents.py"],
 [python,"scripts/verify_manifests.py"],
 [python,"-m","pytest","-q","capstone/tests"],
 ["go","test","./..."],
 [python,"scripts/verify_defects.py"],
 [python,"scripts/verify_releases.py"],
 [python,"scripts/verify_handoff.py"],
 [python,"scripts/check_links.py"],
 [python,"scripts/verify_nav.py"],
 [python,"scripts/capstone_tour.py"],
]
for command in steps:
    result=run(command,cwd=COURSE if command[0]!="go" else CAPSTONE/"controller-go",env=env)
    print(result.stdout,end="")
passed("Course 4 dependency-light core proof")
