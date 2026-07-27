# Self-Review Prompts

Use this page when you want to check whether you can explain the course in your own
words. The prompts are designed to force recall, prediction, and judgment. If they only
trigger recognition, use fewer prompts and answer them without looking at the modules.

## How to use this page well

Pick three prompts only:

1. answer them from memory
2. verify each answer against a command, file, or saved artifact
3. rewrite each answer in plainer language
4. note which module you would revisit if the answer stayed fuzzy

Three honest prompts are worth more than twenty shallow ones.

## Beginner prompts

Use these after Modules 01-03, or anytime the workflow contract still feels unstable.

- Which file contract is doing the real work in the current example?
- What target would you ask a new learner to build first, and why?
- Which wildcard or config choice would most easily make this workflow misleading?
- What command would you run first to explain why Snakemake wants to rerun?
- What would count as an atomic output here, not just a file that happened to appear?
- Which difference belongs in the workflow contract rather than in a profile?

**You are ready to move on when**

You can answer without borrowing the exact wording from Module 01 or Module 03.

## Dynamic-DAG prompts

Use these after Module 02, or when checkpoints still feel magical.

- What durable artifact records the discovered sample set?
- Why is this checkpoint safer than hard-coding the same fan-out by hand?
- What would make you distrust the discovery result even if the run completed?
- How would you explain the graph change to someone who only sees the dry-run?
- Which integrity check should fail if the discovered set is malformed or partial?
- What evidence would you save so another maintainer could review discovery later?

**You are ready to move on when**

You can explain the changing graph as staged evidence rather than runtime cleverness.

## Boundary prompts

Use these after Modules 04-07, or when repository structure is harder to trust than the
workflow itself.

- Should this behavior live in `Snakefile`, rules, modules, scripts, package code, or
  profiles?
- Which file API is carrying the repository boundary here?
- What would make a module split clearer instead of merely flatter?
- Which helper-script behavior would you move back into the workflow contract?
- If you removed one layer, which one would most likely expose hidden coupling?
- Which publish artifact is actually public, and which ones are only run scaffolding?

**You are ready to move on when**

You can explain repository structure as an ownership decision, not a stylistic one.

## Operating-context prompts

Use these after Module 08, or when local, CI, and cluster contexts feel hard to compare.

- Which differences across profiles are allowed, and which would count as semantic drift?
- What should stay stable if you move the same workflow from local development to CI?
- Which executor or storage choice changes cost but not meaning?
- How would you prove that a context change is operationally necessary and analytically
  safe?
- What run artifact would you retain to compare two contexts honestly?
- Which policy leak would be most dangerous because it would still look convenient?

**You are ready to move on when**

You can separate "this runs somewhere else" from "this means something else."

## Incident and stewardship prompts

Use these after Modules 09-10, or when you want to test higher-pressure judgment.

- Which saved evidence bundle would you trust first if logs disappeared?
- What failure class would you name before changing performance settings?
- Which repository layer should absorb the next non-trivial change?
- What would count as semantic drift rather than ordinary operating drift?
- When should Snakemake stop owning the orchestration problem?
- Which governance check would protect this workflow from repeating the same incident?

**You are ready to finish the course when**

You can explain both repair and stewardship without turning either answer into vague
process language.

## Good signs

These prompts are working when they make you do one of the following:

- predict a rerun before you execute it
- name the artifact that settles a discovery or publish question
- identify the exact layer that should own a change
- explain why a profile change is safe or unsafe
- choose a smaller proof route than the one you first wanted

## Warning signs

Slow down and return to the module if:

- your answer depends on repeating course vocabulary without explanation
- you can describe the symptom but not the contract that failed
- you keep citing logs when a durable artifact should exist
- every answer turns into "it depends" before you inspect a concrete surface

## Companion pages

- [Practice Map](practice-map.md)
- [Boundary Review Prompts](boundary-review-prompts.md)
- [Anti-Pattern Atlas](anti-pattern-atlas.md)
- [Completion Rubric](completion-rubric.md)
