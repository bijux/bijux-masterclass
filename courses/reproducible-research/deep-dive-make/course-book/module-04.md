<a id="top"></a>
# Module 04 — Make Semantics Under Pressure: CLI, Precedence, Includes, and Rule Edge-Cases

Modules 01–03 taught you to build truthful graphs, survive `-j`, and enforce determinism and CI contracts. This module is the thing you reach for when you already *know* what you intend, but you need the exact semantics and the sharp edges—fast, provable, and without folklore.

Capstone exists here as **corroboration**: a runnable place where these semantics are exercised. The module stands on its own.

---

<a id="toc"></a>
## 1) Table of Contents

1. [Table of Contents](#toc)
2. [Learning Outcomes](#outcomes)
3. [How to Use This Module](#usage)
4. [Core 1 — CLI Semantics and Debug Control](#core1)
5. [Core 2 — Variables: Precedence, Scope, Export, Expansion](#core2)
6. [Core 3 — Conditionals and Capability Gates](#core3)
7. [Core 4 — Includes, Search, and Remake Semantics](#core4)
8. [Core 5 — Rule Semantics and Special Targets](#core5)
9. [Capstone Sidebar](#capstone)
10. [Exercises](#exercises)
11. [Closing Criteria](#closing)

---

<a id="outcomes"></a>
## 2) Learning Outcomes

By the end of this module, you can:

* Pick CLI options that **isolate** a failure mode (rather than mask it) and prove what changed.
* Predict variable resolution using precedence and scope, then **confirm it empirically** with introspection.
* Write conditional logic that gates **capabilities** (not OS matrices), without injecting hidden inputs.
* Use includes as architecture (layering + overrides) while staying aware of **restart/remake** semantics.
* Use advanced rule features (multi-output, selection, parallel controls) without breaking convergence or `-j` safety.
* Maintain a “special targets” mental map: what each does, when it’s justified, and what it ruins.

[Back to top](#top)

---

<a id="usage"></a>
## 3) How to Use This Module

### 3.1 The incident loop

When something looks wrong, you do this—always:

1. **Preview** what would run (no execution):

   ```sh
   make -n <target>
   ```
2. **Force causality**:

   ```sh
   make --trace <target>
   ```
3. **Dump the evaluated world** (rules, variables, resolved lists):

   ```sh
   make -p
   ```
4. **Only then** add temporary probes (remove immediately after):

  * `$(warning ...)`, `$(info ...)`, `$(error ...)`

### 3.2 What “correct” means in Module 04

This module is passed only if you can do **all** of this on demand:

* Given a symptom, choose the right semantic tool (`-W`, `-B`, `-q`, `-p`, `--trace`) and show the line(s) that prove the cause.
* Given a variable’s surprising value, prove **origin + flavor + raw value**, and show where it was last set.
* Given an “only under `-j`” issue, identify whether it is:

  * missing edge,
  * multi-writer output,
  * non-atomic publish,
  * unsafe multi-output generator rule,
  * or parallel-control misuse.

### 3.3 The two-minute harness

Every concept in this module can be validated with a tiny scratch Makefile:

```sh
mkdir -p /tmp/mkref && cd /tmp/mkref
cat > Makefile <<'MK'
all:
    @echo ok
MK
make --trace
```

You will replace that Makefile per “Minimal repro” blocks below.

[Back to top](#top)

---

<a id="core1"></a>
## 4) Core 1 — CLI Semantics and Debug Control

### Definition

The CLI is part of Make’s *observable semantics*: it can alter scheduling, staleness assumptions, built-in rule availability, verbosity, and exit behavior.

### Semantics

#### 1) The small set of options that actually change outcomes

| Option               | What it really does                        | Use it for                 | Don’t use it for                                             |
| -------------------- | ------------------------------------------ | -------------------------- | ------------------------------------------------------------ |
| `-n`                 | Expands/evaluates, but doesn’t run recipes | preview DAG actions        | assuming it “does nothing” (it still expands `$(shell ...)`) |
| `--trace`            | Prints *why* each target ran               | causality proof            | performance diagnosis                                        |
| `-p`                 | Dumps the evaluated rule/variable universe | forensic truth             | routine use in CI logs                                       |
| `-W file`            | Pretends `file` is newer than its targets  | simulate skew/staleness    | “fixing” dependency bugs by lying                            |
| `-B`                 | Pretends everything is out-of-date         | smoke a clean-ish rebuild  | replacing correct prerequisites                              |
| `-rR`                | Disables built-in rules and vars           | determinism + explicitness | builds that secretly rely on suffix magic                    |
| `-C dir` / `-f file` | Changes root / selects Makefile            | orchestration              | papering over bad structure                                  |

#### 2) Exit codes you must not misunderstand

* `make <target>`: `0` success, `2` error
* `make -q <target>` (query mode):

  * `0` up-to-date
  * `1` would rebuild (not an “error”; it’s a signal)
  * `2` actual error

### Failure signatures

* “CI says it would rebuild but local says green.” → you never used `-q` or you misread exit `1`.
* “It only fails when I add `-n`.” → you have parse-time effects (`$(shell ...)`, `!=`, generated includes).
* “`-B` ‘fixes’ it.” → your DAG is lying; you’re bypassing correctness.

### Minimal repro

**Repro A: `-W` proving stale edges without touching files**

```make
# Makefile
a: in
    @echo build-a > $@
in:
    @echo seed > $@

.PHONY: clean
clean: ; rm -f a in
```

Run:

```sh
make clean && make
make -W in --trace a
```

### Fix pattern

* Use `-W` to **simulate** staleness only while diagnosing.
* Use `-q` to encode convergence checks (Module 03 selftests).
* Use `-rR` in CI baselines if you want builds that don’t depend on implicit defaults.

### Proof hook

* Prove query semantics:

  ```sh
  make clean && make a
  make -q a; echo $?
  rm -f a
  make -q a; echo $?
  ```

  Expected: first prints `0`, second prints `1`.

[Back to top](#top)

---

<a id="core2"></a>
## 5) Core 2 — Variables: Precedence, Scope, Export, Expansion

### Definition

Variable behavior is Make’s hidden state machine: precedence decides **which value wins**, expansion decides **when it is computed**, and scope decides **where it applies**.

### Semantics

#### 5.1 Precedence ladder (practical model)

Highest wins:

1. **Command line**: `make VAR=...`
2. **`override` in makefiles** (can beat command line; use sparingly)
3. **Makefile assignments**
4. **Environment** (unless `-e` is used; with `-e` env jumps above makefile)
5. **Built-in defaults**

#### 5.2 Expansion modes (the two that matter)

| Operator | Expansion time         | What you use it for         | Typical failure                                                 |
| -------- | ---------------------- | --------------------------- | --------------------------------------------------------------- |
| `:=`     | immediate (“simple”)   | stable lists, computed once | rarely the problem                                              |
| `=`      | deferred (“recursive”) | true laziness (rare)        | self-referential growth; nondeterministic `$(shell ...)` timing |
| `?=`     | conditional default    | knobs                       | “why didn’t it apply?” due to earlier assignment                |
| `+=`     | append                 | flags                       | duplicates if base is recursive                                 |
| `!=`     | shell assignment       | avoid                       | hidden inputs + unstable timing                                 |

#### 5.3 Target-specific variables (scope trap)

Target-specific variables apply to that target and can propagate to prerequisites, but they do **not automatically export** as environment state to sub-makes.

### Failure signatures

* “Works locally, breaks in CI.” → env leaked (`-e`, exported vars, shell init), or precedence differs.
* “This variable explodes / duplicates flags.” → recursive `=` plus `+=`, or self-reference.
* “Sub-make didn’t get my flag.” → target-specific vars are not export semantics.

### Minimal repro

**Repro: precedence proven with introspection**

```make
CFLAGS := FILE

.PHONY: show show-e
show:
    @echo "origin=$(origin CFLAGS) flavor=$(flavor CFLAGS) value='$(value CFLAGS)'"

show-e:
    @$(MAKE) --no-print-directory -e show
```

Run:

```sh
export CFLAGS=ENV
make show
make show-e
make CFLAGS=CLI show
```

### Fix pattern

* Default to `:=` unless you can justify laziness.
* Avoid `-e` except when integrating legacy systems (and then stamp it / attest it).
* If exported variables affect outputs: either **pin** them (`export LC_ALL := C`) or **model** them (stamp/manifest).

### Proof hook

* You pass this core if you can point to:

  * the `origin` output for each case (file/env/command),
  * and you can explain why `-e` flips env precedence.

[Back to top](#top)

---

<a id="core3"></a>
## 6) Core 3 — Conditionals and Capability Gates

### Definition

Conditionals are configuration. Configuration scales only if it gates **capabilities** and stays **single-source** (computed once, used many times).

### Semantics

#### 6.1 What scales

* **Capability gating**: “do we have feature X?” (Make version / tool exists / platform primitive available)
* **Fragments**: include a small file per capability/platform rather than nesting branches forever
* **Fail-fast**: unsupported combos error early, not halfway through a build

#### 6.2 What rots

* Deep OS×tool×mode matrices embedded across multiple files
* Scattered `$(shell uname)` calls (hidden inputs, duplicated logic)
* “Soft fallback” that silently changes correctness behavior

### Failure signatures

* “Same inputs, different behavior per machine.” → capability detection isn’t centralized or isn’t stamped.
* “The build ‘mostly works’ but outputs differ.” → conditional flags changed but were not modeled (stamp).

### Minimal repro

**Repro: clean capability gate using `MAKE_VERSION`**

```make
# Pretend we require grouped targets (GNU Make ≥ 4.3)
HAVE_GROUPED := $(filter 4.3% 4.4% 4.5% 5%,$(MAKE_VERSION))

ifeq ($(HAVE_GROUPED),)
$(error "need grouped targets (&:) or provide fallback")
endif

all: ; @echo ok
```

### Fix pattern

* Put detection in one place.
* Expose capability booleans (`HAVE_X`) and use them everywhere.
* If detection affects outputs, treat it as an input (stamp/manifest) or pin via contract.

### Proof hook

* You can prove gating works by running:

  ```sh
  make -p | grep -E 'MAKE_VERSION|HAVE_GROUPED'
  ```

  and showing the computed feature variable.

[Back to top](#top)

---

<a id="core4"></a>
## 7) Core 4 — Includes, Search, and Remake Semantics

### Definition

Includes are architecture. They also introduce a rarely-understood semantic: **if Make remakes an included makefile, it restarts evaluation**.

### Semantics

#### 7.1 Include types

* `include foo.mk`: missing file is an error
* `-include foo.mk`: missing file is ignored (use for local overrides, depfiles)

#### 7.2 Remaking included makefiles (restart model)

If an included makefile is out-of-date and has a rule to build it, Make will:

1. build the included file,
2. then restart and re-read makefiles.

That’s a feature—until you create a loop.

#### 7.3 Include-order forensics

`MAKEFILE_LIST` is the include stack. It is the first tool you use to prove “where did this assignment come from?”

#### 7.4 Search (`VPATH`/`vpath`) is a truth hazard

It makes Make “find” prerequisites in alternate directories. That can hide where inputs came from. Prefer explicit paths and rooted discovery. If you must use it, treat it as part of the build contract.

### Failure signatures

* “Make keeps re-reading makefiles / never settles.” → generated include loop or nondeterministic include content.
* “It built the wrong file.” → `VPATH` resolved a prerequisite from an unexpected location.
* “Overrides behave randomly.” → include order changed; local override file is leaking into CI.

### Minimal repro

**Repro: include restart loop**

```make
include gen.mk

gen.mk: ; @echo "X:=1" > $@
all: ; @echo X=$(X)
```

Run `make` twice. Then break determinism by writing timestamps into `gen.mk` and watch it loop.

### Fix pattern

* Only generate makefiles if:

  * the generation is deterministic,
  * the generator is single-writer + atomic,
  * and it is covered by convergence tests.
* Use `-include` for optional local overrides; never require them for correctness.

### Proof hook

* Print include stack:

  ```make
  $(warning STACK=$(MAKEFILE_LIST))
  ```

  Then run `make -n` and show the include order is stable.

[Back to top](#top)

---

<a id="core5"></a>
## 8) Core 5 — Rule Semantics and Special Targets

### Definition

This is where senior engineers still get cut: pattern selection ambiguity, multi-output generators, and special targets that mutate Make’s behavior.

### Semantics

#### 8.1 Pattern selection and ambiguity control

* Keep patterns non-overlapping.
* Prefer static pattern rules when fan-out must be controlled.
* When behavior surprises you: `make -p` and search for the chosen rule.

#### 8.2 Multi-output generators: one invocation or you’re lying

If one recipe produces multiple outputs, you need semantics that ensure it runs **exactly once** per logical generation.

* GNU Make ≥ 4.3: grouped targets `&:` solves this cleanly.
* Fallback: a single stamp target + explicit dependencies (still must be atomic).

#### 8.3 Parallel control primitives are last resorts

* `.NOTPARALLEL`: use only when shared mutable state cannot be modeled.
* `.WAIT`: barrier (GNU Make ≥ 4.4). Prefer real edges first.

### Failure signatures

* “Only one of the generated files updates.” → multi-output generator modeled as separate rules without grouping/stamp.
* “Two recipes fight over the same file.” → multi-writer output or overlapping patterns.
* “`-j` flake disappears with `.NOTPARALLEL`.” → you silenced a real bug instead of fixing the DAG.

### Minimal repro

**Repro: broken multi-output generator (double invocation)**

```make
# gen produces a.h and a.c; naive rule causes multiple calls
a.h a.c: gen.py
    @python3 gen.py

all: a.h a.c
```

Under parallel, you can get duplicate runs or partial updates depending on timestamps.

### Fix pattern

**Fix A (GNU Make ≥ 4.3): grouped targets**

```make
a.h a.c &: gen.py
    @python3 gen.py
```

**Fix B (portable): stamp governs generation**

```make
GEN_STAMP := build/gen.stamp

$(GEN_STAMP): gen.py | build/
    @python3 gen.py && touch $@

a.h a.c: $(GEN_STAMP)
```

### Proof hook

* Run:

  ```sh
  make clean
  make -j4 --trace all
  ```

  Expected: generator runs once per logical regeneration; no duplicated recipe lines.

[Back to top](#top)

---

<a id="capstone"></a>
## 9) Capstone Sidebar

Use this to corroborate semantics with a real tree; don’t outsource understanding to it.

### Where to look

* CLI/forensics patterns: `make-capstone/Makefile`
* Variable probes / capability gates: `make-capstone/mk/contract.mk`
* Includes/layering: `make-capstone/mk/common.mk` + `mk/*.mk`
* Multi-output / eval demos: `make-capstone/mk/rules_eval.mk`
* Selftest harness: `make-capstone/tests/run.sh`

### Runbook

```sh
make -C make-capstone selftest
make -C make-capstone --trace all
make -C make-capstone -p | less
make -C make-capstone portability-audit
make -C make-capstone USE_EVAL=yes eval-demo
```

What each proves:

* `selftest`: convergence + serial/parallel equivalence + negative hidden-input detection
* `--trace`: causality is explicit and readable
* `-p`: the evaluated truth (variables, rules, resolved lists)
* `portability-audit`: feature gates computed, not guessed
* `eval-demo`: bounded rule generation remains inspectable

[Back to top](#top)

---

<a id="exercises"></a>
## 10) Exercises

Format is **Task → Expected → Forensics → Fix**. Do these first in a scratch directory, then repeat in capstone where applicable.

### Exercise 1 — `-q` exit codes are not optional knowledge

* Task:

  ```sh
  make clean && make all
  make -q all; echo $?
  rm -f <some-built-file>
  make -q all; echo $?
  ```
* Expected: `0` then `1`.
* Forensics: explain why `1` is not “error.”
* Fix: if your CI treats `1` as a crash, your CI script is wrong.

### Exercise 2 — Prove variable origin and flavor

* Task: create `show` target (Core 2 repro) and run env/CLI variants.
* Expected: `origin` flips as predicted; `flavor` matches `:=` vs `=`.
* Forensics: show the exact `origin=` output lines.
* Fix: eliminate `-e`, eliminate recursive self-references, or stamp exported inputs.

### Exercise 3 — Generated include restart loop (and how to stop it)

* Task: use Core 4 repro; then modify generator to write timestamps.
* Expected: Make never stabilizes / keeps remaking.
* Forensics: `make --trace` shows remake/restart behavior.
* Fix: make generated includes deterministic, or stop generating makefiles.

### Exercise 4 — Multi-output generator: prove single invocation

* Task: implement the broken multi-output rule; run `make -j4 --trace`.
* Expected: you see duplicated generator runs or inconsistent rebuild behavior.
* Forensics: count generator invocations in trace output.
* Fix: grouped targets (`&:`) or stamp-governed generation; rerun and show exactly one invocation.

### Exercise 5 — `.PHONY` misuse causes rebuild loops

* Task:

  ```make
  .PHONY: app
  ```

  then build twice.
* Expected: `app` rebuilds every time (bug).
* Forensics: `--trace` shows `.PHONY` forces out-of-date.
* Fix: `.PHONY` only for non-file orchestration targets.

[Back to top](#top)

---

<a id="closing"></a>
## 11) Closing Criteria

You pass Module 04 only if you can do all of the following without guessing:

* Given “why did it rebuild?”, you can produce **the `--trace` line** that proves the reason.
* Given “why did this variable change?”, you can show **origin + flavor + value** and point to the assigning file/line (via `-p` and include stack).
* Given “only fails under `-j`”, you can classify it as missing edge vs multi-writer vs non-atomic publish vs multi-output rule bug, and apply the correct fix.
* Given a feature (`&:`, `.WAIT`, `.ONESHELL`, `--output-sync`), you can state the **capability gate** and provide a fallback that preserves correctness.

[Back to top](#top)

---