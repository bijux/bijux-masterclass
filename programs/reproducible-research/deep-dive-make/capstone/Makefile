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
DOCS_DIR := docs
ARTIFACTS_DIR ?= ../../../../artifacts
REPO_ROOT := $(abspath ../../../../)
WALKTHROUGH_DIR ?= $(ARTIFACTS_DIR)/walkthrough/reproducible-research/deep-dive-make
TOUR_DIR ?= $(ARTIFACTS_DIR)/tour/reproducible-research/deep-dive-make
SELFTEST_REPORT_DIR ?= $(ARTIFACTS_DIR)/proof/reproducible-research/deep-dive-make/selftest
SELFTEST_WORK_DIR ?= $(SELFTEST_REPORT_DIR)/workspace
SELFTEST_FAULT ?= none
CONTRACT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/contract
INCIDENT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/incident
INCREMENTAL_FAULT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/incremental-faults
SEMANTIC_FAULT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/semantic-faults
ENVIRONMENT_CONTRACT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/environment-contracts
ARCHITECTURE_CONTRACT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/architecture-contracts
ABSTRACTION_CONTRACT_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/abstraction-contracts
PROFILE_AUDIT_DIR ?= $(ARTIFACTS_DIR)/audit/reproducible-research/deep-dive-make/profile
PERFORMANCE_DIR ?= $(ARTIFACTS_DIR)/performance/reproducible-research/deep-dive-make/current
PERFORMANCE_POLICY := performance/scenarios.tsv
INCREMENTAL_POLICY := performance/incremental-policy.tsv
INCREMENTAL_EVIDENCE ?= $(PERFORMANCE_DIR)/incremental-work.json
PERFORMANCE_EVIDENCE ?= $(PERFORMANCE_DIR)/evidence.json
PERFORMANCE_COMPARISON ?= $(PERFORMANCE_DIR)/comparison.json
PERFORMANCE_BASELINE ?=
PERFORMANCE_SAMPLES ?= 5
PERFORMANCE_RUNNER ?= local
TRACE_EVIDENCE_DIR ?= $(ARTIFACTS_DIR)/observability/reproducible-research/deep-dive-make/trace
TRACE_PLAN_MAX ?= 500
SOURCE_BUNDLE_DIR ?= $(ARTIFACTS_DIR)/dist/reproducible-research/deep-dive-make
SOURCE_BUNDLE_PATH ?= $(SOURCE_BUNDLE_DIR)/deep-dive-make-capstone-source.tar.gz
RELEASE_DIR ?= $(ARTIFACTS_DIR)/release/reproducible-research/deep-dive-make
RELEASE_CANDIDATE ?= $(RELEASE_DIR)/candidate/deep-dive-make-capstone.tar.gz
RELEASE_CHECKSUM ?= $(RELEASE_CANDIDATE).sha256
RELEASE_REPORT ?= $(RELEASE_DIR)/evidence/candidate-acceptance.json
RELEASE_INSTALL_ROOT ?= $(RELEASE_DIR)/install-root
RELEASE_INSTALL_REPORT ?= $(RELEASE_DIR)/evidence/install-acceptance.json
RELEASE_ACCEPTANCE ?= $(RELEASE_DIR)/evidence/release-acceptance.json
RELEASE_POLICY := release/package-policy.tsv
RELEASE_INSTALL_POLICY := release/install-policy.tsv
RELEASE_INPUTS = app $(DYN_BINS) $(DYN_HDR)
RELEASE_CANDIDATE_ABS := $(abspath $(RELEASE_CANDIDATE))
RELEASE_CHECKSUM_ABS := $(abspath $(RELEASE_CHECKSUM))
RELEASE_REPORT_ABS := $(abspath $(RELEASE_REPORT))
RELEASE_INSTALL_ROOT_ABS := $(abspath $(RELEASE_INSTALL_ROOT))
RELEASE_INSTALL_REPORT_ABS := $(abspath $(RELEASE_INSTALL_REPORT))
RELEASE_ACCEPTANCE_ABS := $(abspath $(RELEASE_ACCEPTANCE))
SELFTEST_REPORT_DIR_ABS := $(abspath $(SELFTEST_REPORT_DIR))
SELFTEST_WORK_DIR_ABS := $(abspath $(SELFTEST_WORK_DIR))
INCIDENT_CASE ?= all

DEPFLAGS := -MMD -MP

.DEFAULT_GOAL := all
# IMPORTANT: do NOT mark `all` phony; it is a real sentinel file for convergence.
.PHONY: dyn lint test dist verify-dist install-rehearsal accept-release release-check release-selftest selftest-harness-tests repro discovery-audit attest selftest selftest-report verify-report proof walkthrough \
        contract-audit inspect incident-audit incremental-fault-audit semantic-fault-audit semantic-fault-selftest environment-contract-audit environment-contract-selftest architecture-contract-audit architecture-contract-selftest abstraction-contract-audit abstraction-contract-selftest clean submake-demo perf performance-evidence performance-incremental performance-compare performance-selftest trace-report hardened confirm show show-e show-origins FORCE \
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
>     '  dist              write candidate and checksum under artifacts/' \
>     '  verify-dist       verify existing candidate bytes without rebuilding' \
>     '  install-rehearsal prove contained installation and rerun convergence' \
>     '  accept-release    bind candidate and install evidence to one digest' \
>     '  release-check     build, test, and verify one local candidate' \
>     '  release-selftest  prove candidate acceptance and rejection paths' \
>     '  test              run runtime assertions' \
>     '  selftest          convergence + serial/parallel equivalence + negative test' \
>     '  selftest-harness-tests prove selftest acceptance and rejection behavior' \
>     '  selftest-report   write the selftest evidence bundle to artifacts/' \
>     '  verify-report     alias for selftest-report with shared catalog naming' \
>     '  proof             write the sanctioned learner-facing proof bundle set' \
>     '  tour              print the recommended capstone walkthrough' \
>     '  walkthrough       build the learner-facing walkthrough bundle' \
>     '  contract-audit    build the public-contract review bundle' \
>     '  inspect           alias for contract-audit with learner review naming' \
>     '  incident-audit    verify concurrency failure signatures (INCIDENT_CASE=...)' \
>     '  incremental-fault-audit prove stale missing-edge behavior and repaired rebuilds' \
>     '  semantic-fault-audit prove state, edge, and rule-selection semantics' \
>     '  semantic-fault-selftest reject dishonest semantic-audit evidence' \
>     '  environment-contract-audit prove non-file, recursion, and tool contracts' \
>     '  environment-contract-selftest reject dishonest environment evidence' \
>     '  architecture-contract-audit prove API, layer, and output ownership' \
>     '  architecture-contract-selftest reject dishonest architecture evidence' \
>     '  abstraction-contract-audit prove explicit and generated rule contracts' \
>     '  abstraction-contract-selftest reject dishonest abstraction evidence' \
>     '  profile-audit     build the execution-profile review bundle' \
>     '  confirm           alias for hardened with shared catalog naming' \
>     '  discovery-audit   assert deterministic discovery (sorted lists)' \
>     '  repro             show how to run the race repro pack' \
>     '  attest            write build/attest.txt (not a dependency of all)' \
>     '  perf              write governed performance evidence under artifacts/' \
>     '  performance-evidence write the same governed evidence bundle' \
>     '  performance-incremental prove requested work for declared input classes' \
>     '  performance-compare compare current evidence with PERFORMANCE_BASELINE' \
>     '  performance-selftest prove context, rebuild, capture, and comparison gates' \
>     '  trace-report      write bounded, attributable clean-plan trace evidence' \
>     '  portability-audit probe tool/feature availability' \
>     '  eval-demo         optional quarantined eval demo (USE_EVAL=yes)' \
>     '' \
>     'Variables:' \
>     '  DEBUG=1           enable debug symbols (-g)' \
>     '  J=4               parallelism used by some commands' \
>     '  TRACE_PLAN_MAX=500 maximum clean-plan trace volume' \
>     '  PERFORMANCE_SAMPLES=5 repeated samples per governed scenario' \
>     '  PERFORMANCE_BASELINE=path evidence JSON required by performance-compare' \
>     '  PERFORMANCE_RUNNER=local stable label for the execution environment' \
>     '  SELFTEST_FAULT=none controlled harness-test seam; not for ordinary proof' \
>     ''

tour:
>     rm -rf "$(TOUR_DIR)"
>     mkdir -p "$(TOUR_DIR)/mk" "$(TOUR_DIR)/repro" "$(TOUR_DIR)/tests"
>     cp README.md "$(TOUR_DIR)/README.md"
>     cp $(DOCS_DIR)/architecture.md "$(TOUR_DIR)/ARCHITECTURE.md"
>     cp $(DOCS_DIR)/index.md "$(TOUR_DIR)/INDEX.md"
>     cp $(DOCS_DIR)/proof-guide.md "$(TOUR_DIR)/PROOF_GUIDE.md"
>     cp $(DOCS_DIR)/selftest-guide.md "$(TOUR_DIR)/SELFTEST_GUIDE.md"
>     cp $(DOCS_DIR)/release-guide.md "$(TOUR_DIR)/RELEASE_GUIDE.md"
>     cp $(DOCS_DIR)/target-guide.md "$(TOUR_DIR)/TARGET_GUIDE.md"
>     cp $(DOCS_DIR)/walkthrough-guide.md "$(TOUR_DIR)/WALKTHROUGH_GUIDE.md"
>     cp $(DOCS_DIR)/repro-guide.md "$(TOUR_DIR)/REPRO_GUIDE.md"
>     cp Makefile "$(TOUR_DIR)/Makefile"
>     cp $(TST_DIR)/run.sh "$(TOUR_DIR)/tests/run.sh"
>     cp $(MK_DIR)/contract.mk "$(TOUR_DIR)/mk/contract.mk"
>     cp $(MK_DIR)/common.mk "$(TOUR_DIR)/mk/common.mk"
>     cp $(MK_DIR)/objects.mk "$(TOUR_DIR)/mk/objects.mk"
>     cp $(MK_DIR)/stamps.mk "$(TOUR_DIR)/mk/stamps.mk"
>     cp $(REP_DIR)/shared-log-interleaving.mk "$(TOUR_DIR)/repro/shared-log-interleaving.mk"
>     $(MAKE) help > "$(TOUR_DIR)/help.txt"
>     $(MAKE) trace-report
>     printf '%s\n' \
>       'Tour route:' \
>       '  1. Read INDEX.md for the smallest local route.' \
>       '  2. Read README.md for the repository contract.' \
>       '  3. Read TARGET_GUIDE.md for the stable public interface.' \
>       '  4. Read PROOF_GUIDE.md for claim-to-evidence routing.' \
>       '  5. Read ARCHITECTURE.md and WALKTHROUGH_GUIDE.md for ownership and first-pass order.' \
>       '  6. Read RELEASE_GUIDE.md when the question is candidate acceptance.' \
>       '  7. Read SELFTEST_GUIDE.md and tests/run.sh for the reviewable proof route.' \
>       '  8. Run trace-report for bounded, attributable planning evidence.' \
>       '  9. Inspect REPRO_GUIDE.md and repro/shared-log-interleaving.mk for the first incident surface.' > "$(TOUR_DIR)/route.txt"
>     printf '%s\n' \
>       'Focused routes:' \
>       '  generators   -> make --trace dyn' \
>       '  architecture -> read mk/contract.mk, mk/objects.mk, mk/stamps.mk' \
>       '  incidents    -> make -f repro/shared-log-interleaving.mk -j2 all' \
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
>     '  incidents    -> make trace-report && make -f repro/shared-log-interleaving.mk -j2 all'
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(TOUR_DIR)" --output "$(TOUR_DIR)/manifest.json"

walkthrough:
>     rm -rf "$(WALKTHROUGH_DIR)"
>     mkdir -p "$(WALKTHROUGH_DIR)/repro" "$(WALKTHROUGH_DIR)/tests" "$(WALKTHROUGH_DIR)/mk"
>     cp README.md "$(WALKTHROUGH_DIR)/README.md"
>     cp $(DOCS_DIR)/architecture.md "$(WALKTHROUGH_DIR)/ARCHITECTURE.md"
>     cp $(DOCS_DIR)/index.md "$(WALKTHROUGH_DIR)/INDEX.md"
>     cp $(DOCS_DIR)/proof-guide.md "$(WALKTHROUGH_DIR)/PROOF_GUIDE.md"
>     cp $(DOCS_DIR)/selftest-guide.md "$(WALKTHROUGH_DIR)/SELFTEST_GUIDE.md"
>     cp $(DOCS_DIR)/release-guide.md "$(WALKTHROUGH_DIR)/RELEASE_GUIDE.md"
>     cp $(DOCS_DIR)/target-guide.md "$(WALKTHROUGH_DIR)/TARGET_GUIDE.md"
>     cp $(DOCS_DIR)/walkthrough-guide.md "$(WALKTHROUGH_DIR)/WALKTHROUGH_GUIDE.md"
>     cp Makefile "$(WALKTHROUGH_DIR)/Makefile"
>     cp $(TST_DIR)/run.sh "$(WALKTHROUGH_DIR)/tests/run.sh"
>     cp $(MK_DIR)/contract.mk "$(WALKTHROUGH_DIR)/mk/contract.mk"
>     cp $(MK_DIR)/common.mk "$(WALKTHROUGH_DIR)/mk/common.mk"
>     cp $(MK_DIR)/objects.mk "$(WALKTHROUGH_DIR)/mk/objects.mk"
>     cp $(MK_DIR)/stamps.mk "$(WALKTHROUGH_DIR)/mk/stamps.mk"
>     cp $(REP_DIR)/shared-log-interleaving.mk "$(WALKTHROUGH_DIR)/repro/shared-log-interleaving.mk"
>     printf '%s\n' \
>       '1. Read INDEX.md to choose the smallest honest entry route.' \
>       '2. Read WALKTHROUGH_GUIDE.md to understand the recommended first pass.' \
>       '3. Read README.md and TARGET_GUIDE.md to understand the capstone contract and public targets.' \
>       '4. Read PROOF_GUIDE.md, SELFTEST_GUIDE.md, and tests/run.sh to see what selftest is proving.' \
>       '5. Read RELEASE_GUIDE.md when you need the candidate acceptance route.' \
>       '6. Read ARCHITECTURE.md and mk/contract.mk for ownership and boundary design.' \
>       '7. Read mk/objects.mk and mk/stamps.mk for graph truth and modeled hidden inputs.' \
>       '8. Run make help in the capstone directory.' \
>       '9. Run make selftest when you want executed proof.' \
>       '10. Inspect repro/shared-log-interleaving.mk as the first failure class.' > "$(WALKTHROUGH_DIR)/route.txt"
>     printf '%s\n' \
>       'Public entry commands:' \
>       '  make help' \
>       '  make selftest' \
>       '  make repro' \
>       '  make hardened' > "$(WALKTHROUGH_DIR)/commands.txt"
>     printf '%s\n' \
>       'Walkthrough bundle surfaces:' \
>       '  README.md            repository contract and program fit' \
>       '  INDEX.md             stable local route into the capstone docs' \
>       '  TARGET_GUIDE.md      stable public target surface' \
>       '  PROOF_GUIDE.md       claim-to-evidence routing' \
>       '  SELFTEST_GUIDE.md    passing and failing selftest evidence route' \
>       '  RELEASE_GUIDE.md     candidate acceptance and rejection route' \
>       '  WALKTHROUGH_GUIDE.md bounded first-pass reading order' \
>       '  ARCHITECTURE.md      layer ownership and system map' \
>       '  Makefile             stable public target surface' \
>       '  tests/run.sh         selftest proof harness' \
>       '  mk/contract.mk       platform and policy boundaries' \
>       '  mk/objects.mk        rooted discovery and object modeling' \
>       '  mk/stamps.mk         build-state evidence surfaces' \
>       '  repro/shared-log-interleaving.mk first concurrency failure route' > "$(WALKTHROUGH_DIR)/bundle-guide.txt"
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(WALKTHROUGH_DIR)" --output "$(WALKTHROUGH_DIR)/manifest.json"
>     @echo "PASS: wrote capstone walkthrough to $(WALKTHROUGH_DIR)"

contract-audit:
>     rm -rf "$(CONTRACT_AUDIT_DIR)"
>     mkdir -p "$(CONTRACT_AUDIT_DIR)/tests"
>     cp README.md "$(CONTRACT_AUDIT_DIR)/README.md"
>     cp $(DOCS_DIR)/contract-audit-guide.md "$(CONTRACT_AUDIT_DIR)/CONTRACT_AUDIT_GUIDE.md"
>     cp $(DOCS_DIR)/proof-guide.md "$(CONTRACT_AUDIT_DIR)/PROOF_GUIDE.md"
>     cp $(DOCS_DIR)/target-guide.md "$(CONTRACT_AUDIT_DIR)/TARGET_GUIDE.md"
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
>     mkdir -p "$(INCIDENT_AUDIT_DIR)/specimens"
>     $(PYTHON) scripts/audit_incident_signatures.py \
>       --repro-dir "$(REP_DIR)" \
>       --workspace "$(INCIDENT_AUDIT_DIR)/workspace" \
>       --output "$(INCIDENT_AUDIT_DIR)/report.json" \
>       --make "$(MAKE)" \
>       --case "$(INCIDENT_CASE)"
>     cp "$(REP_DIR)/shared-log-interleaving.mk" "$(INCIDENT_AUDIT_DIR)/specimens/"
>     cp "$(REP_DIR)/directory-creation-race.mk" "$(INCIDENT_AUDIT_DIR)/specimens/"
>     cp "$(REP_DIR)/shared-staging-collision.mk" "$(INCIDENT_AUDIT_DIR)/specimens/"
>     cp $(DOCS_DIR)/incident-review-guide.md "$(INCIDENT_AUDIT_DIR)/INCIDENT_REVIEW_GUIDE.md"
>     printf '%s\n' \
>       'Incident audit route:' \
>       '  1. Read INCIDENT_REVIEW_GUIDE.md for the incident reading order.' \
>       '  2. Read summary.tsv before opening the complete report.json.' \
>       '  3. Compare each raw run log with its preserved semantic evidence.' \
>       '  4. Inspect workspace/ and specimens/ to connect behavior to graph ownership.' \
>       '  5. Read REPRO_GUIDE.md for repairs and PROOF_GUIDE.md for production proof.' > "$(INCIDENT_AUDIT_DIR)/route.txt"
>     printf '%s\n' \
>       'Repair surfaces:' \
>       '  shared log       private worker records plus one deterministic merge owner' \
>       '  directory race   one directory target used as an order-only prerequisite' \
>       '  staging clash    private staging paths plus one publication owner' \
>       '  REPRO_GUIDE.md   maps each failure class to its repair pattern' \
>       '  PROOF_GUIDE.md   maps repaired claims to production proof surfaces' > "$(INCIDENT_AUDIT_DIR)/repair-surfaces.txt"
>     cp $(DOCS_DIR)/repro-guide.md "$(INCIDENT_AUDIT_DIR)/REPRO_GUIDE.md"
>     cp $(DOCS_DIR)/proof-guide.md "$(INCIDENT_AUDIT_DIR)/PROOF_GUIDE.md"
>     $(PYTHON) scripts/write_bundle_manifest.py --bundle-dir "$(INCIDENT_AUDIT_DIR)" --output "$(INCIDENT_AUDIT_DIR)/manifest.json"
>     @echo "PASS: verified incident signatures in $(INCIDENT_AUDIT_DIR)"

incremental-fault-audit:
>     rm -rf "$(INCREMENTAL_FAULT_AUDIT_DIR)"
>     mkdir -p "$(INCREMENTAL_FAULT_AUDIT_DIR)"
>     cp -R "$(REP_DIR)/incremental-edges" "$(INCREMENTAL_FAULT_AUDIT_DIR)/specimens"
>     cp "$(DOCS_DIR)/incremental-fault-audit-guide.md" "$(INCREMENTAL_FAULT_AUDIT_DIR)/INCREMENTAL_FAULT_AUDIT_GUIDE.md"
>     cp "$(DOCS_DIR)/repro-guide.md" "$(INCREMENTAL_FAULT_AUDIT_DIR)/REPRO_GUIDE.md"
>     $(PYTHON) scripts/audit_incremental_faults.py \
>       --specimens "$(REP_DIR)/incremental-edges" \
>       --workspace "$(abspath $(INCREMENTAL_FAULT_AUDIT_DIR))/workspace" \
>       --output "$(abspath $(INCREMENTAL_FAULT_AUDIT_DIR))/report.json" \
>       --make "$(MAKE)" \
>       --compiler "$(CC)" \
>       --python "$(PYTHON)"
>     printf '%s\n' \
>       'Incremental fault audit route:' \
>       '  1. Read INCREMENTAL_FAULT_AUDIT_GUIDE.md for the claim and PASS semantics.' \
>       '  2. Read summary.tsv across both specimens and both edge models.' \
>       '  3. Read report.json for expected and observed outputs.' \
>       '  4. Read traces/ to contrast no selected work with causal rebuild paths.' \
>       '  5. Compare specimens/ with the mutated workspace/ copies.' \
>       '  6. Read REPRO_GUIDE.md to connect the fault to graph repair.' > "$(INCREMENTAL_FAULT_AUDIT_DIR)/route.txt"
>     $(PYTHON) scripts/write_bundle_manifest.py \
>       --bundle-dir "$(INCREMENTAL_FAULT_AUDIT_DIR)" \
>       --output "$(INCREMENTAL_FAULT_AUDIT_DIR)/manifest.json"
>     @echo "PASS: wrote incremental fault audit to $(INCREMENTAL_FAULT_AUDIT_DIR)"

semantic-fault-audit:
>     rm -rf "$(SEMANTIC_FAULT_AUDIT_DIR)"
>     mkdir -p "$(SEMANTIC_FAULT_AUDIT_DIR)"
>     cp -R "$(REP_DIR)/semantic-faults" "$(SEMANTIC_FAULT_AUDIT_DIR)/specimens"
>     $(PYTHON) scripts/audit_semantic_faults.py \
>       --specimens "$(REP_DIR)/semantic-faults" \
>       --workspace "$(SEMANTIC_FAULT_AUDIT_DIR)/workspace" \
>       --output "$(SEMANTIC_FAULT_AUDIT_DIR)/report.json" \
>       --make "$(MAKE)" \
>       --python "$(PYTHON)"
>     printf '%s\n' \
>       'Semantic fault audit route:' \
>       '  1. Read SEMANTIC_FAULT_AUDIT_GUIDE.md for PASS semantics and comparison order.' \
>       '  2. Read summary.tsv across all seven broken and control models.' \
>       '  3. Read report.json for exact stability, freshness, and selection observations.' \
>       '  4. Read traces/ to connect each observation to selected Make rules.' \
>       '  5. Compare specimens/ with workspace/, then use the repro and proof guides.' > "$(SEMANTIC_FAULT_AUDIT_DIR)/route.txt"
>     cp "$(DOCS_DIR)/semantic-fault-audit-guide.md" "$(SEMANTIC_FAULT_AUDIT_DIR)/SEMANTIC_FAULT_AUDIT_GUIDE.md"
>     cp "$(DOCS_DIR)/repro-guide.md" "$(SEMANTIC_FAULT_AUDIT_DIR)/REPRO_GUIDE.md"
>     cp "$(DOCS_DIR)/proof-guide.md" "$(SEMANTIC_FAULT_AUDIT_DIR)/PROOF_GUIDE.md"
>     $(PYTHON) scripts/write_bundle_manifest.py \
>       --bundle-dir "$(SEMANTIC_FAULT_AUDIT_DIR)" \
>       --output "$(SEMANTIC_FAULT_AUDIT_DIR)/manifest.json"
>     @echo "PASS: wrote semantic fault audit to $(SEMANTIC_FAULT_AUDIT_DIR)"

semantic-fault-selftest:
>     $(PYTHON) -m unittest $(TST_DIR)/test_semantic_fault_audit.py

environment-contract-audit:
>     rm -rf "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)"
>     mkdir -p "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)"
>     cp -R "$(REP_DIR)/environment-contracts" "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)/specimens"
>     $(PYTHON) scripts/audit_environment_contracts.py \
>       --specimens "$(REP_DIR)/environment-contracts" \
>       --workspace "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)/workspace" \
>       --output "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)/report.json" \
>       --make "$(MAKE)" \
>       --python "$(PYTHON)"
>     printf '%s\n' \
>       'Environment contract audit route:' \
>       '  1. Read ENVIRONMENT_CONTRACT_AUDIT_GUIDE.md for PASS semantics and comparison order.' \
>       '  2. Read summary.tsv across all seven broken and control models.' \
>       '  3. Read report.json for exact state, recursion, and tool observations.' \
>       '  4. Read traces/ to connect each observation to Make execution.' \
>       '  5. Compare specimens/ with workspace/, then use the repro and proof guides.' > "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)/route.txt"
>     cp "$(DOCS_DIR)/environment-contract-audit-guide.md" "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)/ENVIRONMENT_CONTRACT_AUDIT_GUIDE.md"
>     cp "$(DOCS_DIR)/repro-guide.md" "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)/REPRO_GUIDE.md"
>     cp "$(DOCS_DIR)/proof-guide.md" "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)/PROOF_GUIDE.md"
>     $(PYTHON) scripts/write_bundle_manifest.py \
>       --bundle-dir "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)" \
>       --output "$(ENVIRONMENT_CONTRACT_AUDIT_DIR)/manifest.json"
>     @echo "PASS: wrote environment contract audit to $(ENVIRONMENT_CONTRACT_AUDIT_DIR)"

environment-contract-selftest:
>     $(PYTHON) -m unittest $(TST_DIR)/test_environment_contract_audit.py

architecture-contract-audit:
>     rm -rf "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)"
>     mkdir -p "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)"
>     cp -R "$(REP_DIR)/architecture-contracts" "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)/specimens"
>     $(PYTHON) scripts/audit_architecture_contracts.py \
>       --specimens "$(REP_DIR)/architecture-contracts" \
>       --workspace "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)/workspace" \
>       --output "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)/report.json" \
>       --make "$(MAKE)"
>     printf '%s\n' \
>       'Architecture contract audit route:' \
>       '  1. Read ARCHITECTURE_CONTRACT_AUDIT_GUIDE.md for PASS semantics.' \
>       '  2. Read summary.tsv across all six broken and control models.' \
>       '  3. Read report.json for exact API, policy, and output observations.' \
>       '  4. Read traces/ to connect each observation to Make execution.' \
>       '  5. Compare specimens/ with workspace/ before proposing a refactor.' > "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)/route.txt"
>     cp "$(DOCS_DIR)/architecture-contract-audit-guide.md" "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)/ARCHITECTURE_CONTRACT_AUDIT_GUIDE.md"
>     cp "$(DOCS_DIR)/repro-guide.md" "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)/REPRO_GUIDE.md"
>     cp "$(DOCS_DIR)/proof-guide.md" "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)/PROOF_GUIDE.md"
>     $(PYTHON) scripts/write_bundle_manifest.py \
>       --bundle-dir "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)" \
>       --output "$(ARCHITECTURE_CONTRACT_AUDIT_DIR)/manifest.json"
>     @echo "PASS: wrote architecture contract audit to $(ARCHITECTURE_CONTRACT_AUDIT_DIR)"

architecture-contract-selftest:
>     $(PYTHON) -m unittest $(TST_DIR)/test_architecture_contract_audit.py

abstraction-contract-audit:
>     rm -rf "$(ABSTRACTION_CONTRACT_AUDIT_DIR)"
>     mkdir -p "$(ABSTRACTION_CONTRACT_AUDIT_DIR)"
>     cp -R "$(REP_DIR)/abstraction-contracts" "$(ABSTRACTION_CONTRACT_AUDIT_DIR)/specimens"
>     $(PYTHON) scripts/audit_abstraction_contracts.py \
>       --specimens "$(REP_DIR)/abstraction-contracts" \
>       --workspace "$(ABSTRACTION_CONTRACT_AUDIT_DIR)/workspace" \
>       --output "$(ABSTRACTION_CONTRACT_AUDIT_DIR)/report.json" \
>       --make "$(MAKE)"
>     printf '%s\n' \
>       'Abstraction contract audit route:' \
>       '  1. Read ABSTRACTION_CONTRACT_AUDIT_GUIDE.md for PASS semantics.' \
>       '  2. Read summary.tsv across the explicit, bounded, and opaque models.' \
>       '  3. Read report.json for rule, target, policy, and artifact observations.' \
>       '  4. Read contract and database traces before the complete build trace.' \
>       '  5. Compare specimens/ with workspace/ before accepting a macro.' > "$(ABSTRACTION_CONTRACT_AUDIT_DIR)/route.txt"
>     cp "$(DOCS_DIR)/abstraction-contract-audit-guide.md" "$(ABSTRACTION_CONTRACT_AUDIT_DIR)/ABSTRACTION_CONTRACT_AUDIT_GUIDE.md"
>     cp "$(DOCS_DIR)/proof-guide.md" "$(ABSTRACTION_CONTRACT_AUDIT_DIR)/PROOF_GUIDE.md"
>     $(PYTHON) scripts/write_bundle_manifest.py \
>       --bundle-dir "$(ABSTRACTION_CONTRACT_AUDIT_DIR)" \
>       --output "$(ABSTRACTION_CONTRACT_AUDIT_DIR)/manifest.json"
>     @echo "PASS: wrote abstraction contract audit to $(ABSTRACTION_CONTRACT_AUDIT_DIR)"

abstraction-contract-selftest:
>     $(PYTHON) -m unittest $(TST_DIR)/test_abstraction_contract_audit.py

profile-audit:
>     rm -rf "$(PROFILE_AUDIT_DIR)"
>     mkdir -p "$(PROFILE_AUDIT_DIR)/mk"
>     cp README.md "$(PROFILE_AUDIT_DIR)/README.md"
>     cp $(DOCS_DIR)/profile-audit-guide.md "$(PROFILE_AUDIT_DIR)/PROFILE_AUDIT_GUIDE.md"
>     cp $(DOCS_DIR)/proof-guide.md "$(PROFILE_AUDIT_DIR)/PROOF_GUIDE.md"
>     cp $(DOCS_DIR)/target-guide.md "$(PROFILE_AUDIT_DIR)/TARGET_GUIDE.md"
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

dist: $(RELEASE_CANDIDATE) $(RELEASE_CHECKSUM)
>     @printf 'PASS: wrote release candidate %s\n' "$(RELEASE_CANDIDATE_ABS)"

$(RELEASE_CANDIDATE): $(RELEASE_INPUTS) $(RELEASE_POLICY) scripts/mkdist.py scripts/release_policy.py
>     $(PYTHON) scripts/mkdist.py --policy "$(RELEASE_POLICY)" --output "$(RELEASE_CANDIDATE_ABS)"

$(RELEASE_CHECKSUM): $(RELEASE_CANDIDATE) scripts/write_release_checksum.py
>     $(PYTHON) scripts/write_release_checksum.py \
>       --candidate "$(RELEASE_CANDIDATE_ABS)" \
>       --output "$(RELEASE_CHECKSUM_ABS)"

verify-dist:
>     $(PYTHON) scripts/verify_release_candidate.py \
>       --candidate "$(RELEASE_CANDIDATE_ABS)" \
>       --checksum "$(RELEASE_CHECKSUM_ABS)" \
>       --policy "$(RELEASE_POLICY)" \
>       --report "$(RELEASE_REPORT_ABS)"

install-rehearsal:
>     $(PYTHON) scripts/rehearse_release_install.py \
>       --candidate "$(RELEASE_CANDIDATE_ABS)" \
>       --acceptance "$(RELEASE_REPORT_ABS)" \
>       --package-policy "$(RELEASE_POLICY)" \
>       --install-policy "$(RELEASE_INSTALL_POLICY)" \
>       --root "$(RELEASE_INSTALL_ROOT_ABS)" \
>       --report "$(RELEASE_INSTALL_REPORT_ABS)"

accept-release:
>     $(PYTHON) scripts/write_release_acceptance.py \
>       --candidate-report "$(RELEASE_REPORT_ABS)" \
>       --install-report "$(RELEASE_INSTALL_REPORT_ABS)" \
>       --output "$(RELEASE_ACCEPTANCE_ABS)"

release-check: test selftest release-selftest dist
>     @$(MAKE) --no-print-directory verify-dist
>     @$(MAKE) --no-print-directory install-rehearsal
>     @$(MAKE) --no-print-directory accept-release
>     @echo "PASS: local release candidate accepted"

release-selftest:
>     $(PYTHON) -m unittest discover -s $(TST_DIR) -p 'test_release_*.py'

repro:
>     @printf '%s\n' \
>     'Repro pack:' \
>     '  make -f repro/shared-log-interleaving.mk -j2 all       shared mutable log output' \
>     '  make -f repro/shared-staging-collision.mk -j2 all      shared staging-path collision' \
>     '  make -f repro/directory-creation-race.mk -j2 all       directory creation race' \
>     '  make incremental-fault-audit                             missing-edge versus declared-edge proof' \
>     '  make semantic-fault-audit                                state, order-only, and pattern-selection proof' \
>     '  make environment-contract-audit                           non-file, recursion, and required-tool proof' \
>     '' \
>     'Suggested first route:' \
>     '  1. repro/shared-log-interleaving.mk' \
>     '  2. repro/directory-creation-race.mk' \
>     '  3. semantic-fault-audit' \
>     '' \
>     'For the capstone teaching route, read docs/repro-guide.md' \
>     'For the course route, read docs/repro-guide.md'

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
>     rm -rf "$(SELFTEST_REPORT_DIR_ABS)"
>     mkdir -p "$(SELFTEST_REPORT_DIR_ABS)"
>     MAKE="$(MAKE)" \
>       PYTHON="$(PYTHON)" \
>       SELFTEST_FAULT="$(SELFTEST_FAULT)" \
>       SELFTEST_REPORT_DIR="$(SELFTEST_REPORT_DIR_ABS)" \
>       SELFTEST_WORK_DIR="$(SELFTEST_WORK_DIR_ABS)" \
>       $(TST_DIR)/run.sh

selftest-harness-tests:
>     $(PYTHON) -m unittest $(TST_DIR)/test_selftest_harness.py

selftest-report:
>     rm -rf "$(SELFTEST_REPORT_DIR_ABS)"
>     mkdir -p "$(SELFTEST_REPORT_DIR_ABS)"
>     status=0; \
>       MAKE="$(MAKE)" \
>       PYTHON="$(PYTHON)" \
>       SELFTEST_FAULT="$(SELFTEST_FAULT)" \
>       SELFTEST_REPORT_DIR="$(SELFTEST_REPORT_DIR_ABS)" \
>       SELFTEST_WORK_DIR="$(SELFTEST_WORK_DIR_ABS)" \
>       $(TST_DIR)/run.sh || status=$$?; \
>       $(PYTHON) scripts/write_selftest_bundle.py \
>         --report-dir "$(SELFTEST_REPORT_DIR_ABS)" \
>         --selftest-guide "$(DOCS_DIR)/selftest-guide.md" \
>         --proof-guide "$(DOCS_DIR)/proof-guide.md"; \
>       if [ "$$status" -ne 0 ]; then \
>         echo "FAIL: preserved selftest report at $(SELFTEST_REPORT_DIR_ABS)" >&2; \
>         exit "$$status"; \
>       fi
>     @echo "PASS: wrote selftest report to $(SELFTEST_REPORT_DIR_ABS)"

verify-report: selftest-report
>     @echo "PASS: verify-report completed via $(SELFTEST_REPORT_DIR_ABS)"

proof: walkthrough selftest-report contract-audit incident-audit incremental-fault-audit semantic-fault-audit environment-contract-audit architecture-contract-audit profile-audit
>     @printf '%s\n' \
>       'PASS: wrote learner-facing proof bundles:' \
>       "  walkthrough: $(WALKTHROUGH_DIR)" \
>       "  selftest report: $(SELFTEST_REPORT_DIR_ABS)" \
>       "  contract audit: $(CONTRACT_AUDIT_DIR)" \
>       "  incident audit: $(INCIDENT_AUDIT_DIR)" \
>       "  incremental fault audit: $(INCREMENTAL_FAULT_AUDIT_DIR)" \
>       "  semantic fault audit: $(SEMANTIC_FAULT_AUDIT_DIR)" \
>       "  environment contract audit: $(ENVIRONMENT_CONTRACT_AUDIT_DIR)" \
>       "  architecture contract audit: $(ARCHITECTURE_CONTRACT_AUDIT_DIR)" \
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

# ---- governed performance evidence (no universal timing gates) ----
perf: performance-evidence
>     @printf 'PASS: performance evidence is reviewable at %s\n' "$(abspath $(PERFORMANCE_DIR))"

performance-evidence:
>     rm -rf "$(PERFORMANCE_DIR)"
>     mkdir -p "$(PERFORMANCE_DIR)"
>     cp "$(PERFORMANCE_POLICY)" "$(PERFORMANCE_DIR)/scenarios.tsv"
>     cp "$(INCREMENTAL_POLICY)" "$(PERFORMANCE_DIR)/incremental-policy.tsv"
>     cp "$(DOCS_DIR)/performance-evidence-guide.md" "$(PERFORMANCE_DIR)/PERFORMANCE_EVIDENCE_GUIDE.md"
>     printf '%s\n' \
>       'Performance evidence route:' \
>       '  1. Read PERFORMANCE_EVIDENCE_GUIDE.md for the question, limits, and comparison rules.' \
>       '  2. Read scenarios.tsv and incremental-policy.tsv for the experiment contracts.' \
>       '  3. Read incremental-summary.tsv across all declared input classes.' \
>       '  4. Use incremental-work.json for per-case traces, missing work, and unexpected work.' \
>       '  5. Read evidence.json for provenance, bound requested work, raw samples, and trusted outputs.' \
>       '  6. Read summary.tsv and logs/ only after compatibility and semantics are established.' \
>       '  7. Read manifest.json to review the complete bundle.' > "$(PERFORMANCE_DIR)/route.txt"
>     $(MAKE) --no-print-directory performance-incremental
>     $(PYTHON) scripts/collect_performance_evidence.py \
>       --policy "$(PERFORMANCE_POLICY)" \
>       --output "$(abspath $(PERFORMANCE_EVIDENCE))" \
>       --samples "$(PERFORMANCE_SAMPLES)" \
>       --make "$(MAKE)" \
>       --compiler "$(CC)" \
>       --incremental-evidence "$(abspath $(INCREMENTAL_EVIDENCE))" \
>       --runner-label "$(PERFORMANCE_RUNNER)"
>     $(PYTHON) scripts/write_bundle_manifest.py \
>       --bundle-dir "$(PERFORMANCE_DIR)" \
>       --output "$(PERFORMANCE_DIR)/manifest.json"

performance-incremental:
>     $(PYTHON) scripts/capture_incremental_work.py \
>       --policy "$(INCREMENTAL_POLICY)" \
>       --output "$(abspath $(INCREMENTAL_EVIDENCE))" \
>       --make "$(MAKE)"

performance-compare:
>     test -n "$(PERFORMANCE_BASELINE)" || { \
>       printf '%s\n' 'FAIL: PERFORMANCE_BASELINE must name a prior evidence.json' >&2; \
>       exit 2; \
>     }
>     $(PYTHON) scripts/compare_performance_evidence.py \
>       --baseline "$(PERFORMANCE_BASELINE)" \
>       --candidate "$(abspath $(PERFORMANCE_EVIDENCE))" \
>       --output "$(abspath $(PERFORMANCE_COMPARISON))"
>     $(PYTHON) scripts/write_bundle_manifest.py \
>       --bundle-dir "$(PERFORMANCE_DIR)" \
>       --output "$(PERFORMANCE_DIR)/manifest.json"

performance-selftest:
>     $(PYTHON) -m unittest discover -s $(TST_DIR) -p 'test_execution_context.py'
>     $(PYTHON) -m unittest discover -s $(TST_DIR) -p 'test_incremental_*.py'
>     $(PYTHON) -m unittest discover -s $(TST_DIR) -p 'test_performance_*.py'

trace-report:
>     rm -rf "$(TRACE_EVIDENCE_DIR)"
>     mkdir -p "$(TRACE_EVIDENCE_DIR)"
>     $(MAKE) --no-print-directory clean
>     $(MAKE) --no-print-directory --trace -n all > "$(TRACE_EVIDENCE_DIR)/trace.log" 2>&1
>     $(PYTHON) scripts/analyze_trace_evidence.py \
>       --trace "$(TRACE_EVIDENCE_DIR)/trace.log" \
>       --output "$(TRACE_EVIDENCE_DIR)/trace-evidence.json" \
>       --route all --state clean-plan --focus all \
>       --maximum-lines "$(TRACE_PLAN_MAX)"
>     $(PYTHON) scripts/write_bundle_manifest.py \
>       --bundle-dir "$(TRACE_EVIDENCE_DIR)" \
>       --output "$(TRACE_EVIDENCE_DIR)/manifest.json"

# ---- hardened build verification ----
hardened: selftest selftest-harness-tests incremental-fault-audit semantic-fault-audit semantic-fault-selftest environment-contract-audit environment-contract-selftest architecture-contract-audit architecture-contract-selftest discovery-audit attest test release-check
>     @$(MAKE) -q all || { echo "FAIL: non-convergent" >&2; exit 1; }
>     @echo "PASS: hardened invariants"

confirm: hardened
>     @echo "PASS: confirm route completed"

# ---- source baseline ----
source-baseline-check:
>     @paths=''; \
>     for path in build stamps app all; do \
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
>     rm -rf $(BLD_DIR) stamps app all
>     find . -type f \( -name '*.tmp.*' -o -name '*.tmp' -o -name '*.d.tmp' -o -name '*.tmp.d' \) -delete 2>/dev/null || true

FORCE:
