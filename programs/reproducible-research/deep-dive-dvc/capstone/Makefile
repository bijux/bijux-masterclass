SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/reproducible-research/deep-dive-dvc/capstone
VENV_BIN := $(VENV_DIR)/bin
VENV_PY := $(abspath $(VENV_BIN)/python)
PIP := $(VENV_PY) -m pip
PYTEST := $(VENV_PY) -m pytest
DVC := $(VENV_PY) -m dvc
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/reproducible-research/deep-dive-dvc

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
	@$(VENV_PY) -m incident_escalation_capstone.verify --publish publish/v1

.PHONY: tour
tour: verify ## Build the learner-facing proof bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR)/publish-v1
	@$(DVC) status > $(TOUR_DIR)/status.txt
	@$(DVC) dag --dot > $(TOUR_DIR)/pipeline.dot
	@cp dvc.yaml $(TOUR_DIR)/dvc.yaml
	@cp dvc.lock $(TOUR_DIR)/dvc.lock
	@cp params.yaml $(TOUR_DIR)/params.yaml
	@cp metrics/metrics.json $(TOUR_DIR)/metrics.json
	@cp publish/v1/manifest.json $(TOUR_DIR)/publish-v1/manifest.json
	@cp publish/v1/metrics.json $(TOUR_DIR)/publish-v1/metrics.json
	@cp publish/v1/params.yaml $(TOUR_DIR)/publish-v1/params.yaml
	@cp publish/v1/data-profile.json $(TOUR_DIR)/publish-v1/data-profile.json
	@cp publish/v1/report.md $(TOUR_DIR)/publish-v1/report.md
	@cp TOUR.md $(TOUR_DIR)/TOUR.md
	@echo "tour_dir=$(TOUR_DIR)" > $(TOUR_DIR)/bundle.env
	@echo "publish_dir=$(TOUR_DIR)/publish-v1" >> $(TOUR_DIR)/bundle.env
	@echo "✔ wrote learner-facing tour to $(TOUR_DIR)"

.PHONY: walkthrough
walkthrough: ## Print the recommended first capstone walkthrough
	@printf '%s\n' \
		'Capstone walkthrough:' \
		'  1. read README.md for the repository contract' \
		'  2. read dvc.yaml and then dvc.lock' \
		'  3. inspect params.yaml and metrics/metrics.json' \
		'  4. run make verify' \
		'  5. run make tour' \
		'  6. inspect publish/v1/manifest.json and publish/v1/report.md' \
		'' \
		'Focused proof targets:' \
		'  make verify         validate the promoted artifact contract' \
		'  make confirm        run verify, tests, and recovery drill' \
		'  make recovery-drill prove remote-backed restoration after loss'

.PHONY: push
push: repro ## Push tracked artifacts to the local training remote
	@$(DVC) push

.PHONY: recovery-drill
recovery-drill: push ## Rebuild the workspace from the remote after cache loss
	@rm -rf data/derived metrics models publish state .dvc/cache
	@$(DVC) pull
	@$(DVC) checkout
	@$(VENV_PY) -m incident_escalation_capstone.verify --publish publish/v1

.PHONY: confirm
confirm: verify test recovery-drill ## Run the full capstone verification suite

.PHONY: clean-generated
clean-generated: ## Remove generated pipeline outputs
	@rm -rf data/derived metrics models publish state

.PHONY: clean
clean: clean-generated ## Remove local virtual environment and caches
	@rm -rf $(VENV_DIR) .pytest_cache .dvc/cache __pycache__
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
