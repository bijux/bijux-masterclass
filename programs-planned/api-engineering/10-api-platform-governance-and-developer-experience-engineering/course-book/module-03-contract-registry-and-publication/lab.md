# Lab — Publish four immutable protocol releases

> **Module 03:** Contract Registry and Multi-Protocol Publication

## Objective

Register the four inherited interface releases by digest and publication evidence.

## Why this lab matters

This lab turns the module’s governing question—**What makes an API contract a trustworthy published release across HTTP, events, RPC, and GraphQL?**—into a falsifiable experiment. publish(apiRef: string, version: string, digest: string): string { const key = ${apiRef}@${version}; const previous = this.releases.get(key); if (previous !== undefined && previous !== digest) { throw new Error("immutable-release"); } if (previous === digest) return "idempotent"; this.releases.set(key, digest); return "published"; } } ```

It advances the cumulative Analysis Runs Platform by requiring this result: **Register the four inherited interface releases by digest and publication evidence**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make registry-proof` and inspect `capstone/registry/releases.json`.

## Hypothesis

The clean implementation should satisfy this claim: **Identical replay is idempotent. Changed bytes under an existing version fail. A new version without evidence fails. Promotion references the existing digest.** When the lab introduces this fault—**Then attempt: identical replay, changed bytes under the same version, a new version without compatibility evidence, and an experimental promotion that rebuilds rather than reuses bytes**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

For each protocol, verify the registered digest. Then attempt: identical replay,
changed bytes under the same version, a new version without compatibility
evidence, and an experimental promotion that rebuilds rather than reuses bytes.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Then attempt: identical replay, changed bytes under the same version, a new version without compatibility evidence, and an experimental promotion that rebuilds rather than reuses bytes**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Register the four inherited interface releases by digest and publication evidence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Identical replay is idempotent. Changed bytes under an existing version fail. A
new version without evidence fails. Promotion references the existing digest.

## Required evidence

Write `reports/module-03-registry-publication.json` with protocol, version,
digest, evidence profile, replay result, and rejected mutation.

## Interpretation and defense

1. Which state or effect is authoritative for **Contract Registry and Multi-Protocol Publication**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Then attempt: identical replay, changed bytes under the same version, a new version without compatibility evidence, and an experimental promotion that rebuilds rather than reuses bytes** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Delete scratch releases and restore registry state.

## Completion gate

Every active contract resolves to exact bytes, owner, lifecycle, and
protocol-appropriate compatibility evidence.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Contract Registry and Multi-Protocol Publication**. A green command without the negative case and causal explanation does not satisfy this gate.
