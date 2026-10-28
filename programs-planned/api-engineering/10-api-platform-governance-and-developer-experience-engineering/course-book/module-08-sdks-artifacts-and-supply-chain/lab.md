# Lab — Trace one SDK from contract to consumer

> **Module 08:** SDKs, CLIs, Artifacts, SBOMs, and Provenance

## Objective

Publish Python and TypeScript client artifacts with contract identity, SBOM, and bounded provenance evidence.

## Why this lab matters

This lab turns the module’s governing question—**How can developer artifacts remain convenient, idiomatic, reproducible, and traceable to the contracts that produced them?**—into a falsifiable experiment. Python and npm differ in naming, dependency resolution, lockfiles, build artifacts, typing, and distribution. Publish ecosystem-native metadata. Avoid forcing one organization-wide package layout when the underlying tools disagree. Standardize the evidence and support contract instead.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish Python and TypeScript client artifacts with contract identity, SBOM, and bounded provenance evidence**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make sdk-proof`. Inspect the Python and TypeScript packages, publication
record, SBOM, provenance, and Analysis HTTP contract digest.

## Hypothesis

The clean implementation should satisfy this claim: **Digest changes, missing evidence, and altered provenance subjects reject local publication. An untrusted builder identity remains environment-backed rather than being falsely accepted by file shape alone.** When the lab introduces this fault—**Then change one SDK byte, remove the contract digest, remove provenance, and alter the builder identifier**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Verify the normal publication. Then change one SDK byte, remove the contract
digest, remove provenance, and alter the builder identifier. Classify which
checks are local integrity checks and which require an externally trusted build
platform.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Then change one SDK byte, remove the contract digest, remove provenance, and alter the builder identifier**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish Python and TypeScript client artifacts with contract identity, SBOM, and bounded provenance evidence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Digest changes, missing evidence, and altered provenance subjects reject local
publication. An untrusted builder identity remains environment-backed rather than
being falsely accepted by file shape alone.

## Required evidence

Create `reports/module-08-sdk-publication.json` with subject digests, API release,
SBOM profile, provenance predicate, executed checks, and unexecuted trust checks.

## Interpretation and defense

1. Which state or effect is authoritative for **SDKs, CLIs, Artifacts, SBOMs, and Provenance**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Then change one SDK byte, remove the contract digest, remove provenance, and alter the builder identifier** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Restore artifacts and rerun SDK proof.

## Completion gate

A consumer can identify exactly which contract and build evidence produced each
package, and the report does not claim more trust than was verified.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **SDKs, CLIs, Artifacts, SBOMs, and Provenance**. A green command without the negative case and causal explanation does not satisfy this gate.
