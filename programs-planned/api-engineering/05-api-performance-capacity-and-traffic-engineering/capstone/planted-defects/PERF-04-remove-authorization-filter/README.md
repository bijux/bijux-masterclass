# PERF-04 — Remove Authorization Filter

## Mutation

A query is faster because tenant ownership is no longer enforced.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `correctness-gate`. The proof must fail before a latency or
throughput improvement can approve the candidate.
