# Checkpoint — Module 07: Streaming and Artifact Integrity

## Required result

Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.

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

## Defend the design

1. Answer the central question: **How do large request and response bodies move through the service without unbounded memory or corrupt publication?**
2. Demonstrate this capstone result: Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: staging is bounded, publication is atomic and no-clobber, and the digest names exactly the published bytes.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.—all focused checks pass, the **Streaming and Artifact Integrity** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
