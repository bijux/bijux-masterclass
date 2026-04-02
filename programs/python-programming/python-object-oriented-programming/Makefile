SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

CAPSTONE_DIR := capstone
RUN_CAPSTONE = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(CAPSTONE_DIR)
ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/python-programming/python-object-oriented-programming
COURSE_VENV_DIR ?= $(ARTIFACTS_DIR)/venv/python-programming/python-object-oriented-programming

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone confirmation suite
	@$(RUN_CAPSTONE) confirm

.PHONY: demo
demo: ## Run the capstone scenario walkthrough
	@$(RUN_CAPSTONE) demo

.PHONY: inspect
inspect: ## Inspect the capstone learner-facing state
	@$(RUN_CAPSTONE) inspect

.PHONY: capstone-walkthrough
capstone-walkthrough: ## Run the capstone learner-facing walkthrough route
	@$(RUN_CAPSTONE) tour

.PHONY: capstone-tour
capstone-tour: ## Run the capstone learner-facing tour route
	@$(RUN_CAPSTONE) tour

.PHONY: capstone-confirm
capstone-confirm: ## Run the capstone confirmation route
	@$(RUN_CAPSTONE) confirm

.PHONY: proof
proof: ## Run the full capstone proof route
	@$(RUN_CAPSTONE) proof

.PHONY: clean
clean: ## Remove build artifacts
	@rm -rf $(COURSE_VENV_DIR) $(SITE_DIR) .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@$(RUN_CAPSTONE) clean
