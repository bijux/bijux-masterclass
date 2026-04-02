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
INSPECT := $(VENV_PY) -m incident_escalation_capstone.inspect
WALKTHROUGH_DIR ?= $(ARTIFACTS_DIR)/walkthrough/reproducible-research/deep-dive-dvc
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/reproducible-research/deep-dive-dvc
RELEASE_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-dvc
VERIFY_REPORT_DIR ?= $(ARTIFACTS_DIR)/proof/reproducible-research/deep-dive-dvc/verify
RECOVERY_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-dvc/recovery
EXPERIMENT_REVIEW_DIR ?= $(ARTIFACTS_DIR)/review/reproducible-research/deep-dive-dvc/experiments

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: venv
venv: ## Create the local virtual environment
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: install
install: venv ## Install capstone dependencies
	@rm -rf src/incident_escalation_capstone.egg-info
	@$(PIP) install -e . pytest dvc

.PHONY: platform-report
platform-report: install ## Print the supported Python, Git, and DVC versions
	@printf 'python_executable=%s\n' "$(VENV_PY)"
	@$(VENV_PY) -c 'import sys; print(f"python_version={sys.version.split()[0]}")'
	@printf 'git_version=%s\n' "$$(git --version | awk "{print \$$3}")"
	@printf 'dvc_version=%s\n' "$$($(DVC) version | awk "NR==1 {print \$$3}")"

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
	@$(VENV_PY) scripts/write_bundle_manifest.py --bundle-dir $(VERIFY_REPORT_DIR) --output $(VERIFY_REPORT_DIR)/manifest.json
	@echo "✔ wrote verification report to $(VERIFY_REPORT_DIR)"

.PHONY: state-summary
state-summary: verify ## Render the combined declaration, execution, and release summary
	@$(INSPECT) state-summary --publish publish/v1 --metrics metrics/metrics.json --params params.yaml --lock dvc.lock

.PHONY: stage-summary
stage-summary: verify ## Render the declared and recorded stage contract summary
	@$(INSPECT) stage-summary --pipeline dvc.yaml --lock dvc.lock

.PHONY: profile-summary
profile-summary: verify ## Render the promoted data profile summary
	@$(INSPECT) profile-summary --publish publish/v1

.PHONY: model-summary
model-summary: verify ## Render the promoted model summary
	@$(INSPECT) model-summary --publish publish/v1

.PHONY: release-summary
release-summary: verify ## Render the promoted release summary
	@$(INSPECT) release-summary --publish publish/v1

.PHONY: review-queue
review-queue: verify ## Render the structured prediction review queue
	@$(INSPECT) review-queue --publish publish/v1

.PHONY: threshold-review
threshold-review: verify ## Render borderline predictions near the decision threshold
	@$(INSPECT) threshold-review --publish publish/v1

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
	@cp ARCHITECTURE.md $(TOUR_DIR)/ARCHITECTURE.md
	@cp EXPERIMENT_GUIDE.md $(TOUR_DIR)/EXPERIMENT_GUIDE.md
	@cp RECOVERY_GUIDE.md $(TOUR_DIR)/RECOVERY_GUIDE.md
	@cp RELEASE_REVIEW_GUIDE.md $(TOUR_DIR)/RELEASE_REVIEW_GUIDE.md
	@cp metrics/metrics.json $(TOUR_DIR)/metrics.json
	@cp publish/v1/manifest.json $(TOUR_DIR)/publish-v1/manifest.json
	@cp publish/v1/metrics.json $(TOUR_DIR)/publish-v1/metrics.json
	@cp publish/v1/params.yaml $(TOUR_DIR)/publish-v1/params.yaml
	@cp publish/v1/data-profile.json $(TOUR_DIR)/publish-v1/data-profile.json
	@cp publish/v1/model.json $(TOUR_DIR)/publish-v1/model.json
	@cp publish/v1/predictions.csv $(TOUR_DIR)/publish-v1/predictions.csv
	@cp publish/v1/report.md $(TOUR_DIR)/publish-v1/report.md
	@cp TOUR.md $(TOUR_DIR)/TOUR.md
	@$(INSPECT) profile-summary --publish publish/v1 > $(TOUR_DIR)/profile-summary.json
	@$(INSPECT) model-summary --publish publish/v1 > $(TOUR_DIR)/model-summary.json
	@$(INSPECT) stage-summary --pipeline dvc.yaml --lock dvc.lock > $(TOUR_DIR)/stage-summary.json
	@$(INSPECT) state-summary --publish publish/v1 --metrics metrics/metrics.json --params params.yaml --lock dvc.lock > $(TOUR_DIR)/state-summary.json
	@$(INSPECT) release-summary --publish publish/v1 > $(TOUR_DIR)/release-summary.json
	@$(INSPECT) review-queue --publish publish/v1 > $(TOUR_DIR)/review-queue.json
	@$(INSPECT) threshold-review --publish publish/v1 > $(TOUR_DIR)/threshold-review.json
	@printf '%s\n' \
		'Executed proof route:' \
		'  1. Read status.txt for DVC up-to-date state.' \
		'  2. Read stage-summary.json before comparing dvc.yaml and dvc.lock directly.' \
		'  3. Read dvc.yaml and dvc.lock together.' \
		'  4. Read publish-v1/manifest.json and PUBLISH_CONTRACT.md together.' \
		'  5. Read profile-summary.json, model-summary.json, publish-v1/metrics.json, threshold-review.json, and publish-v1/params.yaml together.' \
		'  6. Read remote.txt when reviewing recovery assumptions.' > $(TOUR_DIR)/route.txt
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
	@$(VENV_PY) scripts/write_bundle_manifest.py --bundle-dir $(TOUR_DIR) --output $(TOUR_DIR)/manifest.json
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
	@$(VENV_PY) scripts/write_bundle_manifest.py --bundle-dir $(RELEASE_AUDIT_DIR) --output $(RELEASE_AUDIT_DIR)/manifest.json
	@echo "✔ wrote release audit bundle to $(RELEASE_AUDIT_DIR)"

.PHONY: release-review
release-review: release-audit ## Build a focused release review bundle


.PHONY: recovery-audit
recovery-audit: push ## Capture the remote-backed recovery route as a review bundle
	@rm -rf $(RECOVERY_AUDIT_DIR)
	@mkdir -p $(RECOVERY_AUDIT_DIR)/publish-v1
	@$(DVC) status > $(RECOVERY_AUDIT_DIR)/before-status.txt
	@$(DVC) remote list > $(RECOVERY_AUDIT_DIR)/remote.txt
	@rm -rf data/derived metrics models publish state .dvc/cache
	@$(DVC) pull > $(RECOVERY_AUDIT_DIR)/pull.txt
	@$(DVC) checkout > $(RECOVERY_AUDIT_DIR)/checkout.txt
	@$(VENV_PY) -m incident_escalation_capstone.verify --publish publish/v1 --report $(RECOVERY_AUDIT_DIR)/verify.json
	@$(DVC) status > $(RECOVERY_AUDIT_DIR)/after-status.txt
	@cp dvc.lock $(RECOVERY_AUDIT_DIR)/dvc.lock
	@cp publish/v1/manifest.json $(RECOVERY_AUDIT_DIR)/publish-v1/manifest.json
	@cp publish/v1/report.md $(RECOVERY_AUDIT_DIR)/publish-v1/report.md
	@printf '%s\n' \
		'Recovery audit route:' \
		'  1. Read remote.txt to confirm the configured recovery source.' \
		'  2. Compare before-status.txt and after-status.txt to see the repository state around the drill.' \
		'  3. Read pull.txt and checkout.txt for the recovery commands that rebuilt local state.' \
		'  4. Read verify.json and publish-v1/manifest.json to confirm the restored publish contract.' \
		'  5. Compare dvc.lock against the restored publish bundle when you need recorded provenance.' > $(RECOVERY_AUDIT_DIR)/route.txt
	@printf '%s\n' \
		'Recovery questions:' \
		'  Which facts come from the remote-backed restore rather than the working tree?' \
		'  Which restored files are safe for downstream trust without re-running training?' \
		'  Which parts of recovery still depend on repository-internal state rather than the publish bundle alone?' > $(RECOVERY_AUDIT_DIR)/review-questions.txt
	@$(VENV_PY) scripts/write_bundle_manifest.py --bundle-dir $(RECOVERY_AUDIT_DIR) --output $(RECOVERY_AUDIT_DIR)/manifest.json
	@echo "✔ wrote recovery audit bundle to $(RECOVERY_AUDIT_DIR)"

.PHONY: recovery-review
recovery-review: recovery-audit ## Capture the remote-backed recovery review bundle

.PHONY: experiment-review
experiment-review: verify ## Build a focused experiment comparison bundle
	@rm -rf $(EXPERIMENT_REVIEW_DIR)
	@mkdir -p $(EXPERIMENT_REVIEW_DIR)
	@cp params.yaml $(EXPERIMENT_REVIEW_DIR)/params.yaml
	@cp metrics/metrics.json $(EXPERIMENT_REVIEW_DIR)/metrics.json
	@cp publish/v1/report.md $(EXPERIMENT_REVIEW_DIR)/report.md
	@$(DVC) exp show --no-pager > $(EXPERIMENT_REVIEW_DIR)/exp-show.txt
	@printf '%s\n' \
		'Experiment review route:' \
		'  1. Read params.yaml for the baseline control surface.' \
		'  2. Read metrics.json for the baseline quantitative surface.' \
		'  3. Read exp-show.txt for comparable experiment records.' \
		'  4. Read report.md when you need the current promoted human review surface.' > $(EXPERIMENT_REVIEW_DIR)/route.txt
	@printf '%s\n' \
		'Experiment review questions:' \
		'  Which declared parameter changes are being compared?' \
		'  Which metric changes matter enough to justify promotion review?' \
		'  Which candidate still needs release-boundary evidence before downstream trust?' > $(EXPERIMENT_REVIEW_DIR)/review-questions.txt
	@$(VENV_PY) scripts/write_bundle_manifest.py --bundle-dir $(EXPERIMENT_REVIEW_DIR) --output $(EXPERIMENT_REVIEW_DIR)/manifest.json
	@echo "✔ wrote experiment review bundle to $(EXPERIMENT_REVIEW_DIR)"

.PHONY: walkthrough
walkthrough: ## Build the learner-facing capstone walkthrough bundle
	@rm -rf $(WALKTHROUGH_DIR)
	@mkdir -p $(WALKTHROUGH_DIR)/src/incident_escalation_capstone $(WALKTHROUGH_DIR)/tests $(WALKTHROUGH_DIR)/publish-v1
	@cp README.md $(WALKTHROUGH_DIR)/README.md
	@cp DOMAIN_GUIDE.md $(WALKTHROUGH_DIR)/DOMAIN_GUIDE.md
	@cp STAGE_CONTRACT_GUIDE.md $(WALKTHROUGH_DIR)/STAGE_CONTRACT_GUIDE.md
	@cp STATE_LAYER_GUIDE.md $(WALKTHROUGH_DIR)/STATE_LAYER_GUIDE.md
	@cp CONTROL_SURFACE_GUIDE.md $(WALKTHROUGH_DIR)/CONTROL_SURFACE_GUIDE.md
	@cp ARCHITECTURE.md $(WALKTHROUGH_DIR)/ARCHITECTURE.md
	@cp PUBLISH_CONTRACT.md $(WALKTHROUGH_DIR)/PUBLISH_CONTRACT.md
	@cp dvc.yaml $(WALKTHROUGH_DIR)/dvc.yaml
	@cp dvc.lock $(WALKTHROUGH_DIR)/dvc.lock
	@cp params.yaml $(WALKTHROUGH_DIR)/params.yaml
	@cp TOUR.md $(WALKTHROUGH_DIR)/TOUR.md
	@cp src/incident_escalation_capstone/prepare.py $(WALKTHROUGH_DIR)/src/incident_escalation_capstone/prepare.py
	@cp src/incident_escalation_capstone/fit.py $(WALKTHROUGH_DIR)/src/incident_escalation_capstone/fit.py
	@cp src/incident_escalation_capstone/evaluate.py $(WALKTHROUGH_DIR)/src/incident_escalation_capstone/evaluate.py
	@cp src/incident_escalation_capstone/publish.py $(WALKTHROUGH_DIR)/src/incident_escalation_capstone/publish.py
	@cp src/incident_escalation_capstone/inspect.py $(WALKTHROUGH_DIR)/src/incident_escalation_capstone/inspect.py
	@cp src/incident_escalation_capstone/verify.py $(WALKTHROUGH_DIR)/src/incident_escalation_capstone/verify.py
	@cp tests/test_prepare.py $(WALKTHROUGH_DIR)/tests/test_prepare.py
	@cp tests/test_inspect.py $(WALKTHROUGH_DIR)/tests/test_inspect.py
	@cp tests/test_verify.py $(WALKTHROUGH_DIR)/tests/test_verify.py
	@cp publish/v1/manifest.json $(WALKTHROUGH_DIR)/publish-v1/manifest.json
	@cp publish/v1/report.md $(WALKTHROUGH_DIR)/publish-v1/report.md
	@printf '%s\n' \
		'1. Read README.md to understand the repository contract.' \
		'2. Read DOMAIN_GUIDE.md, STAGE_CONTRACT_GUIDE.md, STATE_LAYER_GUIDE.md, and CONTROL_SURFACE_GUIDE.md to understand the repository model before reading code.' \
		'3. Read PUBLISH_CONTRACT.md to understand the promoted boundary.' \
		'4. Read dvc.yaml to inspect the declared pipeline.' \
		'5. Read dvc.lock to compare recorded state against the declaration.' \
		'6. Read params.yaml to see the declared control surface.' \
		'7. Read prepare.py, fit.py, evaluate.py, publish.py, inspect.py, and verify.py in stage order.' \
		'8. Read the matching tests to see how the contracts are enforced.' \
		'9. Read publish-v1/manifest.json and publish-v1/report.md as concrete promotion examples.' \
		'10. Run make verify when you want executed proof.' \
		'11. Run make tour when you want the full evidence bundle.' > $(WALKTHROUGH_DIR)/route.txt
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
		'  DOMAIN_GUIDE.md       operational problem and data vocabulary' \
		'  STAGE_CONTRACT_GUIDE.md stage-by-stage ownership boundaries' \
		'  STATE_LAYER_GUIDE.md  authority map for repository state layers' \
		'  CONTROL_SURFACE_GUIDE.md params-and-metrics comparability rules' \
		'  ARCHITECTURE.md       file-level ownership route' \
		'  PUBLISH_CONTRACT.md   promoted boundary and trust limits' \
		'  dvc.yaml              declared stage contract' \
		'  dvc.lock              recorded execution state' \
		'  params.yaml           control surface' \
		'  prepare.py            split and profile stage implementation' \
		'  fit.py                model-training stage implementation' \
		'  evaluate.py           metrics and predictions stage implementation' \
		'  publish.py            promotion stage implementation' \
		'  inspect.py            learner-facing summary routes' \
		'  verify.py             publish-contract enforcement logic' \
		'  test_prepare.py       split and profile regression coverage' \
		'  test_inspect.py       summary-route regression coverage' \
		'  test_verify.py        contract regression coverage' \
		'  publish-v1/manifest.json concrete promoted inventory' \
		'  publish-v1/report.md  concrete review surface' \
		'  TOUR.md               proof-bundle reading route' > $(WALKTHROUGH_DIR)/bundle-guide.txt
	@$(VENV_PY) scripts/write_bundle_manifest.py --bundle-dir $(WALKTHROUGH_DIR) --output $(WALKTHROUGH_DIR)/manifest.json
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
	@rm -rf $(VENV_DIR) .pytest_cache .dvc/cache __pycache__ src/incident_escalation_capstone.egg-info
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
