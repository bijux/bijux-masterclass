# Lab — Break and repair nullability

> **Module 02:** Type System, Nullability, and Semantic Modeling

## Objective

Observe nullability as executable failure control rather than a type-style preference. Prove OneOf input coercion and output-completion behavior.

## Why this lab matters

This lab turns the module’s governing question—**How does the schema make useful promises without promising values the runtime cannot sustain?**—into a falsifiable experiment. OneOf Input Objects model exclusive alternatives. NodeLookup @oneOf requires exactly one non-null field, so {id: ...} and {externalId: ...} are valid while {} and {id: ..., externalId: ...} are not. This is superior to an input object whose resolver must guess precedence between two optional keys.

It advances the cumulative Analysis Runs Platform by requiring this result: **Release Analysis Graph API 1.0 type and nullability policies**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Complete Module 1. Copy `capstone/contracts/schema.graphql` to a scratch directory; never edit the released schema in place.

## Hypothesis

The clean implementation should satisfy this claim: **released remote field failure preserves the AnalysisRun object; scratch non-null field increases the bubbling blast radius; null list items obey item nullability; invalid resolver output is an execution/completion error; OneOf accepts exactly one non-null alternative; every rejected input makes zero source calls.** When the lab introduces this fault—**Inject Artifact Service unavailability and repeat**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

### 1. Capture the released behavior

Execute `GetRun` with Artifact Service healthy and record a complete result. Inject Artifact Service unavailability and repeat. The run must remain present, `artifacts` must become null, and the error path must point to `analysisRun.artifacts`.

### 2. Strengthen nullability unsafely

Change only the scratch SDL to `[Artifact!]!`. Execute the same failure through a complete framework adapter when available or the checked-in completion simulator otherwise. Draw the exact propagation path from `artifacts` to its nearest nullable ancestor.

### 3. Violate item nullability

Return a list containing one null item for `[Artifact!]`. Confirm that the list itself becomes null and the error path includes the item index. Compare this with `[Artifact]`, and explain why the latter is not the chosen contract.

### 4. Test scalar and enum completion

Inject an invalid `size`, malformed `DateTime`, and unknown `RunStatus` output. These are server contract failures. They must not be reported as client variable errors.

### 5. Test OneOf coercion

Evaluate:

```text
{id: "..."}
{externalId: "..."}
{}
{id: "...", externalId: "..."}
{id: null}
```

Exactly one non-null member is required. Record whether rejection occurs before resolver execution.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject Artifact Service unavailability and repeat**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Observe nullability as executable failure control rather than a type-style preference. Prove OneOf input coercion and output-completion behavior**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- released remote field failure preserves the `AnalysisRun` object;
- scratch non-null field increases the bubbling blast radius;
- null list items obey item nullability;
- invalid resolver output is an execution/completion error;
- OneOf accepts exactly one non-null alternative;
- every rejected input makes zero source calls.

## Required evidence

Create `reports/module-02-type-nullability.json` containing the released and scratch type declarations, completed data trees, error paths, bubble targets, and OneOf coercion table. Include a short design decision explaining why the released nullability is sustainable across authorization and source failure.

## Interpretation and defense

1. Which state or effect is authoritative for **Type System, Nullability, and Semantic Modeling**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject Artifact Service unavailability and repeat** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Delete the scratch schema and injected fixtures. Re-run schema, vector, and module proofs. The released SDL and predecessor handoff must have no diff.

## Completion gate

Your evidence predicts every completion tree before execution, OneOf outcomes match both language tracks, and the scratch non-null change is classified correctly by the release checker.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Type System, Nullability, and Semantic Modeling**. A green command without the negative case and causal explanation does not satisfy this gate.
