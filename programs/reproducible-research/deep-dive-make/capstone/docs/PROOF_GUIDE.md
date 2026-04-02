<a id="top"></a>

# Proof Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  guide["Capstone docs"]
  section["PROOF_GUIDE"]
  page["Proof Guide"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  orient["Read the guide boundary"] --> inspect["Inspect the named files, targets, or artifacts"]
  inspect --> run["Run the confirm, demo, selftest, or proof command"]
  run --> compare["Compare output with the stated contract"]
  compare --> review["Return to the course claim with evidence"]
```
<!-- page-maps:end -->

This capstone is designed to prove build-system properties, not just compile a small C
program. Use this guide when you want the shortest route from a claim to the target, file,
or failure surface that defends it.

When you want one bounded review pass instead of a custom sequence, run `make proof`.
That target writes the walkthrough, selftest report, contract audit, and incident audit
bundles together, and now includes the profile audit as part of the sanctioned review set.

---

## Claims And Their First Evidence

| Claim | First target | First files to inspect |
| --- | --- | --- |
| what is the smallest honest review entrypoint | `make inspect` | `CONTRACT_AUDIT_GUIDE.md`, `TARGET_GUIDE.md` |
| the graph is truthful and reaches a stable state | `make selftest` | `Makefile`, `tests/run.sh` |
| serial and parallel schedules mean the same thing | `make selftest` | `tests/run.sh`, `mk/objects.mk`, `mk/stamps.mk` |
| the executed proof can be reviewed later without terminal scrollback | `make verify-report` | `SELFTEST_GUIDE.md`, `summary.txt`, `serial.sum`, `parallel.sum` |
| generated files are modeled as real edges | `make dyn` | `scripts/gen_dynamic_h.py`, `Makefile`, `repro/04-generated-header.mk` |
| artifact publication is atomic | `make all` | `Makefile`, `mk/macros.mk` |
| deterministic discovery is rooted and reviewable | `make discovery-audit` | `Makefile`, `mk/objects.mk` |
| the build boundary is portable enough to be explicit | `make portability-audit` | `Makefile`, `mk/contract.mk` |
| execution-policy assumptions are explicit enough to audit | `make profile-audit` | `PROFILE_AUDIT_GUIDE.md`, `mk/contract.mk`, `help.txt`, `origins.txt` |
| failure classes are teachable instead of folklore | `make repro` | `repro/`, `REPRO_GUIDE.md` |

[Back to top](#top)

---

## Best Reading Order

Use this order the first time:

1. `README.md` for the repository contract
2. `TARGET_GUIDE.md` for the public interface by question
3. `Makefile` for the public interface implementation
4. `tests/run.sh` for the proof harness
5. `ARCHITECTURE.md` and `mk/contract.mk` for platform and ownership boundaries
6. `mk/objects.mk` and `mk/stamps.mk` for graph truth
7. `REPRO_GUIDE.md` and `repro/` for failure teaching surfaces

That route keeps contract and proof ahead of implementation detail.

[Back to top](#top)

---

## Best Targets By Question

| Question | First target | Why |
| --- | --- | --- |
| what is the sanctioned end-to-end learner proof route | `make proof` | it writes the bounded bundle set used by the course-book review pages |
| what is the smallest bounded review route | `make inspect` | it writes the public-boundary review bundle without forcing the full proof path |
| does the build still tell the truth after a successful run | `make selftest` | it checks convergence and negative hidden-input behavior |
| how do I preserve the current proof result for later review | `make verify-report` | it writes the selftest evidence bundle with reading-order guides |
| which parts of the build are safe under `-j` | `make selftest` | it compares serial and parallel artifact hashes |
| what is publicly supported for learners and reviewers | `make help` | it exposes the stable command surface |
| where do the common defects live in miniature form | `make repro` | it lists the curated failure pack |
| what assumptions does this capstone make about platform and tools | `make portability-audit` | it prints the declared execution boundary |
| what is the strongest published confirmation route | `make confirm` | it aliases the strongest built-in validation with shared catalog naming |

[Back to top](#top)

---

## Companion Surfaces

Use these files together:

* `README.md` for the repository contract
* `TARGET_GUIDE.md` for stable target selection
* `ARCHITECTURE.md` for ownership boundaries
* `WALKTHROUGH_GUIDE.md` for first-pass reading order
* `CONTRACT_AUDIT_GUIDE.md` for public-boundary review
* `INCIDENT_REVIEW_GUIDE.md` for executed failure review
* `PROFILE_AUDIT_GUIDE.md` for execution-policy review
* `REPRO_GUIDE.md` for the failure-class route
* `tests/run.sh` for the strongest proof path
* `mk/contract.mk` for boundary declarations
* `mk/common.mk` and `mk/macros.mk` for reusable build mechanics

[Back to top](#top)
