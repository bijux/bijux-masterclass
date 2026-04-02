SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

CAPSTONE_DIR := capstone
RUN_CAPSTONE = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(CAPSTONE_DIR)
ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/python-programming/python-meta-programming
COURSE_VENV_DIR ?= $(ARTIFACTS_DIR)/venv/python-programming/python-meta-programming

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone confirmation suite
	@$(RUN_CAPSTONE) confirm

.PHONY: capstone-tour
capstone-tour: ## Build the learner-facing capstone proof bundle
	@$(RUN_CAPSTONE) tour

.PHONY: capstone-proof
capstone-proof: ## Run the full capstone proof route
	@$(RUN_CAPSTONE) proof

.PHONY: capstone-manifest
capstone-manifest: ## Render the capstone manifest from the public CLI
	@$(RUN_CAPSTONE) manifest

.PHONY: capstone-trace
capstone-trace: ## Trace one capstone invocation from the public CLI
	@$(RUN_CAPSTONE) trace

.PHONY: clean
clean: ## Remove build and virtualenv artifacts
	@rm -rf $(COURSE_VENV_DIR) $(SITE_DIR) .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@$(RUN_CAPSTONE) clean
