SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

CAPSTONE_DIR := capstone
RUN_CAPSTONE = tool=make; if command -v gmake >/dev/null 2>&1; then tool=gmake; fi; $$tool -C $(CAPSTONE_DIR)
ARTIFACTS_DIR ?= ../../../artifacts
SITE_DIR ?= $(ARTIFACTS_DIR)/site/reproducible-research/deep-dive-dvc
COURSE_VENV_DIR ?= $(ARTIFACTS_DIR)/venv/reproducible-research/deep-dive-dvc

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run the capstone confirmation suite
	@$(RUN_CAPSTONE) confirm

.PHONY: capstone-tour
capstone-tour: ## Build the learner-facing capstone proof bundle
	@$(RUN_CAPSTONE) tour

.PHONY: capstone-platform-report
capstone-platform-report: ## Print the supported Python, Git, and DVC versions
	@$(RUN_CAPSTONE) platform-report

.PHONY: capstone-repro
capstone-repro: ## Execute the capstone DVC pipeline
	@$(RUN_CAPSTONE) repro

.PHONY: capstone-verify-report
capstone-verify-report: ## Build the capstone verification report bundle
	@$(RUN_CAPSTONE) verify-report

.PHONY: capstone-state-summary
capstone-state-summary: ## Render a combined declaration, execution, and release summary
	@$(RUN_CAPSTONE) state-summary

.PHONY: capstone-release-summary
capstone-release-summary: ## Render the promoted release summary
	@$(RUN_CAPSTONE) release-summary

.PHONY: capstone-review-queue
capstone-review-queue: ## Render the structured prediction review queue
	@$(RUN_CAPSTONE) review-queue

.PHONY: capstone-verify
capstone-verify: ## Run the capstone contract verification route
	@$(RUN_CAPSTONE) verify

.PHONY: capstone-confirm
capstone-confirm: ## Run the capstone's strongest confirmation route
	@$(RUN_CAPSTONE) confirm

.PHONY: capstone-walkthrough
capstone-walkthrough: ## Build the learner-facing capstone walkthrough bundle
	@$(RUN_CAPSTONE) walkthrough

.PHONY: capstone-release-audit
capstone-release-audit: ## Build the capstone release-boundary audit bundle
	@$(RUN_CAPSTONE) release-audit

.PHONY: capstone-release-review
capstone-release-review: ## Build the capstone release review bundle
	@$(RUN_CAPSTONE) release-review

.PHONY: capstone-recovery-audit
capstone-recovery-audit: ## Build the capstone remote-recovery audit bundle
	@$(RUN_CAPSTONE) recovery-audit

.PHONY: capstone-recovery-drill
capstone-recovery-drill: ## Rebuild the workspace from the remote after cache loss
	@$(RUN_CAPSTONE) recovery-drill

.PHONY: capstone-recovery-review
capstone-recovery-review: ## Build the capstone remote recovery review bundle
	@$(RUN_CAPSTONE) recovery-review

.PHONY: capstone-recovery-readiness-audit
capstone-recovery-readiness-audit: ## Audit protected revisions before remote cutover
	@$(RUN_CAPSTONE) recovery-readiness-audit

.PHONY: capstone-recovery-readiness-selftest
capstone-recovery-readiness-selftest: ## Enforce recovery cutover evidence
	@$(RUN_CAPSTONE) recovery-readiness-selftest

.PHONY: capstone-promotion-integrity-audit
capstone-promotion-integrity-audit: ## Audit release identity, integrity, provenance, and approval
	@$(RUN_CAPSTONE) promotion-integrity-audit

.PHONY: capstone-promotion-integrity-selftest
capstone-promotion-integrity-selftest: ## Enforce promotion integrity decisions
	@$(RUN_CAPSTONE) promotion-integrity-selftest

.PHONY: capstone-boundary-migration-audit
capstone-boundary-migration-audit: ## Audit a governed consumer-boundary cutover
	@$(RUN_CAPSTONE) boundary-migration-audit

.PHONY: capstone-boundary-migration-selftest
capstone-boundary-migration-selftest: ## Enforce governed boundary cutover decisions
	@$(RUN_CAPSTONE) boundary-migration-selftest

.PHONY: capstone-experiment-review
capstone-experiment-review: ## Build the capstone experiment comparison bundle
	@$(RUN_CAPSTONE) experiment-review

.PHONY: capstone-stage-contract-audit
capstone-stage-contract-audit: ## Audit declared and hidden stage influences
	@$(RUN_CAPSTONE) stage-contract-audit

.PHONY: capstone-stage-contract-selftest
capstone-stage-contract-selftest: ## Reject dishonest stage contract evidence
	@$(RUN_CAPSTONE) stage-contract-selftest

.PHONY: capstone-data-identity-audit
capstone-data-identity-audit: ## Audit pointer, cache, workspace, and remote identity
	@$(RUN_CAPSTONE) data-identity-audit

.PHONY: capstone-data-identity-selftest
capstone-data-identity-selftest: ## Enforce data identity and recovery evidence
	@$(RUN_CAPSTONE) data-identity-selftest

.PHONY: capstone-runtime-contract-audit
capstone-runtime-contract-audit: ## Audit declared and hidden runtime influences
	@$(RUN_CAPSTONE) runtime-contract-audit

.PHONY: capstone-runtime-contract-selftest
capstone-runtime-contract-selftest: ## Enforce declared and hidden runtime evidence
	@$(RUN_CAPSTONE) runtime-contract-selftest

.PHONY: capstone-metric-contract-audit
capstone-metric-contract-audit: ## Audit metric semantic comparability
	@$(RUN_CAPSTONE) metric-contract-audit

.PHONY: capstone-metric-contract-selftest
capstone-metric-contract-selftest: ## Enforce metric semantic comparability evidence
	@$(RUN_CAPSTONE) metric-contract-selftest

.PHONY: capstone-experiment-comparability-audit
capstone-experiment-comparability-audit: ## Audit experiment comparison and promotion boundaries
	@$(RUN_CAPSTONE) experiment-comparability-audit

.PHONY: capstone-experiment-comparability-selftest
capstone-experiment-comparability-selftest: ## Enforce experiment comparison and promotion evidence
	@$(RUN_CAPSTONE) experiment-comparability-selftest

.PHONY: capstone-reviewer-handoff-audit
capstone-reviewer-handoff-audit: ## Audit clean reviewer handoff evidence
	@$(RUN_CAPSTONE) reviewer-handoff-audit

.PHONY: capstone-reviewer-handoff-selftest
capstone-reviewer-handoff-selftest: ## Enforce clean reviewer handoff evidence
	@$(RUN_CAPSTONE) reviewer-handoff-selftest

.PHONY: capstone-source-bundle
capstone-source-bundle: ## Build the capstone tracked-source release bundle
	@$(RUN_CAPSTONE) source-bundle

.PHONY: clean
clean: ## Remove build artifacts
	@rm -rf $(COURSE_VENV_DIR) $(SITE_DIR) .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@$(RUN_CAPSTONE) clean
