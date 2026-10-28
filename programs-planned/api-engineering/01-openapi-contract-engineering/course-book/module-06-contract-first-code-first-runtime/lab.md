# Lab — Module 06: Contract-First and Code-First Runtimes

## Objective

Inject four asymmetric provider defects and use operation mapping, provider-neutral scenarios, and generated-observation reports to locate them before opening implementation files.

## Setup conditions

The previous baseline is: **The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we implement one contract in two frameworks without letting framework defaults become accidental public behavior?*

## Failure action and investigation

1. Generate the canonical operation ledger and list the exact public triples each provider must expose.
2. Capture FastAPI and Fastify generated descriptions as reports without modifying canonical source.
3. Plant one wrong status in Python, one leaked field in TypeScript, one coercion mismatch, and one renamed operation ID.
4. Run the same black-box scenarios against each base URL and record the first observable divergence.
5. Run handler-map comparison and generated-observation analysis; classify each defect as operation, request, response, or framework-default drift.
6. Repair adapters and response schemas without changing the canonical contract to accommodate bugs.
7. Add a focused regression for every planted defect and produce a bounded limitation note for generated-document comparison.

### Required planted defect

Choose one defect from Failure Modes. Before fixing it, keep:

```text
defect:
predicted first failing gate:
actual first failing gate:
minimal request/instance/diff:
root cause:
repair:
permanent regression location:
```

## Operational oracle

The system satisfies the chapter’s central question: How do we implement one contract in two frameworks without letting framework defaults become accidental public behavior? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Contract-First and Code-First Runtimes** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Keep the canonical contract authoritative.
- public, durable, security, or operational observation showing: Both providers implement the complete contract and pass one provider-neutral behavioral suite.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Contract-First and Code-First Runtimes**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Contract-First and Code-First Runtimes**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=06`.
4. Confirm the system again provides this result: Both providers implement the complete contract and pass one provider-neutral behavioral suite.

## Completion gate

- canonical operation triples equal both handler maps
- validation errors use one public problem shape
- undeclared internal fields are filtered
- shared scenarios pass against both base URLs
- no semantic difference is hidden by an allowlist
- generated documents remain observations
