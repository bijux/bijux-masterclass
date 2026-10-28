SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
PYTHON ?= python3

.PHONY: help program-help doctor setup predecessor-proof handoff-proof test hcl-check \
        links-proof core-proof capstone-tour manifest-build manifest-proof tofu-proof \
        aws-preflight aws-plan-foundation aws-plan-workload aws-apply-foundation \
        aws-apply-workload aws-destroy-workload aws-destroy-foundation docs-build \
        docs-serve clean

help: ## Show stable course commands.
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-26s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

program-help: help ## Alias used by the Bijux Masterclass program router.

doctor: ## Classify available local, OpenTofu, AWS, and documentation environments.
	$(PYTHON) scripts/doctor.py

setup: ## Install Python proof and documentation dependencies in the current environment.
	$(PYTHON) -m pip install -r requirements.txt -r requirements-docs.txt

predecessor-proof: ## Verify the exact Course 1 handoff.
	$(PYTHON) scripts/verify_handoff.py

handoff-proof: ## Verify predecessor and outgoing Course 3 handoffs.
	$(PYTHON) scripts/verify_handoff.py

test: ## Run the dependency-light semantic and inherited runtime tests.
	PYTHONPATH=capstone:capstone/runtime $(PYTHON) -m pytest -q capstone/tests

hcl-check: ## Run dependency-light HCL safety and pin guards.
	$(PYTHON) scripts/hcl_guard.py

links-proof: ## Verify local Markdown links.
	$(PYTHON) scripts/check_links.py

capstone-tour: ## Run the local Atlas planning, identity, network, workload, and recovery tour.
	PYTHONPATH=capstone:capstone/runtime $(PYTHON) capstone/scripts/run_capstone_tour.py

core-proof: ## Run the complete dependency-light course proof.
	$(PYTHON) scripts/course_proof.py

manifest-build: ## Generate the exact course manifest after final source changes.
	$(PYTHON) scripts/course_manifest.py build

manifest-proof: ## Verify the exact course manifest.
	$(PYTHON) scripts/course_manifest.py verify

tofu-proof: ## Run native OpenTofu formatting and dependency-light naming-module tests.
	@command -v tofu >/dev/null || { echo "tofu is required for tofu-proof" >&2; exit 2; }
	tofu fmt -check -recursive capstone
	cd capstone/modules/naming && tofu init -backend=false && tofu test

aws-preflight: ## Verify tool, account, and region identity before any AWS plan/apply.
	$(PYTHON) scripts/aws_preflight.py

aws-plan-foundation: aws-preflight ## Produce a saved foundation plan in the declared sandbox.
	@command -v tofu >/dev/null
	cd capstone/stacks/foundation && tofu init -reconfigure -backend-config=backend.hcl && tofu plan -out=foundation.tfplan

aws-plan-workload: aws-preflight ## Produce a saved workload plan in the declared sandbox.
	@command -v tofu >/dev/null
	cd capstone/stacks/workload-dev && tofu init -reconfigure -backend-config=backend.hcl && tofu plan -out=workload.tfplan

aws-apply-foundation: aws-preflight ## Apply the reviewed saved foundation plan; requires ALLOW_AWS_APPLY=1.
	@test "$${ALLOW_AWS_APPLY:-}" = 1 || { echo "set ALLOW_AWS_APPLY=1 after review" >&2; exit 2; }
	cd capstone/stacks/foundation && tofu apply foundation.tfplan

aws-apply-workload: aws-preflight ## Apply the reviewed saved workload plan; requires ALLOW_AWS_APPLY=1.
	@test "$${ALLOW_AWS_APPLY:-}" = 1 || { echo "set ALLOW_AWS_APPLY=1 after review" >&2; exit 2; }
	cd capstone/stacks/workload-dev && tofu apply workload.tfplan

aws-destroy-workload: aws-preflight ## Destroy the sandbox workload root after explicit opt-in.
	@test "$${ALLOW_AWS_DESTROY:-}" = 1 || { echo "set ALLOW_AWS_DESTROY=1" >&2; exit 2; }
	cd capstone/stacks/workload-dev && tofu destroy

aws-destroy-foundation: aws-preflight ## Destroy the sandbox foundation root after workload cleanup and opt-in.
	@test "$${ALLOW_AWS_DESTROY:-}" = 1 || { echo "set ALLOW_AWS_DESTROY=1" >&2; exit 2; }
	cd capstone/stacks/foundation && tofu destroy

docs-build: ## Build the reader site strictly when MkDocs is installed.
	@command -v mkdocs >/dev/null || { echo "mkdocs is required" >&2; exit 2; }
	mkdocs build --strict

docs-serve: ## Serve the course book locally.
	@command -v mkdocs >/dev/null || { echo "mkdocs is required" >&2; exit 2; }
	mkdocs serve

clean: ## Remove generated proof, cache, plan, site, and OpenTofu working files.
	rm -rf .pytest_cache site reports/core-proof.json capstone/reports/*.json
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.tfplan' \) -delete
	find capstone -type d -name .terraform -prune -exec rm -rf {} +
