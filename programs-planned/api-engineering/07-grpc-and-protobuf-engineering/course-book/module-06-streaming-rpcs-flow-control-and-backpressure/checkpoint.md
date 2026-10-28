# Checkpoint — Module 06: Streaming RPCs, Flow Control, and Backpressure

## Required result

Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing.

## Demonstrate

- [ ] Choose unary, server-streaming, client-streaming, or bidirectional rpc from interaction semantics.
- [ ] Design protocol frames and state machines rather than treating a stream as an unbounded message list.
- [ ] Combine http/2 flow control with bounded application queues and backpressure.
- [ ] Implement resumable ordered observation without claiming a durable event log.
- [ ] Stream large uploads and downloads with exact size, checksum, and cancellation guarantees.
- [ ] Keep durable worker leases authoritative when bidirectional sessions disconnect or reconnect.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/shared/vectors/streaming.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/shared/vectors/flow-control.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-06-streaming-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we design long-lived and bulk-transfer RPCs so that slow peers, reconnects, oversized messages, and stale attempts cannot exhaust memory or corrupt state?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Streaming RPCs, Flow Control, and Backpressure** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
