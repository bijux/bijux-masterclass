# Makefile

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c
.ONESHELL:
.DEFAULT_GOAL := help

# ---- knobs ----
SNAKEMAKE ?= snakemake
PROFILE   ?= profiles/local
CORES     ?= all
CONFIG    ?= config/config.yaml

PYTHON    ?= python3
PYTEST    ?= pytest
RUFF      ?= ruff
DOT       ?= dot

# ---- artifacts sandbox (no root pollution) ----
ARTIFACTS_DIR ?= ../../../../artifacts
LINT_DIR      ?= $(ARTIFACTS_DIR)/lint/reproducible-research/deep-dive-snakemake
TEST_DIR      ?= $(ARTIFACTS_DIR)/test/reproducible-research/deep-dive-snakemake
WF_DIR        ?= $(ARTIFACTS_DIR)/workflow/reproducible-research/deep-dive-snakemake
TMP_DIR       ?= $(ARTIFACTS_DIR)/tmp/reproducible-research/deep-dive-snakemake
WALKTHROUGH_DIR ?= $(ARTIFACTS_DIR)/walkthrough/reproducible-research/deep-dive-snakemake
TOUR_DIR      ?= $(ARTIFACTS_DIR)/tour/reproducible-research/deep-dive-snakemake

# ---- workflow outputs ----
PUBLISH_DIR ?= publish/v1
MANIFEST    ?= $(PUBLISH_DIR)/manifest.json

# ---- absolute paths ----
ARTIFACTS_DIR_ABS := $(abspath $(ARTIFACTS_DIR))
LINT_DIR_ABS      := $(abspath $(LINT_DIR))
TEST_DIR_ABS      := $(abspath $(TEST_DIR))
WF_DIR_ABS        := $(abspath $(WF_DIR))
TMP_DIR_ABS       := $(abspath $(TMP_DIR))
WALKTHROUGH_DIR_ABS := $(abspath $(WALKTHROUGH_DIR))
TOUR_DIR_ABS      := $(abspath $(TOUR_DIR))
MANIFEST_ABS      := $(abspath $(MANIFEST))
PUBLISH_DIR_ABS   := $(abspath $(PUBLISH_DIR))

# ---- phony ----
.PHONY: help info \
	clean purge-dsstore \
	fmt fmt-check lint test \
	wf-lint wf-dryrun wf-run dag rulegraph \
	validate-config verify-artifacts walkthrough tour \
	check ci validate verify confirm selftest \
	docker-build docker-run

help: ## Show available targets
	@awk 'BEGIN {FS=":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

info: ## Print tool versions and key settings
	@echo "SNAKEMAKE = $(SNAKEMAKE)"
	@echo "PROFILE   = $(PROFILE)"
	@echo "CORES     = $(CORES)"
	@echo "CONFIG    = $(CONFIG)"
	@echo "ARTIFACTS = $(ARTIFACTS_DIR_ABS)"
	@echo
	@command -v $(PYTHON) >/dev/null && $(PYTHON) --version || echo "python missing"
	@command -v $(SNAKEMAKE) >/dev/null && $(SNAKEMAKE) --version || echo "snakemake missing"
	@command -v $(RUFF) >/dev/null && $(RUFF) --version || echo "ruff missing"
	@command -v $(PYTEST) >/dev/null && $(PYTEST) --version || echo "pytest missing"

clean: ## Remove build/run artifacts (keeps git-tracked files)
	rm -rf .snakemake publish results logs benchmarks .hypothesis .benchmarks dag.png rulegraph.png .pytest_cache
	rm -rf "$(ARTIFACTS_DIR_ABS)" .ruff_cache artifacts
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@true

purge-dsstore: ## Delete .DS_Store everywhere (also add to .gitignore)
	find . -name ".DS_Store" -type f -delete

fmt: ## Auto-format with ruff (writes changes)
	@command -v $(RUFF) >/dev/null || { echo "✘ ruff not found"; exit 1; }
	$(RUFF) format .
	$(RUFF) check --fix .

fmt-check: ## Formatting gate (fails if reformat needed)
	@command -v $(RUFF) >/dev/null || { echo "✘ ruff not found"; exit 1; }
	$(RUFF) format --check .

lint: ## Static checks (does NOT enforce formatting)
	@mkdir -p "$(LINT_DIR_ABS)"
	$(PYTHON) -m compileall -q src tests
	@command -v $(RUFF) >/dev/null || { echo "✘ ruff not found"; exit 1; }
	$(RUFF) check .

test: ## Run unit tests
	@mkdir -p "$(TEST_DIR_ABS)"
	@command -v $(PYTEST) >/dev/null || { echo "✘ pytest not found"; exit 1; }
	$(PYTEST) -q

wf-lint: ## Snakemake lint
	@command -v $(SNAKEMAKE) >/dev/null || { echo "✘ snakemake not found"; exit 1; }
	$(SNAKEMAKE) --lint

wf-dryrun: ## Snakemake dry-run with printed commands
	@command -v $(SNAKEMAKE) >/dev/null || { echo "✘ snakemake not found"; exit 1; }
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) -n -p

wf-run: ## Run workflow
	@command -v $(SNAKEMAKE) >/dev/null || { echo "✘ snakemake not found"; exit 1; }
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG)

dag: ## Render DAG to dag.png (requires graphviz dot)
	@command -v $(DOT) >/dev/null || { echo "✘ dot (graphviz) not found"; exit 1; }
	$(SNAKEMAKE) --profile $(PROFILE) --configfile $(CONFIG) --dag | $(DOT) -Tpng > dag.png
	@echo "✔ Wrote dag.png"

rulegraph: ## Render rulegraph to rulegraph.png (requires graphviz dot)
	@command -v $(DOT) >/dev/null || { echo "✘ dot (graphviz) not found"; exit 1; }
	$(SNAKEMAKE) --profile $(PROFILE) --configfile $(CONFIG) --rulegraph | $(DOT) -Tpng > rulegraph.png
	@echo "✔ Wrote rulegraph.png"

validate-config: ## Validate config/config.yaml against config/schema.yaml (best-effort)
	@mkdir -p "$(LINT_DIR_ABS)" "$(TMP_DIR_ABS)"
	@command -v $(PYTHON) >/dev/null || { echo "✘ python missing"; exit 1; }
	@$(PYTHON) scripts/validate_config.py --config config/config.yaml --schema config/schema.yaml \
		2>&1 | tee "$(LINT_DIR_ABS)/config_schema.log"

verify-artifacts: ## Verify publish artifacts exist and are parseable (best-effort)
	@mkdir -p "$(LINT_DIR_ABS)" "$(TMP_DIR_ABS)"
	@command -v $(PYTHON) >/dev/null || { echo "✘ python missing"; exit 1; }
	@$(PYTHON) scripts/verify_publish.py --publish "$(PUBLISH_DIR_ABS)" \
		2>&1 | tee "$(LINT_DIR_ABS)/verify_artifacts.log"

# ---- high-level flows ----
check: lint test wf-lint wf-dryrun validate-config ## Fast pre-flight (no workflow execution); NOT a formatting gate
ci: fmt-check lint test wf-lint wf-dryrun validate-config ## Strict gate (includes formatting)

validate: check ## Alias
verify: wf-run verify-artifacts ## Execute workflow then verify outputs
confirm: clean purge-dsstore ci verify ## Clean-room confirmation (strict)
selftest: ## Prove deterministic publish behavior across core counts
	@/bin/bash tests/selftest.sh

walkthrough: clean validate-config wf-lint ## Build a light learner-facing bundle without executing the workflow
	@mkdir -p "$(WALKTHROUGH_DIR_ABS)"
	$(SNAKEMAKE) --list-rules > "$(WALKTHROUGH_DIR_ABS)/list-rules.txt"
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) -n -p > "$(WALKTHROUGH_DIR_ABS)/dryrun.txt"
	cp README.md "$(WALKTHROUGH_DIR_ABS)/README.md"
	cp FILE_API.md "$(WALKTHROUGH_DIR_ABS)/FILE_API.md"
	cp TOUR.md "$(WALKTHROUGH_DIR_ABS)/TOUR.md"
	@printf '%s\n' \
		'1. Read README.md to understand the repository contract.' \
		'2. Read list-rules.txt to see the visible workflow surface.' \
		'3. Read dryrun.txt to inspect the planned jobs without execution.' \
		'4. Read FILE_API.md to see which outputs are public contracts.' \
		'5. Run make selftest when you want deterministic execution proof.' \
		'6. Run make tour when you want executed proof artifacts.' > "$(WALKTHROUGH_DIR_ABS)/route.txt"
	@echo "✔ wrote workflow walkthrough to $(WALKTHROUGH_DIR_ABS)"

tour: clean validate-config wf-lint ## Build a learner-facing workflow proof bundle
	@mkdir -p "$(TOUR_DIR_ABS)"
	$(SNAKEMAKE) --list-rules > "$(TOUR_DIR_ABS)/list-rules.txt"
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) -n -p > "$(TOUR_DIR_ABS)/dryrun.txt"
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) 2>&1 | tee "$(TOUR_DIR_ABS)/run.txt"
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) --summary > "$(TOUR_DIR_ABS)/summary.txt"
	cp FILE_API.md "$(TOUR_DIR_ABS)/FILE_API.md"
	cp "$(MANIFEST_ABS)" "$(TOUR_DIR_ABS)/manifest.json"
	cp "$(PUBLISH_DIR_ABS)/provenance.json" "$(TOUR_DIR_ABS)/provenance.json"
	cp README.md "$(TOUR_DIR_ABS)/README.md"
	cp TOUR.md "$(TOUR_DIR_ABS)/TOUR.md"
	@echo "✔ wrote workflow tour to $(TOUR_DIR_ABS)"

# ---- docker ----
docker-build: ## Build docker image
	docker build -t snakemake-capstone:latest .

docker-run: ## Run workflow inside docker (bind-mount repo)
	docker run --rm -it \
		-v "$$(pwd)":/work \
		-w /work \
		snakemake-capstone:latest \
		snakemake --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG)
