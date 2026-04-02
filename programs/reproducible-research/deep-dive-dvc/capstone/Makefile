SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

PYTHON ?= python3
ARTIFACTS_DIR ?= ../../../../artifacts
VENV_DIR ?= $(ARTIFACTS_DIR)/venv/reproducible-research/deep-dive-dvc/capstone
VENV_BIN := $(VENV_DIR)/bin
VENV_PY := $(abspath $(VENV_BIN)/python)
PIP := $(VENV_PY) -m pip
PYTEST := $(VENV_PY) -m pytest
DVC := $(VENV_PY) -m dvc
WALKTHROUGH_DIR ?= $(ARTIFACTS_DIR)/walkthrough/reproducible-research/deep-dive-dvc
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/reproducible-research/deep-dive-dvc
RELEASE_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-dvc
VERIFY_REPORT_DIR ?= $(ARTIFACTS_DIR)/proof/reproducible-research/deep-dive-dvc/verify

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: venv
venv: ## Create the local virtual environment
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: install
install: venv ## Install capstone dependencies
	@$(PIP) install -e . pytest dvc

.PHONY: dvc-init
dvc-init: install ## Initialize DVC metadata and the local training remote
	@if [ ! -d .dvc ]; then $(DVC) init --subdir -q; fi
	@if ! $(DVC) remote list | grep -q '^training-local'; then $(DVC) remote add -d training-local .dvc-remote; fi

.PHONY: repro
repro: dvc-init ## Execute the DVC pipeline
	@$(DVC) repro

.PHONY: test
test: install ## Run the Python test suite
	@$(PYTEST)

.PHONY: verify
verify: repro ## Validate the published artifact contract
	@$(VENV_PY) -m incident_escalation_capstone.verify --publish publish/v1

.PHONY: verify-report
verify-report: repro ## Write a structured verification report for the published contract
	@rm -rf $(VERIFY_REPORT_DIR)
	@mkdir -p $(VERIFY_REPORT_DIR)
	@$(VENV_PY) -m incident_escalation_capstone.verify --publish publish/v1 --report $(VERIFY_REPORT_DIR)/verify.json
	@printf '%s\n' \
		'Verification report route:' \
		'  1. Read verify.json for the per-surface contract results.' \
		'  2. Read publish/v1/manifest.json beside it when you need promoted file inventory.' \
		'  3. Read publish/v1/report.md when you need the human-readable release story.' > $(VERIFY_REPORT_DIR)/route.txt
	@echo "✔ wrote verification report to $(VERIFY_REPORT_DIR)"

.PHONY: tour
tour: verify ## Build the learner-facing proof bundle
	@rm -rf $(TOUR_DIR)
	@mkdir -p $(TOUR_DIR)/publish-v1
	@$(DVC) status > $(TOUR_DIR)/status.txt
	@$(DVC) remote list > $(TOUR_DIR)/remote.txt
	@$(DVC) dag --dot > $(TOUR_DIR)/pipeline.dot
	@cp dvc.yaml $(TOUR_DIR)/dvc.yaml
	@cp dvc.lock $(TOUR_DIR)/dvc.lock
	@cp params.yaml $(TOUR_DIR)/params.yaml
	@cp PUBLISH_CONTRACT.md $(TOUR_DIR)/PUBLISH_CONTRACT.md
	@cp metrics/metrics.json $(TOUR_DIR)/metrics.json
	@cp publish/v1/manifest.json $(TOUR_DIR)/publish-v1/manifest.json
	@cp publish/v1/metrics.json $(TOUR_DIR)/publish-v1/metrics.json
	@cp publish/v1/params.yaml $(TOUR_DIR)/publish-v1/params.yaml
	@cp publish/v1/data-profile.json $(TOUR_DIR)/publish-v1/data-profile.json
	@cp publish/v1/model.json $(TOUR_DIR)/publish-v1/model.json
	@cp publish/v1/predictions.csv $(TOUR_DIR)/publish-v1/predictions.csv
	@cp publish/v1/report.md $(TOUR_DIR)/publish-v1/report.md
	@cp TOUR.md $(TOUR_DIR)/TOUR.md
	@printf '%s\n' \
		'Executed proof route:' \
		'  1. Read status.txt for DVC up-to-date state.' \
		'  2. Read dvc.yaml and dvc.lock together.' \
		'  3. Read publish-v1/manifest.json and PUBLISH_CONTRACT.md together.' \
		'  4. Read publish-v1/metrics.json and publish-v1/params.yaml.' \
		'  5. Read remote.txt when reviewing recovery assumptions.' > $(TOUR_DIR)/route.txt
	@printf '%s\n' \
		'Release boundary evidence:' \
		'  publish-v1/manifest.json   inventory, hashes, and promoted training summary' \
		'  publish-v1/metrics.json    promoted evaluation metrics' \
		'  publish-v1/params.yaml     promoted control surface' \
		'  publish-v1/report.md       human-readable review surface' \
		'  PUBLISH_CONTRACT.md        meaning and trust limits for promoted files' > $(TOUR_DIR)/release-boundary.txt
	@printf '%s\n' \
		'Recovery evidence:' \
		'  remote.txt                 configured DVC recovery source' \
		'  status.txt                 repository state after verification' \
		'  dvc.lock                   recorded execution state that publish/v1 came from' > $(TOUR_DIR)/recovery-evidence.txt
	@echo "tour_dir=$(TOUR_DIR)" > $(TOUR_DIR)/bundle.env
	@echo "publish_dir=$(TOUR_DIR)/publish-v1" >> $(TOUR_DIR)/bundle.env
	@echo "✔ wrote learner-facing tour to $(TOUR_DIR)"

.PHONY: release-audit
release-audit: verify ## Build a focused release-boundary audit bundle
	@rm -rf $(RELEASE_AUDIT_DIR)
	@mkdir -p $(RELEASE_AUDIT_DIR)/publish-v1
	@cp PUBLISH_CONTRACT.md $(RELEASE_AUDIT_DIR)/PUBLISH_CONTRACT.md
	@cp publish/v1/manifest.json $(RELEASE_AUDIT_DIR)/publish-v1/manifest.json
	@cp publish/v1/metrics.json $(RELEASE_AUDIT_DIR)/publish-v1/metrics.json
	@cp publish/v1/params.yaml $(RELEASE_AUDIT_DIR)/publish-v1/params.yaml
	@cp publish/v1/report.md $(RELEASE_AUDIT_DIR)/publish-v1/report.md
	@cp dvc.lock $(RELEASE_AUDIT_DIR)/dvc.lock
	@printf '%s\n' \
		'Release audit route:' \
		'  1. Read publish-v1/manifest.json for the promoted inventory.' \
		'  2. Read PUBLISH_CONTRACT.md for meaning and trust limits.' \
		'  3. Read publish-v1/params.yaml and publish-v1/metrics.json together.' \
		'  4. Read publish-v1/report.md for the human-readable summary.' \
		'  5. Compare dvc.lock against the promoted contract when you need recorded provenance.' > $(RELEASE_AUDIT_DIR)/route.txt
	@printf '%s\n' \
		'Release questions:' \
		'  Which promoted files are safe for downstream trust?' \
		'  Which review claims still depend on repository-internal evidence?' \
		'  Which promoted metrics and params remain semantically meaningful later?' > $(RELEASE_AUDIT_DIR)/review-questions.txt
	@echo "audit_dir=$(RELEASE_AUDIT_DIR)" > $(RELEASE_AUDIT_DIR)/bundle.env
	@echo "publish_dir=$(RELEASE_AUDIT_DIR)/publish-v1" >> $(RELEASE_AUDIT_DIR)/bundle.env
	@echo "✔ wrote release audit bundle to $(RELEASE_AUDIT_DIR)"

.PHONY: walkthrough
walkthrough: ## Build the learner-facing capstone walkthrough bundle
	@rm -rf $(WALKTHROUGH_DIR)
	@mkdir -p $(WALKTHROUGH_DIR)
	@cp README.md $(WALKTHROUGH_DIR)/README.md
	@cp PUBLISH_CONTRACT.md $(WALKTHROUGH_DIR)/PUBLISH_CONTRACT.md
	@cp dvc.yaml $(WALKTHROUGH_DIR)/dvc.yaml
	@cp dvc.lock $(WALKTHROUGH_DIR)/dvc.lock
	@cp params.yaml $(WALKTHROUGH_DIR)/params.yaml
	@cp TOUR.md $(WALKTHROUGH_DIR)/TOUR.md
	@printf '%s\n' \
		'1. Read README.md to understand the repository contract.' \
		'2. Read PUBLISH_CONTRACT.md to understand the promoted boundary.' \
		'3. Read dvc.yaml to inspect the declared pipeline.' \
		'4. Read dvc.lock to compare recorded state against the declaration.' \
		'5. Read params.yaml to see the declared control surface.' \
		'6. Run make verify when you want executed proof.' \
		'7. Run make tour when you want the full evidence bundle.' > $(WALKTHROUGH_DIR)/route.txt
	@printf '%s\n' \
		'Public entry commands:' \
		'  make walkthrough' \
		'  make repro' \
		'  make verify' \
		'  make confirm' \
		'  make recovery-drill' \
		'  make tour' > $(WALKTHROUGH_DIR)/commands.txt
	@printf '%s\n' \
		'Review questions:' \
		'  Which state is authoritative for declaration, execution, and promotion?' \
		'  Which params and metrics are safe to compare later?' \
		'  Which promoted files could a downstream reviewer trust without private context?' \
		'  Which guarantees still depend on the DVC remote rather than the publish bundle alone?' > $(WALKTHROUGH_DIR)/review-questions.txt
	@printf '%s\n' \
		'Walkthrough bundle surfaces:' \
		'  README.md             repository contract and learner entry rule' \
		'  PUBLISH_CONTRACT.md   promoted boundary and trust limits' \
		'  dvc.yaml              declared stage contract' \
		'  dvc.lock              recorded execution state' \
		'  params.yaml           control surface' \
		'  TOUR.md               proof-bundle reading route' > $(WALKTHROUGH_DIR)/bundle-guide.txt
	@echo "✔ wrote learner-facing walkthrough to $(WALKTHROUGH_DIR)"

.PHONY: push
push: repro ## Push tracked artifacts to the local training remote
	@$(DVC) push

.PHONY: recovery-drill
recovery-drill: push ## Rebuild the workspace from the remote after cache loss
	@rm -rf data/derived metrics models publish state .dvc/cache
	@$(DVC) pull
	@$(DVC) checkout
	@$(VENV_PY) -m incident_escalation_capstone.verify --publish publish/v1

.PHONY: confirm
confirm: verify test recovery-drill ## Run the full capstone verification suite

.PHONY: clean-generated
clean-generated: ## Remove generated pipeline outputs
	@rm -rf data/derived metrics models publish state

.PHONY: clean
clean: clean-generated ## Remove local virtual environment and caches
	@rm -rf $(VENV_DIR) .pytest_cache .dvc/cache __pycache__
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
