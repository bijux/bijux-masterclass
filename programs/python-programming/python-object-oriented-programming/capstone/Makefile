SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
INSPECT_DIR ?= $(ARTIFACTS_DIR)/inspect/python-programming/python-object-oriented-programming
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/python-programming/python-object-oriented-programming
VERIFY_REPORT_DIR ?= $(ARTIFACTS_DIR)/review/python-programming/python-object-oriented-programming
WRITE_BUNDLE_MANIFEST := $(PYTHON) scripts/write_bundle_manifest.py

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone test suite
	@PYTHONPATH=src $(PYTHON) -m pytest -q

.PHONY: confirm
confirm: test proof ## Run the executable validation suite

.PHONY: demo
demo: ## Run the capstone scenario walkthrough
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.demo

.PHONY: tour
tour: ## Build the learner-facing walkthrough bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR)
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.demo > $(TOUR_DIR)/walkthrough.txt
	@cp README.md $(TOUR_DIR)/README.md
	@cp TOUR.md $(TOUR_DIR)/TOUR.md
	@cp DOMAIN_GUIDE.md $(TOUR_DIR)/DOMAIN_GUIDE.md
	@cp SCENARIO_GUIDE.md $(TOUR_DIR)/SCENARIO_GUIDE.md
	@cp RULE_LIFECYCLE_GUIDE.md $(TOUR_DIR)/RULE_LIFECYCLE_GUIDE.md
	@cp EVENT_FLOW_GUIDE.md $(TOUR_DIR)/EVENT_FLOW_GUIDE.md
	@cp BUNDLE_GUIDE.md $(TOUR_DIR)/BUNDLE_GUIDE.md
	@cp CHANGE_RECIPES.md $(TOUR_DIR)/CHANGE_RECIPES.md
	@cp SOURCE_GUIDE.md $(TOUR_DIR)/SOURCE_GUIDE.md
	@cp WALKTHROUGH_GUIDE.md $(TOUR_DIR)/WALKTHROUGH_GUIDE.md
	@cp ARCHITECTURE.md $(TOUR_DIR)/ARCHITECTURE.md
	@cp TARGET_GUIDE.md $(TOUR_DIR)/TARGET_GUIDE.md
	@printf '%s\n' \
		'Walkthrough route:' \
		'  1. Read walkthrough.txt for the scenario output.' \
		'  2. Read DOMAIN_GUIDE.md, SCENARIO_GUIDE.md, RULE_LIFECYCLE_GUIDE.md, and TOUR.md for the vocabulary, fixed inputs, lifecycle, and narrative sequence.' \
		'  3. Read WALKTHROUGH_GUIDE.md, EVENT_FLOW_GUIDE.md, and TARGET_GUIDE.md for the command and file route.' \
		'  4. Read ARCHITECTURE.md when you need object ownership while following the story.' \
		> $(TOUR_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(TOUR_DIR) --output $(TOUR_DIR)/manifest.json
	@echo "wrote learner-facing walkthrough bundle to $(TOUR_DIR)"

.PHONY: inspect-summary
inspect-summary: ## Inspect the scenario summary
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli summary

.PHONY: inspect-rules
inspect-rules: ## Inspect the rule lifecycle summary
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli rules

.PHONY: inspect-history
inspect-history: ## Inspect incident history by metric
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli history

.PHONY: inspect-timeline
inspect-timeline: ## Inspect the ordered scenario timeline
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli timeline

.PHONY: inspect
inspect: ## Build the capstone learner-facing inspection bundle
	@rm -rf $(INSPECT_DIR)
	@mkdir -p $(INSPECT_DIR)
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli summary > $(INSPECT_DIR)/summary.txt
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli rules > $(INSPECT_DIR)/rules.txt
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli history > $(INSPECT_DIR)/history.txt
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli timeline > $(INSPECT_DIR)/timeline.txt
	@cp README.md $(INSPECT_DIR)/README.md
	@cp ARCHITECTURE.md $(INSPECT_DIR)/ARCHITECTURE.md
	@cp DOMAIN_GUIDE.md $(INSPECT_DIR)/DOMAIN_GUIDE.md
	@cp SCENARIO_GUIDE.md $(INSPECT_DIR)/SCENARIO_GUIDE.md
	@cp RULE_LIFECYCLE_GUIDE.md $(INSPECT_DIR)/RULE_LIFECYCLE_GUIDE.md
	@cp BUNDLE_GUIDE.md $(INSPECT_DIR)/BUNDLE_GUIDE.md
	@cp CHANGE_RECIPES.md $(INSPECT_DIR)/CHANGE_RECIPES.md
	@cp SOURCE_GUIDE.md $(INSPECT_DIR)/SOURCE_GUIDE.md
	@cp PACKAGE_GUIDE.md $(INSPECT_DIR)/PACKAGE_GUIDE.md
	@cp TARGET_GUIDE.md $(INSPECT_DIR)/TARGET_GUIDE.md
	@cp INSPECTION_GUIDE.md $(INSPECT_DIR)/INSPECTION_GUIDE.md
	@cp EXTENSION_GUIDE.md $(INSPECT_DIR)/EXTENSION_GUIDE.md
	@printf '%s\n' \
		'Inspection route:' \
		'  1. Read summary.txt for the current policy and open incident state.' \
		'  2. Read rules.txt for rule lifecycle state.' \
		'  3. Read history.txt and timeline.txt for metric-level incident history and ordered scenario flow.' \
		'  4. Read DOMAIN_GUIDE.md, SCENARIO_GUIDE.md, RULE_LIFECYCLE_GUIDE.md, INSPECTION_GUIDE.md, PACKAGE_GUIDE.md, and TARGET_GUIDE.md to connect the outputs to the code.' \
		> $(INSPECT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(INSPECT_DIR) --output $(INSPECT_DIR)/manifest.json
	@echo "wrote learner-facing inspection bundle to $(INSPECT_DIR)"

.PHONY: verify-report
verify-report: ## Build the capstone verification report bundle
	@rm -rf $(VERIFY_REPORT_DIR)
	@mkdir -p $(VERIFY_REPORT_DIR)
	@PYTHONPATH=src $(PYTHON) -m pytest -q 2>&1 | tee $(VERIFY_REPORT_DIR)/pytest.txt
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli summary > $(VERIFY_REPORT_DIR)/summary.txt
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli history > $(VERIFY_REPORT_DIR)/history.txt
	@PYTHONPATH=src $(PYTHON) -m service_monitoring.cli timeline > $(VERIFY_REPORT_DIR)/timeline.txt
	@cp README.md $(VERIFY_REPORT_DIR)/README.md
	@cp PROOF_GUIDE.md $(VERIFY_REPORT_DIR)/PROOF_GUIDE.md
	@cp TEST_GUIDE.md $(VERIFY_REPORT_DIR)/TEST_GUIDE.md
	@cp EVENT_FLOW_GUIDE.md $(VERIFY_REPORT_DIR)/EVENT_FLOW_GUIDE.md
	@cp BUNDLE_GUIDE.md $(VERIFY_REPORT_DIR)/BUNDLE_GUIDE.md
	@cp WALKTHROUGH_GUIDE.md $(VERIFY_REPORT_DIR)/WALKTHROUGH_GUIDE.md
	@cp INSPECTION_GUIDE.md $(VERIFY_REPORT_DIR)/INSPECTION_GUIDE.md
	@printf '%s\n' \
		'Verification route:' \
		'  1. Read pytest.txt for executable confirmation.' \
		'  2. Read summary.txt, history.txt, and timeline.txt for the learner-facing state and sequence captured alongside the tests.' \
		'  3. Read PROOF_GUIDE.md and EVENT_FLOW_GUIDE.md for claim-to-evidence and event-to-artifact routing.' \
		'  4. Read TEST_GUIDE.md, WALKTHROUGH_GUIDE.md, and INSPECTION_GUIDE.md for the matching human review path.' \
		> $(VERIFY_REPORT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(VERIFY_REPORT_DIR) --output $(VERIFY_REPORT_DIR)/manifest.json
	@echo "wrote capstone verification report to $(VERIFY_REPORT_DIR)"

.PHONY: proof
proof: inspect tour verify-report ## Run the full learner proof route

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache $(INSPECT_DIR) $(TOUR_DIR) $(VERIFY_REPORT_DIR)
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
