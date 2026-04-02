SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -euo pipefail -c

.DEFAULT_GOAL := help

ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/reproducible-research/deep-dive-snakemake

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"; printf "\nTargets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

docs-clean: ## Remove built site directory
	rm -rf "$(SITE_DIR)"

capstone-check: ## Run fast checks in capstone (format/lint/tests + lint workflow)
	$(MAKE) -C capstone check

capstone-confirm: ## Full clean-room confirmation in capstone (runs workflow + verifies artifacts)
	$(MAKE) -C capstone confirm

capstone-selftest: ## Determinism proof in capstone (compares published output across core counts)
	$(MAKE) -C capstone selftest

capstone-verify-report: ## Write a structured publish verification report bundle
	$(MAKE) -C capstone verify-report

capstone-walkthrough: ## Build the learner-facing capstone walkthrough bundle
	$(MAKE) -C capstone walkthrough

capstone-tour: ## Build the learner-facing capstone proof bundle
	$(MAKE) -C capstone tour

capstone-profile-audit: ## Package execution profile review evidence
	$(MAKE) -C capstone profile-audit

check: capstone-check ## Run capstone fast checks

test: check ## Run the course's default verification target

clean: docs-clean ## Remove common build artifacts
	rm -rf "$(ARTIFACTS_DIR)/venv/reproducible-research/deep-dive-snakemake" .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -name ".DS_Store" -type f -delete
