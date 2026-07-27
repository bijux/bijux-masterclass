# Glossary

Scaling a workflow is not only about adding more rules. It is about keeping the workflow
understandable while the repository grows. This glossary helps you describe that growth in
terms of boundaries a reviewer can actually inspect.

Use it whenever architecture discussion starts sounding abstract instead of concrete.

## When to stop and check the glossary

Pause and check a term when:

- your explanation depends on "modular" without naming the actual ownership boundary
- you are treating an include split and a reusable module as if they were the same thing
- you cannot separate a module declaration from a `use rule` caller binding
- a module reads config, but nobody can say whether that policy is public or private
- you can tell a path matters to consumers but cannot yet say whether it is public or internal
- you are calling a gate useful without saying what contract it protects

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| caller binding | The local input, output, parameter, log, resource, or name assigned when a caller imports a module rule with `use rule`. |
| file API | The documented public file contract that tells another consumer which paths and semantics are stable to trust. |
| gate | A named review or CI surface that protects one specific repository boundary. |
| hidden coupling | Behavior that depends on private config, paths, helpers, or policy not named at the caller interface. |
| include boundary | A split inside one visible workflow graph, usually used to group coherent rule families by ownership. |
| internal state | Workflow files that help execution or review but are not part of the downstream public contract. |
| module boundary | A reusable workflow boundary with explicit interface expectations, stronger than a mere file split. |
| module config scope | The configuration object passed by a caller's `module` declaration; a narrow owned subtree makes dependencies reviewable. |
| named ownership | The ability to say in one sentence which workflow concern a file or boundary owns. |
| override matrix | A table that records module defaults, caller bindings, and final ownership for each imported rule surface. |
| public contract | The smaller set of paths, semantics, or interfaces that downstream users are allowed to depend on. |
| rejection test | A controlled dishonest change that must fail a gate for the promised reason. |
| review surface | A command, graph, bundle, or document that helps a human inspect one boundary deliberately. |
| rule family | A coherent group of related rules that belong together inside one repository concern. |
| scaling boundary | The point where repository growth is absorbed without making workflow meaning harder to explain. |
| schema validation | A structured check that fails early when a config or artifact boundary violates its declared shape. |
| visible graph | The workflow story that a reader can still explain from the top-level orchestration surface. |

## The vocabulary standard for this module

When you explain a Module 04 situation, aim to say things like:

- "this split improves named ownership without hiding the visible graph"
- "that boundary is not ready to become a module because policy remains hidden in broad config"
- "the caller binding owns paths and artifact policy; the module owns implementation"
- "the public file API is smaller than the repository's internal state"
- "this rejection test proves the interface gate notices a missing caller binding"
- "the executor-facing policy adapts a workflow-side resource distinction"

Those sentences are much more useful than saying only "the repo should be more modular."

## Confusion pairs worth fixing early

These pairs matter because they separate helpful structure from architecture theater:

- `include boundary` versus `module boundary`: an include split groups files inside one
  graph; a module boundary implies a stronger reusable interface.
- `module declaration` versus `caller binding`: the declaration selects module source and
  config scope; `use rule` selects and locally binds imported rule surfaces.
- `narrow config` versus `hidden coupling`: narrow config exposes an owned dependency
  domain; hidden coupling lets private code choose caller-visible meaning without naming
  that dependency.
- `acceptance test` versus `rejection test`: acceptance proves honest evidence can pass;
  rejection proves a controlled lie cannot pass unnoticed.
- `public contract` versus `internal state`: public contract is what consumers may rely
  on; internal state may exist only to help execution or review.
- `file API` versus `visible graph`: a file API explains stable paths and meanings; the
  visible graph explains how the top-level workflow remains understandable.
- `review surface` versus `gate`: a review surface is any inspectable artifact or command;
  a gate is a named check that actively protects a boundary.

## Quick self-check

Before you leave Module 04, make sure you can answer these in a full sentence:

- If you split one long Snakefile into smaller files but reviewers can still see the whole
  workflow story easily, which visibility term fits that design?
- If another workflow can import a boundary only because you documented stable inputs,
  outputs, and semantics, what stronger concept have you created beyond an include file?
- If `--list-rules` and dry-run pass but private module code reads policy from broad config,
  which coupling term describes the unresolved defect?
- If a copied control broadens its config and the gate must fail, what kind of test is
  exercising the gate?
- If a path helps internal debugging but should never be promised downstream, which side
  of the contract line does it belong to?
- If a CI check fails whenever a public artifact disappears from the publish tree, what
  kind of protective surface is that check serving as?

## Terms you should be able to use by the end of the day

If Module 04 is landing properly, these terms should feel ordinary by the end:

- rule family
- named ownership
- visible graph
- file API
- module boundary
- module config scope
- caller binding
- override matrix
- hidden coupling
- rejection test
- public contract
- review surface

If those still feel decorative rather than useful, revisit the worked example and the
first seven exercises before moving on.
