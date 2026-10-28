# Checkpoint — Event Thinking, Ownership, and Message Taxonomy

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Explain why temporal decoupling does not eliminate semantic coupling.
- Distinguish a rejected command from a malformed delivery of an already-recorded event.
- Name the owner and durable oracle for every Analysis Events 1.0 type.
- Explain why the partition key is not automatically the correlation ID.

## Required result

- `work/module-01/interaction-map.md`
- `work/module-01/publication-decisions.yaml`
- `work/module-01/rejected-candidates.md`
- `work/module-01/evidence.json`
- `work/module-01/residual-risk.md`

## Commands

```bash
make predecessor-proof
make event-case-proof
make vector-proof
make module-proof MODULE=01 TRACK=$TRACK
```

## Defend the design

- Defend one interaction that remains synchronous.
- Show how a domain event is transformed before becoming an integration event.
- Explain what would happen if a second producer emitted the same event type.
- Describe the compatibility obligation created by publishing one new field.

## Continue only when

- Any public message lacks an authoritative owner.
- A command is named or documented as an immutable fact.
- A public payload exposes storage or security internals.
- The learner cannot identify a durable record that proves an event.

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.
