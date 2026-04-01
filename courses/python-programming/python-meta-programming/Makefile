SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
VENV_DIR ?= .venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip
MKDOCS := $(VENV_BIN)/mkdocs

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: venv install-docs
venv: ## Create the local virtual environment
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

install-docs: venv ## Install documentation dependencies
	@$(PIP) install -r requirements-docs.txt

.PHONY: docs-build docs-serve test
docs-build: install-docs ## Build MkDocs documentation
	@$(MKDOCS) build --strict

docs-serve: install-docs ## Serve MkDocs locally
	@$(MKDOCS) serve

test: docs-build ## Run the course's default verification target

.PHONY: clean
clean: ## Remove build and virtualenv artifacts
	@rm -rf $(VENV_DIR) site .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
