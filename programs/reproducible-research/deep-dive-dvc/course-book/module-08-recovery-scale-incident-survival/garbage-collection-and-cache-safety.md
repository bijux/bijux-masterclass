# Garbage Collection and Cache Safety

Cleanup is not automatically safe because it makes the repository smaller.

In a DVC project, cleanup can remove the only local copy of an object. If the remote does
not contain that object, or if a historical reference still needs it, cleanup can damage
recoverability.

This is why Module 08 treats `dvc gc` as a recovery decision, not a tidying reflex.

## What cleanup can remove

DVC garbage collection removes objects that are not protected by the reference scope you
choose.

That scope matters.

Examples:

```bash
dvc gc --workspace --dry-run
dvc gc --all-branches --dry-run
dvc gc --all-commits --dry-run
```

These commands do not mean the same thing. They ask DVC to consider different sets of
references when deciding what is still needed.

The learner rule is:

> If you cannot explain the reference scope, you are not ready to delete.

## Dry run is a review surface

Use dry run output as evidence for review.

Before deletion, ask:

- which objects would be removed?
- are those objects needed by any protected release?
- are they present in the shared remote if recovery still matters?
- does retention policy allow removal?
- has another maintainer reviewed the deletion when release history is involved?

Dry run is not a formality. It is the place where the cleanup decision becomes visible.

## Local cleanup differs from remote cleanup

Removing local cache may be safe when shared remotes contain the objects that matter.

Removing remote objects is more serious because it can remove the recovery path for every
collaborator.

Treat remote deletion as a governed action:

- require clear retention policy
- verify protected release references
- document the deletion reason
- keep audit evidence when required
- rehearse restore for important states before cleanup

Local disk pressure is not enough reason to damage shared recoverability.

## A safe cleanup sequence

A cautious cleanup flow looks like:

```bash
dvc status
dvc push
dvc gc --all-branches --dry-run
```

Then review the proposed deletions against retention policy.

Only after that should deletion be considered:

```bash
dvc gc --all-branches
```

Even this example is not a universal recommendation. It shows the habit: inspect state,
ensure important objects are pushed, preview deletion, then act only with a clear scope.

## Cleanup should follow value, not age alone

Old does not always mean disposable.

A two-year-old release artifact may still matter more than yesterday's abandoned
experiment. A recent exploratory output may be safe to remove once the candidate was
discarded. Retention value should drive cleanup.

## Review checkpoint

You understand this core when you can:

- explain what reference scope a cleanup command uses
- treat dry run output as review evidence
- distinguish local cache cleanup from remote object deletion
- connect cleanup decisions to retention policy
- stop cleanup when release recovery would become unclear

Cleanup is maintenance only when recoverability remains intentional.
