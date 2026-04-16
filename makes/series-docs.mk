.PHONY: series-docs-venv
series-docs-venv: ## Create the virtual environment for the series site
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip

.PHONY: series-docs-install
series-docs-install: series-docs-venv ## Install series documentation dependencies
	@$(PIP) install -r $(DOCS_REQUIREMENTS)

.PHONY: series-docs-build
series-docs-build: series-docs-install bijux-docs-sync ## Build the series documentation site
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(MKDOCS) build -f $(ROOT_MKDOCS_FILE) --strict

.PHONY: series-docs-serve
series-docs-serve: series-docs-install bijux-docs-sync ## Serve the series documentation site locally
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(ROOT_MKDOCS_FILE))
