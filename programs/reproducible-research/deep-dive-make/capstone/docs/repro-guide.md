# Repro Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  guide["Capstone docs"]
  section["Docs"]
  page["Repro Guide"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  orient["Read the guide boundary"] --> inspect["Inspect the named files, targets, or artifacts"]
  inspect --> run["Run the confirm, demo, selftest, or proof command"]
  run --> compare["Compare output with the stated contract"]
  compare --> review["Return to the course claim with evidence"]
```
<!-- page-maps:end -->

The repro pack turns build failures into reviewable failure surfaces. Use it
when you want to study one failure class at a time instead of treating concurrency and
graph defects as random incidents.
When you want one curated executed example instead of choosing a repro by hand, use
`make incident-audit` and read `INCIDENT_REVIEW_GUIDE.md`.

---

## Repro Files By Failure Class

| File | Failure class | What it teaches |
| --- | --- | --- |
| `repro/shared-log-interleaving.mk` | shared mutable output | concurrent writers need isolated or atomic publication |
| `repro/shared-staging-collision.mk` | shared staging path | each publisher needs uniquely owned staging state |
| `repro/clock-based-stamp.mk` | dishonest stamp boundary | stamps cannot hide meaningful inputs |
| `repro/generated-header-edge.mk` | generated dependency modeling | generated headers must be declared as real edges |
| `repro/directory-creation-race.mk` | directory creation race | directory setup must be idempotent and correctly scoped |
| `repro/order-only-dependency-misuse.mk` | order-only misuse | ordering constraints do not replace semantic dependencies |
| `repro/pattern-rule-ambiguity.mk` | ambiguous rule selection | pattern rules must remain legible under growth |

---

## Best First Route

Use this route when the repro pack is new:

1. `repro/shared-log-interleaving.mk` for obvious schedule-dependent output
2. `repro/directory-creation-race.mk` for setup races that often hide in "small" builds
3. `repro/order-only-dependency-misuse.mk` for graph lies that still look tidy
4. `repro/generated-header-edge.mk` for generated-file truthfulness

That route moves from visible failure into subtler graph-modeling mistakes.

---

## Incident Bundle Route

Use this when you want a saved executed incident review:

1. Run `make incident-audit`.
2. Read `INCIDENT_REVIEW_GUIDE.md`.
3. Read `command.txt`, `run.txt`, and `exit-status.txt`.
4. Read the copied repro makefile.
5. Return to `PROOF_GUIDE.md` to match the repair to the real capstone.

---

## Review Questions

Ask these while using a repro:

* which output is being shared dishonestly
* which dependency is missing or misclassified
* whether the failure changes under `-j`
* which repair pattern belongs in the real capstone
