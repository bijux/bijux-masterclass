# Lab — Module 02: Operations, Parameters, and Messages

> **Module 02:** Operations, Parameters, and Messages

## Objective

Add project patch and dataset collection/member operations, then prove parameter serialization, response fields, and content semantics at the raw HTTP boundary.

## Why this lab matters

This lab turns the module’s governing question—**How are parameters, request bodies, media types, status codes, and headers modeled without ambiguity?**—into a falsifiable experiment. Choose location from semantics before choosing framework syntax. A filter does not become a path segment because a router makes it easy. A concurrency precondition does not belong in the JSON patch because intermediaries and generic HTTP tooling understand the field-line semantics. 2. Parameter serialization is a wire algorithm

It advances the cumulative Analysis Runs Platform by requiring this result: **Complete project and dataset messages, including pagination inputs, creation responses, and problem representations**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we specify every input and output precisely enough that independent clients serialize the same exchange?*

## Hypothesis

The clean implementation should satisfy this claim: **every value has one intentional wire location; serialization has literal examples; 201 includes Location; 204 carries no content; validation uses application/problem+json; both providers reject the same malformed messages.** When the lab introduces this fault—**Plant a body on one 204 response, demonstrate the failing raw-byte assertion, then repair it**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a body on one 204 response, demonstrate the failing raw-byte assertion, then repair it**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Add project patch and dataset collection/member operations, then prove parameter serialization, response fields, and content semantics at the raw HTTP boundary**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- every value has one intentional wire location
- serialization has literal examples
- 201 includes Location
- 204 carries no content
- validation uses application/problem+json
- both providers reject the same malformed messages

## Required evidence

- baseline transcript proving the previous checkpoint before **Operations, Parameters, and Messages** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Operations, Parameters, and Messages**
- focused result for: Model path, query, header, cookie, and body input deliberately.
- public, durable, security, or operational observation showing: Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Operations, Parameters, and Messages**
- a limitation statement naming every live dependency required to support the strongest **Operations, Parameters, and Messages** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Operations, Parameters, and Messages**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a body on one 204 response, demonstrate the failing raw-byte assertion, then repair it** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Operations, Parameters, and Messages**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Operations, Parameters, and Messages** experiment.
3. Rerun the focused regression and `make module-proof MODULE=02`.
4. Confirm the system again provides this result: Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.

## Completion gate

- every value has one intentional wire location
- serialization has literal examples
- 201 includes Location
- 204 carries no content
- validation uses application/problem+json
- both providers reject the same malformed messages

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Operations, Parameters, and Messages**. A green command without the negative case and causal explanation does not satisfy this gate.
