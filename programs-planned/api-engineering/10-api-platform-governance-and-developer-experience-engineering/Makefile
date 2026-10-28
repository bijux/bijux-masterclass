PYTHON ?= python3
TOOL := $(PYTHON) scripts/course_tool.py

.PHONY: help doctor predecessor-proof orientation-proof structure-proof \
	contract-proof catalog-proof registry-proof governance-proof policy-proof \
	lifecycle-proof template-proof documentation-proof docs-proof sandbox-proof \
	sdk-proof runtime-proof analytics-proof support-proof release-proof \
	migration-proof vector-proof python-proof typescript-proof network-lab-proof \
	planted-defect-proof final-defense-proof data-format-proof markdown-link-proof \
	education-proof snippet-proof python-syntax-proof hygiene-proof capstone-tour core-proof \
	full-proof manifest-proof docs-build build-manifest build-artifacts clean \
	module-01-proof module-02-proof module-03-proof module-04-proof module-05-proof \
	module-06-proof module-07-proof module-08-proof module-09-proof module-10-proof

help:
	@printf '%s\n' \
	  'Course 10 — API Platform, Governance, and Developer Experience Engineering' \
	  '' \
	  'Primary learner routes:' \
	  '  make doctor' \
	  '  make predecessor-proof' \
	  '  make capstone-tour' \
	  '  make core-proof' \
	  '  make manifest-proof' \
	  '' \
	  'Focused evidence:' \
	  '  make catalog-proof registry-proof governance-proof lifecycle-proof' \
	  '  make template-proof documentation-proof sandbox-proof sdk-proof' \
	  '  make runtime-proof analytics-proof support-proof release-proof' \
	  '' \
	  'Environment-backed:' \
	  '  make docs-build full-proof'

%-proof:
	$(TOOL) $@ 

doctor:
	$(TOOL) doctor
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
clean:
	$(TOOL) clean
build-artifacts:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) scripts/build_capstone_artifacts.py
build-manifest:
	$(PYTHON) scripts/build_manifest.py
