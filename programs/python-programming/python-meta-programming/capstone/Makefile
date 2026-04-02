SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/python-programming/python-meta-programming

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone test suite
	@$(PYTHON) -m pytest

.PHONY: confirm
confirm: test ## Run the executable validation suite

.PHONY: tour
tour: confirm ## Build the learner-facing proof bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR)
	@$(PYTHON) -m pytest -q 2>&1 | tee $(TOUR_DIR)/pytest.txt
	@find src/incident_plugins -type f | sort > $(TOUR_DIR)/runtime-files.txt
	@find tests -type f | sort > $(TOUR_DIR)/test-files.txt
	@cp README.md $(TOUR_DIR)/README.md
	@cp TOUR.md $(TOUR_DIR)/TOUR.md
	@printf '%s\n' \
		"fields=src/incident_plugins/fields.py" \
		"actions=src/incident_plugins/actions.py" \
		"framework=src/incident_plugins/framework.py" \
		"plugins=src/incident_plugins/plugins.py" \
		"tests=tests" \
		> $(TOUR_DIR)/focus-areas.txt
	@echo "✔ wrote learner-facing tour to $(TOUR_DIR)"

.PHONY: clean
clean: ## Remove generated caches
	@rm -rf .pytest_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
