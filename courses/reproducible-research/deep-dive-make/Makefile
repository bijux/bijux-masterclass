SHELL := /bin/sh
.SHELLFLAGS := -eu -c
# Use '>' as recipe prefix to avoid TAB footgun (GNU Make ≥4.0)
.RECIPEPREFIX := >

.DEFAULT_GOAL := help

PYTHON ?= python3
VENV_DIR ?= .venv
VENV_BIN := $(VENV_DIR)/bin
PY := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip

# Prefer tools from the venv when present, fallback to system.
RUFF   := $(if $(wildcard $(VENV_BIN)/ruff),$(VENV_BIN)/ruff,ruff)
MYPY   := $(if $(wildcard $(VENV_BIN)/mypy),$(VENV_BIN)/mypy,mypy)
MKDOCS := $(if $(wildcard $(VENV_BIN)/mkdocs),$(VENV_BIN)/mkdocs,mkdocs)

CAPSTONE_DIR := make-capstone
PY_LINT_PATHS := $(CAPSTONE_DIR)/scripts

# UX
.PHONY: help
help: ## Show available targets
> awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "\033[36m%-24s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Python env (dependency management via pyproject extras)
.PHONY: venv install install-dev install-docs
venv: ## Create/update local virtualenv in ./.venv
> $(PYTHON) -m venv $(VENV_DIR)
> $(PIP) install -U pip

install: venv ## Install dev+docs extras into the venv
> $(PIP) install ".[docs,dev]"

install-dev: venv ## Install dev tooling into the venv
> $(PIP) install ".[dev]"

install-docs: venv ## Install docs tooling into the venv
> $(PIP) install ".[docs]"

# Quality (Python helper scripts)
.PHONY: lint format typecheck
lint: install-dev ## Run ruff (static checks)
> $(RUFF) check $(PY_LINT_PATHS)

format: install-dev ## Auto-format Python (ruff format)
> $(RUFF) format $(PY_LINT_PATHS)

typecheck: install-dev ## Run mypy on Python helper scripts
> $(MYPY) $(PY_LINT_PATHS)

# Docs
.PHONY: docs-serve docs-build docs-clean
docs-serve: install-docs ## Serve docs locally (live reload)
> $(MKDOCS) serve -f mkdocs.yml

docs-build: install-docs ## Build docs into ./site (strict)
> $(MKDOCS) build -f mkdocs.yml --strict

docs-clean: ## Remove built site output
> rm -rf site

# Capstone (GNU Make repository)
.PHONY: capstone capstone-selftest capstone-hardened capstone-clean
capstone: ## Build the capstone (writes ./all sentinel inside make-capstone)
> $(MAKE) -C $(CAPSTONE_DIR) all

capstone-selftest: ## Capstone selftest (convergence + parallel determinism + negative test)
> $(MAKE) -C $(CAPSTONE_DIR) selftest

capstone-hardened: ## Capstone hardened invariants (selftest + audits + attest + runtime tests)
> $(MAKE) -C $(CAPSTONE_DIR) hardened

capstone-clean: ## Clean capstone outputs
> $(MAKE) -C $(CAPSTONE_DIR) clean

# Convenience alias: "test" means the capstone's selftest.
.PHONY: test
test: capstone-selftest ## Run project tests (capstone selftest)

# Cleaning
.PHONY: clean-soft clean
clean-soft: docs-clean ## Remove build artifacts (keeps venv)
> rm -rf .ruff_cache .mypy_cache
> find . -type d -name "__pycache__" -prune -exec rm -rf {} +

clean: clean-soft capstone-clean ## clean-soft + capstone-clean + remove venv
> rm -rf $(VENV_DIR)