# Lab 03 — Expose and remove N+1

## Purpose

Measure resolver amplification, replace it with request-scoped batching, and prove that batching does not leak values across tenants or requests.

## Prerequisites

Run `make module-02-proof`. Reset service call logs. Use a dataset containing at least twenty runs, duplicate run references, and two tenants with overlapping local identifiers.

## Procedure

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

## Correctness oracle

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

## Interpretation questions

- Why does one large batch still require cardinality admission?
- Which errors can be cached safely for one request?
- When should two fields use different loaders even if they call the same service?
- How does the loader preserve path-specific errors for individual keys?

## Cleanup

Remove the naïve resolver and generated report copies not required by the checkpoint. Clear all request caches and TypeScript build output. Re-run the module proof twice to demonstrate isolation.

## Completion gate

The repaired path has bounded calls, shuffled results remain correct, denied and cross-tenant keys never leak, cancellation settles cleanly, and the planted global-loader defect is rejected.
