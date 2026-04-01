SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -euo pipefail -c

.DEFAULT_GOAL := help

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"; printf "\nTargets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

docs-clean: ## Remove built site directory
	rm -rf site

capstone-check: ## Run fast checks in snakemake-capstone (format/lint/tests + lint workflow)
	$(MAKE) -C snakemake-capstone check

capstone-confirm: ## Full clean-room confirmation in snakemake-capstone (runs workflow + verifies artifacts)
	$(MAKE) -C snakemake-capstone confirm

check: capstone-check ## Run capstone fast checks

test: check ## Run the course's default verification target

clean: docs-clean ## Remove common build artifacts
	rm -rf .venv .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -name ".DS_Store" -type f -delete
