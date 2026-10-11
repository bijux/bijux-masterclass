DOCS_LOCK ?= configs/docs/requirements-docs.lock
DOCS_UV ?= uv
DOCS_VERIFICATION_ENV ?= $(ARTIFACTS_DIR)/venv/catalog-verification
DOCS_VERIFICATION_INSTALL = $(PYTHON) -B scripts/docs_environment.py --root "$(CURDIR)" --python "$(PYTHON)" --environment "$(DOCS_VERIFICATION_ENV)" --lock "$(DOCS_LOCK)" --requirements "$(DOCS_REQUIREMENTS)" --uv "$(DOCS_UV)" --receipt "$(ARTIFACTS_DIR)/docs/verification-environment.json"

.PHONY: series-docs-verification-install
series-docs-verification-install: ## Install or validate the locked local documentation verification environment
	@$(DOCS_VERIFICATION_INSTALL)

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
	@$(DOCS_ENV) $(VENV_PY) scripts/verify_catalog_site.py --config $(ROOT_MKDOCS_FILE) --output artifacts/docs/catalog-links.json

.PHONY: series-docs-serve
series-docs-serve: series-docs-install bijux-docs-sync ## Serve the series documentation site locally
	@$(SYNC_SERIES_DOCS)
	@$(RENDER_ROOT_MKDOCS)
	@$(DOCS_ENV) $(SERVE_DOCS) --config $(abspath $(ROOT_MKDOCS_FILE))
