SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PROGRAMS_DIR := programs
PROGRAM ?= reproducible-research/deep-dive-make
PROGRAM_DIR := $(PROGRAMS_DIR)/$(PROGRAM)
PROGRAM_ORIGIN := $(origin PROGRAM)
PROGRAM_IS_EXPLICIT := $(filter command line environment override,$(PROGRAM_ORIGIN))
RUN_PROGRAM = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(PROGRAM_DIR)
PYTHON ?= python3
ARTIFACTS_DIR ?= artifacts
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/series-docs
VENV_BIN := $(VENV_DIR)/bin
VENV_PY := $(abspath $(VENV_BIN)/python)
PIP := $(VENV_PY) -m pip
MKDOCS := $(VENV_PY) -m mkdocs
SYNC_SERIES_DOCS := $(PYTHON) scripts/sync_series_docs.py
RENDER_ROOT_MKDOCS := $(PYTHON) scripts/render_root_mkdocs.py
DOCS_ENV = NO_MKDOCS_2_WARNING=true
ROOT_MKDOCS_FILE := artifacts/mkdocs.root.yml

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: programs
programs: ## List available programs
	@find $(PROGRAMS_DIR) -mindepth 2 -maxdepth 2 -type d | sed 's#^$(PROGRAMS_DIR)/##' | sort

.PHONY: families
families: ## List available program families
	@find $(PROGRAMS_DIR) -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort

.PHONY: program-help
program-help: ## Show the selected program's Make targets
	@$(RUN_PROGRAM) help

.PHONY: program-docs-build
program-docs-build: series-docs-install ## Build docs for the selected program
	@cd $(PROGRAM_DIR) && $(DOCS_ENV) $(MKDOCS) build -f mkdocs.yml --strict

.PHONY: program-docs-serve
program-docs-serve: series-docs-install ## Serve docs for the selected program
	@cd $(PROGRAM_DIR) && $(DOCS_ENV) $(MKDOCS) serve -f mkdocs.yml

.PHONY: docs-build
docs-build: series-docs-install ## Build the full catalog, or one program if PROGRAM is set explicitly
ifeq ($(PROGRAM_IS_EXPLICIT),)
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(MKDOCS) build -f $(ROOT_MKDOCS_FILE) --strict
else
	@cd $(PROGRAM_DIR) && $(DOCS_ENV) $(MKDOCS) build -f mkdocs.yml --strict
endif

.PHONY: docs-serve
docs-serve: series-docs-install ## Serve the full catalog, or one program if PROGRAM is set explicitly
ifeq ($(PROGRAM_IS_EXPLICIT),)
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(MKDOCS) serve -f $(ROOT_MKDOCS_FILE)
else
	@cd $(PROGRAM_DIR) && $(DOCS_ENV) $(MKDOCS) serve -f mkdocs.yml
endif

.PHONY: test
test: ## Run tests for the selected program
	@$(RUN_PROGRAM) test

.PHONY: demo
demo: ## Run the selected program's learner-facing capstone walkthrough
	@$(RUN_PROGRAM) demo

.PHONY: inspect
inspect: ## Inspect the selected program's learner-facing capstone state
	@$(RUN_PROGRAM) inspect

.PHONY: proof
proof: ## Run the selected program's strongest learner-facing proof route
	@$(RUN_PROGRAM) proof

.PHONY: capstone-walkthrough
capstone-walkthrough: ## Run the selected program's learner-facing capstone walkthrough
	@$(RUN_PROGRAM) capstone-walkthrough

.PHONY: capstone-tour
capstone-tour: ## Run the selected program's learner-facing capstone tour
	@$(RUN_PROGRAM) capstone-tour

.PHONY: capstone-selftest
capstone-selftest: ## Run the selected program's capstone determinism or convergence self-test
	@$(RUN_PROGRAM) capstone-selftest

.PHONY: capstone-contract-audit
capstone-contract-audit: ## Build the selected program's capstone public-contract audit bundle
	@$(RUN_PROGRAM) capstone-contract-audit

.PHONY: capstone-incident-audit
capstone-incident-audit: ## Build the selected program's capstone incident review bundle
	@$(RUN_PROGRAM) capstone-incident-audit

.PHONY: capstone-verify-report
capstone-verify-report: ## Build the selected program's capstone verification report bundle
	@$(RUN_PROGRAM) capstone-verify-report

.PHONY: capstone-profile-audit
capstone-profile-audit: ## Build the selected program's capstone execution-policy audit bundle
	@$(RUN_PROGRAM) capstone-profile-audit

.PHONY: capstone-verify
capstone-verify: ## Run the selected program's capstone contract verification
	@$(RUN_PROGRAM) capstone-verify

.PHONY: capstone-confirm
capstone-confirm: ## Run the selected program's strongest capstone confirmation route
	@$(RUN_PROGRAM) capstone-confirm

.PHONY: clean
clean: ## Run clean for the selected program
	@$(RUN_PROGRAM) clean

.PHONY: docs-audit
docs-audit: ## Audit course-book and capstone documentation rules
	@$(PYTHON) scripts/audit_masterclass_docs.py

.PHONY: series-docs-venv
series-docs-venv: ## Create the virtual environment for the series site
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: series-docs-install
series-docs-install: series-docs-venv ## Install series documentation dependencies
	@$(PIP) install -r requirements-docs.txt

.PHONY: series-docs-build
series-docs-build: series-docs-install ## Build the series documentation site
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(MKDOCS) build -f $(ROOT_MKDOCS_FILE) --strict

.PHONY: series-docs-serve
series-docs-serve: series-docs-install ## Serve the series documentation site locally
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(MKDOCS) serve -f $(ROOT_MKDOCS_FILE)
