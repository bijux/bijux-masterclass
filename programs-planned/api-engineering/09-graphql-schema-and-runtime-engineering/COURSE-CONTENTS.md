# Complete course contents

Course 9 is a complete, cumulative self-learning course rather than a schema
syntax survey. The primary product is a 61-page course book containing
orientation, ten full chapters, 120 transfer exercises, 120 corresponding
worked answers, ten laboratories, and ten non-compensable checkpoints.

## Learner-facing material

```text
course-book/
├── index.md
├── start-here.md
├── study-plan.md
├── standards.md
├── language-strategy.md
├── evidence-model.md
├── capstone.md
├── glossary.md
├── module-00-orientation/
└── module-01-... through module-10-.../
```

Every numbered module contains exactly:

```text
index.md              complete authoritative chapter
exercises.md          twelve module-specific transfer problems
exercise-answers.md   twelve matching reasoned solutions
lab.md                one controlled practical investigation
checkpoint.md         required evidence before progression
```

## Contract and publication assets

The capstone contains Analysis Graph API 1.0, ten released persisted operations,
a field-ownership catalogue, a client catalogue, query-budget and release
policies, security rules, compatibility candidates, migration history, and an
exact Course 10 handoff. A frontier schema demonstrates incremental-delivery
syntax without silently adding it to the executable baseline.

## Implementations

The Python reference track provides a dependency-light semantic gateway and an
optional Strawberry adapter. The TypeScript track provides equivalent semantics
and an optional GraphQL Yoga adapter. Both tracks cover identifiers, signed
cursors, operation parsing, demand analysis, batching, source clients, field
policy, mutation delegation, partial data, subscription resume, transport
admission, and release decisions.

The loopback laboratory starts the graph gateway and three source services as
separate HTTP servers. It demonstrates real network composition, batched
collaboration, tenant propagation, and field-specific partial failure.

## Verification assets

The course includes focused proof commands for schema, ownership, batching,
pagination, mutation semantics, authorization, demand control, error behavior,
subscriptions, releases, migrations, vectors, both implementation tracks, the
network laboratory, planted defects, final defense, and the Course 10 handoff.

Ten planted defects verify that the proof system can reject attractive but
unsafe changes, including direct database ownership, unbounded fan-out,
principal-free cache keys, mutation replay without idempotency, silent partial
failure, subscription gaps, and schema releases that invalidate active clients.

The release package also contains exact SHA-256 manifests, this final verification
record, a machine-readable release report, and deterministic archive metadata.
