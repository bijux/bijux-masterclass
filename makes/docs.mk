BIJUX_DOCS_SYNC_SCRIPT ?= internal/scripts/sync_bijux_docs.sh
BIJUX_DOCS_SOT_GUARD ?= internal/scripts/verify_bijux_docs_source_of_truth.sh
BIJUX_DOCS_CONTRACT_GUARD ?= internal/quality/validate_bijux_docs_contract.py

.PHONY: bijux-docs-sync
bijux-docs-sync: ## Synchronize shared Bijux docs shell into docs assets
	@bash "$(BIJUX_DOCS_SYNC_SCRIPT)"

.PHONY: bijux-docs-check
bijux-docs-check: ## Validate Bijux docs shell contract and drift checks
	@"$(PYTHON_BIN)" "$(BIJUX_DOCS_CONTRACT_GUARD)" .
	@bash "$(BIJUX_DOCS_SOT_GUARD)"

.PHONY: docs-build
docs-build: series-docs-install bijux-docs-sync ## Build the full catalog, or one program if PROGRAM is set explicitly
ifeq ($(PROGRAM_IS_EXPLICIT),)
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(MKDOCS) build -f $(ROOT_MKDOCS_FILE) --strict
else
	@cd $(PROGRAM_DIR) && $(DOCS_ENV) $(MKDOCS) build -f mkdocs.yml --strict
endif

.PHONY: docs-serve
docs-serve: series-docs-install bijux-docs-sync ## Serve the full catalog, or one program if PROGRAM is set explicitly
ifeq ($(PROGRAM_IS_EXPLICIT),)
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(ROOT_MKDOCS_FILE))
else
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(PROGRAM_DIR)/mkdocs.yml)
endif

.PHONY: docs-audit
docs-audit: ## Audit course-book and capstone documentation rules
	@$(PYTHON) scripts/audit_masterclass_docs.py

.PHONY: docs-nav-check
docs-nav-check: series-docs-build bijux-docs-check ## Check rendered masterclass navigation rows
	@$(PYTHON) scripts/check_masterclass_navigation.py
	@$(PYTHON) scripts/check_masterclass_library_tree.py
	@$(PYTHON) scripts/check_masterclass_shell.py
