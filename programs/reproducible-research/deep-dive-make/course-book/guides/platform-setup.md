<a id="top"></a>

# Platform Setup

Use this page before you trust local results. Deep Dive Make depends on GNU Make features
that are not available in every default `make`, especially on macOS. The goal here is
not to produce a perfect workstation. The goal is to prove you are running the same class
of toolchain the course assumes.

## What you need

The program assumes:

- GNU Make 4.3 or newer
- a POSIX shell at `/bin/sh`
- a working C compiler
- Python 3 for helper scripts inside the capstone

If one of those is missing, the course can still teach concepts, but the executable proof
routes stop being trustworthy.

[Back to top](#top)

## First check

Run these from the repository root:

```sh
make PROGRAM=reproducible-research/deep-dive-make program-help
make PROGRAM=reproducible-research/deep-dive-make test
```

Those commands prove two things quickly:

- the program-level wrapper targets are available
- the selected `make` is good enough to run the capstone selftest route

[Back to top](#top)

## macOS

macOS commonly ships `/usr/bin/make` as GNU Make 3.81. That is too old for this course.

Install a current GNU Make:

```sh
brew install make
```

Then keep the command layers straight:

- from repository root: keep using `make PROGRAM=reproducible-research/deep-dive-make ...`
- from `programs/reproducible-research/deep-dive-make/`: use `make ...`
- from `programs/reproducible-research/deep-dive-make/capstone/`: use `gmake ...`

The first two layers call the program wrappers. The last layer runs the raw capstone
build directly.

[Back to top](#top)

## Linux

Most Linux distributions already ship a compatible GNU Make, but check anyway:

```sh
make --version | head -1
```

If the version is older than 4.3, upgrade it before relying on any proof output.

[Back to top](#top)

## Raw capstone check

When you want to verify the executable reference build directly, run:

```sh
gmake -C programs/reproducible-research/deep-dive-make/capstone help
gmake -C programs/reproducible-research/deep-dive-make/capstone selftest
```

On Linux, replace `gmake` with `make` only after confirming `make --version` reports GNU
Make 4.3 or newer.

[Back to top](#top)

## Common setup failures

| Symptom | Likely cause | What to fix |
| --- | --- | --- |
| grouped target or recipe-prefix errors | old GNU Make | install or invoke GNU Make 4.3+ |
| docs say one command, local shell needs another | wrong command layer | decide whether you are at repo root, program root, or capstone root |
| selftest fails before build logic is exercised | missing compiler or broken shell assumption | verify `cc` and `/bin/sh` first |
| helper scripts fail | missing Python 3 | install Python 3 and rerun the capstone route |

[Back to top](#top)

## Good stopping point

Stop when you can answer three questions clearly:

- which `make` binary you are using
- which command layer you are currently in
- whether the failure is a setup problem or a course concept you still need to learn

[Back to top](#top)
