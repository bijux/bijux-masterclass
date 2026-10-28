# Evidence tour

Run from `capstone/`:

```bash
make tour
```

The tour first validates source structure, both OpenAPI versions, external references, deterministic bundling, examples, 60+ schema fixtures, handler coverage, overlays, the Arazzo workflow, release compatibility, and Markdown links. It then executes a concrete workflow against the Python provider in-process.

Expected progression:

```text
PASS anonymous health                   200
PASS create project                     201
PASS register dataset                   201
PASS upload multipart content           201
PASS accept asynchronous run            202
PASS observe running state              200
PASS observe completed state            200
PASS retrieve artifacts                 200
```

The printed JSON contains the actual project, dataset, run, and artifact identifiers created during the tour. The route is deterministic but not a prerecorded transcript.

For cross-language evidence, run:

```bash
make live-conformance
```

That command starts each provider from clean state and applies the same scope, precondition, upload, idempotency, ownership, streaming, webhook, and diagnostics checks.
