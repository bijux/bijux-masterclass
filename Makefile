SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

COURSES_DIR := courses
COURSE ?= reproducible-research/deep-dive-make
COURSE_DIR := $(COURSES_DIR)/$(COURSE)
RUN_COURSE = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(COURSE_DIR)
PYTHON ?= python3
VENV_DIR ?= .venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip
MKDOCS := $(VENV_BIN)/mkdocs

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: courses
courses: ## List available courses
	@find $(COURSES_DIR) -mindepth 2 -maxdepth 2 -type d | sed 's#^$(COURSES_DIR)/##' | sort

.PHONY: families
families: ## List available course families
	@find $(COURSES_DIR) -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort

.PHONY: course-help
course-help: ## Show the selected course's Make targets
	@$(RUN_COURSE) help

.PHONY: docs-build
docs-build: ## Build docs for the selected course
	@$(RUN_COURSE) docs-build

.PHONY: docs-serve
docs-serve: ## Serve docs for the selected course
	@$(RUN_COURSE) docs-serve

.PHONY: test
test: ## Run tests for the selected course
	@$(RUN_COURSE) test

.PHONY: clean
clean: ## Run clean for the selected course
	@$(RUN_COURSE) clean

.PHONY: series-docs-venv
series-docs-venv: ## Create the virtual environment for the series site
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: series-docs-install
series-docs-install: series-docs-venv ## Install series documentation dependencies
	@$(PIP) install -r requirements-docs.txt

.PHONY: series-docs-build
series-docs-build: series-docs-install ## Build the series documentation site
	@$(MKDOCS) build --strict

.PHONY: series-docs-serve
series-docs-serve: series-docs-install ## Serve the series documentation site locally
	@$(MKDOCS) serve
