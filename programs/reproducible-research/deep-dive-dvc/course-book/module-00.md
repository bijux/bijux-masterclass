<a id="top"></a>

# Deep Dive DVC: Program Outline

Deep Dive DVC is now a ten-module program that starts from first-contact reproducibility
thinking and ends with long-lived state stewardship. The through-line stays constant:

- **Stable identity**: data and artifacts are known by what they are, not only where they live.
- **Truthful state transitions**: pipelines, params, and experiments declare the real change surface.
- **Durable evidence**: metrics, manifests, locks, and publish bundles make claims reviewable.
- **Operational survival**: remotes, retention, recovery, and promotion keep state trustworthy over time.
- **Stewardship judgment**: teams know which state is authoritative and how to migrate it safely.

This repository contains both the program guide in `course-book/` and the executable DVC
reference repository in `capstone/`.

---

## Program Arc

### Module 01 — Why Reproducibility Fails

Start from the failure modes that push teams toward DVC in the first place: results that
cannot be defended, datasets that drift silently, and metrics that stop meaning what they
appear to mean.

**Deliverable:** a precise explanation of what problem DVC solves and what it does not solve by itself.

### Module 02 — Data Identity and Content Addressing

Learn why paths are only locators and why reproducibility starts with immutable,
content-addressed identity across workspace, cache, Git, and remote layers.

**Deliverable:** a repository that can distinguish location from identity and explain how a datum is recovered.

### Module 03 — Execution Environments as Inputs

Move beyond code and data alone. Environments, runtime assumptions, and tool versions
become part of the declared input surface rather than invisible luck.

**Deliverable:** a state story that includes the runtime boundary instead of hand-waving it away.

### Module 04 — Pipelines as Truthful DAGs

Turn DVC stages into honest state transitions. Dependencies, outputs, params, and lock
state become a reviewable graph rather than a convenient script wrapper.

**Deliverable:** a `dvc.yaml` pipeline whose stage behavior can be explained and defended under review.

### Module 05 — Metrics, Parameters, and Meaning

Treat numbers as semantic contracts, not just logged values. Parameters and metrics become
first-class state that preserve comparability across time.

**Deliverable:** a repository whose comparisons remain meaningful instead of only mechanically repeatable.

### Module 06 — Experiments Without Chaos

Formalize exploration as a controlled, reversible process. Experiments become comparable
deviations from a baseline rather than local folklore.

**Deliverable:** an experiment workflow that allows change without corrupting baseline history.

### Module 07 — Collaboration, CI, and Social Contracts

Make good behavior enforceable across humans. Reviews, remotes, CI gates, and promotion
habits become social contracts with technical backing.

**Deliverable:** a repository where another person can verify trustworthy state without private context.

### Module 08 — Production, Scale, and Incident Survival

Design for time as an adversary. Retention, garbage collection, cache loss, remote
migration, and recovery drills become part of the system instead of afterthoughts.

**Deliverable:** a repository that can survive time pressure and still restore authoritative state.

### Module 09 — Promotion, Registry Boundaries, Release Contracts, and Auditability

Separate exploratory state from promoted state. Publish surfaces, manifests, params,
metrics, and lock evidence become a defendable release contract for downstream users.

**Deliverable:** a promoted state bundle another reviewer or consumer can validate without guesswork.

### Module 10 — Mastery: Migration, Governance, Anti-Patterns, and DVC Tool Boundaries

Finish with stewardship judgment: reviewing real repositories, planning migrations,
setting governance rules, rejecting recurring anti-patterns, and deciding where DVC
should remain authoritative versus where another system should take over.

**Deliverable:** an evidence-based review and stewardship plan for a real DVC repository.

---

## Recommended Reading Path

1. Read Modules 01 to 10 in order.
2. Use the capstone lightly at first, then heavily from Modules 04 to 09.
3. Re-run proof commands as you go instead of trusting prose summaries.
4. Treat Module 10 as the finish of the program, not as optional appendix material.

If you are totally new to DVC, spend extra time in Modules 01 and 02 before rushing into
pipelines or experiments. If you already use DVC in production, Modules 07 to 10 will be
the fastest route to operational value.

---

## Capstone Relationship

The capstone is strongest as the executable companion to Modules 04 to 09, where truthful
pipelines, metrics, experiments, promotion, remotes, and recovery become concrete. The
early modules still benefit from smaller mental and local examples first so the learner
can understand state identity before the repository becomes the main teaching surface.

Use [Capstone Map](capstone-map.md) when you want one clear route from a module concept
to the exact repository files and proof command that demonstrate it.

**Proof command:**

```bash
make PROGRAM=reproducible-research/deep-dive-dvc test
```

Use the capstone to keep answering one question: when a result is challenged months later,
which exact state can the repository recover, compare, and prove?

[Back to top](#top)
