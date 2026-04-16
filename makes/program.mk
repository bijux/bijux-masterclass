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
