SHELL := /bin/bash
TRACK ?= python
RELEASE ?= 1.0

.PHONY: help core-proof up down reset logs smoke postgres conformance concurrency query recovery artifact webhook release final

help:
	@$(MAKE) -C .. program-help

core-proof:
	@$(MAKE) -C .. core-proof

up:
	@$(MAKE) -C .. postgres-up TRACK=$(TRACK) RELEASE=$(RELEASE)

down:
	@$(MAKE) -C .. postgres-down TRACK=$(TRACK)

reset:
	@$(MAKE) -C .. postgres-reset

logs:
	@$(MAKE) -C .. logs TRACK=$(TRACK) RELEASE=$(RELEASE)

smoke:
	@$(MAKE) -C .. smoke-proof TRACK=$(TRACK) RELEASE=$(RELEASE)

postgres:
	@$(MAKE) -C .. postgres-proof TRACK=$(TRACK) RELEASE=$(RELEASE)

conformance:
	@$(MAKE) -C .. conformance-proof TRACK=$(TRACK) RELEASE=$(RELEASE)

concurrency:
	@$(MAKE) -C .. concurrency-proof TRACK=$(TRACK) RELEASE=$(RELEASE)

query:
	@$(MAKE) -C .. query-proof TRACK=$(TRACK) RELEASE=$(RELEASE)

recovery:
	@$(MAKE) -C .. recovery-proof TRACK=$(TRACK) RELEASE=$(RELEASE)

artifact:
	@$(MAKE) -C .. artifact-proof TRACK=$(TRACK) RELEASE=$(RELEASE)

webhook:
	@$(MAKE) -C .. webhook-proof TRACK=$(TRACK) RELEASE=$(RELEASE)

release:
	@$(MAKE) -C .. release-proof TRACK=$(TRACK)

final:
	@$(MAKE) -C .. final-proof TRACK=$(TRACK) RELEASE=$(RELEASE)
