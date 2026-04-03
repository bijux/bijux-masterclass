SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
DOCS_DIR := docs
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

.PHONY: plugin
plugin: ## Render one concrete plugin contract from the public CLI
	@PYTHONPATH=src $(CLI) plugin delivery webhook

.PHONY: field
field: ## Render one concrete field contract from the public CLI
	@PYTHONPATH=src $(CLI) field delivery webhook endpoint

.PHONY: action
action: ## Render one concrete action contract from the public CLI
	@PYTHONPATH=src $(CLI) action delivery pager preview

.PHONY: registry
registry: ## Render the delivery registry from the public CLI
	@PYTHONPATH=src $(CLI) registry --group delivery

.PHONY: signatures
signatures: ## Render generated constructor and action signatures from the public CLI
	@PYTHONPATH=src $(CLI) signatures --group delivery

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
	@mkdir -p $(INSPECT_DIR) $(INSPECT_DIR)/docs
	@PYTHONPATH=src $(CLI) manifest --group delivery > $(INSPECT_DIR)/manifest.json
	@PYTHONPATH=src $(CLI) registry --group delivery > $(INSPECT_DIR)/registry.json
	@PYTHONPATH=src $(CLI) plugin delivery webhook > $(INSPECT_DIR)/plugin.json
	@PYTHONPATH=src $(CLI) field delivery webhook endpoint > $(INSPECT_DIR)/field.json
	@PYTHONPATH=src $(CLI) action delivery pager preview > $(INSPECT_DIR)/action.json
	@PYTHONPATH=src $(CLI) signatures --group delivery > $(INSPECT_DIR)/signatures.json
	@cp README.md $(INSPECT_DIR)/README.md
	@cp $(DOCS_DIR)/GUIDE_INDEX.md $(INSPECT_DIR)/GUIDE_INDEX.md
	@cp $(DOCS_DIR)/BUNDLE_GUIDE.md $(INSPECT_DIR)/BUNDLE_GUIDE.md
	@cp $(DOCS_DIR)/COMMAND_GUIDE.md $(INSPECT_DIR)/COMMAND_GUIDE.md
	@cp $(DOCS_DIR)/DESIGN_BOUNDARIES.md $(INSPECT_DIR)/DESIGN_BOUNDARIES.md
	@cp $(DOCS_DIR)/FIRST_SESSION_GUIDE.md $(INSPECT_DIR)/FIRST_SESSION_GUIDE.md
	@cp $(DOCS_DIR)/PACKAGE_GUIDE.md $(INSPECT_DIR)/PACKAGE_GUIDE.md
	@cp $(DOCS_DIR)/PUBLIC_SURFACE_MAP.md $(INSPECT_DIR)/PUBLIC_SURFACE_MAP.md
	@cp $(DOCS_DIR)/REVIEW_ROUTE_MAP.md $(INSPECT_DIR)/REVIEW_ROUTE_MAP.md
	@cp $(DOCS_DIR)/SOURCE_TO_PROOF_MAP.md $(INSPECT_DIR)/SOURCE_TO_PROOF_MAP.md
	@cp $(DOCS_DIR)/TARGET_GUIDE.md $(INSPECT_DIR)/TARGET_GUIDE.md
	@cp $(DOCS_DIR)/INSPECTION_GUIDE.md $(INSPECT_DIR)/INSPECTION_GUIDE.md
	@cp $(DOCS_DIR)/PROOF_GUIDE.md $(INSPECT_DIR)/PROOF_GUIDE.md
	@cp $(DOCS_DIR)/*.md $(INSPECT_DIR)/
	@cp $(DOCS_DIR)/*.md $(INSPECT_DIR)/docs/
	@for doc in $(INSPECT_DIR)/*.md; do \
		[ "$$doc" = "$(INSPECT_DIR)/README.md" ] && continue; \
		python3 -c "from pathlib import Path; path = Path('$$doc'); path.write_text(path.read_text(encoding='utf-8').replace('](../README.md)', '](README.md)'), encoding='utf-8')"; \
	done
	@printf '%s\n' \
		'Inspection route:' \
		'  1. Read manifest.json for group-level field and action metadata.' \
		'  2. Read registry.json, plugin.json, field.json, action.json, and signatures.json for registered plugins, one concrete plugin, one concrete field, one concrete action, and generated callable shapes.' \
		'  3. Read INSPECTION_GUIDE.md, PUBLIC_SURFACE_MAP.md, and TARGET_GUIDE.md for the next review route.' \
		'  4. Read PACKAGE_GUIDE.md and SOURCE_TO_PROOF_MAP.md when you need to connect the outputs back to source ownership and proof.' \
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
	@PYTHONPATH=src $(CLI) plugin delivery webhook > $(VERIFY_REPORT_DIR)/plugin.json
	@PYTHONPATH=src $(CLI) signatures --group delivery > $(VERIFY_REPORT_DIR)/signatures.json
	@PYTHONPATH=src $(CLI) trace delivery pager preview \
		--config "service=core" \
		--config "routing_key=sev1" \
		--arg "title=Queue lag" \
		--arg "severity=critical" \
		--arg "summary=worker backlog growing" \
		> $(VERIFY_REPORT_DIR)/trace.json
	@cp README.md $(VERIFY_REPORT_DIR)/README.md
	@cp $(DOCS_DIR)/GUIDE_INDEX.md $(VERIFY_REPORT_DIR)/GUIDE_INDEX.md
	@cp $(DOCS_DIR)/BUNDLE_GUIDE.md $(VERIFY_REPORT_DIR)/BUNDLE_GUIDE.md
	@cp $(DOCS_DIR)/COMMAND_GUIDE.md $(VERIFY_REPORT_DIR)/COMMAND_GUIDE.md
	@cp $(DOCS_DIR)/DESIGN_BOUNDARIES.md $(VERIFY_REPORT_DIR)/DESIGN_BOUNDARIES.md
	@cp $(DOCS_DIR)/PROOF_GUIDE.md $(VERIFY_REPORT_DIR)/PROOF_GUIDE.md
	@cp $(DOCS_DIR)/REVIEW_ROUTE_MAP.md $(VERIFY_REPORT_DIR)/REVIEW_ROUTE_MAP.md
	@cp $(DOCS_DIR)/SOURCE_TO_PROOF_MAP.md $(VERIFY_REPORT_DIR)/SOURCE_TO_PROOF_MAP.md
	@cp $(DOCS_DIR)/TEST_GUIDE.md $(VERIFY_REPORT_DIR)/TEST_GUIDE.md
	@cp $(DOCS_DIR)/TEST_READING_MAP.md $(VERIFY_REPORT_DIR)/TEST_READING_MAP.md
	@cp $(DOCS_DIR)/WALKTHROUGH_GUIDE.md $(VERIFY_REPORT_DIR)/WALKTHROUGH_GUIDE.md
	@cp $(DOCS_DIR)/TARGET_GUIDE.md $(VERIFY_REPORT_DIR)/TARGET_GUIDE.md
	@printf '%s\n' \
		'Verification route:' \
		'  1. Read pytest.txt for executable proof.' \
		'  2. Read manifest.json, plugin.json, signatures.json, and trace.json for the saved public-surface evidence.' \
		'  3. Read TEST_GUIDE.md, TEST_READING_MAP.md, and PROOF_GUIDE.md for the closest claim-to-proof route.' \
		'  4. Read SOURCE_TO_PROOF_MAP.md and REVIEW_ROUTE_MAP.md when you need to connect a code change back to the saved proof.' \
		> $(VERIFY_REPORT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(VERIFY_REPORT_DIR) --output $(VERIFY_REPORT_DIR)/bundle-manifest.json
	@echo "wrote capstone verification report to $(VERIFY_REPORT_DIR)"

.PHONY: tour
tour: ## Build the learner-facing walkthrough bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR)
	@PYTHONPATH=src $(CLI) manifest --group delivery > $(TOUR_DIR)/manifest.json
	@PYTHONPATH=src $(CLI) registry --group delivery > $(TOUR_DIR)/registry.json
	@PYTHONPATH=src $(CLI) plugin delivery webhook > $(TOUR_DIR)/plugin.json
	@PYTHONPATH=src $(CLI) signatures --group delivery > $(TOUR_DIR)/signatures.json
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
	@cp $(DOCS_DIR)/FIRST_SESSION_GUIDE.md $(TOUR_DIR)/FIRST_SESSION_GUIDE.md
	@cp $(DOCS_DIR)/GUIDE_INDEX.md $(TOUR_DIR)/GUIDE_INDEX.md
	@cp $(DOCS_DIR)/BUNDLE_GUIDE.md $(TOUR_DIR)/BUNDLE_GUIDE.md
	@cp $(DOCS_DIR)/COMMAND_GUIDE.md $(TOUR_DIR)/COMMAND_GUIDE.md
	@cp $(DOCS_DIR)/ARCHITECTURE.md $(TOUR_DIR)/ARCHITECTURE.md
	@cp $(DOCS_DIR)/DESIGN_BOUNDARIES.md $(TOUR_DIR)/DESIGN_BOUNDARIES.md
	@cp $(DOCS_DIR)/PROOF_GUIDE.md $(TOUR_DIR)/PROOF_GUIDE.md
	@cp $(DOCS_DIR)/PUBLIC_SURFACE_MAP.md $(TOUR_DIR)/PUBLIC_SURFACE_MAP.md
	@cp $(DOCS_DIR)/REVIEW_ROUTE_MAP.md $(TOUR_DIR)/REVIEW_ROUTE_MAP.md
	@cp $(DOCS_DIR)/SOURCE_TO_PROOF_MAP.md $(TOUR_DIR)/SOURCE_TO_PROOF_MAP.md
	@cp $(DOCS_DIR)/TOUR.md $(TOUR_DIR)/TOUR.md
	@cp $(DOCS_DIR)/WALKTHROUGH_GUIDE.md $(TOUR_DIR)/WALKTHROUGH_GUIDE.md
	@cp $(DOCS_DIR)/TARGET_GUIDE.md $(TOUR_DIR)/TARGET_GUIDE.md
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
		'  1. Read manifest.json, registry.json, plugin.json, and signatures.json to inspect the public runtime shape.' \
		'  2. Read demo.json for one concrete invocation.' \
		'  3. Read trace.json for configuration and action-history visibility.' \
		'  4. Read WALKTHROUGH_GUIDE.md, PUBLIC_SURFACE_MAP.md, and TOUR.md for the review order.' \
		'  5. Read REVIEW_ROUTE_MAP.md and SOURCE_TO_PROOF_MAP.md when you need to connect the tour back to local guides or source ownership.' \
		> $(TOUR_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(TOUR_DIR) --output $(TOUR_DIR)/bundle-manifest.json
	@echo "wrote learner-facing walkthrough bundle to $(TOUR_DIR)"

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache $(TOUR_DIR) $(INSPECT_DIR) $(VERIFY_REPORT_DIR)
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
