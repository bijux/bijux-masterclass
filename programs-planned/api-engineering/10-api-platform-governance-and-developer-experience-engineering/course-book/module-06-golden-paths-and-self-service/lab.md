# Lab — Generate, break, and repair a golden path

> **Module 06:** Golden Paths, Templates, and Self-Service Provisioning

## Objective

Publish and verify the `api-capability-v1` golden path and generated reference fixture.

## Why this lab matters

This lab turns the module’s governing question—**How can a platform reduce repeated setup work without hiding essential engineering decisions or creating clone-and-forget debt?**—into a falsifiable experiment. A golden path has an input contract, output contract, upgrade policy, support owner, and tests. Course 10’s api-capability-v1 requires a canonical API name, title, owner, protocol, and system. It emits exactly six files: ownership metadata, a contract location, quickstart, policy metadata, test, and README. Exact outputs make review and regression possible.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish and verify the `api-capability-v1` golden path and generated reference fixture**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make template-proof`. Inspect the template specification and skeleton.

## Hypothesis

The clean implementation should satisfy this claim: **Valid generation is deterministic and complete. Invalid inputs fail before publication. Secret and output-contract defects fail. Version impact is explained from generated-consumer compatibility, not intuition.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Generate `reporting-api` with valid parameters. Then attempt invalid API identity,
an unresolved placeholder, an extra undeclared output, and an embedded token.
Finally, alter a safe default and determine whether the template needs a patch,
minor, or major release.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish and verify the api-capability-v1 golden path and generated reference fixture**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Valid generation is deterministic and complete. Invalid inputs fail before
publication. Secret and output-contract defects fail. Version impact is explained
from generated-consumer compatibility, not intuition.

## Required evidence

Create `reports/module-06-golden-path.json` with template version, parameters,
file digests, rejected defects, and upgrade classification.

## Interpretation and defense

1. Which state or effect is authoritative for **Golden Paths, Templates, and Self-Service Provisioning**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Delete generated scratch projects and rerun template proof.

## Completion gate

The golden path is useful without being magical: it creates a safe proposed API,
not an automatically approved active product.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Golden Paths, Templates, and Self-Service Provisioning**. A green command without the negative case and causal explanation does not satisfy this gate.
