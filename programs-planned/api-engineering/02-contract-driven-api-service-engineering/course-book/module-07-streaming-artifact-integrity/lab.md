# Lab — Module 07: Streaming and Artifact Integrity

> **Module 07:** Streaming and Artifact Integrity

## Objective

Upload content larger than the configured memory budget, interrupt it without publishing an artifact, verify checksums, stream progress and downloads, and detect deliberate on-disk corruption.

## Why this lab matters

This lab turns the module’s governing question—**How can large uploads, progress streams, and artifacts remain bounded, durable, and integrity-checked?**—into a falsifiable experiment. The Streaming and Artifact Integrity increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do large request and response bodies move through the service without unbounded memory or corrupt publication?*

## Hypothesis

The clean implementation should satisfy this claim: **At every interruption point, the final object is either absent or complete and hash-valid; no partial object is addressable by the API.** When the lab introduces this fault—**Plant direct-to-final upload, observe a concurrent partial read, repair, and retain the regression**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. **Implement chunked multipart staging with actual-byte limit and SHA-256.**
2. **Implement atomic content-addressed publication and metadata transaction.**
3. **Implement orphan and staging cleanup audits.**
4. **Implement owner-qualified artifact retrieval with bounded download stream.**
5. **Implement SSE and NDJSON from persisted event positions.**
6. **Run large, limit, limit+1, interrupted, duplicate-content, and foreign-owner cases.**
7. **Tamper with a published file and prove integrity detection.**
8. **Plant direct-to-final upload, observe a concurrent partial read, repair, and retain the regression.**

### Required planted defect

> Write uploads directly to the final served path and use a slow producer so another request can observe partial bytes.

Preserve the following evidence:

```text
prediction:
change introduced:
minimal setup:
first failing command:
public symptom:
durable/process state:
root cause:
repair:
regression path:
remaining limitation:
```

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant direct-to-final upload, observe a concurrent partial read, repair, and retain the regression**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Upload content larger than the configured memory budget, interrupt it without publishing an artifact, verify checksums, stream progress and downloads, and detect deliberate on-disk corruption**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

At every interruption point, the final object is either absent or complete and hash-valid; no partial object is addressable by the API.

## Required evidence

- baseline transcript proving the previous checkpoint before **Streaming and Artifact Integrity** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Streaming and Artifact Integrity**
- focused result for: Enforce limits while streaming rather than after buffering.
- public, durable, security, or operational observation showing: Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **bounded content-addressed artifact publication**
- a limitation statement naming every live dependency required to support the strongest **Streaming and Artifact Integrity** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Streaming and Artifact Integrity**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant direct-to-final upload, observe a concurrent partial read, repair, and retain the regression** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Streaming and Artifact Integrity**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Streaming and Artifact Integrity** experiment.
3. Rerun the focused regression and `make module-proof MODULE=07`.
4. Confirm the system again provides this result: Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.

## Completion gate

- bounded upload
- actual-byte limit
- private staging
- atomic publication
- orphan audit
- integrity proof
- owner-qualified access
- correct stream framing

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Streaming and Artifact Integrity**. A green command without the negative case and causal explanation does not satisfy this gate.
