<a id="top"></a>
# Module 05 — Hardening: Portability, Jobserver, Hermeticity, Performance, and Failure Modes

This module turns “a correct build” into a **declared contract** with **auditable assumptions**. You stop trusting your workstation, your shell, your locale, your toolchain, and your process—and you model what matters.

A hardened build system has two properties:

1. it **degrades intentionally** (portability, feature gates, fallbacks), and
2. it **proves itself** (convergence, equivalence, negative tests, and measurement).

---

<a id="toc"></a>
## 1) Table of Contents

1. [Table of Contents](#toc)
2. [Learning Outcomes](#outcomes)
3. [How to Use This Module](#usage)
4. [Core 1 — Portability Contract and Version Gates](#core1)
5. [Core 2 — Jobserver and Controlled Recursion](#core2)
6. [Core 3 — Hermeticity by Modeling Inputs](#core3)
7. [Core 4 — Performance Engineering](#core4)
8. [Core 5 — Failure Modes, Migration Rubric, Canon, Anti-Patterns](#core5)
9. [Capstone Sidebar](#capstone)
10. [Exercises](#exercises)
11. [Closing Criteria](#closing)

---

<a id="outcomes"></a>
## 2) Learning Outcomes

By the end, you can:

* Declare a **Make contract**: minimum GNU Make, required shell behavior, required tools, and controlled fallbacks.
* Prove parallel scheduling survives boundaries: **jobserver tokens propagate**, recursion is bounded, and diagnostics are readable.
* Model “hermetic enough” builds: inputs are explicit, **stamps are convergent**, attestations don’t poison artifacts.
* Measure and reduce Make overhead using profiling, trace volume, and parse-time cost control.
* Decide when Make is no longer the core tool using a rubric, and migrate via safe hybrids without losing your proof harness.

[Back to top](#top)

---

<a id="usage"></a>
## 3) How to Use This Module

### 3.1 The five commands (your default loop)

Run these in *every* hardening incident:

1. **Confess what would run**

   ```sh
   make -n all
   ```
2. **Show why it ran**

   ```sh
   make --trace all
   ```
3. **Dump the resolved world (rules/vars)**

   ```sh
   make -p > build/make.dump
   ```
4. **Prove convergence**

   ```sh
   make all && make -q all
   ```
5. **Measure**

   ```sh
   make trace-count

   (/usr/bin/time -p make -n all >/dev/null) 2>&1
   ```

### 3.2 Escalation ladder (when you’re stuck)

* Add `--warn-undefined-variables` to catch silent expansion bugs.
* Add `-rR` and `.SUFFIXES:` to eliminate built-in rule noise.
* Add `--output-sync=recurse` under `-j` when logs become unusable.
* Reduce to a minimal repro Makefile that demonstrates the failure in ≤20 lines.

### 3.3 “Correct” means (hardening edition)

A hardened build must satisfy all:

* **Contracted environment**: minimum GNU Make version, shell flags, and portability gates are explicit.
* **Bounded recursion**: if recursion exists, it is intentional, jobserver-aware, and depth-capped.
* **Modeled inputs**: toolchain identity and relevant env/flags are captured as stamps/manifests.
* **Attestation doesn’t contaminate**: metadata is produced without injecting entropy into equivalence artifacts.
* **Measured**: you can produce at least one trace-volume metric and one timed parse/decision metric.
* **Proof harness exists**: convergence + equivalence + at least one negative test.

[Back to top](#top)

---

<a id="core1"></a>
## 4) Core 1 — Portability Contract and Version Gates

### Definition

A portability contract is a **declared, testable boundary**: *which Make*, *which features*, *which shell*, and *which fallbacks*.

### Semantics

* GNU Make features are not “available”; they are **conditional capabilities**. You must gate them by `$(MAKE_VERSION)`.
* “Portable shell” means POSIX `/bin/sh` behavior. Don’t assume Bash features.
* Your contract must separate:

    * **required** (fail fast) vs
    * **optional** (warn + safe fallback).

### Failure signatures

* Builds succeed locally but fail in CI (different Make versions / different shell).
* A feature silently does nothing (e.g., `.WAIT` not supported).
* Paths break on Windows/MSYS2; timestamps skew; whitespace in `MAKEFLAGS` handling breaks recursion.

### Minimal repro

**Repro: using `.WAIT` unconditionally.**

```make
all: a b
a:
    @echo a
.WAIT:
b:
    @echo b
```

On versions without `.WAIT`, this is not the barrier you think it is.

### Fix pattern

**Gate features and provide a deterministic fallback.**

```make
# mk/contract.mk — feature gates, version checks (Module 05 discipline)

# GNU Make ≥ 4.3 required (core contract for grouped targets and full patterns).
# MAKE_VERSION is provided by GNU Make. If missing, this Make is unsupported.
ifeq ($(origin MAKE_VERSION),undefined)
  $(error This repository requires GNU Make (MAKE_VERSION not defined).)
endif

GNU_GE_4_3 := $(filter 4.3% 4.4% 5.%,$(MAKE_VERSION))
ifeq ($(GNU_GE_4_3),)
  $(error GNU Make >= 4.3 required for grouped targets and full patterns (found $(MAKE_VERSION)).)
endif

# Feature probes (used for optional demos; do not change core correctness).
HAVE_GROUPED_TARGETS := $(filter 4.3% 4.4% 5.%,$(MAKE_VERSION))
HAVE_WAIT            := $(filter 4.4% 5.%,$(MAKE_VERSION))
```

### Proof hook

* Prove the contract trips on unsupported Make:

  ```sh
  make -p | grep '^MAKE_VERSION'
  ```
* Prove the fallback path is active:

  ```sh
  make --trace all | sed -n '1,120p'
  ```

### Verified portability matrix (keep as your living boundary)

Use this as the explicit “what we rely on” table.

| Feature               |          GNU Make |                              bmake | Windows notes                           |
| --------------------- |------------------:| ---------------------------------: | --------------------------------------- |
| Jobserver tokens      |             ≥3.78 | Partial (`-j` local; no sub-pipes) | WSL: OK; MSYS2: fragile spacing         |
| `$(MAKE)` propagation |              Full |                            Partial | WSL: OK; MSYS2: timestamp skew observed |
| `.WAIT`               |              ≥4.4 |              No (`.ORDER` instead) | WSL: OK; MSYS2: skew risks              |
| Grouped targets `&:`  |              ≥4.3 |                                 No | WSL: OK; MSYS2: path escaping pain      |
| `.ONESHELL`           |             ≥3.82 |                                 No | WSL: OK; MSYS2: shell variance          |
| `--trace`             | ≥4.3 (contracted) |                                 No | WSL: OK; MSYS2: verbose output          |

(If you claim more than this, you must attach an audit command.)

[Back to top](#top)

---

<a id="core2"></a>
## 5) Core 2 — Jobserver and Controlled Recursion

### Definition

The jobserver is GNU Make’s token system that enforces `-jN` across the build. Recursion is acceptable only when it **participates in the same budget** and stays observable.

### Semantics

* Always invoke sub-make as `$(MAKE)`, never `make`.
  `$(MAKE)` is special: it propagates jobserver flags in `MAKEFLAGS`.
* If the recipe is a recursive make, prefix with `+` so it still runs under `-n` (dry-run semantics).
* Bound recursion by `MAKELEVEL`:

    * `MAKELEVEL=0`: top
    * `MAKELEVEL=1`: first recursion
    * deeper than your budget → fail fast.

### Failure signatures

* `make -j8` behaves like `-j1` inside subdirectories (jobserver not propagated).
* `make -n` “skips” recursion targets (missing `+`).
* Parallel builds hang (sub-make launched without jobserver tokens, or deadlocking on inherited auth).

### Minimal repro

**Repro A: jobserver lost**

```make
sub:
    @make -C thirdparty all   # WRONG
```

**Repro B: dry-run lies**

```make
sub:
    @$(MAKE) -C thirdparty all  # still skipped under -n unless prefixed
```

### Fix pattern

```make
# Depth cap
ifeq ($(MAKELEVEL),2)
  $(error recursion too deep: MAKELEVEL=$(MAKELEVEL))
endif

.PHONY: thirdparty
thirdparty:
    +@$(MAKE) -C thirdparty all --no-print-directory
```

**Diagnostics (safe logging)**

```make
diag:
    @echo "MAKELEVEL=$(MAKELEVEL)"
    @echo "$(MAKEFLAGS)" | sed 's/--jobserver-auth=[^ ]*/--jobserver-auth=REDACTED/'
```

### Proof hook

* Prove propagation:

  ```sh
  make -j4 thirdparty --trace | grep -E '\$\(MAKE\)|jobserver|MAKEFLAGS' -n
  ```
* Prove dry-run correctness:

  ```sh
  make -n thirdparty | grep thirdparty
  ```

[Back to top](#top)

---

<a id="core3"></a>
## 6) Core 3 — Hermeticity by Modeling Inputs

### Definition

Hermeticity here does **not** mean “rebuild the world in a sandbox”. It means: *if an input can change an output, the graph models it*—without turning metadata into entropy.

### Semantics

* **Stamps/manifests** represent hidden inputs (tool versions, flags, env).
* Use **order-only prerequisites** (`|`) when you need the stamp present but do not want it to trigger rebuilds.
* Attestation is **post-build metadata**, not part of artifact identity, unless you explicitly choose otherwise.

### Failure signatures

* You “added attestations” and now hashes differ every run (you injected non-determinism).
* Changing compilers doesn’t rebuild when it should (tool identity not modeled).
* Environment drift causes mysterious output changes (locale/timezone/paths not pinned or modeled).

### Minimal repro

**Repro: attestation contaminates artifact identity**

```make
all: app attest    # WRONG: attest now participates in “all” artifact set
attest:
    date > build/attest.txt
```

### Fix pattern

**A) Tool + env stamps as order-only, metadata separate**

```make
SHELL := /bin/sh
.SHELLFLAGS := -eu -c

export LC_ALL := C
export TZ := UTC

stamps/tool/cc.txt: FORCE | stamps/tool/
    @$(CC) --version > $@
stamps/env.txt: FORCE | stamps/
    @printf 'LC_ALL=%s\nTZ=%s\nPATH=%s\n' "$$LC_ALL" "$$TZ" "$$PATH" > $@

# app does not rebuild because stamps changed, but metadata can be produced deterministically.
app: main.o | stamps/tool/cc.txt stamps/env.txt
    @$(CC) -o $@ main.o

attest: | stamps/tool/cc.txt stamps/env.txt
    @cat stamps/tool/cc.txt stamps/env.txt > build/attest.txt

FORCE:
stamps/ stamps/tool/:
    @mkdir -p $@
```

**B) If flags/tool changes must force rebuild, make the stamp a *real prerequisite* of the compilation steps**
(That’s “correctness-first mode”; pick intentionally.)

### Proof hook

* Prove attest does not poison equivalence artifacts:

  ```sh
  make clean all && sha256sum app
  make attest && sha256sum app   # same hash
  ```
* Prove stamps exist and are stable enough to diff:

  ```sh
  diff -u build/attest.txt build/attest.txt || true
  ```

[Back to top](#top)

---

<a id="core4"></a>
## 7) Core 4 — Performance Engineering

### Definition

Make performance issues are typically **self-inflicted parse-time work**: repeated `wildcard`, repeated `patsubst`, or `$(shell ...)` used as a compute engine.

### Semantics

* Parse-time is the enemy: anything executed during expansion happens *before* the DAG is even scheduled.
* “Fast enough” must be evidenced by:

    * trace volume for representative goals (`make trace-count`),
    * a timed parse/decision run (e.g., `(/usr/bin/time -p make -n all >/dev/null) 2>&1`),
    * and stable discovery (no churn).

### Failure signatures

* “Make is slow” and the timed `make -n all` run shows most time is spent before the DAG is scheduled (often heavy function expansion or `$(shell ...)`).
* `--trace | wc -l` explodes because the graph is defined redundantly.
* Rebuild churn from unstable discovery lists.

### Minimal repro

```make
# WRONG: repeated expensive work
SRCS = $(wildcard src/*.c)
OBJS = $(patsubst src/%.c,build/%.o,$(wildcard src/*.c))
```

### Fix pattern

```make
SRCS := $(sort $(wildcard src/*.c))
OBJS := $(patsubst src/%.c,build/%.o,$(SRCS))
```

* If you need expensive computation, move it into a target (a manifest), not `$(shell ...)`.

### Proof hook

Capture baseline metrics:

```sh
mkdir -p build
make trace-count | tee build/trace.before
(/usr/bin/time -p make -n all >/dev/null) 2>&1 | tee build/time.before
```

After your change, capture again and diff:

```sh
make trace-count | tee build/trace.after
(/usr/bin/time -p make -n all >/dev/null) 2>&1 | tee build/time.after
diff -u build/trace.before build/trace.after || true
diff -u build/time.before build/time.after || true
```

Treat `trace-count` as a heuristic (a signal), not a gate.

[Back to top](#top)

---

<a id="core5"></a>
## 8) Core 5 — Failure Modes, Migration Rubric, Canon, Anti-Patterns

### Definition

This core is where you stop pretending every problem is solvable “with better Make”. It also gives you a pasteable canon of patterns you can deploy without improvisation.

### Semantics

* Make is excellent when:

    * outputs are files,
    * dependencies are expressible as edges,
    * and concurrency hazards are controlled.
* Make becomes the wrong core tool when:

    * you need remote caching/sandboxing as a first-class guarantee,
    * non-file semantics dominate,
    * platform/config matrix dominates the Makefiles.

### Migration Rubric: When to Stay vs. Hybrid vs. Migrate

Use this concrete decision framework:

| Question                                      | Stay with Make                  | Consider Hybrid                        | Migrate Away                          |
|-----------------------------------------------|---------------------------------|----------------------------------------|---------------------------------------|
| Primary outputs are files with clear deps?    | Yes                             | Maybe                                  | No                                    |
| Concurrency hazards modelable with edges?     | Yes                             | Yes                                    | No                                    |
| Need remote caching/sandboxing first-class?   | No                              | Yes (wrap tools like Bazel/Ninja)      | Yes                                   |
| Configuration matrix dominates Makefiles?     | No                              | Maybe                                  | Yes                                   |
| Non-file tasks (deploy, DB migrations) central?| No                              | Yes                                    | Yes                                   |

**Safe hybrid examples**:
- Keep Make as top-level orchestrator with public API and proofs.
- Delegate subsystems via stamped targets:
  ```make
  rust-lib: rust.stamp
      +cargo build --release
      touch rust.stamp
  app: rust-lib $(OBJS)
      $(CC) ... rust-lib/target/release/lib.a
  ```
- Treat external tools as black-box producers with explicit stamp boundaries.

This ensures deliberate evolution while preserving verification (selftests remain valid).

### Failure signatures (canonical)

* **Non-convergence**: second run still does work.
* **Serial/parallel mismatch**: `-j1` output differs from `-jN`.
* **Heisenbugs**: races disappear under `-j1` or “after clean”.
* **Entropy injection**: metadata becomes part of artifact identity unintentionally.
* **Recursion collapse**: sub-build ignores jobserver budget.

### Minimal repro

**Repro: shared append race (two writers, one file)**

```make
all: a b
a:
    @echo A >> build/log.txt
b:
    @echo B >> build/log.txt
```

Under `-j`, the interleavings are nondeterministic; under enough stress you’ll see corruption or order variance.

### Fix pattern

* One writer per output. If you need aggregation, model it as a separate target that **reads** inputs and atomically publishes a single output.

### Proof hook

* Prove the bug exists:

  ```sh
  rm -f build/log.txt; make -j8 all; cat build/log.txt
  ```
* Prove the fix removes nondeterminism:

  ```sh
  rm -f build/log.txt; make -j8 all; sha256sum build/log.txt
  rm -f build/log.txt; make -j8 all; sha256sum build/log.txt  # same
  ```

### Pasteable canon (10 patterns, with invariants)

These are intentionally boring. Each exists to eliminate a known class of failures.

1. **Atomic publish + delete on error**

```make
.DELETE_ON_ERROR:
%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@.tmp && mv -f $@.tmp $@
```

2. **Directory scaffold (order-only)**

```make
build/subdir: | build/
    mkdir -p $@
build/:
    mkdir -p $@
```

3. **Depfiles (`.d`) + inclusion**

```make
OBJS := foo.o bar.o
%.o: %.c
    $(CC) $(CFLAGS) -MD -MF $(@:.o=.d) -c $< -o $@
-include $(OBJS:.o=.d)
```

4. **Grouped multi-output with version fallback (≥4.3)**

```make
ifeq ($(filter 4.3% 4.4% 5.%,$(MAKE_VERSION)),)
gen.h: gen.py ; $(PYTHON) $<
gen.c: gen.py ; $(PYTHON) $<
else
gen.h gen.c &: gen.py ; $(PYTHON) $<
endif
```

5. **Toolchain identity stamp (order-only)**

```make
stamps/cc.txt: | stamps/
    tmp=$@.tmp.$$; $(CC) --version > $$tmp; \
    if ! cmp -s $$tmp $@ 2>/dev/null; then mv -f $$tmp $@; else rm -f $$tmp; fi
app: main.o | stamps/cc.txt
    $(CC) -o $@ main.o
```

6. **Docker context hash stamp**
   (Only works if your context file list is explicit and stable.)

7. **Non-recursive Rust aggregation**
   (Prefer a single DAG; treat Cargo as a tool invocation.)

8. **CI up-to-date check (`-q` exit semantics)**

```make
ci-check:
    @$(MAKE) -q all; echo $$?
```

9. **Environment pin + env stamp (convergent vs attest)**

Convergent stamp (safe to be in `all`’s closure):

```make
export LC_ALL := C
stamps/env.txt: | stamps/
    tmp=$@.tmp.$$; printf 'LC_ALL=%s\n' "$$LC_ALL" > $$tmp; \
    if ! cmp -s $$tmp $@ 2>/dev/null; then mv -f $$tmp $@; else rm -f $$tmp; fi
app: main.o | stamps/env.txt
```

Attestation stamp (uses `FORCE`; keep it out of `all`):

```make
attest: stamps/env.txt
stamps/env.txt: FORCE | stamps/
    printf 'LC_ALL=%s\n' "$$LC_ALL" > $@
```

10. **Normalized archive**

```make
dist.tar.gz: all
    # Portable, reproducible archive (stable order + fixed mtimes), matching capstone.
    $(PYTHON) scripts/mkdist.py $@ build/
```


### Anti-pattern gallery (memorize the smell)

* `.PHONY` on real file targets → perpetual rebuild loops.
* “Always-run stamp” (`stamp: ; date > $@`) → non-convergence by design.
* Temp collisions (`tmp=build/tmp`) under parallelism → intermittent corruption.
* Parse-time discovery via `$(shell find / ...)` → nondeterminism + slowness.
* Recursive make via `make -C` (not `$(MAKE)`) → jobserver collapse.

[Back to top](#top)

---

<a id="capstone"></a>
## 9) Capstone Sidebar

Use capstone to validate, not to learn the basics.

### Runbook (repo root)

```sh
make -C make-capstone portability-audit
make -C make-capstone selftest
make -C make-capstone attest
make -C make-capstone trace-count
make -C make-capstone perf
```

### Where to look (file map)

* Contract gates + probes: `make-capstone/mk/contract.mk`
* Atomic helpers and safe shell patterns: `make-capstone/mk/macros.mk`
* Object rules + depfiles: `make-capstone/mk/objects.mk`
* Convergent stamps/manifests: `make-capstone/mk/stamps.mk`
* Proof harness (convergence/equivalence/negative/perf): `make-capstone/tests/run.sh`
* Race repro pack: `make-capstone/repro/*.mk`
* Codegen stressors: `make-capstone/scripts/*`

[Back to top](#top)

---

<a id="exercises"></a>
## 10) Exercises

Each exercise is **Task → Expected → Forensics → Fix**.

### Exercise 1 — Add a hard GNU Make floor

* **Task:** enforce GNU Make ≥ 4.3 at parse-time.
* **Expected:** unsupported Make fails immediately with a clear error.
* **Forensics:** `make -p | grep '^MAKE_VERSION'`.
* **Fix:** use prefix filtering (`4.% 5.%`), not naive string comparisons.

### Exercise 2 — Prove jobserver propagation across recursion

* **Task:** create `thirdparty/Makefile` with a slow target and call it from the root.
* **Expected:** `make -j4 thirdparty` respects the same job budget.
* **Forensics:** `make --trace -j4 thirdparty | grep -n '\-C thirdparty'`.
* **Fix:** replace `make` with `$(MAKE)`; add `+` to preserve dry-run semantics.

### Exercise 3 — Hermeticity-by-modeling: tool and env stamps

* **Task:** implement `stamps/tool/cc.txt` and `stamps/env.txt`.
* **Expected:** stamps update when inputs drift; `app` rebuild behavior matches your chosen policy (order-only vs real prereq).
* **Forensics:** `make --trace app` and inspect which prereq triggered.
* **Fix:** make stamps convergent; avoid writing timestamps unless explicitly intended.

### Exercise 4 — Attestation must not poison equivalence artifacts

* **Task:** add `attest` target that writes `build/attest.txt`.
* **Expected:** running `make attest` does not change the hash of build outputs.
* **Forensics:** `sha256sum app` before/after.
* **Fix:** do not include `attest` in `all` prerequisites; keep it post-build.

### Exercise 5 — Remove one avoidable parse-time cost

* **Task:** introduce a deliberately repeated expansion; measure; then cache it.
* **Expected:** trace-count and timed `make -n all` show reduced parse/decision cost; build behavior unchanged.
* **Forensics:** diff your `build/trace.*` and `build/time.*` before/after; confirm `make -q all`.
* **Fix:** compute discovery lists once; push expensive work into targets.

### Exercise 6 — Migration drill (hybrid boundary)

* **Task:** wrap an external build tool behind a single Make target with an explicit stamp.
* **Expected:** Make remains the orchestrator; proof harness still validates declared artifacts.
* **Forensics:** demonstrate `selftest` (or your local equivalent) still proves equivalence.
* **Fix:** treat external system as a black box; don’t dissolve your artifact boundary.

[Back to top](#top)

---

<a id="closing"></a>
## 11) Closing Criteria

You are done only when all proofs pass:

1. **Contract proof**: unsupported GNU Make fails fast; supported versions warn+fallback correctly.
2. **Recursion proof**: `$(MAKE)` is used everywhere recursion exists; jobserver propagation is observable; `MAKELEVEL` is bounded.
3. **Hermeticity proof**: tool/env/flags are modeled via convergent stamps/manifests; you can explain every rebuild with `--trace`.
4. **Attestation proof**: `attest` produces metadata without changing artifact hashes (unless explicitly designed to).
5. **Performance proof**: you can demonstrate at least one removed parse/decision-time cost using trace-count and timing.
6. **Failure-mode proof**: you can reproduce (and then eliminate) at least one nondeterminism bug (shared append, temp collision, or missing edge).
7. **Decision proof**: if rubric says “hybrid”, you can keep Make’s public API stable while delegating internals safely.

[Back to top](#top)

---