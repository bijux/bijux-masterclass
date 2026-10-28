# PERF-06 — Cache Without Principal

## Mutation

Private representations share a cache key across principals.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `cache-key-vector`. The proof must fail before a latency or
throughput improvement can approve the candidate.
