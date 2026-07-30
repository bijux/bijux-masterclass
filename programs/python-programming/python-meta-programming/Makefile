SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

CAPSTONE_DIR := capstone
RUN_CAPSTONE = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(CAPSTONE_DIR)
PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/python-programming/python-meta-programming
COURSE_VENV_DIR ?= $(ARTIFACTS_DIR)/venv/python-programming/python-meta-programming

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: lab-test ## Run course labs and the capstone confirmation suite
	@$(RUN_CAPSTONE) confirm

.PHONY: lab
lab: ## Run the Module 01 runtime-object evidence lab
	@$(PYTHON) -m labs.runtime_objects

.PHONY: lab-test
lab-test: ## Verify the executable course labs
	@$(PYTHON) -m unittest discover -s tests -v

.PHONY: observation-lab
observation-lab: ## Run the Module 02 safe-observation evidence lab
	@$(PYTHON) -m labs.runtime_observation

.PHONY: observation-lab-test
observation-lab-test: ## Verify the Module 02 observation boundaries
	@$(PYTHON) -m unittest discover -s tests -p "test_runtime_observation_lab.py" -v

.PHONY: observation-debug-view
observation-debug-view: ## Render the Module 02 attachment-first debug view
	@$(PYTHON) -m labs.runtime_observation.debug_demo

.PHONY: evidence-lab
evidence-lab: ## Run the Module 03 runtime-evidence trust lab
	@$(PYTHON) -m labs.runtime_evidence

.PHONY: evidence-lab-test
evidence-lab-test: ## Verify the Module 03 evidence classifications
	@$(PYTHON) -m unittest discover -s tests -p "test_runtime_evidence_lab.py" -v

.PHONY: evidence-repr
evidence-repr: ## Run the Module 03 signature-guided representation
	@$(PYTHON) -m labs.runtime_evidence.repr_demo

.PHONY: evidence-repr-test
evidence-repr-test: ## Verify the Module 03 representation boundaries
	@$(PYTHON) -m unittest discover -s tests -p "test_signature_guided_repr.py" -v

.PHONY: wrapper-lab
wrapper-lab: ## Run the Module 04 wrapper lifecycle evidence lab
	@$(PYTHON) -m labs.wrapper_runtime

.PHONY: wrapper-lab-test
wrapper-lab-test: ## Verify Module 04 wrapper timing and transparency
	@$(PYTHON) -m unittest discover -s tests -p "test_wrapper_runtime_lab.py" -v

.PHONY: wrapper-cache
wrapper-cache: ## Run the Module 04 bounded-cache worked example
	@$(PYTHON) -m labs.wrapper_runtime.cache_demo

.PHONY: wrapper-cache-test
wrapper-cache-test: ## Verify the Module 04 bounded-cache policy
	@$(PYTHON) -m unittest discover -s tests -p "test_bounded_cache_lab.py" -v

.PHONY: demo
demo: ## Run one learner-facing capstone invocation
	@$(RUN_CAPSTONE) demo

.PHONY: inspect
inspect: ## Inspect the capstone learner-facing public surface
	@$(RUN_CAPSTONE) inspect

.PHONY: capstone-tour
capstone-tour: ## Build the learner-facing capstone proof bundle
	@$(RUN_CAPSTONE) tour

.PHONY: capstone-walkthrough
capstone-walkthrough: ## Build the learner-facing capstone walkthrough bundle
	@$(RUN_CAPSTONE) tour

.PHONY: capstone-verify-report
capstone-verify-report: ## Build the capstone verification report bundle
	@$(RUN_CAPSTONE) verify-report

.PHONY: capstone-confirm
capstone-confirm: ## Run the capstone's strongest confirmation route
	@$(RUN_CAPSTONE) confirm

.PHONY: proof
proof: ## Run the full capstone proof route
	@$(RUN_CAPSTONE) proof

.PHONY: capstone-manifest
capstone-manifest: ## Render the capstone manifest from the public CLI
	@$(RUN_CAPSTONE) manifest

.PHONY: capstone-bind-action
capstone-bind-action: ## Validate a capstone action call without executing it
	@$(RUN_CAPSTONE) bind-action

.PHONY: capstone-trace
capstone-trace: ## Trace one capstone invocation from the public CLI
	@$(RUN_CAPSTONE) trace

.PHONY: clean
clean: ## Remove build and virtualenv artifacts
	@rm -rf $(COURSE_VENV_DIR) $(SITE_DIR) .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@$(RUN_CAPSTONE) clean
