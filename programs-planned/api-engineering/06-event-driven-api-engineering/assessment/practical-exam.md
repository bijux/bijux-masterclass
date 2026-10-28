# Practical examination

The examiner provides one accepted event contract and one flawed candidate system. The flaw is selected from partition drift, acknowledgement before commit, incomplete inbox identity, unsafe replay, event-time misuse, overbroad producer authority, or unbounded retry.

The learner has four tasks:

1. reproduce the failure with a bounded fixture;
2. identify the smallest violated invariant and authoritative state;
3. repair one primary implementation track without changing the public event meaning;
4. run the comparative track or shared vectors and produce a release decision.

The submission includes the failing trace, the repaired trace, schema or policy diff, durable before/after state, exact proof command, and residual risk. A performance improvement, cleaner diagram, or broker configuration is irrelevant unless the correctness oracle passes.
