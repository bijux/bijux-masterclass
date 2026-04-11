# Glossary

This glossary keeps the language of Module 07 stable. The goal is practical architecture
clarity: when the same terms keep the same meaning, repository review gets faster and more
honest.

## Terms

| Term | Meaning in this module |
| --- | --- |
| entrypoint | The top-level workflow assembly surface, usually `Snakefile`, where reviewers should first understand how the workflow is composed. |
| visible assembly | A repository design where the top-level workflow shape is easy to discover without digging through helper code first. |
| repository layer | A named architectural surface such as `workflow/rules/`, `workflow/modules/`, `workflow/scripts/`, `src/`, `profiles/`, or `config/`, each with a distinct job. |
| rule family | A coherent group of rules that share one workflow concern, file-surface family, or review question. |
| workflow module | A reusable workflow bundle that owns a clearer interface than a local rule-family file. |
| ownership boundary | The line that explains which repository surface owns orchestration, implementation, policy, or path contracts. |
| file API | A document that records which paths are stable, what they mean, and which surfaces are internal versus public. |
| workflow-facing path contract | A stable path promise used inside the workflow, such as discovery artifacts or per-sample result families. |
| downstream-facing path contract | A stable path promise exposed to downstream consumers, such as versioned publish surfaces. |
| step-local implementation | Code near one workflow step, often a good fit for `workflow/scripts/`. |
| reusable package code | Importable implementation code under `src/` that deserves direct tests and reuse across steps. |
| hidden coupling | A dependency on files, config, or side effects that is not visible in the declared repository surfaces. |
| architecture drift | The gradual weakening of repository clarity as boundaries, docs, and ownership signals stop matching the real code. |
| refactor trigger | A concrete review or maintenance signal that justifies reshaping repository boundaries. |
| private framework | A repository that technically works but hides its meaning behind helper layers and insider knowledge. |

## How to use these terms

If an architecture discussion starts to feel fuzzy, ask which term has become unclear:

- is this an entrypoint problem, a rule-family problem, or a helper-coupling problem?
- is this path workflow-facing or downstream-facing?
- is this refactor fixing a real boundary, or only changing the tree shape?

That question usually exposes the real architectural issue quickly.
