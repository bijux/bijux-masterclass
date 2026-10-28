# Lab — Evolve Analysis RPC without lying about compatibility

**Module:** Wire Format, Unknown Fields, and Compatibility Discipline

## Objective

Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes.

## Setup

Use RPC 1.0 as the baseline. Copy it into a temporary candidate workspace and keep the checked-in golden bytes and consumer declarations unchanged.

## Controlled actions

1. Add one optional response field with a fresh tag and classify it across wire, source, JSON, and behavior.
2. Create a candidate that reuses a removed tag and confirm the local and external-compatible proof reject it.
3. Renumber an enum value and observe golden semantic failure.
4. Rename a field without changing its tag and record the binary/source/JSON disagreement.
5. Change a unary method to streaming and confirm it is classified as a new incompatible method shape.
6. Regenerate or compare descriptors and run supported Python, TypeScript, and optional Buf checks.

## Correctness oracle

The additive candidate is accepted only with consumer evidence. Tag reuse, enum renumbering, and method-shape mutation are rejected. Reports identify compatibility dimension and affected consumers rather than returning one undifferentiated boolean.

## Required evidence

- `capstone/releases/rpc-1.1/compatibility-report.json`
- `capstone/shared/golden/analysis-run-v1.bin`
- `reports/module-03-wire-proof.json`

## Cleanup

Delete temporary candidates, restore the baseline schema digest, and verify golden fixtures remain unchanged.

## Completion gate

No release may be labeled compatible without separate wire, source, ProtoJSON, behavioral, and consumer evidence.

A successful command without this evidence does not complete the lab.
