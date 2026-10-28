# Contract decisions

## Resource shape over command endpoints

Projects, datasets, analysis runs, artifacts, and webhook subscriptions are addressable resources. Cancellation is modeled as a subordinate command resource because it represents an attempted state transition rather than replacement of the whole run.

## `202 Accepted` for analysis submission

Run creation accepts work but does not claim completion. The response includes the run representation, `Location` pointing to the status monitor, `Retry-After`, and `Idempotent-Replay`. Polling is deterministic in the training provider: the first retrieval reaches `running`, the next reaches `completed`.

## Idempotency key binding

The key is scoped to the authenticated principal and bound to a canonical hash of the request body. Reusing the same key and body returns the same logical run. Reusing the key with changed input returns `409`; creating another run would defeat the guarantee.

## Conditional project updates

`PATCH /projects/{projectId}` requires `If-Match`. Missing preconditions return `428`; stale entity tags return `412`. This makes lost-update behavior explicit rather than relying on last-write-wins.

## Error vocabulary

Operational failures use `application/problem+json`. Validation failures extend the common shape with a bounded `errors` collection containing location, message, and stable code. A framework's native exception JSON never crosses the public boundary.

## Missing and concealed resources

A principal asking for another owner's object receives `404`. This avoids teaching that a valid scope is complete authorization and avoids disclosing object existence.

## Upload limits

The training limit is one MiB. The contract distinguishes empty input (`422`), unsupported part media type (`415`), excessive content (`413`), absent resources (`404`), and invalid lifecycle use (`409`).

## Sequential progress representations

The 3.1 baseline describes `text/event-stream` and `application/x-ndjson` as media types with examples. The 3.2 frontier adds `itemSchema` to describe the schema of each streamed item. Neither provider pretends the complete stream is one JSON array.

## Current-standard frontier

OpenAPI 3.2 features are isolated in `openapi-3.2.yaml`. The course does not downgrade the standard to the toolchain, nor does it claim unsupported tools are compliant. Capability evidence records supported, transformed, partially supported, or unsupported outcomes.
