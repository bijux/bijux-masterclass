# Lab — Module 03: JSON Schema Contract Modeling

> **Module 03:** JSON Schema Contract Modeling

## Objective

Build a 60+ case schema corpus that distinguishes absence, null, boundaries, closure, maps, and union exclusivity, then make both providers agree with the independent validator.

## Why this lab matters

This lab turns the module’s governing question—**How do schemas reject invalid states while remaining usable for providers, clients, and future evolution?**—into a falsifiable experiment. The course’s independent validator uses a format checker, and both providers configure formats needed by their runtime schemas. Capability differences are evidence, not reasons to assume validation occurred. 6. Input and output models serve different trust directions

It advances the cumulative Analysis Runs Platform by requiring this result: **Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which JSON values are legal, and which invalid states must the contract make impossible?*

## Hypothesis

The clean implementation should satisfy this claim: **at least 60 fixtures cover valid and invalid boundaries; missing and null are independent; domain objects are closed; intentional maps have bounded value schemas; source branches are mutually exclusive; independent and runtime validators agree.** When the lab introduces this fault—**Plant an overlapping union branch, observe the independent failure, and repair it without weakening closure**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant an overlapping union branch, observe the independent failure, and repair it without weakening closure**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Build a 60+ case schema corpus that distinguishes absence, null, boundaries, closure, maps, and union exclusivity, then make both providers agree with the independent validator**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- at least 60 fixtures cover valid and invalid boundaries
- missing and null are independent
- domain objects are closed
- intentional maps have bounded value schemas
- source branches are mutually exclusive
- independent and runtime validators agree

## Required evidence

- baseline transcript proving the previous checkpoint before **JSON Schema Contract Modeling** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **JSON Schema Contract Modeling**
- focused result for: Distinguish missing, null, empty, and default.
- public, durable, security, or operational observation showing: Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **JSON Schema Contract Modeling**
- a limitation statement naming every live dependency required to support the strongest **JSON Schema Contract Modeling** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **JSON Schema Contract Modeling**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant an overlapping union branch, observe the independent failure, and repair it without weakening closure** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **JSON Schema Contract Modeling**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **JSON Schema Contract Modeling** experiment.
3. Rerun the focused regression and `make module-proof MODULE=03`.
4. Confirm the system again provides this result: Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.

## Completion gate

- at least 60 fixtures cover valid and invalid boundaries
- missing and null are independent
- domain objects are closed
- intentional maps have bounded value schemas
- source branches are mutually exclusive
- independent and runtime validators agree

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **JSON Schema Contract Modeling**. A green command without the negative case and causal explanation does not satisfy this gate.
