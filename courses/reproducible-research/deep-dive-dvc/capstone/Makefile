SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/reproducible-research/deep-dive-dvc/capstone
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

.PHONY: dvc-init
dvc-init: install ## Initialize DVC metadata and the local training remote
	@if [ ! -d .dvc ]; then $(DVC) init --subdir -q; fi
	@if ! $(DVC) remote list | grep -q '^training-local'; then $(DVC) remote add -d training-local .dvc-remote; fi

.PHONY: repro
repro: dvc-init ## Execute the DVC pipeline
	@$(DVC) repro

.PHONY: test
test: install ## Run the Python test suite
	@$(PYTEST)

.PHONY: verify
verify: repro ## Validate the published artifact contract
	@$(VENV_BIN)/python -m incident_escalation_capstone.verify --publish publish/v1

.PHONY: push
push: repro ## Push tracked artifacts to the local training remote
	@$(DVC) push

.PHONY: recovery-drill
recovery-drill: push ## Rebuild the workspace from the remote after cache loss
	@rm -rf data/derived metrics models publish state .dvc/cache
	@$(DVC) pull
	@$(DVC) checkout
	@$(VENV_BIN)/python -m incident_escalation_capstone.verify --publish publish/v1

.PHONY: confirm
confirm: verify test recovery-drill ## Run the full capstone verification suite

.PHONY: clean-generated
clean-generated: ## Remove generated pipeline outputs
	@rm -rf data/derived metrics models publish state

.PHONY: clean
clean: clean-generated ## Remove local virtual environment and caches
	@rm -rf $(VENV_DIR) .pytest_cache .dvc/cache __pycache__
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
