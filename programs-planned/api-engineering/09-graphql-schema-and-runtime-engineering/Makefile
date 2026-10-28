PYTHON ?= python3
TOOL := $(PYTHON) scripts/course_tool.py

.PHONY: help doctor predecessor-proof orientation-proof structure-proof \
	schema-proof ownership-proof batching-proof pagination-proof mutation-proof \
	authorization-proof demand-proof error-proof subscription-proof release-proof \
	migration-proof vector-proof python-proof typescript-proof network-lab-proof \
	planted-defect-proof final-defense-proof handoff-proof data-format-proof \
	markdown-link-proof education-proof python-syntax-proof hygiene-proof \
	capstone-tour core-proof full-proof manifest-proof docs-build framework-proof \
	module-01-proof module-02-proof module-03-proof module-04-proof module-05-proof \
	module-06-proof module-07-proof module-08-proof module-09-proof module-10-proof \
	setup clean build-manifest

help:
	@printf '%s\n' \
	  'Course 9 — GraphQL Schema and Runtime Engineering' \
	  '' \
	  'Primary learner routes:' \
	  '  make doctor' \
	  '  make predecessor-proof' \
	  '  make capstone-tour' \
	  '  make core-proof' \
	  '  make manifest-proof' \
	  '' \
	  'Focused evidence:' \
	  '  make schema-proof ownership-proof batching-proof pagination-proof' \
	  '  make mutation-proof authorization-proof demand-proof error-proof' \
	  '  make subscription-proof release-proof network-lab-proof' \
	  '' \
	  'Environment-backed:' \
	  '  make framework-proof docs-build full-proof'

doctor:
	$(TOOL) doctor
predecessor-proof:
	$(TOOL) predecessor-proof
orientation-proof:
	$(TOOL) orientation-proof
structure-proof:
	$(TOOL) structure-proof
schema-proof:
	$(TOOL) schema-proof
ownership-proof:
	$(TOOL) ownership-proof
batching-proof:
	$(TOOL) batching-proof
pagination-proof:
	$(TOOL) pagination-proof
mutation-proof:
	$(TOOL) mutation-proof
authorization-proof:
	$(TOOL) authorization-proof
demand-proof:
	$(TOOL) demand-proof
error-proof:
	$(TOOL) error-proof
subscription-proof:
	$(TOOL) subscription-proof
release-proof:
	$(TOOL) release-proof
migration-proof:
	$(TOOL) migration-proof
vector-proof:
	$(TOOL) vector-proof
python-proof:
	$(TOOL) python-proof
typescript-proof:
	$(TOOL) typescript-proof
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
framework-proof:
	$(TOOL) framework-proof
module-01-proof:
	$(TOOL) module-01-proof
module-02-proof:
	$(TOOL) module-02-proof
module-03-proof:
	$(TOOL) module-03-proof
module-04-proof:
	$(TOOL) module-04-proof
module-05-proof:
	$(TOOL) module-05-proof
module-06-proof:
	$(TOOL) module-06-proof
module-07-proof:
	$(TOOL) module-07-proof
module-08-proof:
	$(TOOL) module-08-proof
module-09-proof:
	$(TOOL) module-09-proof
module-10-proof:
	$(TOOL) module-10-proof

setup:
	$(PYTHON) -m pip install -e capstone/tracks/python-graphql
	cd capstone/tracks/typescript-graphql && npm install
	$(PYTHON) -m pip install -r requirements-docs.txt

build-manifest:
	$(PYTHON) scripts/build_manifest.py

clean:
	$(TOOL) clean
