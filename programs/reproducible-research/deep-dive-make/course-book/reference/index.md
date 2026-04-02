# Reference

<!-- page-maps:start -->
## Reference Position

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Make"]
  program --> reference["Reference"]
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

The reference surface holds the durable reading aids for Deep Dive Make. These pages are
for questions that recur across modules: vocabulary, learning order, stable target
surfaces, build layers, artifact boundaries, incident debugging order, and review
standards.

## Use This Section When

- you need the right vocabulary before reading a module again
- you want to know which target or layer is public and which is implementation detail
- you need the right proof route instead of the strongest one
- you are reviewing whether the course and capstone are keeping their promises

## Reference Pages

- [Module Dependency Map](module-dependency-map.md) for concept order and safe reading sequence
- [Build-Graph Glossary](build-graph-glossary.md) for durable terminology
- [Topic Boundaries](topic-boundaries.md) for what the course treats as core, supporting, and boundary material
- [Concept Index](concept-index.md) for locating where an idea is taught
- [Anti-Pattern Atlas](anti-pattern-atlas.md) for routing common Make smells to the right repair path
- [Practice Map](practice-map.md) for module-to-proof routing
- [Public Targets](public-targets.md) for stable command surfaces
- [Incident Ladder](incident-ladder.md) for debugging order under pressure
- [Mk Layer Guide](mk-layer-guide.md) for the layered build architecture
- [Artifact Boundary Guide](artifact-boundary-guide.md) for separating outputs, proofs, and teaching surfaces
- [Selftest Map](selftest-map.md) for reading the build proof harness
- [Completion Rubric](completion-rubric.md) for course and repository review
