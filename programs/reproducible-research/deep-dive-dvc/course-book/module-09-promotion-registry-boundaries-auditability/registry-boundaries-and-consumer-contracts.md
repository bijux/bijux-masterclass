# Registry Boundaries and Consumer Contracts

A registry boundary is where internal artifacts become named products.

It may be a model registry, a published directory, an object-store prefix, or a release
record. The form can vary. The contract is stable:

> Consumers use this named release surface, not arbitrary internal pipeline paths.

## Registry boundaries protect consumers

Internal project structure changes often:

- stages are renamed
- feature paths move
- report generation changes
- intermediate outputs split or merge
- experiment candidates appear and disappear

Downstream consumers should not break every time internal structure improves.

A registry boundary gives them a smaller contract:

```text
registry/
  incident-escalation/
    v1/
      model.json
      metrics.json
      params.yaml
      manifest.json
```

Consumers depend on `incident-escalation/v1`, not the internal training directory.

## The registry should say what is supported

A registry entry should answer:

- what artifact or bundle is approved?
- which version is being consumed?
- which metadata travels with it?
- what compatibility or usage expectation exists?
- where is the audit trail?

If the registry only stores a model file, consumers may miss the parameters and metrics
that explain it.

## Do not leak exploratory state into the registry

Exploratory results can be useful without being registry-ready.

Keep out:

- candidate outputs without review
- debug plots
- old metric files
- internal cache files
- local notebook exports
- unreviewed model variants

The registry boundary should say "this is supported," not "this was nearby."

## Consumer contract examples

Weak:

> Use whatever model is in `outputs/latest/`.

Stronger:

> Use `publish/v1/model.json` with the matching `publish/v1/params.yaml` and
> `publish/v1/metrics.json`; do not depend on files outside `publish/v1/`.

Stronger still:

> Use registry entry `incident-escalation/v1`; it contains a manifest, promoted model,
> release metrics, promoted parameters, and review link. Internal pipeline paths are not a
> supported interface.

The last version gives consumers a clear contract and maintainers room to change internals.

## Review checkpoint

You understand this core when you can:

- define the registry boundary for one promoted result
- explain what consumers are allowed to depend on
- keep exploratory or debug state out of the registry
- include metadata and audit evidence beside the artifact
- protect consumers from internal pipeline churn

A registry is not a storage drawer. It is a consumer-facing promise.
