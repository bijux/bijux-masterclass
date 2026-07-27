# Performance Evidence Guide

Use this guide when a build-cost claim needs evidence that another learner or reviewer can
inspect without reconstructing a shell loop. The route measures local behavior. It does not
define a universal speed threshold.

## Start with the question

`make perf` answers:

> What do the governed clean, converged no-op, and converged dry-run routes cost in this
> environment, and did each route preserve the capstone's trusted outputs and convergence?

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
3. `summary.tsv` for min, median, max, spread, and convergence
4. `incremental-policy.tsv` for the declared input and expected rebuild scope
5. `incremental-work.json` for missing and unexpected rebuilds
6. `evidence.json` for context, every sample, and trusted-output inventories
7. `logs/` for command output and exit status from each sample
8. `manifest.json` for the bundle member inventory

The summary is an entry surface, not a substitute for raw samples.

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

Final bytes are not enough. The incremental route advances `src/util.c` without changing
its contents, runs the real build, then restores the source timestamp. The policy requires
`build/util.o`, `app`, and `all` to rebuild while unrelated objects, dynamic binaries, and
the generated header remain untouched. Missing work exposes stale-output risk; unexpected
work exposes an overbroad graph.

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
- different scenario sets, states, routes, or job counts
- failed evidence
- failed convergence
- changed trusted-output inventories

Only after those checks pass does it report median deltas. The report deliberately does not
label a negative delta a “win.” Compare the delta with both observed spread and a stated
operational objective.

## Review the gate itself

Run:

```sh
gmake performance-selftest
```

The tests prove that:

- a complete governed capture passes
- fewer than three samples are rejected
- a failed command produces failed evidence
- compatible bundles can be compared
- policy, sample-count, result, and artifact drift are rejected

This matters because a gate that has only seen passing input is not yet trustworthy.

## Make an honest decision

Use one of these outcomes:

| Evidence | Defensible decision |
| --- | --- |
| one bundle, no prior compatible evidence | baseline established; regression unproven |
| compatible bundles, delta inside observed spread | no material change established |
| compatible bundles, objective exceeded, semantics match | investigate or accept the measured change |
| comparison rejected for artifact drift | performance claim blocked by semantic change |
| comparison rejected for contract drift | recollect under one experiment contract |

Write down what remains unknown. A local experiment can support a local engineering
decision without pretending to be a portable benchmark.

## Companion routes

- `make trace-count` for one rough trace-volume signal
- `make selftest-report` for convergence and schedule-equivalence proof
- `make incident-audit` for one executed failure specimen
- `make profile-audit` for tool, platform, and variable-origin boundaries
