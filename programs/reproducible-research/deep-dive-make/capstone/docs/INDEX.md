# Capstone Index

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  question["Current review question"] --> index["INDEX.md"]
  index --> target["TARGET_GUIDE.md"]
  index --> proof["PROOF_GUIDE.md"]
  index --> repro["REPRO_GUIDE.md"]
  index --> walk["WALKTHROUGH_GUIDE.md"]
```

```mermaid
flowchart LR
  start["Name the current claim"] --> choose["Choose the smallest guide"]
  choose --> inspect["Inspect the matching target, file, or bundle"]
  inspect --> escalate["Escalate only if the claim changes"]
```
<!-- page-maps:end -->

Use this page as the stable entry route for the Make capstone docs.

## Start here by question

| If the question is... | Start here | Escalate only if needed |
| --- | --- | --- |
| what this repository promises | `WALKTHROUGH_GUIDE.md` | `TARGET_GUIDE.md` and `make walkthrough` |
| which public targets are stable | `TARGET_GUIDE.md` | `CONTRACT_AUDIT_GUIDE.md` and `make inspect` |
| how the build proves convergence and parallel safety | `SELFTEST_GUIDE.md` | `PROOF_GUIDE.md` and `make selftest` |
| which failure class the capstone teaches | `REPRO_GUIDE.md` | `INCIDENT_REVIEW_GUIDE.md` and `make incident-audit` |
| how the system is layered | `ARCHITECTURE.md` | `PROFILE_AUDIT_GUIDE.md` and `make proof` |

## Stable local doc surface

- `ARCHITECTURE.md`
- `CONTRACT_AUDIT_GUIDE.md`
- `INCIDENT_REVIEW_GUIDE.md`
- `INDEX.md`
- `PROFILE_AUDIT_GUIDE.md`
- `PROOF_GUIDE.md`
- `REPRO_GUIDE.md`
- `SELFTEST_GUIDE.md`
- `TARGET_GUIDE.md`
- `WALKTHROUGH_GUIDE.md`
