SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PROGRAMS_DIR := programs
PROGRAM ?= reproducible-research/deep-dive-make
PROGRAM_DIR := $(PROGRAMS_DIR)/$(PROGRAM)
RUN_PROGRAM = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(PROGRAM_DIR)
PYTHON ?= python3
ARTIFACTS_DIR ?= artifacts
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/series-docs
VENV_BIN := $(VENV_DIR)/bin
VENV_PY := $(abspath $(VENV_BIN)/python)
PIP := $(VENV_PY) -m pip
MKDOCS := $(VENV_PY) -m mkdocs

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

.PHONY: docs-build
docs-build: series-docs-install ## Build docs for the selected program
	@cd $(PROGRAM_DIR) && $(MKDOCS) build -f mkdocs.yml --strict

.PHONY: docs-serve
docs-serve: series-docs-install ## Serve docs for the selected program
	@cd $(PROGRAM_DIR) && $(MKDOCS) serve -f mkdocs.yml

.PHONY: test
test: ## Run tests for the selected program
	@$(RUN_PROGRAM) test

.PHONY: capstone-walkthrough
capstone-walkthrough: ## Run the selected program's learner-facing capstone walkthrough
	@$(RUN_PROGRAM) capstone-walkthrough

.PHONY: capstone-tour
capstone-tour: ## Run the selected program's learner-facing capstone tour
	@$(RUN_PROGRAM) capstone-tour

.PHONY: clean
clean: ## Run clean for the selected program
	@$(RUN_PROGRAM) clean

.PHONY: series-docs-venv
series-docs-venv: ## Create the virtual environment for the series site
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: series-docs-install
series-docs-install: series-docs-venv ## Install series documentation dependencies
	@$(PIP) install -r requirements-docs.txt

.PHONY: series-docs-build
series-docs-build: series-docs-install ## Build the series documentation site
	@$(MKDOCS) build --strict

.PHONY: series-docs-serve
series-docs-serve: series-docs-install ## Serve the series documentation site locally
	@$(MKDOCS) serve
