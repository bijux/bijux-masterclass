# Promotion Failures and Review Repairs

Promotion failures are dangerous because they often look orderly.

The folder exists. The model file exists. The report opens. The metric file has numbers.
But the bundle may still be wrong, incomplete, or impossible to defend.

Module 09 asks learners to review promotion by evidence, not by tidiness.

## Common failure patterns

| Failure | Why it matters | Repair |
| --- | --- | --- |
| metrics do not match promoted params | consumers trust the wrong result story | regenerate or replace the mismatched file |
| manifest omits the promoted model | consumers cannot tell what is supported | update manifest and review bundle shape |
| release includes debug files | consumer contract becomes noisy | remove unsupported files or mark them internal |
| registry points at `latest` | result can change without version clarity | publish a named version |
| lock evidence is unclear | audit trail cannot connect bundle to pipeline state | record or reference the relevant DVC state |

Use the table to identify the repair, not just the symptom.

## A neat bundle can still be deceptive

Example:

```text
publish/v1/
  model.json
  metrics.json
  params.yaml
```

This looks reasonable. But if `metrics.json` came from a different run than `params.yaml`,
the bundle is deceptive.

The review should ask:

- were these files produced by the same promoted state?
- do the metrics describe the promoted model?
- do the params describe the run that produced those metrics?
- does the lock evidence support the artifact?
- does the manifest list all supported files?

## Repair should preserve the audit trail

Do not repair a release by manually editing the number until it "looks right."

A better repair is:

- identify the mismatch
- return to the recorded state or rerun the declared pipeline
- regenerate the affected release files
- update the manifest if bundle shape changed
- rerun the release audit route
- write a review note explaining the repair

The goal is not only a clean directory. The goal is a defensible directory.

## Reject promotion when evidence is missing

Sometimes the right repair is to stop promotion.

Stop when:

- the candidate cannot be linked to a baseline or experiment review
- parameters and metrics cannot be matched
- the release artifact cannot be restored
- metric meaning changed without a review note
- registry consumers would depend on internal paths

Rejection is not failure. It protects downstream trust.

## Review checkpoint

You understand this core when you can:

- spot a neat-looking but inconsistent release bundle
- name the evidence mismatch precisely
- repair by regenerating or replacing evidence, not by cosmetic editing
- reject a promotion that cannot be audited
- write a review note that explains the repair

Promotion review exists because a tidy bundle is not the same thing as a trustworthy
bundle.
