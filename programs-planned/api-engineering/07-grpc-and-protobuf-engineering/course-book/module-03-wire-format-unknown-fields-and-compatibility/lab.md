# Lab — Evolve Analysis RPC without lying about compatibility

> **Module 03:** Wire Format, Unknown Fields, and Compatibility Discipline

## Objective

Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes.

## Why this lab matters

This lab turns the module’s governing question—**How can an RPC contract evolve without corrupting old data, breaking generated clients, or creating behavior that is wire-readable but operationally unsafe?**—into a falsifiable experiment. The final release report joins schema analysis with consumer declarations and golden bytes. It states: wire compatible; source compatible for declared generated consumers; ProtoJSON additive with one repaired strict consumer; behavior review approved under a bounded operator-visible policy. It also records Buf as not executed when unavailable.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Use RPC 1.0 as the baseline. Copy it into a temporary candidate workspace and keep the checked-in golden bytes and consumer declarations unchanged.

## Hypothesis

The clean implementation should satisfy this claim: **The additive candidate is accepted only with consumer evidence. Tag reuse, enum renumbering, and method-shape mutation are rejected. Reports identify compatibility dimension and affected consumers rather than returning one undifferentiated boolean.** When the lab introduces this fault—**Renumber an enum value and observe golden semantic failure**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Add one optional response field with a fresh tag and classify it across wire, source, JSON, and behavior.
2. Create a candidate that reuses a removed tag and confirm the local and external-compatible proof reject it.
3. Renumber an enum value and observe golden semantic failure.
4. Rename a field without changing its tag and record the binary/source/JSON disagreement.
5. Change a unary method to streaming and confirm it is classified as a new incompatible method shape.
6. Regenerate or compare descriptors and run supported Python, TypeScript, and optional Buf checks.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Renumber an enum value and observe golden semantic failure**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The additive candidate is accepted only with consumer evidence. Tag reuse, enum renumbering, and method-shape mutation are rejected. Reports identify compatibility dimension and affected consumers rather than returning one undifferentiated boolean.

## Required evidence

- `capstone/releases/rpc-1.1/compatibility-report.json`
- `capstone/shared/golden/analysis-run-v1.bin`
- `reports/module-03-wire-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Wire Format, Unknown Fields, and Compatibility Discipline**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Renumber an enum value and observe golden semantic failure** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Delete temporary candidates, restore the baseline schema digest, and verify golden fixtures remain unchanged.

## Completion gate

No release may be labeled compatible without separate wire, source, ProtoJSON, behavioral, and consumer evidence.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Wire Format, Unknown Fields, and Compatibility Discipline**. A green command without the negative case and causal explanation does not satisfy this gate.
