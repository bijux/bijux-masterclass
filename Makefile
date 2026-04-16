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
BIJUX_DOCS_SYNC_SCRIPT ?= internal/scripts/sync_bijux_docs.sh
BIJUX_DOCS_SOT_GUARD ?= internal/scripts/verify_bijux_docs_source_of_truth.sh
BIJUX_DOCS_CONTRACT_GUARD ?= internal/quality/validate_bijux_docs_contract.py
BIJUX_STD_CHECK_SCRIPT ?= shared/bijux-makes-py/ci/check-bijux-std.sh
BIJUX_STD_REF ?= main
BIJUX_STD_REMOTE ?= https://raw.githubusercontent.com/bijux/bijux-std

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: bijux-docs-sync
bijux-docs-sync: ## Synchronize shared Bijux docs shell into docs assets
	@bash "$(BIJUX_DOCS_SYNC_SCRIPT)"

.PHONY: bijux-docs-check
bijux-docs-check: ## Validate Bijux docs shell contract and drift checks
	@"$(PYTHON_BIN)" "$(BIJUX_DOCS_CONTRACT_GUARD)" .
	@bash "$(BIJUX_DOCS_SOT_GUARD)"

.PHONY: bijux-std
bijux-std: ## Verify shared directories match bijux-std (set BIJUX_STD_REF for pinning)
	@BIJUX_STD_REF="$(BIJUX_STD_REF)" BIJUX_STD_REMOTE="$(BIJUX_STD_REMOTE)" bash "$(BIJUX_STD_CHECK_SCRIPT)"

.PHONY: programs
programs: ## List available programs
	@find $(PROGRAMS_DIR) -mindepth 2 -maxdepth 2 -type d | sed 's#^$(PROGRAMS_DIR)/##' | sort

.PHONY: families
families: ## List available program families
	@find $(PROGRAMS_DIR) -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort

.PHONY: program-help
program-help: ## Show the selected program's Make targets
	@$(RUN_PROGRAM) help

.PHONY: program-docs-build
program-docs-build: series-docs-install ## Build docs for the selected program
	@cd $(PROGRAM_DIR) && $(DOCS_ENV) $(MKDOCS) build -f mkdocs.yml --strict

.PHONY: program-docs-serve
program-docs-serve: series-docs-install ## Serve docs for the selected program
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(PROGRAM_DIR)/mkdocs.yml)

.PHONY: docs-build
docs-build: series-docs-install bijux-docs-sync ## Build the full catalog, or one program if PROGRAM is set explicitly
ifeq ($(PROGRAM_IS_EXPLICIT),)
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(MKDOCS) build -f $(ROOT_MKDOCS_FILE) --strict
else
	@cd $(PROGRAM_DIR) && $(DOCS_ENV) $(MKDOCS) build -f mkdocs.yml --strict
endif

.PHONY: docs-serve
docs-serve: series-docs-install bijux-docs-sync ## Serve the full catalog, or one program if PROGRAM is set explicitly
ifeq ($(PROGRAM_IS_EXPLICIT),)
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(ROOT_MKDOCS_FILE))
else
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(PROGRAM_DIR)/mkdocs.yml)
endif

.PHONY: test
test: ## Run tests for the selected program
	@$(RUN_PROGRAM) test

.PHONY: demo
demo: ## Run the selected program's learner-facing capstone walkthrough
	@$(RUN_PROGRAM) demo

.PHONY: inspect
inspect: ## Inspect the selected program's learner-facing capstone state
	@$(RUN_PROGRAM) inspect

.PHONY: proof
proof: ## Run the selected program's strongest learner-facing proof route
	@$(RUN_PROGRAM) proof

.PHONY: history-refresh
history-refresh: ## Build the selected program's generated module history worktrees
	@$(RUN_PROGRAM) history-refresh

.PHONY: history-clean
history-clean: ## Remove the selected program's generated module history worktrees
	@$(RUN_PROGRAM) history-clean

.PHONY: history-freeze-code
history-freeze-code: ## Freeze the selected program's generated module history worktrees
	@$(RUN_PROGRAM) history-freeze-code

.PHONY: capstone-walkthrough
capstone-walkthrough: ## Run the selected program's learner-facing capstone walkthrough
	@$(RUN_PROGRAM) capstone-walkthrough

.PHONY: capstone-tour
capstone-tour: ## Run the selected program's learner-facing capstone tour
	@$(RUN_PROGRAM) capstone-tour

.PHONY: capstone-platform-report
capstone-platform-report: ## Print the selected program's supported toolchain versions
	@$(RUN_PROGRAM) capstone-platform-report

.PHONY: capstone-repro
capstone-repro: ## Execute the selected program's capstone pipeline
	@$(RUN_PROGRAM) capstone-repro

.PHONY: capstone-state-summary
capstone-state-summary: ## Render the selected program's capstone state summary
	@$(RUN_PROGRAM) capstone-state-summary

.PHONY: capstone-validate-config
capstone-validate-config: ## Validate the selected program's capstone configuration
	@$(RUN_PROGRAM) capstone-validate-config

.PHONY: capstone-wf-dryrun
capstone-wf-dryrun: ## Print the selected program's capstone dry-run plan
	@$(RUN_PROGRAM) capstone-wf-dryrun

.PHONY: capstone-bootstrap-confirm
capstone-bootstrap-confirm: ## Create the selected program's capstone toolchain and run clean-room confirmation
	@$(RUN_PROGRAM) capstone-bootstrap-confirm

.PHONY: capstone-selftest
capstone-selftest: ## Run the selected program's capstone determinism or convergence self-test
	@$(RUN_PROGRAM) capstone-selftest

.PHONY: capstone-contract-audit
capstone-contract-audit: ## Build the selected program's capstone public-contract audit bundle
	@$(RUN_PROGRAM) capstone-contract-audit

.PHONY: capstone-incident-audit
capstone-incident-audit: ## Build the selected program's capstone incident review bundle
	@$(RUN_PROGRAM) capstone-incident-audit

.PHONY: capstone-verify-report
capstone-verify-report: ## Build the selected program's capstone verification report bundle
	@$(RUN_PROGRAM) capstone-verify-report

.PHONY: capstone-verify-artifacts
capstone-verify-artifacts: ## Verify the selected program's published capstone artifacts
	@$(RUN_PROGRAM) capstone-verify-artifacts

.PHONY: capstone-release-audit
capstone-release-audit: ## Build the selected program's capstone release audit bundle
	@$(RUN_PROGRAM) capstone-release-audit

.PHONY: capstone-release-review
capstone-release-review: ## Build the selected program's capstone release review bundle
	@$(RUN_PROGRAM) capstone-release-review

.PHONY: capstone-recovery-audit
capstone-recovery-audit: ## Build the selected program's capstone recovery audit bundle
	@$(RUN_PROGRAM) capstone-recovery-audit

.PHONY: capstone-recovery-drill
capstone-recovery-drill: ## Run the selected program's capstone recovery drill
	@$(RUN_PROGRAM) capstone-recovery-drill

.PHONY: capstone-recovery-review
capstone-recovery-review: ## Build the selected program's capstone recovery review bundle
	@$(RUN_PROGRAM) capstone-recovery-review

.PHONY: capstone-experiment-review
capstone-experiment-review: ## Build the selected program's capstone experiment review bundle
	@$(RUN_PROGRAM) capstone-experiment-review

.PHONY: capstone-profile-audit
capstone-profile-audit: ## Build the selected program's capstone execution-policy audit bundle
	@$(RUN_PROGRAM) capstone-profile-audit

.PHONY: capstone-discovery-audit
capstone-discovery-audit: ## Build the selected program's capstone discovery audit bundle
	@$(RUN_PROGRAM) capstone-discovery-audit

.PHONY: capstone-portability-audit
capstone-portability-audit: ## Build the selected program's capstone portability audit bundle
	@$(RUN_PROGRAM) capstone-portability-audit

.PHONY: capstone-source-bundle
capstone-source-bundle: ## Build the selected program's tracked-source capstone bundle
	@$(RUN_PROGRAM) capstone-source-bundle

.PHONY: capstone-verify
capstone-verify: ## Run the selected program's capstone contract verification
	@$(RUN_PROGRAM) capstone-verify

.PHONY: capstone-confirm
capstone-confirm: ## Run the selected program's strongest capstone confirmation route
	@$(RUN_PROGRAM) capstone-confirm

.PHONY: clean
clean: ## Run clean for the selected program
	@$(RUN_PROGRAM) clean

.PHONY: docs-audit
docs-audit: ## Audit course-book and capstone documentation rules
	@$(PYTHON) scripts/audit_masterclass_docs.py

.PHONY: docs-nav-check
docs-nav-check: series-docs-build bijux-docs-check ## Check rendered masterclass navigation rows
	@$(PYTHON) scripts/check_masterclass_navigation.py
	@$(PYTHON) scripts/check_masterclass_library_tree.py
	@$(PYTHON) scripts/check_masterclass_shell.py

.PHONY: series-docs-venv
series-docs-venv: ## Create the virtual environment for the series site
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: series-docs-install
series-docs-install: series-docs-venv ## Install series documentation dependencies
	@$(PIP) install -r $(DOCS_REQUIREMENTS)

.PHONY: series-docs-build
series-docs-build: series-docs-install bijux-docs-sync ## Build the series documentation site
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(MKDOCS) build -f $(ROOT_MKDOCS_FILE) --strict

.PHONY: series-docs-serve
series-docs-serve: series-docs-install bijux-docs-sync ## Serve the series documentation site locally
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(ROOT_MKDOCS_FILE))
