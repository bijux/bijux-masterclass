# Deep Dive Make Capstone Docs

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  guide["Capstone docs"]
  section["Docs"]
  page["Deep Dive Make Capstone Docs"]
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

Use this page as the stable entry route for the Make capstone docs.

## Start here by question

| If the question is... | Start here | Escalate only if needed |
| --- | --- | --- |
| what this repository promises | `WALKTHROUGH_GUIDE.md` | `TARGET_GUIDE.md` and `make walkthrough` |
| which public targets are stable | `TARGET_GUIDE.md` | `CONTRACT_AUDIT_GUIDE.md` and `make inspect` |
| how the build proves convergence and parallel safety | `SELFTEST_GUIDE.md` | `PROOF_GUIDE.md` and `make selftest` |
| how one release candidate is accepted locally | `RELEASE_GUIDE.md` | `TARGET_GUIDE.md` and `make release-check` |
| how to establish or compare local build-cost evidence | `PERFORMANCE_EVIDENCE_GUIDE.md` | `make perf` and `make performance-compare` |
| how the capstone proves distinct concurrency failure mechanisms | `INCIDENT_REVIEW_GUIDE.md` | `make incident-audit`, then `REPRO_GUIDE.md` |
| why missing edges can produce successful stale builds | `INCREMENTAL_FAULT_AUDIT_GUIDE.md` | `make incremental-fault-audit` |
| how the system is layered | `ARCHITECTURE.md` | `PROFILE_AUDIT_GUIDE.md` and `make proof` |

## Stable local doc surface

- [Architecture Guide](architecture.md)
- [Contract Audit Guide](contract-audit-guide.md)
- [Incident Review Guide](incident-review-guide.md)
- [Incremental Fault Audit Guide](incremental-fault-audit-guide.md)
- [Performance Evidence Guide](performance-evidence-guide.md)
- [Profile Audit Guide](profile-audit-guide.md)
- [Proof Guide](proof-guide.md)
- [Release Acceptance Guide](release-guide.md)
- [Repro Guide](repro-guide.md)
- [Selftest Guide](selftest-guide.md)
- [Target Guide](target-guide.md)
- [Walkthrough Guide](walkthrough-guide.md)
