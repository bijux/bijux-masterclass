SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
DOCS_DIR := docs
DOC_FILES := \
	architecture.md:ARCHITECTURE.md \
	command-guide.md:COMMAND_GUIDE.md \
	domain-guide.md:DOMAIN_GUIDE.md \
	extension-guide.md:EXTENSION_GUIDE.md \
	index.md:INDEX.md \
	package-guide.md:PACKAGE_GUIDE.md \
	proof-guide.md:PROOF_GUIDE.md \
	test-guide.md:TEST_GUIDE.md \
	tour.md:TOUR.md \
	walkthrough-guide.md:WALKTHROUGH_GUIDE.md
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
	@for doc in $(DOC_FILES); do \
		src=$${doc%%:*}; dest=$${doc#*:}; \
		cp $(DOCS_DIR)/$$src $(TOUR_DIR)/$$dest; \
		cp $(DOCS_DIR)/$$src $(TOUR_DIR)/docs/$$dest; \
	done
	@printf '%s\n' \
		'Walkthrough route:' \
		'  1. Read INDEX.md for the smallest local route.' \
		'  2. Read walkthrough.txt for the scenario output.' \
		'  3. Read DOMAIN_GUIDE.md, ARCHITECTURE.md, PACKAGE_GUIDE.md, and TOUR.md for the vocabulary, authority model, lifecycle, and narrative sequence.' \
		'  4. Read WALKTHROUGH_GUIDE.md, PROOF_GUIDE.md, and COMMAND_GUIDE.md for the scenario and command route.' \
		'  5. Read EXTENSION_GUIDE.md when you need the next honest change path.' \
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
	@for doc in $(DOC_FILES); do \
		src=$${doc%%:*}; dest=$${doc#*:}; \
		cp $(DOCS_DIR)/$$src $(INSPECT_DIR)/$$dest; \
		cp $(DOCS_DIR)/$$src $(INSPECT_DIR)/docs/$$dest; \
	done
	@printf '%s\n' \
		'Inspection route:' \
		'  1. Read INDEX.md and COMMAND_GUIDE.md for the smallest local route.' \
		'  2. Read summary.txt for the current policy and open incident state.' \
		'  3. Read rules.txt for rule lifecycle state.' \
		'  4. Read history.txt, timeline.txt, retirement.txt, rate_of_change.txt, and snapshot.json for shipped scenario variants and the structured state surface.' \
		'  5. Read ARCHITECTURE.md, DOMAIN_GUIDE.md, PROOF_GUIDE.md, PACKAGE_GUIDE.md, WALKTHROUGH_GUIDE.md, and COMMAND_GUIDE.md to connect the outputs to the code.' \
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
	@for doc in $(DOC_FILES); do \
		src=$${doc%%:*}; dest=$${doc#*:}; \
		cp $(DOCS_DIR)/$$src $(VERIFY_REPORT_DIR)/$$dest; \
		cp $(DOCS_DIR)/$$src $(VERIFY_REPORT_DIR)/docs/$$dest; \
	done
	@printf '%s\n' \
		'Verification route:' \
		'  1. Read INDEX.md and COMMAND_GUIDE.md for the local route into the saved bundle.' \
		'  2. Read pytest.txt for executable confirmation.' \
		'  3. Read summary.txt, history.txt, timeline.txt, retirement.txt, rate_of_change.txt, and snapshot.json for the learner-facing state, variants, and structured snapshot captured alongside the tests.' \
		'  4. Read PROOF_GUIDE.md, ARCHITECTURE.md, and DOMAIN_GUIDE.md for claim-to-evidence and authority routing.' \
		'  5. Read TEST_GUIDE.md, WALKTHROUGH_GUIDE.md, EXTENSION_GUIDE.md, and PROOF_GUIDE.md for the matching human review path.' \
		> $(VERIFY_REPORT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(VERIFY_REPORT_DIR) --output $(VERIFY_REPORT_DIR)/manifest.json
	@echo "wrote capstone verification report to $(VERIFY_REPORT_DIR)"

.PHONY: proof
proof: inspect tour verify-report ## Run the full learner proof route

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache $(INSPECT_DIR) $(TOUR_DIR) $(VERIFY_REPORT_DIR)
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
