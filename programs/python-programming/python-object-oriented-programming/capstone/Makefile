SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
DOCS_DIR := docs
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/python-programming/python-object-oriented-programming/capstone
VENV_BIN := $(VENV_DIR)/bin
VENV_PY := $(abspath $(VENV_BIN)/python)
PIP := $(VENV_PY) -m pip
INSPECT_DIR ?= $(ARTIFACTS_DIR)/inspect/python-programming/python-object-oriented-programming
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/python-programming/python-object-oriented-programming
VERIFY_REPORT_DIR ?= $(ARTIFACTS_DIR)/review/python-programming/python-object-oriented-programming
WRITE_BUNDLE_MANIFEST := $(VENV_PY) scripts/write_bundle_manifest.py

$(VENV_PY):
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: install
install: $(VENV_PY) ## Install the capstone test environment
	@$(PIP) install -e . pytest

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: install ## Run the capstone test suite
	@PYTHONPATH=src $(VENV_PY) -m pytest -q

.PHONY: confirm
confirm: test proof ## Run the executable validation suite

.PHONY: demo
demo: ## Run the capstone scenario walkthrough
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.demo

.PHONY: tour
tour: ## Build the learner-facing walkthrough bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR) $(TOUR_DIR)/docs
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.demo > $(TOUR_DIR)/walkthrough.txt
	@cp README.md $(TOUR_DIR)/README.md
	@cp $(DOCS_DIR)/GUIDE_INDEX.md $(TOUR_DIR)/GUIDE_INDEX.md
	@cp $(DOCS_DIR)/FIRST_SESSION_GUIDE.md $(TOUR_DIR)/FIRST_SESSION_GUIDE.md
	@cp $(DOCS_DIR)/COMMAND_GUIDE.md $(TOUR_DIR)/COMMAND_GUIDE.md
	@cp $(DOCS_DIR)/OWNERSHIP_BOUNDARIES.md $(TOUR_DIR)/OWNERSHIP_BOUNDARIES.md
	@cp $(DOCS_DIR)/SCENARIO_BOUNDARY_MAP.md $(TOUR_DIR)/SCENARIO_BOUNDARY_MAP.md
	@cp $(DOCS_DIR)/TOUR.md $(TOUR_DIR)/TOUR.md
	@cp $(DOCS_DIR)/DOMAIN_GUIDE.md $(TOUR_DIR)/DOMAIN_GUIDE.md
	@cp $(DOCS_DIR)/SCENARIO_GUIDE.md $(TOUR_DIR)/SCENARIO_GUIDE.md
	@cp $(DOCS_DIR)/RETIREMENT_SCENARIO_GUIDE.md $(TOUR_DIR)/RETIREMENT_SCENARIO_GUIDE.md
	@cp $(DOCS_DIR)/RATE_OF_CHANGE_SCENARIO_GUIDE.md $(TOUR_DIR)/RATE_OF_CHANGE_SCENARIO_GUIDE.md
	@cp $(DOCS_DIR)/RULE_LIFECYCLE_GUIDE.md $(TOUR_DIR)/RULE_LIFECYCLE_GUIDE.md
	@cp $(DOCS_DIR)/EVENT_FLOW_GUIDE.md $(TOUR_DIR)/EVENT_FLOW_GUIDE.md
	@cp $(DOCS_DIR)/BUNDLE_GUIDE.md $(TOUR_DIR)/BUNDLE_GUIDE.md
	@cp $(DOCS_DIR)/MANIFEST_GUIDE.md $(TOUR_DIR)/MANIFEST_GUIDE.md
	@cp $(DOCS_DIR)/CHANGE_RECIPES.md $(TOUR_DIR)/CHANGE_RECIPES.md
	@cp $(DOCS_DIR)/PUBLIC_API_GUIDE.md $(TOUR_DIR)/PUBLIC_API_GUIDE.md
	@cp $(DOCS_DIR)/RUNTIME_GUIDE.md $(TOUR_DIR)/RUNTIME_GUIDE.md
	@cp $(DOCS_DIR)/PROJECTION_GUIDE.md $(TOUR_DIR)/PROJECTION_GUIDE.md
	@cp $(DOCS_DIR)/SOURCE_GUIDE.md $(TOUR_DIR)/SOURCE_GUIDE.md
	@cp $(DOCS_DIR)/SCENARIO_SELECTION_GUIDE.md $(TOUR_DIR)/SCENARIO_SELECTION_GUIDE.md
	@cp $(DOCS_DIR)/WALKTHROUGH_GUIDE.md $(TOUR_DIR)/WALKTHROUGH_GUIDE.md
	@cp $(DOCS_DIR)/ARCHITECTURE.md $(TOUR_DIR)/ARCHITECTURE.md
	@cp $(DOCS_DIR)/TARGET_GUIDE.md $(TOUR_DIR)/TARGET_GUIDE.md
	@cp $(DOCS_DIR)/*.md $(TOUR_DIR)/
	@cp $(DOCS_DIR)/*.md $(TOUR_DIR)/docs/
	@printf '%s\n' \
		'Walkthrough route:' \
		'  1. Read GUIDE_INDEX.md and FIRST_SESSION_GUIDE.md for the smallest local route.' \
		'  2. Read walkthrough.txt for the scenario output.' \
		'  3. Read DOMAIN_GUIDE.md, SCENARIO_GUIDE.md, RULE_LIFECYCLE_GUIDE.md, OWNERSHIP_BOUNDARIES.md, and TOUR.md for the vocabulary, authority model, lifecycle, and narrative sequence.' \
		'  4. Read SCENARIO_BOUNDARY_MAP.md, WALKTHROUGH_GUIDE.md, EVENT_FLOW_GUIDE.md, TARGET_GUIDE.md, and COMMAND_GUIDE.md for the scenario and command route.' \
		'  5. Read ARCHITECTURE.md when you need object ownership while following the story.' \
		> $(TOUR_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(TOUR_DIR) --output $(TOUR_DIR)/manifest.json
	@echo "wrote learner-facing walkthrough bundle to $(TOUR_DIR)"

.PHONY: inspect-summary
inspect-summary: ## Inspect the scenario summary
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli summary

.PHONY: inspect-rules
inspect-rules: ## Inspect the rule lifecycle summary
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli rules

.PHONY: inspect-history
inspect-history: ## Inspect incident history by metric
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli history

.PHONY: inspect-timeline
inspect-timeline: ## Inspect the ordered scenario timeline
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli timeline

.PHONY: inspect-retirement
inspect-retirement: ## Inspect the retirement scenario before and after state
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli retirement

.PHONY: inspect-rate-of-change
inspect-rate-of-change: ## Inspect the alternate rate-of-change scenario
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli rate-of-change

.PHONY: inspect-json
inspect-json: ## Inspect the default scenario as machine-readable JSON
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli snapshot-json

.PHONY: inspect
inspect: ## Build the capstone learner-facing inspection bundle
	@rm -rf $(INSPECT_DIR)
	@mkdir -p $(INSPECT_DIR) $(INSPECT_DIR)/docs
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli summary > $(INSPECT_DIR)/summary.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli rules > $(INSPECT_DIR)/rules.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli history > $(INSPECT_DIR)/history.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli timeline > $(INSPECT_DIR)/timeline.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli retirement > $(INSPECT_DIR)/retirement.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli rate-of-change > $(INSPECT_DIR)/rate_of_change.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli snapshot-json > $(INSPECT_DIR)/snapshot.json
	@cp README.md $(INSPECT_DIR)/README.md
	@cp $(DOCS_DIR)/GUIDE_INDEX.md $(INSPECT_DIR)/GUIDE_INDEX.md
	@cp $(DOCS_DIR)/FIRST_SESSION_GUIDE.md $(INSPECT_DIR)/FIRST_SESSION_GUIDE.md
	@cp $(DOCS_DIR)/COMMAND_GUIDE.md $(INSPECT_DIR)/COMMAND_GUIDE.md
	@cp $(DOCS_DIR)/OWNERSHIP_BOUNDARIES.md $(INSPECT_DIR)/OWNERSHIP_BOUNDARIES.md
	@cp $(DOCS_DIR)/SCENARIO_BOUNDARY_MAP.md $(INSPECT_DIR)/SCENARIO_BOUNDARY_MAP.md
	@cp $(DOCS_DIR)/ARCHITECTURE.md $(INSPECT_DIR)/ARCHITECTURE.md
	@cp $(DOCS_DIR)/DOMAIN_GUIDE.md $(INSPECT_DIR)/DOMAIN_GUIDE.md
	@cp $(DOCS_DIR)/SCENARIO_GUIDE.md $(INSPECT_DIR)/SCENARIO_GUIDE.md
	@cp $(DOCS_DIR)/RETIREMENT_SCENARIO_GUIDE.md $(INSPECT_DIR)/RETIREMENT_SCENARIO_GUIDE.md
	@cp $(DOCS_DIR)/RATE_OF_CHANGE_SCENARIO_GUIDE.md $(INSPECT_DIR)/RATE_OF_CHANGE_SCENARIO_GUIDE.md
	@cp $(DOCS_DIR)/RULE_LIFECYCLE_GUIDE.md $(INSPECT_DIR)/RULE_LIFECYCLE_GUIDE.md
	@cp $(DOCS_DIR)/BUNDLE_GUIDE.md $(INSPECT_DIR)/BUNDLE_GUIDE.md
	@cp $(DOCS_DIR)/MANIFEST_GUIDE.md $(INSPECT_DIR)/MANIFEST_GUIDE.md
	@cp $(DOCS_DIR)/CHANGE_RECIPES.md $(INSPECT_DIR)/CHANGE_RECIPES.md
	@cp $(DOCS_DIR)/PUBLIC_API_GUIDE.md $(INSPECT_DIR)/PUBLIC_API_GUIDE.md
	@cp $(DOCS_DIR)/RUNTIME_GUIDE.md $(INSPECT_DIR)/RUNTIME_GUIDE.md
	@cp $(DOCS_DIR)/PROJECTION_GUIDE.md $(INSPECT_DIR)/PROJECTION_GUIDE.md
	@cp $(DOCS_DIR)/SOURCE_GUIDE.md $(INSPECT_DIR)/SOURCE_GUIDE.md
	@cp $(DOCS_DIR)/SCENARIO_SELECTION_GUIDE.md $(INSPECT_DIR)/SCENARIO_SELECTION_GUIDE.md
	@cp $(DOCS_DIR)/PACKAGE_GUIDE.md $(INSPECT_DIR)/PACKAGE_GUIDE.md
	@cp $(DOCS_DIR)/TARGET_GUIDE.md $(INSPECT_DIR)/TARGET_GUIDE.md
	@cp $(DOCS_DIR)/INSPECTION_GUIDE.md $(INSPECT_DIR)/INSPECTION_GUIDE.md
	@cp $(DOCS_DIR)/EXTENSION_GUIDE.md $(INSPECT_DIR)/EXTENSION_GUIDE.md
	@cp $(DOCS_DIR)/*.md $(INSPECT_DIR)/
	@cp $(DOCS_DIR)/*.md $(INSPECT_DIR)/docs/
	@printf '%s\n' \
		'Inspection route:' \
		'  1. Read GUIDE_INDEX.md, FIRST_SESSION_GUIDE.md, and COMMAND_GUIDE.md for the smallest local route.' \
		'  2. Read summary.txt for the current policy and open incident state.' \
		'  3. Read rules.txt for rule lifecycle state.' \
		'  4. Read history.txt, timeline.txt, retirement.txt, rate_of_change.txt, and snapshot.json for shipped scenario variants and the structured state surface.' \
		'  5. Read OWNERSHIP_BOUNDARIES.md, SCENARIO_BOUNDARY_MAP.md, DOMAIN_GUIDE.md, SCENARIO_GUIDE.md, RULE_LIFECYCLE_GUIDE.md, RETIREMENT_SCENARIO_GUIDE.md, RATE_OF_CHANGE_SCENARIO_GUIDE.md, INSPECTION_GUIDE.md, PACKAGE_GUIDE.md, and TARGET_GUIDE.md to connect the outputs to the code.' \
		> $(INSPECT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(INSPECT_DIR) --output $(INSPECT_DIR)/manifest.json
	@echo "wrote learner-facing inspection bundle to $(INSPECT_DIR)"

.PHONY: verify-report
verify-report: ## Build the capstone verification report bundle
	@rm -rf $(VERIFY_REPORT_DIR)
	@mkdir -p $(VERIFY_REPORT_DIR) $(VERIFY_REPORT_DIR)/docs
	@PYTHONPATH=src $(VENV_PY) -m pytest -q 2>&1 | tee $(VERIFY_REPORT_DIR)/pytest.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli summary > $(VERIFY_REPORT_DIR)/summary.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli history > $(VERIFY_REPORT_DIR)/history.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli timeline > $(VERIFY_REPORT_DIR)/timeline.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli retirement > $(VERIFY_REPORT_DIR)/retirement.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli rate-of-change > $(VERIFY_REPORT_DIR)/rate_of_change.txt
	@PYTHONPATH=src $(VENV_PY) -m service_monitoring.cli snapshot-json > $(VERIFY_REPORT_DIR)/snapshot.json
	@cp README.md $(VERIFY_REPORT_DIR)/README.md
	@cp $(DOCS_DIR)/GUIDE_INDEX.md $(VERIFY_REPORT_DIR)/GUIDE_INDEX.md
	@cp $(DOCS_DIR)/FIRST_SESSION_GUIDE.md $(VERIFY_REPORT_DIR)/FIRST_SESSION_GUIDE.md
	@cp $(DOCS_DIR)/COMMAND_GUIDE.md $(VERIFY_REPORT_DIR)/COMMAND_GUIDE.md
	@cp $(DOCS_DIR)/OWNERSHIP_BOUNDARIES.md $(VERIFY_REPORT_DIR)/OWNERSHIP_BOUNDARIES.md
	@cp $(DOCS_DIR)/SCENARIO_BOUNDARY_MAP.md $(VERIFY_REPORT_DIR)/SCENARIO_BOUNDARY_MAP.md
	@cp $(DOCS_DIR)/PROOF_GUIDE.md $(VERIFY_REPORT_DIR)/PROOF_GUIDE.md
	@cp $(DOCS_DIR)/TEST_GUIDE.md $(VERIFY_REPORT_DIR)/TEST_GUIDE.md
	@cp $(DOCS_DIR)/EVENT_FLOW_GUIDE.md $(VERIFY_REPORT_DIR)/EVENT_FLOW_GUIDE.md
	@cp $(DOCS_DIR)/BUNDLE_GUIDE.md $(VERIFY_REPORT_DIR)/BUNDLE_GUIDE.md
	@cp $(DOCS_DIR)/MANIFEST_GUIDE.md $(VERIFY_REPORT_DIR)/MANIFEST_GUIDE.md
	@cp $(DOCS_DIR)/PUBLIC_API_GUIDE.md $(VERIFY_REPORT_DIR)/PUBLIC_API_GUIDE.md
	@cp $(DOCS_DIR)/RUNTIME_GUIDE.md $(VERIFY_REPORT_DIR)/RUNTIME_GUIDE.md
	@cp $(DOCS_DIR)/PROJECTION_GUIDE.md $(VERIFY_REPORT_DIR)/PROJECTION_GUIDE.md
	@cp $(DOCS_DIR)/RETIREMENT_SCENARIO_GUIDE.md $(VERIFY_REPORT_DIR)/RETIREMENT_SCENARIO_GUIDE.md
	@cp $(DOCS_DIR)/RATE_OF_CHANGE_SCENARIO_GUIDE.md $(VERIFY_REPORT_DIR)/RATE_OF_CHANGE_SCENARIO_GUIDE.md
	@cp $(DOCS_DIR)/SCENARIO_SELECTION_GUIDE.md $(VERIFY_REPORT_DIR)/SCENARIO_SELECTION_GUIDE.md
	@cp $(DOCS_DIR)/WALKTHROUGH_GUIDE.md $(VERIFY_REPORT_DIR)/WALKTHROUGH_GUIDE.md
	@cp $(DOCS_DIR)/INSPECTION_GUIDE.md $(VERIFY_REPORT_DIR)/INSPECTION_GUIDE.md
	@cp $(DOCS_DIR)/*.md $(VERIFY_REPORT_DIR)/
	@cp $(DOCS_DIR)/*.md $(VERIFY_REPORT_DIR)/docs/
	@printf '%s\n' \
		'Verification route:' \
		'  1. Read GUIDE_INDEX.md, FIRST_SESSION_GUIDE.md, and COMMAND_GUIDE.md for the local route into the saved bundle.' \
		'  2. Read pytest.txt for executable confirmation.' \
		'  3. Read summary.txt, history.txt, timeline.txt, retirement.txt, rate_of_change.txt, and snapshot.json for the learner-facing state, variants, and structured snapshot captured alongside the tests.' \
		'  4. Read PROOF_GUIDE.md, OWNERSHIP_BOUNDARIES.md, SCENARIO_BOUNDARY_MAP.md, and EVENT_FLOW_GUIDE.md for claim-to-evidence and authority routing.' \
		'  5. Read TEST_GUIDE.md, WALKTHROUGH_GUIDE.md, INSPECTION_GUIDE.md, RETIREMENT_SCENARIO_GUIDE.md, and RATE_OF_CHANGE_SCENARIO_GUIDE.md for the matching human review path.' \
		> $(VERIFY_REPORT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(VERIFY_REPORT_DIR) --output $(VERIFY_REPORT_DIR)/manifest.json
	@echo "wrote capstone verification report to $(VERIFY_REPORT_DIR)"

.PHONY: proof
proof: inspect tour verify-report ## Run the full learner proof route

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache $(INSPECT_DIR) $(TOUR_DIR) $(VERIFY_REPORT_DIR)
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
