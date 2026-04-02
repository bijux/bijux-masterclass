SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

CAPSTONE_DIR := capstone
RUN_CAPSTONE = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(CAPSTONE_DIR)
ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/python-programming/python-functional-programming
COURSE_VENV_DIR ?= $(ARTIFACTS_DIR)/venv/python-programming/python-functional-programming

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Install capstone development dependencies
	@$(RUN_CAPSTONE) install

.PHONY: test
test: ## Run the capstone test suite
	@$(RUN_CAPSTONE) test

.PHONY: demo
demo: ## Build the learner-facing capstone walkthrough
	@$(RUN_CAPSTONE) demo

.PHONY: inspect
inspect: ## Build the learner-facing capstone inspection bundle
	@$(RUN_CAPSTONE) inspect

.PHONY: capstone-tour
capstone-tour: ## Build the learner-facing capstone proof bundle
	@$(RUN_CAPSTONE) tour

.PHONY: capstone-verify-report
capstone-verify-report: ## Build the capstone verification report bundle
	@$(RUN_CAPSTONE) verify-report

.PHONY: capstone-confirm
capstone-confirm: ## Run the capstone's strongest confirmation route
	@$(RUN_CAPSTONE) confirm

.PHONY: proof
proof: ## Run the full capstone proof route
	@$(RUN_CAPSTONE) proof

.PHONY: build
build: ## Build capstone distribution artifacts
	@$(RUN_CAPSTONE) build

.PHONY: lint
lint: ## Run capstone linting and type checks
	@$(RUN_CAPSTONE) lint

.PHONY: snapshots
snapshots: ## Export tagged module snapshots
	@$(RUN_CAPSTONE) snapshots

.PHONY: worktrees
worktrees: ## Create detached worktrees for tagged modules
	@$(RUN_CAPSTONE) worktrees

.PHONY: clean-history
clean-history: ## Remove generated worktrees and snapshots
	@$(RUN_CAPSTONE) clean-history

.PHONY: module-md
module-md: ## Concatenate module markdown sources into capstone/all-cores
	@$(RUN_CAPSTONE) module-md

.PHONY: module-funcpipe
module-funcpipe: ## Freeze tagged snapshots into capstone/all-cores
	@$(RUN_CAPSTONE) module-funcpipe

.PHONY: freeze-codebase
freeze-codebase: ## Export the current capstone codebase into markdown
	@$(RUN_CAPSTONE) freeze-codebase

.PHONY: clean
clean: ## Remove course and capstone build artifacts
	@$(RUN_CAPSTONE) clean
	@rm -rf $(COURSE_VENV_DIR) $(SITE_DIR) .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
