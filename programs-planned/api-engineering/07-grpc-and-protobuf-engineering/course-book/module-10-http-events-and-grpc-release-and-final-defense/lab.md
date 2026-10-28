# Lab — Release and roll back the internal Analysis RPC control plane

> **Module 10:** HTTP, Events, and gRPC in One Architecture: Release and Final Defense

## Objective

Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system.

## Why this lab matters

This lab turns the module’s governing question—**How do we introduce an internal RPC control plane without breaking the public HTTP contract, durable event history, database authority, security profile, or rollback path?**—into a falsifiable experiment. Analysis RPC API 1.0 uses package bijux.analysis.v1. Service release 1.0 may expose the methods while the HTTP gateway still uses the local path. A later service release enables canary routing without changing the RPC contract. Schema version, service release, public API version, event API version, and database migration revision remain distinct.

It advances the cumulative Analysis Runs Platform by requiring this result: **Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Start from the Course 6-compatible local application path. Enable the Python live gRPC control plane, shared durable fixture, public HTTP adapter, event relay simulator, and deterministic routing controls.

## Hypothesis

The clean implementation should satisfy this claim: **The public HTTP and Event APIs remain semantically unchanged; durable state is authoritative; retries and rollback do not duplicate effects; stale attempts fail; streams remain bounded; all release gates report their evidence boundary; and the dossier rejects unjustified decomposition.** When the lab introduces this fault—**Inject post-commit response loss, stale worker completion, slow WatchRun consumer, and server drain**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Capture baseline HTTP, durable-state, event, security, reliability, and performance evidence.
2. Shadow eligible read calls through gRPC and compare semantic results.
3. Canary bounded CreateRun traffic using the same persistent request identity and no unsafe fallback.
4. Inject post-commit response loss, stale worker completion, slow WatchRun consumer, and server drain.
5. Cut over the eligible population, then roll back to the local path while preserving expanded migrations.
6. Run schema/generation, public HTTP, event, security, reliability, performance, and rollback gates and produce the Course 8 dossier.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject post-commit response loss, stale worker completion, slow WatchRun consumer, and server drain**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The public HTTP and Event APIs remain semantically unchanged; durable state is authoritative; retries and rollback do not duplicate effects; stale attempts fail; streams remain bounded; all release gates report their evidence boundary; and the dossier rejects unjustified decomposition.

## Required evidence

- `capstone/final-defense/trace.json`
- `capstone/releases/rpc-1.0/release-report.json`
- `capstone/handoff/service-boundary-dossier.yaml`

## Interpretation and defense

1. Which state or effect is authoritative for **HTTP, Events, and gRPC in One Architecture: Release and Final Defense**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject post-commit response loss, stale worker completion, slow WatchRun consumer, and server drain** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Return routing to the documented baseline, stop servers and relays, clear temporary canary state, preserve only deterministic release evidence, and verify manifests.

## Completion gate

Analysis RPC 1.0 is complete only when it can be introduced and removed without changing the public promise, durable event truth, authoritative state, security, or recovery semantics.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **HTTP, Events, and gRPC in One Architecture: Release and Final Defense**. A green command without the negative case and causal explanation does not satisfy this gate.
