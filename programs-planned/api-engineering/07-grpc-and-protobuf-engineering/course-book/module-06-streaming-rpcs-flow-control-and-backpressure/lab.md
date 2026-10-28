# Lab — Break and repair the streaming protocols under slow peers and reconnects

> **Module 06:** Streaming RPCs, Flow Control, and Backpressure

## Objective

Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing.

## Why this lab matters

This lab turns the module’s governing question—**How do we design long-lived and bulk-transfer RPCs so that slow peers, reconnects, oversized messages, and stale attempts cannot exhaust memory or corrupt state?**—into a falsifiable experiment. Unary default message limits may be too small for bulk data and too large for control messages. Configure method-specific limits. UploadDataset uses bounded chunks and a declared total/checksum. DownloadArtifact uses bounded chunks and optional offset/limit. Worker control frames remain small. Reject compressed-message bombs based on decompressed size and work, not only wire bytes.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Use the deterministic stream simulator for both tracks and the Python live gRPC reference for selected network cases. Configure very small queue and chunk limits so pressure appears quickly.

## Hypothesis

The clean implementation should satisfy this claim: **All queues and content paths remain within declared bounds. Invalid framing fails before durable publication. Partial transfers are not exposed. Resume behavior is explicit, duplicate observations are harmless, and stale worker results cannot commit.** When the lab introduces this fault—**Reconnect WatchRun from a valid, duplicate, and expired sequence**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Run valid upload, download, watch, and worker-session sequences.
2. Send illegal metadata/data order, oversized chunks, excessive total bytes, and idle streams.
3. Slow the download and WatchRun consumers while the producer remains fast; record queue high-water marks.
4. Cancel upload mid-write and verify staging cleanup.
5. Reconnect WatchRun from a valid, duplicate, and expired sequence.
6. Reconnect a worker after lease generation changes and send a stale completion.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Reconnect WatchRun from a valid, duplicate, and expired sequence**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement WatchRun, UploadDataset, DownloadArtifact, and the worker Work stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

All queues and content paths remain within declared bounds. Invalid framing fails before durable publication. Partial transfers are not exposed. Resume behavior is explicit, duplicate observations are harmless, and stale worker results cannot commit.

## Required evidence

- `capstone/shared/vectors/streaming.json`
- `capstone/shared/vectors/flow-control.json`
- `reports/module-06-streaming-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Streaming RPCs, Flow Control, and Backpressure**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Reconnect WatchRun from a valid, duplicate, and expired sequence** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove staging and downloaded scratch files, close all streams, release permits, reset leases, and confirm queue gauges return to zero.

## Completion gate

No stream may have an unbounded queue, byte count, lifetime, or authority path; durable state and integrity checks must remain correct under reconnect and cancellation.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Streaming RPCs, Flow Control, and Backpressure**. A green command without the negative case and causal explanation does not satisfy this gate.
