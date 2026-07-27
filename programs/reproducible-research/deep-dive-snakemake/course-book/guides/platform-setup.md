# Platform Setup

Use this page before your first local run or when setup failures are blurring the lesson.
The goal is simple: get to one truthful workflow proof route without treating toolchain
problems as Snakemake concepts.

## How to use this page

Use this page only for setup and environment honesty.

Read it in this order:

1. choose the safest first route
2. identify the command surface you are actually on
3. verify the toolchain in the listed order
4. stop when setup is no longer the thing that is failing

Once the toolchain is honest, go back to the module or proof route. Do not keep treating
workflow questions as setup questions.

## The safest first route

If the machine is fresh, use the repository-managed toolchain instead of trusting a
random global Snakemake install.

From `programs/reproducible-research/deep-dive-snakemake/capstone/`:

```sh
make bootstrap
make walkthrough
make wf-dryrun
```

That route does three useful things in order:

1. creates the supported local toolchain
2. gives you a guided first pass through the capstone
3. proves the workflow can explain its plan before a full execution

If you want the shortest clean-room setup-and-proof route, run:

```sh
make bootstrap-confirm
```

That target creates the supported toolchain and then runs the strongest confirmation path
without depending on a preinstalled global `snakemake`.

## Start by deciding whether the problem is setup or workflow truth

Beginners often lose time because every early failure feels like a Snakemake lesson.

This page is here to prevent that confusion.

Ask:

- does the failure happen before a supported toolchain exists
- or does it happen after setup succeeded and the workflow is now making a real claim

That distinction changes what you should inspect next.

## What you actually need

You do not need a perfect workstation. You need a small, explicit platform contract:

- Python 3.11 or newer
- a writable local filesystem for the capstone working directories
- Snakemake in the supported `>=9.14,<9.24` window if you are relying on a global binary
- Graphviz `dot` only when you want DAG or rulegraph rendering

If you are unsure about the global Snakemake version, prefer the local bootstrap route.

## Choose the right command surface

| Where you are working | Best starting command | Use it for |
| --- | --- | --- |
| repository root | `make PROGRAM=reproducible-research/deep-dive-snakemake program-help` | seeing the program-owned command surface |
| repository root | `make PROGRAM=reproducible-research/deep-dive-snakemake program-docs-build` | building only this program's docs |
| program root | `make capstone-bootstrap-confirm` | creating the supported capstone toolchain and running clean-room confirmation |
| capstone directory | `make help` | seeing the local capstone targets directly |
| capstone directory | `make bootstrap` | creating the local toolchain before the first workflow run |

## Version policy without the confusion

The teaching baseline stays on Snakemake 9.14.x for clean-room reproducibility, while the
supported working window is `>=9.14,<9.24` for compatible local setups.

That split exists for a reason:

- the pinned baseline keeps classroom and container behavior stable
- the broader window lets local development stay usable without pretending every 9.x build is identical

If your machine falls outside that window, fix the toolchain first. Do not debug course
material against an unsupported Snakemake version and call the result a lesson failure.

## Verify setup in the right order

From the capstone directory:

```sh
make help
make bootstrap
make verify
```

That order matters:

- `help` confirms you are on the right command surface
- `bootstrap` creates the supported toolchain
- `verify` checks that the workflow can execute, publish, and validate its promoted outputs

If `bootstrap` succeeds and `verify` fails, you are past setup and into workflow evidence.
Inspect the failing rule, logs, profile assumptions, or config surfaces before changing
lesson conclusions.

## Common setup failures

| Symptom | Likely cause | First repair move |
| --- | --- | --- |
| `make bootstrap` fails immediately | Python 3.11+ is missing or unavailable to `python3` | install Python 3.11 or newer, then rerun `make bootstrap` |
| `snakemake` is missing in `make info` | no global Snakemake is installed and the local toolchain has not been bootstrapped | run `make bootstrap` or point `SNAKEMAKE` at the intended binary |
| config validation skips unexpectedly | `jsonschema` or `pyyaml` is missing from the active environment | repair the Python environment before trusting validation results |
| `dag` or `rulegraph` fails | Graphviz `dot` is missing | install Graphviz only if you need graph rendering |
| `verify` fails after a successful dry-run | runtime dependencies or filesystem assumptions differ from the planning surface | inspect `profiles/`, `config/`, and the failing rule logs before editing workflow code |

## Good stopping point

Stop when you can do two things:

1. name which command surface you are on
2. run one honest proof route without wondering whether the toolchain itself is lying

## The beginner mistake to catch early

The most common beginner mistake is continuing to widen setup work after the course
already reached a truthful workflow failure.

Once `bootstrap` works and a proof route fails honestly, the next move is usually:

- inspect the failing rule
- inspect the config or profile surface
- inspect the saved evidence route

It is usually not "reinstall everything again."
