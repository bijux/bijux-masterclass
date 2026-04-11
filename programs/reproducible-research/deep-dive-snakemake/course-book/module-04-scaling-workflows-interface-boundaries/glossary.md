# Glossary

Use this glossary to keep the language of Module 04 stable while you move between the
core lessons, worked example, exercises, and capstone evidence.

The goal is not extra jargon. The goal is to make scaling and interface decisions sound
like clear repository boundaries instead of vague architecture talk.

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| file API | The documented public file contract that tells another consumer which paths and semantics are stable to trust. |
| gate | A named review or CI surface that protects one specific repository boundary. |
| include boundary | A split inside one visible workflow graph, usually used to group coherent rule families by ownership. |
| internal state | Workflow files that help execution or review but are not part of the downstream public contract. |
| module boundary | A reusable workflow boundary with explicit interface expectations, stronger than a mere file split. |
| named ownership | The ability to say in one sentence which workflow concern a file or boundary owns. |
| public contract | The smaller set of paths, semantics, or interfaces that downstream users are allowed to depend on. |
| review surface | A command, graph, bundle, or document that helps a human inspect one boundary deliberately. |
| rule family | A coherent group of related rules that belong together inside one repository concern. |
| scaling boundary | The point where repository growth is absorbed without making workflow meaning harder to explain. |
| schema validation | A structured check that fails early when a config or artifact boundary violates its declared shape. |
| visible graph | The workflow story that a reader can still explain from the top-level orchestration surface. |

## The vocabulary standard for this module

When you explain a Module 04 situation, aim to say things like:

- "this split improves named ownership without hiding the visible graph"
- "that boundary is not ready to become a module because the interface is still vague"
- "the public file API is smaller than the repository's internal state"
- "this gate protects architecture visibility, not only general quality"
- "the executor-facing policy adapts a workflow-side resource distinction"

Those sentences are much more useful than saying only "the repo should be more modular."
