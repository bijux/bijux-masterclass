<a id="top"></a>

# Command Guide

Deep Dive Snakemake has three command layers: repository root, program directory, and
capstone directory. This page makes those boundaries explicit.

Use it when you know what proof question you have but are not sure where the command
belongs.

---

## Repository Root

Use root-level commands when you want one entrypoint that works across programs.

| Command | What it does |
| --- | --- |
| `make PROGRAM=reproducible-research/deep-dive-snakemake program-help` | show the program Makefile surface |
| `make PROGRAM=reproducible-research/deep-dive-snakemake docs-build` | build the course docs in strict mode |
| `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | build the learner-first capstone walkthrough bundle |
| `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | build the executed capstone proof bundle |
| `make PROGRAM=reproducible-research/deep-dive-snakemake test` | run the course's main verification target |

[Back to top](#top)

---

## Program Directory

Use `programs/reproducible-research/deep-dive-snakemake/` when you want the course-local
surface.

| Command | What it does |
| --- | --- |
| `make help` | show program-level targets |
| `make test` | run the capstone fast verification suite via the program surface |
| `make capstone-walkthrough` | build the learner-first walkthrough bundle |
| `make capstone-tour` | build the executed capstone proof bundle |
| `make clean` | remove program and capstone build artifacts |

[Back to top](#top)

---

## Capstone Directory

Use `capstone/` when you want the raw executable workflow repository.

| Command | What it does |
| --- | --- |
| `make help` | show public capstone targets |
| `make walkthrough` | build the learner-first reading bundle without executing the workflow |
| `make wf-dryrun` | preview the execution plan with printed commands |
| `make verify` | execute the workflow and validate the promoted contract |
| `make confirm` | run formatting, tests, workflow checks, execution, and artifact validation |
| `make tour` | build the executed proof bundle |

[Back to top](#top)

---

## Best Defaults

If you are new:

```sh
make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-snakemake test
```

If you are reviewing the capstone deeply:

```sh
make -C capstone help
make -C capstone verify
make -C capstone confirm
```

[Back to top](#top)
