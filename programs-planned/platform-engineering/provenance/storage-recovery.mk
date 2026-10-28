PYTHON ?= python3
COURSE := 06-kubernetes-storage-stateful-workloads-and-data-resilience-engineering

.PHONY: help doctor core-proof capstone-tour manifest manifest-proof docs-build clean
help:
	@$(MAKE) -C $(COURSE) help
doctor:
	@$(MAKE) -C $(COURSE) doctor
core-proof:
	@$(MAKE) -C $(COURSE) core-proof
capstone-tour:
	@$(MAKE) -C $(COURSE) capstone-tour
manifest:
	@$(MAKE) -C $(COURSE) manifest
	@$(PYTHON) scripts/program_manifest.py
manifest-proof:
	@$(MAKE) -C $(COURSE) manifest-proof
	@$(PYTHON) scripts/program_manifest_proof.py
docs-build:
	mkdocs build --strict
clean:
	@$(MAKE) -C $(COURSE) clean
