# Boundary Review Prompts


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  prompts["Boundary review prompts"]
  api["Public API"]
  persistence["Persistence"]
  runtime["Runtime pressure"]
  extension["Extension seams"]

  prompts --> api
  prompts --> persistence
  prompts --> runtime
  prompts --> extension
```

```mermaid
flowchart TD
  review["Review one boundary"] --> pressure["Name the main pressure"]
  pressure --> authority["Find the authoritative owner"]
  authority --> leak["Check for leaked assumptions"]
  leak --> verdict["Accept, tighten, or redesign"]
```
<!-- page-maps:end -->

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
