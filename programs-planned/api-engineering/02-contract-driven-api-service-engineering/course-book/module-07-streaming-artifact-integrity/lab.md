# Lab — Module 07: Streaming and Artifact Integrity

## Objective

Upload content larger than the configured memory budget, interrupt it without publishing an artifact, verify checksums, stream progress and downloads, and detect deliberate on-disk corruption.

## Setup conditions

The previous baseline is: **Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do large request and response bodies move through the service without unbounded memory or corrupt publication?*

## Failure action and investigation

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

## Operational oracle

At every interruption point, the final object is either absent or complete and hash-valid; no partial object is addressable by the API.

## Required evidence

- baseline transcript proving the previous checkpoint before **Streaming and Artifact Integrity** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Enforce limits while streaming rather than after buffering.
- public, durable, security, or operational observation showing: Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **bounded content-addressed artifact publication**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Streaming and Artifact Integrity**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
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
