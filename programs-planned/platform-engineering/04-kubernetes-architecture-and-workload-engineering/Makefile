PYTHON ?= python3
COURSE := $(CURDIR)
export PYTHONPATH := $(COURSE)/capstone

.PHONY: help doctor setup predecessor-proof structure-proof document-proof manifest-policy-proof \
        python-test go-test defects-proof releases-proof handoff-proof links-proof nav-proof \
        capstone-tour core-proof kind-proof docs-build manifest manifest-proof clean

help:
	@printf '%s\n' \
	  'doctor              report required and optional tools' \
	  'core-proof          run the complete dependency-light course proof' \
	  'capstone-tour       execute the cumulative semantic walkthrough' \
	  'kind-proof          guarded disposable local-cluster observation lane' \
	  'docs-build          strict MkDocs build when dependencies exist' \
	  'manifest            regenerate exact course manifest' \
	  'manifest-proof      verify exact course manifest' \
	  'clean               remove generated proof output'

doctor:
	$(PYTHON) scripts/doctor.py

setup:
	$(PYTHON) -m pip install -r requirements.txt -r requirements-docs.txt

predecessor-proof:
	$(PYTHON) scripts/verify_predecessor.py

structure-proof:
	$(PYTHON) scripts/verify_structure.py

document-proof:
	$(PYTHON) scripts/verify_documents.py

manifest-policy-proof:
	$(PYTHON) scripts/verify_manifests.py

python-test:
	$(PYTHON) -m pytest -q capstone/tests

go-test:
	cd capstone/controller-go && go test ./...

defects-proof:
	$(PYTHON) scripts/verify_defects.py

releases-proof:
	$(PYTHON) scripts/verify_releases.py

handoff-proof:
	$(PYTHON) scripts/verify_handoff.py

links-proof:
	$(PYTHON) scripts/check_links.py

nav-proof:
	$(PYTHON) scripts/verify_nav.py

capstone-tour:
	$(PYTHON) scripts/capstone_tour.py

core-proof:
	$(PYTHON) scripts/core_proof.py

kind-proof:
	ALLOW_KIND_PROOF=1 scripts/kind_proof.sh

docs-build:
	mkdocs build --strict

manifest:
	$(PYTHON) scripts/clean.py
	$(PYTHON) scripts/manifest.py

manifest-proof:
	$(PYTHON) scripts/manifest_proof.py

clean:
	$(PYTHON) scripts/clean.py
