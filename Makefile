SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.DEFAULT_GOAL := help

COURSES_DIR := courses
COURSE ?= deep-dive-make
COURSE_DIR := $(COURSES_DIR)/$(COURSE)

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: courses
courses: ## List available courses
	@find $(COURSES_DIR) -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort

.PHONY: course-help
course-help: ## Show the selected course's Make targets
	@$(MAKE) -C $(COURSE_DIR) help

.PHONY: docs-build
docs-build: ## Build docs for the selected course
	@$(MAKE) -C $(COURSE_DIR) docs-build

.PHONY: docs-serve
docs-serve: ## Serve docs for the selected course
	@$(MAKE) -C $(COURSE_DIR) docs-serve

.PHONY: test
test: ## Run tests for the selected course
	@$(MAKE) -C $(COURSE_DIR) test

.PHONY: clean
clean: ## Run clean for the selected course
	@$(MAKE) -C $(COURSE_DIR) clean
