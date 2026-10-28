SHELL := /bin/bash
.DEFAULT_GOAL := program-help

PYTHON ?= python3
TRACK ?= python
RELEASE ?= 1.0
MIGRATION_TARGET ?= $(if $(filter 1.1,$(RELEASE)),005,002)
COMPOSE_FILE := capstone/compose.yaml
COMPOSE_PROJECT := cdse-analysis-runs
COMPOSE := SERVICE_RELEASE=$(RELEASE) MIGRATION_TARGET=$(MIGRATION_TARGET) docker compose -f $(COMPOSE_FILE) --profile $(TRACK)
TOOL := $(PYTHON) capstone/scripts/course_tool.py
RUNTIME := $(PYTHON) capstone/tests/runtime/proof_runner.py

.PHONY: help program-help setup setup-python setup-typescript doctor \
 predecessor-proof operation-proof migration-proof vector-proof python-proof typescript-core-proof \
 release-proof release-live-proof typescript-syntax-proof course-structure-proof markdown-link-proof hygiene-proof core-proof docs-build docs-serve \
 postgres-up postgres-down postgres-reset logs smoke-proof postgres-proof conformance-proof \
 concurrency-proof query-proof recovery-proof artifact-proof webhook-proof release-proof final-proof \
 manifest-create manifest-proof module-proof capstone-tour capstone-confirm clean

help program-help:
	@printf '%s\n' \
	  'Contract-Driven API Service Engineering' \
	  '' \
	  'Static/dependency-light proof:' \
	  '  make doctor' \
	  '  make predecessor-proof operation-proof migration-proof vector-proof release-proof' \
	  '  make python-proof typescript-core-proof core-proof' \
	  '' \
	  'Documentation:' \
	  '  make docs-build | docs-serve' \
	  '' \
	  'Live topology (TRACK=python|typescript, RELEASE=1.0|1.1):' \
	  '  make postgres-up TRACK=python RELEASE=1.0' \
	  '  make smoke-proof TRACK=python' \
	  '  make final-proof TRACK=python' \
	  '  make postgres-down' \
	  '' \
	  'Integrity:' \
	  '  make manifest-create manifest-proof' \
	  '' \
	  'Live proof requires Docker Compose, PostgreSQL 18, and the selected track dependencies.'

setup:
	$(PYTHON) -m pip install -r requirements.txt

setup-python:
	$(PYTHON) -m pip install -e 'capstone/tracks/python-fastapi[dev]'

setup-typescript:
	npm --prefix capstone/tracks/typescript-fastify install --ignore-scripts


doctor:
	$(TOOL) doctor

predecessor-proof:
	$(TOOL) predecessor-proof

operation-proof:
	$(TOOL) operation-proof

migration-proof:
	$(TOOL) migration-proof

vector-proof:
	$(TOOL) vector-proof

python-proof:
	$(TOOL) python-proof

typescript-core-proof:
	$(TOOL) typescript-core-proof

typescript-syntax-proof:
	$(TOOL) typescript-syntax-proof

course-structure-proof:
	$(TOOL) course-structure-proof

markdown-link-proof:
	$(TOOL) markdown-link-proof

hygiene-proof:
	$(TOOL) hygiene-proof

core-proof:
	$(TOOL) core-proof

docs-build:
	$(PYTHON) -m mkdocs build --strict -f mkdocs.yml

docs-serve:
	$(PYTHON) -m mkdocs serve -f mkdocs.yml

postgres-up:
	@test '$(TRACK)' = python -o '$(TRACK)' = typescript || { echo 'TRACK must be python or typescript' >&2; exit 2; }
	@test '$(RELEASE)' = 1.0 -o '$(RELEASE)' = 1.1 || { echo 'RELEASE must be 1.0 or 1.1' >&2; exit 2; }
	$(COMPOSE) up -d --build postgres receiver $(TRACK)-migrate $(TRACK)-api $(TRACK)-worker
	$(RUNTIME) wait --track $(TRACK) --release $(RELEASE)

postgres-down:
	@docker compose -f $(COMPOSE_FILE) down --remove-orphans

postgres-reset:
	@echo 'Removing course-owned containers and named volumes for $(COMPOSE_PROJECT).'
	@docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans

logs:
	$(COMPOSE) logs --tail=250 -f postgres receiver $(TRACK)-api $(TRACK)-worker

smoke-proof:
	$(RUNTIME) smoke --track $(TRACK) --release $(RELEASE)

postgres-proof:
	$(RUNTIME) postgres --track $(TRACK) --release $(RELEASE)

conformance-proof:
	$(RUNTIME) conformance --track $(TRACK) --release $(RELEASE)

concurrency-proof:
	$(RUNTIME) concurrency --track $(TRACK) --release $(RELEASE)

query-proof:
	$(RUNTIME) query --track $(TRACK) --release $(RELEASE)

recovery-proof:
	$(RUNTIME) recovery --track $(TRACK) --release $(RELEASE)

artifact-proof:
	$(RUNTIME) artifact --track $(TRACK) --release $(RELEASE)

webhook-proof:
	$(RUNTIME) webhook --track $(TRACK) --release $(RELEASE)

release-proof:
	$(TOOL) release-proof

release-live-proof:
	$(PYTHON) capstone/tests/runtime/release_proof.py --track $(TRACK)

final-proof: core-proof
	$(RUNTIME) final --track $(TRACK) --release $(RELEASE)

module-proof:
	@case '$(MODULE)' in \
	  00) $(MAKE) core-proof ;; \
	  01|02) $(MAKE) python-proof typescript-core-proof operation-proof ;; \
	  03) $(MAKE) migration-proof postgres-proof TRACK=$(TRACK) RELEASE=$(RELEASE) ;; \
	  04) $(MAKE) concurrency-proof TRACK=$(TRACK) RELEASE=$(RELEASE) ;; \
	  05) $(MAKE) query-proof TRACK=$(TRACK) RELEASE=$(RELEASE) ;; \
	  06) $(MAKE) recovery-proof TRACK=$(TRACK) RELEASE=$(RELEASE) ;; \
	  07) $(MAKE) artifact-proof TRACK=$(TRACK) RELEASE=$(RELEASE) ;; \
	  08) $(MAKE) webhook-proof TRACK=$(TRACK) RELEASE=$(RELEASE) ;; \
	  09) $(MAKE) final-proof TRACK=$(TRACK) RELEASE=$(RELEASE) ;; \
	  10) $(MAKE) release-proof TRACK=$(TRACK) ;; \
	  *) echo 'MODULE must be 00 through 10' >&2; exit 2 ;; \
	esac

capstone-tour:
	$(RUNTIME) tour --track $(TRACK) --release $(RELEASE)

capstone-confirm:
	$(RUNTIME) conformance --track $(TRACK) --release $(RELEASE)

manifest-create:
	$(TOOL) manifest-create

manifest-proof:
	$(TOOL) manifest-proof

clean:
	rm -rf site .pytest_cache capstone/reports/*.json
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name dist-core \) -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
