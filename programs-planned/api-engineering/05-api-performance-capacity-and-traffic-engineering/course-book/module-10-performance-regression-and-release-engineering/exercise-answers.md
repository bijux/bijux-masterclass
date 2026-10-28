# Worked Answers — Module 10: Performance Regression and Release Engineering

Use these solutions to audit your reasoning for **Performance Regression and Release Engineering**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Order these gates: latency, correctness, environment match, outcome coverage.

Environment/workload comparability first, then correctness/security, then outcome coverage/error/rejection populations, then latency/throughput/resource thresholds. Later metrics cannot approve a candidate that fails earlier gates.

The chapter’s decisive distinction is this: Resource gates may use maximum absolute budgets, such as memory under 512 MiB, and relative service-demand budgets, such as no more than 5% CPU/request increase. Throughput improvements require correctness and a practical minimum.

**Evidence.** Compare repeated runs with the same workload hash and environment fingerprint, account for offered/started/completed/rejected/failed/missing outcomes, and report uncertainty and tail latency.

## 2. Why support `inconclusive`?

Evidence may be incomparable, too noisy, under-sampled, or straddle thresholds. Forcing pass/fail fabricates certainty. Inconclusive blocks the performance claim and requests better evidence.

In the cumulative capstone, the rule becomes concrete: Rule Required behavior Failure if omitted Decisive evidence --- --- --- --- Tiered proof Deterministic and environment-backed checks are separated. Noisy shared CI becomes false authority. Pipeline definition Early-gate precedence Identity/correctness/coverage precede speed. Fast wrong candidate passes. Release evaluator tests Thresholds versioned Absolute/relative/resource rules are fixed before candidate. Gate moves after result. Performance profile Inconclusive supported Noise or mismatch blocks claim without fabricated pass/fail. Uncertain result is forced to victory.

## 3. Design a p95 regression rule with absolute and relative bounds.

Example: reject when p95 increases by more than both 10 ms and 5%, provided runs are comparable and the run-level uncertainty does not make the result inconclusive. State whether both or either condition applies.

A useful way to reason about the boundary is: A database index may remain after application rollback; this can be safe but affects write cost. A cache-key format change may require dual read or natural expiry. Traffic-policy changes need profile/version awareness.

## 4. Which performance checks belong in ordinary shared CI?

Deterministic vectors, output equivalence, operation-count/size bounds, cache/permit invariants, SQL predicate checks, plan-fixture summaries, planted defects, and release evaluator logic. Exact wall-clock p95 generally needs a controlled runner.

The implementation consequence is: Rule Required behavior Failure if omitted Decisive evidence --- --- --- --- Tiered proof Deterministic and environment-backed checks are separated. Noisy shared CI becomes false authority. Pipeline definition Early-gate precedence Identity/correctness/coverage precede speed. Fast wrong candidate passes. Release evaluator tests Thresholds versioned Absolute/relative/resource rules are fixed before candidate. Gate moves after result. Performance profile Inconclusive supported Noise or mismatch blocks claim without fabricated pass/fail. Uncertain result is forced to victory.

## 5. When may a baseline be replaced?

After an accepted intentional release, environment/workload/data version change, corrected benchmark defect, or explicit objective change. Record lineage and reason; never replace it to hide a failed candidate.

The important nuance is: A database index may remain after application rollback; this can be safe but affects write cost. A cache-key format change may require dual read or natural expiry. Traffic-policy changes need profile/version awareness.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 6. A candidate p95 improves 15% but memory exceeds hard budget. Decision?

Reject under the multi-dimensional policy. A latency gain does not compensate for a hard resource/capacity violation unless the policy itself is separately changed and reviewed.

Under concurrency or failure, the distinction becomes: Resource gates may use maximum absolute budgets, such as memory under 512 MiB, and relative service-demand budgets, such as no more than 5% CPU/request increase. Throughput improvements require correctness and a practical minimum.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 7. A candidate is run on a newer CPU. Decision?

Direct code comparison is non-comparable. It may be evaluated as a planned environment scale change if that is the variable under decision and all other factors are controlled; otherwise mark inconclusive.

The design remains honest only if: Rule Required behavior Failure if omitted Decisive evidence --- --- --- --- Tiered proof Deterministic and environment-backed checks are separated. Noisy shared CI becomes false authority. Pipeline definition Early-gate precedence Identity/correctness/coverage precede speed. Fast wrong candidate passes. Release evaluator tests Thresholds versioned Absolute/relative/resource rules are fixed before candidate. Gate moves after result. Performance profile Inconclusive supported Noise or mismatch blocks claim without fabricated pass/fail. Uncertain result is forced to victory.

## 8. Why retain metrics for a rejected correctness candidate?

They may help diagnose mechanism effects, but they cannot support approval. Clearly label them as non-decision performance observations.

The consumer-facing consequence is: Resource gates may use maximum absolute budgets, such as memory under 512 MiB, and relative service-demand budgets, such as no more than 5% CPU/request increase. Throughput improvements require correctness and a practical minimum.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 9. What should a rollback plan include for a new index?

Whether application rollback can coexist with the index, write/storage cost while it remains, process for dropping it safely if needed, plan/SLI triggers, and whether migration tooling supports concurrent operations.

The operational consequence is: A database index may remain after application rollback; this can be safe but affects write cost. A cache-key format change may require dual read or natural expiry. Traffic-policy changes need profile/version awareness.

**Evidence.** Retain before/after EXPLAIN evidence, rows and buffers, write cost, pool pressure, and latency under the declared data distribution and workload.

## 10. How do planted defects improve trust?

They demonstrate that a proof fails when its protected invariant is violated. A test suite that remains green under the defect is not sensitive enough and must be repaired.

The strongest engineering interpretation is: Rule Required behavior Failure if omitted Decisive evidence --- --- --- --- Tiered proof Deterministic and environment-backed checks are separated. Noisy shared CI becomes false authority. Pipeline definition Early-gate precedence Identity/correctness/coverage precede speed. Fast wrong candidate passes. Release evaluator tests Thresholds versioned Absolute/relative/resource rules are fixed before candidate. Gate moves after result. Performance profile Inconclusive supported Noise or mismatch blocks claim without fabricated pass/fail. Uncertain result is forced to victory.

## 11. What should be excluded from the Course 6 handoff?

Secrets, private keys, raw tenant/principal identifiers, environment credentials, ephemeral traces, machine paths, and unneeded raw events. Include sanitized profiles, workloads, budgets, accepted model, migration, and manifests.

The defect-oriented view is: Resource gates may use maximum absolute budgets, such as memory under 512 MiB, and relative service-demand budgets, such as no more than 5% CPU/request increase. Throughput improvements require correctness and a practical minimum.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 12. Write a complete release decision sentence.

Example: Candidate `PERF-1.0.0` is accepted for API 1.2 under `WL-RUN-LIST` in matched Class C environment because correctness and coverage passed, p95 improved 18% across six alternating runs, shared reads fell 72%, write p95 rose 2% within budget, and modeled DB headroom increased from 14% to 31%; remeasure when run rows double or PostgreSQL/runtime version changes.

Across the Python and TypeScript tracks, the invariant is: A database index may remain after application rollback; this can be safe but affects write cost. A cache-key format change may require dual read or natural expiry. Traffic-policy changes need profile/version awareness.
