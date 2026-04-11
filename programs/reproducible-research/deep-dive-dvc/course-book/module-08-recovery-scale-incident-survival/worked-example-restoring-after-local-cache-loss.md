# Worked Example: Restoring After Local Cache Loss


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Recovery Scale Incident Survival"]
  page["Worked Example: Restoring After Local Cache Loss"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

This example shows how Module 08 fits together when a workspace loses its local DVC
cache.

The goal is not to panic or manually recreate files. The goal is to prove whether the
state that matters can be restored from shared evidence.

## The situation

A maintainer deletes the local cache while cleaning disk space.

The workspace still has Git files:

- `dvc.lock`
- `params.yaml`
- `publish/v1/manifest.json`
- `publish/v1/metrics.json`
- `publish/v1/params.yaml`

But the local DVC objects are gone.

The recovery question is:

> Can the important state be restored from the shared remote and verified against the
> published evidence?

## Step 1: Stop guessing

Weak response:

> I can rebuild something similar from raw data.

Stronger response:

> First, restore the declared state from the remote and compare it with the manifest and
> lock evidence.

The second response protects the state story. Rebuilding by memory may create a similar
file while losing the evidence that it is the same state.

## Step 2: Pull from shared authority

The maintainer runs:

```bash
dvc pull
dvc status
```

If the pull succeeds, the shared remote has the objects required by the current workspace.

If the pull fails, the incident is now specific: important objects are missing from the
shared recovery boundary, or credentials and remote configuration are broken.

Either result teaches the team something real.

## Step 3: Verify the release boundary

The maintainer checks the published evidence:

```bash
make -C capstone recovery-review
make -C capstone release-audit
```

The important questions are:

- does the release manifest still describe the restored files?
- do metrics and parameters still match the promoted boundary?
- does the lock evidence still support the restored state?
- can another maintainer repeat the route?

Recovery is not only "files exist again." Recovery means the restored state can be
defended.

## Step 4: Decide whether this was expected cleanup or an incident

If the local cache was deleted but remote restore works, this may be ordinary maintenance.
The team should still confirm the recovery route is documented.

If remote restore fails, this is an incident or at least a durability gap. The next note
should say which boundary failed:

- missing remote object
- remote permission error
- stale remote configuration
- incomplete release manifest
- old state beyond retention policy

Naming the boundary keeps the repair focused.

## Step 5: Turn the finding into a stronger check

If the restore succeeded, the team may add a scheduled recovery check or onboarding drill.

If the restore failed, the team should repair the missing object, permission, or
documentation gap and then rerun the recovery route.

The output of the exercise is not only a restored cache. It is a better recovery contract.

## The review note you would want

> Local DVC cache was removed during disk cleanup. We restored required objects from the
> shared remote with `dvc pull`, confirmed `dvc status`, and ran the recovery and release
> review routes. The published manifest, metrics, and parameters still match the restored
> state. This confirms local cache loss is survivable for the current release boundary.

If restore failed, the note should name the missing boundary and repair instead.

## Why this is a mastery example

This one story exercises the whole module:

- Core 1: local cache was not treated as durable authority
- Core 2: the release boundary was treated as higher value than disposable local state
- Core 3: cleanup was judged by recoverability
- Core 4: remote availability became the key verification point
- Core 5: the recovery note preserved what happened and what now passes

The repository survived because the team restored evidence, not just files.
