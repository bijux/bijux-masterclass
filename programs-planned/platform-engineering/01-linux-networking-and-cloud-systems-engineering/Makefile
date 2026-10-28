SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help
PYTHON ?= python3
COURSE_VENV ?= .venv
MKDOCS ?= $(COURSE_VENV)/bin/mkdocs
SITE_DIR ?= ../../../artifacts/site/platform-engineering/linux-networking-and-cloud-systems-engineering

.PHONY: help doctor setup docs-build docs-serve core-proof test capstone-tour linux-proof systemd-proof pki-proof nginx-proof handoff-export manifest-create manifest-proof proof clean

help: ## Show stable course entrypoints.
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-28s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

doctor: ## Classify host evidence capabilities.
	$(MAKE) -C capstone doctor

setup: ## Create a local environment and install course/documentation dependencies.
	$(PYTHON) -m venv $(COURSE_VENV)
	$(COURSE_VENV)/bin/pip install -r requirements.txt -r requirements-docs.txt

docs-build: ## Build the course book with strict MkDocs checks.
	@test -x $(MKDOCS) || { echo "Run make setup first"; exit 2; }
	$(MKDOCS) build --strict --site-dir $(SITE_DIR)

docs-serve: ## Serve the course book locally.
	@test -x $(MKDOCS) || { echo "Run make setup first"; exit 2; }
	$(MKDOCS) serve

core-proof: ## Run the dependency-light course proof.
	$(MAKE) -C capstone core-proof

test: ## Run capstone tests.
	$(MAKE) -C capstone test

capstone-tour: ## Run the local HTTPS API/worker/edge tour.
	$(MAKE) -C capstone tour

linux-proof: ## Capture real Linux host evidence.
	$(MAKE) -C capstone linux-proof

systemd-proof: ## Verify systemd units.
	$(MAKE) -C capstone systemd-proof

pki-proof: ## Verify local PKI fixtures.
	$(MAKE) -C capstone pki-proof

nginx-proof: ## Verify the Nginx reference configuration when Nginx is available.
	$(MAKE) -C capstone nginx-proof

handoff-export: ## Rebuild Course 2 handoff evidence.
	$(MAKE) -C capstone handoff-export

manifest-create: ## Create exact course payload manifest.
	$(PYTHON) capstone/scripts/course_manifest.py create

manifest-proof: ## Verify exact course payload manifest.
	$(PYTHON) capstone/scripts/course_manifest.py verify

proof: core-proof capstone-tour manifest-proof ## Run the strongest dependency-light release route.

clean: ## Remove generated course outputs.
	$(MAKE) -C capstone clean
	@rm -rf $(SITE_DIR) .pytest_cache __pycache__
