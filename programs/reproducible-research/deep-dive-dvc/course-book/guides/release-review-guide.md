# Release Review Guide

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  module["Module 09"]
  guide["Release Review Guide"]
  capstone["Release route"]
  publish["publish/v1/"]

  module --> guide --> capstone --> publish
```

```mermaid
flowchart TD
  question["What is safe for downstream trust?"] --> contract["Inspect the promoted contract"]
  contract --> evidence["Inspect release evidence in order"]
  evidence --> limits["Record the trust limits"]
  limits --> decision["Make the release decision"]
```
<!-- page-maps:end -->

Use this guide when studying promotion and auditability.

## Review questions

- Which promoted files are part of the downstream contract, and which are intentionally excluded?
- Which trust claims come from the publish bundle alone, and which still require repository-internal evidence?
- Which params and metrics remain meaningful enough for later review?

## Best companion pages

- [Release Audit Checklist](release-audit-checklist.md)
- [Evidence Boundary Guide](../reference/evidence-boundary-guide.md)
- [Capstone Review Worksheet](capstone-review-worksheet.md)
