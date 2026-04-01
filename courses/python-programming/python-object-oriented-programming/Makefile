SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## No course-local executable checks yet
	@true

.PHONY: clean
clean: ## Remove build artifacts
	@rm -rf .venv site .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
