SHELL := /bin/bash
PYTHON ?= python3
TOOL := $(PYTHON) scripts/program_tool.py
COURSES := \
  01-openapi-contract-engineering \
  02-contract-driven-api-service-engineering \
  03-api-security-engineering \
  04-api-reliability-and-observability-engineering \
  05-api-performance-capacity-and-traffic-engineering \
  06-event-driven-api-engineering

.PHONY: help doctor structure nav-proof handoff-proof links quality syntax data-proof \
  release-proof course-proofs core-proof inventory manifest manifest-proof docs-build docs-serve package clean

help:
	@printf '%s\n' \
	  'API Engineering — six-course program' \
	  '' \
	  'Reader and editorial proofs:' \
	  '  make structure       Verify the six-course and sixty-module layout.' \
	  '  make nav-proof       Verify the combined 364-page documentation navigation.' \
	  '  make handoff-proof   Verify all five adjacent course handoffs byte-for-byte.' \
	  '  make links           Verify learner-facing local Markdown links.' \
	  '  make quality         Verify chapter depth, exercise parity, labs, and checkpoints.' \
	  '' \
	  'Executable proofs:' \
	  '  make release-proof   Run program-wide editorial, syntax, and data gates.' \
	  '  make course-proofs   Run all six course-local core proofs.' \
	  '  make core-proof      Run release-proof and all six course proofs.' \
	  '' \
	  'Release:' \
	  '  make manifest        Create the exact program manifest.' \
	  '  make manifest-proof  Verify the exact program payload.' \
	  '  make package         Build a deterministic repository-ready ZIP.' \
	  '  make inventory       Print the current program inventory.' \
	  '  make docs-build      Build the combined learner site with strict warnings.'

doctor:
	@$(PYTHON) --version
	@node --version
	@$(MAKE) --version | head -n 1
	@$(PYTHON) -c 'import yaml; print("PyYAML", yaml.__version__)'

structure nav-proof handoff-proof links quality data-proof release-proof course-proofs core-proof inventory manifest manifest-proof:
	@$(TOOL) $@

syntax:
	@$(TOOL) python-syntax
	@$(TOOL) javascript-syntax


docs-build:
	@command -v mkdocs >/dev/null || { echo 'mkdocs is not available; install the pinned documentation environment'; exit 2; }
	@mkdocs build --strict

docs-serve:
	@command -v mkdocs >/dev/null || { echo 'mkdocs is not available; install the pinned documentation environment'; exit 2; }
	@mkdocs serve

package:
	@$(PYTHON) scripts/package_release.py \
	  --output /mnt/data/api-engineering-six-course-final.zip \
	  --prefix programs/api-engineering \
	  --checksum /mnt/data/api-engineering-six-course-final.zip.sha256 \
	  --report /mnt/data/api-engineering-six-course-final.release.json

clean:
	@set -e; for course in $(COURSES); do $(MAKE) -C "$$course" clean; done
	@rm -rf site .pytest_cache .runtime
	@find . -path '*/reports/last-*.json' -type f -delete
	@find . -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.runtime' -o -name 'site' \) -prune -exec rm -rf {} +
	@find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
