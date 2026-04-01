<a id="top"></a>

# Module 10 — Mastery: Migration, Governance, and Knowing Make's Boundaries

The last module is not about one more GNU Make trick. It is about judgment. Mature build
engineering means knowing how to review a legacy Make system, how to improve it without
breaking trust, and how to recognize when Make should remain the orchestrator versus when
another tool should own a different concern.

Mastery is the ability to preserve correctness while making deliberate boundary decisions.

### Before You Begin

This module works best after the rest of the program. It is designed for review,
migration, and governance work rather than first-contact syntax learning.

Use this module if you need to learn how to:

* audit a real Make system without collapsing into style debates
* design a migration that keeps proof, not just intention
* define long-term ownership and change rules for build infrastructure

### At a glance

| Focus | Learner question | Capstone timing |
| --- | --- | --- |
| legacy review | "Which contracts are broken today?" | use capstone as a review specimen after the rubric is clear |
| migration | "How do I improve the system without losing proof?" | compare your migration plan to the reference build boundaries |
| governance | "What should future maintainers be allowed to change freely?" | inspect public targets and helper layers once review categories are stable |

Proof loop for this module:

```sh
make -n all
make --trace all
make -p > build/review.dump
```

Capstone corroboration:

* review public target promises in `capstone/Makefile`
* review helper boundaries under `capstone/mk/`
* use the capstone repros as migration-risk examples

The course ends well only if the learner leaves with a repeatable review method, not just
with a list of anti-patterns.

---

<a id="toc"></a>
## 1) Table of Contents

1. [Table of Contents](#toc)
2. [Learning Outcomes](#outcomes)
3. [How to Use This Module](#usage)
4. [Core 1 — Reviewing Legacy Makefiles Without Wishful Thinking](#core1)
5. [Core 2 — Safe Migration Plans and Hybrid Boundaries](#core2)
6. [Core 3 — Governance for Long-Lived Build Systems](#core3)
7. [Core 4 — Anti-Patterns That Keep Coming Back](#core4)
8. [Core 5 — Deciding When Make Is Still the Right Core Tool](#core5)
9. [Capstone Sidebar](#capstone)
10. [Exercises](#exercises)
11. [Closing Criteria](#closing)

---

<a id="outcomes"></a>
## 2) Learning Outcomes

By the end of this module, you can:

* audit a legacy Make system for truth, safety, and maintainability risks
* design a migration plan that preserves the working proof harness
* define ownership and review rules for long-lived build infrastructure
* identify recurring anti-patterns before they harden into habit
* decide whether Make should continue as the main build graph or hand responsibility to another tool

[Back to top](#top)

---

<a id="usage"></a>
## 3) How to Use This Module

Take one real Make-based system and write a short build review with five sections:

1. graph truth risks
2. publication and failure risks
3. operational risks
4. migration opportunities
5. tool-boundary recommendation

The goal is not to rewrite the system during the review. The goal is to make the current
state legible enough that change can be deliberate.

[Back to top](#top)

---

<a id="core1"></a>
## 4) Core 1 — Reviewing Legacy Makefiles Without Wishful Thinking

Legacy review starts with evidence:

* what are the public targets?
* which outputs have multiple writers?
* which prerequisites are hidden or implied?
* which shell commands mutate shared state?
* which failures only appear under `-j` or on clean machines?

Do not start by judging style. Start by locating broken contracts.

[Back to top](#top)

---

<a id="core2"></a>
## 5) Core 2 — Safe Migration Plans and Hybrid Boundaries

Migration is safest when you preserve the proof harness:

* keep convergence checks
* keep serial/parallel equivalence checks
* move one truth boundary at a time
* add wrappers only when the handoff is explicit

Common safe hybrids:

* Make orchestrates, a script generates manifests
* Make drives compilation, another tool handles packaging metadata
* Make owns local graph truth, a workflow engine owns distributed execution

The migration should reduce ambiguity, not merely move it.

[Back to top](#top)

---

<a id="core3"></a>
## 6) Core 3 — Governance for Long-Lived Build Systems

Long-lived build systems need rules:

* who can add public targets
* what every new rule must prove
* where macros and includes are allowed to grow
* which diagnostics must remain available
* how breaking changes to target behavior are reviewed

Without governance, build infrastructure becomes a shared superstition.

[Back to top](#top)

---

<a id="core4"></a>
## 7) Core 4 — Anti-Patterns That Keep Coming Back

Patterns worth rejecting on sight:

* phony ordering used instead of real prerequisites
* shared append logs in parallel recipes
* recursive make that hides the real DAG
* stamps that rebuild forever or hide semantic inputs
* non-atomic publication of generated or packaged artifacts
* “performance fixes” that skip truthful rebuilds

Mastery is often the ability to say no before damage spreads.

[Back to top](#top)

---

<a id="core5"></a>
## 8) Core 5 — Deciding When Make Is Still the Right Core Tool

Make remains a strong core tool when:

* the dependency graph is local and explicit
* targets are file-oriented or manifest-oriented
* publication semantics can stay auditable
* the main challenge is correctness and incremental rebuild behavior

Make should stop being the sole core when:

* execution is fundamentally distributed or stateful beyond file edges
* orchestration depends on external authority, long-lived scheduling, or dynamic provenance graphs
* correctness requires abstractions that Make can only fake with brittle indirection

The mature answer is sometimes “keep Make here, hand that concern elsewhere.”

[Back to top](#top)

---

<a id="capstone"></a>
## 9) Capstone Sidebar

Use the capstone as a review specimen:

* Which public targets deserve long-term compatibility promises?
* Which helper layers are safe to extend, and which should stay bounded?
* Which repros model failure patterns you would add to a migration review?
* Which build concerns would still belong in Make if this project doubled in size?

[Back to top](#top)

---

<a id="exercises"></a>
## 10) Exercises

1. Write a build review for one legacy Makefile and classify its top five risks.
2. Propose a migration plan that preserves convergence and equivalence checks while changing one major subsystem.
3. Draft a short governance note for adding new public targets or new macros.
4. Pick one build concern and argue clearly whether Make should keep owning it.

[Back to top](#top)

---

<a id="closing"></a>
## 11) Closing Criteria

You pass this module only if you can demonstrate:

* an evidence-based review of a real build
* a migration plan that preserves proof, not just intent
* explicit governance rules for future changes
* a clear explanation of where Make remains the right tool and where it should stop

[Back to top](#top)
