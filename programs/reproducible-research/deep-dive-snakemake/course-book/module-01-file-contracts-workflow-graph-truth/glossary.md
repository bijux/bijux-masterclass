# Glossary

This glossary is part of the teaching material for Module 01, not a side appendix. Keep
it nearby while you work through the first lessons, the worked example, and the
exercises.

The point is simple: beginner confusion drops fast when the important workflow facts have
stable names. If you can name a problem precisely, you can usually fix it much faster.

## How to use this glossary

If a Snakemake explanation starts drifting into phrases like "it just runs that step" or
"the wildcard is weird," stop and look up the precise term that should replace that vague
phrase. Module 01 becomes much clearer when the nouns are stable.

## When to stop and check the glossary

Pause and check a term when:

- your explanation depends on "some file" instead of a named output contract
- you are using "job" and "rule" as if they mean the same thing
- you are treating a rerun cause and a failure symptom as the same thing
- you can tell a path design feels wrong but cannot yet name the ownership problem

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| ambiguity | A design situation where more than one rule can claim the same target path. |
| atomic publication | Writing to same-filesystem scratch and renaming only after success so readers see the prior trusted final or the new complete final. |
| config | Workflow data that changes what the workflow computes, such as samples, thresholds, or references. |
| convergence | The state where a successful run followed by `snakemake -n` reports nothing more to do for the current tracked workflow meaning. |
| file contract | The rule-level promise connecting declared inputs, declared outputs, and the action that produces those outputs. |
| hidden input | A real output influence that is not represented clearly as config, declared input files, or other intentional tracked workflow meaning. |
| output ownership | The question of which rule is responsible for publishing a given output path. |
| poison artifact | A final-looking output left behind by failure even though it is incomplete or untrustworthy. |
| profile | Execution policy for running the workflow, such as core count, retries, or latency behavior. |
| requested target | The concrete file path or default completion surface that Snakemake is asked to build. |
| rerun cause | The specific tracked or untracked reason a rule runs again or fails to rerun when it should. |
| rule all | The conventional rule that defines the normal finished output set for a workflow run. |
| rule graph | A structural view of rule relationships, as distinct from the concrete job DAG for one requested target set. |
| target surface | The set of outputs that define what "done" means for a normal invocation of the workflow. |
| wildcard binding | The act of matching a concrete filename against an output pattern and assigning values such as `sample = A`. |
| wildcard constraint | A regex restriction that narrows which filename shapes a wildcard may claim. |
| workflow meaning | The semantic content of what the workflow computes, as distinct from execution policy. |
| summary evidence | Output from commands such as `snakemake --summary` that helps explain which rules own which files and what state those files are in. |
| semantic freshness | Agreement between an output's stored meaning and the current values of every real influence on that output. |
| scratch path | An explicitly untrusted write location used before validation and promotion to the final path. |
| trusted final | The published path whose contents have completed the writer's required validation and promotion boundary. |
| under-rebuild | A defect where meaningful state changes but the declared graph does not schedule the work needed to refresh affected outputs. |

## The vocabulary standard for this module

When you explain a Module 01 situation, aim to say things like:

- "that rule is outside the current target surface"
- "the workflow fails to converge because the tracked meaning is unstable"
- "this is a wildcard ownership problem, not just a naming annoyance"
- "that setting belongs in config, not in execution policy"
- "the final path is a poison artifact because it was published before success"

Those sentences are much more useful than saying only "Snakemake is confusing."

## Confusion pairs worth fixing early

These pairs cause trouble on the first day because they sound similar but answer
different questions:

- `rule` versus `job`: a rule is the reusable pattern; a job is one concrete execution of
  that pattern after wildcards are bound.
- `config` versus `profile`: config changes workflow meaning; a profile changes how the
  workflow runs.
- `rerun cause` versus `failure symptom`: the symptom is what you noticed; the rerun cause
  is the specific tracked reason Snakemake decided work was needed again.
- `requested target` versus `rule all`: a requested target is what you asked Snakemake to
  build now; `rule all` is the repository's normal definition of done.
- `planner convergence` versus `semantic freshness`: a quiet dry-run says the declared
  graph is satisfied; freshness additionally requires the graph to represent every real
  influence.
- `scratch path` versus `trusted final`: scratch records an unaccepted attempt; only
  successful validation and promotion changes the final.

## Quick self-check

Before you leave Module 01, make sure you can answer these in a full sentence:

- If two rules can both produce `results/A/report.txt`, what is the exact ownership
  problem called?
- If a run finishes but leaves a final-looking file that was written before the command
  failed, what should you call that file?
- If changing core count affects runtime but should not change biological or analytic
  meaning, which boundary owns that setting?
- If `snakemake -n` still wants more work after a successful run, which term tells you the
  workflow has not reached a stable finished state yet?
- If a policy file changes but the report remains stale because the file was passed only
  through `params`, which defect occurred?

## Terms you should be able to use by the end of the day

If Module 01 is landing properly, these terms should feel ordinary by the end:

- file contract
- requested target
- convergence
- wildcard binding
- output ownership
- workflow meaning
- atomic publication

If those terms still feel decorative rather than useful, revisit the worked example and
the first five exercises before moving on.
