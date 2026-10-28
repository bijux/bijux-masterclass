# Lab — Module 02: Operations, Parameters, and Messages

## Objective

Add project patch and dataset collection/member operations, then prove parameter serialization, response fields, and content semantics at the raw HTTP boundary.

## Setup conditions

The previous baseline is: **The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we specify every input and output precisely enough that independent clients serialize the same exchange?*

## Failure action and investigation

1. Create a location table for every new value and justify each path/query/header/body choice.
2. Write literal URI examples for pagination and status filtering, plus malformed variants.
3. Add modular Parameter, Header, Request Body, and Response Objects; reuse only when semantics truly match.
4. Implement adapters in Python and TypeScript and translate native validation failures to the public problem schema.
5. Add tests for 201/Location, empty 204, invalid cursor, unknown query, unsupported content type, and malformed JSON.
6. Run the same behavioral cases against both providers.
7. Plant a body on one 204 response, demonstrate the failing raw-byte assertion, then repair it.

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

The system satisfies the chapter’s central question: How do we specify every input and output precisely enough that independent clients serialize the same exchange? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Operations, Parameters, and Messages** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Model path, query, header, cookie, and body input deliberately.
- public, durable, security, or operational observation showing: Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Operations, Parameters, and Messages**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Operations, Parameters, and Messages**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=02`.
4. Confirm the system again provides this result: Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.

## Completion gate

- every value has one intentional wire location
- serialization has literal examples
- 201 includes Location
- 204 carries no content
- validation uses application/problem+json
- both providers reject the same malformed messages
