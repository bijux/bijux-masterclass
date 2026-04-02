# Boundary Review Prompts


<!-- page-maps:start -->
## Reference Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Object-Oriented Programming"]
  program --> reference["Boundary Review Prompts"]
  reference --> review["Design or review decision"]
  review --> capstone["Capstone proof surface"]
```

```mermaid
flowchart TD
  trigger["Hit a naming, boundary, or trade-off question"] --> lookup["Use this page as a glossary, map, rubric, or atlas"]
  lookup --> compare["Compare the current code or workflow against the boundary"]
  compare --> decision["Turn the comparison into a keep, change, or reject call"]
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
