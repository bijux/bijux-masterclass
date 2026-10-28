# PERF-05 — Unbounded Admission Wait

## Mutation

Every caller waits indefinitely and memory becomes the queue.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `admission-bound-proof`. The proof must fail before a latency or
throughput improvement can approve the candidate.
