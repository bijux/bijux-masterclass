#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, shutil, sys
from common import passed

print(f"Python {sys.version.split()[0]}")
for module in ("yaml", "pytest"):
    print(f"{module}: {'available' if importlib.util.find_spec(module) else 'missing'}")
for tool in ("go", "kubectl", "kind", "docker", "podman", "mkdocs", "kubeconform", "helm", "kustomize"):
    print(f"{tool}: {shutil.which(tool) or 'not available'}")
passed("doctor completed; missing optional tools are not converted into proof")
