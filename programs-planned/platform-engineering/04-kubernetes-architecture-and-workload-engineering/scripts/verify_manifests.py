#!/usr/bin/env python3
from common import CAPSTONE, fail, passed
import sys
sys.path.insert(0,str(CAPSTONE))
from atlas_kube.validation import validate_tree
for lane in ("base","controller","labs"):
    findings=validate_tree(CAPSTONE/"manifests"/lane)
    if findings: fail("manifest policy:\n"+"\n".join(findings))
passed("production-intent and laboratory manifest policy")
