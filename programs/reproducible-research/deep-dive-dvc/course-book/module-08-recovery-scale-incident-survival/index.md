# Module 08: Recovery, Scale, and Incident Survival

Module 08 treats time as part of the reproducibility system.

A repository can be healthy today and still become unrecoverable later. Storage grows,
remotes move, credentials rotate, CI images drift, maintainers leave, and old states become
harder to interpret. None of that is exceptional. It is normal system life.

This module is about long-lived trust:

- which states must remain recoverable
- which states can expire
- when cleanup is safe
- how remote migration preserves evidence
- how CI and maintainer handoffs survive time
- how incidents are handled without improvising the state story

The central learner question is:

> If local cache, local memory, or one storage provider disappeared, which results could
> still be restored and defended?

If the answer is unclear, the repository may be tidy today but not durable.

The capstone corroboration surface for this module is the set of files and commands that
make recovery and long-lived state visible: `capstone/dvc.lock`,
`capstone/publish/v1/manifest.json`, `capstone/docs/RECOVERY_GUIDE.md`,
`capstone/docs/STATE_LAYER_GUIDE.md`, `capstone/docs/RELEASE_REVIEW_GUIDE.md`, and the
`make -C capstone recovery-review` route.

## Why this module exists

Reproducibility is not a setup achievement.

Long-lived workflows fail through ordinary pressure:

- old artifacts are deleted because storage feels expensive
- nobody knows which releases must remain restorable
- `dvc gc` is run without understanding what it can remove
- a remote migration copies recent objects but misses older release evidence
- CI images update and results drift
- the only person who knew the recovery route leaves the team

These are design problems. The point of Module 08 is to make them discussable before they
become incidents.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: durability boundaries"]
  core1 --> core2["Core 2: retention policy"]
  core2 --> core3["Core 3: cleanup and cache safety"]
  core3 --> core4["Core 4: migration and CI drift"]
  core4 --> core5["Core 5: incident response and handoff"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order the first time.

If the problem is already partly clear, use this shortcut:

- open Core 1 when the main confusion is "what must survive local loss?"
- open Core 2 when the main confusion is "which history should we keep, and for how long?"
- open Core 3 when the main confusion is "when is cleanup safe?"
- open Core 4 when the main confusion is "how do remotes or CI change over time?"
- open Core 5 when the main confusion is "how should we respond when recovery is needed?"

## Module map

| Page | Purpose |
| --- | --- |
| `index.md` | explains the module promise and study route |
| `durability-boundaries-and-recovery-goals.md` | teaches what must survive local cache loss and maintainer turnover |
| `retention-policy-and-history-value.md` | teaches how to decide which historical states deserve durable recovery |
| `garbage-collection-and-cache-safety.md` | teaches cleanup discipline around `dvc gc` and cache removal |
| `remote-migration-and-ci-drift.md` | teaches remote transitions and CI drift as long-lived system risks |
| `incident-response-and-maintainer-handoffs.md` | teaches incident response and knowledge continuity |
| `worked-example-restoring-after-local-cache-loss.md` | walks through one realistic recovery check |
| `exercises.md` | gives five mastery exercises |
| `exercise-answers.md` | explains model answers and review logic |
| `glossary.md` | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- what state must survive local cache loss
- how retention policy differs across release, audit, operational, and exploratory states
- why cleanup can be destructive when references and remotes are misunderstood
- how remote migration can preserve or break historical continuity
- why CI drift and maintainer turnover belong in the recovery model
- how an incident response route protects evidence before repair

## Commands to keep close

These commands form the evidence loop for Module 08:

```bash
make -C capstone recovery-review
make -C capstone state-summary
make -C capstone release-audit
dvc pull
dvc status
dvc gc --dry-run
```

Use the `make` routes for the course-provided capstone review. Treat `dvc gc --dry-run` as
a planning command, not permission to delete anything.

## Capstone route

Use the capstone after you can name what needs to survive.

Best corroboration surfaces for this module:

- `capstone/dvc.lock`
- `capstone/publish/v1/manifest.json`
- `capstone/publish/v1/metrics.json`
- `capstone/publish/v1/params.yaml`
- `capstone/docs/RECOVERY_GUIDE.md`
- `capstone/docs/STATE_LAYER_GUIDE.md`
- `capstone/docs/PUBLISH_CONTRACT.md`

Useful proof route:

```bash
make -C capstone state-summary
make -C capstone recovery-review
make -C capstone release-audit
```

The point of that route is not to admire a clean repository. It is to ask whether the
state that matters can still be found, restored, checked, and explained after ordinary
time pressure.
