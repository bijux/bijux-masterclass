# Capstone File Guide

Use this page when you know the repository is the right surface but do not yet know which
file owns the answer. The goal is to shorten the path from question to owning file.

## Start with the file that owns the question

| If the question is about... | Open this file first | Then open |
| --- | --- | --- |
| what the capstone publicly supports | `capstone/Makefile` | [Command Guide](command-guide.md) |
| what the build proves about itself | `capstone/tests/run.sh` | [Capstone Proof Guide](capstone-proof-guide.md) |
| tool, shell, and policy assumptions | `capstone/mk/contract.mk` | `capstone/Makefile` |
| shared helper behavior such as atomic writes | `capstone/mk/macros.mk` | `capstone/mk/common.mk` |
| which sources and objects enter the graph | `capstone/mk/objects.mk` | `capstone/src/` |
| how hidden inputs and state evidence are modeled | `capstone/mk/stamps.mk` | `capstone/tests/run.sh` |
| generated-header behavior | `capstone/scripts/gen_dynamic_h.py` | `capstone/Makefile` |
| source and release packaging | `capstone/scripts/mkdist.py` | `course-book/capstone-docs/target-guide.md` |
| one failure class in isolation | `capstone/repro/01-shared-log.mk` or another repro file | [Capstone Proof Guide](capstone-proof-guide.md) |

## Directory responsibilities

| Path | What belongs there |
| --- | --- |
| `capstone/Makefile` | public targets and top-level composition |
| `capstone/mk/` | layered policy, graph, and helper mechanics |
| `capstone/src/` and `capstone/include/` | the small C program used to exercise build behavior |
| `capstone/scripts/` | explicit generator and packaging helpers |
| `capstone/tests/` | the proof harness for build-system behavior |
| `capstone/repro/` | controlled failure specimens for one lesson at a time |
| `course-book/capstone-docs/` | repository-local guide pages for bounded review routes |

## Good first reading order

If this is your first serious repository pass, use this sequence:

1. `capstone/Makefile`
2. `capstone/tests/run.sh`
3. `capstone/mk/contract.mk`
4. `capstone/mk/objects.mk`
5. `capstone/mk/stamps.mk`
6. one file under `capstone/repro/`
7. one script under `capstone/scripts/`

That order keeps contract first, proof second, policy third, and failure teaching last.

## Wrong reading orders

Avoid these:

- opening random `mk/*.mk` files before reading `Makefile`
- starting with `repro/` before you know what the healthy build promises
- reading helper scripts before you know why the build calls them
- using directory names as a substitute for ownership

If you are still browsing by folder name, the repository has not become legible yet.
