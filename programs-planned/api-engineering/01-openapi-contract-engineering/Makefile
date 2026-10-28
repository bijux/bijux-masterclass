SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

CAPSTONE_DIR := capstone
ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/api-engineering/openapi-contract-engineering
COURSE_VENV_DIR ?= .venv
PYTHON ?= python3
MKDOCS ?= $(COURSE_VENV_DIR)/bin/mkdocs

define run_capstone
	@tool=make; \
	if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; \
	$$tool -C $(CAPSTONE_DIR) $(1)
endef

.PHONY: help doctor setup docs-build docs-serve core-proof test \
	capstone-walkthrough capstone-tour capstone-confirm capstone-verify-report \
	capability-report typescript-audit handoff-export manifest-create manifest-proof proof clean

help: ## Show stable program entrypoints.
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-28s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

doctor: ## Check host tools and course structure.
	$(call run_capstone,doctor)

setup: ## Install pinned Python and Node dependencies.
	$(call run_capstone,setup)

docs-build: ## Build the MkDocs course site.
	@mkdir -p "$(SITE_DIR)"
	@if [ ! -x "$(MKDOCS)" ]; then \
		printf '%s\n' "mkdocs is not installed in $(COURSE_VENV_DIR). Run 'make setup'."; \
		exit 2; \
	fi
	"$(MKDOCS)" build --strict --site-dir "$(SITE_DIR)"

docs-serve: ## Serve course documentation locally.
	@if [ ! -x "$(MKDOCS)" ]; then \
		printf '%s\n' "mkdocs is not installed in $(COURSE_VENV_DIR). Run 'make setup'."; \
		exit 2; \
	fi
	"$(MKDOCS)" serve

core-proof: ## Run dependency-light contract, schema, reference, workflow, and documentation gates.
	$(call run_capstone,core-proof)

test: ## Run complete local contract, Python, and TypeScript suites.
	$(call run_capstone,test)

capstone-walkthrough: ## Print the narrated capstone walkthrough.
	$(call run_capstone,walkthrough)

capstone-tour: ## Run the deterministic capstone evidence tour.
	$(call run_capstone,tour)

capstone-confirm: ## Run all local completion gates.
	$(call run_capstone,confirm)

capstone-verify-report: ## Produce a machine-readable local verification report.
	$(call run_capstone,verify-report)

capability-report: ## Inventory pinned tools; feature support is proven separately in Module 10.
	$(call run_capstone,capability-report)

typescript-audit: ## Semantically compile the TypeScript provider and client without installed framework packages.
	$(call run_capstone,typescript-audit)

handoff-export: core-proof ## Export the immutable Course 1 → Course 2 handoff.
	$(PYTHON) capstone/scripts/export_handoff.py

manifest-create: ## Create the deterministic course payload manifest.
	$(PYTHON) capstone/scripts/course_manifest.py create

manifest-proof: ## Verify the exact course payload against its manifest.
	$(PYTHON) capstone/scripts/course_manifest.py verify

proof: ## Run the strongest proof route and write its report.
	$(call run_capstone,proof)

clean: ## Remove generated sites, reports, caches, bundles, and clients.
	$(call run_capstone,clean)
	@rm -rf "$(SITE_DIR)"
