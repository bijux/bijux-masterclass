# Ten-day intensive study plan

The course is designed as ten dense days after orientation. A realistic day includes reading, prediction, implementation inspection, a controlled failure, evidence review, and retrieval practice. Do not compress two modules into one day simply because the YAML appears familiar; the difficult material is ownership and failure semantics.

| Day | Central question | Capstone increment | Required evidence |
|---:|---|---|---|
| 1 | Who reconciles which transition? | component-ownership contract and semantic API store | earliest-missing-transition analysis |
| 2 | How do several actors modify one API safely? | apply conflicts, resource versions, finalizer lifecycle | managed-field and deletion transcript |
| 3 | What exactly is a Pod lifecycle boundary? | secure API/worker Pod templates | container-state and shutdown evidence |
| 4 | How is a rollout bounded mathematically? | three-replica API Deployment and strategy | resolved rollout integers and stalled-release diagnosis |
| 5 | Which controller matches the workload invariant? | Job, CronJob, DaemonSet laboratories | retry/effect identity and controller-choice dossier |
| 6 | How do configuration, secrets, and identity reach a workload? | configuration and ServiceAccount projection | change-consumption and rotation contract |
| 7 | Why can or cannot a Pod schedule? | resource and topology model | per-Node predicate explanation |
| 8 | Which failures remove traffic, restart a process, or block disruption? | probes, shutdown, PDB | availability-population calculation |
| 9 | Which identity must survive replacement? | StatefulSet sentinel and worker-fit rejection | stable-identity decision and residual data risk |
| 10 | Is a custom declarative API justified? | AtlasWorkload CRD, controller, finalizer, release | no-churn convergence and Course 5 handoff |

## Daily rhythm

A useful schedule is:

```text
08:30–09:00  retrieval from the previous module
09:00–11:00  chapter reading and diagrams
11:15–12:30  exercises 1–6
13:30–14:30  implementation and manifest walkthrough
14:45–17:15  controlled laboratory
17:30–18:30  exercises 7–12 and answer comparison
19:30–20:30  evidence packet and checkpoint defense
```

## Middle-week review

After Day 5, repeat three analyses without notes:

- trace a Deployment from admission to ready Pod;
- distinguish Job completion from exactly-once effect;
- explain a field conflict without saying “last write wins.”

If those cannot be explained clearly, repair them before moving into configuration and scheduling.

## Completion rule

Reading all pages does not complete the course. Every checkpoint is non-compensable. The final defense requires exact predecessor and successor manifests, controller idempotency, rollout/scheduling calculations, failure evidence, and honest claim boundaries.
