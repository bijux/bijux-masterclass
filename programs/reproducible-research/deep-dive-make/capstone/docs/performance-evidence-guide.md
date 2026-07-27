# Performance Evidence Guide

Use this guide when a build-cost claim needs evidence that another learner or reviewer can
inspect without reconstructing a shell loop. The route measures local behavior. It does not
define a universal speed threshold.

## Start with the question

`make perf` answers:

> What do the governed clean, converged no-op, and converged dry-run routes cost in this
> named environment and revision, and did each route preserve convergence, trusted outputs,
> and the declared incremental rebuild scope?

It does not answer:

- whether the current revision regressed without a compatible earlier bundle
- whether a small delta matters operationally
- which recipe lies on the critical path
- whether timings from another machine are directly comparable

## Produce one evidence bundle

From `capstone/`, run:

```sh
gmake perf
```

Use `PERFORMANCE_SAMPLES` only when the experiment contract calls for another repetition
count:

```sh
gmake perf PERFORMANCE_SAMPLES=7
```

Name a stable execution environment when evidence may be compared later:

```sh
gmake perf PERFORMANCE_RUNNER=local-macos-arm64
```

The label is not decoration. It distinguishes environments that a platform string may not,
such as a laptop run and a CI runner with the same operating system. Keep one label for one
stable environment; do not rename a changed machine to make evidence compare.

The minimum is three. Five is the default because one timing is not a baseline and a very
large local sample count would imply precision this teaching route does not provide.

## Read the bundle in order

The bundle is written under:

```text
artifacts/performance/reproducible-research/deep-dive-make/current/
```

Read:

1. `route.txt` for the question and limits
2. `scenarios.tsv` for the exact state, job count, and route contract
3. `incremental-policy.tsv` for every declared input class and expected impact
4. `incremental-summary.tsv` for the observed change-impact matrix
5. `incremental-work.json` for per-case traces, missing work, and unexpected work
6. `evidence.json` for provenance, the bound incremental matrix, every timing sample, and
   trusted-output inventories
7. `summary.tsv` for min, median, max, spread, and convergence
8. `logs/` for command output and exit status from each timing sample
9. `manifest.json` for the bundle member inventory

This order is deliberate. A median is interpretable only after you know what ran, where it
ran, and whether it did the same work.

## Read execution context as evidence

The `context` object in `evidence.json` records:

| Field | Why it belongs in the claim |
| --- | --- |
| repository revision | identifies the source and Make graph measured |
| repository status and status digest | exposes uncommitted source state |
| resolved GNU Make command and version | identifies the evaluator and scheduler |
| resolved compiler command and version | identifies the main clean-build recipe tool |
| Python version | identifies the evidence collector runtime |
| platform | provides the operating-system and machine boundary |
| runner label | names the stable execution environment chosen by the operator |

Collection records a dirty worktree rather than hiding it. Comparison rejects dirty or
unavailable repository provenance because two timings cannot establish a revision-to-revision
change when either side includes unidentified source edits.

Different revisions are expected in a useful comparison. The report names both revisions;
it does not require them to match. The compiler, GNU Make, Python, platform, runner label,
scenario policy, and sample count do have to match. If one changes, recollect or describe a
cross-environment observation without calling it a controlled performance comparison.

## Understand the scenarios

| Scenario | State established before each sample | Route | Teaching purpose |
| --- | --- | --- | --- |
| `clean-build` | documented `clean` route | parallel `all` | observe full production cost |
| `converged-noop` | `all` succeeds and `make -q all` passes | serial `all` | observe an up-to-date invocation |
| `converged-dry-run` | `all` succeeds and `make -q all` passes | serial `-n all` | localize cost before ordinary recipe execution |

Dry-run is not pure parse timing. It includes evaluation and graph decisions, and recursive
Make recipes have special dry-run behavior.

## Why the inventories belong beside timing

After every scenario, the collector requires `make -q all` to pass and inventories:

- `all`
- `app`
- `build/bin/dyn1`
- `build/bin/dyn2`
- `build/include/dynamic.h`

A candidate that omits work may be faster. It is not comparable if those trusted outputs
change unexpectedly or the route stops converging.

Final bytes are not enough. The incremental route executes a change-impact matrix:

| Input advanced | Must rebuild | Must remain unchanged | Edge class under review |
| --- | --- | --- | --- |
| `src/util.c` | `build/util.o`, `app`, `all` | other objects and dynamic pipeline | direct source dependency |
| `include/util.h` | `build/main.o`, `build/util.o`, `app`, `all` | sub object and dynamic pipeline | depfile-discovered shared header |
| `include/sub.h` | `build/main.o`, `build/sub/sub.o`, `app`, `all` | util object and dynamic pipeline | depfile-discovered shared header |
| `scripts/gen_dynamic_h.py` | generated header, both dynamic binaries, `all` | application and ordinary objects | generated producer fan-out |
| `src/dynamic/dyn1.c` | `build/bin/dyn1`, `all` | application, ordinary objects, sibling binary, generated header | independent dynamic source |

Every row classifies the same governed output universe. That completeness rule matters. If
an output appeared in neither column, the runner would not observe it and a false pass
would be possible.

For each row, the runner:

1. converges `all`
2. snapshots every governed output timestamp
3. advances only the declared input beyond all outputs
4. executes `make --trace all`
5. restores the input timestamp even when the case fails
6. classifies observed, missing, and unexpected rebuilds

The next case starts from a converged build, not from the previous case's artificial input
timestamp. Passing cases remain in the report when a later case fails, so reviewers can see
the exact stopping evidence without losing earlier observations.

Missing work exposes stale-output risk. Unexpected work exposes an overbroad graph. The two
failures lead to different repairs: restore a required edge versus narrow an unnecessary
one.

The collector copies the passing semantic fields into `evidence.json`. This binding matters:
the comparator does not look for a conveniently named sibling file and hope it belongs to the
timings. It compares the policy digest, complete input set, and each case's expected and
observed rebuild sets carried by both evidence documents.

Run that proof alone with:

```sh
gmake performance-incremental
```

## Compare two compatible bundles

Preserve the earlier bundle outside `current/`, because the next `make perf` replaces that
directory. Then run:

```sh
gmake performance-compare \
  PERFORMANCE_BASELINE=/path/to/baseline/evidence.json
```

The comparison rejects:

- different scenario-policy digests
- different sample counts
- different GNU Make, compiler, Python, platform, or runner identities
- dirty or unavailable repository provenance
- different scenario sets, states, routes, or job counts
- failed evidence
- failed convergence
- changed trusted-output inventories
- different incremental policy or input-case set
- different expected or observed work in any case, including a non-first case
- missing or unexpected incremental rebuilds

It deliberately permits different clean revision identifiers and records both in
`execution_context`. Only after all compatibility and semantic checks pass does it report
median deltas. The report does not label a negative delta a “win.” Compare the delta with
both observed spread and a stated operational objective.

## Review the gate itself

Run:

```sh
gmake performance-selftest
```

The tests prove that:

- resolved tool and repository identity are captured
- clean, dirty, and unavailable repository states remain distinguishable
- every policy case classifies one complete governed output set
- later failing cases remain attributable and restore their inputs
- missing cases and non-first-case rebuild drift are rejected
- a complete governed capture passes
- fewer than three samples are rejected
- a failed command produces failed evidence
- compatible bundles can be compared
- context, policy, sample-count, result, artifact, and requested-work drift are rejected

This matters because a gate that has only seen passing input is not yet trustworthy.

## Make an honest decision

Use one of these outcomes:

| Evidence | Defensible decision |
| --- | --- |
| one bundle, no prior compatible evidence | baseline established; regression unproven |
| compatible bundles, delta inside observed spread | no material change established |
| compatible bundles, objective exceeded, semantics match | investigate or accept the measured change |
| comparison rejected for toolchain or runner drift | evidence describes different environments |
| comparison rejected for dirty provenance | commit or restore the intended source state, then recollect |
| comparison rejected for requested-work drift | timing claim blocked until the graph change is explained |
| comparison rejected for artifact drift | performance claim blocked by semantic change |
| comparison rejected for contract drift | recollect under one experiment contract |

Write down what remains unknown. A local experiment can support a local engineering
decision without pretending to be a portable benchmark.

## Companion routes

- `make trace-report` for bounded clean-plan causality and attribution evidence
- `make selftest-report` for convergence and schedule-equivalence proof
- `make incident-audit` for one executed failure specimen
- `make profile-audit` for tool, platform, and variable-origin boundaries
