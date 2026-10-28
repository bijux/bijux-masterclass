# PERF-07 — Global Rate Limit Only

## Mutation

One tenant can consume the entire shared budget.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `fairness-vector`. The proof must fail before a latency or
throughput improvement can approve the candidate.
