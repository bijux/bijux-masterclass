# Completion Rubric

Use this page when you think you are done with a module, a capstone route, or the course
as a whole. Deep Dive Snakemake should end with more than syntax familiarity or command
recognition. It should end with judgment you can transfer to a new workflow and defend in
review.

This rubric exists to slow down premature confidence.

## What completion means here

Completion in this course does not mean:

- you read every page
- you ran the largest capstone route once
- the examples looked familiar
- you can repeat course vocabulary

Completion means you can:

- explain the boundary in plain language
- name the failure that boundary is preventing
- choose a proof route that matches the claim
- transfer the same reasoning to a fresh workflow question

If one of those is missing, the idea is still forming.

## How to use this rubric

Use it in this order:

1. decide which scope you are testing
2. read the completion standard for that scope
3. compare your evidence against the stated bar
4. decide whether you have command or only recognition

Choose one scope only:

- one module
- one capstone route
- the whole course

If you try to assess everything at once, the conclusion will usually be vague.

## The course-wide completion standard

By the end of Deep Dive Snakemake, you should be able to do all of the following:

- explain why a workflow reruns from evidence rather than intuition
- distinguish workflow semantics from profile, executor, and storage policy
- describe what a checkpoint may discover and what it must never hide
- define which outputs are internal and which are safe for downstream trust
- explain which evidence another reviewer should inspect before approving change
- complete all one hundred exercises and retain the requested evidence
- review incident, architecture, publish, and migration questions without collapsing into
  taste

That is the real finish line.

## Start by separating completion from recognition

Recognition sounds like this:

- "I have seen this term before."
- "I know which command the page ran."
- "I can follow the capstone route if I keep the guide open."

Completion sounds like this:

- "I can explain what claim this route is testing."
- "I know which failure would appear if the contract were false."
- "I can choose a smaller proof route when the larger one would be theatrical."

If your confidence depends on the page staying open beside you, count that as partial
understanding rather than finished learning.

## Outcome areas

Use this table to diagnose where the completion gap still lives.

| Area | Completion signal | Common false positive |
| --- | --- | --- |
| file contracts | you can explain which paths are explicit contracts and why they matter | you can read the rule but still cannot explain why Snakemake reran it |
| dynamic DAG behavior | you can describe the checkpoint boundary and its evidence surfaces clearly | you can say "checkpoint" but still treat discovery as runtime magic |
| operational policy | you can show which profile changes are safe and which would leak into semantics | you assume a policy change is harmless because the workflow still runs |
| publish boundaries | you can defend the public file API and the promoted evidence bundle | you call a directory public because downstream users happen to look there |
| architecture and ownership | you can route the next change to the correct layer without guesswork | you can name folders but not their responsibilities |
| incidents and stewardship | you can choose evidence before editing and preserve trust through change | you jump to tuning or migration because it feels productive |

## Module-level completion

A module is complete when you can do four things:

1. explain its main boundary in plain language
2. name the failure that boundary is meant to prevent
3. choose one proportionate proof route
4. transfer the idea to a slightly different workflow question

That is why the course keeps insisting on prediction, observation, and explanation.

## Capstone-route completion

A capstone route is complete only if you can answer:

- what question the route was meant to settle
- why this route was proportionate instead of excessive
- what file, artifact, or report carried the real proof
- what the route did not prove

If you ran the route successfully but cannot answer those questions, the route counted as
activity, not corroboration.

## Exercise evidence

Reading alone does not satisfy the course contract. A complete learning record includes:

- ten exercises from each of the ten teaching modules
- runnable workflow files where implementation was requested
- dry-runs, logs, graphs, manifests, comparisons, or review notes named by the exercises
- corrections recorded after comparing your work with the model answers
- one final stewardship review that connects Modules 01 through 10

If the evidence named by the exercise is missing, the exercise is not fully complete.

## Minimum course evidence

At minimum, a course-complete learner should be able to point to:

1. beginner evidence of graph truth and rerun reasoning
2. discovery evidence that makes dynamic behavior reviewable
3. policy evidence separating semantics from execution context
4. publish evidence defining the downstream contract
5. architecture evidence clarifying ownership
6. incident or governance evidence showing late-course judgment

This course is not complete if all the evidence comes from only one part of the arc.

## A strong end-of-course question

Ask yourself this:

> If I inherit a new Snakemake repository tomorrow, which four surfaces would I inspect
> first, and why?

A strong answer will usually include:

- one workflow-truth surface
- one discovery or policy surface
- one publish or architecture surface
- one evidence or stewardship surface

If your answer collapses into stock phrases, you are not done yet.

## Minimum capstone evidence

These routes make a reasonable minimum capstone portfolio:

1. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough`
2. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour`
3. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-artifacts`
4. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm`

You are not done if you ran them mechanically but cannot explain what each one proved and
what each one left unsettled.

## Reviewer-standard questions

Another reviewer should be able to ask you:

- what this workflow claims to build
- what dynamic discovery is allowed to do here
- what is public for downstream trust
- what changed when moving between local and CI policy
- what would you inspect first before migration

If your answers stay vague, treat that as evidence that the completion bar is not met.

## Honest outcomes

At the end of this rubric, land on one of these conclusions:

- complete: I can explain, prove, and transfer the idea
- almost complete: I understand the concept but still need more evidence or transfer
- not complete: I recognize the material but cannot yet defend it independently

The middle conclusion is useful. It tells you where the next deliberate pass should go.
