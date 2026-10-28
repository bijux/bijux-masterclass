# Lab — Module 01: Application Use Cases and Boundaries

## Objective

Map every frozen operation to one use-case owner, implement the first project slice through ports, and prove the application layer runs without an HTTP server.

## Setup conditions

The previous baseline is: **the orientation baseline** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does a public operation become maintainable application behavior without making route handlers the architecture?*

## Failure action and investigation

1. **Verify the predecessor manifest and copy no contract file into an editable location.**
2. **Build the complete operation ownership map, including anonymous and protected operations.**
3. **Trace `createProject` and `getProject` through transport, command, service, port, mapping, and response.**
4. **Implement the slice first with deterministic in-memory ports in the chosen primary track.**
5. **Run the same use-case tests without starting the framework.**
6. **Wire the route adapters and run the frozen behavioral scenarios for the slice.**
7. **Plant a framework-owned validation rule, observe which direct test fails to detect it, then move the rule and keep the regression.**
8. **Review the second language track and write a comparison note naming one idiomatic difference and one invariant shared at the boundary.**

### Required planted defect

> Put the project-name rule only in the HTTP route. The direct use-case test should reveal that the architecture cannot defend the invariant outside HTTP.

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

A direct application test must reject the same invalid command as the HTTP route while importing no framework package.

## Required evidence

- baseline transcript proving the previous checkpoint before **Application Use Cases and Boundaries** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Separate transport, application, domain, and infrastructure responsibilities.
- public, durable, security, or operational observation showing: Project operations run through framework-independent use cases while preserving the Course 1 contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **operation-to-use-case mapping**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Application Use Cases and Boundaries**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=01`.
4. Confirm the system again provides this result: Project operations run through framework-independent use cases while preserving the Course 1 contract.

## Completion gate

- predecessor hashes unchanged
- all operations assigned
- project use cases execute without HTTP
- no framework imports in domain policies
- one problem translator
- explicit principal input
- composition root owns resources
- planted defect retained as regression
