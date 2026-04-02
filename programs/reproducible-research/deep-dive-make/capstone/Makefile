# Deep Dive Make Capstone — GNU Make Reference Build
# Truthful, parallel-safe reference build (GNU Make >= 4.3; POSIX /bin/sh)

MAKEFLAGS += -rR
.SUFFIXES:
.DELETE_ON_ERROR:

SHELL := /bin/sh
.SHELLFLAGS := -eu -c
# Use '>' as recipe prefix to avoid TAB footgun (GNU Make ≥4.0)
.RECIPEPREFIX := >

export LC_ALL := C
export TZ := UTC

# ---- platform ----
UNAME_S := $(shell uname -s 2>/dev/null || echo Unknown)

# ---- toolchain (override via env/cmdline/config.mk) ----
CC      ?= cc
CC      := $(if $(strip $(CC)),$(CC),cc)
PYTHON  ?= python3
PYTHON  := $(if $(strip $(PYTHON)),$(PYTHON),python3)
CPPFLAGS?=
CFLAGS  ?= -O2
LDFLAGS ?=
LDLIBS  ?=

# ---- layout ----
SRC_DIR := src
INC_DIR := include
BLD_DIR := build
MK_DIR  := mk
TST_DIR := tests
REP_DIR := repro
ARTIFACTS_DIR ?= ../../../../artifacts
REPO_ROOT := $(abspath ../../../../)
WALKTHROUGH_DIR ?= $(ARTIFACTS_DIR)/walkthrough/reproducible-research/deep-dive-make
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/reproducible-research/deep-dive-make
SELFTEST_REPORT_DIR ?= $(ARTIFACTS_DIR)/proof/reproducible-research/deep-dive-make/selftest
CONTRACT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/contract
INCIDENT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/incident
PROFILE_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/profile
SOURCE_BUNDLE_DIR ?= $(ARTIFACTS_DIR)/dist/reproducible-research/deep-dive-make
SOURCE_BUNDLE_PATH ?= $(SOURCE_BUNDLE_DIR)/deep-dive-make-capstone-source.tar.gz
SELFTEST_REPORT_DIR_ABS := $(abspath $(SELFTEST_REPORT_DIR))
REPRO_CASE ?= $(REP_DIR)/05-mkdir-race.mk

DEPFLAGS := -MMD -MP

.DEFAULT_GOAL := all
# IMPORTANT: do NOT mark `all` phony; it is a real sentinel file for convergence.
.PHONY: dyn lint test dist repro discovery-audit attest selftest selftest-report verify-report proof walkthrough \
        contract-audit inspect incident-audit clean submake-demo perf trace-count hardened confirm show show-e show-origins FORCE \
        portability-audit profile-audit eval-demo help tour

# Optional local overrides (must not be required for CI/selftest)
-include config.mk

# Required modules (policy stays here; mechanics live in mk/)
include $(MK_DIR)/contract.mk
include $(MK_DIR)/common.mk
include $(MK_DIR)/macros.mk
include $(MK_DIR)/objects.mk

# ---- UUID handling (must run BEFORE stamps/flags are computed) ----
# Never allow any token containing "no_uuid" to leak into the real link flags.
# This protects macOS (dyld may abort if LC_UUID is suppressed) and also avoids
# toolchain-specific breakage if "-Wl,-no_uuid" leaks elsewhere.
NO_UUID_FLAG := -Wl,-no_uuid

define scrub_no_uuid
$(strip $(foreach f,$(filter-out $(NO_UUID_FLAG),$(1)),$(if $(findstring no_uuid,$(f)),,$(f))))
endef

override LDFLAGS := $(call scrub_no_uuid,$(LDFLAGS))

# Stamps must observe the final/real flags.
include $(MK_DIR)/stamps.mk

# ---- public interface ----
all: app $(DYN_BINS)
>     # convergence sentinel (enables: make -q all)
>     tmp=$@.tmp.$$; printf 'ok\n' > $$tmp && mv -f $$tmp $@ || { rm -f $$tmp; exit 1; }

app: $(OBJS) | $(BLD_DIR)/
>     # atomic publish
>     tmp=$@.tmp.$$; \
>     $(CC) $(LDFLAGS) $^ $(LDLIBS) -o $$tmp && mv -f $$tmp $@ || { rm -f $$tmp; exit 1; }

# Compile objects (atomic .o + .d publish, dir-safe)
$(BLD_DIR)/%.o: $(SRC_DIR)/%.c $(BLD_DIR)/flags.stamp | $(BLD_DIR)/
>     tmp=$@.tmp.$$; dtmp=$(@:.o=.d).tmp.$$; \
>     mkdir -p "$(@D)"; \
>     $(CC) $(CPPFLAGS) $(CFLAGS) $(DEPFLAGS) -MF $$dtmp -MT $@ -c $< -o $$tmp && \
>     mv -f $$tmp $@ && mv -f $$dtmp $(@:.o=.d) || { rm -f $$tmp $$dtmp; exit 1; }

$(BLD_DIR)/:
>     mkdir -p $@

-include $(DEPS)
-include $(DYN_DEPS)

# ---- generated header + dynamic binaries ----
dyn: $(DYN_BINS)

$(DYN_HDR): scripts/gen_dynamic_h.py | $(BLD_DIR)/include/
>     $(call atomic_write,$@,$(PYTHON) $<)

# Dynamic binaries (atomic publish, depfiles for header staleness, flags dep for knobs)
$(BLD_DIR)/bin/%: $(SRC_DIR)/dynamic/%.c $(DYN_HDR) $(BLD_DIR)/flags.stamp | $(BLD_DIR)/bin/
>     tmp=$@.tmp.$$; dtmp=$@.d.tmp.$$; \
>     mkdir -p "$(@D)"; \
>     $(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $(LDLIBS) \
>        $(DEPFLAGS) -MF $$dtmp -MT $@ $< -o $$tmp && \
>     mv -f $$tmp $@ && mv -f $$dtmp $@.d || { rm -f $$tmp $$dtmp; exit 1; }

$(BLD_DIR)/include/:
>     mkdir -p $@

$(BLD_DIR)/bin/:
>     mkdir -p $@

# ---- help (stable public interface) ----
help:
>     @printf '%s\n' \
>     'Public targets:' \
>     '  all               build app + dynamic bins (also writes ./all sentinel)' \
>     '  show              print CFLAGS origin, flavor, and raw value' \
>     '  show-e            rerun show with environment override enabled' \
>     '  source-baseline-check fail if local build state would contaminate a source bundle' \
>     '  source-bundle     write a tracked-source archive for learner or review distribution' \
>     '  test              run runtime assertions' \
>     '  selftest          convergence + serial/parallel equivalence + negative test' \
>     '  selftest-report   write the selftest evidence bundle to artifacts/' \
>     '  verify-report     alias for selftest-report with shared catalog naming' \
>     '  proof             write the sanctioned learner-facing proof bundle set' \
>     '  tour              print the recommended capstone walkthrough' \
>     '  walkthrough       build the learner-facing walkthrough bundle' \
>     '  contract-audit    build the public-contract review bundle' \
>     '  inspect           alias for contract-audit with learner review naming' \
>     '  incident-audit    build an executed failure review bundle (REPRO_CASE=...)' \
>     '  profile-audit     build the execution-profile review bundle' \
>     '  confirm           alias for hardened with shared catalog naming' \
>     '  discovery-audit   assert deterministic discovery (sorted lists)' \
>     '  repro             show how to run the race repro pack' \
>     '  attest            write build/attest.txt (not a dependency of all)' \
>     '  perf              show measurement commands (trace-count + time)' \
>     '  trace-count       count trace lines (heuristic)' \
>     '  portability-audit probe tool/feature availability' \
>     '  eval-demo         optional quarantined eval demo (USE_EVAL=yes)' \
>     '' \
>     'Variables:' \
>     '  DEBUG=1           enable debug symbols (-g)' \
>     '  J=4               parallelism used by some commands' \
>     '  TRACE_MAX=500     selftest trace-line heuristic threshold' \
>     ''

tour:
>     rm -rf "$(TOUR_DIR)"
>     mkdir -p "$(TOUR_DIR)/mk" "$(TOUR_DIR)/repro" "$(TOUR_DIR)/tests"
>     cp README.md "$(TOUR_DIR)/README.md"
>     cp ARCHITECTURE.md "$(TOUR_DIR)/ARCHITECTURE.md"
>     cp PROOF_GUIDE.md "$(TOUR_DIR)/PROOF_GUIDE.md"
>     cp TARGET_GUIDE.md "$(TOUR_DIR)/TARGET_GUIDE.md"
>     cp WALKTHROUGH_GUIDE.md "$(TOUR_DIR)/WALKTHROUGH_GUIDE.md"
>     cp REPRO_GUIDE.md "$(TOUR_DIR)/REPRO_GUIDE.md"
>     cp Makefile "$(TOUR_DIR)/Makefile"
>     cp $(TST_DIR)/run.sh "$(TOUR_DIR)/tests/run.sh"
>     cp $(MK_DIR)/contract.mk "$(TOUR_DIR)/mk/contract.mk"
>     cp $(MK_DIR)/common.mk "$(TOUR_DIR)/mk/common.mk"
>     cp $(MK_DIR)/objects.mk "$(TOUR_DIR)/mk/objects.mk"
>     cp $(MK_DIR)/stamps.mk "$(TOUR_DIR)/mk/stamps.mk"
>     cp $(REP_DIR)/01-shared-log.mk "$(TOUR_DIR)/repro/01-shared-log.mk"
>     $(MAKE) help > "$(TOUR_DIR)/help.txt"
>     $(MAKE) trace-count > "$(TOUR_DIR)/trace-count.txt"
>     printf '%s\n' \
>       'Tour route:' \
>       '  1. Read README.md for the repository contract.' \
>       '  2. Read TARGET_GUIDE.md for the stable public interface.' \
>       '  3. Read PROOF_GUIDE.md for claim-to-evidence routing.' \
>       '  4. Read ARCHITECTURE.md and WALKTHROUGH_GUIDE.md for ownership and first-pass order.' \
>       '  5. Read tests/run.sh and trace-count.txt for proof and observability evidence.' \
>       '  6. Inspect REPRO_GUIDE.md and repro/01-shared-log.mk for the first incident surface.' > "$(TOUR_DIR)/route.txt"
>     printf '%s\n' \
>       'Focused routes:' \
>       '  generators   -> make --trace dyn' \
>       '  architecture -> read mk/contract.mk, mk/objects.mk, mk/stamps.mk' \
>       '  incidents    -> make -f repro/01-shared-log.mk -j2 all' \
>       '  integrity    -> make selftest' > "$(TOUR_DIR)/focused-routes.txt"
>     @printf '%s\n' \
>     'Capstone walkthrough:' \
>     '  1. make walkthrough' \
>     '  2. make help' \
>     '  3. read Makefile for the public build API' \
>     '  4. read tests/run.sh for the proof harness' \
>     '  5. make selftest' \
>     '  6. inspect one repro under repro/' \
>     '' \
>     "Tour bundle: $(TOUR_DIR)" \
>     '' \
>     'Focused routes:' \
>     '  generators  -> make --trace dyn' \
>     '  architecture -> make help && make -p > build/review.dump' \
>     '  incidents    -> make trace-count && make -f repro/01-shared-log.mk -j2 all'
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(TOUR_DIR)" --output "$(TOUR_DIR)/manifest.json"

walkthrough:
>     rm -rf "$(WALKTHROUGH_DIR)"
>     mkdir -p "$(WALKTHROUGH_DIR)/repro" "$(WALKTHROUGH_DIR)/tests" "$(WALKTHROUGH_DIR)/mk"
>     cp README.md "$(WALKTHROUGH_DIR)/README.md"
>     cp ARCHITECTURE.md "$(WALKTHROUGH_DIR)/ARCHITECTURE.md"
>     cp PROOF_GUIDE.md "$(WALKTHROUGH_DIR)/PROOF_GUIDE.md"
>     cp TARGET_GUIDE.md "$(WALKTHROUGH_DIR)/TARGET_GUIDE.md"
>     cp WALKTHROUGH_GUIDE.md "$(WALKTHROUGH_DIR)/WALKTHROUGH_GUIDE.md"
>     cp Makefile "$(WALKTHROUGH_DIR)/Makefile"
>     cp $(TST_DIR)/run.sh "$(WALKTHROUGH_DIR)/tests/run.sh"
>     cp $(MK_DIR)/contract.mk "$(WALKTHROUGH_DIR)/mk/contract.mk"
>     cp $(MK_DIR)/common.mk "$(WALKTHROUGH_DIR)/mk/common.mk"
>     cp $(MK_DIR)/objects.mk "$(WALKTHROUGH_DIR)/mk/objects.mk"
>     cp $(MK_DIR)/stamps.mk "$(WALKTHROUGH_DIR)/mk/stamps.mk"
>     cp $(REP_DIR)/01-shared-log.mk "$(WALKTHROUGH_DIR)/repro/01-shared-log.mk"
>     printf '%s\n' \
>       '1. Read WALKTHROUGH_GUIDE.md to understand the recommended first pass.' \
>       '2. Read README.md and TARGET_GUIDE.md to understand the capstone contract and public targets.' \
>       '3. Read PROOF_GUIDE.md and tests/run.sh to see what selftest is proving.' \
>       '4. Read ARCHITECTURE.md and mk/contract.mk for ownership and boundary design.' \
>       '5. Read mk/objects.mk and mk/stamps.mk for graph truth and modeled hidden inputs.' \
>       '6. Run make help in the capstone directory.' \
>       '7. Run make selftest when you want executed proof.' \
>       '8. Inspect repro/01-shared-log.mk as the first failure class.' > "$(WALKTHROUGH_DIR)/route.txt"
>     printf '%s\n' \
>       'Public entry commands:' \
>       '  make help' \
>       '  make selftest' \
>       '  make repro' \
>       '  make hardened' > "$(WALKTHROUGH_DIR)/commands.txt"
>     printf '%s\n' \
>       'Walkthrough bundle surfaces:' \
>       '  README.md            repository contract and program fit' \
>       '  TARGET_GUIDE.md      stable public target surface' \
>       '  PROOF_GUIDE.md       claim-to-evidence routing' \
>       '  WALKTHROUGH_GUIDE.md bounded first-pass reading order' \
>       '  ARCHITECTURE.md      layer ownership and system map' \
>       '  Makefile             stable public target surface' \
>       '  tests/run.sh         selftest proof harness' \
>       '  mk/contract.mk       platform and policy boundaries' \
>       '  mk/objects.mk        rooted discovery and object modeling' \
>       '  mk/stamps.mk         build-state evidence surfaces' \
>       '  repro/01-shared-log.mk first concurrency failure route' > "$(WALKTHROUGH_DIR)/bundle-guide.txt"
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(WALKTHROUGH_DIR)" --output "$(WALKTHROUGH_DIR)/manifest.json"
>     @echo "PASS: wrote capstone walkthrough to $(WALKTHROUGH_DIR)"

contract-audit:
>     rm -rf "$(CONTRACT_AUDIT_DIR)"
>     mkdir -p "$(CONTRACT_AUDIT_DIR)/tests"
>     cp README.md "$(CONTRACT_AUDIT_DIR)/README.md"
>     cp CONTRACT_AUDIT_GUIDE.md "$(CONTRACT_AUDIT_DIR)/CONTRACT_AUDIT_GUIDE.md"
>     cp PROOF_GUIDE.md "$(CONTRACT_AUDIT_DIR)/PROOF_GUIDE.md"
>     cp TARGET_GUIDE.md "$(CONTRACT_AUDIT_DIR)/TARGET_GUIDE.md"
>     cp Makefile "$(CONTRACT_AUDIT_DIR)/Makefile"
>     cp $(TST_DIR)/run.sh "$(CONTRACT_AUDIT_DIR)/tests/run.sh"
>     $(MAKE) help > "$(CONTRACT_AUDIT_DIR)/help.txt"
>     $(MAKE) portability-audit > "$(CONTRACT_AUDIT_DIR)/portability.txt"
>     $(MAKE) discovery-audit > "$(CONTRACT_AUDIT_DIR)/discovery.txt"
>     printf '%s\n' \
>       'Contract audit route:' \
>       '  1. Read CONTRACT_AUDIT_GUIDE.md for the reading order and review lens.' \
>       '  2. Read README.md and help.txt for the repository claim and stable public targets.' \
>       '  3. Read TARGET_GUIDE.md and PROOF_GUIDE.md for target meaning and claim-to-evidence routing.' \
>       '  4. Read portability.txt for the declared runtime boundary.' \
>       '  5. Read discovery.txt and tests/run.sh for graph and proof discipline.' > "$(CONTRACT_AUDIT_DIR)/route.txt"
>     printf '%s\n' \
>       'Review questions:' \
>       '  Which targets are part of the durable public build contract?' \
>       '  Which boundaries depend on GNU Make or toolchain features?' \
>       '  Which discovery assumptions are explicit enough to audit?' > "$(CONTRACT_AUDIT_DIR)/review-questions.txt"
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(CONTRACT_AUDIT_DIR)" --output "$(CONTRACT_AUDIT_DIR)/manifest.json"
>     @echo "PASS: wrote contract audit to $(CONTRACT_AUDIT_DIR)"

inspect: contract-audit
>     @echo "PASS: inspect route completed via $(CONTRACT_AUDIT_DIR)"

incident-audit:
>     rm -rf "$(INCIDENT_AUDIT_DIR)"
>     mkdir -p "$(INCIDENT_AUDIT_DIR)"
>     cp "$(REPRO_CASE)" "$(INCIDENT_AUDIT_DIR)/$(notdir $(REPRO_CASE))"
>     cp INCIDENT_REVIEW_GUIDE.md "$(INCIDENT_AUDIT_DIR)/INCIDENT_REVIEW_GUIDE.md"
>     printf '%s\n' "make -f $(REPRO_CASE) -j2 all" > "$(INCIDENT_AUDIT_DIR)/command.txt"
>     if $(MAKE) -f "$(REPRO_CASE)" -j2 all > "$(INCIDENT_AUDIT_DIR)/run.txt" 2>&1; then status=0; else status=$$?; fi; \
>       printf 'exit_status=%s\n' "$$status" > "$(INCIDENT_AUDIT_DIR)/exit-status.txt"; \
>       $(MAKE) -f "$(REPRO_CASE)" clean >/dev/null 2>&1 || true
>     printf '%s\n' \
>       'Incident audit route:' \
>       '  1. Read INCIDENT_REVIEW_GUIDE.md for the incident reading order.' \
>       '  2. Read command.txt, run.txt, and exit-status.txt for the observed incident evidence.' \
>       '  3. Read the copied repro makefile for the dishonest or unsafe pattern.' \
>       '  4. Read REPRO_GUIDE.md for the repair route back into the course.' \
>       '  5. Read PROOF_GUIDE.md if you need the matching production proof surface.' > "$(INCIDENT_AUDIT_DIR)/route.txt"
>     printf '%s\n' \
>       'Repair surfaces:' \
>       '  REPRO_GUIDE.md   maps the failure class to the teaching repair pattern' \
>       '  PROOF_GUIDE.md   maps the repaired claim to the reference build surface' \
>       '  mk/objects.mk    shows rooted discovery and directory discipline in the real build' \
>       '  mk/stamps.mk     shows durable state tracking in the real build' > "$(INCIDENT_AUDIT_DIR)/repair-surfaces.txt"
>     cp REPRO_GUIDE.md "$(INCIDENT_AUDIT_DIR)/REPRO_GUIDE.md"
>     cp PROOF_GUIDE.md "$(INCIDENT_AUDIT_DIR)/PROOF_GUIDE.md"
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(INCIDENT_AUDIT_DIR)" --output "$(INCIDENT_AUDIT_DIR)/manifest.json"
>     @echo "PASS: wrote incident audit to $(INCIDENT_AUDIT_DIR)"

profile-audit:
>     rm -rf "$(PROFILE_AUDIT_DIR)"
>     mkdir -p "$(PROFILE_AUDIT_DIR)/mk"
>     cp README.md "$(PROFILE_AUDIT_DIR)/README.md"
>     cp PROFILE_AUDIT_GUIDE.md "$(PROFILE_AUDIT_DIR)/PROFILE_AUDIT_GUIDE.md"
>     cp PROOF_GUIDE.md "$(PROFILE_AUDIT_DIR)/PROOF_GUIDE.md"
>     cp TARGET_GUIDE.md "$(PROFILE_AUDIT_DIR)/TARGET_GUIDE.md"
>     cp Makefile "$(PROFILE_AUDIT_DIR)/Makefile"
>     cp $(MK_DIR)/contract.mk "$(PROFILE_AUDIT_DIR)/mk/contract.mk"
>     $(MAKE) help > "$(PROFILE_AUDIT_DIR)/help.txt"
>     $(MAKE) portability-audit > "$(PROFILE_AUDIT_DIR)/portability.txt"
>     $(MAKE) show-origins > "$(PROFILE_AUDIT_DIR)/origins.txt"
>     printf '%s\n' \
>       'Profile audit route:' \
>       '  1. Read PROFILE_AUDIT_GUIDE.md for the bundle reading order.' \
>       '  2. Read portability.txt and mk/contract.mk for tool, shell, and policy boundaries.' \
>       '  3. Read help.txt and TARGET_GUIDE.md to separate stable targets from internal mechanics.' \
>       '  4. Read origins.txt when you need to review variable precedence.' \
>       '  5. Read PROOF_GUIDE.md if you need the matching claim-to-evidence route.' > "$(PROFILE_AUDIT_DIR)/route.txt"
>     printf '%s\n' \
>       'Review questions:' \
>       '  Which runtime assumptions are explicit enough to audit before execution?' \
>       '  Which features depend on GNU Make rather than POSIX shell alone?' \
>       '  Which variable sources would matter if another environment overrides them?' > "$(PROFILE_AUDIT_DIR)/review-questions.txt"
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(PROFILE_AUDIT_DIR)" --output "$(PROFILE_AUDIT_DIR)/manifest.json"
>     @echo "PASS: wrote profile audit to $(PROFILE_AUDIT_DIR)"

# ---- CI-style entrypoints ----
lint:
>     $(call require_tool,clang-tidy)
>     clang-tidy $(SRCS) $(DYN_SRCS) -- $(CPPFLAGS) $(CFLAGS)

test: app dyn
>     $(call assert_stdout_eq,./app,50)
>     $(call assert_stdout_eq,$(BLD_DIR)/bin/dyn1,Hello from generated header)
>     $(call assert_stdout_eq,$(BLD_DIR)/bin/dyn2,42)

dist: all
>     $(PYTHON) scripts/mkdist.py dist.tar.gz app $(BLD_DIR)/bin $(DYN_HDR)

repro:
>     @printf '%s\n' \
>     'Repro pack:' \
>     '  make -f repro/01-shared-log.mk -j2 all       shared mutable log output' \
>     '  make -f repro/01-shared-append.mk -j2 all    alias for older material' \
>     '  make -f repro/02-temp-collision.mk -j2 all   unsafe temp/publication pattern' \
>     '  make -f repro/03-stamp-clobber.mk -j2 all    dishonest stamp boundary' \
>     '  make -f repro/04-generated-header.mk all      generated-file modeling' \
>     '  make -f repro/05-mkdir-race.mk -j2 all       directory creation race' \
>     '  make -f repro/06-order-only-misuse.mk all    order-only prerequisite misuse' \
>     '  make -f repro/07-pattern-ambiguity.mk all    ambiguous pattern rule selection' \
>     '' \
>     'Suggested first route:' \
>     '  1. repro/01-shared-log.mk' \
>     '  2. repro/05-mkdir-race.mk' \
>     '  3. repro/06-order-only-misuse.mk' \
>     '' \
>     'For the capstone teaching route, read REPRO_GUIDE.md' \
>     'For the course route, read course-book/repro-catalog.md'

discovery-audit:
>     printf '%s\n' $(DYN_SRCS) | LC_ALL=C sort -c
>     printf '%s\n' $(SRCS) | LC_ALL=C sort -c

# ---- attestations without contaminating outputs ----
attest: all | $(BLD_DIR)/
>     tmp="$(BLD_DIR)/attest.txt.tmp.$$"; \
>     { \
>       printf 'MAKE=%s\n' "$$($(MAKE) --version | head -1)"; \
>       printf 'OS=%s\n' "$(UNAME_S)"; \
>       printf 'CC=%s\n' "$(CC)"; \
>       printf 'CFLAGS=%s\n' "$(CFLAGS)"; \
>       printf 'CPPFLAGS=%s\n' "$(CPPFLAGS)"; \
>       printf 'LDFLAGS=%s\n' "$(LDFLAGS)"; \
>       printf 'LDLIBS=%s\n' "$(LDLIBS)"; \
>       printf 'TZ=%s\nLC_ALL=%s\n' "$${TZ:-}" "$${LC_ALL:-}"; \
>       cat $(BLD_DIR)/flags.stamp; \
>       test -f stamps/tool/cc.txt && { echo '---'; head -5 stamps/tool/cc.txt; } || true; \
>     } > "$$tmp" && mv -f "$$tmp" "$(BLD_DIR)/attest.txt" || { rm -f "$$tmp"; exit 1; }

# ---- universal truth command ----
selftest:
>     MAKE="$(MAKE)" $(TST_DIR)/run.sh

selftest-report:
>     rm -rf "$(SELFTEST_REPORT_DIR_ABS)"
>     mkdir -p "$(SELFTEST_REPORT_DIR_ABS)"
>     MAKE="$(MAKE)" SELFTEST_REPORT_DIR="$(SELFTEST_REPORT_DIR_ABS)" $(TST_DIR)/run.sh
>     cp SELFTEST_GUIDE.md "$(SELFTEST_REPORT_DIR_ABS)/SELFTEST_GUIDE.md"
>     cp PROOF_GUIDE.md "$(SELFTEST_REPORT_DIR_ABS)/PROOF_GUIDE.md"
>     printf '%s\n' \
>       'Selftest review route:' \
>       '  1. Read summary.txt for the top-level verdict.' \
>       '  2. Read SELFTEST_GUIDE.md for file meanings and review questions.' \
>       '  3. Read PROOF_GUIDE.md for the wider claim-to-evidence route.' \
>       '  4. Read settings.env for the runtime boundary.' \
>       '  5. Compare serial.sum and parallel.sum for schedule equivalence.' \
>       '  6. Read hidden-input.txt for the negative-proof result.' > "$(SELFTEST_REPORT_DIR_ABS)/route.txt"
>     printf '%s\n' \
>       'Bundle surfaces:' \
>       '  SELFTEST_GUIDE.md  reading order and file meanings' \
>       '  summary.txt        top-level verdict surface' \
>       '  settings.env       runtime boundary and guardrail values' \
>       '  serial.sum         serial artifact inventory' \
>       '  parallel.sum       parallel artifact inventory' \
>       '  hidden-input.txt   dishonest-input detection result' > "$(SELFTEST_REPORT_DIR_ABS)/bundle-guide.txt"
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(SELFTEST_REPORT_DIR_ABS)" --output "$(SELFTEST_REPORT_DIR_ABS)/manifest.json"
>     @echo "PASS: wrote selftest report to $(SELFTEST_REPORT_DIR_ABS)"

verify-report: selftest-report
>     @echo "PASS: verify-report completed via $(SELFTEST_REPORT_DIR_ABS)"

proof: walkthrough selftest-report contract-audit incident-audit profile-audit
>     @printf '%s\n' \
>       'PASS: wrote learner-facing proof bundles:' \
>       "  walkthrough: $(WALKTHROUGH_DIR)" \
>       "  selftest report: $(SELFTEST_REPORT_DIR_ABS)" \
>       "  contract audit: $(CONTRACT_AUDIT_DIR)" \
>       "  incident audit: $(INCIDENT_AUDIT_DIR)" \
>       "  profile audit: $(PROFILE_AUDIT_DIR)"

# ---- quarantined rule-generation demo (optional) ----
USE_EVAL ?= no
ifeq ($(USE_EVAL),yes)
include $(MK_DIR)/rules_eval.mk
endif

eval-demo: $(EVAL_DEMO_TARGETS)
>     @echo "eval-demo: built $(EVAL_DEMO_TARGETS)"

# ---- recursion boundary demo (optional) ----
submake-demo:
>     +@$(MAKE) -C thirdparty --no-print-directory
>     @echo "MAKELEVEL=$(MAKELEVEL)"

# ---- portability and feature audit ----
portability-audit:
>     @printf 'GNU Make: %s\n' "$$($(MAKE) --version | head -1)"
>     @printf 'OS: %s\n' "$(UNAME_S)"
>     @printf 'SHELL: %s\n' "$(SHELL)"
>     @printf 'MAKE_VERSION: %s\n' "$(MAKE_VERSION)"
>     @printf 'HAVE_GROUPED_TARGETS: %s\n' "$(HAVE_GROUPED_TARGETS)"
>     @printf 'HAVE_WAIT: %s\n' "$(HAVE_WAIT)"
>     @command -v $(CC) >/dev/null 2>&1 && printf 'CC: %s\n' "$$($(CC) --version 2>/dev/null | head -1)" || printf 'CC: missing\n'
>     @command -v $(PYTHON) >/dev/null 2>&1 && printf 'PYTHON: %s\n' "$$($(PYTHON) --version 2>/dev/null)" || printf 'PYTHON: missing\n'

# ---- measurement hooks (configurable guardrails in selftest; no hard perf gates here) ----
perf:
>     @echo "perf: quick, portable metrics (not a profiler):" >&2
>     @echo "  $(MAKE) trace-count" >&2
>     @echo "  (/usr/bin/time -p $(MAKE) -n all >/dev/null) 2>&1" >&2

trace-count:
>     @$(MAKE) --trace -n all 2>&1 | wc -l | awk '{print "trace-lines=" $$1}'

# ---- hardened build verification ----
hardened: selftest discovery-audit attest test
>     @$(MAKE) -q all || { echo "FAIL: non-convergent" >&2; exit 1; }
>     @echo "PASS: hardened invariants"

confirm: hardened
>     @echo "PASS: confirm route completed"

# ---- source baseline ----
source-baseline-check:
>     @paths=''; \
>     for path in build stamps app all dist.tar.gz; do \
>         if [ -e "$$path" ]; then \
>             paths="$$paths./$$path\n"; \
>         fi; \
>     done; \
>     tmp_paths="$$(find . -type f -print | grep -E '(\.tmp(\..*)?|\.d\.tmp|\.tmp\.d)$$' || true)"; \
>     if [ -n "$$tmp_paths" ]; then \
>         paths="$$paths$$tmp_paths"; \
>     fi; \
>     if [ -n "$$paths" ]; then \
>         printf '%s\n' 'FAIL: source bundle would include local build state:' "$$paths" >&2; \
>         exit 1; \
>     fi; \
>     printf '%s\n' 'PASS: source baseline contains no local build state'

source-bundle: source-baseline-check
>     mkdir -p "$(SOURCE_BUNDLE_DIR)"
>     $(PYTHON) "$(REPO_ROOT)/scripts/build_clean_source_bundle.py" \
>         --repo-root "$(REPO_ROOT)" \
>         --source-dir "$(CURDIR)" \
>         --output "$(abspath $(SOURCE_BUNDLE_PATH))" \
>         --prefix deep-dive-make-capstone
>     printf 'PASS: wrote %s\n' "$(abspath $(SOURCE_BUNDLE_PATH))"

# ---- precedence introspection ----
show:
>     @echo "origin=$(origin CFLAGS) flavor=$(flavor CFLAGS) value='$(value CFLAGS)'"

show-e:
>     @$(MAKE) --no-print-directory -e show

show-origins:
>     @echo "CFLAGS origin=$(origin CFLAGS) flavor=$(flavor CFLAGS)"

clean:
>     rm -rf $(BLD_DIR) stamps app all dist.tar.gz
>     find . -type f \( -name '*.tmp.*' -o -name '*.tmp' -o -name '*.d.tmp' -o -name '*.tmp.d' \) -delete 2>/dev/null || true

FORCE:
