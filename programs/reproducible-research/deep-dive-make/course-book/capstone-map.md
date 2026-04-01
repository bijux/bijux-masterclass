<a id="top"></a>

# Deep Dive Make: Capstone Map

The capstone is not the first stop for every lesson. It is the executable cross-check for
the program once a concept is already legible in a smaller local exercise.

Use this page when you want one answer to three questions:

1. When should I enter the capstone?
2. Which files or targets match the module I am studying?
3. What command proves the concept instead of merely describing it?

---

## Recommended Entry Rule

Use the capstone sparingly in Modules 01-02, heavily in Modules 03-09, and as a review
specimen in Module 10.

If you are still learning basic syntax, keep working in the local module playgrounds
first. The capstone is designed to confirm understanding, not replace first-contact
teaching.

---

## Module-to-Capstone Route

| Module | Learner goal | Capstone surfaces | Proof command |
| --- | --- | --- | --- |
| 01 Foundations | See a truthful graph and atomic publication at small scale | `capstone/Makefile`, `capstone/src/`, `capstone/include/` | `make -C capstone -n all` |
| 02 Scaling | Watch parallel safety and deterministic discovery under pressure | `capstone/repro/`, `capstone/mk/objects.mk`, `capstone/tests/run.sh` | `make -C capstone selftest` |
| 03 Production Practice | See CI-stable targets and build-system selftests | `capstone/Makefile`, `capstone/tests/run.sh`, `capstone/mk/macros.mk` | `make -C capstone selftest` |
| 04 Semantics Under Pressure | Inspect precedence, help surface, and optional rule generation | `capstone/Makefile`, `capstone/mk/rules_eval.mk` | `make -C capstone show-origins` |
| 05 Hardening | Confirm portability boundaries, attestations, and guarded recursion | `capstone/mk/contract.mk`, `capstone/Makefile`, `capstone/thirdparty/` | `make -C capstone hardened` |
| 06 Generated Files | Follow the generated-header path and boundary files | `capstone/scripts/`, `capstone/mk/stamps.mk`, `capstone/Makefile` | `make -C capstone --trace dyn` |
| 07 Build Architecture | Read the layered `mk/*.mk` structure as a public API | `capstone/Makefile`, `capstone/mk/*.mk` | `make -C capstone help` |
| 08 Release Engineering | Inspect packaging and evidence surfaces without polluting identity | `capstone/Makefile`, `capstone/scripts/mkdist.py`, `capstone/build/attest.txt` | `make -C capstone dist attest` |
| 09 Incident Response | Measure trace volume and operational diagnostics | `capstone/tests/run.sh`, `capstone/Makefile`, `capstone/repro/` | `make -C capstone trace-count` |
| 10 Mastery | Review the whole build as a migration and governance specimen | `capstone/Makefile`, `capstone/mk/`, `capstone/repro/`, `capstone/tests/` | `make -C capstone help && make -C capstone -p > build/review.dump` |

[Back to top](#top)

---

## First Capstone Tour

If you want a sane first walkthrough, use this order:

1. Read `capstone/Makefile` from the public targets down to the build rules.
2. Read `capstone/mk/objects.mk` and `capstone/mk/stamps.mk` to see discovery and modeled inputs.
3. Read `capstone/tests/run.sh` to see what the build is actually required to prove.
4. Run `make -C capstone selftest` and compare the output to the course claims.

This route keeps the learner focused on contract first, mechanics second.

[Back to top](#top)

---

## Fast Routes by Goal

Use these shortcuts when you are returning later for one kind of question:

| Goal | Start here | Then inspect |
| --- | --- | --- |
| Why did this rebuild? | `make -C capstone --trace all` | `capstone/mk/stamps.mk`, `capstone/mk/objects.mk` |
| Why is `-j` unsafe? | `make -C capstone selftest` | `capstone/repro/`, `capstone/tests/run.sh` |
| How is code generation modeled? | `make -C capstone --trace dyn` | `capstone/scripts/`, generated-header rules in `capstone/Makefile` |
| Where is the public API? | `make -C capstone help` | top-level targets in `capstone/Makefile` |
| What counts as hardened? | `make -C capstone hardened` | `capstone/mk/contract.mk`, `capstone/Makefile` |
| What would I review before migration? | `make -C capstone -p > build/review.dump` | `capstone/mk/`, `capstone/tests/`, `capstone/repro/` |

[Back to top](#top)

---

## Capstone Discipline

Use the capstone correctly:

* read the module first, then verify in the capstone
* trust commands and files more than prose summaries
* prefer one investigation question at a time
* treat repros as training material, not as production patterns

If the capstone ever feels larger than the concept you are studying, step back to the
module playground and return after the smaller exercise makes the graph legible again.

[Back to top](#top)
