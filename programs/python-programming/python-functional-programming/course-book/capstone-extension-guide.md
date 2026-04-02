# Capstone Extension Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  review["Capstone review"] --> extension["Capstone Extension Guide"]
  extension --> local["capstone/EXTENSION_GUIDE.md"]
  local --> code["Owning package"]
```

```mermaid
flowchart LR
  request["New change request"] --> classify["Classify the change"]
  classify --> pure["Pure or modelling"]
  classify --> policy["Policy or pipeline"]
  classify --> effect["Boundary or adapter"]
  classify --> interop["Interop bridge"]
```
<!-- page-maps:end -->

Use this page when the course asks not only "what is this boundary?" but also "where
should the next change land?"

## Recommended route

1. Read `capstone/EXTENSION_GUIDE.md`.
2. Compare the change you are imagining with [Capstone File Guide](capstone-file-guide.md).
3. Use [Capstone Review Worksheet](capstone-review-worksheet.md) to decide what proof must change with the implementation.

## What a good answer looks like

- you can name the owning package before editing code
- you can explain why another nearby package should not absorb the change
- you can name the proof surface that must evolve with the implementation
