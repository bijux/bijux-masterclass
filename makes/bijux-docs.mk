# Shared Bijux docs shell synchronization and contract enforcement.

PYTHON_BIN ?= $(shell command -v python3 2>/dev/null)
BIJUX_DOCS_SYNC_SCRIPT ?= .bijux/shared/bijux-docs/tooling/scripts/sync_bijux_docs.sh
BIJUX_DOCS_SOT_GUARD ?= .bijux/shared/bijux-docs/tooling/scripts/verify_bijux_docs_source_of_truth.sh
BIJUX_DOCS_CONTRACT_GUARD ?= .bijux/shared/bijux-docs/tooling/quality/validate_bijux_docs_contract.py
BIJUX_DOCS_ARTIFACTS_DIR ?= $(ARTIFACTS_DIR)/bijux-docs
BIJUX_DOCS_LOG_DIR ?= $(BIJUX_DOCS_ARTIFACTS_DIR)/logs

.PHONY: bijux-docs-sync bijux-docs-check shell-sync shell-check

bijux-docs-sync: ## Synchronize shared Bijux docs shell into docs assets
	@bash "$(BIJUX_DOCS_SYNC_SCRIPT)"

bijux-docs-check: series-docs-install ## Validate Bijux docs shell contract and drift checks
	@mkdir -p "$(BIJUX_DOCS_LOG_DIR)"
	@"$(VENV_PY)" "$(BIJUX_DOCS_CONTRACT_GUARD)" . 2>&1 | tee "$(BIJUX_DOCS_LOG_DIR)/contract.log"
	@bash "$(BIJUX_DOCS_SOT_GUARD)" 2>&1 | tee "$(BIJUX_DOCS_LOG_DIR)/source-of-truth.log"

# Backward-compatible aliases.
shell-sync: bijux-docs-sync ## Alias for bijux-docs-sync
shell-check: bijux-docs-check ## Alias for bijux-docs-check
