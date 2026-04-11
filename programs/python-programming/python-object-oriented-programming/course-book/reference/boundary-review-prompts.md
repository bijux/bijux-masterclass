# Boundary Review Prompts


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Reference"]
  page["Boundary Review Prompts"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Read the first diagram as a lookup map: this page is part of the review shelf, not a first-read narrative. Read the second diagram as the reference rhythm: arrive with a concrete ambiguity, compare the current work against the boundary on the page, then turn that comparison into a decision.

Use these prompts when a design crosses process, time, persistence, or extension
boundaries. These are the places where object-oriented systems usually stop being
clear unless the ownership rules are made explicit.

## Public API prompts

- Which names are intentionally public, and which ones are only convenient today?
- Does the facade reflect the real domain boundary or just the current file layout?
- Are examples and commands proving the same contract the docs describe?

## Persistence prompts

- Does storage mapping preserve domain invariants, or does it bypass them?
- Which serialized shape is a contract, and how would it evolve safely?
- Where is conflict detection or rollback responsibility made visible?

## Runtime prompts

- Which object owns clocks, retries, queues, async bridges, or worker coordination?
- Does runtime orchestration coordinate the domain, or is it absorbing domain rules?
- Which behavior would become unsafe first under concurrency or cancellation pressure?

## Extension prompts

- What is the narrowest supported extension seam?
- Could a plugin or adapter mutate domain internals it should not control?
- Which review or compatibility checks would fail first if an extension broke the contract?

## Decision bar after the prompts

After you answer the prompts for one boundary, force a clear verdict:

- keep the current boundary because ownership, proof, and review cost still line up
- tighten the boundary because convenient access is creating accidental authority
- redesign the boundary because the current split no longer matches who owns the rule

## Evidence to ask for before accepting the boundary

- which guide, file, or command would you show another reviewer first
- which proof surface should fail first if this boundary drifts
- which neighboring boundary becomes safer because this one stayed narrow
