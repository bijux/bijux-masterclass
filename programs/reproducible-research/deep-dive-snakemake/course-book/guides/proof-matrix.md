# Proof Matrix

Use this page when you care about a claim but want the fastest honest evidence route. A
good proof route is not the longest one. It is the one that answers the claim directly,
with the smallest amount of extra machinery.

## How to use the matrix

Read each row from left to right:

1. name the claim you want to test
2. start with the first command that can falsify it
3. inspect the listed file surfaces
4. stop unless the claim is still genuinely underdetermined

If you already know you need a stronger route, keep [Proof Ladder](proof-ladder.md)
open beside this page.

## Workflow understanding claims

| Claim | Best first command | File surfaces to inspect | Why this is enough first |
| --- | --- | --- | --- |
| the capstone has a bounded first-pass reading route | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `course-book/capstone/index.md`, `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/` | first-pass orientation should begin with the guided route, not a full run |
| the workflow exposes its public rule surface clearly | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `capstone/Snakefile`, `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/list-rules.txt` | a walkthrough plus rule list usually answers public-surface questions without executing everything |
| dynamic discovery becomes explicit evidence instead of a hidden side effect | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `capstone/results/discovered_samples.json`, `capstone/publish/v1/discovered_samples.json` | discovery needs an executed story plus the artifact that records what was found |
| promoted outputs are smaller than the full internal repository state | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md), `capstone/publish/v1/`, `capstone/results/` | the tour makes the contrast between internal run state and published contract visible |

## Execution and policy claims

| Claim | Best first command | File surfaces to inspect | Why this is enough first |
| --- | --- | --- | --- |
| profiles change execution policy without changing workflow meaning | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit` | `capstone/profiles/`, `capstone/Makefile` | profile audit is the smallest route that keeps policy differences visible |
| the workflow validates configuration before execution | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-validate-config` | `capstone/config/config.yaml`, `capstone/config/schema.yaml` | validation claims should start at the schema and config surface, not a later run |
| the workflow can explain its plan before a run | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/dryrun.txt`, `capstone/workflow/rules/` | dry-run evidence is the honest first surface for plan questions |
| workflow incidents can be reviewed with narrower evidence than a full rewrite | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-selftest` or `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `capstone/tests/selftest.sh`, `capstone/logs/`, `artifacts/tour/reproducible-research/deep-dive-snakemake/` | incident review should begin with the narrowest reproducing surface |

## Publish and stewardship claims

| Claim | Best first command | File surfaces to inspect | Why this is enough first |
| --- | --- | --- | --- |
| the publish bundle can defend itself after execution | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-artifacts` | `capstone/publish/v1/manifest.json`, `capstone/publish/v1/provenance.json` | manifest and provenance review is the first honest publish-defense route |
| the publish boundary is reviewable as a durable contract | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` | [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md), `artifacts/proof/reproducible-research/deep-dive-snakemake/verify/` | reviewable contract questions need saved evidence, not just terminal output |
| the executed workflow tour is reviewable as evidence | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `artifacts/tour/reproducible-research/deep-dive-snakemake/`, [`capstone-proof-guide.md`](../capstone/capstone-proof-guide.md) | the tour gives one executable workflow story without escalating to the strongest bundle |
| the repository can prove itself through one stronger end-to-end route | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` | `capstone/Makefile`, `capstone/tests/` | this is the appropriate first route only when the claim is explicitly strong |

## Start with the question you actually have

| Question | Best first command | Best first file |
| --- | --- | --- |
| where should a first-time reader start in the capstone | `capstone-walkthrough` | `course-book/capstone/index.md` |
| what does this workflow claim it will build | `capstone-wf-dryrun` | `capstone/Snakefile` |
| what exactly is public for downstream trust | `capstone-verify-artifacts` | [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md) |
| which surface explains dynamic discovery honestly | `capstone-tour` | `capstone/workflow/rules/preprocess.smk` |
| what would I inspect before migration | `capstone-confirm` | `course-book/capstone/index.md` |

## Best companion pages

- [Command Guide](../capstone/command-guide.md) when the command layer itself is unclear
- [Topic Boundaries](../reference/topic-boundaries.md) when the claim is crossing workflow and policy surfaces
- [Practice Map](../reference/practice-map.md) when you want to turn a proof route into rehearsal
- [Capstone File Guide](../capstone/capstone-file-guide.md) when the right file surface is still unclear
- [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) when publish trust is the central question
- [Capstone Proof Guide](../capstone/capstone-proof-guide.md) when you need the stronger corroboration route
