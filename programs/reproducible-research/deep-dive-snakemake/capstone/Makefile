# Makefile

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c
.ONESHELL:
.DEFAULT_GOAL := help

# ---- knobs ----
PROFILE   ?= profiles/local
CORES     ?= all
CONFIG    ?= config/config.yaml

SYSTEM_PYTHON ?= $(if $(shell command -v python3.11 2>/dev/null),python3.11,python3)
DOT       ?= dot

# ---- artifacts sandbox (no root pollution) ----
ARTIFACTS_DIR ?= ../../../../artifacts
LINT_DIR      ?= $(ARTIFACTS_DIR)/lint/reproducible-research/deep-dive-snakemake
TEST_DIR      ?= $(ARTIFACTS_DIR)/test/reproducible-research/deep-dive-snakemake
WF_DIR        ?= $(ARTIFACTS_DIR)/workflow/reproducible-research/deep-dive-snakemake
TMP_DIR       ?= $(ARTIFACTS_DIR)/tmp/reproducible-research/deep-dive-snakemake
WALKTHROUGH_DIR ?= $(ARTIFACTS_DIR)/walkthrough/reproducible-research/deep-dive-snakemake
TOUR_DIR      ?= $(ARTIFACTS_DIR)/tour/reproducible-research/deep-dive-snakemake
VERIFY_REPORT_DIR ?= $(ARTIFACTS_DIR)/proof/reproducible-research/deep-dive-snakemake/verify
PROFILE_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-snakemake/profile

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
TOOLS_VENV_DIR ?= $(ARTIFACTS_DIR)/venv/reproducible-research/deep-dive-snakemake/capstone
TOOLS_VENV_DIR_ABS := $(abspath $(TOOLS_VENV_DIR))
TOOLS_BIN := $(TOOLS_VENV_DIR_ABS)/bin
TOOLS_PY := $(TOOLS_BIN)/python
TOOLS_PIP := $(TOOLS_PY) -m pip
REPO_ROOT := $(abspath ../../../..)
SOURCE_BUNDLE_DIR ?= $(ARTIFACTS_DIR)/dist/reproducible-research/deep-dive-snakemake
SOURCE_BUNDLE_PATH ?= $(SOURCE_BUNDLE_DIR)/deep-dive-snakemake-capstone.tar.gz

SNAKEMAKE ?= $(if $(wildcard $(TOOLS_BIN)/snakemake),$(TOOLS_BIN)/snakemake,snakemake)
PYTHON ?= $(if $(wildcard $(TOOLS_PY)),$(TOOLS_PY),$(SYSTEM_PYTHON))
PYTEST ?= $(if $(wildcard $(TOOLS_BIN)/pytest),$(TOOLS_BIN)/pytest,pytest)
RUFF ?= $(if $(wildcard $(TOOLS_BIN)/ruff),$(TOOLS_BIN)/ruff,ruff)

# ---- phony ----
.PHONY: help info bootstrap bootstrap-confirm \
	clean purge-dsstore source-baseline-clean source-baseline-check source-bundle \
	fmt fmt-check lint test \
	wf-lint wf-dryrun wf-run dag rulegraph \
	validate-config verify-artifacts walkthrough tour \
	publish-summary profile-summary config-summary results-summary evidence-summary \
	verify-report profile-audit \
	check ci validate verify confirm selftest proof \
	docker-build docker-run

help: ## Show available targets
	@awk 'BEGIN {FS=":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

bootstrap: ## Create the supported local toolchain and print the resolved versions
	@$(SYSTEM_PYTHON) -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' || { echo "✘ bootstrap requires Python 3.11+ via SYSTEM_PYTHON=$(SYSTEM_PYTHON)"; exit 1; }
	@rm -rf "$(TOOLS_VENV_DIR_ABS)"
	@$(SYSTEM_PYTHON) -m venv "$(TOOLS_VENV_DIR_ABS)"
	@$(TOOLS_PIP) install -U pip
	@$(TOOLS_PIP) install "snakemake>=8" pytest ruff pyyaml jsonschema
	@$(MAKE) info SNAKEMAKE="$(TOOLS_BIN)/snakemake" PYTHON="$(TOOLS_PY)" PYTEST="$(TOOLS_BIN)/pytest" RUFF="$(TOOLS_BIN)/ruff"

bootstrap-confirm: bootstrap ## Create the supported toolchain and run clean-room confirmation
	@$(MAKE) confirm SNAKEMAKE="$(TOOLS_BIN)/snakemake" PYTHON="$(TOOLS_PY)" PYTEST="$(TOOLS_BIN)/pytest" RUFF="$(TOOLS_BIN)/ruff"

info: ## Print tool versions and key settings
	@echo "SNAKEMAKE = $(SNAKEMAKE)"
	@echo "PROFILE   = $(PROFILE)"
	@echo "CORES     = $(CORES)"
	@echo "CONFIG    = $(CONFIG)"
	@echo "ARTIFACTS = $(ARTIFACTS_DIR_ABS)"
	@echo "TOOLS_VENV = $(TOOLS_VENV_DIR_ABS)"
	@echo
	@command -v $(PYTHON) >/dev/null && $(PYTHON) --version || echo "python missing"
	@command -v $(SNAKEMAKE) >/dev/null && $(SNAKEMAKE) --version || echo "snakemake missing"
	@command -v $(RUFF) >/dev/null && $(RUFF) --version || echo "ruff missing"
	@command -v $(PYTEST) >/dev/null && $(PYTEST) --version || echo "pytest missing"

clean: ## Remove build/run artifacts (keeps git-tracked files)
	rm -rf .snakemake publish results logs benchmarks .hypothesis .benchmarks dag.png rulegraph.png .pytest_cache
	rm -rf "$(LINT_DIR_ABS)" "$(TEST_DIR_ABS)" "$(WF_DIR_ABS)" "$(TMP_DIR_ABS)" "$(WALKTHROUGH_DIR_ABS)" "$(TOUR_DIR_ABS)" .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@true

source-baseline-clean: clean ## Remove local-only state that must not ship in a source bundle
	@true

source-baseline-check: ## Fail if local-only state would contaminate a source bundle
	@paths="$$(find . \
		\( -path './.snakemake' -o -path './publish' -o -path './results' -o -path './logs' \
		   -o -path './benchmarks' -o -path './.pytest_cache' -o -path './.ruff_cache' \
		   -o -name '__pycache__' -o -name 'dag.png' -o -name 'rulegraph.png' \) \
		-prune -print | sort)"; \
	if [ -n "$$paths" ]; then \
		printf '%s\n' 'FAIL: source bundle would include local-only state:' "$$paths" >&2; \
		exit 1; \
	fi; \
	printf '%s\n' 'PASS: source baseline contains no local-only state'

source-bundle: source-baseline-check ## Build a tracked-source bundle for release or learner download
	@mkdir -p "$(SOURCE_BUNDLE_DIR)"
	@$(PYTHON) "$(REPO_ROOT)/scripts/build_clean_source_bundle.py" \
		--repo-root "$(REPO_ROOT)" \
		--source-dir "$(CURDIR)" \
		--output "$(abspath $(SOURCE_BUNDLE_PATH))" \
		--prefix deep-dive-snakemake-capstone
	@printf 'PASS: wrote %s\n' "$(abspath $(SOURCE_BUNDLE_PATH))"

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

verify-report: verify ## Write a structured publish verification report
	@mkdir -p "$(VERIFY_REPORT_DIR)/report"
	@command -v $(PYTHON) >/dev/null || { echo "✘ python missing"; exit 1; }
	@cp FILE_API.md "$(VERIFY_REPORT_DIR)/FILE_API.md"
	@cp PUBLISH_REVIEW_GUIDE.md "$(VERIFY_REPORT_DIR)/PUBLISH_REVIEW_GUIDE.md"
	@cp README.md "$(VERIFY_REPORT_DIR)/README.md"
	@cp "$(PUBLISH_DIR_ABS)/manifest.json" "$(VERIFY_REPORT_DIR)/manifest.json"
	@cp "$(PUBLISH_DIR_ABS)/discovered_samples.json" "$(VERIFY_REPORT_DIR)/discovered_samples.json"
	@cp "$(PUBLISH_DIR_ABS)/summary.json" "$(VERIFY_REPORT_DIR)/summary.json"
	@cp "$(PUBLISH_DIR_ABS)/summary.tsv" "$(VERIFY_REPORT_DIR)/summary.tsv"
	@cp "$(PUBLISH_DIR_ABS)/provenance.json" "$(VERIFY_REPORT_DIR)/provenance.json"
	@cp "$(PUBLISH_DIR_ABS)/report/index.html" "$(VERIFY_REPORT_DIR)/report/index.html"
	@$(PYTHON) scripts/verify_publish.py --publish "$(PUBLISH_DIR_ABS)" --report "$(VERIFY_REPORT_DIR)/verify.json"
	@printf '%s\n' \
		'Verification report route:' \
		'  1. Read PUBLISH_REVIEW_GUIDE.md and FILE_API.md to understand the contract under review.' \
		'  2. Read verify.json for the per-surface publish checks.' \
		'  3. Read manifest.json, discovered_samples.json, summary.json, and provenance.json together.' \
		'  4. Read summary.tsv and report/index.html when you need the compact human-facing review surfaces.' \
		'  5. Use README.md if you need to reconnect the publish boundary to the repository contract.' > "$(VERIFY_REPORT_DIR)/route.txt"
	@printf '%s\n' \
		'Publish review questions:' \
		'  Which files are public contracts and which are only supporting evidence?' \
		'  Which check would fail first if the publish boundary drifted silently?' \
		'  Which publish file would require a version bump if its semantics changed?' > "$(VERIFY_REPORT_DIR)/review-questions.txt"
	@$(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(VERIFY_REPORT_DIR)" --output "$(VERIFY_REPORT_DIR)/bundle-manifest.json"
	@echo "✔ wrote publish verification report to $(VERIFY_REPORT_DIR)"

publish-summary: verify ## Write a compact publish-boundary summary
	@mkdir -p "$(VERIFY_REPORT_DIR)"
	@command -v $(PYTHON) >/dev/null || { echo "✘ python missing"; exit 1; }
	@$(PYTHON) scripts/publish_summary.py --publish "$(PUBLISH_DIR_ABS)" --out "$(VERIFY_REPORT_DIR)/publish-summary.json"
	@echo "✔ wrote publish summary to $(VERIFY_REPORT_DIR)/publish-summary.json"

profile-audit: validate-config ## Build the profile review bundle
	@rm -rf "$(PROFILE_AUDIT_DIR)"
	@mkdir -p "$(PROFILE_AUDIT_DIR)/profiles/local" "$(PROFILE_AUDIT_DIR)/profiles/ci" "$(PROFILE_AUDIT_DIR)/profiles/slurm"
	cp profiles/local/config.yaml "$(PROFILE_AUDIT_DIR)/profiles/local/config.yaml"
	cp profiles/ci/config.yaml "$(PROFILE_AUDIT_DIR)/profiles/ci/config.yaml"
	cp profiles/slurm/config.yaml "$(PROFILE_AUDIT_DIR)/profiles/slurm/config.yaml"
	$(SNAKEMAKE) --profile profiles/local --cores $(CORES) --configfile $(CONFIG) -n -p > "$(PROFILE_AUDIT_DIR)/local-dryrun.txt"
	$(SNAKEMAKE) --profile profiles/ci --cores $(CORES) --configfile $(CONFIG) -n -p > "$(PROFILE_AUDIT_DIR)/ci-dryrun.txt"
	$(SNAKEMAKE) --profile profiles/slurm --cores $(CORES) --configfile $(CONFIG) -n -p > "$(PROFILE_AUDIT_DIR)/slurm-dryrun.txt"
	@printf '%s\n' \
		'Profile audit route:' \
		'  1. Read the three profile config files side by side.' \
		'  2. Compare local-dryrun.txt, ci-dryrun.txt, and slurm-dryrun.txt.' \
		'  3. Ask which settings change execution policy without changing workflow meaning.' \
		'  4. Return to README.md and PROOF_GUIDE.md if you need the workflow contract context.' > "$(PROFILE_AUDIT_DIR)/route.txt"
	@printf '%s\n' \
		'Profile questions:' \
		'  Which differences are executor policy and which would change workflow meaning?' \
		'  Which profile assumptions would matter for reproducibility review later?' \
		'  Which resources are resolved differently across local, ci, and slurm?' > "$(PROFILE_AUDIT_DIR)/review-questions.txt"
	@$(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(PROFILE_AUDIT_DIR)" --output "$(PROFILE_AUDIT_DIR)/bundle-manifest.json"
	@echo "✔ wrote profile audit bundle to $(PROFILE_AUDIT_DIR)"

profile-summary: profile-audit ## Write a compact comparison of local, CI, and SLURM profiles
	@command -v $(PYTHON) >/dev/null || { echo "✘ python missing"; exit 1; }
	@$(PYTHON) scripts/profile_summary.py \
		--local "$(PROFILE_AUDIT_DIR)/profiles/local/config.yaml" \
		--ci "$(PROFILE_AUDIT_DIR)/profiles/ci/config.yaml" \
		--slurm "$(PROFILE_AUDIT_DIR)/profiles/slurm/config.yaml" \
		--out "$(PROFILE_AUDIT_DIR)/profile-summary.json"
	@echo "✔ wrote profile summary to $(PROFILE_AUDIT_DIR)/profile-summary.json"

config-summary: verify ## Write a compact summary of the materialized workflow configuration
	@mkdir -p "$(VERIFY_REPORT_DIR)"
	@command -v $(PYTHON) >/dev/null || { echo "✘ python missing"; exit 1; }
	@$(PYTHON) scripts/config_summary.py \
		--config "config/config.yaml" \
		--provenance "$(PUBLISH_DIR_ABS)/provenance.json" \
		--out "$(VERIFY_REPORT_DIR)/config-summary.json"
	@echo "✔ wrote config summary to $(VERIFY_REPORT_DIR)/config-summary.json"

results-summary: verify ## Write a compact summary of internal per-sample result surfaces
	@mkdir -p "$(VERIFY_REPORT_DIR)"
	@command -v $(PYTHON) >/dev/null || { echo "✘ python missing"; exit 1; }
	@$(PYTHON) scripts/results_summary.py \
		--results-dir "results" \
		--summary-json "$(PUBLISH_DIR_ABS)/summary.json" \
		--out "$(VERIFY_REPORT_DIR)/results-summary.json"
	@echo "✔ wrote results summary to $(VERIFY_REPORT_DIR)/results-summary.json"

evidence-summary: verify ## Write a compact summary of executed logs, benchmarks, and provenance
	@mkdir -p "$(VERIFY_REPORT_DIR)"
	@command -v $(PYTHON) >/dev/null || { echo "✘ python missing"; exit 1; }
	@$(PYTHON) scripts/evidence_summary.py \
		--logs-dir "logs" \
		--benchmarks-dir "benchmarks" \
		--provenance "$(PUBLISH_DIR_ABS)/provenance.json" \
		--manifest "$(PUBLISH_DIR_ABS)/manifest.json" \
		--out "$(VERIFY_REPORT_DIR)/evidence-summary.json"
	@echo "✔ wrote evidence summary to $(VERIFY_REPORT_DIR)/evidence-summary.json"

# ---- high-level flows ----
check: lint test wf-lint wf-dryrun validate-config ## Fast pre-flight (no workflow execution); NOT a formatting gate
ci: fmt-check lint test wf-lint wf-dryrun validate-config ## Strict gate (includes formatting)

validate: check ## Alias
verify: wf-run verify-artifacts ## Execute workflow then verify outputs
confirm: clean purge-dsstore ci verify ## Clean-room confirmation (strict)
selftest: ## Prove deterministic publish behavior across core counts
	@PYTHON_BIN="$(PYTHON)" /bin/bash tests/selftest.sh

proof: tour verify-report profile-audit ## Run the sanctioned learner-facing proof route

walkthrough: clean validate-config wf-lint ## Build a light learner-facing bundle without executing the workflow
	@mkdir -p \
		"$(WALKTHROUGH_DIR_ABS)/workflow/rules" \
		"$(WALKTHROUGH_DIR_ABS)/workflow/modules/qc_module" \
		"$(WALKTHROUGH_DIR_ABS)/workflow/modules/screen_module" \
		"$(WALKTHROUGH_DIR_ABS)/workflow/scripts" \
		"$(WALKTHROUGH_DIR_ABS)/profiles/local" \
		"$(WALKTHROUGH_DIR_ABS)/profiles/ci" \
		"$(WALKTHROUGH_DIR_ABS)/profiles/slurm" \
		"$(WALKTHROUGH_DIR_ABS)/scripts"
	$(SNAKEMAKE) --list-rules > "$(WALKTHROUGH_DIR_ABS)/list-rules.txt"
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) -n -p > "$(WALKTHROUGH_DIR_ABS)/dryrun.txt"
	cp README.md "$(WALKTHROUGH_DIR_ABS)/README.md"
	cp DOMAIN_GUIDE.md "$(WALKTHROUGH_DIR_ABS)/DOMAIN_GUIDE.md"
	cp WORKFLOW_STAGE_GUIDE.md "$(WALKTHROUGH_DIR_ABS)/WORKFLOW_STAGE_GUIDE.md"
	cp CHECKPOINT_GUIDE.md "$(WALKTHROUGH_DIR_ABS)/CHECKPOINT_GUIDE.md"
	cp EXACT_SOURCE_GUIDE.md "$(WALKTHROUGH_DIR_ABS)/EXACT_SOURCE_GUIDE.md"
	cp ARCHITECTURE.md "$(WALKTHROUGH_DIR_ABS)/ARCHITECTURE.md"
	cp WALKTHROUGH_GUIDE.md "$(WALKTHROUGH_DIR_ABS)/WALKTHROUGH_GUIDE.md"
	cp PROOF_GUIDE.md "$(WALKTHROUGH_DIR_ABS)/PROOF_GUIDE.md"
	cp Snakefile "$(WALKTHROUGH_DIR_ABS)/Snakefile"
	cp FILE_API.md "$(WALKTHROUGH_DIR_ABS)/FILE_API.md"
	cp config/config.yaml "$(WALKTHROUGH_DIR_ABS)/config.yaml"
	cp config/schema.yaml "$(WALKTHROUGH_DIR_ABS)/schema.yaml"
	cp workflow/rules/common.smk "$(WALKTHROUGH_DIR_ABS)/workflow/rules/common.smk"
	cp workflow/rules/preprocess.smk "$(WALKTHROUGH_DIR_ABS)/workflow/rules/preprocess.smk"
	cp workflow/rules/summarize_report.smk "$(WALKTHROUGH_DIR_ABS)/workflow/rules/summarize_report.smk"
	cp workflow/rules/publish.smk "$(WALKTHROUGH_DIR_ABS)/workflow/rules/publish.smk"
	cp workflow/modules/qc_module/Snakefile "$(WALKTHROUGH_DIR_ABS)/workflow/modules/qc_module/Snakefile"
	cp workflow/modules/screen_module/Snakefile "$(WALKTHROUGH_DIR_ABS)/workflow/modules/screen_module/Snakefile"
	cp workflow/scripts/provenance.py "$(WALKTHROUGH_DIR_ABS)/workflow/scripts/provenance.py"
	cp profiles/local/config.yaml "$(WALKTHROUGH_DIR_ABS)/profiles/local/config.yaml"
	cp profiles/ci/config.yaml "$(WALKTHROUGH_DIR_ABS)/profiles/ci/config.yaml"
	cp profiles/slurm/config.yaml "$(WALKTHROUGH_DIR_ABS)/profiles/slurm/config.yaml"
	cp scripts/validate_config.py "$(WALKTHROUGH_DIR_ABS)/scripts/validate_config.py"
	cp scripts/verify_publish.py "$(WALKTHROUGH_DIR_ABS)/scripts/verify_publish.py"
	cp TOUR.md "$(WALKTHROUGH_DIR_ABS)/TOUR.md"
	@printf '%s\n' \
		'1. Read DOMAIN_GUIDE.md if the sample story or biological vocabulary is still fuzzy.' \
		'2. Read README.md for the repository contract and WORKFLOW_STAGE_GUIDE.md for stage ownership.' \
		'3. Read CHECKPOINT_GUIDE.md and Snakefile to see how discovery becomes a durable artifact.' \
		'4. Read the copied rule files, module Snakefiles, and list-rules.txt for visible workflow meaning.' \
		'5. Read dryrun.txt to inspect the declared plan before execution.' \
		'6. Read ARCHITECTURE.md and EXACT_SOURCE_GUIDE.md when the next file is not obvious.' \
		'7. Read profiles/*/config.yaml, config.yaml, and schema.yaml to separate workflow meaning from policy.' \
		'8. Read workflow/scripts/provenance.py and scripts/*.py to see how provenance, config, and publish checks are enforced.' \
		'9. Read FILE_API.md to see which outputs are public contracts.' \
		'10. Run make selftest when the next honest question is determinism.' \
		'11. Run make tour when you need executed proof artifacts.' > "$(WALKTHROUGH_DIR_ABS)/route.txt"
	@printf '%s\n' \
		'Public entry commands:' \
		'  make walkthrough' \
		'  make wf-dryrun' \
		'  make selftest' \
		'  make verify' \
		'  make confirm' \
		'  make tour' > "$(WALKTHROUGH_DIR_ABS)/commands.txt"
	@printf '%s\n' \
		'Review questions:' \
		'  Which file should a first-time learner read before touching the workflow itself?' \
		'  Where does dynamic discovery become explicit and reviewable?' \
		'  Which layer owns workflow meaning, operating policy, and downstream trust?' \
		'  Which published outputs are safe for downstream trust?' \
		'  Which guarantees come from clean-room confirmation rather than a dry-run?' > "$(WALKTHROUGH_DIR_ABS)/review-questions.txt"
	@$(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(WALKTHROUGH_DIR_ABS)" --output "$(WALKTHROUGH_DIR_ABS)/bundle-manifest.json"
	@echo "✔ wrote workflow walkthrough to $(WALKTHROUGH_DIR_ABS)"

tour: clean validate-config wf-lint ## Build a learner-facing workflow proof bundle
	@mkdir -p \
		"$(TOUR_DIR_ABS)/workflow/rules" \
		"$(TOUR_DIR_ABS)/profiles/local" \
		"$(TOUR_DIR_ABS)/profiles/ci" \
		"$(TOUR_DIR_ABS)/profiles/slurm" \
		"$(TOUR_DIR_ABS)/report"
	$(SNAKEMAKE) --list-rules > "$(TOUR_DIR_ABS)/list-rules.txt"
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) -n -p > "$(TOUR_DIR_ABS)/dryrun.txt"
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) 2>&1 | tee "$(TOUR_DIR_ABS)/run.txt"
	$(SNAKEMAKE) --profile $(PROFILE) --cores $(CORES) --configfile $(CONFIG) --summary > "$(TOUR_DIR_ABS)/summary.txt"
	$(PYTHON) scripts/verify_publish.py --publish "$(PUBLISH_DIR_ABS)" > "$(TOUR_DIR_ABS)/verify.txt"
	cp README.md "$(TOUR_DIR_ABS)/README.md"
	cp DOMAIN_GUIDE.md "$(TOUR_DIR_ABS)/DOMAIN_GUIDE.md"
	cp WORKFLOW_STAGE_GUIDE.md "$(TOUR_DIR_ABS)/WORKFLOW_STAGE_GUIDE.md"
	cp CHECKPOINT_GUIDE.md "$(TOUR_DIR_ABS)/CHECKPOINT_GUIDE.md"
	cp EXACT_SOURCE_GUIDE.md "$(TOUR_DIR_ABS)/EXACT_SOURCE_GUIDE.md"
	cp ARCHITECTURE.md "$(TOUR_DIR_ABS)/ARCHITECTURE.md"
	cp Snakefile "$(TOUR_DIR_ABS)/Snakefile"
	cp PROOF_GUIDE.md "$(TOUR_DIR_ABS)/PROOF_GUIDE.md"
	cp FILE_API.md "$(TOUR_DIR_ABS)/FILE_API.md"
	cp PUBLISH_REVIEW_GUIDE.md "$(TOUR_DIR_ABS)/PUBLISH_REVIEW_GUIDE.md"
	cp PROFILE_AUDIT_GUIDE.md "$(TOUR_DIR_ABS)/PROFILE_AUDIT_GUIDE.md"
	cp INCIDENT_REVIEW_GUIDE.md "$(TOUR_DIR_ABS)/INCIDENT_REVIEW_GUIDE.md"
	cp EXTENSION_GUIDE.md "$(TOUR_DIR_ABS)/EXTENSION_GUIDE.md"
	cp config/config.yaml "$(TOUR_DIR_ABS)/config.yaml"
	cp config/schema.yaml "$(TOUR_DIR_ABS)/schema.yaml"
	cp workflow/rules/common.smk "$(TOUR_DIR_ABS)/workflow/rules/common.smk"
	cp workflow/rules/preprocess.smk "$(TOUR_DIR_ABS)/workflow/rules/preprocess.smk"
	cp workflow/rules/summarize_report.smk "$(TOUR_DIR_ABS)/workflow/rules/summarize_report.smk"
	cp workflow/rules/publish.smk "$(TOUR_DIR_ABS)/workflow/rules/publish.smk"
	cp profiles/local/config.yaml "$(TOUR_DIR_ABS)/profiles/local/config.yaml"
	cp profiles/ci/config.yaml "$(TOUR_DIR_ABS)/profiles/ci/config.yaml"
	cp profiles/slurm/config.yaml "$(TOUR_DIR_ABS)/profiles/slurm/config.yaml"
	cp "$(MANIFEST_ABS)" "$(TOUR_DIR_ABS)/publish-manifest.json"
	cp "$(PUBLISH_DIR_ABS)/discovered_samples.json" "$(TOUR_DIR_ABS)/discovered_samples.json"
	cp "$(PUBLISH_DIR_ABS)/provenance.json" "$(TOUR_DIR_ABS)/provenance.json"
	cp "$(PUBLISH_DIR_ABS)/summary.json" "$(TOUR_DIR_ABS)/summary.json"
	cp "$(PUBLISH_DIR_ABS)/summary.tsv" "$(TOUR_DIR_ABS)/summary.tsv"
	cp "$(PUBLISH_DIR_ABS)/report/index.html" "$(TOUR_DIR_ABS)/report/index.html"
	cp TOUR.md "$(TOUR_DIR_ABS)/TOUR.md"
	@printf '%s\n' \
		'Executed review route:' \
		'  1. Read README.md and DOMAIN_GUIDE.md to reset the repository and domain contract.' \
		'  2. Read list-rules.txt, dryrun.txt, and WORKFLOW_STAGE_GUIDE.md for the declared workflow shape.' \
		'  3. Read CHECKPOINT_GUIDE.md with discovered_samples.json when discovery behavior is the review target.' \
		'  4. Read summary.txt and run.txt for executed workflow evidence.' \
		'  5. Read publish-manifest.json, summary.json, summary.tsv, provenance.json, and report/index.html together.' \
		'  6. Read FILE_API.md and PUBLISH_REVIEW_GUIDE.md to interpret the published boundary.' \
		'  7. Read ARCHITECTURE.md, PROFILE_AUDIT_GUIDE.md, and INCIDENT_REVIEW_GUIDE.md when the issue is ownership or operating context.' \
		'  8. Read EXACT_SOURCE_GUIDE.md when the next file is still not obvious.' > "$(TOUR_DIR_ABS)/route.txt"
	@printf '%s\n' \
		'Review questions:' \
		'  Which workflow claims are visible before execution, and which only after execution?' \
		'  Which publish artifacts would you trust downstream without reading logs?' \
		'  Which behavior is tied to workflow design rather than executor choice?' \
		'  Which guide would you hand to a reviewer who only cares about discovery, publish trust, or profile drift?' > "$(TOUR_DIR_ABS)/review-questions.txt"
	@$(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(TOUR_DIR_ABS)" --output "$(TOUR_DIR_ABS)/bundle-manifest.json"
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
