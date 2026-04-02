<a id="top"></a>

# Command Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Command Guide"]
  page["Command Guide"]
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

Deep Dive Make has three command layers: repository root, program directory, and capstone
directory. This page makes those boundaries explicit so the learner does not have to guess
where a command belongs.

---

## Repository Root

Use root-level commands when you want one entrypoint that works across programs.

| Command | What it does |
| --- | --- |
| `make PROGRAM=reproducible-research/deep-dive-make test` | run the course's main verification target |
| `make PROGRAM=reproducible-research/deep-dive-make docs-build` | build the course docs in strict mode |
| `make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough` | build the learner-facing walkthrough bundle |
| `make PROGRAM=reproducible-research/deep-dive-make capstone-tour` | print the capstone reading route |
| `make PROGRAM=reproducible-research/deep-dive-make proof` | build the sanctioned learner-facing proof bundle set |
| `make PROGRAM=reproducible-research/deep-dive-make program-help` | show the program Makefile surface |

[Back to top](#top)

---

## Program Directory

Use `programs/reproducible-research/deep-dive-make/` when you want the course-local
surface.

| Command | What it does |
| --- | --- |
| `make help` | show program-level targets |
| `make test` | run the capstone selftest via the program surface |
| `make capstone-walkthrough` | build the learner-facing walkthrough bundle |
| `make capstone-tour` | print the capstone reading route |
| `make proof` | build the sanctioned learner-facing proof bundle set |
| `make capstone-hardened` | run the strongest built-in capstone verification |
| `make clean` | clear program and capstone artifacts |

[Back to top](#top)

---

## Capstone Directory

Use `capstone/` when you want the raw executable reference build.

| Command | What it does |
| --- | --- |
| `gmake help` | show public capstone targets on macOS |
| `gmake walkthrough` | build the learner-facing walkthrough bundle |
| `gmake tour` | print the recommended reading route |
| `gmake selftest` | run convergence, equivalence, and negative checks |
| `gmake proof` | write the sanctioned learner-facing proof bundle set |
| `gmake hardened` | run the strongest capstone validation set |
| `gmake repro` | list the failure-mode repro pack |

[Back to top](#top)

---

## Best Defaults

If you are new:

```sh
make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-make proof
make PROGRAM=reproducible-research/deep-dive-make test
```

If you are reviewing the capstone deeply:

```sh
gmake -C capstone help
gmake -C capstone proof
gmake -C capstone repro
```

[Back to top](#top)
