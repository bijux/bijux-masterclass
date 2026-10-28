# Lab — Module 07: Distributed Tracing Across Asynchronous Work

## Objective

Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits.


## Setup conditions

The previous baseline is: **The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we reconstruct one outcome across HTTP, database, worker, storage, and webhook boundaries without inventing false parentage?*

## Failure action and investigation

1. Submit and persist a run, then restart before worker claim.
2. Show that process-local context is lost.
3. Store validated bounded context with the job and start a linked worker trace.
4. Record queue delay and processing separately.
5. Fail the first webhook attempt and retain attempt evidence.
6. Drop all traces and prove reconciliation still decides correctness.

### Required planted defect

Remove or bypass the central control for **Distributed Tracing Across Asynchronous Work** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- The request ends after durable acceptance.
- Worker execution is linked, not falsely nested for its full lifetime.
- Queue delay and processing time are distinguishable.
- Both webhook attempts are visible when sampled.
- Durable correctness remains decidable with zero traces.

## Required evidence

- baseline transcript proving the previous checkpoint before **Distributed Tracing Across Asynchronous Work** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Parse and validate W3C trace context.
- public, durable, security, or operational observation showing: One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **trace context across asynchronous work**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Remove planted context-local dependency.
2. Clear trace fixtures and exporter buffers.
3. Run privacy/cardinality scan over retained trace JSON.
4. Retain topology diagram and sampling-limit note.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=07` succeeds on the primary track.
