<a id="top"></a>

# Deep Dive Make: The Course-Book Outline

A five-module course-book that treats **GNU Make as a build-graph engine** with a strict correctness contract:

- **Truthful DAG**: every real dependency edge is declared.
- **Atomic outputs**: artifacts are published only on success.
- **Parallel safety**: `-j` changes throughput, not semantics.
- **Determinism**: serial and parallel runs converge to identical results.
- **Testable invariants**: correctness is verified, not assumed.

This repository contains both the text (**`course-book/`**) and a runnable reference implementation (**`make-capstone/`**) that proves the claims.

---

## Module 01 — Foundations: The Graph, the Truth, the Rules

1. **Make’s execution model (DAG evaluation)**
   Targets, prerequisites, recipes, default goals—and the central idea: Make executes what the graph declares runnable.

2. **Rebuild semantics and convergence**
   mtimes, existence checks, hidden inputs, and the practical invariant: a correct build *converges* (`make -q` eventually goes green).

3. **Rule design that scales**
   Explicit rules vs patterns vs static patterns; controlled fan-out; and why naïve multi-target rules lie unless you model single-invocation semantics.

4. **Variables and expansion discipline**
   Parse-time vs run-time; `:=` vs `=`; avoiding entropy via `$(shell ...)`; inspecting provenance with `origin` / `flavor` / `value`.

5. **Correct publication and failure hygiene**
   temp→rename publishing, `.DELETE_ON_ERROR`, depfiles (`.d`) as first-class edges, and eliminating “poison artifacts” after failures.

**Deliverable:** A small Makefile that (1) converges, (2) rebuilds correctly on header edits via depfiles, (3) models at least one hidden input, (4) publishes atomically, and (5) remains correct after an induced failure.

[Back to top](#top)

---

## Module 02 — Scaling: Parallelism Without Accidents

1. **What Make parallelizes**
   `-j` parallelizes runnable *targets*; missing edges become illegal interleavings; diagnosing serial vs parallel behavior with `--trace`.

2. **A parallel-safety contract**
   One-writer-per-path, atomic publish, and a race taxonomy: shared appends/logs, temp collisions, mkdir hazards, partial writes.

3. **Ordering tools that preserve truth**
   Real prerequisites vs order-only (`|`) vs semantic stamps/manifests; boundaries and last-resort serialization (`.WAIT`, `.NOTPARALLEL`).

4. **Large-project structure without recursive-make decay**
   One public DAG, a stable top-level API, layered `mk/` includes, and configuration overrides that cannot mutate correctness.

5. **Selftests and a race repro pack**
   Convergence and serial/parallel equivalence as gates; repros that train you to map failure signatures back to graph defects.

**Deliverable:** A parallel-safe build with selftests enforcing convergence + serial/parallel equivalence, plus a repro pack demonstrating and fixing at least three distinct race classes.

[Back to top](#top)

---

## Module 03 — Production Practice: Determinism, CI Contracts, and a Disciplined DSL

1. **Determinism under change**
   Stable discovery (rooted + sorted), no parse-time randomness, single-writer generators, and modeling tool/flag/environment inputs.

2. **A forensic debugging ladder**
   `-n` (what), `--trace` (why), `-p` (what Make evaluated), and the canonical signatures: missing edges, stamp lies, non-atomic publish, unstable discovery.

3. **CI as a contract**
   Public targets with behavior guarantees, strict failure semantics, and a separation between correctness artifacts and diagnostic/attestation outputs.

4. **Selftests for the build system**
   Convergence, serial/parallel equivalence, meaningful negative tests (hidden-input injection), and sandboxing so local state cannot “help.”

5. **A disciplined Make DSL**
   Use macros (`define`/`call`) to enforce invariants; quarantine `eval` so it is bounded, auditable, and disable-able without correctness loss.

**Deliverable:** A CI-ready contract (`all`/`test`/`selftest`), deterministic discovery, a selftest harness with a negative hidden-input test, and a quarantined `eval` demo.

[Back to top](#top)

---

## Module 04 — Semantics Under Pressure: CLI, Precedence, Includes, Rule Edge Cases

1. **CLI semantics for diagnosis**
   Outcome-changing flags: `-n`, `--trace`, `-p`, `-q`, `-W`, `-B`, `-rR`, and controlled invocation (`-C`, `-f`)—used to reveal defects, not mask them.

2. **Variable precedence and provenance**
   Practical precedence ladder (CLI/override/makefile/env/built-ins), export behavior, environment leakage, and inspecting `origin` / `flavor` / `value`.

3. **Conditionals and capability gates**
   Capability-based gating (features/tools/platform), fail-fast policies, and the rule: if detection affects outputs, it must be modeled.

4. **Includes and remake semantics**
   `include` vs `-include`, remaking included makefiles (restart model), include order stability, avoiding loops, and safe overrides.

5. **Rule semantics and special targets**
   Pattern ambiguity control, static patterns for bounded fan-out, correct multi-output modeling (grouped targets `&:` or stamp fallback), and last-resort parallel controls (`.WAIT`, `.NOTPARALLEL`, `.ONESHELL`, `.PHONY`).

**Deliverable:** A practical runbook: reproducible CLI debugging steps, proven variable provenance, a fixed include/restart issue, and a multi-output generator proven to run exactly once per logical generation.

[Back to top](#top)

---

## Module 05 — Hardening: Portability, Jobserver, Hermeticity, Performance, Failure Modes

1. **Portability boundary and version gates**
   Declare what you support: GNU Make floor, feature gates via `$(MAKE_VERSION)`, POSIX shell assumptions, and documented fallbacks.

2. **Jobserver and controlled recursion**
   Correct `$(MAKE)` propagation, `+` under `-n`, bounding recursion via `MAKELEVEL`, and recognizing deadlock/collapse signatures.

3. **Hermeticity by modeling inputs**
   Stamps/manifests for tools/flags/env; order-only prerequisites for “must exist but mustn’t trigger rebuild”; attestations that do not contaminate artifact identity unless explicitly chosen.

4. **Performance engineering**
   Parse-time vs run-time costs, `--profile` discipline, trace volume as a signal, and eliminating avoidable shell-outs and churny discovery.

5. **Failure modes and migration rubric**
   Canonical failure signatures, an anti-pattern gallery, safe hybrid boundaries, and a decision rubric for when Make stops being the right core tool.

**Deliverable:** A hardened capstone: portability audit + jobserver proof + modeled inputs + non-poisoning attestations + profiling guardrails + a migration drill demonstrating a clean hybrid boundary.

[Back to top](#top)

---

## Reference Implementation — The Capstone

The capstone is the executable realization of Modules 01–05:

- **Build system:** `make-capstone/Makefile` + `make-capstone/mk/*.mk`
- **Selftests:** `make-capstone/tests/run.sh` (convergence, serial/parallel equivalence, negative tests)
- **Repro pack:** `make-capstone/repro/*.mk` (intentional failures + fixes)
- **Generators:** `make-capstone/scripts/` (single-output and multi-output stress cases)

**Truth command:**
```sh
make -C make-capstone selftest
```

macOS:

```sh
gmake -C make-capstone selftest
```

[Back to top](#top)
