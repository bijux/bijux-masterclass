# Lab — Module 05: Telemetry Architecture and Structured Events

## Objective

Define the telemetry schema, W3C trace-context boundary, structured event vocabulary, redaction policy, bounded exporters, and collector-failure behavior across API, worker, storage, and webhook paths.


## Setup conditions

The previous baseline is: **API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *What should the system record so an operator can reconstruct behavior without leaking secrets or blocking the request path?*

## Failure action and investigation

1. Process valid and invalid trace headers through both language cores.
2. Emit structured events and inspect the pre-export sink for redaction.
3. Disconnect the collector and generate more events than queue capacity.
4. Verify customer operations remain successful while drops increase.
5. Restore the collector and verify no unbounded replay storm.
6. Compare durable run truth with sampled/missing trace evidence.

### Required planted defect

Remove or bypass the central control for **Telemetry Architecture and Structured Events** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- No raw secret appears in any buffered or exported event.
- Invalid context cannot control trace identity.
- Queue memory remains bounded.
- Collector outage does not change durable API outcome.
- Drop and recovery transitions are visible with bounded labels.

## Required evidence

- baseline transcript proving the previous checkpoint before **Telemetry Architecture and Structured Events** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Separate logs, metrics, traces, and audit records by purpose.
- public, durable, security, or operational observation showing: API, worker, storage, and webhook paths emit consistent, privacy-safe operational events.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **bounded structured telemetry**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Reconnect or stop the synthetic collector.
2. Clear in-memory buffers and fixture secrets.
3. Verify no telemetry files remain outside the lab evidence directory.
4. Retain sanitized vector and drop reports.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=05` succeeds on the primary track.
