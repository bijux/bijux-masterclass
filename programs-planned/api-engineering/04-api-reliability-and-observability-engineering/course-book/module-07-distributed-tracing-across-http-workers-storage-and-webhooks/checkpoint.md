# Checkpoint — Module 07: Distributed Tracing Across Asynchronous Work

## Required result

Implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes.

## Demonstrate

- Parse and validate W3C trace context.
- Create bounded span names and attributes.
- Represent queue and worker attempts accurately.
- Link asynchronous work to durable causation.
- Understand sampling and missing-span limits.

## Commands

```bash
make module-proof MODULE=07
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Distributed Tracing Across Asynchronous Work** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Distributed Tracing Across Asynchronous Work**
- focused result for: Parse and validate W3C trace context.
- public, durable, security, or operational observation showing: One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **trace context across asynchronous work**
- a limitation statement naming every live dependency required to support the strongest **Distributed Tracing Across Asynchronous Work** claim but not exercised

## Defend the design

1. Answer the central question: **How do we reconstruct one outcome across HTTP, database, worker, storage, and webhook boundaries without inventing false parentage?**
2. Demonstrate this capstone result: One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.
3. Show the **Distributed Tracing Across Asynchronous Work** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: untrusted incoming context is validated; synchronous work uses parentage and durable asynchronous work uses links plus attempt identity.
5. State which environment-backed **Distributed Tracing Across Asynchronous Work** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.—all focused checks pass, the **Distributed Tracing Across Asynchronous Work** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
