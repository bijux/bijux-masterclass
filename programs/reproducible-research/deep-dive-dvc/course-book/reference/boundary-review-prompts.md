# Boundary Review Prompts

Use this page when a DVC review feels fuzzy and you need sharper keep, change, or reject
 questions tied to repository boundaries.

## Declaration versus execution

- Does `dvc.yaml` describe the same contract that `dvc.lock` records?
- Is the implementation readable without weakening the declared pipeline boundary?
- Would a reviewer know which file should win if declaration and execution seem to disagree?

## Promotion versus internal state

- Is the promoted bundle smaller and clearer than the whole repository?
- Has any internal artifact started masquerading as downstream contract?
- Would a downstream reviewer know what they may rely on without oral explanation?

## Recovery versus convenience

- Is the recovery story really remote-backed, or is it leaning on local convenience?
- Which claim is about durability, and which is only about ordinary verification?
- What evidence would make you reject the current recovery boundary as too soft?
