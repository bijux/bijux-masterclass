<a id="top"></a>

# Capstone Walkthrough

This walkthrough gives the capstone a teaching route, not just a repository map.

Use it when you want a bounded tour of the reference build with a clear question at each
step.

---

## 30-Minute Tour

Use this when you want the minimum useful capstone pass.

1. Run `make -C capstone walkthrough`
2. Run `make -C capstone help`
3. Read `capstone/Makefile` and identify the public targets
4. Read `capstone/tests/run.sh` and list the invariants it proves
5. Run `make -C capstone selftest`
6. Inspect one repro under `capstone/repro/`

Goal: leave with a clear picture of what the capstone promises and how it proves it.

[Back to top](#top)

---

## 60-Minute Tour

Use this after Modules 03-06.

1. Follow object discovery in `capstone/mk/objects.mk`
2. Follow modeled inputs in `capstone/mk/stamps.mk`
3. Trace generated header production from `scripts/gen_dynamic_h.py`
4. Run `make -C capstone --trace dyn`
5. Compare the build contract in the docs to the behavior you observed

Goal: see how truthful graph modeling survives a more realistic repository.

[Back to top](#top)

---

## 90-Minute Steward Tour

Use this during Modules 07-10.

1. Read `capstone/Makefile` for public API boundaries
2. Read `capstone/mk/*.mk` for layer responsibilities
3. Inspect `capstone/scripts/mkdist.py` for release boundary design
4. Review `capstone/repro/` as migration-risk examples
5. Run `make -C capstone hardened`

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
