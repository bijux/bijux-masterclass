PYTHON ?= python3

.PHONY: install docs-install audit links source-audit investigations typecheck build test docs verify proof clean
install:
	npm install

docs-install:
	$(PYTHON) -m pip install -r ../requirements-docs.txt

audit:
	$(PYTHON) tools/audit.py

links:
	$(PYTHON) tools/check_links.py

source-audit:
	$(PYTHON) tools/check_ts_sources.py

investigations:
	$(PYTHON) tools/run_investigations.py

typecheck:
	$(PYTHON) tools/run_packages.py typecheck

build:
	$(PYTHON) tools/run_packages.py build

test:
	$(PYTHON) tools/run_packages.py test

docs:
	mkdocs build --strict -f mkdocs.yml

verify:
	$(PYTHON) tools/proof.py --compatibility

proof:
	$(PYTHON) tools/proof.py

clean:
	find . -type d -name dist -prune -exec rm -rf {} +
	find . -type d -name site -prune -exec rm -rf {} +
	find compiler-labs -type f -name .tsbuildinfo -delete
