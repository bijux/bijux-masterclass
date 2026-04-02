<a id="top"></a>

# Platform Setup


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Make"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Platform Setup"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

Deep Dive Make depends on GNU Make semantics, not merely on the presence of a `make`
binary. This page makes the platform contract explicit before the learner hits avoidable
tooling failures.

---

## Minimum Tooling

You need:

* GNU Make 4.3 or newer
* a POSIX shell available as `/bin/sh`
* a working C compiler toolchain
* Python 3 for helper scripts in the capstone

[Back to top](#top)

---

## macOS

macOS often ships `/usr/bin/make` as GNU Make 3.81, which does not satisfy the course
requirement.

Install GNU Make:

```sh
brew install make
```

Then use `gmake` for course and capstone commands:

```sh
gmake -C capstone help
gmake -C capstone selftest
```

[Back to top](#top)

---

## Linux

Most Linux distributions already provide a compatible GNU Make, but you should still
verify it:

```sh
make --version | head -1
```

If the reported version is older than 4.3, upgrade before trusting the course results.

[Back to top](#top)

---

## Verify Your Setup

From `programs/reproducible-research/deep-dive-make/`:

```sh
make help
```

From `capstone/`:

```sh
gmake help
gmake selftest
```

Use `make` instead of `gmake` on Linux only if `make --version` confirms GNU Make 4.3+.

[Back to top](#top)

---

## Common Setup Failures

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| grouped-target or pattern support errors | old GNU Make | install GNU Make 4.3+ |
| commands behave differently on macOS than the course says | using `/usr/bin/make` | switch to `gmake` |
| selftest fails before the build logic is really exercised | missing compiler or shell assumptions | verify C toolchain and `/bin/sh` |
| helper scripts fail unexpectedly | missing Python 3 | install Python 3 and rerun |

[Back to top](#top)
