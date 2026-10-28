# PERF-01 — Drop Missing Outcomes

## Mutation

A timed-out request is removed from the terminal population.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `coverage-gate`. The proof must fail before a latency or
throughput improvement can approve the candidate.
