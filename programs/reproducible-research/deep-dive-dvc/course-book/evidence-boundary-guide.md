<a id="top"></a>

# Evidence Boundary Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Evidence Boundary Guide"]
  page["Evidence Boundary Guide"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Deep Dive DVC asks learners to compare several kinds of evidence that sound similar but
settle different questions.

Use this guide when you need to know which artifact proves declaration, execution,
comparison, promotion, or recovery.

---

## Evidence Types

| Evidence type | Main surfaces | What it proves | What it does not prove |
| --- | --- | --- | --- |
| declared workflow evidence | `capstone/dvc.yaml`, `capstone/params.yaml` | what the repository claims should influence execution | that the declared workflow has already run |
| recorded execution evidence | `capstone/dvc.lock` | the dependency and output state captured after execution | the downstream release contract by itself |
| tracked comparison evidence | `capstone/metrics/metrics.json`, `capstone/params.yaml` | what comparisons are meant to remain semantically stable | that a downstream consumer should trust every internal artifact |
| promoted release evidence | `capstone/publish/v1/manifest.json`, `capstone/publish/v1/metrics.json`, `capstone/publish/v1/params.yaml` | what the repository intentionally exports for downstream trust | the full internal training or experimentation story |
| recovery evidence | `make -C capstone recovery-drill`, DVC remote state | that tracked artifacts can be restored after local loss | that the repository is pedagogically clear or well-governed |

[Back to top](#top)

---

## Which Evidence To Reach For First

| Question | Start with |
| --- | --- |
| what does this repository say should matter | declared workflow evidence |
| what exact state did the pipeline record | recorded execution evidence |
| are these params and metrics safe to compare | tracked comparison evidence |
| what can a downstream reviewer rely on | promoted release evidence |
| what survives when local material is deleted | recovery evidence |

[Back to top](#top)

---

## Evidence Progression

Read the evidence in this order:

1. declaration
2. recorded execution
3. comparison surfaces
4. promoted contract
5. recovery proof

That sequence mirrors the course: first understand what the repository claims, then what
it recorded, then what remains comparable, then what gets promoted, then what survives
time and loss.

[Back to top](#top)

---

## Common Evidence Mistakes

| Mistake | Why it fails |
| --- | --- |
| treating `dvc.yaml` as sufficient proof | declaration is not recorded execution |
| treating `metrics/metrics.json` as the publish contract | internal comparison surfaces are not the same as promoted trust surfaces |
| treating `publish/v1/` as the whole repository story | release evidence is intentionally smaller than internal evidence |
| treating recovery success as proof that comparisons remain meaningful | durability alone does not preserve semantic clarity |

[Back to top](#top)

---

## Best Companion Pages

The most useful companion pages for this guide are:

* [`authority-map.md`](authority-map.md)
* [`proof-matrix.md`](proof-matrix.md)
* [`capstone-map.md`](capstone-map.md)
* [`repository-layer-guide.md`](repository-layer-guide.md)

[Back to top](#top)
