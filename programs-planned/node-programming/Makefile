COURSES := 01-node-typescript-foundations 02-javascript-object-model-runtime-protocols 03-advanced-typescript-library-api-design 04-async-node-event-driven-architecture 05-node-streams-filesystems-data-pipelines 06-node-networking-http-service-architecture
PYTHON ?= python3

.PHONY: install docs-install audit program-audit links source-audit investigations typecheck build test verify proof docs clean

install source-audit investigations typecheck build test verify proof clean:
	@set -e; for course in $(COURSES); do $(MAKE) -C $$course $@; done

audit:
	@set -e; for course in $(COURSES); do $(MAKE) -C $$course audit; done
	$(PYTHON) tools/audit_program.py

program-audit:
	$(PYTHON) tools/audit_program.py

links:
	$(PYTHON) tools/check_links.py

docs-install:
	$(PYTHON) -m pip install -r requirements-docs.txt

docs:
	mkdocs build --strict -f mkdocs.yml
