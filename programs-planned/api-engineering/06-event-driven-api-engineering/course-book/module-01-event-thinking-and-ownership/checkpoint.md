# Checkpoint — Module 01: Event Thinking, Ownership, and Message Taxonomy

## Required result

Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary.

## Demonstrate

- Explain why temporal decoupling does not eliminate semantic coupling.
- Distinguish a rejected command from a malformed delivery of an already-recorded event.
- Name the owner and durable oracle for every Analysis Events 1.0 type.
- Explain why the partition key is not automatically the correlation ID.

## Commands

```bash
make predecessor-proof
make event-case-proof
make vector-proof
make module-proof MODULE=01 TRACK=$TRACK
```

## Evidence to retain

- `work/module-01/interaction-map.md`
- `work/module-01/publication-decisions.yaml`
- `work/module-01/rejected-candidates.md`
- a diff for `message-taxonomy.yaml` and `event-catalog.yaml`
- output from `make module-proof MODULE=01 TRACK=$TRACK`
- one paragraph explaining which important interaction remains synchronous

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

The **Event Thinking, Ownership, and Message Taxonomy** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.
