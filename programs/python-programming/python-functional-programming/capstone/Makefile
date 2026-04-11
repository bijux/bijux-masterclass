# Makefile for funcpipe-rag

# ===== Basics =====
.PHONY: install test build lint clean clean-all venv rebuild-venv demo inspect verify-report tour proof confirm \
        history-refresh history-verify history-clean history-freeze-code module-md freeze-codebase \
        help

.DEFAULT_GOAL := install

ARTIFACTS_DIR ?= ../../../../artifacts
DOCS_DIR   := docs
VENV       ?= $(ARTIFACTS_DIR)/venv/python-programming/python-functional-programming/capstone
PYTHON     ?= $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null)
VENV_PY    := $(VENV)/bin/python
VENV_PIP   := $(VENV_PY) -m pip
RUFF       := $(VENV)/bin/ruff
MYPY       := $(VENV)/bin/mypy
PYTEST     := $(VENV)/bin/pytest
HATCH      := $(VENV)/bin/hatch
TOUR_DIR   ?= $(ARTIFACTS_DIR)/tour/python-programming/python-functional-programming
INSPECT_DIR ?= $(ARTIFACTS_DIR)/inspect/python-programming/python-functional-programming
VERIFY_REPORT_DIR ?= $(ARTIFACTS_DIR)/review/python-programming/python-functional-programming

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"; printf "\nTargets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

$(VENV_PY):
	$(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install -U pip

venv: $(VENV_PY) ## Create the local virtual environment

rebuild-venv: ## Recreate the local virtual environment in place
	$(PYTHON) -m venv --clear $(VENV)
	$(VENV_PIP) install -U pip

install: venv ## Install development dependencies
	@set -e; \
	$(VENV_PIP) install -e '.[dev]' || { \
		$(MAKE) rebuild-venv; \
		$(VENV_PIP) install -e '.[dev]'; \
	}; \
	test -x $(RUFF) && test -x $(MYPY) && test -x $(PYTEST) && test -x $(HATCH) || { \
		$(MAKE) rebuild-venv; \
		$(VENV_PIP) install -e '.[dev]'; \
	}

test: install ## Run the test suite
	$(PYTEST) -q

demo: tour ## Build the learner-facing capstone walkthrough

inspect: install ## Build the learner-facing inspection bundle
	rm -rf $(INSPECT_DIR)
	mkdir -p $(INSPECT_DIR) $(INSPECT_DIR)/docs
	$(VENV)/bin/funcpipe-rag-review summary --format text --project-root . > $(INSPECT_DIR)/summary.txt
	$(VENV)/bin/funcpipe-rag-review summary --format json --project-root . > $(INSPECT_DIR)/summary.json
	cp README.md $(INSPECT_DIR)/README.md
	for doc in INDEX.md COMMAND_GUIDE.md ARCHITECTURE.md EXTENSION_GUIDE.md PACKAGE_GUIDE.md PROOF_GUIDE.md PUBLIC_SURFACE_MAP.md TEST_GUIDE.md TOUR.md WALKTHROUGH_GUIDE.md; do \
		cp $(DOCS_DIR)/$$doc $(INSPECT_DIR)/$$doc; \
		cp $(DOCS_DIR)/$$doc $(INSPECT_DIR)/docs/$$doc; \
	done
	printf '%s\n' \
		'Inspection route:' \
		'  1. Read summary.txt for the human review map.' \
		'  2. Read summary.json for the machine-readable package and test groups.' \
		'  3. Read INDEX.md, PACKAGE_GUIDE.md, and TEST_GUIDE.md for the local reading routes.' \
		'  4. Read PUBLIC_SURFACE_MAP.md and PROOF_GUIDE.md when you need ownership and route depth.' \
		'  5. Read ARCHITECTURE.md when you need the broader package map.' \
		> $(INSPECT_DIR)/route.txt
	$(PYTHON) scripts/write_bundle_manifest.py --bundle-dir $(INSPECT_DIR) --output $(INSPECT_DIR)/manifest.json
	@echo "✔ wrote learner-facing inspection bundle to $(INSPECT_DIR)"

verify-report: install ## Build the structured capstone verification report bundle
	rm -rf $(VERIFY_REPORT_DIR)
	mkdir -p $(VERIFY_REPORT_DIR) $(VERIFY_REPORT_DIR)/docs
	$(PYTEST) -q 2>&1 | tee $(VERIFY_REPORT_DIR)/pytest.txt
	$(VENV)/bin/funcpipe-rag-review summary --format json --project-root . > $(VERIFY_REPORT_DIR)/review-summary.json
	$(VENV)/bin/funcpipe-rag-review summary --format text --project-root . > $(VERIFY_REPORT_DIR)/review-summary.txt
	cp README.md $(VERIFY_REPORT_DIR)/README.md
	for doc in ARCHITECTURE.md COMMAND_GUIDE.md EXTENSION_GUIDE.md INDEX.md PACKAGE_GUIDE.md PROOF_GUIDE.md PUBLIC_SURFACE_MAP.md TEST_GUIDE.md TOUR.md WALKTHROUGH_GUIDE.md; do \
		cp $(DOCS_DIR)/$$doc $(VERIFY_REPORT_DIR)/$$doc; \
		cp $(DOCS_DIR)/$$doc $(VERIFY_REPORT_DIR)/docs/$$doc; \
	done
	printf '%s\n' \
		'Verification report route:' \
		'  1. Read pytest.txt for the executed verification result.' \
		'  2. Read review-summary.txt for the package, test, and route inventory.' \
		'  3. Read INDEX.md, PROOF_GUIDE.md, and TEST_GUIDE.md when you need claim-to-evidence routing.' \
		'  4. Read PUBLIC_SURFACE_MAP.md when you need to connect the saved artifact back to the published routes.' \
		'  5. Read WALKTHROUGH_GUIDE.md and TOUR.md when you want the matching human review order.' \
		> $(VERIFY_REPORT_DIR)/route.txt
	$(PYTHON) scripts/write_bundle_manifest.py --bundle-dir $(VERIFY_REPORT_DIR) --output $(VERIFY_REPORT_DIR)/manifest.json
	@echo "✔ wrote capstone verification report to $(VERIFY_REPORT_DIR)"

tour: install ## Build the learner-facing proof bundle
	rm -rf $(TOUR_DIR)
	mkdir -p $(TOUR_DIR) $(TOUR_DIR)/docs
	$(PYTEST) -q 2>&1 | tee $(TOUR_DIR)/pytest.txt
	find src/funcpipe_rag -type d | sort > $(TOUR_DIR)/package-tree.txt
	find tests -type d | sort > $(TOUR_DIR)/test-tree.txt
	cp README.md $(TOUR_DIR)/README.md
	cp pyproject.toml $(TOUR_DIR)/pyproject.toml
	for doc in ARCHITECTURE.md COMMAND_GUIDE.md EXTENSION_GUIDE.md INDEX.md PACKAGE_GUIDE.md PROOF_GUIDE.md PUBLIC_SURFACE_MAP.md TEST_GUIDE.md TOUR.md WALKTHROUGH_GUIDE.md; do \
		cp $(DOCS_DIR)/$$doc $(TOUR_DIR)/$$doc; \
		cp $(DOCS_DIR)/$$doc $(TOUR_DIR)/docs/$$doc; \
	done
	printf '%s\n' \
		"core=src/funcpipe_rag/core" \
		"result=src/funcpipe_rag/result" \
		"boundaries=src/funcpipe_rag/boundaries" \
		"async_effects=src/funcpipe_rag/domain/effects/async_" \
		"tests=tests/unit" \
		> $(TOUR_DIR)/focus-areas.txt
	$(PYTHON) scripts/write_bundle_manifest.py --bundle-dir $(TOUR_DIR) --output $(TOUR_DIR)/manifest.json
	printf '%s\n' \
		'Tour route:' \
		'  1. Read package-tree.txt and test-tree.txt for the repository shape.' \
		'  2. Read focus-areas.txt for the highest-signal package groups.' \
		'  3. Read TOUR.md and WALKTHROUGH_GUIDE.md for the human reading order.' \
		'  4. Read PUBLIC_SURFACE_MAP.md and PROOF_GUIDE.md when you need to connect the walkthrough back to commands and proof groups.' \
		'  5. Read TEST_GUIDE.md when the current pressure is clearer than the route itself.' \
		> $(TOUR_DIR)/route.txt
	@echo "✔ wrote learner-facing tour to $(TOUR_DIR)"

proof: test inspect tour ## Run the sanctioned learner-facing proof route

confirm: lint build verify-report proof ## Run the strongest capstone confirmation route

build: install ## Build distribution artifacts
	$(HATCH) build

lint: install ## Run linting and type checks
	$(RUFF) check src tests
	$(MYPY) --strict src/funcpipe_rag

clean: ## Remove build and virtualenv artifacts
	rm -rf dist build *.egg-info \
		.pytest_cache .mypy_cache .ruff_cache .hypothesis .benchmarks \
		$(VENV)

clean-all: clean ## Remove additional generated caches
	find . -type d \( \
		-name "__pycache__" -o \
		-name ".pytest_cache" -o \
		-name ".mypy_cache" -o \
		-name ".ruff_cache" -o \
		-name ".hypothesis" -o \
		-name ".venv" \
	\) -prune -exec rm -rf {} +


# ===== Git history utilities =====

MODULES       := 01 02 03 04 05 06 07 08 09 10
HISTORY_DIR   := _history
WORKTREES_DIR := $(HISTORY_DIR)/worktrees
FREEZE_OUT    ?= all-cores/funcpipe-rag-all-code.md

history-refresh: ## Build local module tags and generated worktrees under _history
	$(PYTHON) scripts/build_module_history.py --out-dir $(HISTORY_DIR)

history-verify: ## Verify generated module worktrees against the tracked snapshot sources
	$(PYTHON) scripts/build_module_history.py --out-dir $(HISTORY_DIR) --verify-only

history-clean: ## Remove generated module history worktrees and metadata
	@rm -rf "$(HISTORY_DIR)"; \
	for tag in $$(git tag --list 'python-functional-programming-module-*'); do \
		git tag -d "$$tag" >/dev/null; \
	done; \
	git update-ref -d refs/heads/python-functional-programming-history 2>/dev/null || true; \
	git worktree prune

# Concatenate all core markdowns per module into all-cores/
# Supports:
#   1) legacy:  module-01/module-01-md/core-*.md
#   2) flat:    module-01/M01C01.md ... M01C10.md
module-md: ## Concatenate module markdown sources into all-cores
	@set -e; \
	parent_dir="."; \
	out_dir="$$parent_dir/all-cores"; \
	mkdir -p "$$out_dir"; \
	for mod in "$$parent_dir"/course-book/module-[0-9][0-9]; do \
		if [ ! -d "$$mod" ]; then \
			continue; \
		fi; \
		mod_name=`basename "$$mod"`; \
		legacy_dir="$$mod/$$mod_name-md"; \
		if [ -d "$$legacy_dir" ]; then \
			out="$$out_dir/cores-$$mod_name.md"; \
			echo ">> $$out (legacy layout: $$legacy_dir/core-*.md)"; \
			cat "$$legacy_dir"/core-*.md > "$$out"; \
			continue; \
		fi; \
		set -- "$$mod"/M??C??.md; \
		if [ -e "$$1" ]; then \
			out="$$out_dir/cores-$$mod_name.md"; \
			echo ">> $$out (flat layout: $$mod/M??C??.md)"; \
			cat "$$mod"/M??C??.md > "$$out"; \
		else \
			echo "!! Skipping $$mod_name (no legacy dir and no MxxCxx markdown files)"; \
		fi; \
	done


# Freeze each generated module worktree (_history/worktrees/module-XX) into all-cores/
history-freeze-code: history-refresh ## Freeze generated module worktrees into all-cores markdown bundles
	@set -e; \
	mkdir -p all-cores; \
	for base in _history/worktrees/module-[0-9][0-9]; do \
		if [ -d "$$base" ]; then \
			num="$${base##*/module-}"; \
			out="all-cores/funcpipe-rag-all-code-module-$$num-reference-state.md"; \
			echo ">> $$out"; \
			{ \
				echo "# funcpipe-rag module $$num reference state"; \
				echo; \
				echo "## Tree (src and tests)"; \
				echo '```text'; \
				if command -v tree >/dev/null 2>&1; then \
					( cd "$$base" && tree -a -I ".git|.venv|__pycache__|.mypy_cache|.pytest_cache|.ruff_cache|.hypothesis|*.egg-info|.DS_Store" src tests 2>/dev/null || true ); \
				else \
					( cd "$$base" && \
					  find src tests \
						-type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" -o -name ".ruff_cache" -o -name ".hypothesis" \) -prune -o \
						-type f ! -name ".DS_Store" ! -name "*.pyc" -print 2>/dev/null | sort || true ); \
				fi; \
				echo '```'; \
				echo; \
				if [ -f "$$base/README.md" ]; then \
					echo "## README.md"; \
					echo '```markdown'; \
					cat "$$base/README.md"; \
					echo '```'; \
					echo; \
				fi; \
				if [ -f "$$base/pyproject.toml" ]; then \
					echo "## pyproject.toml"; \
					echo '```toml'; \
					cat "$$base/pyproject.toml"; \
					echo '```'; \
					echo; \
				fi; \
				for dir in src tests; do \
					if [ -d "$$base/$$dir" ]; then \
						( cd "$$base" && \
						  find "$$dir" \
							-type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" -o -name ".ruff_cache" -o -name ".hypothesis" \) -prune -o \
							-type f ! -name "*.pyc" ! -name ".DS_Store" -print | sort | \
						  while IFS= read -r f; do \
							ext="$${f##*.}"; lang="text"; \
							case "$$ext" in \
								py)   lang="python" ;; \
								md)   lang="markdown" ;; \
								toml) lang="toml" ;; \
								sh)   lang="bash" ;; \
								yml|yaml) lang="yaml" ;; \
							esac; \
							echo "## $$f"; \
							echo '```'$$lang; \
							cat "$$f"; \
							echo '```'; \
							echo; \
						  done ); \
					fi; \
				done; \
			} > "$$out"; \
		else \
			echo "!! Skipping $$base (not a dir)"; \
		fi; \
	done


freeze-codebase: ## Export the current codebase into a markdown bundle
	@set -e; \
	out="$(FREEZE_OUT)"; \
	echo ">> $$out"; \
	mkdir -p "$$(dirname "$$out")"; \
	{ \
		echo "# funcpipe-rag codebase freeze"; \
		echo; \
		echo "## Tree (src and tests)"; \
		echo '```text'; \
		if command -v tree >/dev/null 2>&1; then \
			tree -a -I ".git|.venv|__pycache__|.mypy_cache|.pytest_cache|.ruff_cache|.hypothesis|*.egg-info|.DS_Store" src tests; \
		else \
			( \
				find src tests \
					-type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" -o -name ".ruff_cache" \) -prune -o \
					-type f ! -name ".DS_Store" ! -name "*.pyc" -print \
			); \
		fi; \
		echo '```'; \
		echo; \
		if [ -f README.md ]; then \
			echo "## README.md"; \
			echo '```markdown'; \
			cat README.md; \
			echo '```'; \
			echo; \
		fi; \
		if [ -f pyproject.toml ]; then \
			echo "## pyproject.toml"; \
			echo '```toml'; \
			cat pyproject.toml; \
			echo '```'; \
			echo; \
		fi; \
		for dir in src tests; do \
			if [ -d "$$dir" ]; then \
				find "$$dir" \
					-type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" -o -name ".ruff_cache" \) -prune -o \
					-type f ! -name "*.pyc" ! -name ".DS_Store" -print | sort | \
				while IFS= read -r f; do \
					ext="$${f##*.}"; \
					lang="text"; \
					case "$$ext" in \
						py)   lang="python" ;; \
						md)   lang="markdown" ;; \
						toml) lang="toml" ;; \
						sh)   lang="bash" ;; \
						yml|yaml) lang="yaml" ;; \
					esac; \
					echo "## $$f"; \
					echo '```'$$lang; \
					cat "$$f"; \
					echo '```'; \
					echo; \
				done; \
			fi; \
		done; \
	} > "$$out"
