<a id="top"></a>

# Capstone Walkthrough


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Make"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone Walkthrough"]
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

This walkthrough gives the capstone a teaching route, not just a repository map.

Use it when you want a bounded tour of the reference build with a clear question at each
step.

---

## 30-Minute Tour

Use this when you want the minimum useful capstone pass.

1. Run `make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough`
2. Read the capstone's local [`WALKTHROUGH_GUIDE.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/reproducible-research/deep-dive-make/capstone/WALKTHROUGH_GUIDE.md)
3. Run `make PROGRAM=reproducible-research/deep-dive-make inspect`
4. Read `capstone/Makefile` and identify the public targets with the local [`TARGET_GUIDE.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/reproducible-research/deep-dive-make/capstone/TARGET_GUIDE.md)
5. Read `capstone/tests/run.sh` and list the invariants it proves
6. Run `make PROGRAM=reproducible-research/deep-dive-make test`
7. Inspect one repro under `capstone/repro/`

Goal: leave with a clear picture of what the capstone promises and how it proves it.

[Back to top](#top)

---

## 60-Minute Tour

Use this after Modules 03-06.

1. Read the capstone's local [`ARCHITECTURE.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/reproducible-research/deep-dive-make/capstone/ARCHITECTURE.md)
2. Follow object discovery in `capstone/mk/objects.mk`
3. Follow modeled inputs in `capstone/mk/stamps.mk`
4. Trace generated header production from `scripts/gen_dynamic_h.py`
5. Run `gmake -C capstone --trace dyn`
6. Compare the build contract in the docs to the behavior you observed

Goal: see how truthful graph modeling survives a more realistic repository.

[Back to top](#top)

---

## 90-Minute Steward Tour

Use this during Modules 07-10.

1. Read the capstone's local [`TARGET_GUIDE.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/reproducible-research/deep-dive-make/capstone/TARGET_GUIDE.md)
2. Read the capstone's local [`ARCHITECTURE.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/reproducible-research/deep-dive-make/capstone/ARCHITECTURE.md)
3. Read `capstone/mk/*.mk` for layer responsibilities
4. Inspect `capstone/scripts/mkdist.py` for release boundary design
5. Review `capstone/repro/` as migration-risk examples
6. Run `make PROGRAM=reproducible-research/deep-dive-make capstone-confirm`

Goal: evaluate the capstone as a build-system specimen, not just as a demo.

[Back to top](#top)

---

## Questions To Keep Asking

At every step, ask:

* what is the declared input boundary
* what would break under `-j` if the graph were lying
* which target is public versus internal
* how would another maintainer discover this behavior later

If you cannot answer those, slow down before opening more files.

[Back to top](#top)

---

## Exit Criteria

The walkthrough has done its job when you can:

* explain why `selftest` is stronger than `all`
* point to one modeled hidden input
* point to one deliberate publication boundary
* identify one repro that teaches a real failure class

[Back to top](#top)
