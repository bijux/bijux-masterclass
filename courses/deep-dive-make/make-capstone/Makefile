# Capstone Repository — Make & Makefiles Deep Dive
# Final state after Modules 01–05 (GNU Make ≥ 4.3; POSIX /bin/sh)

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

DEPFLAGS := -MMD -MP

.DEFAULT_GOAL := all
# IMPORTANT: do NOT mark `all` phony; it is a real sentinel file for convergence.
.PHONY: dyn lint test dist repro discovery-audit attest selftest \
        clean submake-demo perf trace-count hardened show-origins FORCE \
        portability-audit eval-demo help

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

# ---- module 03: codegen + dynamic binaries ----
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
>     '  test              run runtime assertions' \
>     '  selftest          convergence + serial/parallel equivalence + negative test' \
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
>     @echo "repro: run the race repro pack directly, e.g.:" >&2
>     @echo "  make -f $(REP_DIR)/01-shared-log.mk -j2 all" >&2
>     @echo "  make -f $(REP_DIR)/01-shared-append.mk -j2 all  # alias/back-compat" >&2

discovery-audit:
>     printf '%s\n' $(DYN_SRCS) | LC_ALL=C sort -c
>     printf '%s\n' $(SRCS) | LC_ALL=C sort -c

# ---- hardening (module 05): attestations without contaminating outputs ----
attest: all | $(BLD_DIR)/
>     $(call atomic_write,$(BLD_DIR)/attest.txt, \
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
>     )

# ---- universal truth command ----
selftest:
>     MAKE="$(MAKE)" $(TST_DIR)/run.sh

# ---- quarantined eval demo (Module 03B, optional) ----
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

# ---- portability / feature audit (Module 05: explicit contract) ----
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

# ---- module 05 checklist verification ----
hardened: selftest discovery-audit attest test
>     @$(MAKE) -q all || { echo "FAIL: non-convergent" >&2; exit 1; }
>     @echo "PASS: hardened invariants"

# ---- module 04: precedence introspection ----
show-origins:
>     @echo "CFLAGS origin=$(origin CFLAGS) flavor=$(flavor CFLAGS)"

clean:
>     rm -rf $(BLD_DIR) stamps app all dist.tar.gz
>     find . -type f \( -name '*.tmp.*' -o -name '*.tmp' -o -name '*.d.tmp' -o -name '*.tmp.d' \) -delete 2>/dev/null || true

FORCE:
