# Target Guide

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  guide["Capstone docs"]
  section["TARGET_GUIDE"]
  page["Target Guide"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  question["Name the question"] --> target["Choose the smallest public target"]
  target --> output["Read the bundle or console output"]
  output --> next["Escalate only if the question changes"]
```
<!-- page-maps:end -->

Use this guide when `make help` gives you names, but not judgment. The point is not to
memorize every target. The point is to pick the smallest command that answers the
question honestly.

---

## Choose by question

| Question | Start here | Escalate if needed |
| --- | --- | --- |
| what does this repository promise publicly | `make inspect` | `make contract-audit` |
| what are the stable public targets | `make help` | `make inspect` |
| does the ordinary build succeed | `make all` | `make test` |
| does the build graph still tell the truth | `make selftest` | `make verify-report` |
| do I need the proof saved as a review bundle | `make verify-report` | `make proof` |
| what is the shortest human-first route into the capstone | `make walkthrough` | `make tour` |
| which failure class does the repro pack teach | `make incident-audit` | `make repro` |
| what does this repository assume about tools or variable sources | `make profile-audit` | `make portability-audit` and `make show-origins` |
| can this tree be published as source without local residue | `make source-baseline-check` | `make source-bundle` |
| what is the strongest shared stewardship route | `make confirm` | none; this is the top route |

---

## Stable review targets

| Target | What it produces | Use when |
| --- | --- | --- |
| `help` | the published target list and key variables | you need the supported surface |
| `all` | the ordinary build outputs and convergence sentinel | you need the baseline build result |
| `test` | runtime behavior checks | you need product-facing validation |
| `selftest` | convergence, schedule equivalence, and hidden-input checks | you need build-system proof |
| `walkthrough` | the bounded first-pass bundle | you need an ordered entry route |
| `tour` | the shortest printed walkthrough plus supporting bundle | you need quick orientation |
| `contract-audit` | the public-contract review bundle | you are reviewing promises and boundaries |
| `inspect` | the same contract route under review naming | you want the smallest honest review route |
| `incident-audit` | one executed incident bundle | you want one failure class with evidence |
| `profile-audit` | the execution-profile review bundle | you are reviewing portability and precedence |
| `selftest-report` | the saved selftest evidence bundle | you need durable proof output |
| `verify-report` | the same selftest bundle under shared catalog naming | you need the catalog label used elsewhere |
| `proof` | the sanctioned multi-bundle review set | one question now spans multiple routes |
| `hardened` | selftest, audits, attestation, and runtime checks | you want the strongest built-in validation body |
| `confirm` | the same strongest route under shared naming | you are closing stewardship review |

---

## Distinctions that matter

- `all` builds outputs once; `selftest` proves the build contract
- `walkthrough` writes a first-pass bundle; `tour` prints the shortest route and focused follow-ups
- `contract-audit` and `inspect` are the same route with different naming context
- `selftest-report` and `verify-report` are the same saved evidence bundle
- `profile-audit` is about declared execution boundary and variable sources, not raw performance benchmarking
- `proof` is not "better selftest"; it is the point where one review question has become several
- `hardened` and `confirm` are the strongest built-in routes, not the default starting point

---

## Source packaging route

Use this route when the question is not "does the build pass?" but "would the tracked
source tree be safe to hand to another reviewer?"

Run these commands from the capstone directory:

```bash
gmake clean
gmake source-baseline-check
gmake source-bundle
```

They do different jobs:

- `gmake clean` removes generated build state
- `gmake source-baseline-check` proves the tree no longer carries local build residue
- `gmake source-bundle` writes a tracked-source archive from `git ls-files`

What must stay out of the source bundle:

- `build/` and `stamps/` because they are derived state, not source inputs
- `app`, `all`, and `dist.tar.gz` because they are generated deliverables
- temporary files such as `*.tmp`, `*.tmp.*`, and `*.d.tmp` because they are local residue

What belongs in the source bundle:

- `Makefile` and `mk/` because they define the build contract
- `README.md`, [TARGET_GUIDE.md](target-guide.md), and [PROOF_GUIDE.md](proof-guide.md) because they explain the repository surface
- `src/`, `include/`, `tests/`, `repro/`, and helper scripts because they are tracked project inputs

---

## Useful companions

- [PROOF_GUIDE.md](proof-guide.md)
- [WALKTHROUGH_GUIDE.md](walkthrough-guide.md)
- [SELFTEST_GUIDE.md](selftest-guide.md)
- [CONTRACT_AUDIT_GUIDE.md](contract-audit-guide.md)
- [INCIDENT_REVIEW_GUIDE.md](incident-review-guide.md)
- [PROFILE_AUDIT_GUIDE.md](profile-audit-guide.md)
