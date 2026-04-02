# Capstone Architecture Guide

<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive DVC"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone Architecture Guide"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

Use this guide when the DVC capstone feels understandable at the repository level but not
yet at the ownership level.

## Architectural route

- declaration lives in `dvc.yaml`, `params.yaml`, and the repository README
- execution logic lives in `src/incident_escalation_capstone/`
- promotion logic lives in `publish.py` and `publish/v1/`
- contract enforcement lives in `verify.py`
- review packaging lives in the capstone Makefile targets and generated bundles

## Best reading order

1. Read `capstone/README.md`.
2. Read `capstone/ARCHITECTURE.md`.
3. Read `capstone/dvc.yaml` and `capstone/dvc.lock`.
4. Read one implementation file from `src/incident_escalation_capstone/`.
5. Run the proof command that matches the question you are asking.

## Best companion pages

- [Repository Layer Guide](repository-layer-guide.md)
- [Capstone File Guide](capstone-file-guide.md)
- [Capstone Map](capstone-map.md)
- [Verification Route Guide](../reference/verification-route-guide.md)
