<a id="top"></a>
# Module 02 — Scaling: Parallelism, Safety, and Large-Project Structure

Module 01 taught correctness on a small graph. Module 02 is where that correctness either survives contact with reality—or collapses the first time someone runs `make -j` on a slightly larger repo.

This module does **not** treat parallelism as a performance trick. It treats it as an adversarial test of whether your DAG is telling the truth.

Capstone is **only** corroboration. This module remains complete and runnable even if `make-capstone/` didn’t exist.

---

<a id="toc"></a>
## 1) Table of Contents

1. [Table of Contents](#toc)
2. [Learning Outcomes](#outcomes)
3. [How to Use This Module](#usage)
4. [Core 1 — What Make Parallelizes](#core1)
5. [Core 2 — Parallel-Safety Contract](#core2)
6. [Core 3 — Ordering Tools That Don’t Lie](#core3)
7. [Core 4 — Large-Project Structure Without Recursive Make Rot](#core4)
8. [Core 5 — Selftests + Race Repro Pack](#core5)
9. [Capstone Sidebar](#capstone)
10. [Exercises](#exercises)
11. [Closing Criteria](#closing)

---

<a id="outcomes"></a>
## 2) Learning Outcomes

By the end of this module, you can:

* Predict **exactly** what Make may run concurrently and why.
* Enforce a non-negotiable parallel-safety contract: **one writer per output, atomic publish, no shared appends, directory-safe recipes, failure hygiene**.
* Choose ordering tools correctly: real prerequisites vs order-only vs stamps/manifests vs last-resort serialization.
* Scale a repo into layers (`mk/*.mk`, optional overrides) while preserving a **single top-level DAG**.
* Prove correctness under concurrency using a selftest harness and a repro pack you can run until you can **predict** the failure.

[Back to top](#top)

---

<a id="usage"></a>
## 3) How to Use This Module

### 3.1 Build the local “Module 02 simulator” project

Create this project (separate from capstone):

```
m02/
  Makefile
  mk/
    common.mk
    objects.mk
    rules.mk
  include/
    util.h
    sub.h
  src/
    main.c
    util.c
    sub/sub.c
  repro/
    01-shared-log.mk
    02-temp-collision.mk
    03-stamp-clobber.mk
    04-generated-header.mk
    05-mkdir-race.mk
```

**Note:** the simulator uses `mk/rules.mk` as a teaching simplification. In the capstone repo, the same surface is split across the top-level `Makefile` and `mk/*.mk` (notably `mk/objects.mk` + `mk/stamps.mk`), so you won’t find a literal `mk/rules.mk` there. Capstone also ships `repro/01-shared-append.mk` as a backward-compatible alias for older text; in this module we treat `repro/01-shared-log.mk` as canonical.

Use the source files below (same semantics every machine; output must be `50`):

`include/util.h`

```c
#pragma once
int util_add(int a, int b);
```

`src/util.c`

```c
#include "util.h"
int util_add(int a, int b) { return a + b; }
```

`include/sub.h`

```c
#pragma once
int sub_mult(int a, int b);
```

`src/sub/sub.c`

```c
#include "sub.h"
int sub_mult(int a, int b) { return a * b; }
```

`src/main.c`

```c
#include <stdio.h>
#include "util.h"
#include "sub.h"

int main(void) {
    printf("%d\n", util_add(2, 3) * sub_mult(2, 5)); /* 5 * 10 = 50 */
    return 0;
}
```

### 3.1.1 Paste the simulator build system (complete; no invention required)

The goal is that **you can run this immediately**:

```sh
# Linux:
make -C m02 selftest
# macOS (GNU Make):
gmake -C m02 selftest
```

Create these files exactly.

#### `m02/Makefile`

```make
# m02/Makefile — Module 02 simulator (GNU Make ≥ 4.3)
#
# Contract: convergent, parallel-safe, deterministic discovery, and a selftest
# that proves serial/parallel equivalence.

MAKEFLAGS += -rR
.SUFFIXES:
.DELETE_ON_ERROR:

SHELL := /bin/sh
.SHELLFLAGS := -eu -c

.DEFAULT_GOAL := help
.PHONY: help all test selftest clean repro

# Public interface
help:
    @printf '%s\n' \
      'Targets:' \
      '  help      - this help' \
      '  all       - build the program' \
      '  test      - run runtime assertion' \
      '  selftest  - prove convergence + serial/parallel equivalence' \
      '  clean     - remove build artifacts' \
      '  repro     - list the repro pack (run with: make -f repro/<file>.mk -j8 all)'

# Layering
include mk/common.mk
include mk/objects.mk
include mk/rules.mk

all: $(APP)

test: $(APP)
    @out=$$(./$(APP)); \
      [ "$$out" = "50" ] || { echo "test failed: expected 50, got $$out" >&2; exit 1; }

# Selftest is a build-system test, not a program test.
selftest:
    @MAKE="$(MAKE)" sh tests/run.sh

clean:
    @rm -rf $(BLD_DIR) $(APP)

repro:
    @printf '%s\n' \
      'Repro pack:' \
      '  repro/01-shared-log.mk' \
      '  repro/02-temp-collision.mk' \
      '  repro/03-stamp-clobber.mk' \
      '  repro/04-generated-header.mk' \
      '  repro/05-mkdir-race.mk'
```

#### `m02/mk/common.mk`

```make
# m02/mk/common.mk — small, stable policy knobs

CC       ?= cc
CPPFLAGS ?= -Iinclude
CFLAGS   ?= -O2
LDFLAGS  ?=
LDLIBS   ?=

SRC_DIR := src
BLD_DIR := build

APP := app
DEPFLAGS := -MMD -MP
```

#### `m02/mk/objects.mk`

```make
# m02/mk/objects.mk — deterministic discovery and mapping

SRCS := $(sort \
  $(wildcard $(SRC_DIR)/*.c) \
  $(wildcard $(SRC_DIR)/sub/*.c) \
)

OBJS := $(patsubst $(SRC_DIR)/%.c,$(BLD_DIR)/%.o,$(SRCS))
DEPS := $(OBJS:.o=.d)
```

#### `m02/mk/rules.mk`

```make
# m02/mk/rules.mk — rules + correctness scaffolding

# Directory scaffold
$(BLD_DIR)/:
    mkdir -p $@

# ---- Semantic flags stamp (convergent) ----
# If flags change, we must rebuild; Make itself won't notice, so we model it.
FLAGS_LINE := CC=$(CC) CPPFLAGS=$(CPPFLAGS) CFLAGS=$(CFLAGS) DEPFLAGS=$(DEPFLAGS) LDFLAGS=$(LDFLAGS) LDLIBS=$(LDLIBS)
FLAGS_ID   := $(shell printf '%s' "$(FLAGS_LINE)" | cksum | awk '{print $$1}' | cut -c1-12)

FLAGS_STAMP_REAL := $(BLD_DIR)/flags.$(FLAGS_ID).stamp
FLAGS_STAMP      := $(BLD_DIR)/flags.stamp

$(FLAGS_STAMP_REAL): | $(BLD_DIR)/
    @printf '%s\n' "$(FLAGS_LINE)" > $@

# Stable name used everywhere; content changes only if FLAGS_ID changes.
$(FLAGS_STAMP): $(FLAGS_STAMP_REAL) | $(BLD_DIR)/
    @cp -f $< $@

# ---- Link (atomic publish) ----
$(APP): $(OBJS)
    @tmp=$@.tmp; \
      $(CC) $(LDFLAGS) $^ $(LDLIBS) -o $$tmp && mv -f $$tmp $@ || { rm -f $$tmp; exit 1; }

# ---- Compile (atomic .o + .d publish; depfiles for headers) ----
$(BLD_DIR)/%.o: $(SRC_DIR)/%.c $(FLAGS_STAMP) | $(BLD_DIR)/
    @tmp=$@.tmp; dtmp=$(@:.o=.d).tmp; \
      mkdir -p "$(@D)"; \
      $(CC) $(CPPFLAGS) $(CFLAGS) $(DEPFLAGS) -MF $$dtmp -MT $@ -c $< -o $$tmp && \
      mv -f $$tmp $@ && mv -f $$dtmp $(@:.o=.d) || { rm -f $$tmp $$dtmp; exit 1; }

-include $(DEPS)
```

#### `m02/tests/run.sh`

```sh
#!/bin/sh
set -eu

MAKE="${MAKE:-make}"

fail() { echo "selftest: FAIL: $*" >&2; exit 1; }
pass() { echo "selftest: PASS: $*"; }

# Always run in a clean, local sandbox copy to avoid "local state helps".
tmp="${TMPDIR:-/tmp}/m02-selftest.$$"
trap 'rm -rf "$tmp"' EXIT INT TERM
mkdir -p "$tmp"

# Copy only what we need.
# (No build/ or app.)
tar -C . -cf - Makefile mk include src repro tests 2>/dev/null | tar -C "$tmp" -xf -

cd "$tmp"

echo "Running convergence check..."
$MAKE clean >/dev/null 2>&1 || true
$MAKE -j1 all >/dev/null
$MAKE -q all && pass "convergence" || fail "convergence (make -q all != 0)"

hash_tree() {
  # Hash semantic artifacts (app + the build directory). Order must be stable.
  ( \
    printf '%s\n' "./$(APP)"; \
    find "$(BLD_DIR)" -type f -print 2>/dev/null \
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

pass "selftest complete"
```

#### Repro pack (paste these exact files)

`m02/repro/01-shared-log.mk`

```make
.PHONY: all clean
all: a b
a:
    printf 'A\n' >> shared.log
b:
    printf 'B\n' >> shared.log
clean:
    rm -f shared.log
```

`m02/repro/02-temp-collision.mk`

```make
.PHONY: all clean
all: x y
x:
    printf 'X\n' > tmp.out
    mv -f tmp.out x.out
y:
    printf 'Y\n' > tmp.out
    mv -f tmp.out y.out
clean:
    rm -f tmp.out x.out y.out
```

`m02/repro/03-stamp-clobber.mk`

```make
# Demonstrates "always-run stamp" -> non-convergence by design.
.PHONY: all clean
all: out

out: in stamp
    cp in out

in:
    printf 'seed\n' > $@

stamp:
    date > $@

clean:
    rm -f out in stamp
```

`m02/repro/04-generated-header.mk`

```make
# BUG: missing atomic publish + sloppy modeling.
.PHONY: all clean
all: a b

a: gen.h
    printf '#include "gen.h"\nint main(){return X;}\n' > a.c
    $(CC) a.c -o a

b: gen.h
    printf '#include "gen.h"\nint main(){return X;}\n' > b.c
    $(CC) b.c -o b

gen.h:
    # Non-atomic write: consumer can observe partial content.
    printf '#define X 42\n' > gen.h

clean:
    rm -f a b a.c b.c gen.h
```

`m02/repro/05-mkdir-race.mk`

```make
.PHONY: all clean
all: out/a out/b

out/a:
    mkdir out
    printf 'A\n' > $@

out/b:
    mkdir out
    printf 'B\n' > $@

clean:
    rm -rf out
```

> These are **broken on purpose**. Your job in Module 02 is to predict the failure signature under `-j`, then fix them using graph truth (unique writers, atomic publish, correct ordering).

### 3.2 The runbook you use under pressure

From `m02/`:

```sh
make help
make selftest
make -n <target>
make --trace <target>
make -p
```

**Interpretation rules (don’t freestyle them):**

* `-n` answers: *what would run?*
* `--trace` answers: *why did Make decide it must run?*
* `-p` answers: *what rules/variables did Make end up with after parsing/includes?*
* `selftest` answers: *is the DAG still truthful under serial and parallel scheduling?*

### 3.3 The definition of “correct under -j” for Module 02

You pass Module 02 only if all are true:

* **Convergence:** after a successful build, `make -q all` exits `0`.
* **Serial/parallel equivalence:** declared artifacts are hash-equal under `-j1` and `-jN`.
* **No poison artifacts:** failures do not leave plausible outputs behind.
* **No concurrency-dependent behavior:** `-j` changes speed, not semantics.

[Back to top](#top)

---

<a id="core1"></a>
## 4) Core 1 — What Make Parallelizes

### Definition

Make parallelizes **targets** (nodes), not “files in general” and not “recipe lines”.

### Semantics

A target becomes runnable when all its declared prerequisites are up-to-date. Under `-jN`, Make runs up to `N` runnable targets concurrently.

The entire failure mode is simple: **if the graph is missing an edge, Make will schedule an illegal interleaving**.

### Failure signatures

* `make -j` flakes but `make -j1` “works”.
* Two identical builds produce different outputs.
* `--trace` reveals a consumer target running before a producer’s output exists (or before it’s fully published).

### Minimal repro

Create `m02/repro/04-generated-header.mk`:

```make
# BUG: missing atomic publish + sloppy modeling.
.PHONY: all clean
all: a b

a: gen.h
    printf '#include "gen.h"\nint main(){return X;}\n' > a.c
    $(CC) a.c -o a

b: gen.h
    printf '#include "gen.h"\nint main(){return X;}\n' > b.c
    $(CC) b.c -o b

gen.h:
    # Non-atomic write: consumer can observe partial content.
    printf '#define X 42\n' > gen.h

clean:
    rm -f a b a.c b.c gen.h
```

Run:

```sh
make -f repro/04-generated-header.mk clean
make -f repro/04-generated-header.mk -j2 all
```

### Fix pattern

* Make the producer a **real target** with **single-writer** ownership.
* Publish generated outputs **atomically** (temp → rename).
* Ensure consumers have a **real prerequisite edge** to the generated file(s) (or to a stamp that models them).

### Proof hook

After the fix, this must be stable:

```sh
make -f repro/04-generated-header.mk clean
make -f repro/04-generated-header.mk -j8 all
make -f repro/04-generated-header.mk -j8 all   # second run must be a no-op
```

[Back to top](#top)

---

<a id="core2"></a>
## 5) Core 2 — Parallel-Safety Contract

### Definition

A build is parallel-safe iff **every output path has exactly one writer** and recipes **publish atomically**.

### Semantics

Parallelism makes races visible; it does not create them. A race exists whenever:

* two targets can write the same path, or
* a consumer can observe a partially published artifact, or
* multiple recipes append to the same file, or
* directory creation is non-idempotent across concurrent recipes.

### The Parallel-Safety Contract (verbatim; you will reuse it)

1. **One writer per output path.** If two recipes can publish the same path, the build is incorrect.
2. **Publish `$@` only at the end.** Write to a temp, then `mv` into place.
3. **Temps are unique per output.** Safest is “derived from `$@`”. PID suffix is optional, but if you use PID: in Make recipes `$$$$` becomes `$$` in the shell.
4. **Failure hygiene is mandatory.** `.DELETE_ON_ERROR` plus explicit temp cleanup on failure paths.
5. **No shared appends.** `>> shared.log` from multiple recipes is nondeterminism by definition.

### Failure signatures

* “Works after clean” (poison artifacts or missing prereqs).
* Nondeterministic logs/manifests/stamps.
* Random `File exists` / `No such file or directory` during directory creation.
* Builds that “stabilize” only when output is synchronized (that’s not a fix; it’s sedation).

### Minimal repro

`m02/repro/01-shared-log.mk`:

```make
.PHONY: all clean
all: a b
a:
    printf 'A\n' >> shared.log
b:
    printf 'B\n' >> shared.log
clean:
    rm -f shared.log
```

Run repeatedly:

```sh
make -f repro/01-shared-log.mk clean
make -f repro/01-shared-log.mk -j2 all
cat shared.log
```

### Fix pattern

* Per-target logs (`a.log`, `b.log`) produced by single writers.
* One aggregation target (`shared.log: a.log b.log`) that concatenates deterministically.

### Proof hook

The fixed build must produce identical content across runs:

```sh
make -f repro/01-shared-log.mk clean
make -f repro/01-shared-log.mk -j8 all
cksum shared.log
make -f repro/01-shared-log.mk clean
make -f repro/01-shared-log.mk -j8 all
cksum shared.log   # must match
```

[Back to top](#top)

---

<a id="core3"></a>
## 6) Core 3 — Ordering Tools That Don’t Lie

### Definition

Ordering in Make must represent **semantic dependency**, not “I want this first”.

### Semantics

Use the smallest tool that expresses the truth:

| Need                                                       | Correct tool             | What it means              | Common misuse                                                |
| ---------------------------------------------------------- | ------------------------ | -------------------------- | ------------------------------------------------------------ |
| Y depends on X’s content                                   | `Y: X`                   | X changes ⇒ Y must rebuild | Replacing with order-only to “avoid rebuilds” (that’s lying) |
| Y needs X to exist, but X’s mtime must not trigger rebuild | `Y: \| X`                | existence barrier only     | Using real prereq on dirs ⇒ rebuild storms                   |
| Hidden input changes outputs                               | stamp/manifest prereq    | semantic state is modeled  | writing “always-run stamp” ⇒ non-convergence                 |
| You need a boundary but none exists                        | introduce an artifact    | create a file boundary     | serializing instead of modeling                              |
| You can’t model it cleanly                                 | `.NOTPARALLEL` / `.WAIT` | last resort serialization  | using as first fix (masking a lying DAG)                     |

### Failure signatures

* “Touching a directory triggers rebuilds.”
* “Changing flags doesn’t rebuild.”
* “Randomly rebuilds every time” (stamp drift).
* “Fixed by adding `.NOTPARALLEL`” (translation: you didn’t fix it).

### Minimal repro

Directory storm mistake:

```make
# BUG: out rebuilds whenever dir's mtime changes.
out: in dir/
    cp in out

dir/:
    mkdir -p dir
```

### Fix pattern

* Prefer directory creation inside recipes: `mkdir -p "$(@D)"`.
* Use order-only only when a separate directory target is justified.

### Proof hook

After fixing, this must hold:

```sh
make all
touch build/        # or any directory used for outputs
make -n all         # should show no rebuild caused *only* by directory mtime noise
```

[Back to top](#top)

---

<a id="core4"></a>
## 7) Core 4 — Large-Project Structure Without Recursive Make Rot

### Definition

Scaling is not “more Make tricks”. Scaling is **predictable layering** while keeping one DAG.

### Semantics

A maintainable large build has:

* A **single top-level orchestrator** (`Makefile`) that owns the public API.
* An `mk/` layer split by responsibility:

  * `common.mk` = policy/flags (boring, stable)
  * `objects.mk` = rooted + sorted discovery and mappings
  * `rules.mk` = rules (compile/link/codegen)
* Optional local overrides via `-include config.mk` that must not change correctness guarantees.

**Hard rule:** recursive make is not your default architecture. If you recurse, it’s a boundary with explicit inputs/outputs (treated like a tool invocation, not “more DAG”).

### Failure signatures

* “Works on my machine” via override leakage.
* Unexplained rebuilds from environment exports.
* Jobs collapse / weird concurrency due to sub-make misuse.
* Hidden cross-directory deps because each subdir has its own private DAG.

### Minimal repro

Accidental override rot:

```make
-include config.mk
CFLAGS += -O2
```

If `config.mk` changes semantics silently (or is missing in CI), you’ve created two builds.

### Fix pattern

* `config.mk` is allowed only for *local ergonomics*, not correctness (e.g., `DEBUG=1`, paths).
* Anything that changes semantics must be modeled as a stamp/manifest prerequisite (Module 01 pattern; Module 03 productionizes it).

### Proof hook

You must be able to run:

```sh
rm -f config.mk
make clean && make selftest
```

and still pass.

[Back to top](#top)

---

<a id="core5"></a>
## 8) Core 5 — Selftests + Race Repro Pack

### Definition

A scalable Make system is one that can **prove** it’s not lying.

### Semantics

Your selftest must enforce two invariants:

1. **Convergence:** build, then `make -q all` must exit `0`.
2. **Serial/parallel equivalence:** clean build under `-j1` and `-jN` must match on a declared artifact set.

And your repro pack must teach the only skill that matters under `-j`: **predicting the failure signature from the graph bug**.

### Failure signatures

* Selftest passes once but fails intermittently (unstable outputs or discovery).
* Convergence fails (stamp drift, phony misuse, touching outputs unnecessarily).
* Equivalence fails (multi-writer, non-atomic publish, missing edges).

### Minimal repro

`m02/repro/02-temp-collision.mk`:

```make
.PHONY: all clean
all: x y
x:
    printf 'X\n' > tmp.out
    mv -f tmp.out x.out
y:
    printf 'Y\n' > tmp.out
    mv -f tmp.out y.out
clean:
    rm -f tmp.out x.out y.out
```

### Fix pattern

Temp derived from `$@` (unique per output), then atomic rename:

```sh
tmp="$@.tmp"
```

### Proof hook

You must be able to run each repro until it fails, then apply the fix and make it stable under `-j8`.

[Back to top](#top)

---

<a id="capstone"></a>
## 9) Capstone Sidebar

Capstone is corroboration and an engineering-grade example—not the lesson itself.

### Runbook (from repo root)

```sh
make -C make-capstone selftest
make -C make-capstone discovery-audit
make -C make-capstone --trace all
```

### Where to look (file map)

* Parallel-safe primitives (atomic publish, assertions): `make-capstone/mk/macros.mk`
* Discovery and mapping (rooted + sorted): `make-capstone/mk/objects.mk`
* Hidden-input modeling (stamps/manifests): `make-capstone/mk/stamps.mk`
* Orchestration/public API: `make-capstone/Makefile`
* Selftest harness: `make-capstone/tests/run.sh`
* Race teaching pack: `make-capstone/repro/*.mk`

[Back to top](#top)

---

<a id="exercises"></a>
## 10) Exercises

Format is always **Task → Expected → Forensics → Fix**.

### Exercise 1 — Make parallelism confess

* **Task:** `make -j8 all --trace`
* **Expected:** only runnable targets schedule concurrently; rebuild reasons are explicit.
* **Forensics:** paste the `--trace` line that made each target run.
* **Fix:** missing prereq edge, multi-writer output, or stamp drift.

### Exercise 2 — Predict and fix a shared-append race

* **Task:** run `repro/01-shared-log.mk` under `-j2` until you see nondeterminism.
* **Expected:** log ordering/content varies across runs.
* **Forensics:** show that both writers are runnable concurrently (that’s the entire bug).
* **Fix:** per-target logs + a single aggregation target.

### Exercise 3 — Predict and fix a temp collision

* **Task:** run `repro/02-temp-collision.mk` under `-j2` repeatedly.
* **Expected:** eventually corrupted or swapped outputs.
* **Forensics:** identify the shared path (`tmp.out`) as the multi-writer output.
* **Fix:** `tmp="$@.tmp"` + atomic rename.

### Exercise 4 — Predict and fix a mkdir race

* **Task:** run `repro/05-mkdir-race.mk` under `-j2`.
* **Expected:** intermittent “File exists”.
* **Forensics:** both recipes execute `mkdir dir` concurrently.
* **Fix:** `mkdir -p "$(@D)"` or a correctly modeled idempotent directory target.

### Exercise 5 — Build-system proof (not “it seems fine”)

* **Task:** implement `selftest` in `m02/Makefile` enforcing convergence + serial/parallel equivalence.
* **Expected:** `make selftest` passes, repeatedly.
* **Forensics:** if it fails, the *first* divergence is diagnosed with `--trace`.
* **Fix:** tighten the graph, fix atomic publishing, fix stamps, fix discovery.

[Back to top](#top)

---

<a id="closing"></a>
## 11) Closing Criteria

You pass Module 02 only if you can demonstrate (in the **Module 02 simulator**, not only capstone):

* `make selftest` enforces convergence and serial/parallel equivalence.
* Every real artifact has exactly one writer, and publishing is atomic.
* You can take each repro, predict the failure, fix it with a graph change (not serialization), and prove stability under `-j`.
* Your build scales via layering (`mk/*.mk`, optional overrides) while remaining a single top-level DAG.

Next: Module 03 makes determinism, CI contracts, and build-system selftests non-negotiable at production pressure.

[Back to top](#top)

---