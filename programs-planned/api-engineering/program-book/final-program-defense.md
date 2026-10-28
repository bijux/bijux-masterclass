# Final Program Defense

The final defense is not a repository tour. It is an end-to-end explanation of one platform outcome across all six responsibilities.

## Required scenario

Use one analysis run from authenticated submission through artifact publication and one asynchronous consumer effect. Demonstrate or explain:

1. the legal HTTP request and response contract;
2. schema validation and public error semantics;
3. the application use case and domain transition;
4. the transaction, idempotency record, version check, job, artifact, and outbox facts;
5. authentication, authorization, tenant isolation, and hostile-input boundaries;
6. deadlines, retry ownership, lifecycle, telemetry, SLI, SLO, alert, and runbook;
7. workload identity, query/runtime evidence, admission, traffic policy, and capacity limit;
8. event ownership, canonical envelope, publication, delivery attempt, inbox/effect transaction, acknowledgement, replay, and release compatibility.

## Questions the learner must answer

- Which artifact is authoritative at each stage?
- Which failures are retried, rejected, concealed, degraded, reconciled, or dead-lettered?
- Where can duplicate work occur, and why do duplicate effects not occur?
- Which identifiers connect HTTP, durable state, telemetry, workload evidence, and events without making them interchangeable?
- Which public versions and profiles are in force?
- Which proof is deterministic, which requires live dependencies, and which claim remains unexecuted in the current environment?
- What is the first bottleneck under the declared workload?
- Which interaction remains synchronous, and why?
- Which proposed microservice split would you reject at this point?

## Passing standard

The defense passes when the learner can move from user-visible promise to authoritative state and back without hand-waving. Tool names may support the explanation, but they cannot replace the engineering model. Every claim must have an owner, a failure, an oracle, and an honest evidence boundary.
