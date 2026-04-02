# Practice Map


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Practice Map"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

This page turns the course into a repeatable rehearsal loop. The goal is not only to
finish reading. The goal is to improve judgment under change.

## Recommended rhythm

1. Read the module overview first.
2. Read the lesson sequence in order.
3. Pause after each major concept and write one sentence beginning with: "This boundary exists because..."
4. Inspect the capstone package or guide that expresses that boundary.
5. Run or review the matching executable proof.
6. Compare your understanding with `_history/worktrees/module-XX` when the module ends.
7. Rephrase the lesson in terms of change: what becomes easier to refactor or review now?

## Questions that travel across modules

- What is still pure?
- What is now explicit data?
- Where does materialization happen, and why there?
- Which failure shape is visible to the caller?
- Which effectful behavior is controlled by a protocol, shell, or adapter?

## What this prevents

This practice loop prevents passive reading, diagram memorization, and the common mistake
of admiring a functional abstraction without being able to say how it makes the codebase
safer to change.
