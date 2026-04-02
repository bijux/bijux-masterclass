SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/python-programming/python-meta-programming
INSPECT_DIR ?= $(ARTIFACTS_DIR)/inspect/python-programming/python-meta-programming
VERIFY_REPORT_DIR ?= $(ARTIFACTS_DIR)/review/python-programming/python-meta-programming
CLI := $(PYTHON) -m incident_plugins.cli
WRITE_BUNDLE_MANIFEST := $(PYTHON) scripts/write_bundle_manifest.py

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone test suite
	@$(PYTHON) -m pytest -q

.PHONY: confirm
confirm: test ## Run the executable validation suite

.PHONY: manifest
manifest: ## Render the delivery manifest from the public CLI
	@PYTHONPATH=src $(CLI) manifest --group delivery

.PHONY: registry
registry: ## Render the delivery registry from the public CLI
	@PYTHONPATH=src $(CLI) registry --group delivery

.PHONY: demo
demo: ## Invoke one delivery action from the public CLI
	@PYTHONPATH=src $(CLI) invoke delivery console deliver \
		--config "prefix=[ops]" \
		--config "uppercase_severity=true" \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%"

.PHONY: trace
trace: ## Trace one delivery action and its recorded history
	@PYTHONPATH=src $(CLI) trace delivery pager preview \
		--config "service=core" \
		--config "routing_key=sev1" \
		--arg "title=Queue lag" \
		--arg "severity=critical" \
		--arg "summary=worker backlog growing"

.PHONY: inspect
inspect: ## Build the learner-facing inspection bundle
	@rm -rf $(INSPECT_DIR)
	@mkdir -p $(INSPECT_DIR)
	@PYTHONPATH=src $(CLI) manifest --group delivery > $(INSPECT_DIR)/manifest.json
	@PYTHONPATH=src $(CLI) registry --group delivery > $(INSPECT_DIR)/registry.json
	@cp README.md $(INSPECT_DIR)/README.md
	@cp PACKAGE_GUIDE.md $(INSPECT_DIR)/PACKAGE_GUIDE.md
	@cp TARGET_GUIDE.md $(INSPECT_DIR)/TARGET_GUIDE.md
	@cp INSPECTION_GUIDE.md $(INSPECT_DIR)/INSPECTION_GUIDE.md
	@cp PROOF_GUIDE.md $(INSPECT_DIR)/PROOF_GUIDE.md
	@printf '%s\n' \
		'Inspection route:' \
		'  1. Read manifest.json for field and action metadata.' \
		'  2. Read registry.json for the registered plugin names.' \
		'  3. Read INSPECTION_GUIDE.md and TARGET_GUIDE.md for the next review route.' \
		'  4. Read PACKAGE_GUIDE.md when you need to connect the outputs back to source ownership.' \
		> $(INSPECT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(INSPECT_DIR) --output $(INSPECT_DIR)/bundle-manifest.json
	@echo "wrote learner-facing inspection bundle to $(INSPECT_DIR)"

.PHONY: proof
proof: inspect tour verify-report ## Run the full public proof route

.PHONY: verify-report
verify-report: ## Build the structured capstone verification report
	@rm -rf $(VERIFY_REPORT_DIR)
	@mkdir -p $(VERIFY_REPORT_DIR)
	@$(PYTHON) -m pytest -q 2>&1 | tee $(VERIFY_REPORT_DIR)/pytest.txt
	@PYTHONPATH=src $(CLI) manifest --group delivery > $(VERIFY_REPORT_DIR)/manifest.json
	@PYTHONPATH=src $(CLI) trace delivery pager preview \
		--config "service=core" \
		--config "routing_key=sev1" \
		--arg "title=Queue lag" \
		--arg "severity=critical" \
		--arg "summary=worker backlog growing" \
		> $(VERIFY_REPORT_DIR)/trace.json
	@cp README.md $(VERIFY_REPORT_DIR)/README.md
	@cp PROOF_GUIDE.md $(VERIFY_REPORT_DIR)/PROOF_GUIDE.md
	@cp TEST_GUIDE.md $(VERIFY_REPORT_DIR)/TEST_GUIDE.md
	@cp WALKTHROUGH_GUIDE.md $(VERIFY_REPORT_DIR)/WALKTHROUGH_GUIDE.md
	@cp TARGET_GUIDE.md $(VERIFY_REPORT_DIR)/TARGET_GUIDE.md
	@printf '%s\n' \
		'Verification route:' \
		'  1. Read pytest.txt for executable proof.' \
		'  2. Read manifest.json and trace.json for the saved public-surface evidence.' \
		'  3. Read TEST_GUIDE.md and PROOF_GUIDE.md for the closest claim-to-proof route.' \
		> $(VERIFY_REPORT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(VERIFY_REPORT_DIR) --output $(VERIFY_REPORT_DIR)/bundle-manifest.json
	@echo "wrote capstone verification report to $(VERIFY_REPORT_DIR)"

.PHONY: tour
tour: ## Build the learner-facing walkthrough bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR)
	@PYTHONPATH=src $(CLI) manifest --group delivery > $(TOUR_DIR)/manifest.json
	@PYTHONPATH=src $(CLI) registry --group delivery > $(TOUR_DIR)/registry.json
	@PYTHONPATH=src $(CLI) invoke delivery console deliver \
		--config "prefix=[ops]" \
		--config "uppercase_severity=true" \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%" \
		> $(TOUR_DIR)/demo.json
	@PYTHONPATH=src $(CLI) trace delivery pager preview \
		--config "service=core" \
		--config "routing_key=sev1" \
		--arg "title=Queue lag" \
		--arg "severity=critical" \
		--arg "summary=worker backlog growing" \
		> $(TOUR_DIR)/trace.json
	@find src/incident_plugins -type f | sort > $(TOUR_DIR)/runtime-files.txt
	@find tests -type f | sort > $(TOUR_DIR)/test-files.txt
	@cp README.md $(TOUR_DIR)/README.md
	@cp ARCHITECTURE.md $(TOUR_DIR)/ARCHITECTURE.md
	@cp PROOF_GUIDE.md $(TOUR_DIR)/PROOF_GUIDE.md
	@cp TOUR.md $(TOUR_DIR)/TOUR.md
	@cp WALKTHROUGH_GUIDE.md $(TOUR_DIR)/WALKTHROUGH_GUIDE.md
	@cp TARGET_GUIDE.md $(TOUR_DIR)/TARGET_GUIDE.md
	@printf '%s\n' \
		"fields=src/incident_plugins/fields.py" \
		"actions=src/incident_plugins/actions.py" \
		"cli=src/incident_plugins/cli.py" \
		"framework=src/incident_plugins/framework.py" \
		"plugins=src/incident_plugins/plugins.py" \
		"tests=tests" \
		> $(TOUR_DIR)/focus-areas.txt
	@printf '%s\n' \
		'Walkthrough route:' \
		'  1. Read manifest.json and registry.json to inspect the public runtime shape.' \
		'  2. Read demo.json for one concrete invocation.' \
		'  3. Read trace.json for configuration and action-history visibility.' \
		'  4. Read WALKTHROUGH_GUIDE.md and TOUR.md for the review order.' \
		> $(TOUR_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(TOUR_DIR) --output $(TOUR_DIR)/bundle-manifest.json
	@echo "wrote learner-facing walkthrough bundle to $(TOUR_DIR)"

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache $(TOUR_DIR) $(INSPECT_DIR) $(VERIFY_REPORT_DIR)
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
