# Standards and version policy

The course separates standards, Atlas platform contracts, reference-tool behavior, and bounded course profiles.

## Executable standards baseline

| Concern | Course baseline |
|---|---|
| OCI Image Specification | 1.1.1 |
| OCI Runtime Specification | 1.3.0 |
| OCI Distribution Specification | 1.1.1 |
| OCI Image Layout marker | 1.0.0 |
| SLSA specification | 1.2 |
| SLSA provenance predicate | v1 |
| in-toto Statement | v1 |
| CycloneDX | 1.7 |
| SPDX comparison model | 3.0.1 |
| DSSE | typed-envelope profile used by the capstone |

The OCI projects define image structure, runtime bundle/lifecycle, and registry distribution separately. The course keeps those boundaries. “Docker image/container format” is not used as a substitute for the standards model.

## Atlas profiles

Atlas defines course-specific policies for deterministic JSON/archive production, build inputs, runtime hardening, SBOM completeness, vulnerability/VEX disposition, signer/builder authorization, promotion, retention, and Course 4 handoff. These are not OCI or SLSA requirements. They are versioned platform choices.

## Normative words

When reading specifications, distinguish `MUST`, `SHOULD`, and `MAY` requirements from examples and implementation conventions. Identify which document owns a field. For example, a registry stores media-typed bytes; runtime behavior is governed by a runtime configuration, not by registry semantics.

## Version discipline

`tool-versions.json` records observed build-environment versions and optional tools not executed. Provenance records actual tools/materials for the candidate. A current reference version never substitutes for evidence that the tool ran.

When a specification/profile version changes:

1. identify changed normative behavior and media/schema versions;
2. classify compatibility for existing objects/evidence;
3. update semantic and native-tool tests;
4. regenerate checked evidence;
5. retain the old verifier where rollback/historical subjects require it;
6. update Course 4 handoff only when externally relevant guarantees change.

Use [Reading OCI specifications](guides/reading-oci-specifications.md) for a method and the [reference atlas](reference/index.md) for object relationships.
