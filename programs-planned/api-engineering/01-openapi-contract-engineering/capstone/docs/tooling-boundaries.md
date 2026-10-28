# Tooling boundaries

## Why more than one tool

Redocly, Spectral, Prism, Schemathesis, language generators, and `oasdiff` answer different questions. Treating one green command as universal correctness is a category error.

## Generator view

`spec/dist/openapi.client.yaml` is an explicit derived artifact. It removes callbacks, root-level webhooks, streaming endpoints, and internal diagnostics because selected generators do not uniformly model those constructs. The canonical contract remains unchanged, and the omissions are visible in the generation script.

This is preferable to silently editing generated code or pretending a partial SDK covers every operation.

## OpenAPI 3.2 capability report

The frontier is run against installed tools separately. A parser accepting the version string does not prove support for `QUERY`, `querystring`, enhanced tags, or sequential `itemSchema`. The report must classify feature behavior rather than merely record process exit zero.
