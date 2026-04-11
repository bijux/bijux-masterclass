# Practice Map

Use this page when you want to know what kind of local exercise, proof, or capstone
follow-up best fits each stage of the course.

## Module practice surfaces

| Module | Primary practice surface | Main proof loop | Best capstone follow-up |
| --- | --- | --- | --- |
| 01 | purity and immutability refactors | run the same function twice and compare contracts and results | inspect pure package boundaries first |
| 02 | data-first pipeline rewrites | replace object-shaped orchestration with value flow and compare clarity | inspect file and package reading order |
| 03 | iterator and streaming exercises | compare eager and lazy routes for the same dataflow | inspect pipeline assembly and materialization points |
| 04 | failure-handling and retry exercises | name the failure surface before choosing recovery behavior | inspect proof routes around policies and domain failures |
| 05 | validation and algebraic modelling labs | compare invalid-state handling across value types and tests | inspect `result`, `rag`, and policy boundaries |
| 06 | explicit-context and chaining exercises | explain what context is being carried and why | inspect composition and review surfaces together |
| 07 | effect-boundary refactors | move one ambient effect behind a named boundary and prove the seam | inspect boundaries, adapters, and domain ownership |
| 08 | async pipeline labs | compare backpressure, fairness, and orchestration choices with named policies | inspect async boundaries and orchestration packages |
| 09 | interop wrappers and boundary discipline | wrap one external tool or library without leaking its shape inward | inspect interop and infrastructure seams |
| 10 | sustainment review | write one design judgment backed by one proof route | use the capstone as the final review specimen |

## Reusable proof loops

- purity loop: identify hidden state, remove it, then prove the same inputs still mean the same result
- boundary loop: name the pure core, the effect edge, and the test or proof that keeps them distinct
- sustainment loop: name what changed, which package owns it now, and which proof route would fail first if the claim were false
