# Lab 03 — Publish four immutable protocol releases

## Setup

Run `make registry-proof` and inspect `capstone/registry/releases.json`.

## Controlled action

For each protocol, verify the registered digest. Then attempt: identical replay,
changed bytes under the same version, a new version without compatibility
evidence, and an experimental promotion that rebuilds rather than reuses bytes.

## Oracle

Identical replay is idempotent. Changed bytes under an existing version fail. A
new version without evidence fails. Promotion references the existing digest.

## Required evidence

Write `reports/module-03-registry-publication.json` with protocol, version,
digest, evidence profile, replay result, and rejected mutation.

## Cleanup

Delete scratch releases and restore registry state.

## Completion gate

Every active contract resolves to exact bytes, owner, lifecycle, and
protocol-appropriate compatibility evidence.
