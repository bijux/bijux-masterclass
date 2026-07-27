# Deep Dive Make Capstone

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  guide["Capstone docs"]
  section["README"]
  page["Deep Dive Make Capstone"]
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

Read the first diagram as the capstone shape. Read the second diagram as the entry rule:
choose the smallest route that answers the current question, then escalate only when the
question changes.

This capstone is the executable reference build for Deep Dive Make. It is a compact C
project used to corroborate the course's main claims about truthful graphs, atomic
publication, parallel safety, determinism, and self-testing. It is not meant to be a
first-contact playground for Make syntax.

## Use this capstone when

- the module idea is already legible and you want executable corroboration
- you need one repository that keeps graph truth, publication, and proof visible together
- you are reviewing whether a small build behaves like a serious build under pressure

## Do not use this capstone when

- you still need first exposure to the concept itself
- you want to browse the whole repository before choosing a question
- the strongest proof route feels safer than naming the current claim

## Choose the entry route by question

| If the question is... | Start here | Escalate only if needed |
| --- | --- | --- |
| what does this repository promise | `make walkthrough` | `make inspect` |
| which targets are public and what they mean | `make inspect` | `make contract-audit` |
| does the build prove convergence and parallel safety | `make selftest` | inspect `summary.txt`, then `make verify-report` |
| does the selftest reject a known schedule defect | `make selftest-harness-tests` | inspect the rejected test bundle |
| does one candidate satisfy the local release contract | `make release-check` | `make confirm` |
| what do the governed build routes cost here | `make perf` | preserve the bundle before comparing another revision |
| do source, header, generator, and generated-consumer changes select only required work | `make performance-incremental` | read the complete summary, then inspect any failing case trace |
| how can a successful Make run leave authored or generated consumers stale | `make incremental-fault-audit` | compare missing-edge and declared-edge traces |
| can clock state, false ordering, or overlapping rules change successful output meaning | `make semantic-fault-audit` | compare all seven broken and control rows |
| can non-file state, recursion, or required tools violate the environment contract | `make environment-contract-audit` | compare each defect with its declared control |
| can private callers, policy scope, or flat paths violate architecture ownership | `make architecture-contract-audit` | compare all six defect and control rows |
| did a macro preserve the explicit rule contract or introduce hidden surfaces | `make abstraction-contract-audit` | compare the explicit, bounded, and opaque models |
| did cost change under compatible context and equivalent work | `make performance-compare` | inspect context, requested work, trusted outputs, then deltas |
| do controlled concurrency faults match their promised signatures | `make incident-audit` | inspect semantic evidence before `make proof` |
| should I trust this as a stewardship specimen | `make proof` | `make confirm` |

From the repository root, the matching course-level commands are:

```sh
make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-make inspect
make PROGRAM=reproducible-research/deep-dive-make proof
```

Inside `capstone/`, use `gmake` on macOS because `/usr/bin/make` is BSD Make.

## First honest pass

1. Run `make walkthrough`.
2. Read [INDEX.md](docs/index.md).
3. Read [WALKTHROUGH_GUIDE.md](docs/walkthrough-guide.md).
4. Run `make inspect`.
5. Read [TARGET_GUIDE.md](docs/target-guide.md).
6. Run `make selftest`.
7. Read [PROOF_GUIDE.md](docs/proof-guide.md).

Stop there first. That is enough to see the public contract, the proof harness, and one
bounded review route without turning the capstone into a browsing exercise.

## What the main targets prove

| Target | What it proves | Why it matters |
| --- | --- | --- |
| `walkthrough` | the learner-facing reading order is bounded and explicit | first capstone contact stays humane |
| `inspect` | the public build contract is visible without the full proof route | review starts from stable surfaces |
| `selftest` | convergence, serial/parallel equivalence, negative hidden-input detection, and raw evidence | the build system is tested as a system |
| `selftest-harness-tests` | truthful schedules pass and controlled artifact drift fails | the proof harness is tested, not merely trusted |
| `verify-report` | passing or failing selftest evidence is completed as a review bundle | proof can be inspected without rerunning |
| `release-check` | one candidate passes archive and contained-install acceptance | release claims bind to exact bytes |
| `performance-incremental` | every governed input class is classified against the same output universe | incremental proof covers more than one convenient mutation |
| `incremental-fault-audit` | missing semantic edges stay stale while declared controls refresh | the evidence route proves it can discriminate graph lies |
| `semantic-fault-audit` | clock, order-only, and pattern-selection models match paired contracts | successful execution is not mistaken for honest semantics |
| `environment-contract-audit` | stale state, hidden recursion, and late tool checks match their paired controls | external facts have explicit evaluation and failure boundaries |
| `architecture-contract-audit` | public caller, include-policy, and output-ownership models match paired contracts | successful builds do not conceal ownership drift |
| `architecture-contract-selftest` | altered architecture controls are rejected | the architecture audit is discriminating, not ceremonial |
| `abstraction-contract-audit` | explicit, bounded, and opaque generation match their promised rule, policy, and publication surfaces | macro brevity is not mistaken for preserved ownership |
| `abstraction-contract-selftest` | altered bounded and opaque models are rejected | the abstraction audit can discriminate hidden targets and policy mutation |
| `perf` | governed scenarios bind provenance, a complete change-impact matrix, samples, and outputs | a local baseline is attributable and reviewable |
| `performance-selftest` | context, rebuild, capture, and comparison dishonesty is rejected | performance claims are gated, not trusted |
| `proof` | the sanctioned review bundles include positive invariants and paired missing-edge controls | stewardship has a durable discriminating route |
| `confirm` | the strongest built-in path, including semantic specimens and rejection tests, still passes | final review is stronger than first-pass learning |

## Repository shape

```mermaid
graph TD
  capstone["capstone/"]
  capstone --> makefile["Makefile"]
  capstone --> mk["mk/"]
  capstone --> src["src/"]
  capstone --> include["include/"]
  capstone --> scripts["scripts/"]
  capstone --> tests["tests/"]
  capstone --> repro["repro/"]
  capstone --> docs["docs/"]
```

Use these areas deliberately:

- `Makefile` for public targets and entrypoints
- `mk/` for layered build responsibilities
- `scripts/` for generator and packaging boundaries
- `tests/` for build-system proof
- `repro/` for controlled failure teaching material
- `docs/` for bounded review routes

## Capstone docs

All capstone documentation lives under `docs/`:

- [ARCHITECTURE.md](docs/architecture.md)
- [ARCHITECTURE_CONTRACT_AUDIT_GUIDE.md](docs/architecture-contract-audit-guide.md)
- [ABSTRACTION_CONTRACT_AUDIT_GUIDE.md](docs/abstraction-contract-audit-guide.md)
- [CONTRACT_AUDIT_GUIDE.md](docs/contract-audit-guide.md)
- [INCIDENT_REVIEW_GUIDE.md](docs/incident-review-guide.md)
- [INDEX.md](docs/index.md)
- [PROFILE_AUDIT_GUIDE.md](docs/profile-audit-guide.md)
- [PERFORMANCE_EVIDENCE_GUIDE.md](docs/performance-evidence-guide.md)
- [PROOF_GUIDE.md](docs/proof-guide.md)
- [RELEASE_GUIDE.md](docs/release-guide.md)
- [REPRO_GUIDE.md](docs/repro-guide.md)
- [INCREMENTAL_FAULT_AUDIT_GUIDE.md](docs/incremental-fault-audit-guide.md)
- [SEMANTIC_FAULT_AUDIT_GUIDE.md](docs/semantic-fault-audit-guide.md)
- [ENVIRONMENT_CONTRACT_AUDIT_GUIDE.md](docs/environment-contract-audit-guide.md)
- [SELFTEST_GUIDE.md](docs/selftest-guide.md)
- [TARGET_GUIDE.md](docs/target-guide.md)
- [WALKTHROUGH_GUIDE.md](docs/walkthrough-guide.md)

## Good stopping point

Stop when you can name:

- the current claim
- the smallest route that proves it
- the next stronger route only if the current one stops being enough
