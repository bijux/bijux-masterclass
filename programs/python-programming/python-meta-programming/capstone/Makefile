SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
DOCS_DIR := docs
DOC_FILES := \
	architecture.md:ARCHITECTURE.md \
	command-guide.md:COMMAND_GUIDE.md \
	design-boundaries.md:DESIGN_BOUNDARIES.md \
	extension-guide.md:EXTENSION_GUIDE.md \
	index.md:INDEX.md \
	package-guide.md:PACKAGE_GUIDE.md \
	proof-guide.md:PROOF_GUIDE.md \
	test-guide.md:TEST_GUIDE.md \
	tour.md:TOUR.md \
	walkthrough-guide.md:WALKTHROUGH_GUIDE.md
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/python-programming/python-meta-programming/capstone
VENV_BIN := $(VENV_DIR)/bin
VENV_PY := $(abspath $(VENV_BIN)/python)
PIP := $(VENV_PY) -m pip
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/python-programming/python-meta-programming
INSPECT_DIR ?= $(ARTIFACTS_DIR)/inspect/python-programming/python-meta-programming
VERIFY_REPORT_DIR ?= $(ARTIFACTS_DIR)/review/python-programming/python-meta-programming
CLI := $(VENV_PY) -m incident_plugins.cli
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
	@$(VENV_PY) -m pytest -q

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

.PHONY: field-ownership
field-ownership: ## Inspect one field descriptor without constructing a plugin
	@PYTHONPATH=src $(CLI) field-ownership delivery webhook endpoint

.PHONY: field-system
field-system: ## Inspect field-system powers without constructing a plugin
	@PYTHONPATH=src $(CLI) field-system delivery webhook

.PHONY: action
action: ## Render one concrete action contract from the public CLI
	@PYTHONPATH=src $(CLI) action delivery pager preview

.PHONY: bind-action
bind-action: ## Validate one action call without constructing or invoking a plugin
	@PYTHONPATH=src $(CLI) bind-action delivery console deliver \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%"

.PHONY: action-wrapper
action-wrapper: ## Audit one action wrapper chain without execution
	@PYTHONPATH=src $(CLI) action-wrapper delivery console deliver

.PHONY: check-action
check-action: ## Check supported action hints without construction or execution
	@PYTHONPATH=src $(CLI) check-action delivery console deliver \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%"

.PHONY: class-creation
class-creation: ## Inspect stored class-creation provenance without construction
	@PYTHONPATH=src $(CLI) class-creation delivery console

.PHONY: registry
registry: ## Render the delivery registry from the public CLI
	@PYTHONPATH=src $(CLI) registry --group delivery

.PHONY: governance
governance: ## Review accepted, constrained, and rejected runtime powers
	@PYTHONPATH=src $(CLI) governance

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
	@PYTHONPATH=src $(CLI) field-ownership delivery webhook endpoint \
		> $(INSPECT_DIR)/field-ownership.json
	@PYTHONPATH=src $(CLI) field-system delivery webhook \
		> $(INSPECT_DIR)/field-system.json
	@PYTHONPATH=src $(CLI) action delivery pager preview > $(INSPECT_DIR)/action.json
	@PYTHONPATH=src $(CLI) action-wrapper delivery console deliver \
		> $(INSPECT_DIR)/action-wrapper.json
	@PYTHONPATH=src $(CLI) bind-action delivery console deliver \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%" \
		> $(INSPECT_DIR)/bind-action.json
	@PYTHONPATH=src $(CLI) check-action delivery console deliver \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%" \
		> $(INSPECT_DIR)/check-action.json
	@PYTHONPATH=src $(CLI) class-creation delivery console \
		> $(INSPECT_DIR)/class-creation.json
	@PYTHONPATH=src $(CLI) governance > $(INSPECT_DIR)/governance.json
	@PYTHONPATH=src $(CLI) signatures --group delivery > $(INSPECT_DIR)/signatures.json
	@cp README.md $(INSPECT_DIR)/README.md
	@for doc in $(DOC_FILES); do \
		src=$${doc%%:*}; dest=$${doc#*:}; \
		cp $(DOCS_DIR)/$$src $(INSPECT_DIR)/$$dest; \
		cp $(DOCS_DIR)/$$src $(INSPECT_DIR)/docs/$$dest; \
	done
	@for doc in $(INSPECT_DIR)/*.md; do \
		[ "$$doc" = "$(INSPECT_DIR)/README.md" ] && continue; \
		perl -0pi -e "s#\\]\\(\\.\\./capstone/index\\.md\\)#](README.md)#g" "$$doc"; \
	done
	@for doc in $(INSPECT_DIR)/docs/*.md; do \
		perl -0pi -e "s#\\]\\(\\.\\./capstone/index\\.md\\)#](../README.md)#g" "$$doc"; \
	done
	@printf '%s\n' \
		'Inspection route:' \
		'  1. Read manifest.json for group-level field and action metadata.' \
		'  2. Read registry.json, plugin.json, field.json, field-ownership.json, field-system.json, action.json, signatures.json, action-wrapper.json, bind-action.json, check-action.json, and class-creation.json for concrete contracts, descriptor-system boundaries, callable policy, and class-creation provenance.' \
		'  3. Read governance.json to review which runtime powers the application accepts, constrains, and rejects.' \
		'  4. Read COMMAND_GUIDE.md and PROOF_GUIDE.md for the next review route.' \
		'  5. Read PACKAGE_GUIDE.md when you need to connect the outputs back to source ownership and proof.' \
		> $(INSPECT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(INSPECT_DIR) --output $(INSPECT_DIR)/bundle-manifest.json
	@echo "wrote learner-facing inspection bundle to $(INSPECT_DIR)"

.PHONY: proof
proof: inspect tour verify-report ## Run the full public proof route

.PHONY: verify-report
verify-report: ## Build the structured capstone verification report
	@rm -rf $(VERIFY_REPORT_DIR)
	@mkdir -p $(VERIFY_REPORT_DIR) $(VERIFY_REPORT_DIR)/docs
	@$(VENV_PY) -m pytest -q 2>&1 | tee $(VERIFY_REPORT_DIR)/pytest.txt
	@PYTHONPATH=src $(CLI) manifest --group delivery > $(VERIFY_REPORT_DIR)/manifest.json
	@PYTHONPATH=src $(CLI) plugin delivery webhook > $(VERIFY_REPORT_DIR)/plugin.json
	@PYTHONPATH=src $(CLI) field-ownership delivery webhook endpoint \
		> $(VERIFY_REPORT_DIR)/field-ownership.json
	@PYTHONPATH=src $(CLI) field-system delivery webhook \
		> $(VERIFY_REPORT_DIR)/field-system.json
	@PYTHONPATH=src $(CLI) signatures --group delivery > $(VERIFY_REPORT_DIR)/signatures.json
	@PYTHONPATH=src $(CLI) action-wrapper delivery console deliver \
		> $(VERIFY_REPORT_DIR)/action-wrapper.json
	@PYTHONPATH=src $(CLI) bind-action delivery console deliver \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%" \
		> $(VERIFY_REPORT_DIR)/bind-action.json
	@PYTHONPATH=src $(CLI) check-action delivery console deliver \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%" \
		> $(VERIFY_REPORT_DIR)/check-action.json
	@PYTHONPATH=src $(CLI) class-creation delivery console \
		> $(VERIFY_REPORT_DIR)/class-creation.json
	@PYTHONPATH=src $(CLI) governance > $(VERIFY_REPORT_DIR)/governance.json
	@PYTHONPATH=src $(CLI) trace delivery pager preview \
		--config "service=core" \
		--config "routing_key=sev1" \
		--arg "title=Queue lag" \
		--arg "severity=critical" \
		--arg "summary=worker backlog growing" \
		> $(VERIFY_REPORT_DIR)/trace.json
	@cp README.md $(VERIFY_REPORT_DIR)/README.md
	@for doc in $(DOC_FILES); do \
		src=$${doc%%:*}; dest=$${doc#*:}; \
		cp $(DOCS_DIR)/$$src $(VERIFY_REPORT_DIR)/$$dest; \
		cp $(DOCS_DIR)/$$src $(VERIFY_REPORT_DIR)/docs/$$dest; \
	done
	@for doc in $(VERIFY_REPORT_DIR)/*.md; do \
		[ "$$doc" = "$(VERIFY_REPORT_DIR)/README.md" ] && continue; \
		perl -0pi -e "s#\\]\\(\\.\\./capstone/index\\.md\\)#](README.md)#g" "$$doc"; \
	done
	@for doc in $(VERIFY_REPORT_DIR)/docs/*.md; do \
		perl -0pi -e "s#\\]\\(\\.\\./capstone/index\\.md\\)#](../README.md)#g" "$$doc"; \
	done
	@printf '%s\n' \
		'Verification route:' \
		'  1. Read pytest.txt for executable proof.' \
		'  2. Read manifest.json, plugin.json, field-ownership.json, field-system.json, signatures.json, action-wrapper.json, bind-action.json, check-action.json, class-creation.json, governance.json, and trace.json to compare runtime ownership and review decisions with execution.' \
		'  3. Read TEST_GUIDE.md and PROOF_GUIDE.md for the closest claim-to-proof route.' \
		'  4. Read PACKAGE_GUIDE.md when you need to connect a code change back to the saved proof.' \
		> $(VERIFY_REPORT_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(VERIFY_REPORT_DIR) --output $(VERIFY_REPORT_DIR)/bundle-manifest.json
	@echo "wrote capstone verification report to $(VERIFY_REPORT_DIR)"

.PHONY: tour
tour: ## Build the learner-facing walkthrough bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR) $(TOUR_DIR)/docs
	@PYTHONPATH=src $(CLI) manifest --group delivery > $(TOUR_DIR)/manifest.json
	@PYTHONPATH=src $(CLI) registry --group delivery > $(TOUR_DIR)/registry.json
	@PYTHONPATH=src $(CLI) plugin delivery webhook > $(TOUR_DIR)/plugin.json
	@PYTHONPATH=src $(CLI) field-ownership delivery webhook endpoint \
		> $(TOUR_DIR)/field-ownership.json
	@PYTHONPATH=src $(CLI) field-system delivery webhook \
		> $(TOUR_DIR)/field-system.json
	@PYTHONPATH=src $(CLI) signatures --group delivery > $(TOUR_DIR)/signatures.json
	@PYTHONPATH=src $(CLI) action-wrapper delivery console deliver \
		> $(TOUR_DIR)/action-wrapper.json
	@PYTHONPATH=src $(CLI) bind-action delivery console deliver \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%" \
		> $(TOUR_DIR)/bind-action.json
	@PYTHONPATH=src $(CLI) check-action delivery console deliver \
		--arg "title=CPU high" \
		--arg "severity=warning" \
		--arg "summary=node-1 crossed 90%" \
		> $(TOUR_DIR)/check-action.json
	@PYTHONPATH=src $(CLI) class-creation delivery console \
		> $(TOUR_DIR)/class-creation.json
	@PYTHONPATH=src $(CLI) governance > $(TOUR_DIR)/governance.json
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
	@for doc in $(DOC_FILES); do \
		src=$${doc%%:*}; dest=$${doc#*:}; \
		cp $(DOCS_DIR)/$$src $(TOUR_DIR)/$$dest; \
		cp $(DOCS_DIR)/$$src $(TOUR_DIR)/docs/$$dest; \
	done
	@for doc in $(TOUR_DIR)/*.md; do \
		[ "$$doc" = "$(TOUR_DIR)/README.md" ] && continue; \
		perl -0pi -e "s#\\]\\(\\.\\./capstone/index\\.md\\)#](README.md)#g" "$$doc"; \
	done
	@for doc in $(TOUR_DIR)/docs/*.md; do \
		perl -0pi -e "s#\\]\\(\\.\\./capstone/index\\.md\\)#](../README.md)#g" "$$doc"; \
	done
	@printf '%s\n' \
		"fields=src/incident_plugins/fields.py" \
		"actions=src/incident_plugins/actions.py" \
		"cli=src/incident_plugins/cli.py" \
		"framework=src/incident_plugins/framework.py" \
		"governance=src/incident_plugins/governance.py" \
		"plugins=src/incident_plugins/plugins.py" \
		"tests=tests" \
		> $(TOUR_DIR)/focus-areas.txt
	@printf '%s\n' \
		'Walkthrough route:' \
		'  1. Read manifest.json, registry.json, plugin.json, and signatures.json to inspect the public runtime shape.' \
		'  2. Read field-ownership.json, field-system.json, action-wrapper.json, bind-action.json, check-action.json, and class-creation.json for descriptor-system ownership, callable ownership, partial contracts, and class-creation provenance without execution.' \
		'  3. Read governance.json for the accepted, constrained, and rejected runtime powers.' \
		'  4. Read demo.json and trace.json for deliberate invocation, configuration, and successful action-history visibility.' \
		'  5. Read WALKTHROUGH_GUIDE.md, COMMAND_GUIDE.md, and TOUR.md for the review order.' \
		'  6. Read PACKAGE_GUIDE.md and PROOF_GUIDE.md when you need to connect the tour back to local guides or source ownership.' \
		> $(TOUR_DIR)/route.txt
	@$(WRITE_BUNDLE_MANIFEST) --bundle-dir $(TOUR_DIR) --output $(TOUR_DIR)/bundle-manifest.json
	@echo "wrote learner-facing walkthrough bundle to $(TOUR_DIR)"

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache $(TOUR_DIR) $(INSPECT_DIR) $(VERIFY_REPORT_DIR)
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
