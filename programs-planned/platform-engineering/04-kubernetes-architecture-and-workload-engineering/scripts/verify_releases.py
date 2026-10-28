#!/usr/bin/env python3
from common import CAPSTONE, fail, load_json, passed
releases=[load_json(path) for path in sorted((CAPSTONE/"releases").glob("*/release.json"))]
states={r["decision"] for r in releases}
required={"accepted","rejected","review-required","not-executed"}
if not required <= states: fail(f"missing release states {required-states}")
accepted=[r for r in releases if r["decision"]=="accepted"]
if len(accepted)!=1: fail("expected one accepted release")
passed(f"release corpus — {len(releases)} candidates across {sorted(states)}")
