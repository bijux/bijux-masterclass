# Course 9 Final Review — Rust Performance and Production Engineering

Begin every part from a blank page. You may use your code and the records you created, but do not follow the chapters line by line. The purpose is to expose whether the model can be reconstructed and transferred.

## Part 1 — Reconstruct the ten questions

For each question, supply a smallest working example, a causal negative example, the earliest decisive phase or event, a requirement-preserving repair, and one limit on the evidence you would use.

81. **Performance Contracts, Workloads, and Benchmark Design** — What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?
82. **CPU Profiling, Cost Models, and Hot-Path Optimization** — Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?
83. **Allocation, Memory Footprint, and Ownership Cost** — Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?
84. **Data Movement, Buffering, and Zero-Copy Boundaries** — Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?
85. **Runtime Efficiency: Contention, Queueing, Batching, and Async Load** — When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency?
86. **Observability: Structured Tracing, Metrics, and Diagnostic Context** — What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?
87. **Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation** — How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?
88. **Security and Supply-Chain Engineering** — Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?
89. **Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases** — How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?
90. **Production Readiness, Capacity Planning, Rollouts, and Incident Learning** — What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?

API names without the governing relationship do not answer this part.

## Part 2 — Independent construction

Build this product without copying a course domain:

> Take a bounded service and produce a complete production dossier: benchmark protocol, profile, memory and byte accounting, load curve, observability map, reliability policy, threat model, release manifest, and go/no-go decision.

Before implementation, write:

```text
product promise and non-goals
owners and authorities
valid and invalid states
success transition
failure, cleanup, and retry state
order and capacity
external assumptions
public API
verification plan
three rejected designs
```

After implementation, preserve six traces: ordinary success, malformed input, rejected state, partial work before failure, cleanup, and one compatibility, platform, scheduler, workload, or peer edge relevant to this course.

## Part 3 — Capstone change

Apply this change to MetricRail:

> Add one high-cardinality MetricRail query while preserving bounded memory, deterministic output, observability cardinality, overload behavior, and artifact traceability.

Do not introduce a second source of truth for validation, state, ordering, storage, protocol, scheduling, generation, measurement, or compatibility. Revise the authority map first when the change does not fit the current architecture.

Review the change through:

1. public behavior;
2. owner of the new invariant;
3. state after each failure point;
4. ownership and cleanup;
5. ordering and resource bounds;
6. compatibility or format consequences;
7. independent tests and their limits;
8. the simpler design you rejected.

## Part 4 — Cross-course preservation

Select one guarantee from Course 8 — Rust Async and Networked Services and prove that the new construction does not regress it.

Trace one requirement from input to internal state, effect, output, and test. If Course 9 introduces a stronger mechanism, explain why the earlier simpler design is no longer sufficient rather than assuming that greater abstraction is automatically better.

## Part 5 — Diagnosis sprint

Choose three unfamiliar cases from the course: one valid, one rejected by an early decisive phase, and one that compiles or runs while violating the product contract. Freeze the prediction, use a **production decision record**, observe the result, and explain every mismatch between prediction and evidence.

## Part 6 — Oral defense

- **Module 81 — Performance Contracts, Workloads, and Benchmark Design:** answer “What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 82 — CPU Profiling, Cost Models, and Hot-Path Optimization:** answer “Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 83 — Allocation, Memory Footprint, and Ownership Cost:** answer “Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 84 — Data Movement, Buffering, and Zero-Copy Boundaries:** answer “Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 85 — Runtime Efficiency: Contention, Queueing, Batching, and Async Load:** answer “When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 86 — Observability: Structured Tracing, Metrics, and Diagnostic Context:** answer “What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 87 — Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation:** answer “How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 88 — Security and Supply-Chain Engineering:** answer “Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 89 — Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases:** answer “How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 90 — Production Readiness, Capacity Planning, Rollouts, and Incident Learning:** answer “What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.

End with a fifteen-minute defense of MetricRail: product and non-goals, ownership and authority, main invariant, failure model, ordering and bounds, one difficult proof boundary, one rejected shortcut, evidence limits, and the handoff to the next course.

## Completion standard

Course 9 — Rust Performance and Production Engineering is complete when another competent Rust reader can reproduce the product behavior and causal explanation from your public contract, tests, and reasoning records. You must be able to say which claims are guaranteed by Rust, supplied by a library, chosen by the product, conditioned on a target or peer, or merely observed for one artifact and workload.

## Seven-day retention check

Without opening the course, redraw the ten-module chain and the core **production decision record**. Rebuild one small example in a new domain. Revisit only the relationships you cannot recover, then repeat the reconstruction rather than rereading the answer passively.
