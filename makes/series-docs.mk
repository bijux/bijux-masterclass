DOCS_LOCK ?= configs/docs/requirements-docs.lock
DOCS_UV ?= uv
DOCS_PROFILE ?=
DOCS_VERIFICATION_PROFILE ?= darwin-arm64-cpython-314
DOCS_VERIFICATION_ENV ?= $(ARTIFACTS_DIR)/venv/catalog-verification
DOCS_VERIFICATION_INSTALL = $(PYTHON) -B scripts/docs_environment.py --root "$(CURDIR)" --python "$(PYTHON)" --environment "$(DOCS_VERIFICATION_ENV)" --lock "$(DOCS_LOCK)" --requirements "$(DOCS_REQUIREMENTS)" --uv "$(DOCS_UV)" --receipt "$(ARTIFACTS_DIR)/docs/verification-environment.json" --profile "$(DOCS_VERIFICATION_PROFILE)"

.PHONY: series-docs-verification-install
series-docs-verification-install: ## Install or validate the locked local documentation verification environment
	@$(DOCS_VERIFICATION_INSTALL)

.PHONY: series-docs-venv
series-docs-venv: ## Create the virtual environment for the series site
ifeq ($(strip $(DOCS_PROFILE)),)
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install -U pip
endif

.PHONY: series-docs-install
series-docs-install: series-docs-venv ## Install series documentation dependencies
ifeq ($(strip $(DOCS_PROFILE)),)
	@$(PIP) install -r $(DOCS_REQUIREMENTS)
else
	@$(PYTHON) -B scripts/docs_environment.py --root "$(CURDIR)" --python "$(PYTHON)" --environment "$(VENV_DIR)" --lock "$(DOCS_LOCK)" --requirements "$(DOCS_REQUIREMENTS)" --uv "$(DOCS_UV)" --receipt "$(ARTIFACTS_DIR)/docs/verification-environment.json" --profile "$(DOCS_PROFILE)"
endif

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
