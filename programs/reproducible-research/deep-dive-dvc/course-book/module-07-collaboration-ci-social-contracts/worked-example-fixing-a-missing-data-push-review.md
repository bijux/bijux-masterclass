# Worked Example: Fixing a Missing Data Push Review

This example shows how Module 07 fits together when a pull request looks complete in Git
but cannot be restored by another maintainer.

The goal is not to scold the author. The goal is to repair the missing collaboration
contract.

## The situation

A pull request changes:

- `data/raw/service_incidents.csv.dvc`
- `dvc.lock`
- `metrics/metrics.json`

The author's local run passes. The metric movement looks reasonable. The reviewer starts
from a clean checkout and runs:

```bash
dvc pull
```

The pull fails because the DVC object referenced by the new metadata is not in the shared
remote.

This is the Module 07 failure:

> Git contains a state claim that the shared artifact store cannot satisfy.

## Step 1: Name the contract failure

Weak review response:

> CI is broken.

Stronger review response:

> The pull request changed DVC-tracked state, but the corresponding object is not
> available in the shared remote. Another maintainer cannot restore the declared state
> from a clean checkout, so this cannot merge yet.

That response names the missing contract instead of blaming the person or the tool.

## Step 2: Confirm the failure in CI

The team checks whether CI runs a remote-backed route.

If CI already runs:

```bash
dvc pull
dvc status
```

then CI should fail for the same reason. That is good. The shared executor caught a real
collaboration problem.

If CI does not run a remote-backed check, the team has found a second issue: the review
process relied on a human to notice missing shared data.

## Step 3: Repair the pull request

The author pushes the missing DVC object:

```bash
dvc push
```

Then the reviewer or CI retries from a clean state:

```bash
dvc pull
dvc status
make -C capstone confirm
```

The exact capstone route can vary, but the proof should be clean: another executor can
restore and verify the declared state without private local files.

## Step 4: Review the related evidence

The reviewer does not stop at "pull works now."

Because metrics changed, the reviewer also checks:

- does `dvc.lock` match the declared pipeline state?
- do metrics have matching parameter evidence?
- is the metric movement explained?
- does the release boundary need updates?
- does CI prove the same route another maintainer needs?

The original failure was missing data availability. The full review still needs the
normal DVC evidence chain.

## Step 5: Improve the contract

If the project did not already have a remote-backed CI check, the team adds one.

The new rule becomes:

> Pull requests that change DVC state must pass a clean verification route that pulls
> required objects from the shared remote.

That rule is better than "remember to push data" because it can fail visibly.

## The review note you would want

> This pull request updated DVC-tracked state, but the referenced object was missing from
> the shared remote, so a clean checkout could not restore the declared state. The author
> pushed the missing object, and the remote-backed verification route now succeeds. The
> review contract is that DVC state changes must be restorable by another maintainer or CI
> before merge.

That note is useful later because it records the failure mode and the repair.

## Why this is a mastery example

This one story exercises the whole module:

- Core 1: the issue was framed as a missing social contract
- Core 2: CI became the shared executor for the check
- Core 3: merge readiness depended on complete DVC evidence
- Core 4: the remote was treated as shared artifact infrastructure
- Core 5: clean-state restoration served as a small recovery rehearsal

The repository became stronger because the failure turned into an enforceable review
expectation.
