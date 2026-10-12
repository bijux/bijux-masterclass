# Shared Bijux docs shell synchronization and contract enforcement.

PYTHON_BIN ?= $(shell command -v python3 2>/dev/null)
BIJUX_DOCS_SOURCE_SCRIPT ?= scripts/verify_docs_source.sh
BIJUX_DOCS_CONTRACT_GUARD ?= .bijux/shared/bijux-docs/tooling/quality/validate_bijux_docs_contract.py
BIJUX_DOCS_ARTIFACTS_DIR ?= $(ARTIFACTS_DIR)/bijux-docs
BIJUX_DOCS_LOG_DIR ?= $(BIJUX_DOCS_ARTIFACTS_DIR)/logs

.PHONY: bijux-docs-sync bijux-docs-check shell-sync shell-check

bijux-docs-sync: ## Synchronize shared Bijux docs shell into docs assets
	@env -u BIJUX_STD_ROOT -u BIJUX_STD_REF bash "$(BIJUX_DOCS_SOURCE_SCRIPT)" sync

bijux-docs-check: series-docs-install ## Validate Bijux docs shell contract and drift checks
	@mkdir -p "$(BIJUX_DOCS_LOG_DIR)"
	@bash -o pipefail -c '"$(VENV_PY)" "$(BIJUX_DOCS_CONTRACT_GUARD)" . 2>&1 | tee "$(BIJUX_DOCS_LOG_DIR)/contract.log"'
	@bash -o pipefail -c 'env -u BIJUX_STD_ROOT -u BIJUX_STD_REF bash "$(BIJUX_DOCS_SOURCE_SCRIPT)" check 2>&1 | tee "$(BIJUX_DOCS_LOG_DIR)/source-of-truth.log"'

# Backward-compatible aliases.
shell-sync: bijux-docs-sync ## Alias for bijux-docs-sync
shell-check: bijux-docs-check ## Alias for bijux-docs-check
