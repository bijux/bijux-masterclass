#!/usr/bin/env python3
from common import COURSE, passed
import shutil
for path in COURSE.rglob("__pycache__"): shutil.rmtree(path,ignore_errors=True)
for path in COURSE.rglob(".pytest_cache"): shutil.rmtree(path,ignore_errors=True)
for name in ("capstone-tour.json","kind-objects.yaml","kind-events.yaml","kind-kubeconfig"):
    path=COURSE/"capstone"/"reports"/name
    path.unlink(missing_ok=True)
binary=COURSE/"capstone"/"controller-go"/"atlas-controller"
binary.unlink(missing_ok=True)
passed("generated proof output cleaned")
