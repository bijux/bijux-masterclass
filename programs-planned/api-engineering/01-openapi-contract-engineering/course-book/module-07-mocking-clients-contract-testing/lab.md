# Lab — Module 07: Mocks, Clients, and Contract Testing

## Objective

Execute the full contract toolchain, promote at least five generated boundary failures into permanent fixtures, and prove Python and TypeScript consumers complete the same outcome workflow.

## Setup conditions

The previous baseline is: **Both providers implement the complete contract and pass one provider-neutral behavioral suite.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we turn the contract into a development and verification tool rather than a static document?*

## Failure action and investigation

1. Add and fixture custom lint rules for operation identity, explicit security, response content, and public descriptions.
2. Bundle the canonical source deterministically and start a contract mock with request validation enabled.
3. Generate Python and TypeScript clients from the same bundled description; compile/import them without hand edits.
4. Run consumer happy-path and documented-error tests against the mock, then both real providers.
5. Run generated property tests with bounded cases and deterministic reporting; classify every failure.
6. Run a stateful workflow or explicit state machine across create, upload, start, progress, artifact, and cancellation behavior.
7. Promote minimized high-value failures into `tests/fixtures` or shared scenarios and update the capability matrix.

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

The system satisfies the chapter’s central question: How do we turn the contract into a development and verification tool rather than a static document? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Mocks, Clients, and Contract Testing** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Distinguish syntax, semantic linting, conformance, and consumer tests.
- public, durable, security, or operational observation showing: Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Mocks, Clients, and Contract Testing**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Mocks, Clients, and Contract Testing**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=07`.
4. Confirm the system again provides this result: Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.

## Completion gate

- custom rules have passing/failing fixtures
- mock requests are validated
- both generated clients build or import
- consumer workflow runs against real providers
- generated failures are reproducible
- unsupported features are reported rather than dropped
