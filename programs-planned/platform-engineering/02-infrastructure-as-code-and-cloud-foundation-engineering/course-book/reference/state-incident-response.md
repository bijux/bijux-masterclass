# Reference — State Incident Response

State incidents are dangerous because the infrastructure can continue operating while the tool’s authority record becomes incomplete, stale, or ambiguous. The first response is to stop producing new state, not to force the system back into a green pipeline.

## Common symptoms

- lock cannot be acquired or appears abandoned;
- state lineage or serial differs from expectation;
- plan proposes mass creation or destruction without a matching design change;
- a remote resource exists but is absent from state;
- state references the wrong account, provider alias, workspace, or address;
- backend object was deleted, overwritten, or restored;
- apply failed after some remote operations succeeded;
- two pipelines report different plans for the same root;
- a manual `state` command was run without a complete transcript.

## Immediate containment

1. Stop all automated and human writers for the affected backend key.
2. Preserve current backend object, version history, and lock record.
3. Record active sessions and determine whether an original writer is still running.
4. Capture source commit, input digest, backend key, state lineage/serial, provider lock, account, region, and caller identity.
5. Do not run `force-unlock`, `state push`, broad import, or a new apply merely to make the pipeline proceed.

The goal is to prevent a second writer from converting ambiguity into corruption.

## Classify the incident

### Stale lock

The lock remains after the original process has definitely stopped. Evidence must establish the lock owner, process/session termination, backend key, lock ID, and absence of another writer. Force-unlock is appropriate only for the exact abandoned lock.

### Wrong backend or workspace

The operator initialized against a different key, account, or workspace. The safe response is to identify the authoritative key and restore correct configuration—not to merge histories by intuition.

### Partial apply

A provider created or changed an object, but a later operation or state write failed. Compare cloud audit/API evidence with state. Each unmatched object receives an explicit disposition: import/adopt, delete, or leave unmanaged with a named owner.

### Lost or overwritten state

Use backend version history and independent object inventory. Restore a candidate snapshot into a separate rehearsal key, refresh it, and compare planned actions. Never overwrite the authoritative key before the candidate has been evaluated.

### Wrong lineage

A snapshot belongs to another state history. Even when addresses look familiar, it must not be treated as a newer or older revision of the authoritative lineage. Determine whether it represents another environment, a copied bootstrap, or an accidental reinitialization.

### Address or provider migration failure

State may bind an object to an old address/provider alias after code moved. Prefer configuration-driven `moved` blocks and provider replacement mechanisms. Direct state surgery is a last resort with backup, exclusive lock, peer review, transcript, and rollback plan.

## Reconciliation table

Use one row per resource:

| Address intended | State object | Remote object | Evidence | Disposition |
|---|---|---|---|---|
| present | present | present | IDs match | keep |
| present | absent | present | audit event from failed apply | import after complete config |
| present | present | absent | provider confirms deletion | recreate or retire after review |
| absent | present | present | old module address | move/transfer/forget intentionally |
| absent | absent | present | unrelated or orphan | assign owner, import, or delete |

Do not infer identity solely from a resource name. Compare immutable provider identifiers and architecture context.

## Recovery sequence

A defensible recovery usually follows:

```text
freeze writers
→ preserve evidence
→ classify incident
→ restore candidate into isolated key if needed
→ refresh and reconcile
→ review one bounded repair
→ apply with one writer
→ verify data plane
→ document control failure
```

If direct state mutation is unavoidable:

- take a protected state backup;
- verify exclusive ownership of the lock;
- write exact before/after addresses and IDs;
- use the smallest possible command;
- retain the command transcript and state digests;
- recalculate a full plan afterward;
- validate the service outside state.

## Force-unlock decision

Before force-unlock, answer:

1. Which exact backend key and lock ID are affected?
2. Which identity owns the lock?
3. Is the original process definitely stopped?
4. Could another runner still be applying?
5. What remote changes may have completed?
6. Who approved unlocking?
7. Which reconciliation follows immediately?

Lock age alone is not sufficient. Long operations, stalled provider calls, and network partitions can produce old but active locks.

## What not to do

- do not disable locking to “get unstuck”;
- do not restore directly over authoritative state;
- do not push edited state without peer review and rollback evidence;
- do not rerun apply before identifying partially created resources;
- do not delete a remote object merely because state lacks it;
- do not call a clean plan proof that business behavior recovered.

## Close the incident

Closure requires:

- authoritative state lineage and serial recorded;
- no unexplained remote/state mismatches;
- one writer policy restored;
- data-plane checks passed;
- temporary imports or manual changes represented in configuration;
- recovery evidence protected;
- root cause and prevention recorded.

A recovered pipeline without an understood incident remains a latent state failure.
