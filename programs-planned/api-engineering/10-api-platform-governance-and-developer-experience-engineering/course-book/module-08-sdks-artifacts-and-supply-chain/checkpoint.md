# Checkpoint — Module 08: SDKs, CLIs, Artifacts, SBOMs, and Provenance

## Required result

Publish Python and TypeScript client artifacts with contract identity, SBOM, and bounded provenance evidence.

## Demonstrate

- [ ] Design sdks as supported products rather than raw generated code.
- [ ] Link packages to exact contract releases.
- [ ] Distinguish sbom, provenance, checksum, and signature evidence.
- [ ] Govern package versioning and retention.
- [ ] Reject untraceable or misleading publication claims.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-08-sdk-publication.json` with subject digests, API release,
SBOM profile, provenance predicate, executed checks, and unexecuted trust checks.

## Defend the design

1. Answer the central question in one paragraph: How can developer artifacts remain convenient, idiomatic, reproducible, and traceable to the contracts that produced them?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **SDKs, CLIs, Artifacts, SBOMs, and Provenance** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
