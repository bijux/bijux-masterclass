# PERF-10 — Optimize By Disabling Telemetry

## Mutation

The candidate appears faster by removing inherited reliability evidence.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `profile-freeze-proof`. The proof must fail before a latency or
throughput improvement can approve the candidate.
