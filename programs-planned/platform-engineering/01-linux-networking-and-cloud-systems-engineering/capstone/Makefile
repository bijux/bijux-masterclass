SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help
PYTHON ?= python3

.PHONY: help doctor core-proof test tour linux-proof systemd-proof pki-proof nginx-proof privileged-network-lab resource-lab handoff-export clean

help: ## Show capstone targets.
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-28s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

doctor: ## Classify available evidence environments.
	$(PYTHON) scripts/doctor.py

core-proof: ## Run dependency-light structure, data, code, handoff, tests, and PKI checks.
	PYTHONPATH=. $(PYTHON) scripts/course_tool.py core-proof

test: ## Run the Python capstone tests.
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

tour: ## Run the HTTPS API/worker/edge capstone tour.
	PYTHONPATH=. $(PYTHON) scripts/run_tour.py

linux-proof: ## Capture real Linux process, resource, and socket evidence.
	PYTHONPATH=. $(PYTHON) scripts/linux_probe.py

systemd-proof: ## Verify systemd unit syntax when systemd-analyze is available.
	@command -v systemd-analyze >/dev/null 2>&1 || { echo 'systemd-analyze not available'; exit 2; }
	systemd-analyze verify systemd/*.service systemd/*.timer

pki-proof: ## Inspect certificate names and local trust material.
	$(PYTHON) scripts/verify_pki.py

nginx-proof: ## Validate the maintained Nginx reference configuration.
	$(PYTHON) scripts/verify_nginx.py

privileged-network-lab: ## Run the disposable network-namespace lab.
	ALLOW_PRIVILEGED_LAB=1 scripts/namespace_lab.sh

resource-lab: ## Run a bounded systemd resource-control exercise.
	ALLOW_RESOURCE_LAB=1 scripts/resource_lab.sh

handoff-export: ## Rebuild the Course 2 handoff manifest.
	$(PYTHON) scripts/export_handoff.py

clean: ## Remove generated reports and runtime artifacts.
	@find reports -type f ! -name .gitkeep -delete
	@rm -rf runtime
	@find . -type d -name __pycache__ -prune -exec rm -rf {} +
	@find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
