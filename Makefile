SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -euo pipefail -c

PY ?= python3
VENV_DIR ?= .venv
VENV_PY := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip
MKDOCS := $(VENV_DIR)/bin/mkdocs

.DEFAULT_GOAL := help

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"; printf "\nTargets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

venv: ## Create venv and install docs tooling (plus light dev tooling)
	$(PY) -m venv $(VENV_DIR)
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PIP) install -e ".[docs,dev]"

docs-serve: venv ## Serve MkDocs locally
	$(MKDOCS) serve

docs-build: venv ## Build MkDocs site strictly into ./site
	$(MKDOCS) build --strict

docs-clean: ## Remove built site directory
	rm -rf site

capstone-check: ## Run fast checks in snakemake-capstone (format/lint/tests + lint workflow)
	$(MAKE) -C snakemake-capstone check

capstone-confirm: ## Full clean-room confirmation in snakemake-capstone (runs workflow + verifies artifacts)
	$(MAKE) -C snakemake-capstone confirm

check: docs-build capstone-check ## Run root docs build + capstone fast checks

clean: docs-clean ## Remove common build artifacts
	rm -rf $(VENV_DIR) .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -name ".DS_Store" -type f -delete
