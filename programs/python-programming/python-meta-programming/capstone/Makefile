SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/python-programming/python-meta-programming
CLI := $(PYTHON) -m incident_plugins.cli

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone test suite
	@$(PYTHON) -m pytest

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

.PHONY: proof
proof: confirm manifest registry demo trace ## Run the full public proof route

.PHONY: tour
tour: proof ## Build the learner-facing proof bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR)
	@$(PYTHON) -m pytest -q 2>&1 | tee $(TOUR_DIR)/pytest.txt
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
	@printf '%s\n' \
		"fields=src/incident_plugins/fields.py" \
		"actions=src/incident_plugins/actions.py" \
		"cli=src/incident_plugins/cli.py" \
		"framework=src/incident_plugins/framework.py" \
		"plugins=src/incident_plugins/plugins.py" \
		"tests=tests" \
		> $(TOUR_DIR)/focus-areas.txt
	@echo "✔ wrote learner-facing tour to $(TOUR_DIR)"

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
