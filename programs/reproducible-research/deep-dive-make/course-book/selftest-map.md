<a id="top"></a>

# Selftest Map


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Selftest Map"]
  page["Selftest Map"]
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

`selftest` is the most important executable proof in Deep Dive Make. This page maps each
step of the harness to the build claim it is defending.

Use it when you want to understand why `selftest` is stronger than `make all`.

---

## Selftest Steps

| Step in `tests/run.sh` | What it proves | Main files |
| --- | --- | --- |
| convergence | a successful build reaches an up-to-date state | `capstone/Makefile`, `capstone/tests/run.sh` |
| serial-parallel equivalence | `-j` changes throughput, not artifact meaning | `capstone/tests/run.sh`, `capstone/repro/` |
| trace guardrail | observability cost is bounded instead of drifting silently | `capstone/tests/run.sh`, `capstone/Makefile` |
| hidden input detection | the harness can detect a lying graph rather than only happy paths | `capstone/tests/run.sh`, `capstone/mk/stamps.mk` |

[Back to top](#top)

---

## Why This Matters

`make all` tells you the build succeeded once. `selftest` tells you whether the build
contract is still honest.

That distinction is why the course keeps returning to `selftest` when it talks about
proof, not only compilation.

[Back to top](#top)

---

## Best Reading Order

1. `capstone/Makefile`
2. `capstone/tests/run.sh`
3. this page
4. `make -C capstone selftest`

That order keeps the learner anchored in contract, then harness, then executed proof.

[Back to top](#top)

---

## Best Companion Pages

Use these pages with this map:

* [`capstone-proof-checklist.md`](capstone-proof-checklist.md)
* [`proof-matrix.md`](proof-matrix.md)
* [`capstone-review-worksheet.md`](capstone-review-worksheet.md)

[Back to top](#top)
