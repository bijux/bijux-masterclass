SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PROGRAMS_DIR := programs
PROGRAM ?= reproducible-research/deep-dive-make
PROGRAM_DIR := $(PROGRAMS_DIR)/$(PROGRAM)
PROGRAM_ORIGIN := $(origin PROGRAM)
PROGRAM_IS_EXPLICIT := $(filter command line environment override,$(PROGRAM_ORIGIN))
RUN_PROGRAM = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(PROGRAM_DIR)
PYTHON ?= python3
ARTIFACTS_DIR ?= artifacts
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/series-docs
VENV_BIN := $(VENV_DIR)/bin
VENV_PY := $(abspath $(VENV_BIN)/python)
PIP := $(VENV_PY) -m pip
MKDOCS := $(VENV_PY) -m mkdocs
DOCS_REQUIREMENTS ?= configs/docs/requirements-docs.txt
DOCS_HOST ?= 127.0.0.1
DOCS_PORT ?= 8000
DOCS_PORT_SEARCH_LIMIT ?= 25
SERVE_DOCS := $(VENV_PY) scripts/serve_docs.py --host $(DOCS_HOST) --port $(DOCS_PORT) --port-search-limit $(DOCS_PORT_SEARCH_LIMIT)
SYNC_SERIES_DOCS := $(VENV_PY) scripts/sync_series_docs.py
RENDER_ROOT_MKDOCS := $(VENV_PY) scripts/render_root_mkdocs.py
DOCS_ENV = NO_MKDOCS_2_WARNING=true
ROOT_MKDOCS_FILE := artifacts/mkdocs.root.yml
PYTHON_BIN ?= $(shell command -v python3 2>/dev/null)

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: programs
programs: ## List available programs
	@find $(PROGRAMS_DIR) -mindepth 2 -maxdepth 2 -type d | sed 's#^$(PROGRAMS_DIR)/##' | sort

.PHONY: families
families: ## List available program families
	@find $(PROGRAMS_DIR) -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
