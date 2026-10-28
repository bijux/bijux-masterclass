# Module 02 lab — Expose coordinated omission and run-order bias

## Objective

Use the local slow-path injection to compare closed and open schedules, then run alternating baseline/candidate series with a predeclared decision rule.

## Setup conditions

- Module 1 workload identities pass
- local laboratory server is available
- the slow-path delay is deterministic and disabled by default
- thresholds are written before candidate runs

## Failure action and investigation


1. Configure a two-second server pause at a known point.
2. Run a closed workload with ten users.
3. Run an open workload at 100 arrivals/s over the same interval.
4. Compare offered, started, completed, delayed, and dropped populations.
5. Run `B-A-B-A-B-A` baseline/candidate order with the pause disabled.
6. Recompute nearest-rank summaries from retained events.
7. Evaluate the predeclared release rule.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons. A passing command without this causal explanation is insufficient.

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
