# Lab — Break and repair the streaming protocols under slow peers and reconnects

**Module:** Streaming RPCs, Flow Control, and Backpressure

## Objective

Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing.

## Setup

Use the deterministic stream simulator for both tracks and the Python live gRPC reference for selected network cases. Configure very small queue and chunk limits so pressure appears quickly.

## Controlled actions

1. Run valid upload, download, watch, and worker-session sequences.
2. Send illegal metadata/data order, oversized chunks, excessive total bytes, and idle streams.
3. Slow the download and WatchRun consumers while the producer remains fast; record queue high-water marks.
4. Cancel upload mid-write and verify staging cleanup.
5. Reconnect WatchRun from a valid, duplicate, and expired sequence.
6. Reconnect a worker after lease generation changes and send a stale completion.

## Correctness oracle

All queues and content paths remain within declared bounds. Invalid framing fails before durable publication. Partial transfers are not exposed. Resume behavior is explicit, duplicate observations are harmless, and stale worker results cannot commit.

## Required evidence

- `capstone/shared/vectors/streaming.json`
- `capstone/shared/vectors/flow-control.json`
- `reports/module-06-streaming-proof.json`

## Cleanup

Remove staging and downloaded scratch files, close all streams, release permits, reset leases, and confirm queue gauges return to zero.

## Completion gate

No stream may have an unbounded queue, byte count, lifetime, or authority path; durable state and integrity checks must remain correct under reconnect and cancellation.

A successful command without this evidence does not complete the lab.
