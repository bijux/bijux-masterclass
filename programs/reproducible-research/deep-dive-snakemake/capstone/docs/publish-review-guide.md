# Publish Review Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  guide["Capstone docs"]
  section["Docs"]
  page["Publish Review Guide"]
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

This guide explains how to review the publish boundary as a contract, not only as a
directory that happens to contain files.

Use [File API](file-api.md) first when the real question is which surfaces are already
part of the public contract. Use [Architecture Guide](architecture.md) when the question
is whether an internal surface deserves promotion into that contract at all.

---

## Primary Review Route

1. Read `FILE_API.md`.
2. Run `make publish-summary` when you need the shortest honest publish overview.
3. Run `make verify-report` when you need the fuller contract review bundle.
4. Read this guide, `publish-summary.json`, `verify.json`, `route.txt`, and `review-questions.txt` in the bundle.
5. Compare the report with `manifest.json`, `discovered_samples.json`, `summary.json`, `summary.tsv`, and `provenance.json`.
6. Read `report/index.html` when you need the compact human-facing publish surface.

---

## What The Review Should Settle

- which files are safe for downstream trust
- which checks are proving existence, parseability, and contract shape
- which files remain internal execution state even if they are useful during review
- which published summary surfaces are optimized for machine comparison versus human review

---

## Failure Questions

- Which publish artifact would be hardest to change safely without a version bump?
- Which publish check would you strengthen first if downstream trust became more demanding?
- Which internal result would you refuse to promote without a clearer contract?

