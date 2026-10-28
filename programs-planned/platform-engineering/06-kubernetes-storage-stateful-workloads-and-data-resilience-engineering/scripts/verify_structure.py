#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, fail

book = ROOT / "course-book"
modules = sorted(path for path in book.glob("module-*") if path.is_dir())
if len(modules) != 11:
    fail(f"expected orientation plus 10 modules, got {len(modules)}")
for module in modules:
    required = {"index.md", "lab.md", "checkpoint.md"}
    if "module-00-" not in module.name:
        required |= {"exercises.md", "exercise-answers.md"}
    missing = sorted(name for name in required if not (module / name).is_file())
    if missing:
        fail(f"{module.name} missing {missing}")
for directory in ["guides", "reference", "casebook", "capstone", "assessment", "instructor"]:
    if not (book / directory).is_dir():
        fail(f"missing course-book/{directory}")
for directory in [
    "atlas_data", "tests", "manifests", "releases", "planted-defects",
    "runbooks", "shared/vectors", "handoff", "predecessor/handoff",
]:
    if not (ROOT / "capstone" / directory).exists():
        fail(f"missing capstone/{directory}")
print("PASS course structure — reader book, 10 modules, capstone, and handoffs")
