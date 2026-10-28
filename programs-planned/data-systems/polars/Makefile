SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.DEFAULT_GOAL := help

PYTHON ?= python3
VENV_DIR ?= .venv
VENV_BIN := $(VENV_DIR)/bin
PY := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip

# Prefer tools from the venv when present, fallback to system.
SNAKEMAKE := $(if $(wildcard $(VENV_BIN)/snakemake),$(VENV_BIN)/snakemake,snakemake)
MKDOCS := $(if $(wildcard $(VENV_BIN)/mkdocs),$(VENV_BIN)/mkdocs,mkdocs)

CAPSTONE_DIR := snakemake-capstone

# -----------------------------
# UX
# -----------------------------
.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# -----------------------------
# Python env
# -----------------------------
.PHONY: venv install install-dev install-docs install-capstone
venv: ## Create/update local virtualenv in ./.venv
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install -U pip

install: venv ## Install dev+docs+capstone extras into the venv
	$(PIP) install -e ".[capstone,docs,dev]"

install-dev: venv ## Install dev tooling into the venv
	$(PIP) install -e ".[dev]"

install-docs: venv ## Install docs tooling into the venv
	$(PIP) install -e ".[docs]"

install-capstone: venv ## Install snakemake (capstone extra) into the venv
	$(PIP) install -e ".[capstone]"

# -----------------------------
# Quality
# -----------------------------
.PHONY: lint test
lint: install-dev ## Run ruff (static checks)
	$(VENV_BIN)/ruff check .

test: install-dev ## Run unit tests (capstone scripts)
	$(PY) -m pytest

# -----------------------------
# Docs
# -----------------------------
.PHONY: docs-serve docs-build docs-clean
docs-serve: install-docs ## Serve docs locally (live reload)
	$(MKDOCS) serve -f mkdocs.yml

docs-build: install-docs ## Build docs into ./site (strict)
	$(MKDOCS) build -f mkdocs.yml --strict

docs-clean: ## Remove built site output
	rm -rf site

# -----------------------------
# Capstone
# -----------------------------
.PHONY: capstone capstone-dry capstone-selftest capstone-clean
capstone: ## Run the capstone workflow
	$(MAKE) -C $(CAPSTONE_DIR) run SNAKEMAKE="$(SNAKEMAKE)"

capstone-dry: ## Dry-run the capstone workflow
	$(MAKE) -C $(CAPSTONE_DIR) dry SNAKEMAKE="$(SNAKEMAKE)"

capstone-selftest: ## Integration selftest (serial vs parallel determinism)
	$(MAKE) -C $(CAPSTONE_DIR) selftest SNAKEMAKE="$(SNAKEMAKE)"

capstone-clean: ## Remove capstone outputs (results/logs/publish/benchmarks)
	$(MAKE) -C $(CAPSTONE_DIR) clean

# -----------------------------
# Cleaning
# -----------------------------
.PHONY: clean-soft clean
clean-soft: docs-clean ## Remove build/test artifacts (keeps venv)
	rm -rf .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	# capstone outputs
	rm -rf $(CAPSTONE_DIR)/results $(CAPSTONE_DIR)/publish $(CAPSTONE_DIR)/logs $(CAPSTONE_DIR)/benchmarks

clean: clean-soft ## clean-soft + remove venv and ALL .snakemake caches
	rm -rf $(VENV_DIR)
	find . -type d -name ".snakemake" -prune -exec rm -rf {} +
