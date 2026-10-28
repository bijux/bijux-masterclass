# Tool-boundary and capability evidence

The deterministic Python gates prove source structure, reference resolution, examples, fixtures, overlays, workflow references, release fixtures, and provider-handler coverage without depending on one vendor implementation.

The external toolchain then exercises Redocly, Spectral, Prism, Schemathesis, `openapi-typescript`, `openapi-python-client`, and `oasdiff`. Each tool proves a bounded stage; no green command is promoted to “full OpenAPI support.”

## Two reports

`make capability-report` writes an **installation inventory**. It distinguishes an installed executable from `not-executed` and deliberately makes no feature-support claim.

Module 10 uses [`capability-cases.yaml`](capability-cases.yaml) to produce the feature/stage matrix. Each row records the exact tool version, command, artifact digest, observable assertion, and one of:

```text
supported
partial
transformed
unsupported
not-executed
```

A missing executable is `not-executed`. A parser that accepts OpenAPI 3.2 but drops `itemSchema` during generation is `partial` or `transformed`, not supported. A tool crash is preserved as evidence and classified separately from a provider defect.

## Full proof

`make proof` invokes every installed required route. It stops at the first failed gate and writes `reports/proof.json`. The learner’s final capability matrix may include not-executed rows, but final course completion requires the mandatory baseline routes defined in the assessment rubric.
