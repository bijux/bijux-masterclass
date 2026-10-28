PYTHON ?= python3
TOOL := $(PYTHON) scripts/course_tool.py
MODULE ?= 01
TRACK ?= python

.PHONY: help doctor predecessor-proof security-case-proof vector-proof migration-proof python-proof typescript-core-proof incident-proof release-proof structure-proof markdown-link-proof education-proof hygiene-proof module-proof core-proof manifest-create manifest-proof docs-build full-proof clean

help:
	@printf '%s\n' \
	  'API Security Engineering' \
	  '  make doctor' \
	  '  make predecessor-proof' \
	  '  make module-proof MODULE=03 TRACK=python' \
	  '  make core-proof' \
	  '  make manifest-create manifest-proof' \
	  '  make docs-build      # requires pinned MkDocs environment' \
	  '  make full-proof      # core plus manifest and optional external gates'

doctor:
	$(TOOL) doctor
predecessor-proof:
	$(TOOL) predecessor-proof
security-case-proof:
	$(TOOL) security-case-proof
vector-proof:
	$(TOOL) vector-proof
migration-proof:
	$(TOOL) migration-proof
python-proof:
	$(TOOL) python-proof
typescript-core-proof:
	$(TOOL) typescript-core-proof
incident-proof:
	$(TOOL) incident-proof
release-proof:
	$(TOOL) release-proof
structure-proof:
	$(TOOL) structure-proof
markdown-link-proof:
	$(TOOL) markdown-link-proof
education-proof:
	$(TOOL) education-proof
hygiene-proof:
	$(TOOL) hygiene-proof
module-proof:
	$(TOOL) module-proof --module $(MODULE) --track $(TRACK)
core-proof:
	$(TOOL) core-proof
manifest-create:
	$(TOOL) manifest-create
manifest-proof:
	$(TOOL) manifest-proof
docs-build:
	@command -v mkdocs >/dev/null || { echo 'mkdocs not available; install the pinned docs environment'; exit 2; }
	mkdocs build --strict
full-proof: core-proof manifest-proof docs-build
clean:
	rm -rf .pytest_cache capstone/tracks/python-fastapi/.pytest_cache capstone/tracks/typescript-fastify/dist-security
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
