# PERF-09 — Rewrite Baseline On Failure

## Mutation

A failed candidate silently becomes the new baseline.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `baseline-registry-proof`. The proof must fail before a latency or
throughput improvement can approve the candidate.
