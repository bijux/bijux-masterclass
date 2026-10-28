PYTHON ?= python3
GOTOOLCHAIN ?= local

.PHONY: help doctor predecessor-proof structure-proof document-proof nav-proof \
	data-proof link-proof code-proof pki-proof manifest-resource-proof python-proof \
	go-proof release-proof defect-proof handoff-proof capstone-tour core-proof \
	manifest manifest-proof kind-proof docs-build clean

help:
	@echo "Course 5 — Kubernetes Networking, Gateway, and Service Connectivity Engineering"
	@echo "make doctor | predecessor-proof | core-proof | capstone-tour | manifest-proof"
	@echo "Optional: make kind-proof | docs-build"

doctor:
	@$(PYTHON) scripts/doctor.py

predecessor-proof:
	@$(PYTHON) scripts/verify_predecessor.py

structure-proof:
	@$(PYTHON) scripts/verify_structure.py

document-proof:
	@$(PYTHON) scripts/verify_documents.py

nav-proof:
	@$(PYTHON) scripts/verify_nav.py

data-proof:
	@$(PYTHON) scripts/verify_data.py

link-proof:
	@$(PYTHON) scripts/verify_links.py

code-proof:
	@$(PYTHON) scripts/verify_code.py

pki-proof:
	@$(PYTHON) scripts/verify_pki.py

manifest-resource-proof:
	@$(PYTHON) scripts/verify_manifests.py

python-proof:
	@PYTHONPATH=capstone $(PYTHON) -m unittest discover -s capstone/tests -p 'test_*.py' -v

go-proof:
	@cd capstone/cni-go && GOTOOLCHAIN=$(GOTOOLCHAIN) go test ./...
	@cd capstone/netprobe-go && GOTOOLCHAIN=$(GOTOOLCHAIN) go test ./...

release-proof:
	@PYTHONPATH=capstone $(PYTHON) scripts/verify_releases.py

defect-proof:
	@$(PYTHON) scripts/verify_defects.py

handoff-proof:
	@$(PYTHON) scripts/verify_handoff.py

capstone-tour:
	@PYTHONPATH=capstone $(PYTHON) capstone/scripts/capstone_tour.py

core-proof: predecessor-proof structure-proof document-proof nav-proof data-proof \
	link-proof code-proof pki-proof manifest-resource-proof python-proof go-proof \
	release-proof defect-proof handoff-proof capstone-tour
	@$(PYTHON) scripts/verify_educational_quality.py
	@echo "PASS Course 5 core proof"

manifest:
	@$(PYTHON) scripts/manifest.py

manifest-proof:
	@$(PYTHON) scripts/manifest_proof.py

kind-proof:
	@capstone/kind/cluster_proof.sh

docs-build:
	@mkdocs build --strict

clean:
	@PYTHONPATH=capstone $(PYTHON) capstone/scripts/clean.py
	@find . -type d -name __pycache__ -prune -exec rm -rf {} +
	@rm -rf .pytest_cache capstone/tests/.pytest_cache site reports/generated
