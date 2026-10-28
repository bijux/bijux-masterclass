# Checkpoint — Module 07: Distributed Tracing Across Asynchronous Work

## Required result

One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.

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

## Defend the design

1. Answer the central question: **How do we reconstruct one outcome across HTTP, database, worker, storage, and webhook boundaries without inventing false parentage?**
2. Demonstrate this capstone result: One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: untrusted incoming context is validated; synchronous work uses parentage and durable asynchronous work uses links plus attempt identity.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.—all focused checks pass, the **Distributed Tracing Across Asynchronous Work** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
