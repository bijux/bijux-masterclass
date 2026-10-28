# Checkpoint — Module 07: Streaming and Artifact Integrity

## Required result

Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download.

## Demonstrate

- Enforce limits while streaming rather than after buffering.
- Stage bytes safely and clean up failures.
- Use content addressing and no-clobber publication.
- Persist event streams for SSE and NDJSON consumers.
- Keep artifact authorization and storage paths separate.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=07 TRACK=python
make module-proof MODULE=07 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Streaming and Artifact Integrity** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Streaming and Artifact Integrity**
- focused result for: Enforce limits while streaming rather than after buffering.
- public, durable, security, or operational observation showing: Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **bounded content-addressed artifact publication**
- a limitation statement naming every live dependency required to support the strongest **Streaming and Artifact Integrity** claim but not exercised

## Defend the design

1. Answer the central question: **How do large request and response bodies move through the service without unbounded memory or corrupt publication?**
2. Demonstrate this capstone result: Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.
3. Show the **Streaming and Artifact Integrity** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: staging is bounded, publication is atomic and no-clobber, and the digest names exactly the published bytes.
5. State which environment-backed **Streaming and Artifact Integrity** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.—all focused checks pass, the **Streaming and Artifact Integrity** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
