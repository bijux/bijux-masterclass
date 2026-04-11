# Capstone File Guide

Use this page when you know the repository is the right surface but do not yet know which
file owns the answer. The goal is to shorten the path from question to owning file.

## Start with the file that owns the question

| If the question is about... | Open this file first | Then open |
| --- | --- | --- |
| what the pipeline declares it will do | `capstone/dvc.yaml` | `capstone/dvc.lock` |
| what the last recorded execution actually resolved | `capstone/dvc.lock` | the matching stage implementation under `src/incident_escalation_capstone/` |
| which parameters are part of comparable state | `capstone/params.yaml` | the declared `params:` keys in `capstone/dvc.yaml` |
| how publish artifacts are assembled and promoted | `capstone/src/incident_escalation_capstone/publish.py` | `capstone/publish/v1/manifest.json` |
| how promoted state is verified | `capstone/src/incident_escalation_capstone/verify.py` | `capstone/tests/test_verify.py` |
| what downstream users are allowed to trust | `capstone/publish/v1/manifest.json` | [Release Review Guide](release-review-guide.md) |
| what survives local loss and remote restore | `capstone/.dvc-remote/` as the durability source, then `capstone/dvc.lock` | [Recovery Review Guide](recovery-review-guide.md) |
| what learner-facing proof routes exist | `capstone/Makefile` | [Command Guide](command-guide.md) |

## Directory responsibilities

| Path | What belongs there |
| --- | --- |
| `capstone/dvc.yaml` | declared stage graph and tracked dependencies |
| `capstone/dvc.lock` | recorded execution state |
| `capstone/params.yaml` | declared control surface |
| `capstone/src/incident_escalation_capstone/` | implementation of preparation, fitting, evaluation, publication, inspection, and verification |
| `capstone/state/`, `capstone/metrics/`, `capstone/models/`, `capstone/data/derived/` | internal repository outputs and intermediate state |
| `capstone/publish/v1/` | promoted downstream-facing contract |
| `capstone/.dvc-remote/` | local training remote used to prove recovery |
| `capstone/tests/` | executable checks for code-level and contract-level behavior |

## Architectural route

Use this sequence when the repository is understandable at the directory level but not
yet at the ownership level:

1. [DVC Capstone Guide](index.md)
2. `capstone/dvc.yaml` and `capstone/dvc.lock`
3. one implementation file under `capstone/src/incident_escalation_capstone/`
4. the matching review route for the current question

That keeps the capstone centered on declaration, recorded state, implementation, and
review packaging in the same order the repository is meant to be read.

### Ownership boundaries

| Layer | Main surfaces | Responsibility |
| --- | --- | --- |
| repository contract | `README.md`, [DVC Capstone Guide](index.md) | explain what the repository is trying to prove |
| declared workflow | `capstone/dvc.yaml`, `capstone/params.yaml` | declare the intended execution graph and control surface |
| recorded workflow state | `capstone/dvc.lock` | record the exact state transition after execution |
| implementation | `capstone/src/incident_escalation_capstone/` | implement the stages the workflow declares |
| promoted contract | `capstone/publish/v1/` | expose the smaller, reviewable bundle downstream users may trust |
| contract enforcement | `capstone/src/incident_escalation_capstone/verify.py` | validate the promoted contract against the supported rules |
| review packaging | `capstone/Makefile` targets and generated bundles | package saved evidence for later inspection |

## Layer questions

Use this table when the repository feels crowded and you need to know which layer you
are actually reading.

| Question | Best layer to inspect first |
| --- | --- |
| what is this repository promising to defend | repository contract |
| what should happen when the pipeline runs | declared workflow |
| what did happen on the recorded run | recorded workflow state |
| where is the behavior actually implemented | implementation |
| which generated artifacts are only internal | internal repository outputs |
| what may a downstream reviewer rely on | promoted contract |
| what survives local loss | recovery durability |
| what makes one changed run meaningfully comparable to the baseline | declared workflow plus promoted contract |

## Good first reading order

If this is your first serious repository pass, use this sequence:

1. `capstone/dvc.yaml`
2. `capstone/dvc.lock`
3. `capstone/params.yaml`
4. `capstone/Makefile`
5. `capstone/src/incident_escalation_capstone/publish.py`
6. `capstone/src/incident_escalation_capstone/verify.py`
7. `capstone/publish/v1/manifest.json`
8. one route page that matches your question: experiment, recovery, or release

That order keeps declaration first, recorded state second, enforcement third, and
promotion last.

## Wrong reading orders

Avoid these:

- opening implementation files before reading `dvc.yaml`
- treating `publish/v1/` as the whole repository story
- reading `dvc.lock` before you know what `dvc.yaml` declared
- using folder names as a substitute for authority and ownership

If you are still navigating by directory names alone, the repository has not become
legible yet.

## Best companion pages

The most useful companion pages for this guide are:

* [`capstone-map.md`](capstone-map.md)
* [`command-guide.md`](command-guide.md)
* [`authority-map.md`](../reference/authority-map.md)
* [`proof-matrix.md`](../guides/proof-matrix.md)

