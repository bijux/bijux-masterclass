<a id="top"></a>

# Platform Setup


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Platform Setup"]
  page["Platform Setup"]
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

Deep Dive DVC depends on more than a `dvc` binary existing somewhere on the machine. The
course assumes a small, explicit platform contract.

This page makes that contract clear before the learner hits avoidable setup failures.

---

## Minimum Tooling

You need:

* Python 3.10 or newer
* Git available on the command line
* DVC available inside the capstone virtual environment
* a writable local filesystem for the capstone remote at `.dvc-remote/`

[Back to top](#top)

---

## Repository Root

The course-level commands use the repository root Makefile:

```sh
make PROGRAM=reproducible-research/deep-dive-dvc program-help
make PROGRAM=reproducible-research/deep-dive-dvc docs-build
```

Use these commands when you want docs or program-level verification.

[Back to top](#top)

---

## Capstone Setup

From `programs/reproducible-research/deep-dive-dvc/capstone/`:

```sh
make install
make dvc-init
make repro
```

That sequence creates the virtual environment, installs DVC plus the capstone package,
initializes `.dvc/`, and configures the local training remote.

[Back to top](#top)

---

## Verify Your Setup

From the capstone directory:

```sh
make help
make walkthrough
make verify
```

If `make verify` succeeds, the capstone can execute, validate the publish bundle, and
read the configured remote-backed state surfaces.

[Back to top](#top)

---

## Common Setup Failures

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `python` or `pip` errors during `make install` | missing supported Python | install Python 3.10+ and recreate the virtual environment |
| `dvc` commands fail after install | virtual environment not created or not used through `make` | rerun `make install` and invoke DVC through the Make targets |
| `recovery-drill` fails to restore state | `.dvc-remote/` missing or not writable | rerun `make dvc-init` and verify local filesystem permissions |
| `docs-build` fails while capstone commands work | docs virtual environment missing | run `make PROGRAM=reproducible-research/deep-dive-dvc docs-build` from the repository root |

[Back to top](#top)
