# Glossary

Use this glossary to keep the language of Module 08 stable while you move between the core
lessons, worked example, and exercises.

The goal is not more jargon. The goal is to make sure the same release fact keeps the same
name whenever you explain a target promise, a bundle boundary, or a verification file.

## How to use this glossary

If a release discussion starts drifting into vague phrases like "the artifact sort of
contains everything we need" or "install mostly works," stop and look up the term doing the
most work in the argument. Module 08 becomes much clearer when the team agrees on the right
nouns.

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| artifact identity | The stable published content that defines what the release artifact actually is. |
| artifact evidence | Supporting proof about the artifact, such as attestations or diagnostics, that may live beside the artifact rather than inside its core identity. |
| bundle manifest | A file that records stable information about the packaged contents or release tree. |
| checksum | A verification description of an artifact's bytes, usually tied to artifact identity. |
| destination contract | The declared meaning of an `install` route: where files go, how reruns behave, and what tree is being published. |
| distribution target | A public release-oriented target such as `dist` that promises a specific packaged result. |
| idempotent install | An install behavior where rerunning the route produces the same intended destination tree rather than compounding side effects. |
| package truth | The correctness of the release bundle contents and layout. |
| publication boundary | The point after which a release artifact or installed tree may be trusted by another system. |
| publish truth | The correctness of the final publication act, such as archive creation or installation into a destination tree. |
| release contract | The stable promise made by a release-oriented target or bundle layout. |
| release evidence policy | The rule for deciding which proof files belong inside the artifact, beside it, or outside the release entirely. |
| release surface | The collection of release-oriented targets and artifact boundaries that users and automation are allowed to trust. |
| sidecar evidence | A proof file published alongside an artifact rather than embedded inside its identity. |
| staged bundle tree | A temporary or intermediate directory that assembles the intended release layout before final publication. |
| unstable identity | A broken release state where the artifact changes between runs because unstable evidence or noise is treated as core content. |
| install root | The destination boundary for installation, often built from `DESTDIR` and `PREFIX`. |

## The vocabulary standard for this module

When you explain a Module 08 incident, aim to say things like:

- "`dist` has contract drift"
- "that file belongs outside the bundle as sidecar evidence"
- "the manifest describes package truth"
- "install needs an explicit destination contract"
- "the failure is in publish truth, not build truth"

Those sentences are much more useful than saying only "the release step is weird."
