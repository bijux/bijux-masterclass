# Checkpoint — AsyncAPI, CloudEvents, and Contract Architecture

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Explain operation direction from the application perspective.
- Distinguish logical channel, physical address, message name, and CloudEvents type.
- Describe the three layers: envelope, payload schema, and business invariant.
- State which parts of CloudEvents are standard and which are course-profile extensions.

## Required result

- `work/module-02/contract-review.md`
- `work/module-02/reference-map.json`
- `work/module-02/example-results.json`
- `work/module-02/evidence.json`
- `work/module-02/residual-risk.md`

## Commands

```bash
make data-proof
make contract-proof
make event-case-proof
make module-proof MODULE=02 TRACK=$TRACK
```

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

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.
