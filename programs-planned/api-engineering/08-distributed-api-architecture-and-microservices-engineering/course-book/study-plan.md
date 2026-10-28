# Ten-day study plan

Course 8 is designed as ten dense study days after orientation. Each day produces one durable architecture artifact. The artifacts accumulate into the final extraction and defense; they are not isolated assignments.

## Before Day 1 — orientation

Prove the Course 7 handoff, select a primary implementation track, and trace one analysis from public request to artifact and notification. Do not begin decomposition until you can identify every existing transaction authority and contract.

## Daily progression

| Day | Module | Cumulative result |
|---:|---|---|
| 1 | Distribution economics and boundary evidence | boundary scorecard with approved, conditional, retained, and rejected candidates |
| 2 | Service boundaries and contract ownership | service catalogue, context map, contract ownership, and anti-corruption mappings |
| 3 | Data ownership and cross-service queries | one-writer data map, projection policies, staleness contracts, and reconciliation design |
| 4 | Synchronous collaboration | acyclic dependency graph, absolute budgets, bounded composition, and truthful partiality |
| 5 | Sagas and compensation | durable artifact-completion process manager with failure schedules and manual-review state |
| 6 | Service identity and authorization | workload/user/tenant/effect identity matrix and narrow artifact capabilities |
| 7 | Discovery, routing, and topology | health-aware routing, gateway limits, shadow safety, and declared network paths |
| 8 | Deployment independence | old/new compatibility matrix, service-owned migrations, shadow/canary evidence, and rollback |
| 9 | Distributed verification | proof matrix, fault experiments, reconciliation findings, and operability review |
| 10 | Incremental extraction | notification and artifact strangler migration, decommission evidence, merge-back criteria, and final defense |

## Suggested daily rhythm

```text
08:30–09:00  retrieval from the previous module
09:00–11:15  authoritative chapter and worked decisions
11:30–12:30  architecture artifact review
13:30–15:00  primary implementation track
15:15–17:30  controlled lab or failure schedule
18:30–19:30  twelve exercises
19:30–20:30  compare worked answers and revise
20:30–21:00  checkpoint evidence and architecture journal
```

The schedule is demanding because the course is cumulative. Do not compensate for a missing checkpoint by reading faster. Repair the evidence.

## Middle-of-course review after Module 5

Before continuing, defend these statements without notes:

- why Notification deserves extraction before Artifact;
- why Analysis Control remains cohesive;
- which facts each proposed service may write;
- how a run-with-artifacts query behaves during Artifact outage;
- why a timeout does not reveal whether a remote mutation committed;
- how the artifact saga handles a stale worker attempt;
- why compensation is a new business action rather than rollback.

Then run:

```bash
make boundary-proof
make ownership-proof
make data-proof
make dependency-proof
make saga-proof
```

## Final review after Module 10

The final defense is not a tour of files. It is a causal explanation of one workflow and one failure:

1. show the public request and owner decision;
2. identify each local transaction;
3. show every remote contract and identity;
4. inject response loss after Artifact commit;
5. recover with stable effect identity;
6. reconcile owner state;
7. show mixed-version compatibility and route rollback;
8. justify every retained and extracted boundary;
9. identify a merge-back condition.

## Alternative pacing

A self-directed learner may take two weeks with weekends reserved for repair:

```text
Week 1: orientation and Modules 1–5
Weekend: repeat failure schedules and repair evidence
Week 2: Modules 6–10 and final defense
```

Do not split one module across many weeks without revisiting earlier artifacts. Distributed architecture concepts depend heavily on retained context.
