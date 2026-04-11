<a id="top"></a>

# Capstone File Guide

Use this page when you know the repository is the right surface but do not yet know which
file owns the answer. The goal is to shorten the path from question to owning file.

## Start with the file that owns the question

| If the question is about... | Open this file first | Then open |
| --- | --- | --- |
| how the repository is assembled at the top level | `capstone/Snakefile` | `capstone/workflow/rules/common.smk` |
| how the workflow discovers and fans out sample work | `capstone/workflow/rules/preprocess.smk` | `capstone/publish/v1/discovered_samples.json` after execution |
| how publish artifacts are assembled and promoted | `capstone/workflow/rules/publish.smk` | `capstone/workflow/contracts/FILE_API.md` |
| how summary and report surfaces are produced | `capstone/workflow/rules/summarize_report.smk` | `capstone/publish/v1/summary.json` |
| what downstream users are allowed to trust | `capstone/workflow/contracts/FILE_API.md` | [Publish Review Guide](publish-review-guide.md) |
| where local, CI, and SLURM policy differ | `capstone/profiles/local/config.yaml` | `capstone/profiles/ci/config.yaml` and `capstone/profiles/slurm/config.yaml` |
| what learner-facing proof routes exist | `capstone/Makefile` | [Command Guide](command-guide.md) |
| where helper logic lives outside the rule files | `capstone/workflow/scripts/provenance.py` or `capstone/src/capstone/` | `capstone/environment.yaml` or `capstone/workflow/envs/` |
| how the repository is defended | `capstone/tests/` | [Capstone Review Worksheet](capstone-review-worksheet.md) |

[Back to top](#top)

## Directory responsibilities

| Path | What belongs there |
| --- | --- |
| `capstone/Snakefile` | top-level assembly and workflow entry |
| `capstone/workflow/rules/` | rule families with visible workflow meaning |
| `capstone/workflow/modules/` | reusable workflow boundaries with explicit interfaces |
| `capstone/workflow/contracts/` | published file-level contracts |
| `capstone/workflow/scripts/` | helper code that belongs beside orchestration |
| `capstone/src/capstone/` | reusable Python implementation code |
| `capstone/profiles/` | operating-policy differences across execution contexts |
| `capstone/tests/` | unit and workflow-level proof surfaces |
| `capstone/publish/v1/` | downstream-facing publish boundary |

[Back to top](#top)

## Good first reading order

If this is your first serious repository pass, use this sequence:

1. `capstone/Snakefile`
2. `capstone/workflow/rules/common.smk`
3. `capstone/workflow/rules/preprocess.smk`
4. `capstone/workflow/rules/summarize_report.smk`
5. `capstone/workflow/rules/publish.smk`
6. `capstone/workflow/contracts/FILE_API.md`
7. `capstone/Makefile`
8. one profile file
9. one test surface

That order keeps workflow meaning first, publish trust second, policy third, and proof
surfaces last.

[Back to top](#top)

## Wrong reading orders

Avoid these:

- opening helper Python code before reading the visible rule contract
- starting with `publish/v1/` before you know how the repository promotes files into it
- reading profiles before you know which workflow behavior must remain invariant
- using folder names as a substitute for ownership

If you are still navigating by directory names alone, the repository has not become
legible yet.

[Back to top](#top)
