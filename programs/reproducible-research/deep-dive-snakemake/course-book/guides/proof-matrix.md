# Proof Matrix

Use this page when you care about a claim but want the fastest honest evidence route. A
good proof route is not the longest one. It is the one that answers the claim directly
with the least extra machinery.

This page is for claim-to-command routing.

## The question this page answers

This page helps with a narrower question than [Proof Ladder](proof-ladder.md):

> Given this claim, what command and file surfaces should I inspect first?

If you still do not know how strong the route should be, keep the ladder open beside this
page.

## How to use this matrix

Work in this order:

1. phrase the claim as something that could be false
2. find the matching claim family
3. start with the listed first command
4. inspect the listed file surfaces
5. stop unless the claim is still genuinely underdetermined

If the claim is still too broad, sharpen the claim before you choose a command.

## Start by phrasing the claim honestly

Weak proof questions sound like this:

- what should I run
- what is the best proof route
- what command is safest

Stronger proof questions sound like this:

- the capstone has a bounded first-pass route
- profiles change policy without changing workflow meaning
- the publish bundle can defend itself after execution

Once the claim can be false, the matrix becomes much easier to use well.

## Workflow-understanding claims

| Claim | Best first command | File surfaces to inspect | Why this is enough first |
| --- | --- | --- | --- |
| the capstone has a bounded first-pass reading route | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `course-book/capstone/index.md`, `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/` | first-pass orientation should begin with the guided route, not a full run |
| the workflow exposes its public rule surface clearly | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `capstone/Snakefile`, `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/list-rules.txt` | a walkthrough plus the rule list usually answers public-surface questions without executing everything |
| dynamic discovery becomes explicit evidence instead of a hidden side effect | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `capstone/results/discovered_samples.json`, `capstone/publish/v1/discovered_samples.json` | discovery needs an executed story plus the artifact that records what was found |
| promoted outputs are smaller than the full internal repository state | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `capstone/publish/v1/`, `capstone/results/`, [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) | the tour makes the contrast between internal run state and published contract visible |

## Execution and policy claims

| Claim | Best first command | File surfaces to inspect | Why this is enough first |
| --- | --- | --- | --- |
| profiles change execution policy without changing workflow meaning | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-context-invariance-audit` | `capstone/repro/context-invariance/`, `capstone/scripts/audit_context_invariance.py`, generated plans and artifacts | the paired audit proves preservation and reproduces path and sample leaks |
| the workflow validates configuration before execution | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-validate-config` | `capstone/config/config.yaml`, `capstone/config/schema.yaml` | validation claims should start at the schema and config surface, not a later run |
| the workflow can explain its plan before a run | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/dryrun.txt`, `capstone/workflow/rules/` | dry-run evidence is the honest first surface for plan questions |
| workflow incidents can be reviewed with narrower evidence than a full rewrite | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-selftest` or `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `capstone/tests/selftest.sh`, `capstone/logs/`, `artifacts/tour/reproducible-research/deep-dive-snakemake/` | incident review should begin with the narrowest reproducible surface |

## Publish and stewardship claims

| Claim | Best first command | File surfaces to inspect | Why this is enough first |
| --- | --- | --- | --- |
| the publish bundle can defend itself after execution | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-artifacts` | `capstone/publish/v1/manifest.json`, `capstone/publish/v1/provenance.json` | manifest and provenance review is the first honest publish-defense route |
| the publish boundary is reviewable as a durable contract | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md), `artifacts/proof/reproducible-research/deep-dive-snakemake/verify/` | contract questions need saved evidence, not just terminal output |
| the executed workflow tour is reviewable as evidence | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `artifacts/tour/reproducible-research/deep-dive-snakemake/`, [Capstone Proof Guide](../capstone/capstone-proof-guide.md) | the tour gives one executable workflow story without widening into stewardship |
| the repository can prove itself through one stronger end-to-end route | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` | `capstone/Makefile`, `capstone/tests/` | this is appropriate only when the claim is explicitly strong |

## Start with the question you actually have

| Question | Best first command | Best first file surface |
| --- | --- | --- |
| where should a first-time reader start in the capstone | `capstone-walkthrough` | `course-book/capstone/index.md` |
| what does this workflow claim it will build | `capstone-wf-dryrun` | `capstone/Snakefile` |
| what exactly is public for downstream trust | `capstone-verify-artifacts` | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |
| which surface explains dynamic discovery honestly | `capstone-tour` | `capstone/workflow/rules/preprocess.smk` |
| what would I inspect before migration | `capstone-confirm` | `course-book/capstone/index.md` |

## One honest matrix decision

Suppose your question is:

> Which surface explains dynamic discovery honestly?

The matrix should send you to `capstone-tour` plus the discovery artifacts, not to a full
stewardship route. That is the whole discipline this page is teaching: route the claim to
the smallest surfaces that actually own it.

## Good stopping point

Stop when you can say:

- which claim family matched your question
- which command was the first honest falsifier
- which files actually carried the proof

If you still cannot say those three things, the problem is usually the claim, not the
command.

## Companion pages

- [Proof Ladder](proof-ladder.md) when route strength is still unclear
- [Command Guide](../capstone/command-guide.md) when the command layer itself is unclear
- [Capstone File Guide](../capstone/capstone-file-guide.md) when the right file surface
  is still unclear
- [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) when publish
  trust is the central question
