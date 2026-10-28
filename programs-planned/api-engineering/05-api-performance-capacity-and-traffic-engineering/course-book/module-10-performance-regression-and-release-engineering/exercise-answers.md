# Reference Answers — Module 10: Module 10 exercise answers — Performance Regression and Release Engineering

Read after attempting all twelve Performance Regression and Release Engineering exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Order these gates: latency, correctness, environment match, outcome coverage.

Environment/workload comparability first, then correctness/security, then outcome coverage/error/rejection populations, then latency/throughput/resource thresholds. Later metrics cannot approve a candidate that fails earlier gates.

## 2. Why support `inconclusive`?

Evidence may be incomparable, too noisy, under-sampled, or straddle thresholds. Forcing pass/fail fabricates certainty. Inconclusive blocks the performance claim and requests better evidence.

## 3. Design a p95 regression rule with absolute and relative bounds.

Example: reject when p95 increases by more than both 10 ms and 5%, provided runs are comparable and the run-level uncertainty does not make the result inconclusive. State whether both or either condition applies.

## 4. Which performance checks belong in ordinary shared CI?

Deterministic vectors, output equivalence, operation-count/size bounds, cache/permit invariants, SQL predicate checks, plan-fixture summaries, planted defects, and release evaluator logic. Exact wall-clock p95 generally needs a controlled runner.

## 5. When may a baseline be replaced?

After an accepted intentional release, environment/workload/data version change, corrected benchmark defect, or explicit objective change. Record lineage and reason; never replace it to hide a failed candidate.

## 6. A candidate p95 improves 15% but memory exceeds hard budget. Decision?

Reject under the multi-dimensional policy. A latency gain does not compensate for a hard resource/capacity violation unless the policy itself is separately changed and reviewed.

## 7. A candidate is run on a newer CPU. Decision?

Direct code comparison is non-comparable. It may be evaluated as a planned environment scale change if that is the variable under decision and all other factors are controlled; otherwise mark inconclusive.

## 8. Why retain metrics for a rejected correctness candidate?

They may help diagnose mechanism effects, but they cannot support approval. Clearly label them as non-decision performance observations.

## 9. What should a rollback plan include for a new index?

Whether application rollback can coexist with the index, write/storage cost while it remains, process for dropping it safely if needed, plan/SLI triggers, and whether migration tooling supports concurrent operations.

## 10. How do planted defects improve trust?

They demonstrate that a proof fails when its protected invariant is violated. A test suite that remains green under the defect is not sensitive enough and must be repaired.

## 11. What should be excluded from the Course 6 handoff?

Secrets, private keys, raw tenant/principal identifiers, environment credentials, ephemeral traces, machine paths, and unneeded raw events. Include sanitized profiles, workloads, budgets, accepted model, migration, and manifests.

## 12. Write a complete release decision sentence.

Example: Candidate `PERF-1.0.0` is accepted for API 1.2 under `WL-RUN-LIST` in matched Class C environment because correctness and coverage passed, p95 improved 18% across six alternating runs, shared reads fell 72%, write p95 rose 2% within budget, and modeled DB headroom increased from 14% to 31%; remeasure when run rows double or PostgreSQL/runtime version changes.
