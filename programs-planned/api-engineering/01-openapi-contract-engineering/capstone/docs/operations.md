# Operation inventory

The generated inventory is written to `spec/dist/operation-ledger.md` by `make operations`. The canonical path surface contains 19 operations, plus one request callback and one root-level webhook operation.

Functional groups:

- **System:** anonymous health and admin diagnostics.
- **Projects:** create, list, retrieve, conditionally update.
- **Datasets:** register, list, retrieve, upload, delete.
- **Analysis Runs:** create, list, retrieve, cancel, stream events.
- **Artifacts:** list per run and retrieve metadata.
- **Webhooks:** register a destination, describe completion delivery, and describe per-request callback delivery.

Operation IDs are stable consumer identifiers. The release fixture proves that renaming one without changing the path is still a breaking change for generated clients.
