# Lab — Module 07: Distributed Tracing Across Asynchronous Work

> **Module 07:** Distributed Tracing Across Asynchronous Work

## Objective

Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits.

## Why this lab matters

This lab turns the module’s governing question—**How does trace context cross HTTP, queues, workers, storage, retries, and webhooks without inventing false parentage?**—into a falsifiable experiment. Apply Span relationship, Propagation carrier, Queue timing to this module’s capstone increment: Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits. State one misleading green signal and the durable observation that would overrule it.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we reconstruct one outcome across HTTP, database, worker, storage, and webhook boundaries without inventing false parentage?*

## Hypothesis

The clean implementation should satisfy this claim: **The request ends after durable acceptance; Worker execution is linked, not falsely nested for its full lifetime; Queue delay and processing time are distinguishable; Both webhook attempts are visible when sampled; Durable correctness remains decidable with zero traces.** When the lab introduces this fault—**Remove or bypass the central control for Distributed Tracing Across Asynchronous Work in a temporary branch**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Submit and persist a run, then restart before worker claim.
2. Show that process-local context is lost.
3. Store validated bounded context with the job and start a linked worker trace.
4. Record queue delay and processing separately.
5. Fail the first webhook attempt and retain attempt evidence.
6. Drop all traces and prove reconciliation still decides correctness.

### Required planted defect

Remove or bypass the central control for **Distributed Tracing Across Asynchronous Work** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control for Distributed Tracing Across Asynchronous Work in a temporary branch**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- The request ends after durable acceptance.
- Worker execution is linked, not falsely nested for its full lifetime.
- Queue delay and processing time are distinguishable.
- Both webhook attempts are visible when sampled.
- Durable correctness remains decidable with zero traces.

## Required evidence

- baseline transcript proving the previous checkpoint before **Distributed Tracing Across Asynchronous Work** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Distributed Tracing Across Asynchronous Work**
- focused result for: Parse and validate W3C trace context.
- public, durable, security, or operational observation showing: One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **trace context across asynchronous work**
- a limitation statement naming every live dependency required to support the strongest **Distributed Tracing Across Asynchronous Work** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Distributed Tracing Across Asynchronous Work**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control for Distributed Tracing Across Asynchronous Work in a temporary branch** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Remove planted context-local dependency.
2. Clear trace fixtures and exporter buffers.
3. Run privacy/cardinality scan over retained trace JSON.
4. Retain topology diagram and sampling-limit note.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=07` succeeds on the primary track.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Distributed Tracing Across Asynchronous Work**. A green command without the negative case and causal explanation does not satisfy this gate.
