PYTHON ?= python3
TOOL := $(PYTHON) scripts/course_tool.py

.PHONY: help doctor predecessor-proof orientation-proof structure-proof \
	boundary-proof ownership-proof data-proof dependency-proof saga-proof \
	reconciliation-proof security-proof routing-proof release-proof extraction-proof \
	migration-proof vector-proof python-proof typescript-proof distributed-proof network-lab-proof \
	planted-defect-proof final-defense-proof handoff-proof data-format-proof \
	markdown-link-proof education-proof python-syntax-proof hygiene-proof \
	capstone-tour core-proof full-proof manifest-proof docs-build compose-proof \
	kubernetes-proof postgres-proof setup clean

help:
	@printf '%s\n' \
	  'Course 8 — Distributed API Architecture and Microservices Engineering' \
	  '' \
	  'Primary learner routes:' \
	  '  make doctor' \
	  '  make predecessor-proof' \
	  '  make capstone-tour' \
	  '  make core-proof' \
	  '  make manifest-proof' \
	  '' \
	  'Focused evidence:' \
	  '  make boundary-proof ownership-proof data-proof dependency-proof' \
	  '  make saga-proof security-proof routing-proof release-proof' \
	  '  make distributed-proof network-lab-proof extraction-proof final-defense-proof' \
	  '' \
	  'Environment-backed:' \
	  '  make postgres-proof compose-proof kubernetes-proof docs-build full-proof'

doctor:
	$(TOOL) doctor
predecessor-proof:
	$(TOOL) predecessor-proof
orientation-proof:
	$(TOOL) orientation-proof
structure-proof:
	$(TOOL) structure-proof
boundary-proof:
	$(TOOL) boundary-proof
ownership-proof:
	$(TOOL) ownership-proof
data-proof:
	$(TOOL) data-proof
dependency-proof:
	$(TOOL) dependency-proof
saga-proof:
	$(TOOL) saga-proof
reconciliation-proof:
	$(TOOL) reconciliation-proof
security-proof:
	$(TOOL) security-proof
routing-proof:
	$(TOOL) routing-proof
release-proof:
	$(TOOL) release-proof
extraction-proof:
	$(TOOL) extraction-proof
migration-proof:
	$(TOOL) migration-proof
vector-proof:
	$(TOOL) vector-proof
python-proof:
	$(TOOL) python-proof
typescript-proof:
	$(TOOL) typescript-proof
distributed-proof:
	$(TOOL) distributed-proof
network-lab-proof:
	$(TOOL) network-lab-proof
planted-defect-proof:
	$(TOOL) planted-defect-proof
final-defense-proof:
	$(TOOL) final-defense-proof
handoff-proof:
	$(TOOL) handoff-proof
data-format-proof:
	$(TOOL) data-format-proof
markdown-link-proof:
	$(TOOL) markdown-link-proof
education-proof:
	$(TOOL) education-proof
python-syntax-proof:
	$(TOOL) python-syntax-proof
hygiene-proof:
	$(TOOL) hygiene-proof
capstone-tour:
	$(TOOL) capstone-tour
core-proof:
	$(TOOL) core-proof
full-proof:
	$(TOOL) full-proof
manifest-proof:
	$(TOOL) manifest-proof
docs-build:
	$(TOOL) docs-build
compose-proof:
	$(TOOL) compose-proof
kubernetes-proof:
	$(TOOL) kubernetes-proof
postgres-proof:
	$(TOOL) postgres-proof

setup:
	$(PYTHON) -m pip install -e capstone/tracks/python-distributed
	cd capstone/tracks/typescript-distributed && npm install
	$(PYTHON) -m pip install -r requirements-docs.txt

clean:
	rm -rf site .tmp
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	rm -rf capstone/tracks/typescript-distributed/dist
	find . -name '*.pyc' -delete
