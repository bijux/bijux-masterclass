# Module 07: Collaboration, CI, and Social Contracts

Module 07 turns reproducibility from a single-person practice into a team contract.

By now, you know how a DVC project should represent data identity, runtime evidence,
pipeline truth, metric meaning, and controlled experiments. The next pressure is ordinary
collaboration: another person clones the repository, reviews a change, relies on CI, and
expects the same state story to hold without private context.

This module is about shared proof:

- what failures appear when more than one person touches the workflow
- what CI should verify instead of trusting memory
- what branch and review rules should block
- how DVC remotes become part of collaboration, not only storage
- how recovery drills turn "we can restore it" into evidence

The central question is:

> Can another maintainer verify the same result without knowing what happened on my
> laptop?

If the answer is no, the repository still depends on social memory instead of a durable
contract.

The capstone corroboration surface for this module is the set of shared verification and
remote-backed review routes: `capstone/Makefile`, `capstone/dvc.lock`,
`capstone/docs/review-route-guide.md`, `capstone/docs/recovery-guide.md`,
`capstone/docs/publish-contract.md`, and the `make -C capstone confirm` route.

## Why this module exists

Reproducibility often fails after the technical model is clear.

Common collaboration failures look familiar:

- a `.dvc` pointer or lockfile is merged but the data was never pushed
- a reviewer trusts a local result without a clean verification route
- CI checks formatting but not DVC state recovery
- a release bundle is promoted without the parameters and metrics needed for review
- a teammate can reproduce the code but not the data-backed result
- branch history is rewritten and nobody knows which artifacts still matter

These are not only human mistakes. They are missing contracts.

The point of Module 07 is not to add ceremony. The point is to decide which promises the
system should enforce because humans under pressure will forget them.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: collaboration failure modes"]
  core1 --> core2["Core 2: CI as shared executor"]
  core2 --> core3["Core 3: merge and branch contracts"]
  core3 --> core4["Core 4: remote stewardship"]
  core4 --> core5["Core 5: recovery and incident rehearsal"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order the first time.

If the problem is already partly clear, use this shortcut:

- open Core 1 when the main confusion is "why careful people are not enough"
- open Core 2 when the main confusion is "what CI should prove for DVC"
- open Core 3 when the main confusion is "what should block a merge"
- open Core 4 when the main confusion is "how remotes become team infrastructure"
- open Core 5 when the main confusion is "how do we know recovery will work?"

## Module map

| Page | Purpose |
| --- | --- |
| [Overview](index.md) | explains the module promise and study route |
| [Collaboration Failures and Social Contracts](collaboration-failures-and-social-contracts.md) | teaches how social failures become reproducibility failures |
| [CI as Shared Reproducibility Executor](ci-as-shared-reproducibility-executor.md) | teaches what CI should verify and why local success is not enough |
| [Merge Review and Branch Protection](merge-review-and-branch-protection.md) | teaches merge gates, branch rules, and review evidence |
| [DVC Remotes and Shared Artifact Stewardship](dvc-remotes-and-shared-artifact-stewardship.md) | teaches remote-backed collaboration and artifact stewardship |
| [Recovery Drills and Incident Readiness](recovery-drills-and-incident-readiness.md) | teaches recovery rehearsal and incident response as proof surfaces |
| [Worked Example: Fixing a Missing Data Push Review](worked-example-fixing-a-missing-data-push-review.md) | walks through one realistic collaboration failure and repair |
| [Exercises](exercises.md) | gives five mastery exercises |
| [Exercise Answers](exercise-answers.md) | explains model answers and review logic |
| [Glossary](glossary.md) | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- why careful teams still need enforceable reproducibility contracts
- what a DVC-aware CI route should verify
- which merge events should block until data and lock evidence are complete
- how DVC remotes support collaboration and recovery
- why recovery drills matter before an incident
- how to write review expectations that another maintainer can follow without private context

## Commands to keep close

These commands form the evidence loop for Module 07:

```bash
make -C capstone confirm
make -C capstone recovery-review
make -C capstone release-audit
dvc pull
dvc status
dvc repro
```

Use the `make` routes for the course-provided capstone review. Use the DVC commands inside
a workspace when checking whether another maintainer can restore, inspect, and reproduce
declared state.

## Capstone route

Use the capstone after you can name the collaboration failure being prevented.

Best corroboration surfaces for this module:

- `capstone/Makefile`
- `capstone/dvc.lock`
- `capstone/docs/review-route-guide.md`
- `capstone/docs/recovery-guide.md`
- `capstone/docs/publish-contract.md`
- `capstone/publish/v1/`

Useful proof route:

```bash
make -C capstone confirm
make -C capstone recovery-review
```

The point of that route is not to prove that one author can run the project locally. It is
to prove that the repository carries enough evidence for another maintainer to verify the
same state story.
