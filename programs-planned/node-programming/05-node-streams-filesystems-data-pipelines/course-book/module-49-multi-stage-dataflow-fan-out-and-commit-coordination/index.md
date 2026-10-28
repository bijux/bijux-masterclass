# Module 49 — Multi-Stage Dataflow, Fan-Out, and Commit Coordination

**Progress: 49/100**

## The governing question

> How do you coordinate branches, side outputs, metadata, and multiple candidate files when a linear pipeline is no longer enough?

## Why this module comes now

Modules 41–48 established correct linear flows. Products often need a primary output, digest metadata, rejects file, metrics, or audit log. Branching introduces a new rule: the fastest sink cannot outrun the slowest sink when every branch must receive every item, and one failed branch can invalidate the complete candidate set.

Modules 41–48 built reliable linear flows. Real exports often need a required data file, a rejects file, a manifest, and advisory metrics. Branching creates multiple pressure domains and multiple visibility points. The architecture must classify each branch before choosing whether failure cancels the whole operation or is merely recorded.

This module reuses Course 4’s terminal accounting: every accepted record and every required output branch must reach one explicit terminal state. Completion order is not presentation order, and a sequence of renames is not automatically one transaction.

## Observable outcomes

By the end of this module, you can:

- distinguish observation taps, lossy side channels, and required fan-out branches

- coordinate backpressure across multiple required destinations

- define all-or-nothing, best-effort, and independently committed side-output policies

- stage and publish related outputs without claiming impossible filesystem atomicity

- produce deterministic reports from schedule-independent terminal evidence

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| branch class | Is the branch authoritative, required derivative, advisory, or debugging-only? |
| delivery rule | Must every item reach every branch, or can observation be lossy? |
| pressure join | Which branch determines when the producer may continue? |
| failure propagation | Does one branch failure cancel siblings and upstream? |
| publication unit | Is one path committed, several files staged, or an immutable bundle published by a pointer? |
| conservation | Which equations prove every record and byte reached exactly one permitted outcome? |

## Not every side effect is a branch

A counter or hash updated synchronously inside a Transform observes chunks without creating another asynchronous destination. A metrics event may be best effort and intentionally lossy. A rejects file is often a required output. These responsibilities need different failure policies. Treating all of them as generic listeners makes it impossible to tell whether a listener failure invalidates the data product.

Classify each side output as authoritative, required derivative, advisory observation, or debugging evidence. Only then choose whether its failure stops the pipeline.

## Required fan-out follows the slowest branch

If every chunk must reach two Writable destinations, the source may continue only when both branches have accepted capacity. A simple source.pipe(a); source.pipe(b) applies stream mechanics but makes coordinated completion and error policy harder to centralize. A custom fan-out Writable or async loop can await each branch’s pressure and destroy all branches when one fails.

The total memory model includes each branch queue. Duplicating a chunk reference does not duplicate the underlying bytes, but one slow branch can retain chunks and their backing allocations longer. Copy only when mutation or independent lifetime requires it.

## Multiple files rarely have one atomic rename

A filesystem generally lets one rename publish one pathname. Publishing data plus manifest plus rejects file requires a protocol: immutable version directory plus one pointer file, staged files with a manifest committed last, or independent commits with recovery metadata. Do not call a sequence of renames a transaction unless the environment provides that guarantee.

A strong application pattern writes a versioned bundle in a new directory, synchronizes its contents, then atomically replaces a small current-pointer file. Readers follow only complete bundles. Course 5 keeps the capstone to one primary output plus a report returned to the caller, but this module teaches the larger design.

## Terminal accounting precedes deterministic reporting

Concurrent or branched work can finish in any order. The final report should be reconstructed from stable source identities and typed terminal outcomes rather than append order. Counters observed live are useful diagnostics, not proof that every accepted item became accepted, rejected, skipped, or failed exactly once.

For record pipelines, maintain counts that satisfy a conservation equation such as inspected equals emitted plus filtered plus rejected. Assert it after successful completion and include it in tests.

## Commit coordination needs a failure matrix

List failure before any stage, after one candidate completes, during synchronization, during the first publication, and after the publication point. For each state, say which outputs are visible and which cleanup is safe. This matrix is more useful than a broad promise such as “atomic export”.

When no perfect rollback exists, prefer immutable versioned outputs and recovery tools over complicated best-effort reversal.

## Required fan-out is a coordinated write protocol

When two destinations must receive every chunk, the branch point cannot declare success until both accept the chunk. The producer should advance at the pace of the slowest required branch. Independent `pipe()` calls can work mechanically, but custom coordination often makes shared cancellation, exact terminal accounting, and branch-specific errors clearer.

The same Buffer can often be written to multiple destinations without copying because writable implementations should treat input chunks as read-only during the call. If a branch mutates or retains beyond its contract, copy at that boundary. Copying every chunk preemptively increases memory without solving pressure or completion.

## Side effects need authority classes

A synchronous byte counter or hash tap is an observation inside the main path. A metrics event may be allowed to drop. A rejects file may be a required product. An audit manifest may be the authority that tells readers a bundle is complete. These should not share one generic “listener” abstraction.

Write the failure policy next to the branch class. Required derivative failure cancels publication. Advisory observer failure may be logged or counted but must not corrupt the primary product. An authoritative manifest is committed last and may define which earlier staged files become visible to readers.

## Multi-file publication requires a recoverable protocol

Most filesystems provide atomic rename for one pathname, not an all-or-nothing group of unrelated renames. Strong designs use immutable version directories and one small current pointer, or publish all immutable data then commit a manifest that readers require. The protocol should make incomplete bundles ignorable and cleanup safe.

If the product instead commits files independently, document partial visibility and provide recovery metadata. The word transaction should be reserved for guarantees the storage system and protocol actually provide.

## Worked case — Conservation accounting

```ts
export interface RecordAccounting {
  readonly inspected: number;
  readonly emitted: number;
  readonly filtered: number;
  readonly rejected: number;
}

export function assertConservation(value: RecordAccounting): void {
  const terminal = value.emitted + value.filtered + value.rejected;
  if (terminal !== value.inspected) {
    throw new Error(`record accounting mismatch: inspected=${value.inspected}, terminal=${terminal}`);
  }
}
```

The equation is meaningful only when categories are mutually exclusive and every inspected record reaches exactly one terminal category. A stream error before a record is framed may leave input bytes without a record identity; byte accounting handles that separate layer. The final report should distinguish successful completion from partial diagnostic state after pipeline failure.

## Extended case analysis

An export produces `accepted.ndjson`, `rejected.ndjson`, and `manifest.json`. Publishing accepted then rejected then manifest creates intermediate states, but readers that only trust a complete manifest never observe a valid partial bundle. If manifest publication fails, the data files are orphan candidates that cleanup or a later recovery tool can remove. The manifest acts as authority; the earlier files are immutable derivatives.

## What this mechanism establishes

A correct implementation establishes these local facts:

- Every required destination receives identical bytes in identical order.

- The source advances only after all branches accept the current chunk.

- One branch failure destroys sibling branches and rejects the owner.

It does **not** establish the stronger claims hidden by these shortcuts:

- using EventEmitter for required async delivery;

- advancing when only one branch accepts capacity;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. Classify every side output by authority and failure policy.

2. Draw each queue and identify which branches must receive every item.

3. Coordinate pressure at the branch point rather than after memory has accumulated.

4. Choose one explicit multi-output publication protocol and state its limits.

5. Define conservation equations for bytes, records, and terminal outcomes.

6. Test every branch failing at several positions and inspect visible artifacts afterward.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Using EventEmitter for required side outputs

Synchronous listener invocation does not provide backpressure or coordinated async failure.

### Calling sequential renames atomic

Each pathname can become visible at a different point.

### Copying every chunk for fan-out

It can double memory without solving completion or branch pressure.

### Building final reports in completion order

Schedule variation leaks into user-visible output.

## Apply the mechanism in FlowLedger

Finalize FlowLedger reports and conservation equations. Keep the main output as the sole committed file, return digest and accounting metadata only after commit, and document how a future multi-file bundle would be versioned.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design an export that produces data.ndjson, rejects.ndjson, and manifest.json. Choose a publication protocol and give the visible-artifact state after each possible failure.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 49 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Coordinated Fan-Out Writer** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Distinguish observation taps, lossy side channels, and required fan-out branches

- Coordinate backpressure across multiple required destinations

- Define all-or-nothing, best-effort, and independently committed side-output policies

- Stage and publish related outputs without claiming impossible filesystem atomicity

- Produce deterministic reports from schedule-independent terminal evidence
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/stream.html](https://nodejs.org/docs/latest-v24.x/api/stream.html)
- [https://nodejs.org/docs/latest-v24.x/api/fs.html](https://nodejs.org/docs/latest-v24.x/api/fs.html)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-49-coordinated-fan-out-writer/README.md)
- [FlowLedger engineering guide](../capstone.md)
