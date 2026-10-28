# Checkpoint — Module 02: AsyncAPI, CloudEvents, and Contract Architecture

## Required result

Publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles.

## Demonstrate

- Explain operation direction from the application perspective.
- Distinguish logical channel, physical address, message name, and CloudEvents type.
- Describe the three layers: envelope, payload schema, and business invariant.
- State which parts of CloudEvents are standard and which are course-profile extensions.

## Commands

```bash
make data-proof
make contract-proof
make event-case-proof
make module-proof MODULE=02 TRACK=$TRACK
```

## Evidence to retain

- `work/module-02/contract-review.md`
- `work/module-02/reference-map.json`
- `work/module-02/example-results.json`
- failure outputs for reversed direction, bad example, and missing reference
- repaired contract diff
- `make contract-proof` output
- optional independent-validator output marked executed or not executed

## Defend the design

- Trace one operation through every referenced artifact.
- Defend one field placed in the envelope rather than the payload.
- Explain why a generated TypeScript type is not runtime validation.
- Describe exactly what the local contract proof does not prove.

## Continue only when

- Any example fails envelope or payload validation.
- Any reference requires network access.
- Any operation direction is ambiguous or reversed.
- The learner overstates custom-validator conformance.

The **AsyncAPI, CloudEvents, and Contract Architecture** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.
