# Completion Rubric

Deep Dive Snakemake should end with more than syntax familiarity. Use this rubric to
judge whether you can reason about workflow truth, dynamic behavior, policy boundaries,
and publish contracts without hand-waving.

## Completion standard

You should be able to do all of the following:

- explain why a workflow reruns with evidence rather than intuition
- distinguish rule semantics from profile or executor policy
- describe what a checkpoint may discover and what it must never hide
- identify which outputs are internal versus safe for downstream trust
- explain which artifacts another reviewer should inspect before approving change
- complete all one hundred exercises and retain the requested evidence

## Course outcomes

| Area | Completion signal |
| --- | --- |
| file contracts | you can explain which paths are explicit contracts and why they matter |
| dynamic DAG behavior | you can describe the checkpoint boundary and its evidence surfaces clearly |
| operational policy | you can show which profile changes are safe and which would leak into semantics |
| publish boundaries | you can defend the public file API and the promoted evidence bundle |
| stewardship | you can review the workflow for drift, risk, and migration pressure |

## Exercise evidence

Reading every page does not satisfy the course contract. A complete portfolio includes:

- ten exercises from each of the ten teaching modules
- runnable workflow files where implementation was requested
- dry-runs, logs, graphs, manifests, comparisons, or review notes named by each exercise
- corrections recorded after comparing your work with the model answers
- one final stewardship review that connects Modules 01-10

## Completion versus recognition

You are not done if you can only:

- recognize the term after seeing it
- rerun the same commands mechanically
- quote the answer page without naming the evidence
- pass through the capstone without explaining why a route was proportionate

Completion means you can transfer the idea to a fresh workflow question.

## Minimum capstone evidence

Use these proof routes as the minimum capstone evidence:

1. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough`
2. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour`
3. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-artifacts`
4. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm`

You are not done if you ran them mechanically but cannot explain what each one proved.

## Reviewer questions

A reviewer should be able to ask:

- what this workflow claims to build
- what dynamic discovery is allowed to do here
- what is public for downstream trust
- what changed when moving between local and CI policy
- what would you inspect first before migration

If those answers stay vague, you are not done yet.

## Best use of this page

Use this rubric at three moments:

1. after a module when you think you are ready to move on
2. after a capstone route when you want to know what it actually proved
3. at the end of the course when you want to separate real command from surface familiarity
