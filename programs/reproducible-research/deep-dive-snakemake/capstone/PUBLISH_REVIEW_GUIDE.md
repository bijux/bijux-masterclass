<a id="top"></a>

# Publish Review Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  guide["Capstone docs"]
  section["PUBLISH_REVIEW_GUIDE"]
  page["Publish Review Guide"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  contract["FILE_API.md"] --> report["make verify-report"]
  report --> verify["verify.json and route.txt"]
  verify --> publish["publish/v1/ artifacts"]
  publish --> review["Downstream trust decision"]
```
<!-- page-maps:end -->

This guide explains how to review the publish boundary as a contract, not only as a
directory that happens to contain files.

---

## Primary Review Route

1. Read `FILE_API.md`.
2. Run `make verify-report`.
3. Read `verify.json`, `route.txt`, and `bundle-manifest.json`.
4. Compare the report with `publish/v1/manifest.json`, `summary.json`, and `provenance.json`.

[Back to top](#top)

---

## What The Review Should Settle

- which files are safe for downstream trust
- which checks are proving existence, parseability, and contract shape
- which files remain internal execution state even if they are useful during review

[Back to top](#top)

---

## Failure Questions

- Which publish artifact would be hardest to change safely without a version bump?
- Which publish check would you strengthen first if downstream trust became more demanding?
- Which internal result would you refuse to promote without a clearer contract?

[Back to top](#top)
