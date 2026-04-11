# Extension Guide

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  guide["Capstone docs"]
  section["Docs"]
  page["Extension Guide"]
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

Use this guide when a change seems reasonable in more than one place. The main job is to
keep ownership obvious a year later: workflow meaning in workflow files, policy in
profiles or config, reusable code in code, and public trust changes in the publish
contract.

---

## If the change affects workflow meaning

Prefer:

- `Snakefile`
- `workflow/rules/`
- `workflow/modules/`

Also update:

- [Walkthrough Guide](walkthrough-guide.md) or [Architecture Guide](architecture.md) if a
  new reader should notice it
- `make walkthrough` or `make tour` evidence if the visible route changed

---

## If the change affects execution policy

Prefer:

- `profiles/`
- validated config under `config/`

Also update:

- [Profile Audit Guide](profile-audit-guide.md)
- `make profile-audit` expectations

If the change would alter analytical meaning, it does not belong here.

---

## If the change affects the public publish contract

Prefer:

- `FILE_API.md`
- publish rules
- verification surfaces such as `verify-report`

Also update:

- [Publish Review Guide](publish-review-guide.md)
- compatibility expectations and versioning decisions

Treat this as a trust-boundary change, not a convenience edit.

---

## If the change affects helper implementation

Prefer:

- `workflow/scripts/` for orchestration-adjacent helpers
- `src/capstone/` for reusable implementation code with clearer software boundaries

Also update:

- the tests or verification surfaces that would catch drift in that helper

Do not let helper code become the only place where workflow meaning can be found.

---

## Final ownership test

Before merging a change, ask:

1. would another maintainer know where this belongs without reading the diff twice
2. which guide or audit bundle should mention it
3. which route would fail first if this change drifted later

