# Module Glossary

This glossary belongs to **Module 09: Promotion, Registry Boundaries, and Auditability**
in **Deep Dive DVC**.

Use it to keep the module language stable while you move between the core lessons, the
worked example, the exercises, and capstone review.

## How to use this glossary

Read the directory index first. Return here when a promotion, release bundle, registry, or
audit discussion starts to feel vague.

The goal is not extra theory. The goal is shared language for deciding what downstream
users may trust.

## Terms in this directory

| Term | Meaning in this directory |
| --- | --- |
| promotion | The deliberate act of approving a specific result for downstream use. |
| promoted state | The artifact bundle and evidence that downstream users are allowed to trust. |
| promotion contract | The claim that a promoted result is approved, bounded, and supported by evidence. |
| downstream consumer | A person or system that uses the promoted result without depending on internal pipeline context. |
| release surface | The small, stable set of files exposed for downstream use. |
| release bundle | A versioned group of promoted artifacts and supporting evidence. |
| manifest | A file that lists the contents and roles of the promoted bundle. |
| registry boundary | The named surface, registry entry, or published directory consumers are expected to use. |
| consumer contract | The rule that tells downstream users which files are supported and which internals are not. |
| internal pipeline state | Intermediate, candidate, debug, or implementation files not promised to consumers. |
| audit evidence | Params, metrics, lock evidence, manifests, and notes used to defend promoted state. |
| promoted params | Parameter values copied or recorded as part of the promoted evidence. |
| promoted metrics | Metric values copied or recorded as part of the promoted evidence. |
| lock evidence | Recorded DVC execution state that links promoted artifacts back to declared pipeline state. |
| review note | Human-readable rationale explaining why promotion was accepted and what limits apply. |
| bundle mismatch | A release defect where files in the bundle describe different runs or incompatible evidence. |
| unsupported file | A file present in the repository or bundle that downstream consumers should not depend on. |
| versioned boundary | A release or registry surface with a durable name such as `v1`, not a moving label like `latest`. |

## Stable review questions

Use these questions when the module feels abstract:

- What exactly is being promoted?
- Who may consume it?
- Which files form the release surface?
- Does the manifest list the supported bundle?
- Do promoted params and metrics describe the same state?
- Can the artifact be linked back to DVC lock evidence?
- Which internal files are excluded from the consumer contract?
- Would another maintainer be able to defend this promotion later?
