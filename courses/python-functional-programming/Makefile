# Makefile for funcpipe-rag

# ===== Basics =====
.PHONY: install test build lint clean clean-all venv \
        worktrees snapshots clean-history module-md module-funcpipe freeze-codebase \
        docs docs-deps docs-serve docs-build

.DEFAULT_GOAL := install

VENV       ?= .venv
PYTHON     ?= python3
VENV_PY    := $(VENV)/bin/python
VENV_PIP   := $(VENV)/bin/pip
RUFF       := $(VENV)/bin/ruff
MYPY       := $(VENV)/bin/mypy
PYTEST     := $(VENV)/bin/pytest
HATCH      := $(VENV)/bin/hatch
MKDOCS     := $(VENV)/bin/mkdocs

$(VENV_PY):
	$(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install -U pip

venv: $(VENV_PY)

install: venv
	$(VENV_PIP) install -e '.[dev]'

test: venv
	$(PYTEST) -q

build: venv
	$(HATCH) build

lint: venv
	$(RUFF) check src tests
	$(MYPY) --strict src/funcpipe_rag

docs-deps: venv
	$(VENV_PIP) install -e '.[docs]'

docs: docs-build

docs-build: docs-deps
	$(MKDOCS) build --strict

docs-serve: docs-deps
	$(MKDOCS) serve

clean:
	rm -rf dist build *.egg-info \
		.pytest_cache .mypy_cache .ruff_cache .hypothesis .benchmarks \
		$(VENV)

clean-all: clean
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
HISTORY_DIR   := history
WORKTREES_DIR := $(HISTORY_DIR)/worktrees
SNAPSHOTS_DIR := $(HISTORY_DIR)/snapshots
FREEZE_OUT    ?= all-cores/funcpipe-rag-all-code.md

# Export src + tests from each tag into history/snapshots/module-XX/
snapshots:
	@set -e; \
	mkdir -p "$(SNAPSHOTS_DIR)"; \
	for m in $(MODULES); do \
		tag="module-$$m"; \
		if git rev-parse -q --verify "refs/tags/$$tag" >/dev/null; then \
			dest="$(SNAPSHOTS_DIR)/$$tag"; \
			echo ">> Generating snapshot $$dest from $$tag"; \
			rm -rf "$$dest"; \
			mkdir -p "$$dest"; \
			git archive "$$tag" src tests | tar -x -C "$$dest"; \
		else \
			echo "!! Warning: Missing tag $$tag (skipping snapshot)"; \
		fi; \
	done

# (optional) handy alias
snapshot: snapshots

# Create detached worktrees at module tags (if you still want this)
worktrees:
	@mkdir -p "$(WORKTREES_DIR)"; \
	for m in $(MODULES); do \
		tag="module-$$m"; \
		dir="$(WORKTREES_DIR)/$$tag"; \
		if git rev-parse -q --verify "refs/tags/$$tag" >/dev/null; then \
			if [ ! -d "$$dir" ]; then \
				echo ">> Creating worktree $$dir @ $$tag"; \
				git worktree add --detach "$$dir" "$$tag"; \
			else \
				echo "== Worktree exists: $$dir (already there)"; \
			fi; \
		else \
			echo "!! Warning: Missing tag $$tag (skipping worktree)"; \
		fi; \
	done

clean-history:
	@rm -rf "$(WORKTREES_DIR)" "$(SNAPSHOTS_DIR)"; \
	git worktree prune

# Concatenate all core markdowns per module into all-cores/
# Supports:
#   1) legacy:  module-01/module-01-md/core-*.md
#   2) flat:    module-01/M01C01.md ... M01C10.md
module-md:
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


# Freeze each snapshot module (history/snapshots/module-XX) into all-cores/
module-funcpipe: snapshots
	@set -e; \
	mkdir -p all-cores; \
	for base in history/snapshots/module-[0-9][0-9]; do \
		if [ -d "$$base" ]; then \
			num="$${base##*/module-}"; \
			out="all-cores/funcpipe-rag-all-code-module-$$num-snapshot.md"; \
			echo ">> $$out"; \
			{ \
				echo "# funcpipe-rag snapshot module $$num"; \
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


freeze-codebase:
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
