# Content Addressing, Cache, and Pointer Files


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Data Identity Content Addressing"]
  page["Content Addressing, Cache, and Pointer Files"]
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

Once paths stop being mistaken for identity, the next question becomes:

> how does DVC represent identity instead?

The answer is content addressing plus recorded references.

## The core claim

In DVC, two artifacts are treated as the same data when their content is the same.

That sounds simple, but it changes the whole trust model:

- renaming a file does not create a new identity
- moving a file does not create a new identity
- changing even one byte creates a different identity

This is much stronger than path-based naming conventions.

## The three pieces you need to understand

When you run `dvc add`, three ideas matter most:

1. DVC reads the content and computes a content-derived identifier
2. DVC stores the content in the cache
3. DVC records a small pointer file that refers to that identity

Those three pieces are enough for Module 02.

## What the pointer file is doing

A `.dvc` file is not the data itself.

It is a recorded claim about the data:

- which path in the workspace is being tracked
- which content-derived identity it points to
- what size or metadata is associated with that tracked artifact

That means Git can version the pointer while DVC manages the actual data identity and
recovery story.

## A practical picture

```mermaid
flowchart LR
  workspace["workspace file"] --> add["dvc add"]
  add --> pointer[".dvc pointer file"]
  add --> cache["content-addressed cache object"]
  pointer --> git["Git records the pointer"]
```

This diagram matters because it is easy to blur the pointer and the content together.

They are related, but they are not the same layer.

## A small example

Suppose you track `data/raw.csv` with DVC.

What matters most is not the exact cache path syntax.

What matters is:

- the workspace still has a file at `data/raw.csv`
- DVC now has a content-addressed cached copy
- a `.dvc` file now tells Git and the team which data identity the workspace path refers to

Once you see that, later recovery commands stop feeling magical.

## Why the cache matters

The cache is what makes identity reusable and restorable.

Without the cache, the pointer would be only a label.

With the cache, the recorded identity can be connected back to real bytes again.

That is why cache layout is not just a storage detail. It is part of how DVC turns an
identity claim into something operationally useful.

## Why this supports collaboration

Content addressing helps collaboration because:

- identical content does not need to be treated as unrelated just because it moved
- the system can reuse stored artifacts instead of duplicating them blindly
- teams can compare and recover data based on identity rather than on guesswork

This is one of the biggest reasons DVC is more than "Git for big files."

## Put the claim under pressure

Run the course's isolated identity audit from the repository root:

```bash
make -C programs/reproducible-research/deep-dive-dvc/capstone data-identity-audit
```

Open `summary.tsv`, then compare these generated cases:

- `workspace/same-content/`
- `workspace/changed-content/`

The first case adds identical bytes at two paths:

```text
data/observations.csv
archive/renamed.csv
```

The paths differ, but the `md5` fields in both `.dvc` pointers match. That is positive
evidence for content identity surviving relocation.

The second case appends one row to `data/observations.csv` and runs `dvc add` again. The
workspace path remains stable, but the pointer's `md5` changes. That is negative evidence
against path-based identity.

Read the cases as one causal contrast:

| What changed? | What stayed fixed? | Identity result |
| --- | --- | --- |
| path | bytes | same content ID |
| bytes | path | new content ID |

Either row alone is suggestive. Together they rule out the path as the cause of identity.

## Follow a pointer to bytes

In `workspace/pointer-cache/`, open `data/observations.csv.dvc`. Its output record contains
three fields that answer different questions:

| Field | Question answered |
| --- | --- |
| `path` | where should the workspace project the content? |
| `md5` | which managed content does the pointer name? |
| `size` | how many bytes should that content contain? |

The audit follows the `md5` into:

```text
.dvc/cache/files/md5/<first-two-characters>/<remaining-characters>
```

It then compares the cache object's bytes with the workspace file using SHA-256. This
second digest is not a replacement for DVC's identifier. It is an independent audit
check that the two inspected files contain equal bytes.

The resulting evidence chain is:

```mermaid
flowchart LR
  pointer["pointer: ID + size + path"] --> object["cache object named by ID"]
  object --> digest["independent byte comparison"]
  digest --> workspace["workspace projection matches"]
```

A pointer alone establishes only the first edge. Recovery requires accessible content at
the second edge.

## Separate identity from availability

The audit's `POINTER_ONLY_IS_NOT_RECOVERABLE` row deliberately preserves the `.dvc`
pointer while deleting both workspace and cache content. `dvc checkout` fails.

This is not contradictory:

- the pointer can still name the intended identity
- the content can still be unavailable from every configured storage layer

Use precise language:

> The identity reference remains intact, but the named bytes are unavailable.

Do not call the pointer corrupt merely because checkout fails. Do not call the data
recoverable merely because the pointer parses.

## Evidence checkpoint

Before moving on, answer from generated files rather than memory:

1. Which two pointer files prove that different paths can share one identity?
2. Which before-and-after pointer IDs prove that one path can name different content?
3. Which cache path is derived from the pointer's content ID?
4. Which receipt proves that metadata without accessible content cannot rebuild the
   workspace?

If you cannot identify all four surfaces, rerun the audit and follow `route.txt`.

## What this page is not claiming

This page is not claiming that content identity tells you whether the data is good,
meaningful, or scientifically valid.

It only tells you whether the system is talking about the same bytes.

That is a narrower claim, but it is a necessary one.

## Keep this standard

When teaching or reviewing DVC, avoid saying only:

> the file is tracked now.

Say something stronger:

> the workspace path now refers to a recorded content identity, and that identity can be
> recovered through DVC's cache and storage layers.

That is the level of precision Module 02 is trying to build.
