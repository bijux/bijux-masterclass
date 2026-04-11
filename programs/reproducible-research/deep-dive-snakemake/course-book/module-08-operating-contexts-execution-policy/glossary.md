# Glossary

This glossary keeps the language of Module 08 stable. The goal is practical clarity:
operating-context review gets much easier when the same words keep the same meaning.

## Terms

| Term | Meaning in this module |
| --- | --- |
| operating context | The environment in which the workflow runs, such as local, CI, or scheduler-backed execution. |
| execution policy | Settings that change how the workflow runs or is observed without changing workflow meaning. |
| semantic drift | A change in workflow meaning, trusted outputs, or contract behavior that should not be happening through operating policy alone. |
| profile | A configuration surface that encodes operating policy such as executor defaults, logging, retries, or latency settings. |
| policy leak | A case where profile or context settings start changing workflow semantics instead of only operations. |
| context-invariant meaning | The idea that rule contracts, config meaning, and trusted outputs should stay stable across operating contexts. |
| failure discipline | The explicit operating model for retries, latency waits, incomplete outputs, and failure evidence. |
| transient failure | A failure plausibly caused by operational conditions such as scheduling or visibility delay. |
| deterministic failure | A failure caused by a repeatable defect in workflow logic, runtime, or environment rather than transient operations. |
| latency wait | A policy setting that allows for delayed output visibility, especially on slower or shared filesystems. |
| incomplete output | A partially written or interrupted output that requires explicit handling rather than casual trust. |
| staging | Temporary movement or placement of data during execution before promotion into trusted paths. |
| scratch space | A temporary execution surface, often local to one machine or node, that is not itself a contract surface. |
| policy evidence | The files, dry-runs, and audit bundles that let a reviewer compare operating contexts honestly. |
| profile audit | A side-by-side review of profiles and dry-runs to confirm that context differences remain policy rather than semantic drift. |

## How to use these terms

If an operating-context discussion starts to feel vague, ask which term has become unclear:

- is this a policy difference or a semantic leak?
- is this output on scratch or on a trusted contract path?
- is this retry change explaining failures or postponing diagnosis?

That question usually exposes the real operating-boundary issue quickly.
