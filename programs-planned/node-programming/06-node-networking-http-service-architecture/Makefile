PYTHON ?= python3

.PHONY: install audit links source-audit investigations typecheck build test verify proof docs clean
install:
	npm install
audit:
	$(PYTHON) tools/audit.py
links:
	$(PYTHON) tools/check_links.py
source-audit:
	$(PYTHON) tools/check_ts_sources.py
investigations:
	$(PYTHON) tools/run_investigations.py
typecheck:
	$(PYTHON) tools/run_packages.py typecheck --jobs 2
build:
	$(PYTHON) tools/run_packages.py build --jobs 2
test:
	$(PYTHON) tools/run_packages.py test --jobs 2
verify:
	$(PYTHON) tools/proof.py --compatibility
proof:
	$(PYTHON) tools/proof.py
docs:
	mkdocs build --strict -f mkdocs.yml
clean:
	find . -type d \( -name dist -o -name site -o -name node_modules \) -prune -exec rm -rf {} +
