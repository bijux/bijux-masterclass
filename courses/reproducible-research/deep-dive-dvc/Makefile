SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

CAPSTONE_DIR := capstone
RUN_CAPSTONE = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(CAPSTONE_DIR)
ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/reproducible-research/deep-dive-dvc
COURSE_VENV_DIR ?= $(ARTIFACTS_DIR)/venv/reproducible-research/deep-dive-dvc

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone confirmation suite
	@$(RUN_CAPSTONE) confirm

.PHONY: clean
clean: ## Remove build artifacts
	@rm -rf $(COURSE_VENV_DIR) $(SITE_DIR) .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@$(RUN_CAPSTONE) clean
