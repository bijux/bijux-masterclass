<a id="top"></a>

# Profile Audit Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  guide["Capstone docs"]
  section["PROFILE_AUDIT_GUIDE"]
  page["Profile Audit Guide"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  profiles["profiles/local, ci, slurm"] --> audit["make profile-audit"]
  audit --> bundle["profile audit bundle"]
  bundle --> compare["Compare dry-runs and profile files"]
  compare --> decision["Separate policy from workflow meaning"]
```
<!-- page-maps:end -->

This guide explains how to review execution policy honestly. The key question is not
whether the profiles differ. The key question is whether they differ only in policy, not
in workflow meaning.

---

## Primary Review Route

1. Run `make profile-audit`.
2. Read `route.txt` and `review-questions.txt`.
3. Compare `profiles/local.yaml`, `profiles/ci.yaml`, and `profiles/slurm.yaml`.
4. Compare `local-dryrun.txt`, `ci-dryrun.txt`, and `slurm-dryrun.txt`.

[Back to top](#top)

---

## What The Audit Should Prove

- executor and resource policy are visible as configuration
- the workflow plan remains semantically stable across operating contexts
- profile differences do not become hidden analytical changes

[Back to top](#top)

---

## Review Questions

- Which profile differences are expected because of execution context?
- Which profile difference would worry you because it smells like semantic drift?
- Which profile should a maintainer inspect first before approving a migration to new infrastructure?

[Back to top](#top)
