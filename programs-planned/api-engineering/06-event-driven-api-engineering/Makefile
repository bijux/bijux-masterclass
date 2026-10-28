PYTHON ?= python3
TOOL := $(PYTHON) scripts/course_tool.py
MODULE ?= 01
TRACK ?= python

.PHONY: help program-help doctor setup setup-python setup-typescript \
 predecessor-proof orientation-proof structure-proof data-proof event-case-proof contract-proof \
 vector-proof migration-proof python-proof typescript-proof delivery-proof \
 outbox-inbox-proof evolution-proof replay-proof workflow-proof stream-proof \
 security-proof reliability-proof release-proof planted-defect-proof handoff-proof \
 markdown-link-proof source-reference-proof education-proof hygiene-proof \
 handoff manifest manifest-proof capstone-tour module-proof core-proof full-proof \
 asyncapi-cli-proof postgres-proof docs-build docs-serve nats-up nats-down nats-proof stack-up stack-down clean

help program-help:
	@printf '%s\n' \
	  'Event-Driven API Engineering' \
	  '' \
	  'Learner path:' \
	  '  make doctor' \
	  '  make predecessor-proof' \
	  '  make capstone-tour' \
	  '  make module-proof MODULE=01 TRACK=python' \
	  '  make core-proof' \
	  '' \
	  'Environment-backed routes:' \
	  '  make asyncapi-cli-proof' \
	  '  TEST_DATABASE_URL=... make postgres-proof' \
	  '  make nats-up / make nats-proof / make nats-down' \
	  '  make docs-build' \
	  '  make full-proof'

doctor:
	$(TOOL) doctor

setup: setup-python setup-typescript

setup-python:
	$(PYTHON) -m pip install -e 'capstone/tracks/python-fastapi[dev,api,nats,postgres]'

setup-typescript:
	cd capstone/tracks/typescript-fastify && npm install

predecessor-proof orientation-proof structure-proof data-proof event-case-proof contract-proof vector-proof migration-proof python-proof typescript-proof delivery-proof outbox-inbox-proof evolution-proof replay-proof workflow-proof stream-proof security-proof reliability-proof release-proof planted-defect-proof handoff-proof markdown-link-proof source-reference-proof education-proof hygiene-proof manifest-proof capstone-tour asyncapi-cli-proof postgres-proof docs-build nats-proof:
	$(TOOL) $@

module-proof:
	$(TOOL) module-proof --module $(MODULE) --track $(TRACK)

core-proof:
	$(TOOL) core-proof

full-proof:
	$(TOOL) full-proof

handoff:
	$(PYTHON) scripts/build_handoff.py

manifest:
	$(PYTHON) scripts/build_manifest.py

nats-up:
	docker compose -f capstone/broker/nats/compose.yaml up -d --wait

nats-down:
	docker compose -f capstone/broker/nats/compose.yaml down -v

stack-up:
	docker compose -f capstone/compose.yaml up -d --wait

stack-down:
	docker compose -f capstone/compose.yaml down -v

docs-serve:
	mkdocs serve

clean:
	rm -rf site .pytest_cache capstone/tracks/typescript-fastify/dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
