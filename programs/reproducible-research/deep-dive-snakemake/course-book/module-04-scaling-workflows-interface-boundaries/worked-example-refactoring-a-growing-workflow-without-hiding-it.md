# Worked Example: Refactoring a Growing Workflow Without Hiding It

This file ties the whole module together around one realistic problem:

> a workflow still works, but every new rule makes the repository harder to review, teach, and change safely.

The question is not "how do we create more files?" The question is how to make growth
land in named places without hiding the graph.

## The lab route

Work through the example in this order:

1. name the current rule families that already exist implicitly
2. split one concern into `workflow/rules/` without weakening the entrypoint
3. decide whether one candidate boundary is only an include or a true module
4. document the public file contract the refactor must preserve
5. finish by choosing gates that prove the new structure still tells the truth

## The starting situation

Assume the repository already has:

- truthful rule contracts from Module 01
- disciplined dynamic discovery from Module 02
- explicit production policy from Module 03

What it does not yet have is a calm scaling story.

The maintainers currently live with:

- one `Snakefile` that mixes preprocessing, summarization, and publishing
- helper path logic and structural logic in the same place
- no clear public-versus-internal path note
- CI checks that run, but do not clearly defend any structural claim

That is a good Module 04 starting point because the workflow is not broken. It is merely
becoming exhausting to explain.

## Start with ownership, not abstraction

The first repair is a rule-family split, not a module promotion.

Read the large file and write one sentence of ownership for each cluster of rules. A
useful early outcome might look like this:

```text
workflow/rules/
  preprocess.smk
  summarize_report.smk
  publish.smk
```

Each file now owns one coherent concern:

- `preprocess.smk` prepares declared working data
- `summarize_report.smk` turns processed data into public summaries and report inputs
- `publish.smk` assembles and verifies the downstream contract

The repository improves because a reviewer can explain each boundary quickly, not because
the file count increased.

## Keep the entrypoint short and honest

The top-level `Snakefile` should still reveal orchestration:

```python
configfile: "config/config.yaml"

include: "workflow/rules/preprocess.smk"
include: "workflow/rules/summarize_report.smk"
include: "workflow/rules/publish.smk"

rule all:
    input:
        "publish/v1/manifest.json"
```

This entrypoint still answers the most important questions:

- where configuration starts
- which major rule families exist
- what final contract the workflow promises

If the entrypoint becomes a maze of indirection, the split has already gone too far.

Capture evidence immediately:

```sh
snakemake --list-rules
snakemake --rulegraph mermaid-js > rulegraph.mmd
snakemake -n
```

The structural refactor is not successful unless those surfaces still tell the same
workflow story.

## Promote only a real reusable boundary

Now inspect one candidate concern more closely.

Suppose the repository has a QC bundle used by two entrypoints. That *might* deserve
`workflow/modules/`, but only if the interface is explicit:

- named inputs
- named outputs
- parameters that callers can understand
- software and config assumptions

If the candidate still reaches into top-level globals, undeclared path conventions, or
shared hidden helpers, it is not ready.

That is the key distinction:

- includes group one graph by ownership
- modules expose a reusable boundary with an interface

Do not promote a module just because a file is long.

## Write the public contract before the gate

The refactor is still incomplete if another engineer cannot answer which files are safe
for consumers.

So add or strengthen a contract note such as `FILE_API.md`:

| Path | Stability | Meaning |
| --- | --- | --- |
| `publish/v1/manifest.json` | public | inventory and checksums for the published bundle |
| `publish/v1/summary.json` | public | machine-readable summary with a defined schema |
| `results/staged/` | internal | rebuildable intermediate state with no compatibility promise |
| `.snakemake/` | engine state | private execution metadata |

This step matters because public trust should live in a small documented surface, not in
whoever happens to know the directory tree best.

## Add gates that defend the claim you just made

Only now should you tighten validation.

After the split, different questions need different proof routes:

- does the visible graph still make sense
- does the public file contract still verify
- did the plan for the final target remain stable

That usually leads to a gate set like this:

- `snakemake --list-rules` or rulegraph review for architecture visibility
- `snakemake -n` for target planning
- targeted schema or file-contract validation for public paths
- `snakemake --lint` for design smells that the split exposed

This is the difference between a meaningful gate and generic CI noise.

## Keep resource assumptions portable

One last review often appears during scaling: some rule families are heavier than others.

Keep that distinction visible, but keep executor policy out of the rules. The repository
should be able to say:

- which concern is heavier
- which resource declarations belong to the workflow
- which cluster or local mapping belongs to operating policy

If a rule hardcodes scheduler commands or node names, the structural cleanup has created a
new portability problem.

## The repaired scaling story

By the end of the refactor, the workflow can be described cleanly:

1. top-level orchestration stays visible
2. rule families are grouped by named ownership
3. only genuine interfaces become modules
4. public paths are documented separately from internal state
5. gates defend the structural promises the repository actually makes

That is what it means to refactor a growing workflow without hiding it.

## Review questions for the repaired design

When you inspect a repository shaped like this, ask:

1. which split clarifies ownership and which only creates indirection
2. where is the public contract documented
3. which boundary, if broken, would fail first through validation
4. which candidate module still depends on hidden globals
5. how will the next growth change land without making the graph harder to teach

If those answers are visible, the module’s scaling story has landed.
