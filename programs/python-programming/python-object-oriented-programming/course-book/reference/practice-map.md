# Practice Map

Use this page when you want to know what kind of local exercise, proof, or capstone
follow-up best fits each stage of the OOP course.

## Module practice surfaces

| Module | Primary practice surface | Main proof loop | Best capstone follow-up |
| --- | --- | --- | --- |
| 01 | value and entity design exercises | compare equality, identity, and representation decisions explicitly | inspect value objects and model boundaries |
| 02 | role and layering refactors | name one responsibility per object and move orchestration outward | inspect architecture and file guides together |
| 03 | validation and typestate labs | make legal transitions easier than illegal ones and prove the boundary | inspect lifecycle rules and review prompts |
| 04 | aggregate and event exercises | identify the authoritative object before adding collaboration | inspect aggregate ownership and event flow |
| 05 | failure and evolution exercises | compare design choices by which object absorbs change safely | inspect unit-of-work and extension seams |
| 06 | persistence-boundary reviews | change storage concerns without weakening invariants | inspect repository and codec surfaces |
| 07 | time and concurrency labs | keep scheduling, clocks, and queues outside the domain model | inspect runtime coordination and boundary ownership |
| 08 | testing-depth reviews | choose the narrowest test that proves the current contract | inspect proof routes and saved bundles |
| 09 | public API and extension reviews | name the supported extension seam before adding it | inspect public surfaces and extension guidance |
| 10 | stewardship review | write one architecture judgment backed by one proof route | use the capstone as the final review specimen |

## Reusable proof loops

- ownership loop: name the authoritative object, the derived view, and the first test that should fail if that split drifts
- lifecycle loop: state the legal transitions, the blocked transitions, and where those rules live
- extension loop: explain where a new behavior belongs before you explain how to implement it
