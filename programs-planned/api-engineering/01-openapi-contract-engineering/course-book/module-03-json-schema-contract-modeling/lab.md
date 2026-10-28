# Lab — Module 03: JSON Schema Contract Modeling

## Objective

Build a 60+ case schema corpus that distinguishes absence, null, boundaries, closure, maps, and union exclusivity, then make both providers agree with the independent validator.

## Setup conditions

The previous baseline is: **Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which JSON values are legal, and which invalid states must the contract make impossible?*

## Failure action and investigation

1. Draw the legal instance sets for create, patch, response, problem, dataset source, run parameters, and artifact schemas.
2. Add smallest valid, largest valid, missing, null, wrong-type, boundary, unknown-property, and union-overlap fixtures.
3. Run `make -C capstone fixtures` before adapting provider models; treat failures as design feedback.
4. Map schemas to Pydantic with aliases, forbidden extras, discriminated unions, and bounded fields.
5. Map the same constraints to TypeBox/Ajv and configure required formats explicitly.
6. Add HTTP-level tests proving invalid JSON never enters domain logic and response serialization rejects leakage.
7. Plant an overlapping union branch, observe the independent failure, and repair it without weakening closure.

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

The system satisfies the chapter’s central question: Which JSON values are legal, and which invalid states must the contract make impossible? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **JSON Schema Contract Modeling** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Distinguish missing, null, empty, and default.
- public, durable, security, or operational observation showing: Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **JSON Schema Contract Modeling**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **JSON Schema Contract Modeling**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=03`.
4. Confirm the system again provides this result: Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.

## Completion gate

- at least 60 fixtures cover valid and invalid boundaries
- missing and null are independent
- domain objects are closed
- intentional maps have bounded value schemas
- source branches are mutually exclusive
- independent and runtime validators agree
