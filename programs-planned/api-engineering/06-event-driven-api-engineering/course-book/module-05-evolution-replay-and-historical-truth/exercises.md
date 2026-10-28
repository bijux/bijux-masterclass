# Exercises — Module 05 — Schema Evolution, Compatibility, Replay, and Historical Truth

Treat retained events as public historical data. Every answer must address old records and current consumers.

## 1. Classify an optional addition

Add optional `resultSummary` to a completion event. Identify structural status, semantic review, and historical behavior.

## 2. Reject a required addition

Explain why adding required `region` to v1 breaks retained records even if every new producer supplies it.

## 3. Review an enum expansion

A new `failureKind` value is added. State why the change may be review-required and how to test consumers.

## 4. Choose v2 or upcasting

Rename `durationMs` to `executionDurationMs` and change meaning. Decide whether an upcaster is honest.

## 5. Model unknown history

Old events lack `artifactCount`. Explain why defaulting to zero may be false and propose a target representation.

## 6. Design a correction

A completed event reported the wrong duration. Define a correction strategy without modifying the original record.

## 7. Bound a replay

Write the essential fields for rebuilding analytics v2 for one tenant and one date range.

## 8. Disable side effects

List mechanisms that prevent replay from sending notifications or webhooks.

## 9. Handle live catch-up

Explain how a new projection catches history and then current traffic without a gap or double apply.

## 10. Version inbox identity

Show how v1 and v2 analytics effects can process the same event without suppressing each other.

## 11. Reject nondeterminism

A projection uses current exchange rates from an external API. Explain the replay failure and redesign.

## 12. Evaluate a release

A candidate is structurally additive but lacks a catalogue entry and replay fixture. Determine the release decision.

## Submission format

Submit Module 05 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
