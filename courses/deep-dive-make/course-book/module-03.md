<a id="top"></a>
# Module 03 — Production Practice: Determinism, Debugging, CI Contracts, Selftests, and Disciplined DSL

Modules 01–02 get you to “correct” and “parallel-safe.” Module 03 is where correctness becomes **reliable under change**: the DAG stays stable across machines/CI, rebuilds are explainable under pressure, the build has a CI-stable interface, and the Makefile is protected against abstraction-driven graph rot.

Capstone exists to **corroborate**. This module remains runnable and self-contained; capstone is the validation sidebar. (Capstone mappings/targets shown later mirror the existing repo surface.)

---

<a id="toc"></a>
## 1) Table of Contents

1. [Table of Contents](#toc)
2. [Learning Outcomes](#outcomes)
3. [How to Use This Module](#usage)
4. [Core 1 — Determinism Under Change](#core1)
5. [Core 2 — Forensic Debugging Ladder](#core2)
6. [Core 3 — CI Contract as a Stable API](#core3)
7. [Core 4 — Selftests for the Build System](#core4)
8. [Core 5 — Disciplined DSL: Macros + Quarantined `eval`](#core5)
9. [Capstone Sidebar](#capstone)
10. [Exercises](#exercises)
11. [Closing Criteria](#closing)

---

<a id="outcomes"></a>
## 2) Learning Outcomes

By the end of this module you can:

* Make the DAG **stable** across filesystems, locales, and CI environments (rooted + canonical discovery; fenced shelling-out; single-writer generation).
* Explain **any** rebuild/non-rebuild using Make-native forensics (`-n`, `--trace`, `-p`) rather than folklore.
* Publish artifacts **atomically** and eliminate poison artifacts after failure/interrupts.
* Define and enforce a CI-stable **public interface** (targets, exits, behavior guarantees).
* Test the **build system itself**: convergence + serial/parallel equivalence + meaningful negative tests in a sandbox.
* Use Make as a DSL **without destroying inspectability**: macros enforce invariants; `eval` is bounded, auditable, and switchable.

[Back to top](#top)

---

<a id="usage"></a>
## 3) How to Use This Module

### 3.1 Build a local “production simulator” (this module’s own playground)

You extend your Module 02 project with three stressors:

1. **Dynamic sources**: files appear/disappear under `src/dynamic/`
2. **Codegen**: a generated header used by multiple compilation units
3. **A selftest harness**: proves build invariants, not “it compiled”

Suggested tree (minimal, but sufficient):

```
project/
  Makefile
  mk/
    common.mk      # toolchain + flags policy
    objects.mk     # rooted/sorted discovery
    stamps.mk      # modeled hidden inputs (flags/tool/env signatures)
    macros.mk      # atomic publish helpers
    rules_eval.mk  # optional: quarantined eval demo
  src/
    main.c util.c
    dynamic/
      dyn1.c dyn2.c
  include/
    util.h
  scripts/
    gen_dynamic_h.py
  tests/
    run.sh         # convergence + equivalence + negative test
```

### 3.1.1 Paste the simulator scaffolding (complete; runnable)

If you want this module to be **self-contained**, do not invent missing files. Paste the following exactly.

Run it like this:

```sh
# Linux:
make -C project selftest
# macOS (GNU Make):
gmake -C project selftest
```

#### `project/Makefile`

```make
# project/Makefile — Module 03 simulator (GNU Make ≥ 4.3)
#
# Contract: deterministic discovery + modeled hidden inputs + atomic publish + selftests.

MAKEFLAGS += -rR
.SUFFIXES:
.DELETE_ON_ERROR:

SHELL := /bin/sh
.SHELLFLAGS := -eu -c

.DEFAULT_GOAL := help
.PHONY: help all test selftest clean eval-demo

include mk/common.mk
include mk/macros.mk
include mk/objects.mk
include mk/stamps.mk
-include mk/rules_eval.mk

help:
    @printf '%s\n' \
      'Targets:' \
      '  help      - this help' \
      '  all       - build the program' \
      '  test      - runtime assertion' \
      '  selftest  - convergence + serial/parallel equivalence + negative hidden-input check' \
      '  eval-demo - (optional) bounded eval demo when USE_EVAL=yes' \
      '  clean     - remove build artifacts'

all: $(APP)

# ---- directories ----
$(BLD_DIR)/:
    mkdir -p $@
$(BLD_INC_DIR)/: | $(BLD_DIR)/
    mkdir -p $@

# ---- codegen: build/include/dynamic.h ----
# The header is a coupled unit: its content depends on the *set* of dynamic sources.
$(GEN_HDR): scripts/gen_dynamic_h.py $(DYN_SRCS) | $(BLD_INC_DIR)/
    @tmp=$@.tmp; \
    python3 scripts/gen_dynamic_h.py $$tmp $(DYN_SRCS) && \
    mv -f $$tmp $@ || { rm -f $$tmp; exit 1; }

# main.o includes dynamic.h (explicit edge; depfiles are included for headers too).
$(BLD_DIR)/main.o: $(GEN_HDR)

# ---- compile (atomic .o + .d publish) ----
$(BLD_DIR)/%.o: %.c $(FLAGS_STAMP) | $(BLD_DIR)/
    @tmp=$@.tmp; dtmp=$(@:.o=.d).tmp; \
    mkdir -p "$(@D)"; \
    $(CC) $(CPPFLAGS) $(CFLAGS) $(DEPFLAGS) -MF $$dtmp -MT $@ -c $< -o $$tmp && \
    mv -f $$tmp $@ && mv -f $$dtmp $(@:.o=.d) || { rm -f $$tmp $$dtmp; exit 1; }

-include $(DEPS)

# ---- link (atomic publish) ----
$(APP): $(OBJS)
    @tmp=$@.tmp; \
    $(CC) $(LDFLAGS) $^ $(LDLIBS) -o $$tmp && mv -f $$tmp $@ || { rm -f $$tmp; exit 1; }

test: $(APP)
    @out=$$(./$(APP)); \
    [ "$$out" = "$(EXPECTED_OUTPUT)" ] || { echo "test failed: expected $(EXPECTED_OUTPUT), got $$out" >&2; exit 1; }

selftest:
    @MAKE="$(MAKE)" sh tests/run.sh

eval-demo:
    @if [ "$(USE_EVAL)" = "yes" ]; then $(MAKE) --no-print-directory eval_demo_run; else echo 'eval-demo disabled (set USE_EVAL=yes)'; fi

clean:
    @rm -rf $(BLD_DIR) $(APP)
```

#### `project/mk/common.mk`

```make
# project/mk/common.mk — stable knobs

CC       ?= cc
CPPFLAGS ?= -Iinclude -Ibuild/include
CFLAGS   ?= -O2
LDFLAGS  ?=
LDLIBS   ?=

SRC_DIR := src
DYN_DIR := src/dynamic
BLD_DIR := build
BLD_INC_DIR := build/include

APP := app

DEPFLAGS := -MMD -MP

# Runtime baseline (with dyn1.c + dyn2.c as shipped):
# util_add(2,3)=5; dyn_sum()=10+20=30; 5*30=150
EXPECTED_OUTPUT := 150

# Optional switches
USE_EVAL ?= no
HIDDEN_INPUT ?= 0
```

#### `project/mk/macros.mk`

```make
# project/mk/macros.mk — tiny helpers (keep it auditable)

define assert_nonempty
    @if [ -z "$(strip $(1))" ]; then echo "error: $(2)" >&2; exit 1; fi
endef
```

#### `project/mk/objects.mk`

```make
# project/mk/objects.mk — rooted + sorted discovery

BASE_SRCS := $(sort $(wildcard $(SRC_DIR)/*.c))
DYN_SRCS  := $(sort $(wildcard $(DYN_DIR)/*.c))

# Full source list is deterministic.
SRCS := $(BASE_SRCS) $(DYN_SRCS)

OBJS := $(patsubst %.c,$(BLD_DIR)/%.o,$(SRCS))
DEPS := $(OBJS:.o=.d)

GEN_HDR := $(BLD_INC_DIR)/dynamic.h
```

#### `project/mk/stamps.mk`

```make
# project/mk/stamps.mk — modeled hidden inputs (convergent)

# Intentional negative-test switch:
# When HIDDEN_INPUT=1 we inject parse-time entropy into CFLAGS.
# Selftest must detect this via non-convergence.
ifeq ($(HIDDEN_INPUT),1)
CFLAGS += -DHIDDEN_SEED=$(shell date +%s)
endif

FLAGS_LINE := CC=$(CC) CPPFLAGS=$(CPPFLAGS) CFLAGS=$(CFLAGS) DEPFLAGS=$(DEPFLAGS) LDFLAGS=$(LDFLAGS) LDLIBS=$(LDLIBS)
FLAGS_ID   := $(shell printf '%s' "$(FLAGS_LINE)" | cksum | awk '{print $$1}' | cut -c1-12)

FLAGS_STAMP_REAL := $(BLD_DIR)/flags.$(FLAGS_ID).stamp
FLAGS_STAMP      := $(BLD_DIR)/flags.stamp

$(FLAGS_STAMP_REAL): | $(BLD_DIR)/
    @printf '%s\n' "$(FLAGS_LINE)" > $@

$(FLAGS_STAMP): $(FLAGS_STAMP_REAL) | $(BLD_DIR)/
    @cp -f $< $@
```

#### `project/mk/rules_eval.mk` (optional)

```make
# project/mk/rules_eval.mk — quarantined, bounded eval demo
# Enabled only when USE_EVAL=yes.

ifeq ($(USE_EVAL),yes)
EVAL_WORDS := alpha beta gamma

define _mk_eval_rule
eval_demo_$(1): | $(BLD_DIR)/
    @printf '%s\n' '$(1)' > $(BLD_DIR)/eval.$(1).txt
endef

$(foreach w,$(EVAL_WORDS),$(eval $(call _mk_eval_rule,$(w))))

eval_demo_run: $(addprefix eval_demo_,$(EVAL_WORDS))
    @cat $(BLD_DIR)/eval.*.txt > $(BLD_DIR)/eval.txt
    @echo "wrote $(BLD_DIR)/eval.txt"
endif
```

#### `project/include/util.h`

```c
#pragma once
int util_add(int a, int b);
```

#### `project/src/util.c`

```c
#include "util.h"
int util_add(int a, int b) { return a + b; }
```

#### `project/src/dynamic/dyn1.c`

```c
int dyn1(void) { return 10; }
```

#### `project/src/dynamic/dyn2.c`

```c
int dyn2(void) { return 20; }
```

#### `project/src/main.c`

```c
#include <stdio.h>
#include "util.h"
#include "dynamic.h"  /* generated into build/include */

int main(void) {
    printf("%d\n", util_add(2, 3) * dyn_sum());
    return 0;
}
```

#### `project/scripts/gen_dynamic_h.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(2)

def main(argv: list[str]) -> int:
    if len(argv) < 3:
        die("usage: gen_dynamic_h.py <out> <dyn_src> [<dyn_src> ...]")
    out = Path(argv[1])
    dyn_srcs = [Path(p) for p in argv[2:]]

    # Deterministic: base names sorted by caller; still defensively sort.
    fn_names: list[str] = []
    for p in sorted(dyn_srcs, key=lambda x: x.as_posix()):
        if p.suffix != ".c":
            continue
        fn_names.append(p.stem)

    lines: list[str] = []
    lines.append("#pragma once")
    lines.append("/* generated: do not edit */")
    lines.append(f"#define DYN_COUNT {len(fn_names)}")
    for fn in fn_names:
        lines.append(f"int {fn}(void);")
    # Inline sum keeps main.c constant even when dyn set changes.
    lines.append("static inline int dyn_sum(void) {")
    if fn_names:
        terms = " + ".join(f"{fn}()" for fn in fn_names)
        lines.append(f"    return {terms};")
    else:
        lines.append("    return 0;")
    lines.append("}")
    lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

#### `project/tests/run.sh`

```sh
#!/bin/sh
set -eu

MAKE="${MAKE:-make}"

fail() { echo "selftest: FAIL: $*" >&2; exit 1; }
pass() { echo "selftest: PASS: $*"; }

tmp="${TMPDIR:-/tmp}/m03-selftest.$$"
trap 'rm -rf "$tmp"' EXIT INT TERM
mkdir -p "$tmp"

tar -C . -cf - Makefile mk include src scripts tests 2>/dev/null | tar -C "$tmp" -xf -
cd "$tmp"

echo "Running convergence check..."
$MAKE clean >/dev/null 2>&1 || true
$MAKE -j1 all >/dev/null
$MAKE -q all && pass "convergence" || fail "convergence (make -q all != 0)"

hash_tree() {
  ( \
    printf '%s\n' "./$(APP)"; \
    find "$(BLD_INC_DIR)" -type f -print 2>/dev/null; \
    find "$(BLD_DIR)/src" -type f -name '*.o' -print 2>/dev/null; \
    find "$(BLD_DIR)/src" -type f -name '*.d' -print 2>/dev/null; \
  ) | sort | while IFS= read -r f; do
    [ -f "$f" ] || continue
    cksum "$f"
  done | sort | cksum | awk '{print $1}'
}

echo "Running serial/parallel equivalence check..."
$MAKE clean >/dev/null 2>&1 || true
$MAKE -j1 all >/dev/null
h1="$(hash_tree)"

$MAKE clean >/dev/null 2>&1 || true
$MAKE -j8 all >/dev/null
h2="$(hash_tree)"

[ "$h1" = "$h2" ] && pass "serial-parallel equivalence" || fail "serial-parallel equivalence"

echo "Running runtime test..."
$MAKE -j8 test >/dev/null && pass "runtime test" || fail "runtime test"

echo "Running negative test (hidden input -> non-convergence)..."
$MAKE clean >/dev/null 2>&1 || true
HIDDEN_INPUT=1 $MAKE -j1 all >/dev/null
if HIDDEN_INPUT=1 $MAKE -q all; then
  fail "negative: expected non-convergence, but make -q all returned 0"
else
  pass "negative: hidden input detected (non-convergence)"
fi

pass "selftest complete"
```

This module’s text teaches patterns using `project/`. Capstone later is used to cross-check behavior.

---

### 3.2 The five commands you must internalize (local project)

From `project/`:

```sh
make help
make all
make test
make selftest
make --trace all
```

What each is **for**:

* `help`: the stable interface (targets + knobs). If it’s not in `help`, it’s not public API.
* `all`: builds the declared correctness artifacts.
* `test`: runtime assertions (not “compiled successfully”).
* `selftest`: build-system invariants (convergence + equivalence + negative).
* `--trace all`: causality line-by-line (the only acceptable explanation for rebuilds).

---

### 3.3 The only debugging ladder you’re allowed to use

1. Preview:

```sh
make -n <target>
```

2. Force causality:

```sh
make --trace <target>
```

3. Dump evaluated reality:

```sh
make -p
```

4. Only then add temporary probes (remove afterward):

* `$(warning ...)`, `$(info ...)`, `$(error ...)`

If you say “rebuilt for no reason” without quoting the triggering `--trace` line, you did not debug.

---

### 3.4 What “correct” means in Module 03

A build passes Module 03 only if all are true:

* **Deterministic graph**: rooted discovery, canonical ordering, locale-fenced shell discovery.
* **Convergence**: after a successful build, `make -q all` exits `0`.
* **Serial/parallel equivalence**: `-j1` and `-jN` produce hash-equivalent declared artifacts.
* **Meaningful negative test**: inject a hidden input → the system stops converging and/or fails equivalence.
* **Inspectable**: rebuilds are justified with `--trace`, not guesswork.

[Back to top](#top)

---

<a id="core1"></a>
## 4) Core 1 — Determinism Under Change

### Definition

Determinism is:

**same semantic inputs → same DAG → same rebuild decisions → same artifacts**, independent of filesystem order, locale collation, or parallel schedule.

Module 03 adds one hard constraint: **the DAG must stay stable while the repo changes** (files appear, codegen changes shape, CI differs from dev machines).

---

### Semantics

Determinism breaks in four recurring ways:

1. **Discovery is unstable**

   * `wildcard` results are unsorted
   * `find` output order differs across systems
   * editor backups / temp files leak into lists
   * discovery is unrooted (“scan the world”)

2. **Dynamic behavior leaks into parse-time**

   * `$(shell date)`
   * `$(shell git rev-parse …)` used in prereqs or flags without stamping
   * environment-dependent output (locale/timezone) used as inputs

3. **Generation is not single-writer + atomic**

   * generated header written directly to final path
   * multiple rules can write the same output
   * partially-written generated file consumed by compilers

4. **Hidden inputs aren’t modeled**

   * flags/toolchain/env changes affect outputs, but aren’t prerequisites

---

### Failure signatures

* “Nothing changed, but it rebuilt.” → unstable discovery or drifting stamp content
* “CI differs from my machine.” → locale/tool drift, un-fenced shell, un-modeled hidden input
* “`-j` flakes but `-j1` works.” → missing edge or non-atomic generation (graph is lying)
* “Works after clean.” → poison artifacts or missing prerequisites

---

### Minimal repro

**Repro A: unstable discovery order**

```make
SRCS = $(wildcard src/dynamic/*.c)   # unsorted
OBJS = $(patsubst src/%.c,build/%.o,$(SRCS))
```

Symptoms:

* different link order across machines
* non-reproducible binary (even if compilation is “correct”)
* equivalence tests fail intermittently

**Repro B: hidden input via parse-time shell**

```make
CFLAGS += -DSEED=$(shell date +%s)
```

Symptoms:

* permanent non-convergence (`make -q all` never returns 0)

---

### Fix pattern

**Fix A: canonical discovery (rooted + sorted + fenced)**

* Root discovery under explicit directories only
* Canonicalize ordering

```make
SRCS := $(sort $(wildcard src/dynamic/*.c))
```

If you must use the shell:

```make
SRCS := $(shell LC_ALL=C find src/dynamic -name '*.c' -print | sort)
```

**Fix B: model hidden inputs with a semantic stamp**

* Any variability that can change outputs becomes a prerequisite via a stamp/manifest.
* Stamps must be **convergent**: they change only when the modeled semantics change.

Pattern:

* Create a content-addressed “flags signature” stamp
* Depend on a stable path `build/flags.stamp` whose contents only change when signature changes

---

### Proof hook

After implementing fixes, you must be able to prove:

```sh
make clean && make all
make -q all        # must exit 0
make clean && make -j4 all
make selftest       # must pass equivalence + convergence
```

[Back to top](#top)

---

<a id="core2"></a>
## 5) Core 2 — Forensic Debugging Ladder

### Definition

Debugging in Make is not guesswork. A rebuild always has a cause **in the evaluated graph**; your job is to force Make to confess that cause.

---

### Semantics

* `-n` answers: *what would run?*
* `--trace` answers: *why did it run?* (the most valuable signal)
* `-p` answers: *what graph did Make actually evaluate?*
* probes (`warning/error/info`) are for surgical inspection only after the above

---

### Failure signatures

Common culprits you must learn to recognize (and map to fixes):

* **Perpetual stamp** → stamp recipe writes different content each run → non-convergence
* **Missing generator edge** → generated header exists but is not a prerequisite/depfile input
* **Discovery instability** → list order/membership differs across runs
* **Non-atomic publish** → plausible partial outputs poison incremental correctness
* **Accidental hidden input** → time/env/PATH/locale-dependent behavior

---

### Minimal repro

**Perpetual stamp that guarantees non-convergence:**

```make
build/flags.stamp:
    @date > $@
```

Even if nothing changed, `build/flags.stamp` is always newer → everything that depends on it rebuilds forever.

---

### Fix pattern

Replace perpetual stamps with **semantic stamps**:

* encode the modeled state (flags/tool/env signature)
* write stable content
* do not rewrite when unchanged

Implementation guidance:

* build the signature from *explicit* variables (`CC`, `CFLAGS`, `CPPFLAGS`, tool paths if relevant)
* hash it, and only update the stable stamp when the hash changes
* keep stamps out of `all` unless they are genuine prerequisites

---

### Proof hook

You must be able to answer “why did it rebuild?” with one quoted trace line:

```sh
make --trace all
```

If you can’t point to the trace line that triggered a rebuild, you haven’t located the cause.

[Back to top](#top)

---

<a id="core3"></a>
## 6) Core 3 — CI Contract as a Stable API

### Definition

CI does not “run your Makefile.” CI consumes an **interface**. Your internals can change; the public contract must stay strict and predictable.

---

### Semantics

A CI contract includes:

1. **Public targets (stable surface)**
2. **Behavior guarantees** (what they build, what they check, what they write)
3. **Failure semantics** (exit codes, non-interactive behavior, no silent greens)
4. **Output policy** (what is part of correctness artifacts vs diagnostics)

Required public surface (your local project should implement these; capstone mirrors a similar set):

* `help`, `all`, `test`, `selftest`, plus audits/attestation as needed

Stability rule (non-negotiable):

* If a target is public, you do not silently change its meaning. Breaking changes require rename/deprecation.

---

### Failure signatures

* CI “green” while artifacts are wrong → target doesn’t enforce invariants, or checks are non-fatal
* CI flakes → nondeterminism, hidden inputs, or race-dependent behavior
* `attest` causes rebuild storms → you incorrectly wired diagnostics into correctness outputs

---

### Minimal repro

**Poisoning correctness by wiring attestation into `all`:**

```make
all: app attest
attest:
    @date > build/attest.txt
```

Now “nothing changed” is false forever because `attest` changes every run.

---

### Fix pattern

* Make `attest` a *diagnostic sink*, not a prerequisite of correctness artifacts.
* Keep it out of the equivalence set (it legitimately varies).

Better:

```make
all: app

.PHONY: attest
attest: app
    @mkdir -p build
    @printf 'CC=%s\nCFLAGS=%s\n' "$(CC)" "$(CFLAGS)" > build/attest.txt
```

(Still diagnostic; still not part of correctness DAG.)

---

### Proof hook

In CI you must be able to run:

```sh
make all
make test
make selftest
```

and treat any non-zero exit as a regression, not “a Make quirk.”

[Back to top](#top)

---

<a id="core4"></a>
## 7) Core 4 — Selftests for the Build System

### Definition

Module 03’s defining move: you stop trusting “it builds” and start testing **the build system itself**.

---

### Semantics

Your selftest must enforce four properties:

1. **Convergence**
   After building `all`, the repo must be up-to-date (`make -q all` exits `0`).

2. **Serial/parallel equivalence**
   Build under `-j1`, hash a declared artifact set. Clean, build under `-jN`, hash the same set. Hashes must match.

3. **Meaningful negative test**
   Inject a hidden input. The build must stop converging and/or fail equivalence.

4. **Sandboxing**
   Selftests run in an isolated temp copy so local state cannot “help.”

Choosing the equivalence set (two tiers):

* **Tier A (recommended default):** hash semantic artifacts (binaries, generated headers, published outputs).
* **Tier B (strict / toolchain-sensitive):** additionally hash intermediates you expect to be stable within a fixed toolchain (e.g., `.o`, `.d`, flags stamps).

Never hash noise (logs, timestamps, caches, attestations).

---

### Failure signatures

* selftest “passes” but regressions ship → equivalence set is wrong (hashing too little)
* selftest always fails → hashing entropy, or stamps are non-convergent
* negative test fails “for the wrong reason” → your injection polluted unrelated outputs or broke the harness

---

### Minimal repro

**Bad equivalence set**: hashing `build/attest.txt` (contains timestamps) guarantees failure even if build is correct.

**Bad negative test**: breaking compilation instead of injecting hidden input proves nothing about determinism.

---

### Fix pattern

* Equivalence set must be explicit and justified.
* Negative test must create *hidden variability* without changing declared prerequisites. Examples:

   * add an unmodeled env-dependent flag
   * introduce unstable discovery membership/order (e.g., temp file pickup)
   * inject time-based content into a stamp (then prove it breaks convergence)

---

### Proof hook

Your `tests/run.sh` must be able to:

```sh
make clean && make -j1 all
# hash equivalence set -> H1
make clean && make -j4 all
# hash equivalence set -> H2
test "$H1" = "$H2"
make -q all   # must be 0 after success
```

[Back to top](#top)

---

<a id="core5"></a>
## 8) Core 5 — Disciplined DSL: Macros + Quarantined `eval`

### Definition

Make *is* a language. In Module 03, DSL is allowed only if it **increases correctness without reducing auditability**.

---

### Semantics

Two layers:

1. **Macros (`define` + `call`)**

   * used to enforce invariants consistently (atomic publish, tool checks, assertions)
   * must be small and side-effect minimal
   * must preserve traceability (a reader can still explain the DAG)

2. **Rule generation (`eval`)**
   Allowed only when all are true:

   * bounded (finite, predictable rule set)
   * auditable (`-n`, `--trace`, `-p` show what exists)
   * switchable (can disable it and still pass core build/selftest)

---

### Failure signatures

* “Makefile became a compiler for itself” → uncontrolled eval surface
* `--trace` becomes meaningless → metaprogramming hid the actual graph
* rules differ across machines → eval depends on unstable discovery

---

### Minimal repro

**Unbounded eval generation (pathological):**

```make
$(foreach f,$(shell find src -type f),$(eval ...))
```

This combines the two worst ideas:

* parse-time shell discovery
* rule generation from unstable ordering/membership

---

### Fix pattern

Quarantine + budget + proofs:

* All `eval` lives in **one** include (`mk/rules_eval.mk`)
* It is guarded by an explicit switch (`USE_EVAL=yes`)
* The generated surface area is measurable (count rules, count targets)
* The “normal” build does not depend on eval-demo behavior

---

### Proof hook

You must be able to:

```sh
make -n eval-demo
make --trace eval-demo
make USE_EVAL=yes -n eval-demo
make USE_EVAL=yes --trace eval-demo
make USE_EVAL=yes selftest
make USE_EVAL=no  selftest
```

If disabling eval breaks your core build, you failed the quarantine.

[Back to top](#top)

---

<a id="capstone"></a>
## 9) Capstone Sidebar

Capstone is the runnable cross-check for the invariants and workflows above. Current capstone alignment (file locations + public surface) is documented in the repo module text.

### 9.1 What to run (from repo root)

```sh
make -C make-capstone help
make -C make-capstone selftest
make -C make-capstone discovery-audit
make -C make-capstone attest
make -C make-capstone portability-audit
make -C make-capstone USE_EVAL=yes eval-demo
```

(These entrypoints mirror the intended CI contract and DSL quarantine behavior.)

### 9.2 Where each core lives (capstone map)

* Deterministic discovery: `make-capstone/mk/objects.mk`
* Hidden-input modeling / stamps: `make-capstone/mk/stamps.mk`
* Atomic helpers / invariants: `make-capstone/mk/macros.mk`
* Selftest harness: `make-capstone/tests/run.sh`
* Rule-generation demo: `make-capstone/mk/rules_eval.mk`
* Capability gates / contracts: `make-capstone/mk/contract.mk`
* Public API surface: `make-capstone/Makefile`

[Back to top](#top)

---

<a id="exercises"></a>
## 10) Exercises

Format: **Task → Expected → Forensics → Fix**. Run against your local `project/` first, then validate on capstone.

### Exercise 1 — Discovery determinism (order + membership)

**Task**: Make discovery intentionally unstable (unsorted wildcard or un-fenced `find`), then run:

```sh
make clean && make all
make clean && make -j4 all
make selftest
```

**Expected**: equivalence fails at least once.
**Forensics**: `make --trace all` + inspect the evaluated `SRCS/OBJS` in `make -p`.
**Fix**: rooted + sorted discovery; fence locale for shell discovery.

---

### Exercise 2 — Perpetual stamp (non-convergence on purpose)

**Task**: add the broken stamp:

```make
build/flags.stamp:
    @date > $@
```

Then run:

```sh
make all
make -q all
```

**Expected**: `make -q all` is never up-to-date.
**Forensics**: `make --trace all` shows `build/flags.stamp` being rewritten.
**Fix**: convert to semantic stamp (content-addressed; only updates when modeled state changes).

---

### Exercise 3 — Generator edge + atomic publish

**Task**: add a generated header used by multiple `.c` files, but omit the dependency (first). Run `make -j4 all` repeatedly.

**Expected**: intermittent compile failure or inconsistent rebuild behavior.
**Forensics**: `make --trace` shows compilation occurring before header generation (or consuming partial header).
**Fix**: single-writer rule for generated header + temp→rename publish + explicit prereq (or depfile inclusion).

---

### Exercise 4 — CI contract: stop lying with “green”

**Task**: make `test` always succeed (return 0 regardless), then introduce a runtime failure.

**Expected**: CI would go green incorrectly (this is the failure).
**Forensics**: show that the test target ignores program output/exit.
**Fix**: enforce runtime assertions; treat violations as non-zero exit.

---

### Exercise 5 — Quarantined eval (bounded + switchable)

**Task**: create `mk/rules_eval.mk` that generates a small, fixed rule set. Guard it behind `USE_EVAL=yes`.

Run:

```sh
make selftest
make USE_EVAL=yes eval-demo
make USE_EVAL=yes selftest
```

**Expected**: core build works with eval on or off; eval-demo remains auditable via `-n`/`--trace`.
**Forensics**: `make -p | grep -E '^[^#].*:'` (spot-check generated rules), plus `--trace eval-demo`.
**Fix**: reduce rule generation until it is finite, legible, and independent of unstable discovery.

[Back to top](#top)

---

<a id="closing"></a>
## 11) Closing Criteria

You pass Module 03 only if you can demonstrate all of the following in your **local** `project/` (then corroborate via capstone):

1. **Deterministic DAG**

   * discovery is rooted + canonical
   * generators are single-writer + atomic
   * hidden inputs are modeled via semantic stamps

2. **Forensic explainability**

   * every rebuild can be justified by quoting the triggering `--trace` line

3. **CI-stable contract**

   * `help`, `all`, `test`, `selftest` are stable, strict, non-interactive, and fail loudly

4. **Build-system selftests**

   * convergence holds (`make -q all` after success)
   * serial/parallel equivalence holds
   * a meaningful negative test exists and fails for the right reason

5. **DSL discipline**

   * macros enforce invariants without hiding the DAG
   * any `eval` use is quarantined, bounded, auditable, and switchable

Next: Module 04 becomes your lookup layer under pressure; Module 05 hardens portability, hermeticity, and performance engineering.

[Back to top](#top)

---