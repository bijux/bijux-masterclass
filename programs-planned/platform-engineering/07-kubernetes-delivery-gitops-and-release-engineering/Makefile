PYTHON ?= python3
GOTOOLCHAIN ?= local

.PHONY: help doctor predecessor-proof structure-proof document-proof nav-proof data-proof link-proof code-proof manifest-resource-proof vector-proof python-proof go-proof git-proof release-proof defect-proof handoff-proof educational-proof capstone-tour core-proof manifest manifest-proof kustomize-proof helm-proof argocd-proof flux-proof kind-proof docs-build clean

help:
	@echo "Course 7 — Kubernetes Delivery, GitOps, and Release Engineering"
	@echo "make doctor | predecessor-proof | core-proof | capstone-tour | manifest-proof"
	@echo "Optional native lanes: make kustomize-proof helm-proof argocd-proof flux-proof kind-proof docs-build"

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
manifest-resource-proof:
	@$(PYTHON) scripts/verify_manifests.py
vector-proof:
	@$(PYTHON) scripts/verify_vectors.py
python-proof:
	@PYTHONPATH=capstone $(PYTHON) -m unittest discover -s capstone/tests -p 'test_*.py' -v
go-proof:
	@cd capstone/gitopsprobe-go && GOTOOLCHAIN=$(GOTOOLCHAIN) go test ./...
git-proof:
	@PYTHONPATH=capstone $(PYTHON) scripts/verify_git_history.py
release-proof:
	@PYTHONPATH=capstone $(PYTHON) scripts/verify_releases.py
defect-proof:
	@$(PYTHON) scripts/verify_defects.py
handoff-proof:
	@$(PYTHON) scripts/verify_handoff.py
educational-proof:
	@$(PYTHON) scripts/verify_educational_quality.py
capstone-tour:
	@PYTHONPATH=capstone $(PYTHON) capstone/scripts/capstone_tour.py
core-proof: predecessor-proof structure-proof document-proof nav-proof data-proof link-proof code-proof manifest-resource-proof vector-proof python-proof go-proof git-proof release-proof defect-proof handoff-proof capstone-tour educational-proof
	@echo "PASS Course 7 core proof"
manifest:
	@$(PYTHON) scripts/manifest.py
manifest-proof:
	@$(PYTHON) scripts/manifest_proof.py
kustomize-proof:
	@$(PYTHON) scripts/optional_tool.py kustomize build capstone/repository/apps/atlas/overlays/prod
helm-proof:
	@$(PYTHON) scripts/optional_tool.py helm lint capstone/repository/charts/atlas
argocd-proof:
	@$(PYTHON) scripts/optional_tool.py argocd version --client
flux-proof:
	@$(PYTHON) scripts/optional_tool.py flux check --pre
kind-proof:
	@$(PYTHON) scripts/optional_tool.py kind version
docs-build:
	mkdocs build --strict
clean:
	@$(PYTHON) capstone/scripts/clean.py
