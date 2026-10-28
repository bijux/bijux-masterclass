SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

COURSE_ROOT := $(abspath ..)
CAPSTONE_ROOT := $(abspath .)
VENV := $(COURSE_ROOT)/.venv
PY := $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)
PYTEST := $(if $(wildcard $(VENV)/bin/pytest),$(VENV)/bin/pytest,pytest)
SCHEMATHESIS := $(if $(wildcard $(VENV)/bin/st),$(VENV)/bin/st,$(if $(wildcard $(VENV)/bin/schemathesis),$(VENV)/bin/schemathesis,schemathesis))
OPENAPI_PYTHON_CLIENT := $(if $(wildcard $(VENV)/bin/openapi-python-client),$(VENV)/bin/openapi-python-client,openapi-python-client)
NODE_BIN := $(COURSE_ROOT)/node_modules/.bin
TOOLS_BIN := $(COURSE_ROOT)/.tools/bin
REDOCLY := $(NODE_BIN)/redocly
SPECTRAL := $(NODE_BIN)/spectral
PRISM := $(NODE_BIN)/prism
OPENAPI_TYPESCRIPT := $(NODE_BIN)/openapi-typescript
OASDIFF := $(if $(wildcard $(TOOLS_BIN)/oasdiff),$(TOOLS_BIN)/oasdiff,oasdiff)
REPORTS := reports
PYTHONPATH_VALUE := .:scripts:services/python-fastapi/src:clients/python/src
COURSE_TOOL := PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) scripts/course_tool.py

.PHONY: help doctor setup walkthrough tour structure parse refs bundle bundle-check \
	operations examples fixtures handler-map overlays workflow releases markdown \
	core-proof python-test python-check typescript-audit typescript-typecheck typescript-test typescript \
	test confirm verify-report capability-report client-view clients-generate clients-test security-test diff contract-test \
	lint-contract python-run typescript-run python-live typescript-live live-conformance \
	prism-mock prism-smoke schemathesis oasdiff docs-build proof clean

help: ## Show capstone commands and evidence routes.
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-27s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

doctor: ## Check core host tools, versions, and required files.
	@$(PY) scripts/doctor.py

setup: ## Create the Python environment and install exact Node package versions.
	@cd "$(COURSE_ROOT)"; \
	if command -v uv >/dev/null 2>&1; then \
		uv sync; \
	else \
		python3 -m venv .venv; \
		.venv/bin/python -m pip install --upgrade pip; \
		.venv/bin/python -m pip install -r requirements.txt; \
	fi
	@cd "$(COURSE_ROOT)" && npm install --ignore-scripts
	@npm --prefix services/typescript-fastify install --ignore-scripts
	@npm --prefix clients/typescript install --ignore-scripts
	@$(PY) scripts/install_oasdiff.py
	@printf '%s\n' 'PASS setup complete'

walkthrough: ## Print the capstone evidence walkthrough.
	@cat docs/evidence-tour.md

tour: core-proof ## Run a compact in-process end-to-end evidence tour.
	@PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) scripts/run_inprocess_tour.py

structure: ## Validate the expected course and capstone structure.
	@$(COURSE_TOOL) structure

parse: ## Parse and structurally validate OpenAPI 3.1.2 and 3.2.0.
	@$(COURSE_TOOL) parse

refs: ## Resolve every external reference offline.
	@$(COURSE_TOOL) refs

bundle: ## Produce deterministic baseline and frontier bundles.
	@$(COURSE_TOOL) bundle

bundle-check: ## Prove repeatable bundle bytes and write SHA-256 evidence.
	@$(COURSE_TOOL) bundle-check

operations: ## Write the operation/callback/webhook ledger.
	@$(COURSE_TOOL) operations

examples: ## Validate all examples against their effective schemas.
	@$(COURSE_TOOL) examples

fixtures: ## Run the shared valid/invalid JSON Schema corpus.
	@$(COURSE_TOOL) fixtures

handler-map: ## Prove every path operation exists in both providers.
	@$(COURSE_TOOL) handler-map

overlays: bundle ## Apply and assert the public and partner overlays.
	@$(COURSE_TOOL) overlays

workflow: bundle ## Validate Arazzo step dependencies and operation references.
	@$(COURSE_TOOL) workflow

releases: ## Verify compatible and deliberately breaking release fixtures.
	@$(COURSE_TOOL) releases

markdown: ## Check every local Markdown link.
	@$(COURSE_TOOL) markdown

core-proof: ## Run dependency-light deterministic contract gates in one cached process.
	@$(COURSE_TOOL) core-proof

python-test: ## Run provider, client, contract, and fixture tests in Python.
	@PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTEST) -q

python-check: ## Compile and statically inspect Python source.
	@PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) -m compileall -q scripts services/python-fastapi/src clients/python/src tests
	@if [ -x "$(VENV)/bin/ruff" ]; then "$(VENV)/bin/ruff" check scripts services/python-fastapi/src clients/python/src tests; else printf '%s\n' 'ruff not installed; run make setup'; exit 2; fi

typescript-audit: ## Semantically compile provider and client with narrow local dependency shims.
	@tsc_bin="$(NODE_BIN)/tsc"; \
	if [ ! -x "$$tsc_bin" ]; then tsc_bin=$$(command -v tsc || true); fi; \
	if [ -z "$$tsc_bin" ]; then printf '%s\n' 'TypeScript compiler is missing; run make setup'; exit 2; fi; \
	"$$tsc_bin" -p tsconfig.audit.json --pretty false
	@printf '%s\n' 'PASS TypeScript provider/client semantic audit (course-owned dependency shims)'

# npm dependencies are deliberately not hidden behind a fallback. A missing install is a failed proof.
typescript-typecheck: ## Type-check both TypeScript provider and consumer.
	@npm --prefix services/typescript-fastify run typecheck
	@npm --prefix clients/typescript run typecheck

typescript-test: ## Run both TypeScript test suites.
	@npm --prefix services/typescript-fastify test
	@npm --prefix clients/typescript test

typescript: typescript-typecheck typescript-test ## Run all TypeScript evidence.
	@printf '%s\n' 'PASS TypeScript provider and client'

test: core-proof python-test typescript ## Run the normal complete local test route.
	@printf '%s\n' 'PASS complete local test route'

confirm: core-proof python-test typescript ## Run all local completion gates.
	@printf '%s\n' 'PASS capstone confirmation'

verify-report: ## Write a machine-readable report for dependency-light gates.
	@$(COURSE_TOOL) verify-report

capability-report: ## Inventory installed tool commands without treating availability as support.
	@$(COURSE_TOOL) capability-report

client-view: bundle ## Produce the explicit generator-compatibility contract view.
	@PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) scripts/client_view.py

clients-test: ## Run handwritten and generated-consumer acceptance tests.
	@PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTEST) -q clients/python/tests
	@npm --prefix clients/typescript test

security-test: ## Run focused authentication, scope, ownership, and webhook-security tests.
	@PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTEST) -q services/python-fastapi/tests/test_security.py
	@npm --prefix services/typescript-fastify test -- app.test.ts workflow.test.ts

diff: releases ## Run the dependency-light compatibility and deliberate-break fixture gate.
	@printf '%s\n' 'PASS built-in compatibility diff'

contract-test: live-conformance ## Run the provider-neutral contract behavior suite against both providers.
	@printf '%s\n' 'PASS shared contract behavior'

clients-generate: client-view ## Generate TypeScript and Python SDKs from the pinned contract view.
	@test -x "$(OPENAPI_TYPESCRIPT)" || { printf '%s\n' 'openapi-typescript is missing; run make setup'; exit 2; }
	@"$(OPENAPI_TYPESCRIPT)" spec/dist/openapi.client.yaml -o clients/typescript/generated/schema.generated.d.ts
	@command -v "$(OPENAPI_PYTHON_CLIENT)" >/dev/null 2>&1 || test -x "$(OPENAPI_PYTHON_CLIENT)" || { printf '%s\n' 'openapi-python-client is missing; run make setup'; exit 2; }
	@rm -rf clients/python/generated/sdk
	@"$(OPENAPI_PYTHON_CLIENT)" generate --path spec/dist/openapi.client.yaml --meta none --output-path clients/python/generated/sdk --overwrite
	@printf '%s\n' 'PASS generated Python and TypeScript clients'

lint-contract: bundle ## Run Redocly and Spectral against the canonical baseline, plus Redocly against 3.2.
	@test -x "$(REDOCLY)" || { printf '%s\n' 'Redocly CLI is missing; run make setup'; exit 2; }
	@test -x "$(SPECTRAL)" || { printf '%s\n' 'Spectral CLI is missing; run make setup'; exit 2; }
	@cd "$(COURSE_ROOT)" && "$(REDOCLY)" lint capstone/spec/openapi.yaml --config redocly.yaml
	@cd "$(COURSE_ROOT)" && "$(REDOCLY)" lint capstone/spec/openapi-3.2.yaml --config redocly.yaml
	@cd "$(COURSE_ROOT)" && "$(SPECTRAL)" lint --ruleset .spectral.yaml capstone/spec/openapi.yaml

python-run: ## Run the FastAPI provider on port 8000.
	@PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) -m uvicorn analysis_api.app:app --host 127.0.0.1 --port 8000

typescript-run: ## Run the Fastify provider on port 3000.
	@npm --prefix services/typescript-fastify run start

python-live: ## Start a clean Python provider and run shared live conformance.
	@mkdir -p "$(REPORTS)"; \
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) -m uvicorn analysis_api.app:app --host 127.0.0.1 --port 8011 >"$(REPORTS)/python-provider.log" 2>&1 & \
	pid=$$!; trap 'kill $$pid >/dev/null 2>&1 || true; wait $$pid >/dev/null 2>&1 || true' EXIT; \
	$(PY) scripts/wait_for_http.py http://127.0.0.1:8011/health; \
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) scripts/run_live_conformance.py --base-url http://127.0.0.1:8011 --provider python-fastapi --report "$(REPORTS)/python-live-conformance.json"

typescript-live: ## Start a clean TypeScript provider and run shared live conformance.
	@mkdir -p "$(REPORTS)"; \
	PORT=8012 npm --prefix services/typescript-fastify run start >"$(REPORTS)/typescript-provider.log" 2>&1 & \
	pid=$$!; trap 'kill $$pid >/dev/null 2>&1 || true; wait $$pid >/dev/null 2>&1 || true' EXIT; \
	$(PY) scripts/wait_for_http.py http://127.0.0.1:8012/health; \
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) scripts/run_live_conformance.py --base-url http://127.0.0.1:8012 --provider typescript-fastify --report "$(REPORTS)/typescript-live-conformance.json"

live-conformance: python-live typescript-live ## Prove both providers against one behavioral suite.
	@printf '%s\n' 'PASS cross-provider live conformance'

prism-mock: bundle ## Start Prism mock server on port 4010.
	@test -x "$(PRISM)" || { printf '%s\n' 'Prism is missing; run make setup'; exit 2; }
	@"$(PRISM)" mock spec/dist/openapi.bundle.yaml -h 127.0.0.1 -p 4010

prism-smoke: bundle ## Start Prism, exercise examples, and prove invalid-request rejection.
	@test -x "$(PRISM)" || { printf '%s\n' 'Prism is missing; run make setup'; exit 2; }
	@mkdir -p "$(REPORTS)"; \
	"$(PRISM)" mock spec/dist/openapi.bundle.yaml -h 127.0.0.1 -p 4010 >"$(REPORTS)/prism.log" 2>&1 & \
	pid=$$!; trap 'kill $$pid >/dev/null 2>&1 || true; wait $$pid >/dev/null 2>&1 || true' EXIT; \
	$(PY) scripts/wait_for_http.py http://127.0.0.1:4010/health; \
	$(PY) scripts/prism_smoke.py --base-url http://127.0.0.1:4010

schemathesis: client-view ## Run deterministic generated contract tests against Python.
	@command -v "$(SCHEMATHESIS)" >/dev/null 2>&1 || test -x "$(SCHEMATHESIS)" || { printf '%s\n' 'Schemathesis is missing; run make setup'; exit 2; }
	@mkdir -p "$(REPORTS)/schemathesis"; \
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PY) -m uvicorn analysis_api.app:app --host 127.0.0.1 --port 8013 >"$(REPORTS)/schemathesis-provider.log" 2>&1 & \
	pid=$$!; trap 'kill $$pid >/dev/null 2>&1 || true; wait $$pid >/dev/null 2>&1 || true' EXIT; \
	$(PY) scripts/wait_for_http.py http://127.0.0.1:8013/health; \
	"$(SCHEMATHESIS)" run spec/dist/openapi.client.yaml --url http://127.0.0.1:8013 --header 'X-API-Key: demo-api-key' --phases examples,coverage,fuzzing --mode all --max-examples 20 --seed 20260805 --generation-deterministic --checks all --report junit --report-dir "$(REPORTS)/schemathesis"

oasdiff: ## Run the external breaking-change gate on safe and unsafe releases.
	@command -v "$(OASDIFF)" >/dev/null 2>&1 || test -x "$(OASDIFF)" || { printf '%s\n' 'oasdiff is missing; run make setup'; exit 2; }
	@"$(OASDIFF)" breaking releases/v1.0/openapi.yaml releases/v1.1/openapi.yaml
	@if "$(OASDIFF)" breaking releases/v1.1/openapi.yaml releases/attempted-v1.2-breaking/openapi.yaml >"$(REPORTS)/oasdiff-blocked.txt" 2>&1; then \
		printf '%s\n' 'expected attempted v1.2 to be rejected by oasdiff'; exit 1; \
	fi
	@printf '%s\n' 'PASS oasdiff compatibility gate'

docs-build: ## Build the complete strict course site through the program entrypoint.
	@$(MAKE) -C "$(COURSE_ROOT)" docs-build

proof: ## Run every deterministic, implementation, generator, mock, property, diff, and docs gate.
	@$(PY) scripts/proof.py

clean: ## Remove generated reports, caches, site output, bundles, and generated SDK code.
	@rm -rf reports .pytest_cache services/python-fastapi/.pytest_cache clients/python/.pytest_cache
	@find . -type d -name __pycache__ -prune -exec rm -rf {} +
	@rm -rf spec/dist clients/python/generated/sdk
	@rm -f clients/typescript/generated/schema.generated.d.ts
	@mkdir -p reports spec/dist
	@: > reports/.gitkeep
	@: > spec/dist/.gitkeep
