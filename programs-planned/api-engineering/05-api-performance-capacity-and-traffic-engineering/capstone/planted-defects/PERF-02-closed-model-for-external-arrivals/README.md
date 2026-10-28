# PERF-02 — Closed Model For External Arrivals

## Mutation

The generator waits for responses and therefore lowers offered load during saturation.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `workload-model-review`. The proof must fail before a latency or
throughput improvement can approve the candidate.
