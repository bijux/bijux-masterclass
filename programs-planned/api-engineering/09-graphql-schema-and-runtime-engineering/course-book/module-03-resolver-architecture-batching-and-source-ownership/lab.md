# Lab — Expose and remove N+1

> **Module 03:** Resolver Architecture, Batching, and Source Ownership

## Objective

Measure resolver amplification, replace it with request-scoped batching, and prove that batching does not leak values across tenants or requests.

## Why this lab matters

This lab turns the module’s governing question—**How can nested graph execution remain faithful to service ownership without producing N+1 calls?**—into a falsifiable experiment. Batching does not make an unbounded query safe. A query that requests one thousand parents can still create a one-thousand-key batch. Admission bounds list cardinality; the loader bounds batch size and may split work into controlled chunks. Both controls are required.

It advances the cumulative Analysis Runs Platform by requiring this result: **Replace N+1 nested calls with request-scoped batching**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make module-02-proof`. Reset service call logs. Use a dataset containing at least twenty runs, duplicate run references, and two tenants with overlapping local identifiers.

## Hypothesis

The clean implementation should satisfy this claim: **Property Required result --- --- growth source call count does not grow linearly with parent count duplicates one source key per unique request-scoped identity association values return to the correct keys despite source ordering tenancy no cross-tenant or cross-request cache reuse authorization denied keys do not enter an unauthorized source call cancellation no unresolved loader future or runaway dispatch bounds batch size never exceeds policy** When the lab introduces this fault—**Use a dataset containing at least twenty runs, duplicate run references, and two tenants with overlapping local identifiers**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

### 1. Establish the naïve resolver

In a scratch implementation, resolve `AnalysisRun.artifacts` by calling Artifact Service once per parent. Execute the operation with parent counts 2, 5, and 20. Record source calls and total keys.

Expected relation:

```text
artifact calls = parent occurrences
```

### 2. Install a request-scoped loader

Replace the resolver with `artifactsByRun.load((tenantId, runId))`. The batch function accepts unique keys and returns a mapping. Execute the same parent populations.

Expected relation:

```text
artifact batch calls <= dispatch intervals
keys in source call = unique authorized keys
```

### 3. Test duplicate collapse and result association

Request the same run through aliases and fragments. Confirm one key in the batch and correct values at every response path. Shuffle the source return order to prove the loader maps by key rather than by position.

### 4. Test request and tenant isolation

Finish the first request. Open a second request for another tenant using the same local run identifier. The second request must perform its own authorized source lookup and must not receive a cache hit from the first request.

### 5. Test cancellation and batch bounds

Cancel before dispatch and after dispatch begins. Confirm pending futures settle and no unbounded background batch remains. Submit more keys than the configured batch size and verify controlled chunking rather than one unbounded request.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Use a dataset containing at least twenty runs, duplicate run references, and two tenants with overlapping local identifiers**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Measure resolver amplification, replace it with request-scoped batching, and prove that batching does not leak values across tenants or requests**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

| Property | Required result |
|---|---|
| growth | source call count does not grow linearly with parent count |
| duplicates | one source key per unique request-scoped identity |
| association | values return to the correct keys despite source ordering |
| tenancy | no cross-tenant or cross-request cache reuse |
| authorization | denied keys do not enter an unauthorized source call |
| cancellation | no unresolved loader future or runaway dispatch |
| bounds | batch size never exceeds policy |

## Required evidence

Create `reports/module-03-batching.json` with parent count, field occurrences, unique keys, dispatch count, source calls, maximum batch size, tenant partition, cancellation outcome, and cache scope. Include both the naïve and repaired results.

## Interpretation and defense

1. Which state or effect is authoritative for **Resolver Architecture, Batching, and Source Ownership**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Use a dataset containing at least twenty runs, duplicate run references, and two tenants with overlapping local identifiers** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove the naïve resolver and generated report copies not required by the checkpoint. Clear all request caches and TypeScript build output. Re-run the module proof twice to demonstrate isolation.

## Completion gate

The repaired path has bounded calls, shuffled results remain correct, denied and cross-tenant keys never leak, cancellation settles cleanly, and the planted global-loader defect is rejected.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Resolver Architecture, Batching, and Source Ownership**. A green command without the negative case and causal explanation does not satisfy this gate.
