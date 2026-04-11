# Audit Evidence: Params, Metrics, Locks, and Manifests

A promoted bundle needs evidence that can answer future questions.

The future reviewer may ask:

- what controls produced this result?
- what metrics justified promotion?
- what pipeline state produced the artifacts?
- which files belong to the release?
- how does this bundle relate to the repository history?

No single file answers all of those questions.

## Four evidence surfaces work together

| Surface | What it explains |
| --- | --- |
| promoted params | control values that define the release |
| promoted metrics | review evidence used to justify the release |
| lock evidence | recorded pipeline state behind the artifacts |
| manifest | files included in the promoted bundle |

If one surface is missing, promotion may still be possible, but the audit story weakens.

## Params and metrics must agree

If `publish/v1/params.yaml` says:

```yaml
evaluate:
  threshold: 0.50
```

then `publish/v1/metrics.json` should describe the metrics produced under that promoted
control, not an older threshold.

Mismatch example:

```text
params: threshold 0.50
metrics: copied from threshold 0.65 run
```

That bundle is dangerous because it looks complete while telling the wrong story.

## Lock evidence anchors the bundle

The release surface should not float away from the DVC state that produced it.

The reviewer should be able to connect promoted artifacts back to:

- `dvc.yaml` stage declarations
- `dvc.lock` recorded dependencies and outputs
- parameter values
- metric outputs

This does not mean every consumer needs to read `dvc.lock`. It means the project can defend
the promoted state if challenged.

## Manifests remove ambiguity

A manifest says which files are part of the release.

Without it, reviewers may ask:

- is this debug plot included?
- is this old metric file still relevant?
- which model file should the consumer load?
- is the report generated from the promoted parameters?

The manifest should make those questions boring.

## Review checkpoint

You understand this core when you can:

- explain why params, metrics, locks, and manifests answer different audit questions
- detect a params-metrics mismatch
- connect a promoted artifact back to recorded DVC state
- write a manifest that removes ambiguity
- reject a bundle that is complete-looking but evidentially inconsistent

Auditability means the promoted state can still explain itself later.
