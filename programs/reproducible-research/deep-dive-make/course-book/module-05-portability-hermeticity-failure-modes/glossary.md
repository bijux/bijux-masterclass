# Glossary

Use this glossary to keep the language of Module 05 stable while you move between the core
lessons, worked example, and exercises.

The goal is not more jargon. The goal is to make sure the same build fact keeps the same
name whenever you explain a boundary, a measurement, or a failure.

## How to use this glossary

If a hardening discussion starts drifting into vague words like "portable," "hermetic,"
or "slow," stop and look up the term doing the most work in the discussion. A lot of build
confusion disappears once the team agrees on what a word means locally.

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| attestation | Recording a real external build fact, such as compiler identity, without pretending the fact does not exist. |
| capability gate | A named condition that expresses whether a required feature is available, such as grouped targets support in a given Make version. |
| contract check | An explicit validation step that proves required tools, versions, or shell behavior exist before the build continues. |
| convergence | The property that a successful build reaches a stable state and does not claim more work on the next run. |
| controlled recursion | Recursive Make structure that stays inside a declared ownership boundary and the same parallel budget. |
| environment contract | The declared set of tool, shell, locale, and variable assumptions that the build relies on. |
| hermetic enough | A practical standard where external facts that change artifact meaning are declared, pinned, or attested clearly enough for reproducible reasoning. |
| jobserver | GNU Make's shared token budget for coordinating parallelism across recursive sub-makes. |
| `MAKELEVEL` | The built-in variable that reports recursion depth and helps keep recursive structure bounded. |
| manifest | A file that records build facts such as mode, tool identity, or provenance in a stable, inspectable way. |
| measurement loop | A small repeatable sequence of commands used to distinguish parse cost, recipe cost, and evidence volume before making performance claims. |
| non-file input | A real build fact that is not itself a normal source file, such as locale, selected compiler, or mode flag. |
| ownership boundary | The line that says which tool, sub-build, or target family is responsible for a given artifact or concern. |
| pinning | Forcing a build-relevant value to a chosen setting so behavior stays stable, such as `LC_ALL := C`. |
| portability contract | The declared statement of required Make behavior, shell semantics, tools, and optional fallbacks. |
| proof route | The commands or checks that demonstrate a build claim, such as convergence, equivalence, or boundary validation. |
| recipe cost | The portion of build time spent in external tool execution rather than in Make's own parsing or decision work. |
| stamp | A file that represents a semantic fact or successful build event when no natural output file already carries that meaning. |
| tool boundary | The point where another tool may deserve ownership of a concern because Make no longer models that concern clearly enough. |
| trace volume | A rough measure of how much explanatory output a build emits, often useful as a proxy for operational readability. |

## The vocabulary standard for this module

When you explain a Module 05 incident, aim to say things like:

- "the portability contract is missing a required tool boundary"
- "the recursive boundary lost the shared jobserver budget"
- "that manifest does not converge because it records timestamps"
- "the performance complaint is mostly recipe cost, not Make overhead"
- "this is a tool-boundary problem, not another macro problem"

Those sentences are far more useful than saying only "the build is fragile."
