# Glossary

This glossary keeps the language of Module 02 stable.

The goal is practical clarity: when you keep identity, location, storage, and trust layers
distinct, DVC stops feeling mystical and starts feeling inspectable.

## Terms

| Term | Meaning in this module |
| --- | --- |
| locator | A path or name that tells you where something is expected to be found, without being a durable identity by itself. |
| data identity | The claim that the system is talking about the same exact content rather than only the same path or filename. |
| content addressing | Identifying tracked data by its content rather than by its location. |
| pointer file | A small DVC-tracked file such as a `.dvc` file that records a reference to tracked content identity. |
| local cache | DVC's local content store that makes recorded identity operationally restorable on the machine. |
| remote durability | Off-machine storage that makes tracked content recoverable after local loss. |
| workspace projection | The current visible file in the working tree that reflects tracked content but is not the full identity story by itself. |
| recorded execution state | The DVC-tracked record of what the pipeline actually ran, typically represented by `dvc.lock`. |
| published release state | The smaller downstream-facing release boundary, such as `publish/v1/`, that is meant for review and trust by others. |
| state move | A command effect that changes which layer holds tracked content, such as push to remote or checkout to workspace. |
| recovery route | The commands and evidence that prove tracked content can be restored after loss. |
| authority layer | The layer that is authoritative for a specific question, such as workspace visibility, recorded execution, remote durability, or downstream trust. |

## How to use these terms

If Module 02 starts feeling fuzzy, ask which term has blurred:

- are we talking about a locator or an identity?
- is this the workspace projection or the recorded execution state?
- is the question about remote durability or published release trust?
- did a command move content between layers, or are we only describing a visible file?

Those questions usually turn confusion back into a reviewable DVC story.
