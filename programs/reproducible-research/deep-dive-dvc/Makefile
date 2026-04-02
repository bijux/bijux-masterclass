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

.PHONY: capstone-tour
capstone-tour: ## Build the learner-facing capstone proof bundle
	@$(RUN_CAPSTONE) tour

.PHONY: capstone-verify-report
capstone-verify-report: ## Build the capstone verification report bundle
	@$(RUN_CAPSTONE) verify-report

.PHONY: capstone-state-summary
capstone-state-summary: ## Render a combined declaration, execution, and release summary
	@$(RUN_CAPSTONE) state-summary

.PHONY: capstone-release-summary
capstone-release-summary: ## Render the promoted release summary
	@$(RUN_CAPSTONE) release-summary

.PHONY: capstone-review-queue
capstone-review-queue: ## Render the structured prediction review queue
	@$(RUN_CAPSTONE) review-queue

.PHONY: capstone-verify
capstone-verify: ## Run the capstone contract verification route
	@$(RUN_CAPSTONE) verify

.PHONY: capstone-confirm
capstone-confirm: ## Run the capstone's strongest confirmation route
	@$(RUN_CAPSTONE) confirm

.PHONY: capstone-walkthrough
capstone-walkthrough: ## Build the learner-facing capstone walkthrough bundle
	@$(RUN_CAPSTONE) walkthrough

.PHONY: capstone-release-audit
capstone-release-audit: ## Build the capstone release-boundary audit bundle
	@$(RUN_CAPSTONE) release-audit

.PHONY: capstone-release-review
capstone-release-review: ## Build the capstone release review bundle
	@$(RUN_CAPSTONE) release-review

.PHONY: capstone-recovery-audit
capstone-recovery-audit: ## Build the capstone remote-recovery audit bundle
	@$(RUN_CAPSTONE) recovery-audit

.PHONY: capstone-recovery-review
capstone-recovery-review: ## Build the capstone remote recovery review bundle
	@$(RUN_CAPSTONE) recovery-review

.PHONY: capstone-experiment-review
capstone-experiment-review: ## Build the capstone experiment comparison bundle
	@$(RUN_CAPSTONE) experiment-review

.PHONY: clean
clean: ## Remove build artifacts
	@rm -rf $(COURSE_VENV_DIR) $(SITE_DIR) .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@$(RUN_CAPSTONE) clean
