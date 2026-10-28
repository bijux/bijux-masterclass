# Ten-Day Study Plan

This is a dense two-week course with one numbered module per weekday. The orientation is completed before Day 1.

| Time | Work |
|---|---|
| 08:30–09:00 | Retrieve the previous module without notes |
| 09:00–11:00 | Read and annotate the main chapter |
| 11:15–12:30 | Reconstruct the worked design in your own words |
| 13:30–15:00 | Complete exercises before opening answers |
| 15:15–18:00 | Run the controlled laboratory |
| 19:00–20:00 | Inspect the AWS/OpenTofu reference implementation |
| 20:00–21:00 | Produce checkpoint evidence and a concise decision record |

## Middle weekend

Use Saturday only to repair failed checkpoints or repeat a state-recovery exercise. Sunday introduces no new material.

## Primary-track rule

The dependency-light model is mandatory. OpenTofu execution is strongly recommended. AWS execution is optional but is the only evidence class that can prove provider and data-plane behavior.

## Evidence journal

For every lab retain:

```text
question
environment and identity
configuration digest
state lineage/serial when relevant
plan digest
controlled action
observed result
failure or success oracle
cleanup result
remaining uncertainty
```

A screenshot is supplementary evidence. It is not a substitute for machine-readable state, plan, API, or data-plane output.
