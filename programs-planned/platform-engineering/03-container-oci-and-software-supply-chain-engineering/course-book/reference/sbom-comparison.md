# SBOM comparison and completeness

An SBOM is an inventory claim for a subject and scope. Schema validity does not prove the inventory is complete or correctly bound.

## CycloneDX and SPDX

Both formats can represent components, identities, licenses, hashes, and relationships. CycloneDX commonly emphasizes software-component and vulnerability-oriented workflows. SPDX provides rich package/file/license and relationship vocabularies. Format choice matters less than accurate subject binding, component identity, relationship coverage, and generation evidence.

## Completeness dimensions

Evaluate at least:

- **subject coverage** — every released image/platform covered;
- **application coverage** — first-party binaries/modules represented;
- **OS/package coverage** — distribution packages and unmanaged files;
- **language coverage** — resolved runtime/build dependencies;
- **file/binary coverage** — hashes or paths where policy requires them;
- **relationship coverage** — dependency/contains/generated-from relationships;
- **license coverage** — declared/concluded license and evidence;
- **tool blind spots** — static binaries, plugins, vendored code, generated assets.

Compare SBOM output with independent sources: package manager databases, language lockfiles, compiler module lists, image filesystem inventory, and known application artifacts. Differences are evidence, not automatically errors; they need explanation.

## Multi-platform releases

Platform variants can differ in binaries, shared libraries, OS packages, hashes, and generated files. One generic source SBOM may support understanding, but release authorization should state exactly which image subjects it covers. Prefer per-subject evidence or an aggregate document with explicit component-to-platform relationships.

## Vulnerability and VEX flow

```text
subject-bound inventory
→ identity normalization
→ vulnerability matching
→ applicability/reachability analysis
→ owned disposition
→ release decision
```

A VEX statement needs exact product subject, vulnerability identifier, status, justification, evidence, author, timestamp, and review/expiry semantics. `not_affected` is not a permanent suppression label.

## License decisions

Unknown or conflicting license evidence is usually review-required, not automatically safe or automatically prohibited. Policy should distinguish detection uncertainty, legal review, distribution context, and remediation ownership.
