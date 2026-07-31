.PHONY: program-help
program-help: ## Show the selected program's Make targets
	@$(RUN_PROGRAM) help

.PHONY: program-docs-build
program-docs-build: series-docs-install ## Build docs for the selected program
	@cd $(PROGRAM_DIR) && $(DOCS_ENV) $(MKDOCS) build -f mkdocs.yml --strict

.PHONY: program-docs-serve
program-docs-serve: series-docs-install ## Serve docs for the selected program
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(PROGRAM_DIR)/mkdocs.yml)

.PHONY: test
test: ## Run tests for the selected program
	@$(RUN_PROGRAM) test

.PHONY: capstone-test
capstone-test: ## Run the selected program's capstone test suite
	@$(RUN_PROGRAM) capstone-test

.PHONY: capstone-foundation-proof
capstone-foundation-proof: ## Run the selected program's smallest cumulative capstone proof
	@$(RUN_PROGRAM) capstone-foundation-proof

.PHONY: capstone-foundation-types
capstone-foundation-types: ## Check the selected program's first typed capstone state
	@$(RUN_PROGRAM) capstone-foundation-types

.PHONY: capstone-shell-proof
capstone-shell-proof: ## Run the selected program's first boundary proof
	@$(RUN_PROGRAM) capstone-shell-proof

.PHONY: capstone-data-api-proof
capstone-data-api-proof: ## Run the selected program's data-first API proof
	@$(RUN_PROGRAM) capstone-data-api-proof

.PHONY: capstone-data-shell-proof
capstone-data-shell-proof: ## Run the selected program's Result-bearing filesystem proof
	@$(RUN_PROGRAM) capstone-data-shell-proof

.PHONY: capstone-streaming-rag-proof
capstone-streaming-rag-proof: ## Run the selected program's complete streaming RAG proof
	@$(RUN_PROGRAM) capstone-streaming-rag-proof

.PHONY: capstone-source-scheduling-proof
capstone-source-scheduling-proof: ## Run the selected program's multi-source RAG scheduling proof
	@$(RUN_PROGRAM) capstone-source-scheduling-proof

.PHONY: demo
demo: ## Run the selected program's learner-facing capstone walkthrough
	@$(RUN_PROGRAM) demo

.PHONY: inspect
inspect: ## Inspect the selected program's learner-facing capstone state
	@$(RUN_PROGRAM) inspect

.PHONY: proof
proof: ## Run the selected program's strongest learner-facing proof route
	@$(RUN_PROGRAM) proof

.PHONY: history-refresh
history-refresh: ## Build the selected program's generated module history worktrees
	@$(RUN_PROGRAM) history-refresh

.PHONY: history-verify
history-verify: ## Verify the selected program's generated module history
	@$(RUN_PROGRAM) history-verify

.PHONY: history-clean
history-clean: ## Remove the selected program's generated module history worktrees
	@$(RUN_PROGRAM) history-clean

.PHONY: history-freeze-code
history-freeze-code: ## Freeze the selected program's generated module history worktrees
	@$(RUN_PROGRAM) history-freeze-code

.PHONY: capstone-walkthrough
capstone-walkthrough: ## Run the selected program's learner-facing capstone walkthrough
	@$(RUN_PROGRAM) capstone-walkthrough

.PHONY: capstone-tour
capstone-tour: ## Run the selected program's learner-facing capstone tour
	@$(RUN_PROGRAM) capstone-tour

.PHONY: capstone-governance
capstone-governance: ## Review the selected program's accepted, constrained, and rejected powers
	@$(RUN_PROGRAM) --no-print-directory capstone-governance

.PHONY: capstone-platform-report
capstone-platform-report: ## Print the selected program's supported toolchain versions
	@$(RUN_PROGRAM) capstone-platform-report

.PHONY: capstone-repro
capstone-repro: ## Execute the selected program's capstone pipeline
	@$(RUN_PROGRAM) capstone-repro

.PHONY: capstone-state-summary
capstone-state-summary: ## Render the selected program's capstone state summary
	@$(RUN_PROGRAM) capstone-state-summary

.PHONY: capstone-validate-config
capstone-validate-config: ## Validate the selected program's capstone configuration
	@$(RUN_PROGRAM) capstone-validate-config

.PHONY: capstone-wf-dryrun
capstone-wf-dryrun: ## Print the selected program's capstone dry-run plan
	@$(RUN_PROGRAM) capstone-wf-dryrun

.PHONY: capstone-bootstrap-confirm
capstone-bootstrap-confirm: ## Create the selected program's capstone toolchain and run clean-room confirmation
	@$(RUN_PROGRAM) capstone-bootstrap-confirm

.PHONY: capstone-selftest
capstone-selftest: ## Run the selected program's capstone determinism or convergence self-test
	@$(RUN_PROGRAM) capstone-selftest

.PHONY: capstone-contract-audit
capstone-contract-audit: ## Build the selected program's capstone public-contract audit bundle
	@$(RUN_PROGRAM) capstone-contract-audit

.PHONY: capstone-incident-audit
capstone-incident-audit: ## Build the selected program's capstone incident review bundle
	@$(RUN_PROGRAM) capstone-incident-audit

.PHONY: capstone-verify-report
capstone-verify-report: ## Build the selected program's capstone verification report bundle
	@$(RUN_PROGRAM) capstone-verify-report

.PHONY: capstone-verify-artifacts
capstone-verify-artifacts: ## Verify the selected program's published capstone artifacts
	@$(RUN_PROGRAM) capstone-verify-artifacts

.PHONY: capstone-release-audit
capstone-release-audit: ## Build the selected program's capstone release audit bundle
	@$(RUN_PROGRAM) capstone-release-audit

.PHONY: capstone-release-review
capstone-release-review: ## Build the selected program's capstone release review bundle
	@$(RUN_PROGRAM) capstone-release-review

.PHONY: capstone-release-check
capstone-release-check: ## Build and accept the selected program's local release candidate
	@$(RUN_PROGRAM) capstone-release-check

.PHONY: capstone-recovery-audit
capstone-recovery-audit: ## Build the selected program's capstone recovery audit bundle
	@$(RUN_PROGRAM) capstone-recovery-audit

.PHONY: capstone-recovery-drill
capstone-recovery-drill: ## Run the selected program's capstone recovery drill
	@$(RUN_PROGRAM) capstone-recovery-drill

.PHONY: capstone-recovery-review
capstone-recovery-review: ## Build the selected program's capstone recovery review bundle
	@$(RUN_PROGRAM) capstone-recovery-review

.PHONY: capstone-experiment-review
capstone-experiment-review: ## Build the selected program's capstone experiment review bundle
	@$(RUN_PROGRAM) capstone-experiment-review

.PHONY: capstone-profile-audit
capstone-profile-audit: ## Build the selected program's capstone execution-policy audit bundle
	@$(RUN_PROGRAM) capstone-profile-audit

.PHONY: capstone-performance-diagnostics-audit
capstone-performance-diagnostics-audit: ## Classify selected program performance evidence
	@$(RUN_PROGRAM) capstone-performance-diagnostics-audit

.PHONY: capstone-performance-diagnostics-selftest
capstone-performance-diagnostics-selftest: ## Reject dishonest selected program performance evidence
	@$(RUN_PROGRAM) capstone-performance-diagnostics-selftest

.PHONY: capstone-scheduler-policy-audit
capstone-scheduler-policy-audit: ## Record selected program scheduler policy evidence
	@$(RUN_PROGRAM) capstone-scheduler-policy-audit

.PHONY: capstone-scheduler-policy-selftest
capstone-scheduler-policy-selftest: ## Reject unsafe selected program scheduler mappings
	@$(RUN_PROGRAM) capstone-scheduler-policy-selftest

.PHONY: capstone-file-contract-audit
capstone-file-contract-audit: ## Classify selected program file contract evidence
	@$(RUN_PROGRAM) capstone-file-contract-audit

.PHONY: capstone-file-contract-selftest
capstone-file-contract-selftest: ## Reject dishonest selected program file contract evidence
	@$(RUN_PROGRAM) capstone-file-contract-selftest

.PHONY: capstone-stage-contract-audit
capstone-stage-contract-audit: ## Classify selected program stage contract evidence
	@$(RUN_PROGRAM) capstone-stage-contract-audit

.PHONY: capstone-stage-contract-selftest
capstone-stage-contract-selftest: ## Reject dishonest selected program stage contract evidence
	@$(RUN_PROGRAM) capstone-stage-contract-selftest

.PHONY: capstone-data-identity-audit
capstone-data-identity-audit: ## Classify selected program data identity evidence
	@$(RUN_PROGRAM) capstone-data-identity-audit

.PHONY: capstone-data-identity-selftest
capstone-data-identity-selftest: ## Enforce selected program data identity evidence
	@$(RUN_PROGRAM) capstone-data-identity-selftest

.PHONY: capstone-runtime-contract-audit
capstone-runtime-contract-audit: ## Classify selected program runtime contract evidence
	@$(RUN_PROGRAM) capstone-runtime-contract-audit

.PHONY: capstone-runtime-contract-selftest
capstone-runtime-contract-selftest: ## Enforce selected program runtime contract evidence
	@$(RUN_PROGRAM) capstone-runtime-contract-selftest

.PHONY: capstone-metric-contract-audit
capstone-metric-contract-audit: ## Classify selected program metric comparison evidence
	@$(RUN_PROGRAM) capstone-metric-contract-audit

.PHONY: capstone-metric-contract-selftest
capstone-metric-contract-selftest: ## Enforce selected program metric comparison evidence
	@$(RUN_PROGRAM) capstone-metric-contract-selftest

.PHONY: capstone-experiment-comparability-audit
capstone-experiment-comparability-audit: ## Classify selected program experiment comparison evidence
	@$(RUN_PROGRAM) capstone-experiment-comparability-audit

.PHONY: capstone-experiment-comparability-selftest
capstone-experiment-comparability-selftest: ## Enforce selected program experiment decision evidence
	@$(RUN_PROGRAM) capstone-experiment-comparability-selftest

.PHONY: capstone-reviewer-handoff-audit
capstone-reviewer-handoff-audit: ## Classify selected program reviewer handoff evidence
	@$(RUN_PROGRAM) capstone-reviewer-handoff-audit

.PHONY: capstone-reviewer-handoff-selftest
capstone-reviewer-handoff-selftest: ## Enforce selected program reviewer handoff evidence
	@$(RUN_PROGRAM) capstone-reviewer-handoff-selftest

.PHONY: capstone-recovery-readiness-audit
capstone-recovery-readiness-audit: ## Classify selected program recovery cutover evidence
	@$(RUN_PROGRAM) capstone-recovery-readiness-audit

.PHONY: capstone-recovery-readiness-selftest
capstone-recovery-readiness-selftest: ## Enforce selected program recovery cutover evidence
	@$(RUN_PROGRAM) capstone-recovery-readiness-selftest

.PHONY: capstone-promotion-integrity-audit
capstone-promotion-integrity-audit: ## Classify selected program promotion integrity evidence
	@$(RUN_PROGRAM) capstone-promotion-integrity-audit

.PHONY: capstone-promotion-integrity-selftest
capstone-promotion-integrity-selftest: ## Enforce selected program promotion integrity evidence
	@$(RUN_PROGRAM) capstone-promotion-integrity-selftest

.PHONY: capstone-boundary-migration-audit
capstone-boundary-migration-audit: ## Classify selected program boundary cutover evidence
	@$(RUN_PROGRAM) capstone-boundary-migration-audit

.PHONY: capstone-boundary-migration-selftest
capstone-boundary-migration-selftest: ## Enforce selected program boundary cutover evidence
	@$(RUN_PROGRAM) capstone-boundary-migration-selftest

.PHONY: capstone-workflow-evidence-audit
capstone-workflow-evidence-audit: ## Classify selected program workflow evidence
	@$(RUN_PROGRAM) capstone-workflow-evidence-audit

.PHONY: capstone-workflow-evidence-selftest
capstone-workflow-evidence-selftest: ## Enforce selected program workflow evidence
	@$(RUN_PROGRAM) capstone-workflow-evidence-selftest

.PHONY: capstone-discovery-audit
capstone-discovery-audit: ## Build the selected program's capstone discovery audit bundle
	@$(RUN_PROGRAM) capstone-discovery-audit

.PHONY: capstone-portability-audit
capstone-portability-audit: ## Build the selected program's capstone portability audit bundle
	@$(RUN_PROGRAM) capstone-portability-audit

.PHONY: capstone-source-bundle
capstone-source-bundle: ## Build the selected program's tracked-source capstone bundle
	@$(RUN_PROGRAM) capstone-source-bundle

.PHONY: capstone-verify
capstone-verify: ## Run the selected program's capstone contract verification
	@$(RUN_PROGRAM) capstone-verify

.PHONY: capstone-confirm
capstone-confirm: ## Run the selected program's strongest capstone confirmation route
	@$(RUN_PROGRAM) capstone-confirm

.PHONY: clean
clean: ## Run clean for the selected program
	@$(RUN_PROGRAM) clean
