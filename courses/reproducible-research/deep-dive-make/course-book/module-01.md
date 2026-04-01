<a id="top"></a>
# Module 01 — Foundations: The Build Graph and Truth

### Quick Reference
| Concept                  | Key Takeaway                                      | Proof Command                  |
|--------------------------|---------------------------------------------------|--------------------------------|
| DAG evaluation           | Targets rebuild only when prerequisites are newer  | `make --trace all`             |
| Hidden inputs            | Must be modeled explicitly (stamps)               | Inject time-based flag → non-convergence |
| Atomic publication       | Temp → rename + `.DELETE_ON_ERROR`                | Force failure → no poison artifact |
| Depfiles                 | Automatic header tracking                         | Touch header → correct rebuild |

Module 01 establishes the core model: Make evaluates a dependency graph. Correct rebuild behavior requires explicit edges, safe publication, and convergence. This module is self-contained: you build a tiny project, deliberately break correctness, diagnose with Make’s own forensics, fix with canonical patterns, and **prove convergence**.

This module is self-contained: you build a tiny project, deliberately break correctness, diagnose with Make’s own forensics, fix with canonical patterns, and **prove convergence**.

---

<a id="toc"></a>
## 1) Table of Contents

1. [Table of Contents](#toc)
2. [Learning Outcomes](#outcomes)
3. [How to Use This Module](#usage)
4. [Core 1 — Make’s Model: DAG Evaluation (Targets, Prereqs, Recipes)](#core1)
5. [Core 2 — Rebuild Truth: mtimes, hidden inputs, and convergence](#core2)
6. [Core 3 — Rules That Scale: explicit, pattern, static pattern, multi-output reality](#core3)
7. [Core 4 — Variables & Expansion: parse-time vs run-time, determinism hazards](#core4)
8. [Core 5 — Publishing Correctly: atomic outputs, depfiles, failure hygiene](#core5)
9. [Capstone Sidebar](#capstone)
10. [Exercises](#exercises)
11. [Closing Criteria](#closing)

---

<a id="outcomes"></a>
## 2) Learning Outcomes

By the end of this module you can:

* Read any Makefile as a **DAG** and predict what will run and why.
* Explain rebuilds/skips using **only Make-native evidence**: `-n`, `--trace`, `-p`, `-q`.
* Identify “hidden inputs” and model them as **explicit prerequisites** (often via a convergent stamp).
* Write rules that remain correct under edits and failures: **one writer per output**, **no partial artifacts**, **convergent rebuild behavior**.

[Back to top](#top)

---

<a id="usage"></a>
## 3) How to Use This Module

### 3.1 Build the tiny project (local, not capstone)

Create this directory:

```
project/
  Makefile
  include/
    util.h
  src/
    main.c
    util.c
```

**include/util.h**

```c
#pragma once
int util_add(int a, int b);
```

**src/util.c**

```c
#include "util.h"
int util_add(int a, int b) { return a + b; }
```

**src/main.c**

```c
#include <stdio.h>
#include "util.h"

int main(void) {
    printf("%d\n", util_add(2, 3));
    return 0;
}
```

Then paste the Makefile from **Core 5** into `project/Makefile`.

### 3.2 The five commands you must internalize

Run these inside `project/`:

1. **Preview (no execution)**

```sh
make -n all
```

2. **Causality (why it rebuilt)**

```sh
make --trace all
```

3. **Dump evaluated reality (rules + variables)**

```sh
make -p
```

4. **Up-to-date check (convergence probe)**

```sh
make -q all; echo $?
```

Expected after a successful build: exit code `0`.

5. **Clean, build, prove convergence**

```sh
make clean && make all && make -q all
```

### 3.3 What “correct” means in Module 01

A build passes Module 01 only if all are true:

* **Declared inputs:** If it can change an output, it is in the prerequisite graph (directly or via a stamp/manifest).
* **One writer per output path:** exactly one recipe “owns” each file it publishes.
* **Atomic publish:** outputs appear only when complete.
* **Convergence:** after a successful build, `make -q all` exits `0` (no perpetual rebuild loops).

[Back to top](#top)

---

<a id="core1"></a>
## 4) Core 1 — Make’s Model: DAG Evaluation

### Definition

A Makefile defines a directed acyclic graph of file targets and prerequisites. Make decides whether each target is up-to-date by comparing **existence** and **mtimes**—not contents—unless you explicitly model more.

### Semantics

A rule has three conceptual parts:

* **Target:** usually a file path (e.g., `build/main.o`)
* **Prerequisites:** the declared inputs
* **Recipe:** the publish operation that creates/updates the target

Make evaluates the graph from the requested goal (e.g., `all`) down to leaves, then schedules runnable targets (serially in Module 01).

### Failure signatures

* “It built, but it doesn’t rebuild when I change X.” → X is not a prerequisite (the graph is lying).
* “It rebuilds every time.” → the target is `.PHONY`, or a stamp/output changes every run (non-convergent).
* “Works only after clean.” → missing edges or poison artifacts from failed builds.

### Minimal repro

**Missing edge:** remove header dependency tracking; edit `include/util.h`; observe no rebuild (wrong).

### Fix pattern

* Treat the Makefile as **graph specification**, not a script.
* Any input that can affect outputs must become an edge (direct, depfile, or stamp).

### Proof hook

```sh
make clean && make all && make --trace all
```

Second run must show no rebuild decisions for core targets (or `make -q all` must exit `0`).

[Back to top](#top)

---

<a id="core2"></a>
## 5) Core 2 — Rebuild Truth: mtimes, hidden inputs, convergence

### Definition

Make rebuilds a target when: the target is missing, or a prerequisite is newer, or the target is declared always-out-of-date (e.g., `.PHONY`). Make does **not** inherently track many real inputs (flags, recipe text, environment).

### Semantics

By default, Make is blind to:

* changes in `CFLAGS/CPPFLAGS/LDFLAGS`
* changes in recipe text
* tool version changes
* environment changes (`PATH`, locale, etc.)

If those can affect outputs, you must model them.

### Failure signatures

* “Changed flags but nothing rebuilt.” → flags are a hidden input.
* “Same command, different machine, different output.” → tool/environment is a hidden input.
* “Build never converges.” → you accidentally made a hidden input vary every run (time, random, unstable discovery).

### Minimal repro

Add this to the Makefile:

```make
CFLAGS += $(shell date)
```

Now:

```sh
make clean && make all && make -q all; echo $?
```

You should see exit `1` (stale) after a “successful” build: **non-convergence**.

### Fix pattern

Model hidden inputs using a **convergent semantic stamp**: a file whose content changes *only when the semantic input changes*, and which is a prerequisite for affected targets.

### Proof hook

```sh
make clean && make all && make -q all
```

Must exit `0`. Then change a semantic input (e.g., `make CFLAGS=-O0 all`) and observe expected rebuild via:

```sh
make CFLAGS=-O0 --trace all
```

[Back to top](#top)

---

<a id="core3"></a>
## 6) Core 3 — Rules That Scale: explicit, pattern, static pattern, multi-output reality

### Definition

Make scales through rule forms that describe families of targets without duplicating logic.

### Semantics

* **Explicit rule:** one specific target
* **Pattern rule:** maps `%` across many targets (`build/%.o: src/%.c`)
* **Static pattern rule:** applies a pattern to an explicit target list (controlled fan-out)
* **Multi-output generation:** one invocation creates multiple files; naïve multi-target rules can run multiple times unless you use correct semantics (deep treatment in Module 04).

### Failure signatures

* “Rule ran twice for the same generator.” → you wrote a multi-target rule with replicated execution semantics.
* “Only some objects rebuild.” → pattern doesn’t match what you think; or variables expand unexpectedly.

### Minimal repro

Write `a b: gen` with one recipe; change `gen`; observe Make may invoke the recipe separately for `a` and `b` depending on state. That’s a correctness hazard for generators.

### Fix pattern

* Prefer a single-output publish per target.
* When you must generate multiple outputs from one invocation, treat it as a coupled unit (Module 04 gives the correct primitives and fallbacks).

### Proof hook

Use Make’s own matching evidence:

```sh
make -p | sed -n '/^# Pattern-specific Variable Values/,/^[^#]/p'
```

and `make --trace <target>` to confirm which rule was selected and why.

[Back to top](#top)

---

<a id="core4"></a>
## 7) Core 4 — Variables & Expansion: parse-time vs run-time, determinism hazards

### Definition

Make is a language evaluated in phases. Many bugs come from confusing **parse-time expansion** (Make computes variables/rules) with **run-time execution** (the shell runs recipes).

### Semantics

Key assignment operators:

* `:=` immediate (simple) — safest default
* `=` deferred (recursive) — powerful, easy to shoot yourself with
* `?=` default if undefined
* `+=` append

Determinism hazards:

* `$(shell ...)` runs during expansion; if it observes unstable state, your graph changes between runs.
* Recursive self-reference can explode:

  ```make
  CFLAGS = $(CFLAGS) -O2   # pathological
  ```

Introspection primitives:

* `$(origin VAR)` — where it came from
* `$(flavor VAR)` — simple vs recursive
* `$(value VAR)` — raw, unexpanded value

### Failure signatures

* “Value changes between runs without file changes.” → parse-time shell or recursive expansion.
* “Make hangs or prints enormous variables.” → runaway recursion.

### Minimal repro

Set:

```make
NOW = $(shell date)
```

and print it twice during evaluation; you’ll get different values across invocations → nondeterminism.

### Fix pattern

* Prefer `:=` for computed lists.
* Fence or eliminate `$(shell ...)` from graph-defining variables.
* If it must exist, stamp its semantic result (Core 2).

### Proof hook

```sh
make -p | grep -E '^(NOW|CFLAGS|SRCS)\b'
```

Use this to verify values are stable and originate where you expect.

[Back to top](#top)

---

<a id="core5"></a>
## 8) Core 5 — Publishing Correctly: atomic outputs, depfiles, failure hygiene

### Definition

Correct builds don’t just “run commands”—they **publish artifacts safely**. A safe publish means:

* no partial output can be mistaken for a correct one
* failed recipes don’t poison later incremental builds
* header dependencies are real and automatic

### Semantics

* **Atomic publish:** write to temp → rename into place (`mv` on same filesystem is atomic)
* **Failure hygiene:** `.DELETE_ON_ERROR` plus explicit temp cleanup
* **Depfiles:** compiler emits `.d` files so header dependencies become explicit edges

### Failure signatures

* “After a failed build, future builds skip work incorrectly.” → poison artifact left behind.
* “Changing a header doesn’t rebuild.” → missing depfiles or not including them.
* “Parallel later will break.” → multiple writers, non-atomic generator output (Module 02 expands this).

### Minimal repro

Insert `false` before the final `mv` in a rule that writes `$@`. If `$@` is written directly, you can end up with a plausible partial file.

### Fix pattern

* Always publish `$@` via temp+rename.
* Emit depfiles to a temp, then atomically rename them too.
* Use `.DELETE_ON_ERROR` to avoid keeping broken outputs.

### Proof hook

* Poison prevention: force a failure and confirm the final artifact is absent/unchanged.
* Header edges: touch a header and confirm the right object rebuilds via `--trace`.

### Reference implementation (copy verbatim)

Paste this into `project/Makefile`:

```make
# Makefile — Module 01 (GNU Make ≥ 4.3; /bin/sh)
#
# Goal: smallest build that is (1) graph-correct, (2) failure-safe, (3) convergent.

MAKEFLAGS += -rR
.SUFFIXES:
.DELETE_ON_ERROR:

SHELL := /bin/sh
# Note: most /bin/sh accept -eu; if yours rejects -u, use "-e -c" and add "set -u" in recipes.
.SHELLFLAGS := -eu -c

CC       ?= cc
CPPFLAGS ?= -Iinclude
CFLAGS   ?= -O2
LDFLAGS  ?=
LDLIBS   ?=

SRC_DIR := src
BLD_DIR := build

# Deterministic discovery (rooted + sorted).
SRCS := $(sort $(wildcard $(SRC_DIR)/*.c))
OBJS := $(patsubst $(SRC_DIR)/%.c,$(BLD_DIR)/%.o,$(SRCS))
DEPS := $(OBJS:.o=.d)

DEPFLAGS := -MMD -MP

.DEFAULT_GOAL := all
.PHONY: all test clean

all: app

# ---- semantic flags stamp (convergent) ----
# Use POSIX cksum to avoid environment-dependent hash tool selection.
FLAGS_LINE := CC=$(CC) CPPFLAGS=$(CPPFLAGS) CFLAGS=$(CFLAGS) DEPFLAGS=$(DEPFLAGS) LDFLAGS=$(LDFLAGS) LDLIBS=$(LDLIBS)
FLAGS_ID   := $(shell printf '%s' "$(FLAGS_LINE)" | cksum | awk '{print $$1}' | cut -c1-12)

FLAGS_STAMP_REAL := $(BLD_DIR)/flags.$(FLAGS_ID).stamp
FLAGS_STAMP      := $(BLD_DIR)/flags.stamp

$(BLD_DIR)/:
    mkdir -p $@

$(FLAGS_STAMP_REAL): | $(BLD_DIR)/
    @printf '%s\n' "$(FLAGS_LINE)" > $@

# Stable stamp name used everywhere; content changes only when FLAGS_ID changes.
$(FLAGS_STAMP): $(FLAGS_STAMP_REAL) | $(BLD_DIR)/
    @cp -f $< $@

# ---- link (atomic publish) ----
app: $(OBJS)
    tmp=$@.tmp; \
    $(CC) $(LDFLAGS) $^ $(LDLIBS) -o $$tmp && mv -f $$tmp $@ || { rm -f $$tmp; exit 1; }

# ---- compile (atomic .o + .d publish; depfiles for headers) ----
$(BLD_DIR)/%.o: $(SRC_DIR)/%.c $(FLAGS_STAMP) | $(BLD_DIR)/
    tmp=$@.tmp; dtmp=$(@:.o=.d).tmp; \
    mkdir -p "$(@D)"; \
    $(CC) $(CPPFLAGS) $(CFLAGS) $(DEPFLAGS) -MF $$dtmp -MT $@ -c $< -o $$tmp && \
    mv -f $$tmp $@ && mv -f $$dtmp $(@:.o=.d) || { rm -f $$tmp $$dtmp; exit 1; }

-include $(DEPS)

test: app
    out=$$(./app); \
    [ "$$out" = "5" ] || { echo "test failed: expected 5, got $$out" >&2; exit 1; }

clean:
    rm -rf $(BLD_DIR) app
```

[Back to top](#top)

---

<a id="capstone"></a>
## 9) Capstone Sidebar

Capstone is corroboration, not the lesson. After you finish Module 01 locally, use capstone to confirm you recognize the same patterns at scale.

### Runbook

From repo root:

```sh
make -C make-capstone selftest
make -C make-capstone --trace all
```

### Where to look (file map)

* Flags/tool knobs stamp pattern: `make-capstone/mk/stamps.mk`
* Atomic helpers and publish discipline: `make-capstone/mk/macros.mk`
* Deterministic discovery and mapping: `make-capstone/mk/objects.mk`
* Top-level orchestration and public targets: `make-capstone/Makefile`
* Proof harness: `make-capstone/tests/run.sh`

[Back to top](#top)

---

<a id="exercises"></a>
## 10) Exercises

Each exercise is **Task → Expected → Forensics → Fix**. Do these in `project/`.

### Exercise 1 — Prove convergence is real

**Task**

```sh
make clean && make all && make -q all; echo $?
```

**Expected**: prints `0`.
**Forensics**: if not, run `make --trace all` and identify the exact prerequisite causing rebuild.
**Fix**: a stamp/output is changing every run, or you accidentally made a real file `.PHONY`.

### Exercise 2 — `.PHONY` misuse creates rebuild loops

**Task**: add `.PHONY: app`, then:

```sh
make all && make --trace app
```

**Expected**: `app` relinks every time (bug).
**Forensics**: `--trace` will show it rebuilding despite unchanged prereqs.
**Fix**: remove `.PHONY: app`. `.PHONY` is for orchestration targets only.

### Exercise 3 — Hidden input injection (non-convergence) and repair

**Task**: temporarily add:

```make
CFLAGS += $(shell date)
```

then:

```sh
make clean && make all && make -q all; echo $?
```

**Expected**: prints `1` (stale) → you created a hidden moving input.
**Forensics**: `make -p | grep '^CFLAGS'` to see the expanding value.
**Fix**: remove it; if you truly need dynamic data, stamp it (Core 2 pattern).

### Exercise 4 — Header edits must trigger rebuilds via depfiles

**Task**

```sh
make clean && make all
touch include/util.h
make --trace all
```

**Expected**: at least the relevant `.o` rebuilds, then relink.
**Forensics**: confirm `.d` exists under `build/` and is included:

```sh
ls build/*.d
make -p | grep -E '^-include|DEPS'
```

**Fix**: ensure `-MF` writes where `-include` reads; ensure `.d` is atomically published.

### Exercise 5 — Poison artifact prevention under failure

**Task**: temporarily modify link rule to fail before `mv` (e.g., `... -o $$tmp && false && mv ...`). Then:

```sh
make clean && (make all || true) && test -f app && echo "app exists" || echo "app absent"
```

**Expected**: `app absent` (or unchanged if it existed previously).
**Forensics**: `ls -la app app.tmp*` to verify no plausible final artifact.
**Fix**: keep atomic publish; ensure temp cleanup runs on failure.

[Back to top](#top)

---

<a id="closing"></a>
## 11) Closing Criteria

You have completed Module 01 when you can satisfy all proof obligations below in `project/`:

1. **Build + converge**

```sh
make clean && make all && make -q all
```

2. **Runtime assertion**

```sh
make test
```

3. **Header dependency truth**

```sh
touch include/util.h && make --trace all
```

You can point to the `--trace` line that justifies the rebuild.

4. **Hidden input detection drill**
   You can inject a time-based hidden input and demonstrate it breaks convergence, then remove/fix it and restore convergence.

If you can’t prove these, you don’t “basically understand Make”—you’re still guessing.

[Back to top](#top)
