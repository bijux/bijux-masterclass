# Failure Modes, Recovery, and Trust


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Data Identity Content Addressing"]
  page["Failure Modes, Recovery, and Trust"]
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

Identity matters because failure eventually arrives.

Module 02 is not finished when you can explain hashes in the abstract. It is finished when
you can explain what a broken recovery or identity story actually means.

## What good recovery is proving

When a DVC repository restores tracked content after loss, it is proving something narrow
but important:

- the tracked identity was recorded
- the durable storage layer still has the content
- the workspace can be rebuilt from that recorded state

That is a strong claim.

It is not the same as proving every part of the project is correct or complete.

## Common failure questions

When recovery or identity seems broken, ask:

1. which layer is missing or inconsistent
2. whether the content identity was recorded but not stored durably
3. whether the workspace is out of sync with recorded state
4. whether a published artifact is being confused with full repository state

This keeps the diagnosis grounded.

## A practical failure table

| Symptom | Likely meaning |
| --- | --- |
| tracked file is missing after checkout | cache may not contain the needed content |
| `pull` cannot restore an object | remote durability is incomplete or misconfigured |
| local file exists but hash or identity does not match expectations | workspace drift or external modification occurred |
| published bundle exists but full repository state cannot be rebuilt | published trust and recovery durability are being confused |

These are not random operational annoyances. They are boundary clues.

## Diagnose with a layer ledger

Before repairing anything, record what survived:

| Surface | Present? | Evidence | What it permits you to claim |
| --- | --- | --- | --- |
| pointer | yes or no | parsed content ID, size, path | expected identity is recorded |
| workspace | yes or no | file and digest | bytes are visible locally |
| cache object | yes or no | object path and digest | local restoration is possible |
| configured remote | yes or no | remote config | a recovery source is named |
| remote object | unknown until tested | empty-cache pull | off-machine restoration works |

Configuration is not availability evidence. A remote name in `.dvc/config` tells you where
DVC will look, not whether the required object is there.

## Interpret the pointer-only case

The identity audit deliberately creates this state:

```text
pointer:   present
workspace: absent
cache:     absent
remote:    absent
```

The pointer still contains a valid content ID. `dvc checkout` fails and leaves the
workspace absent.

Classify the incident precisely:

- identity metadata is available
- content bytes are unavailable
- local recovery is impossible from the inspected layers
- the audit itself is working because it preserves the failure receipt

Do not “repair” the demonstration by regenerating arbitrary bytes at the same path. New
bytes would produce a new identity and conceal the unavailable object.

## Distinguish three failure classes

| Failure class | Typical evidence | Correct next question |
| --- | --- | --- |
| projection failure | pointer and cache exist, workspace absent or drifted | can checkout reconstruct the workspace? |
| availability failure | pointer exists, cache and remote cannot supply object | where is a verified copy of this content ID? |
| identity disagreement | workspace digest does not match pointer identity | which bytes are authoritative, and why? |

These classes need different responses. Running pull for an identity disagreement may
overwrite local evidence. Running add for an availability failure records whatever bytes
happen to be nearby as a new identity.

## Build a bounded recovery argument

Use four linked claims:

1. **Recorded identity:** the pointer names content ID `X`.
2. **Tested loss:** the workspace and local cache copies were removed.
3. **Recovery source:** pull retrieved `X` from the configured remote.
4. **Verified result:** the restored workspace and cache bytes match the original digest.

The audit's `REMOTE_RESTORES_AFTER_CACHE_LOSS` and
`REMOTE_RECOVERY_PRESERVES_IDENTITY` rows cover the last two claims. The push receipt
alone covers neither.

## Preserve negative evidence

Expected failures should remain reviewable. For the pointer-only case, keep:

- command and working directory
- nonzero return code
- stderr
- pointer content ID
- assertions that workspace and cache stayed absent

Without that packet, “checkout failed” cannot distinguish a missing object from a malformed
command, permission error, or broken DVC installation.

## A small recovery picture

```mermaid
flowchart LR
  loss["local loss"] --> remote["remote still has tracked content"]
  remote --> pull["dvc pull restores cache"]
  pull --> checkout["dvc checkout rebuilds workspace"]
  checkout --> verify["verify what was restored and what was not"]
```

The last step matters just as much as the restoration commands.

## Why verification still matters after recovery

A restored file in the workspace is not automatically the whole trust story.

You still need to ask:

- did we restore the tracked content we expected
- what layer is authoritative for that claim
- is the published contract still valid after restore

This is why the capstone's recovery route includes review artifacts and not only commands.

## A small example

Suppose you delete local tracked data and then use the remote-backed recovery route.

Strong explanation:

> the repository restored the tracked content from remote to cache and rebuilt the
> workspace from that content. This proves the durable recovery path for tracked artifacts
> is working.

Too-strong explanation:

> everything about the project is now fully recovered.

The second statement overreaches. Recovery is powerful, but it still has a scope.

## Two confusions to avoid

### Confusing published release state with full recovery state

`publish/v1/` may be enough for downstream trust, but it is not the full internal
repository state. A published bundle can remain valid while broader repository recovery is
still a separate question.

### Confusing local convenience with durable truth

If a file still happens to exist on disk, that does not prove the remote story is sound.

Recovery discipline is about surviving loss, not merely about noticing that the workspace
is currently populated.

## What a healthy recovery review sounds like

Good review language sounds like this:

> The remote-backed recovery route successfully restored tracked content and allowed the
> workspace to be rebuilt. The publish bundle also verified after restore. This proves the
> tracked artifact durability story is working for those surfaces.

That sentence is strong because it says what was proven and stops there.

## Keep this standard

Whenever a recovery story sounds vague, ask:

- what exactly was restored
- from which layer
- into which layer
- what evidence confirms the result

Those questions keep Module 02 grounded in trust rather than in command mythology.
