# Glossary

Use this glossary to keep the language of Module 10 stable while you move between review,
migration, governance, boundary decisions, and practice.

The goal is not extra jargon. The goal is to stop teams from using three vague phrases when
one precise term would do.

## How to use this glossary

If a build discussion starts drifting into phrases like "we should modernize this" or "the
boundary feels wrong," stop and look up the term doing the most work in the argument.
Module 10 gets much sharper when stewardship language is precise.

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| accidental public target | A helper target that consumers such as CI or scripts began to rely on even though nobody intentionally promoted it. |
| boundary risk | A sign that Make owns a concern it cannot model honestly, or that a handoff to another tool is vague and untestable. |
| change class | A category of build change, such as public contract change or proof-surface change, used to decide the right review bar. |
| comparison route | A temporary or permanent target that helps compare old and new behavior during migration. |
| contract drift | A situation where a target name, output promise, or user expectation no longer matches what the build really does. |
| governance note | A short written rule set defining what is public, what review is required, and which proof surfaces must be protected. |
| hidden state | Any input, environment fact, or shared mutation that influences build behavior without being modeled clearly in the graph or contract. |
| hybrid boundary | A deliberate split where Make keeps ownership of one responsibility and another tool owns a different concern through an explicit handoff. |
| ownership argument | A justification for why one tool should remain responsible for a concern, based on modeling fit rather than habit or fashion. |
| proof harness | The collection of evidence surfaces and checks that let maintainers trust the build during review or migration. |
| proof surface | Any route, artifact, or check that helps explain and verify build behavior, such as `selftest`, `--trace`, or an audit manifest. |
| public target contract | The stable meaning promised by a target that humans or automation are expected to rely on. |
| retirement condition | The explicit condition that must be true before an old route can be removed during migration. |
| review artifact | A concise written output from a build review, usually summarizing contracts, outputs, hidden inputs, pressure findings, and classified risks. |
| risk class | The type of problem identified in a review, such as graph truth risk, contract drift, environment risk, or boundary risk. |
| stewardship | The practice of maintaining a build as a long-lived product with explicit contracts, proof, and ownership. |
| target promotion rule | The rule a team uses to decide when a helper target becomes a public contract. |
| tool-boundary decision | The act of deciding whether Make should keep owning a concern, share it through a hybrid boundary, or hand it off entirely. |
| truth-preserving migration | A migration sequence that improves the build without deleting the evidence needed to trust old and new behavior. |
| multi-writer output | A trusted output that is rewritten by more than one route, making ownership and incremental behavior hard to trust. |

## The vocabulary standard for this module

When you explain a Module 10 situation, aim to say things like:

- "this is contract drift, not just messy naming"
- "we need a comparison route before retiring the old release path"
- "that helper target became an accidental public target"
- "the governance note should protect this proof surface"
- "deployment policy is a boundary risk, not a packaging problem"

Those sentences are much more useful than saying only "the build needs cleanup."
