# Boundary Review Prompts

Use this page when a review feels blurry and you need sharper keep, change, or reject
questions tied to workflow boundaries. These prompts are meant to turn unease into a
specific boundary judgment.

## How to use the prompts

Pick one section only. Answer the questions out loud or in writing. Then end with one
sentence that starts with one of these:

- keep this boundary because...
- change this boundary because...
- reject this boundary because...

If you cannot finish that sentence, the claim is still too vague.

## Workflow versus policy

- Does this change alter workflow meaning or only execution policy?
- Would a dry-run reveal the important part of the behavior honestly?
- Has a profile started carrying semantic meaning it should not own?

## Discovery versus folklore

- Does dynamic discovery leave a durable artifact that another reviewer can inspect?
- Which rule or artifact actually settles the discovered set?
- Would the workflow still be reviewable if logs were missing?

## Publish and repository boundaries

- Is the published contract smaller and clearer than the whole repository?
- Which layer should own this behavior: `Snakefile`, rules, modules, scripts, package code, or profiles?
- What ambiguity would make you reject the current boundary as too blurry to trust?

## Authority prompts

- Which surface is actually allowed to settle this trust question?
- Is this claim being supported by workflow contracts, durable artifacts, or only logs and memory?
- Would the repository still be reviewable if runtime output disappeared?

## Common strong conclusions

| Situation | Likely conclusion |
| --- | --- |
| a profile change silently changes expected outputs or wildcard meaning | reject the boundary because policy is leaking into semantics |
| a checkpoint decides sample identity but leaves no durable artifact | change the boundary because discovery is still folklore |
| a publish directory contains internal scratch state and public outputs together | change the boundary because downstream trust is too blurry |
| a claim can be settled from the `Snakefile`, manifests, and saved evidence | keep the boundary because the workflow remains reviewable |
