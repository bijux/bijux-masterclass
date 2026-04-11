# Glossary

This glossary keeps the language of Module 10 stable.

The goal is practical stewardship clarity: when migration, governance, and tool-boundary
terms keep the same meaning, review gets calmer and more precise.

## Terms

| Term | Meaning in this module |
| --- | --- |
| current truth | The repository behavior and contract surfaces that are actually in force today, whether or not they are documented well. |
| review route | The shortest honest sequence of commands and artifacts that lets a maintainer inspect the repository before changing it. |
| public contract | The set of files, paths, and meanings that downstream users may safely trust. |
| internal execution surface | Useful workflow state such as `results/`, logs, or intermediates that may help maintainers but is not automatically public. |
| policy boundary | The operating-context surface, such as profiles or executor settings, that should influence how the workflow runs without changing what it means. |
| proof route | The visible commands and artifacts that let a reviewer compare, verify, or audit workflow behavior. |
| migration step | One bounded change that moves a single boundary while preserving enough evidence to compare old and new behavior. |
| preserved proof | The part of the old or current evidence route that remains available while a migration is in progress. |
| retirement condition | The concrete condition that must be met before an old route, helper, or boundary can safely disappear. |
| governance rule | A durable review rule that protects contracts, policy boundaries, proof surfaces, or ownership clarity over time. |
| contract drift | The weakening of the public boundary as consumers, paths, or meanings move outside the reviewed contract. |
| policy leak | A case where operating policy starts changing workflow meaning instead of only execution behavior. |
| invisible complexity | Important workflow meaning hiding in helpers, wrappers, or packages that reviewers do not naturally inspect. |
| evidence suppression | Removing or weakening logs, benchmarks, verification, or comparison surfaces in ways that make the workflow harder to trust. |
| tool boundary | The ownership line that says which concern Snakemake should keep and which concern another system should own. |
| hybrid ownership | A design where Snakemake keeps ownership of file-based workflow truth while another system owns service, platform, or lifecycle concerns. |

## How to use these terms

If a Module 10 discussion starts getting vague, ask which term has become unclear:

- are we describing current truth or a hoped-for redesign?
- is this a policy boundary or a semantic change?
- what proof route is being preserved during this migration step?
- is this concern still within Snakemake's tool boundary?

Those questions usually turn a fuzzy migration argument into a reviewable one.
