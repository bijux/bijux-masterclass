# Release Surfaces and Bundle Shape

A release surface is the small set of files a downstream consumer is expected to use.

It should be more stable than the internal repository layout. If a consumer must browse
the whole project to guess which files matter, the release boundary is weak.

## A useful release surface is small

Example:

```text
publish/
  v1/
    manifest.json
    model.json
    metrics.json
    params.yaml
    review.md
```

This bundle is easier to trust than:

```text
outputs/
  latest/
  debug/
  old/
  model-final-final.json
  metrics-copy.json
```

The first layout names a versioned boundary. The second layout asks consumers to infer
authority.

## The manifest is the bundle map

A manifest tells consumers what is included and what each file is for.

Example:

```json
{
  "release": "v1",
  "artifacts": [
    {"path": "model.json", "role": "promoted model"},
    {"path": "metrics.json", "role": "release metrics"},
    {"path": "params.yaml", "role": "promoted parameter values"}
  ]
}
```

This does not need to be complicated. It needs to remove guessing.

## Keep internal paths out of the consumer contract

Internal paths can change as the pipeline evolves.

A consumer should not need to know:

- where intermediate features were generated
- which temporary report came from a candidate run
- how the training directory is organized
- which cache path held an object

The release surface should say what is supported. Everything else remains internal unless
explicitly promoted.

## Version names should mean something

Avoid vague release labels:

- `latest`
- `final`
- `new`
- `best`

Prefer labels that support review:

- `v1`
- `2026-04-incident-escalation`
- `recall-policy-release`

The exact naming convention can vary. The key is that the name should remain meaningful
after the immediate review conversation is gone.

## Review checkpoint

You understand this core when you can:

- define the files in a release surface
- explain why the surface should be smaller than the internal repository
- write a manifest that removes consumer guesswork
- keep unsupported internal paths out of the consumer contract
- choose release names that remain meaningful later

A release bundle is not a dumping ground. It is the shape of downstream trust.
