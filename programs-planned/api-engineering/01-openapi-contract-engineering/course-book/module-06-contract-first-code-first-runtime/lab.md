# Lab — Module 06: Contract-First and Code-First Runtimes

> **Module 06:** Contract-First and Code-First Runtimes

## Objective

Inject four asymmetric provider defects and use operation mapping, provider-neutral scenarios, and generated-observation reports to locate them before opening implementation files.

## Why this lab matters

This lab turns the module’s governing question—**How do design-first and code-first descriptions relate, and how is semantic drift detected?**—into a falsifiable experiment. Scenarios should remain provider-neutral. They receive a base URL and credentials, not an imported application object. Provider unit tests can be faster and more diagnostic, but only a black-box suite proves that deployment adapters expose the same boundary. 8. Coercion is public behavior

It advances the cumulative Analysis Runs Platform by requiring this result: **Map every operation to both providers and compare generated observations with the canonical contract**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we implement one contract in two frameworks without letting framework defaults become accidental public behavior?*

## Hypothesis

The clean implementation should satisfy this claim: **canonical operation triples equal both handler maps; validation errors use one public problem shape; undeclared internal fields are filtered; shared scenarios pass against both base URLs; no semantic difference is hidden by an allowlist; generated documents remain observations.** When the lab introduces this fault—**Plant one wrong status in Python, one leaked field in TypeScript, one coercion mismatch, and one renamed operation ID**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant one wrong status in Python, one leaked field in TypeScript, one coercion mismatch, and one renamed operation ID**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Inject four asymmetric provider defects and use operation mapping, provider-neutral scenarios, and generated-observation reports to locate them before opening implementation files**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- canonical operation triples equal both handler maps
- validation errors use one public problem shape
- undeclared internal fields are filtered
- shared scenarios pass against both base URLs
- no semantic difference is hidden by an allowlist
- generated documents remain observations

## Required evidence

- baseline transcript proving the previous checkpoint before **Contract-First and Code-First Runtimes** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Contract-First and Code-First Runtimes**
- focused result for: Keep the canonical contract authoritative.
- public, durable, security, or operational observation showing: Both providers implement the complete contract and pass one provider-neutral behavioral suite.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Contract-First and Code-First Runtimes**
- a limitation statement naming every live dependency required to support the strongest **Contract-First and Code-First Runtimes** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Contract-First and Code-First Runtimes**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant one wrong status in Python, one leaked field in TypeScript, one coercion mismatch, and one renamed operation ID** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Contract-First and Code-First Runtimes**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Contract-First and Code-First Runtimes** experiment.
3. Rerun the focused regression and `make module-proof MODULE=06`.
4. Confirm the system again provides this result: Both providers implement the complete contract and pass one provider-neutral behavioral suite.

## Completion gate

- canonical operation triples equal both handler maps
- validation errors use one public problem shape
- undeclared internal fields are filtered
- shared scenarios pass against both base URLs
- no semantic difference is hidden by an allowlist
- generated documents remain observations

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Contract-First and Code-First Runtimes**. A green command without the negative case and causal explanation does not satisfy this gate.
