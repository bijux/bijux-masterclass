# PERF-03 — Compare Different Environments

## Mutation

A candidate from another CPU/runtime profile is reported as an improvement.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `comparability-gate`. The proof must fail before a latency or
throughput improvement can approve the candidate.
