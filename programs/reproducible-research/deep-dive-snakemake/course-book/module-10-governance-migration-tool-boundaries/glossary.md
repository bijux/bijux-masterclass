# Glossary

Module 10 is about stewardship under change. When a repository is being migrated,
governed, or split across tools, weak language makes weak decisions. This glossary keeps
the discussion anchored in reviewable boundaries instead of slogans.

## How to use this glossary

Come back to this page whenever a migration or governance discussion starts drifting into
generic words like "modernize," "platform," "cleanup," or "ownership."

The glossary is not here to sound formal. It is here to keep stewardship discussion sharp
enough that two maintainers can mean the same thing.

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

## Confusion pairs worth fixing early

These pairs matter because governance work often sounds responsible while still weakening
the repository:

- `current truth` versus hoped-for redesign: current truth is what the repository really
  does now; a redesign is only a proposal until proof and migration evidence support it.
- `policy boundary` versus semantic change: policy should change how the workflow runs, not
  what the workflow means.
- `migration step` versus `retirement condition`: a migration step moves one boundary; a
  retirement condition says when an old surface may safely disappear.
- `tool boundary` versus `hybrid ownership`: the tool boundary names what Snakemake should
  own; hybrid ownership describes a deliberate split where another system owns adjacent
  concerns without taking file-truth ownership away from Snakemake.

## Quick self-check

Before you leave Module 10, make sure you can answer these in a full sentence:

- If a maintainer wants to delete an old report route before the replacement can be
  compared honestly, which missing safety condition should stop that deletion?
- If a profile change starts altering final artifact meaning, what governance problem has
  crossed the line from policy into semantics?
- If helper layers hide critical workflow behavior from normal review, which module term
  captures that hidden stewardship risk?
- If a platform service takes over deployment but Snakemake still owns file contracts and
  pipeline truth, what ownership pattern are you describing?

## Terms you should be able to use by the end of the day

By the end of Module 10, you should be comfortable using these in a full sentence:

- current truth
- review route
- migration step
- preserved proof
- retirement condition
- tool boundary
- hybrid ownership
