# Worked answers — SBOM, vulnerabilities, licenses, and VEX

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. Distinguish source, image, and runtime SBOM scopes.

A source SBOM describes declared/resolved source dependencies. An image SBOM describes shipped files/packages/components in an exact image subject. A runtime SBOM can include injected agents, mounted plugins, or dynamically loaded components. The scopes overlap but answer different questions and need explicit subjects.

## 2. Why can a schema-valid SBOM still be dangerously incomplete?

Schemas validate structure and data types, not whether the generator found every relevant component. A BOM with zero components can be schema-valid. Completeness needs independent expectations from lockfiles, rootfs inventories, binary linkage, build records, and required first-party component rules.

## 3. Compare purl, CPE, and file hash as component identifiers.

Purl represents package-manager ecosystem coordinates. CPE maps products into vulnerability-database naming but can be coarse and ambiguous. A hash identifies exact bytes but may not map directly to vulnerability metadata. Strong inventory often combines package identity and file hashes.

## 4. A scanner reports a critical CVE in a package name shared by two ecosystems. What should happen next?

Do not automatically fail or dismiss it. Confirm the actual component ecosystem, supplier, version, purl/hash, and vulnerable range. Review scanner mapping evidence. If unresolved, classify under investigation and block or require review according to risk policy.

## 5. Explain why severity-only release policy is weak.

Severity omits component-presence confidence, exploit preconditions, reachability, environment, fix availability, business impact, and evidence freshness. It can block irrelevant findings while allowing exploitable medium-severity issues. Use severity as one dimension in a documented decision.

## 6. Design evidence for a “vulnerable code not present” VEX justification.

Bind the exact image digest; identify the CVE and component; show the compiled binary/component hash; provide source/build flags and symbol or binary-content evidence that the vulnerable code is absent; state tool limitations; define which dependency/build changes invalidate the assertion; assign an owner and review date.

## 7. Why must a VEX statement be bound to an exact product digest?

A dependency update, compiler flag, base image, or packaging change can alter affectability. A statement about digest A cannot authorize digest B merely because both share a version tag. Exact subject binding makes assumptions auditable and prevents stale evidence reuse.

## 8. A `scratch` image has one static Go binary. Is a one-component SBOM necessarily incomplete?

It can be correct if the image truly contains one static first-party binary and no separately represented dependencies/data under the chosen BOM policy. Verify static linkage, rootfs inventory, and whether language modules should be represented as components. Component count alone cannot decide.

## 9. What does an unknown license field mean operationally?

The release lacks sufficient license evidence for that component. Operational response depends on policy: block, require legal/compliance review, replace the component, or accept under an expiring exception. It should not be silently interpreted as permissive.

## 10. Explain the trade-off between embedding an SBOM in the image and attaching it as an OCI artifact.

Embedded evidence is available with the image offline but changes image bytes and can be harder to update independently. Attached OCI artifacts preserve immutable image identity, allow multiple/evolving evidence objects, and support referrer discovery, but availability depends on registry behavior and retention. Both require subject verification.

## 11. A new base digest changes only CA certificates. Must the SBOM/VEX be reevaluated?

Yes. The image subject and inventory changed. New certificate packages/files may have licenses or vulnerabilities; old VEX statements are bound to the prior digest. The reevaluation may be quick, but it must be explicit.

## 12. Write a completeness rule for the Atlas API image.

Require the Atlas API first-party component with exact binary SHA-256 and purl/version; reconcile all locked Go modules under the chosen representation policy; confirm no unexpected regular executable/shared-library files in the rootfs; require declared licenses; and bind the BOM to the exact index/manifest with platform coverage.

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
