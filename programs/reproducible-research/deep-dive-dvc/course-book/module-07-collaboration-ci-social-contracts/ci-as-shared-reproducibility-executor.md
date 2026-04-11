# CI as Shared Reproducibility Executor

Local success is useful, but it is not enough for team trust.

CI gives the team a shared executor: a place where the repository must prove itself
without the author's local cache, shell history, notebook state, or private files.

That is why CI matters in a DVC project. It is not only a way to run tests. It is a way to
ask whether a clean environment can recover and verify the declared state story.

## What CI should prove

A DVC-aware CI route should prove more than "Python imports."

It should answer:

- can the repository install the required tools?
- can required DVC objects be pulled from the configured remote?
- do `dvc.yaml`, `dvc.lock`, parameters, metrics, and outputs agree?
- can the verification route run without private local state?
- do release or review checks fail loudly when evidence is incomplete?

The exact commands vary by project, but the intent should be stable.

Example review route:

```bash
dvc pull
dvc status
dvc repro
dvc metrics show
```

The capstone may wrap these ideas behind `make -C capstone confirm` so you have one
course-level command to inspect.

## CI should fail for missing shared state

If a pull request updates DVC metadata but does not push the corresponding data, CI should
fail.

That failure is not annoying noise. It is the system protecting collaborators from a
broken state story.

Weak response:

> It works on my machine; CI probably does not have the data.

Stronger response:

> CI correctly found that the shared remote cannot reconstruct the declared state. Push
> the missing DVC objects or revise the change before merge.

The difference is important. CI is not the less-trusted executor. It is the shared proof
surface.

## Keep CI focused enough to be useful

CI does not need to rerun every expensive production workflow on every small change.

But it should include a meaningful route that catches broken collaboration contracts:

- missing remote objects
- inconsistent lock evidence
- undeclared output drift
- invalid release bundle shape
- broken recovery command
- metric or parameter evidence missing from a promotion review

If the full workflow is expensive, split checks by confidence level:

| Check | Purpose |
| --- | --- |
| fast metadata check | catch broken declarations quickly |
| remote pull check | prove shared objects exist |
| small reproducibility route | prove core graph can run cleanly |
| release audit route | prove promotion evidence is complete |
| scheduled recovery route | prove restoration still works |

This keeps CI practical without making it superficial.

## Local failures and CI failures mean different things

If local fails and CI passes, the local environment may be drifted.

If local passes and CI fails, the repository may depend on local state.

Neither result should be dismissed. But for merge trust, CI failure blocks the shared
contract because it proves another clean executor cannot verify the change yet.

That does not mean CI is always perfectly configured. It means CI failures deserve repair
or explicit explanation before merge.

## Review checkpoint

You understand this core when you can:

- explain why local success is not enough for collaboration
- name the DVC state CI should recover or verify
- treat missing remote data as a correct blocking failure
- design a practical verification route instead of an ornamental one
- explain why CI is part of the shared proof surface

CI is not a substitute for review. It is the part of review that does not rely on memory.
