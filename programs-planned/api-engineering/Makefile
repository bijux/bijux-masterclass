SHELL := /bin/bash
PYTHON ?= python3
TOOL := $(PYTHON) scripts/program_tool.py
COURSES := \
  01-openapi-contract-engineering \
  02-contract-driven-api-service-engineering \
  03-api-security-engineering \
  04-api-reliability-and-observability-engineering \
  05-api-performance-capacity-and-traffic-engineering \
  06-event-driven-api-engineering \
  07-grpc-and-protobuf-engineering \
  08-distributed-api-architecture-and-microservices-engineering \
  09-graphql-schema-and-runtime-engineering \
  10-api-platform-governance-and-developer-experience-engineering

.PHONY: help doctor structure nav-proof handoff-proof links quality syntax curriculum-fences \
 data-proof hygiene release-proof course-proofs core-proof inventory manifest manifest-proof \
 docs-build docs-serve package clean

help:
	@printf '%s\n' \
	  'API Engineering — ten-course reader-first program' \
	  '' \
	  'Study and editorial proofs:' \
	  '  make structure       Verify ten courses, 100 modules, and the standard reader shape.' \
	  '  make nav-proof       Verify all 623 learner pages are navigated exactly once.' \
	  '  make handoff-proof   Verify all nine adjacent handoffs byte-for-byte.' \
	  '  make links           Verify learner-facing local Markdown links.' \
	  '  make quality         Verify chapter depth, Q/A parity, labs, checkpoints, and repetition.' \
	  '' \
	  'Code and data:' \
	  '  make syntax          Verify Python and JavaScript syntax.' \
	  '  make curriculum-fences Verify Python/TypeScript/JavaScript examples in course books.' \
	  '  make data-proof      Parse JSON, YAML with duplicate-key detection, and TOML.' \
	  '' \
	  'Program proofs:' \
	  '  make release-proof   Run all dependency-light program release gates.' \
	  '  make course-proofs   Run every course-local dependency-light core proof.' \
	  '  make core-proof      Run release-proof and all ten course proofs.' \
	  '' \
	  'Release:' \
	  '  make manifest        Rebuild the exact program payload manifest.' \
	  '  make manifest-proof  Verify every manifested byte.' \
	  '  make package         Build and clean-extract a deterministic repository-ready ZIP.' \
	  '  make inventory       Print the current program inventory.'

doctor:
	@$(PYTHON) --version
	@node --version
	@tsc --version
	@$(MAKE) --version | head -n 1
	@$(PYTHON) -c 'import yaml; print("PyYAML", yaml.__version__)'

structure nav-proof handoff-proof links quality curriculum-fences data-proof hygiene release-proof course-proofs core-proof inventory manifest manifest-proof:
	@$(TOOL) $@

syntax:
	@$(TOOL) python-syntax
	@$(TOOL) javascript-syntax

docs-build:
	@command -v mkdocs >/dev/null || { echo 'mkdocs is unavailable; install the pinned documentation environment'; exit 2; }
	@mkdocs build --strict

docs-serve:
	@command -v mkdocs >/dev/null || { echo 'mkdocs is unavailable; install the pinned documentation environment'; exit 2; }
	@mkdocs serve

package:
	@$(PYTHON) scripts/package_release.py \
	  --output /mnt/data/api-engineering-ten-course-final.zip \
	  --prefix programs/api-engineering \
	  --checksum /mnt/data/api-engineering-ten-course-final.zip.sha256 \
	  --report /mnt/data/api-engineering-ten-course-final.release.json

clean:
	@set -e; for course in $(COURSES); do $(MAKE) -C "$$course" clean || true; done
	@rm -rf site .pytest_cache .runtime work
	@find . -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.runtime' -o -name 'site' \) -prune -exec rm -rf {} +
	@find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '.DS_Store' \) -delete
