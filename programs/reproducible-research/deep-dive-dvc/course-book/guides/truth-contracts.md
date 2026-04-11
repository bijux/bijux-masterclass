# Truth Contracts

Use this page when the main question is not "which DVC command exists?" but "what
exactly counts as truth here, and how would I prove it to another person?"

## Start with three questions

For every DVC repository question, answer these in order:

1. which layer is authoritative
2. what kind of change DVC will actually treat as meaningful
3. which file or command proves that claim

If you skip the first question, the later answers usually turn into folklore.

## Contract table

| Trust question | Authoritative layer | What counts as changed | Smallest honest proof route |
| --- | --- | --- | --- |
| did an input dataset change | the declared dependency in `dvc.yaml` plus the recorded hash in `dvc.lock` | the dependency content or declared target changed | inspect `dvc.yaml`, then compare `dvc.lock` or run `dvc status` |
| did a parameter change in a way the pipeline knows about | `params.yaml` plus the declared `params:` keys in `dvc.yaml` | only declared parameter keys affect stage change detection | inspect `params:` in `dvc.yaml`, then rerun or inspect `dvc.lock` |
| did a metric change in a reviewable way | the tracked metric file and the stage that produces it | the producing stage ran and wrote a new tracked metric artifact | inspect the metric file, then use `dvc metrics show` or the capstone verify route |
| can this experiment be compared honestly | the same declared deps, params, and outs contract as the baseline | only changes recorded through the declared comparison surface count | inspect declared params first, then use `dvc exp show` or the experiment-review bundle |
| can another person restore the tracked state after local loss | committed declarations plus the configured DVC remote | the remote still has the needed objects and the repository still declares them correctly | run the recovery drill and inspect the recovery review bundle |
| what may a downstream user trust | the promoted publish bundle and its manifest, not the whole repository | only promoted files and documented review meaning belong in the downstream contract | inspect `publish/v1/manifest.json` and the release review route |

## The most common misread

Changing a file does not automatically make it part of DVC's truth contract.

A parameter only becomes part of stage truth when it is declared under `params:` in
`dvc.yaml`. A metric only becomes a reviewable comparison surface when the repository says
what it means and where it comes from. A promoted file only becomes downstream-trustworthy
when the bundle documents why it belongs there.

That is why "the file changed" and "the repository is explicitly tracking that change" are
not the same claim.

## Minimal honest review loop

1. Read the declaration surface first, usually `dvc.yaml`.
2. Read the recorded surface next, usually `dvc.lock`.
3. Run one proof command such as `dvc status`, `dvc metrics show`, `dvc exp show`, or a capstone review route.
4. State what the evidence proves and what it still does not prove.

## Good review questions

- if this file changes, where is that dependency declared
- if this parameter changes, will DVC notice, or are we assuming it will
- if the workspace disappears, which layer restores it
- which proof route would I hand to another maintainer instead of narrating from memory
