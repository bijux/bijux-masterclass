# Lab 08 — Trace one SDK from contract to consumer

## Setup

Run `make sdk-proof`. Inspect the Python and TypeScript packages, publication
record, SBOM, provenance, and Analysis HTTP contract digest.

## Controlled action

Verify the normal publication. Then change one SDK byte, remove the contract
digest, remove provenance, and alter the builder identifier. Classify which
checks are local integrity checks and which require an externally trusted build
platform.

## Oracle

Digest changes, missing evidence, and altered provenance subjects reject local
publication. An untrusted builder identity remains environment-backed rather than
being falsely accepted by file shape alone.

## Required evidence

Create `reports/module-08-sdk-publication.json` with subject digests, API release,
SBOM profile, provenance predicate, executed checks, and unexecuted trust checks.

## Cleanup

Restore artifacts and rerun SDK proof.

## Completion gate

A consumer can identify exactly which contract and build evidence produced each
package, and the report does not claim more trust than was verified.
