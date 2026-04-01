SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
VENV_DIR ?= .venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip
PYTEST := $(VENV_BIN)/pytest
DVC := $(VENV_BIN)/dvc

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: venv
venv: ## Create the local virtual environment
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: install
install: venv ## Install capstone dependencies
	@$(PIP) install -e . pytest dvc

.PHONY: repro
repro: install ## Execute the DVC pipeline
	@$(DVC) repro

.PHONY: test
test: install ## Run the Python test suite
	@$(PYTEST)

.PHONY: clean-generated
clean-generated: ## Remove generated pipeline outputs
	@rm -rf data/derived metrics models publish state

.PHONY: clean
clean: clean-generated ## Remove local virtual environment and caches
	@rm -rf $(VENV_DIR) .pytest_cache __pycache__
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
