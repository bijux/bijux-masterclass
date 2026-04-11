# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning keeps durability, retention, cleanup, and incident
evidence connected.

## Answer 1: Name the durability boundary

Strong recovery goal:

> The release `v1` manifest, metrics, parameters, lock evidence, and DVC-tracked model
> output must survive local cache loss. A maintainer should be able to restore required
> objects from the shared remote and run the recovery and release review routes from a
> clean checkout.

Useful checks:

```bash
dvc pull
dvc status
make -C capstone recovery-review
make -C capstone release-audit
```

The main lesson is that local cache is not the authority for release recovery.

## Answer 2: Classify retention value

Promoted release artifact:

- protected, because downstream readers, rollback, and audit may depend on it

Current mainline training data:

- protected or strongly retained, because collaborators and CI need it for current work

Abandoned exploratory candidate output:

- bounded-retention or discard after review, because it no longer supports a decision

Published analysis dataset:

- protected or policy-driven retention, because publication or stakeholder evidence may depend on it

Temporary local debug report:

- safe to discard after review, unless it became incident evidence

The main lesson is that retention follows value and obligation, not age alone.

## Answer 3: Review a cleanup request

Strong response:

> Before approving `dvc gc --all-branches`, I need a dry run, confirmation of which
> references are protected by that scope, evidence that required release and current
> mainline objects are present in the shared remote, and a retention-policy check showing
> the proposed deletions do not remove recoverable states we still promise to support.

Useful first commands:

```bash
dvc status
dvc push
dvc gc --all-branches --dry-run
```

The exact command depends on the repository. The main lesson is that cleanup needs a
reviewable deletion scope before execution.

## Answer 4: Plan a remote migration check

Strong migration check:

1. Inventory protected states: current mainline, releases, audit or publication bundles.
2. Add the new remote or destination prefix.
3. Push or copy required objects according to retention policy.
4. Verify from a clean checkout using the new remote.
5. Run recovery and release review routes.
6. Cut over only after verification passes.
7. Keep a rollback route until the old remote can be retired safely.

The main lesson is that migration is about continuity of recoverability, not only changing
a remote URL.

## Answer 5: Write an incident note

Strong incident note:

> CI metrics changed after the base image update, so the executor changed as part of the
> evidence surface. Before accepting the new results, compare dependency and tool versions,
> rerun the recovery and metric review routes, and decide whether the movement is expected
> runtime drift or a workflow regression. Update CI image documentation and release notes
> if the executor change affects metric interpretation.

The main lesson is that CI is not background. It is part of the reproducibility evidence.

## Self-check

If your answers consistently explain:

- which state must survive local loss
- why retention value differs by state
- how cleanup can be reviewed safely
- how remote and CI changes affect recovery
- how incident notes preserve failure, repair, and verification

then you are using Module 08 correctly.
