PYTHON ?= python3
TOOL := $(PYTHON) scripts/course_tool.py
MODULE ?= 01
TRACK ?= python
COMPOSE := docker compose -f capstone/observability/compose.yaml

.PHONY: help program-help doctor setup orientation-proof predecessor-proof reliability-case-proof data-proof vector-proof migration-proof python-proof typescript-core-proof observability-config-proof runbook-proof incident-proof planted-defect-proof release-proof structure-proof markdown-link-proof source-reference-proof education-proof hygiene-proof module-proof capstone-tour core-proof manifest-create manifest-proof docs-build promtool-proof postgres-proof telemetry-live-proof game-day-proof stack-up stack-down full-proof clean

help: program-help

program-help:
	@printf '%s\n' \
	  'API Reliability and Observability Engineering' \
	  '' \
	  'Dependency-light routes:' \
	  '  make doctor' \
	  '  make orientation-proof' \
	  '  make module-proof MODULE=02 TRACK=python' \
	  '  make core-proof' \
	  '  make manifest-create manifest-proof' \
	  '  make capstone-tour' \
	  '' \
	  'Environment-backed routes:' \
	  '  make setup' \
	  '  make docs-build' \
	  '  make promtool-proof' \
	  '  TEST_DATABASE_URL=... make postgres-proof' \
	  '  make stack-up telemetry-live-proof game-day-proof stack-down' \
	  '  make full-proof'

doctor:
	$(TOOL) doctor

setup:
	$(PYTHON) -m pip install -e 'capstone/tracks/python-fastapi[dev,observability]'
	cd capstone/tracks/typescript-fastify && npm ci
	$(PYTHON) -m pip install -r requirements-docs.txt

orientation-proof:
	$(TOOL) orientation-proof
predecessor-proof:
	$(TOOL) predecessor-proof
reliability-case-proof:
	$(TOOL) reliability-case-proof
data-proof:
	$(TOOL) data-proof
vector-proof:
	$(TOOL) vector-proof
migration-proof:
	$(TOOL) migration-proof
python-proof:
	$(TOOL) python-proof
typescript-core-proof:
	$(TOOL) typescript-core-proof
observability-config-proof:
	$(TOOL) observability-config-proof
runbook-proof:
	$(TOOL) runbook-proof
incident-proof:
	$(TOOL) incident-proof
planted-defect-proof:
	$(TOOL) planted-defect-proof
release-proof:
	$(TOOL) release-proof
structure-proof:
	$(TOOL) structure-proof
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
capstone-tour:
	$(TOOL) capstone-tour
core-proof:
	$(TOOL) core-proof
manifest-create:
	$(TOOL) manifest-create
manifest-proof:
	$(TOOL) manifest-proof

docs-build:
	@command -v mkdocs >/dev/null || { echo 'mkdocs not available; run make setup or install the pinned docs environment'; exit 2; }
	mkdocs build --strict

promtool-proof:
	@command -v promtool >/dev/null || { echo 'promtool not available'; exit 2; }
	promtool check rules capstone/observability/rules/recording-rules.yaml capstone/observability/rules/alerts.yaml

postgres-proof:
	@test -n "$$TEST_DATABASE_URL" || { echo 'TEST_DATABASE_URL is required'; exit 2; }
	PYTHONPATH=capstone/tracks/python-fastapi/src $(PYTHON) capstone/tests/failure/postgres_proof.py

telemetry-live-proof:
	PYTHONPATH=capstone/tracks/python-fastapi/src $(PYTHON) capstone/tests/failure/telemetry_live_proof.py

game-day-proof:
	PYTHONPATH=capstone/tracks/python-fastapi/src $(PYTHON) capstone/tests/failure/game_day_proof.py

stack-up:
	@command -v docker >/dev/null || { echo 'docker not available'; exit 2; }
	$(COMPOSE) --profile python --profile typescript up -d --build

stack-down:
	@command -v docker >/dev/null || { echo 'docker not available'; exit 2; }
	$(COMPOSE) --profile python --profile typescript down -v --remove-orphans

full-proof:
	$(TOOL) full-proof

clean:
	rm -rf .pytest_cache site .runtime reports/last-*.json
	rm -rf capstone/tracks/python-fastapi/.pytest_cache
	rm -rf capstone/tracks/typescript-fastify/dist capstone/tracks/typescript-fastify/dist-core capstone/tracks/typescript-fastify/dist-security-core capstone/tracks/typescript-fastify/dist-reliability-core capstone/tracks/typescript-fastify/dist-audit
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
