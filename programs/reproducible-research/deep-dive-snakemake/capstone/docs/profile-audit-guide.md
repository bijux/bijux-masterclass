# Profile Audit Guide

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  guide["Capstone docs"]
  section["Docs"]
  page["Profile Audit Guide"]
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

Use this guide when the question is about execution policy: executor choice, resources,
or operating context. The point is not whether the profiles differ. The point is whether
they differ only in policy, not in workflow meaning.

Use `profile-summary` after `profile-audit` when you want the compact comparison JSON.

## What the Slurm profile represents

`profiles/slurm/config.yaml` is the portable scheduler-policy surface used by this
course. It deliberately defines only context-owned behavior that can be reviewed without
access to a particular cluster.

An operator supplies site-owned values such as executor plugin, account, partition,
quality of service, and storage roots through a documented overlay or invocation. Those
values may map declared resources and operating context; they may not replace sample
membership, analytical parameters, final output identities, or publish paths.

This division keeps the capstone executable on ordinary machines while still teaching a
real scheduler boundary. It is not a claim that one profile can submit unchanged to every
Slurm installation.

---

## Primary review route

1. Run `make profile-audit`.
2. Read `route.txt` and `review-questions.txt`.
3. Compare `profiles/local/config.yaml`, `profiles/ci/config.yaml`, and `profiles/slurm/config.yaml`.
4. Compare `local-dryrun.txt`, `ci-dryrun.txt`, and `slurm-dryrun.txt`.
5. Run `make profile-summary` only if you want the compact comparison surface.

---

## What the audit should prove

- executor and resource policy are visible as configuration
- the workflow plan stays semantically stable across operating contexts
- profile differences do not become hidden analytical changes

---

## Review questions

- Which differences are expected because of execution context?
- Which difference would worry you because it smells like semantic drift?
- Which profile should a maintainer inspect first before approving a move to new infrastructure?
