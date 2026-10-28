PYTHON ?= python3
TOOL := $(PYTHON) scripts/course_tool.py

.PHONY: help doctor predecessor-proof structure-proof contract-proof \
	descriptor-proof boundary-proof orientation-proof model-proof compatibility-proof unary-proof \
	deadline-proof streaming-proof security-proof lifecycle-proof governance-proof \
	migration-proof python-proof python-network-proof typescript-proof release-proof \
	planted-defect-proof handoff-proof markdown-link-proof education-proof \
	hygiene-proof capstone-tour core-proof full-proof manifest-proof docs-build \
	protoc-proof buf-proof grpcurl-proof clean setup

help:
	@printf '%s\n' \
	  'Course 7 — gRPC and Protobuf Engineering' \
	  '' \
	  'Core learner routes:' \
	  '  make doctor' \
	  '  make predecessor-proof' \
	  '  make capstone-tour' \
	  '  make core-proof' \
	  '  make manifest-proof' \
	  '' \
	  'Focused routes:' \
	  '  make contract-proof model-proof compatibility-proof' \
	  '  make unary-proof deadline-proof streaming-proof' \
	  '  make security-proof lifecycle-proof governance-proof' \
	  '  make python-network-proof typescript-proof release-proof' \
	  '' \
	  'Environment-backed routes:' \
	  '  make protoc-proof buf-proof grpcurl-proof docs-build full-proof'

doctor:
	$(TOOL) doctor

predecessor-proof:
	$(TOOL) predecessor-proof

orientation-proof:
	$(TOOL) orientation-proof

structure-proof:
	$(TOOL) structure-proof

contract-proof:
	$(TOOL) contract-proof

descriptor-proof:
	$(TOOL) descriptor-proof

boundary-proof:
	$(TOOL) boundary-proof

model-proof:
	$(TOOL) model-proof

compatibility-proof:
	$(TOOL) compatibility-proof

unary-proof:
	$(TOOL) unary-proof

deadline-proof:
	$(TOOL) deadline-proof

streaming-proof:
	$(TOOL) streaming-proof

security-proof:
	$(TOOL) security-proof

lifecycle-proof:
	$(TOOL) lifecycle-proof

governance-proof:
	$(TOOL) governance-proof

migration-proof:
	$(TOOL) migration-proof

python-proof:
	$(TOOL) python-proof

python-network-proof:
	$(TOOL) python-network-proof

typescript-proof:
	$(TOOL) typescript-proof

release-proof:
	$(TOOL) release-proof

planted-defect-proof:
	$(TOOL) planted-defect-proof

handoff-proof:
	$(TOOL) handoff-proof

markdown-link-proof:
	$(TOOL) markdown-link-proof

education-proof:
	$(TOOL) education-proof

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

protoc-proof:
	$(TOOL) protoc-proof

buf-proof:
	$(TOOL) buf-proof

grpcurl-proof:
	$(TOOL) grpcurl-proof

setup:
	$(PYTHON) -m pip install -e 'capstone/tracks/python-grpc[dev]'
	cd capstone/tracks/typescript-grpc && npm install
	$(PYTHON) -m pip install -r requirements-docs.txt

clean:
	rm -rf site .tmp
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	rm -rf capstone/tracks/typescript-grpc/dist
	find . -name '*.pyc' -delete
