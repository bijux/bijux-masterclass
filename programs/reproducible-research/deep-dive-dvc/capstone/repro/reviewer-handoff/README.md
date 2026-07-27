# Reviewer Handoff Specimen

This small DVC project asks whether a reviewer can recover and explain a result using only
tracked repository state and authorized read access to the shared remote.

The governed claim is:

> The selected incident sample contains four records, with a total severity of 11 and two
> weekend handoffs.

The `summarize_incidents` stage computes that claim from `data/incidents.csv`. The data
file and generated result are stored through DVC during the audit, while the pipeline
declaration, implementation, and handoff contract remain Git-tracked. This lets a clean
reviewer inspect the exact recorded result before deciding whether regeneration is needed.

## Handoff boundary

A complete handoff gives a reviewer:

- the Git repository
- read access to the configured DVC remote
- the commands in `handoff-contract.json`
- an expected result contract that explains what to inspect

It does not give the reviewer:

- the author's DVC cache
- untracked helper files
- private shell history
- write access as a prerequisite for verification

## Direct source inspection

Read these files in order:

1. `handoff-contract.json`
2. `dvc.yaml`
3. `scripts/summarize_incidents.py`
4. `data/incidents.csv`

The course audit creates isolated author, Git remote, DVC remote, and reviewer workspaces.
Do not initialize this source directory in place.
