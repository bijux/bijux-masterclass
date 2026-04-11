# Completion Rubric

Use this page when you need to decide whether object-oriented understanding is actually
complete or still resting on vague class-shaped intuition.

## Completion standard

You should be able to do all of the following:

- explain which object is authoritative for a given invariant or lifecycle rule
- distinguish values, entities, aggregates, policies, adapters, and read models clearly
- justify where mutation belongs and where it should be blocked
- explain how persistence, time, or concurrency should adapt to the domain rather than distort it
- review an object boundary by ownership, collaboration, and proof instead of by class count

## Course outcomes

| Area | Completion signal |
| --- | --- |
| object semantics | you can explain identity, equality, and representation choices intentionally |
| boundary ownership | you can point to the object or layer that should absorb a change |
| lifecycle and validation | you can state the legal and illegal transitions and where they are enforced |
| collaboration and extension | you can say which behavior belongs in the domain, orchestration, or adapters |
| stewardship | you can write one architecture judgment backed by one file and one proof route |

## Capstone evidence

Use these as the minimum capstone evidence:

1. `make PROGRAM=python-programming/python-object-oriented-programming capstone-walkthrough`
2. `make PROGRAM=python-programming/python-object-oriented-programming test`
3. `make PROGRAM=python-programming/python-object-oriented-programming proof`

Running them is not enough if you cannot explain which object or boundary each route is proving.

## Reviewer questions

- Which object owns this invariant?
- Which state is authoritative and which is only derived?
- Where should a new rule, sink, or projection land?
- Which proof route would fail first if that ownership story drifted?
