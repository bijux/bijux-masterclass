PYTHON ?= python3

.PHONY: install docs-install audit links source-audit investigations typecheck build test verify docs proof clean
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
	$(PYTHON) tools/run_packages.py test --jobs 8

verify:
	$(PYTHON) tools/proof.py --compatibility

docs:
	mkdocs build --strict -f mkdocs.yml

proof:
	$(PYTHON) tools/proof.py

clean:
	npm run clean
