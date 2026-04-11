# Module 10: Migration, Governance, and DVC Boundaries

Module 10 turns the course into a stewardship method.

The earlier modules teach individual contracts: data identity, environment evidence,
truthful pipelines, meaningful metrics, controlled experiments, collaboration, recovery,
and promotion. The final module asks whether a learner can review a real repository and
make deliberate changes without breaking those contracts.

This module is about mature judgment:

- how to review a DVC repository without wishful thinking
- how to migrate one state boundary safely
- how to write lightweight governance that people can follow
- how to identify recurring DVC anti-patterns before they become culture
- how to decide what DVC should own and what belongs to another layer

The central learner question is:

> Which state contracts are broken, underspecified, or assigned to the wrong tool?

If that answer stays vague, future improvements will become accidental rewrites.

The capstone corroboration surface for this module is the full project review route:
`capstone/dvc.yaml`, `capstone/dvc.lock`, `capstone/params.yaml`, `capstone/publish/v1/`,
`course-book/capstone-docs/architecture.md`, `course-book/capstone-docs/review-route-guide.md`,
`course-book/capstone-docs/recovery-guide.md`, and the `make -C capstone confirm` route.

## Why this module exists

The last skill is not another command.

It is being able to say:

- this state boundary is clear
- this one is fragile
- this migration plan preserves recovery
- this governance rule is worth enforcing
- this shortcut will become an anti-pattern
- this problem is not DVC's job

That judgment is what lets a repository improve without losing trust.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: repository review"]
  core1 --> core2["Core 2: migration safety"]
  core2 --> core3["Core 3: governance rules"]
  core3 --> core4["Core 4: anti-pattern review"]
  core4 --> core5["Core 5: DVC boundaries"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order the first time.

If the problem is already partly clear, use this shortcut:

- open Core 1 when the main confusion is "how do I review a repository honestly?"
- open Core 2 when the main confusion is "how do I move a state boundary safely?"
- open Core 3 when the main confusion is "which rules should stay after the course ends?"
- open Core 4 when the main confusion is "which shortcuts should I reject early?"
- open Core 5 when the main confusion is "what should DVC own, and what should another system own?"

## Module map

| Page | Purpose |
| --- | --- |
| `index.md` | explains the module promise and study route |
| `repository-review-without-wishful-thinking.md` | teaches an evidence-first review method |
| `safe-migration-plans-for-state-boundaries.md` | teaches migration planning that preserves trust |
| `governance-rules-for-long-lived-repositories.md` | teaches small durable rules for future changes |
| `anti-patterns-and-review-interventions.md` | teaches recurring DVC shortcuts and how to stop them |
| `dvc-tool-boundaries-and-system-ownership.md` | teaches where DVC should and should not be authoritative |
| `worked-example-reviewing-a-dvc-repository-for-stewardship.md` | walks through one final repository review |
| `exercises.md` | gives five mastery exercises |
| `exercise-answers.md` | explains model answers and review logic |
| `glossary.md` | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- how to review a DVC repository by evidence, not optimism
- how to plan one safe migration without breaking recovery or auditability
- how governance differs from process clutter
- how anti-patterns emerge from reasonable shortcuts
- when DVC is the right authority and when another layer should own the concern
- how to leave a repository with a concrete stewardship recommendation

## Commands to keep close

These commands form the evidence loop for Module 10:

```bash
make -C capstone confirm
make -C capstone release-audit
make -C capstone recovery-review
dvc status
dvc repro -n
```

Use the `make` routes for the course-provided capstone review. Use the DVC commands to
inspect whether proposed changes preserve the state contracts the repository already
claims.

## Capstone route

Use the capstone as a review specimen.

Best corroboration surfaces for this module:

- `capstone/dvc.yaml`
- `capstone/dvc.lock`
- `capstone/params.yaml`
- `capstone/publish/v1/`
- `course-book/capstone-docs/architecture.md`
- `course-book/capstone-docs/review-route-guide.md`
- `course-book/capstone-docs/recovery-guide.md`
- `capstone/Makefile`

Useful proof route:

```bash
make -C capstone confirm
make -C capstone recovery-review
make -C capstone release-audit
```

The point of that route is not to admire the capstone. It is to practice the final course
skill: reviewing state contracts, proposing safe changes, and knowing where DVC's authority
ends.
