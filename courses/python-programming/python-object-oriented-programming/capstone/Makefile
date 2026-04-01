SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone test suite
	@$(PYTHON) -m pytest

.PHONY: confirm
confirm: test ## Run the executable validation suite

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
