# Lab — Module 09: Fault Injection, Troubleshooting, and Game Days

## Objective

Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive.


## Setup conditions

The previous baseline is: **Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Can the system and its operators detect a controlled failure, find the durable cause, mitigate it, and return to a verified steady state?*

## Failure action and investigation

1. Inject worker claim delay while leaving API health green.
2. Observe run-start freshness burn and queue-age alert.
3. Diagnose from accepted run to durable job and worker claim evidence.
4. Introduce a telemetry-export drop as a secondary fault only after primary diagnosis.
5. Mitigate safely, recover workers, and run read-only reconciliation.
6. Plant one missing alert or misleading dashboard panel and demonstrate detection.

### Required planted defect

Remove or bypass the central control for **Fault Injection, Troubleshooting, and Game Days** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- API availability may remain healthy while run-start freshness fails.
- Durable accepted jobs remain present and recoverable.
- Telemetry loss reduces diagnosis quality but not correctness.
- Mitigation stops budget burn without duplicate completion.
- Cleanup and reconciliation report no unresolved critical finding.

## Required evidence

- baseline transcript proving the previous checkpoint before **Fault Injection, Troubleshooting, and Game Days** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Predict the failure and first oracle before injection.
- public, durable, security, or operational observation showing: A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **bounded fault injection and diagnosis**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Disable all injector profiles and verify control endpoint state.
2. Drain or resolve synthetic jobs and deliveries.
3. Release permits and remove temporary data.
4. Publish timeline, hypotheses, evidence, remediation, and retained regression.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=09` succeeds on the primary track.
