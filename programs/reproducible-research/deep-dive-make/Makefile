SHELL := /bin/sh
.SHELLFLAGS := -eu -c
# Use '>' as recipe prefix to avoid TAB footgun (GNU Make ≥4.0)
.RECIPEPREFIX := >

.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/reproducible-research/deep-dive-make
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/reproducible-research/deep-dive-make
VENV_BIN := $(VENV_DIR)/bin
PY := $(VENV_BIN)/python
PIP := $(PY) -m pip

# Prefer tools from the venv when present, fallback to system.
RUFF   := $(if $(wildcard $(PY)),$(PY) -m ruff,ruff)
MYPY   := $(if $(wildcard $(PY)),$(PY) -m mypy,mypy)

CAPSTONE_DIR := capstone
PY_LINT_PATHS := $(CAPSTONE_DIR)/scripts

# UX
.PHONY: help
help: ## Show available targets
> awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "\033[36m%-24s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Python env (dependency management via pyproject extras)
.PHONY: venv install install-dev
venv: ## Create/update local virtualenv in ./.venv
> $(PYTHON) -m venv $(VENV_DIR)
> $(PIP) install -U pip

install: venv ## Install dev+docs extras into the venv
> $(PIP) install -r ../../../requirements-docs.txt
> $(PIP) install "ruff>=0.5,<1" "mypy>=1.10,<2"

install-dev: venv ## Install dev tooling into the venv
> $(PIP) install "ruff>=0.5,<1" "mypy>=1.10,<2"

# Quality (Python helper scripts)
.PHONY: lint format typecheck
lint: install-dev ## Run ruff (static checks)
> $(RUFF) check $(PY_LINT_PATHS)

format: install-dev ## Auto-format Python (ruff format)
> $(RUFF) format $(PY_LINT_PATHS)

typecheck: install-dev ## Run mypy on Python helper scripts
> $(MYPY) $(PY_LINT_PATHS)

# Capstone (GNU Make repository)
.PHONY: capstone capstone-selftest capstone-hardened capstone-tour capstone-walkthrough \
        capstone-contract-audit capstone-incident-audit capstone-verify-report \
        capstone-profile-audit capstone-confirm capstone-clean demo inspect proof
capstone: ## Build the capstone (writes ./all sentinel inside capstone)
> $(MAKE) -C $(CAPSTONE_DIR) all

capstone-selftest: ## Capstone selftest (convergence + parallel determinism + negative test)
> $(MAKE) -C $(CAPSTONE_DIR) selftest

capstone-hardened: ## Capstone hardened invariants (selftest + audits + attest + runtime tests)
> $(MAKE) -C $(CAPSTONE_DIR) hardened

capstone-tour: ## Print the capstone walkthrough from the program directory
> $(MAKE) -C $(CAPSTONE_DIR) tour

capstone-walkthrough: ## Build the learner-facing capstone walkthrough bundle
> $(MAKE) -C $(CAPSTONE_DIR) walkthrough

capstone-contract-audit: ## Build the capstone public-contract audit bundle
> $(MAKE) -C $(CAPSTONE_DIR) contract-audit

capstone-incident-audit: ## Build the capstone incident review bundle
> $(MAKE) -C $(CAPSTONE_DIR) incident-audit

capstone-verify-report: ## Build the capstone verification report bundle
> $(MAKE) -C $(CAPSTONE_DIR) verify-report

capstone-profile-audit: ## Build the capstone execution-profile audit bundle
> $(MAKE) -C $(CAPSTONE_DIR) profile-audit

capstone-confirm: ## Run the capstone's strongest confirmation route
> $(MAKE) -C $(CAPSTONE_DIR) confirm

capstone-clean: ## Clean capstone outputs
> $(MAKE) -C $(CAPSTONE_DIR) clean

demo: ## Build the learner-facing capstone walkthrough bundle
> $(MAKE) -C $(CAPSTONE_DIR) walkthrough

inspect: ## Build the learner-facing capstone inspection bundle
> $(MAKE) -C $(CAPSTONE_DIR) inspect

proof: ## Build the sanctioned learner-facing capstone proof bundle set
> $(MAKE) -C $(CAPSTONE_DIR) proof

# Convenience alias: "test" means the capstone's selftest.
.PHONY: test
test: capstone-selftest ## Run project tests (capstone selftest)

# Cleaning
.PHONY: clean-soft clean
clean-soft: ## Remove build artifacts (keeps venv)
> rm -rf .ruff_cache .mypy_cache
> rm -rf $(SITE_DIR)
> find . -type d -name "__pycache__" -prune -exec rm -rf {} +

clean: clean-soft capstone-clean ## clean-soft + capstone-clean + remove venv
> rm -rf $(VENV_DIR)
