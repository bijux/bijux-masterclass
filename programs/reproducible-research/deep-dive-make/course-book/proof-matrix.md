<a id="top"></a>

# Proof Matrix

This page maps the course's main claims to the commands and files that prove them.

Use it when you know what concept you care about but want the fastest evidence route.

---

## Core Build Claims

| Claim | Command | File surfaces |
| --- | --- | --- |
| the graph converges after a successful build | `gmake -C capstone selftest` | `capstone/Makefile`, `capstone/tests/run.sh` |
| parallelism does not change artifact meaning | `gmake -C capstone selftest` | `capstone/tests/run.sh`, `capstone/repro/` |
| discovery is deterministic | `gmake -C capstone discovery-audit` | `capstone/mk/objects.mk` |
| hidden inputs are modeled explicitly | `gmake -C capstone --trace all` | `capstone/mk/stamps.mk` |
| generated files are treated as graph nodes | `gmake -C capstone --trace dyn` | `capstone/Makefile`, `capstone/scripts/gen_dynamic_h.py` |

[Back to top](#top)

---

## Operational Claims

| Claim | Command | File surfaces |
| --- | --- | --- |
| the build has a stable public API | `gmake -C capstone help` | `capstone/Makefile` |
| the build can explain rebuild behavior | `gmake -C capstone --trace all` | `capstone/Makefile`, `capstone/mk/*.mk` |
| the build declares portability boundaries | `gmake -C capstone portability-audit` | `capstone/mk/contract.mk` |
| the build produces non-contaminating evidence | `gmake -C capstone attest` | `capstone/Makefile`, `build/attest.txt` |
| the repro pack teaches real failure classes | `gmake -C capstone repro` | `capstone/repro/`, `repro-catalog.md` |

[Back to top](#top)

---

## Review Claims

| Question | Best first command | Best first file |
| --- | --- | --- |
| why did this rebuild | `gmake -C capstone --trace all` | `capstone/mk/stamps.mk` |
| why is `-j` unsafe | `gmake -C capstone selftest` | `capstone/repro/01-shared-log.mk` |
| where is the build API | `gmake -C capstone help` | `capstone/Makefile` |
| how is code generation modeled | `gmake -C capstone --trace dyn` | `capstone/scripts/gen_dynamic_h.py` |
| what would I review before migration | `gmake -C capstone -p > build/review.dump` | `capstone/mk/` |

[Back to top](#top)

---

## Companion Pages

The most useful companion pages for this matrix are:

* [`command-guide.md`](command-guide.md)
* [`public-targets.md`](public-targets.md)
* [`practice-map.md`](practice-map.md)
* [`capstone-file-guide.md`](capstone-file-guide.md)

[Back to top](#top)
