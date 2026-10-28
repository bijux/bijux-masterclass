SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help
PYTHON ?= python3
PYTHONPATH := capstone

.PHONY: help program-help doctor setup predecessor-proof handoff-proof test workload-proof release-proof links-proof checked-release capstone-tour core-proof manifest manifest-proof docs-build docs-serve native-preflight native-build-proof native-runtime-proof native-registry-proof native-supply-chain-proof clean

help: ## Show stable Course 3 entrypoints.
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-28s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

program-help: help ## Compatibility alias used by the program router.

doctor: ## Classify mandatory and optional proof environments.
	$(PYTHON) scripts/doctor.py

setup: ## Install only the pinned Python course requirements.
	$(PYTHON) -m pip install -r requirements.txt

predecessor-proof: ## Verify the exact Course 2 handoff.
	$(PYTHON) scripts/verify_handoff.py

handoff-proof: ## Verify both predecessor and Course 4 handoff manifests.
	$(PYTHON) scripts/verify_handoff.py

test: ## Run dependency-light semantic and course tests.
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest -q -p no:cacheprovider capstone/tests tests

workload-proof: ## Format-check and compile/test the Atlas Go workloads.
	cd capstone/workload && test -z "$$(gofmt -d .)" && GOTOOLCHAIN=local go test ./...

release-proof: ## Verify accepted/rejected release decisions and planted defects.
	$(PYTHON) scripts/verify_releases.py
	$(PYTHON) scripts/verify_defects.py

links-proof: ## Verify reader-facing local Markdown navigation.
	$(PYTHON) scripts/check_links.py

checked-release: ## Rebuild checked release evidence and Course 4 handoff.
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) $(PYTHON) capstone/scripts/generate_checked_release.py

capstone-tour: ## Execute Atlas Workload Release 1.0 end to end.
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) $(PYTHON) capstone/scripts/run_capstone_tour.py

core-proof: ## Run the complete dependency-light reader, code, release, and handoff proof.
	$(PYTHON) scripts/course_proof.py

manifest: ## Regenerate the exact course manifest.
	$(PYTHON) scripts/manifest.py write

manifest-proof: ## Verify the exact course manifest.
	$(PYTHON) scripts/manifest.py verify

docs-build: ## Build the course-book site strictly when MkDocs is installed.
	mkdocs build --strict

docs-serve: ## Serve the course book locally.
	mkdocs serve

native-preflight: ## Report independent builder/runtime/registry/supply-chain tools.
	@for tool in docker podman buildctl runc crun oras skopeo cosign syft grype; do command -v $$tool >/dev/null 2>&1 && echo "present $$tool" || echo "missing $$tool"; done

native-build-proof: ## Run the guarded BuildKit multi-platform lane.
	capstone/native/buildkit-proof.sh "$${EVIDENCE_DIR:-$$(pwd)/native-evidence/build}"

native-runtime-proof: ## Run the guarded external OCI runtime lane; requires BUNDLE_DIR.
	@test -n "$${BUNDLE_DIR:-}" || { echo 'set BUNDLE_DIR' >&2; exit 2; }
	capstone/native/runtime-proof.sh "$$BUNDLE_DIR" "$${EVIDENCE_DIR:-$$(pwd)/native-evidence/runtime}"

native-registry-proof: ## Run the guarded ORAS registry lane; requires ATLAS_REGISTRY and ATLAS_SUBJECT_DIGEST.
	capstone/native/registry-proof.sh "$${EVIDENCE_DIR:-$$(pwd)/native-evidence/registry}"

native-supply-chain-proof: ## Run the guarded Syft/Grype/Cosign lane; requires ATLAS_IMAGE.
	capstone/native/supply-chain-proof.sh "$${EVIDENCE_DIR:-$$(pwd)/native-evidence/supply-chain}"

clean: ## Remove generated caches, local registry state, and rendered docs.
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache -o -name .ruff_cache \) -prune -exec rm -rf {} +
	rm -rf site capstone/registry/local-store reports/core-proof.json reports/doctor.json
