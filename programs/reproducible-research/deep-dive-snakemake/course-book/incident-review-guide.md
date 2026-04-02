<a id="top"></a>

# Incident Review Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  module["Module 09"] --> guide["Incident Review Guide"]
  guide --> local["capstone/INCIDENT_REVIEW_GUIDE.md"]
  local --> evidence["selftest, confirm, and tour evidence"]
```

```mermaid
flowchart LR
  symptom["Workflow concern"] --> classify["Classify the concern"]
  classify --> determinism["Determinism question"]
  classify --> contract["Contract question"]
  classify --> evidence["Executed evidence question"]
  determinism --> route["Choose the narrowest command"]
  contract --> route
  evidence --> route
```
<!-- page-maps:end -->

Use this page when the question is about incident response, reproducibility under
pressure, or workflow debugging with evidence instead of intuition.

---

## Recommended Route

1. Read `capstone/INCIDENT_REVIEW_GUIDE.md`.
2. Use [Proof Matrix](proof-matrix.md) to choose the narrowest command for the current symptom.
3. Compare the result with [Profile Audit Guide](profile-audit-guide.md) and [Publish Review Guide](publish-review-guide.md) if the problem spans multiple boundaries.

[Back to top](#top)

---

## What A Good Incident Review Can Answer

- whether the failure is about workflow semantics, execution policy, or downstream trust
- which command gives the most honest first evidence
- which files should remain unchanged until stronger proof exists

[Back to top](#top)
