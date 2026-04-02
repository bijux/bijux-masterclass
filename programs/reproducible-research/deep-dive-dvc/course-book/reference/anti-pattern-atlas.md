<a id="top"></a>

# Anti-Pattern Atlas


<!-- page-maps:start -->
## Reference Position

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive DVC"]
  program --> reference["Anti-Pattern Atlas"]
  reference --> review["Design or review decision"]
  review --> capstone["Capstone proof surface"]
```

```mermaid
flowchart TD
  trigger["Hit a naming, boundary, or trade-off question"] --> lookup["Use this page as a glossary, map, rubric, or atlas"]
  lookup --> compare["Compare the current code or workflow against the boundary"]
  compare --> decision["Turn the comparison into a keep, change, or reject call"]
```
<!-- page-maps:end -->

Read the first diagram as a lookup map: this page is part of the review shelf, not a first-read narrative. Read the second diagram as the reference rhythm: arrive with a concrete ambiguity, compare the current work against the boundary on the page, then turn that comparison into a decision.

This page is the missing failure crosswalk for Deep Dive DVC. It exists because humans
rarely remember course structure by module title during a real reproducibility problem.
They remember symptoms, smells, and clumsy patterns.

Use this page when the question is “what kind of bad DVC idea is this?” rather than
“which module was that in?”

---

## Common Anti-Patterns

| Anti-pattern | Why it is clumsy | Primary modules | First proof or review route |
| --- | --- | --- | --- |
| path names treated as identity | location is mistaken for recoverable truth | 01, 02 | `capstone-verify` |
| environments treated as background luck | runtime drift is excluded from the state model | 03 | `capstone-verify` |
| `dvc.yaml` and `dvc.lock` telling different stories | declared and recorded execution drift apart | 04 | `capstone-repro` |
| metrics compared after semantic meaning changed | comparisons turn decorative instead of trustworthy | 05 | `capstone-verify-report` |
| experiments treated as freedom without baseline discipline | changed runs muddy the state story | 06 | `capstone-experiment-review` |
| collaboration that depends on private cache state | another person cannot trust or restore the repo | 07, 08 | `capstone-recovery-review` |
| release surfaces that mirror internal repository complexity | downstream trust becomes too large and too vague | 09 | `capstone-release-review` |
| DVC kept as owner after its boundary is exceeded | governance and migration drift become chronic | 10 | `capstone-confirm` |

[Back to top](#top)

---

## Symptom To Anti-Pattern

| Symptom | Likely anti-pattern | Better question |
| --- | --- | --- |
| “the data path is stable, so we are reproducible” | path is standing in for identity | what content-addressed state actually proves the claim |
| “the pipeline reran, so the result is trustworthy” | rerun is standing in for explicit state truth | which inputs, params, and environment assumptions were actually declared |
| “the metric changed, but I do not know whether it means anything” | semantic meaning drifted | what stayed comparable across runs |
| “the repo works here, but I do not know what survives elsewhere” | local cache and remote durability were never separated | which layer is authoritative after local loss |
| “the published bundle exists, but I still do not trust it” | promoted state is larger or blurrier than it should be | what smaller contract is safe for downstream use |

[Back to top](#top)

---

## Repair Direction

When you identify an anti-pattern, do not jump straight to rewriting everything.

Use this order:

1. name the failure class precisely
2. find the matching module and repository review route
3. inspect the authoritative layer
4. apply the narrowest repair that restores state truth

This keeps the course aligned with real maintenance work instead of theatrical refactoring.

[Back to top](#top)

---

## Best Companion Pages

Use these with the atlas:

* [`authority-map.md`](authority-map.md) for state-layer review
* [`module-dependency-map.md`](module-dependency-map.md) for where the idea is taught in sequence
* [`capstone-map.md`](../guides/capstone-map.md) for module-aware repository routing
* [`verification-route-guide.md`](verification-route-guide.md) for narrower proof selection

[Back to top](#top)
