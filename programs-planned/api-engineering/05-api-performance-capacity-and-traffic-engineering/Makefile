PYTHON ?= python3
TOOL := $(PYTHON) scripts/course_tool.py
MODULE ?= 01
TRACK ?= python

.PHONY: help program-help doctor setup orientation-proof predecessor-proof structure-proof data-proof performance-case-proof vector-proof migration-proof python-proof typescript-proof plan-proof release-proof planted-defect-proof capstone-tour markdown-link-proof source-reference-proof education-proof hygiene-proof module-proof core-proof manifest-create manifest-proof docs-build postgres-proof k6-proof locust-proof full-proof clean

help: program-help

program-help:
	@printf '%s\n' \
	  'API Performance, Capacity, and Traffic Engineering' \
	  '' \
	  'Dependency-light routes:' \
	  '  make doctor' \
	  '  make orientation-proof' \
	  '  make module-proof MODULE=04 TRACK=python' \
	  '  make capstone-tour' \
	  '  make core-proof' \
	  '  make manifest-create manifest-proof' \
	  '' \
	  'Environment-backed routes:' \
	  '  make setup' \
	  '  TEST_DATABASE_URL=... make postgres-proof' \
	  '  BASE_URL=... ACCESS_TOKEN=... make k6-proof' \
	  '  BASE_URL=... ACCESS_TOKEN=... make locust-proof' \
	  '  make docs-build' \
	  '  make full-proof'

doctor:
	$(TOOL) doctor

setup:
	$(PYTHON) -m pip install -e 'capstone/tracks/python-fastapi[dev]'
	cd capstone/tracks/typescript-fastify && npm ci
	$(PYTHON) -m pip install -r requirements-docs.txt

orientation-proof:
	$(TOOL) orientation-proof
predecessor-proof:
	$(TOOL) predecessor-proof
structure-proof:
	$(TOOL) structure-proof
data-proof:
	$(TOOL) data-proof
performance-case-proof:
	$(TOOL) performance-case-proof
vector-proof:
	$(TOOL) vector-proof
migration-proof:
	$(TOOL) migration-proof
python-proof:
	$(TOOL) python-proof
typescript-proof:
	$(TOOL) typescript-proof
plan-proof:
	$(TOOL) plan-proof
release-proof:
	$(TOOL) release-proof
planted-defect-proof:
	$(TOOL) planted-defect-proof
capstone-tour:
	$(TOOL) capstone-tour
markdown-link-proof:
	$(TOOL) markdown-link-proof
source-reference-proof:
	$(TOOL) source-reference-proof
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
	@command -v mkdocs >/dev/null || { echo 'mkdocs is not available; install the pinned docs environment'; exit 2; }
	mkdocs build --strict

postgres-proof:
	@test -n "$$TEST_DATABASE_URL" || { echo 'TEST_DATABASE_URL is required'; exit 2; }
	PYTHONPATH=capstone/tracks/python-fastapi/src $(PYTHON) capstone/tests/postgres_plan_proof.py

k6-proof:
	@command -v k6 >/dev/null || { echo 'k6 is not available'; exit 2; }
	@test -n "$$BASE_URL" -a -n "$$ACCESS_TOKEN" || { echo 'BASE_URL and ACCESS_TOKEN are required'; exit 2; }
	k6 run capstone/benchmarks/k6/run-list-open.js

locust-proof:
	@command -v locust >/dev/null || { echo 'locust is not available'; exit 2; }
	@test -n "$$BASE_URL" -a -n "$$ACCESS_TOKEN" || { echo 'BASE_URL and ACCESS_TOKEN are required'; exit 2; }
	locust -f capstone/benchmarks/locust/locustfile.py --headless --host "$$BASE_URL" -u 20 -r 5 -t 60s

full-proof:
	$(TOOL) full-proof

clean:
	rm -rf .pytest_cache site .runtime reports/last-*.json capstone/reports/*.json
	rm -rf capstone/tracks/python-fastapi/.pytest_cache capstone/tracks/typescript-fastify/dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
