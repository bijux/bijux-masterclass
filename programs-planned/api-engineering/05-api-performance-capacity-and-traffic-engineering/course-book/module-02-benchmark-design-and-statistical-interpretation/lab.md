# Lab — Module 02 lab — Expose coordinated omission and run-order bias

> **Module 02:** Benchmark Design and Statistical Interpretation

## Objective

Use the local slow-path injection to compare closed and open schedules, then run alternating baseline/candidate series with a predeclared decision rule.

## Why this lab matters

This lab turns the module’s governing question—**How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning?**—into a falsifiable experiment. For a release comparison, compute each run’s summary, then compare run summaries. A deterministic bootstrap over independent run-level p95 or throughput values can provide an interval for the difference, but it does not rescue a biased workload or correlated runs.

It advances the cumulative Analysis Runs Platform by requiring this result: **Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- Module 1 workload identities pass
- local laboratory server is available
- the slow-path delay is deterministic and disabled by default
- thresholds are written before candidate runs

## Hypothesis

The clean implementation should satisfy this claim: **the open schedule exposes arrivals during the pause; scheduled-to-start delay is retained; closed and open results are not compared as equivalent workloads; summary replay matches packaged calculations; run order and warmup windows are recorded; the decision can be insufficient evidence.** When the lab introduces this fault—**Compare offered, started, completed, delayed, and dropped populations**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Configure a two-second server pause at a known point.
2. Run a closed workload with ten users.
3. Run an open workload at 100 arrivals/s over the same interval.
4. Compare offered, started, completed, delayed, and dropped populations.
5. Run `B-A-B-A-B-A` baseline/candidate order with the pause disabled.
6. Recompute nearest-rank summaries from retained events.
7. Evaluate the predeclared release rule.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Compare offered, started, completed, delayed, and dropped populations**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Use the local slow-path injection to compare closed and open schedules, then run alternating baseline/candidate series with a predeclared decision rule**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- the open schedule exposes arrivals during the pause
- scheduled-to-start delay is retained
- closed and open results are not compared as equivalent workloads
- summary replay matches packaged calculations
- run order and warmup windows are recorded
- the decision can be `insufficient evidence`

## Required evidence

Create:

```text
work/module-02/
├── thresholds.yaml
├── closed-events.jsonl
├── open-events.jsonl
├── closed-summary.json
├── open-summary.json
├── run-series.json
└── decision.md
```

Include a diagram or table showing how many arrivals were scheduled during the pause and how each model represented them. State client schedule coverage.

## Interpretation and defense

1. Which state or effect is authoritative for **Benchmark Design and Statistical Interpretation**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Compare offered, started, completed, delayed, and dropped populations** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Disable the slow-path injection, stop local clients and servers, and verify no process remains bound to the laboratory port.

## Completion gate

- [ ] open and closed schedule semantics are demonstrated
- [ ] coordinated omission is visible in evidence
- [ ] warmup and measurement windows are explicit
- [ ] quantile algorithm and sample count are recorded
- [ ] independent run series is retained
- [ ] threshold was not changed after observing the candidate

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Benchmark Design and Statistical Interpretation**. A green command without the negative case and causal explanation does not satisfy this gate.
