# Evidence model

This course separates claims by the mechanism and environment capable of falsifying them. A green check is meaningful only when its oracle is strong enough for the claim.

## Evidence classes

### Documentary

A specification, design, or policy states what should be true. Examples: runtime profile, release policy, retention design, Course 4 handoff. Documentary evidence is necessary but does not show implementation behavior.

### Dependency-light semantic

The included Python/Go implementation executes object construction, parsing, policy, registry, runtime, and release mechanisms without optional product dependencies. It proves the course model and selected edge cases. It is not independent conformance evidence.

### Independent native-tool

A separate builder, runtime, registry client, inventory/scanning tool, or signing system executes the same mechanism. This challenges assumptions embedded in the semantic implementation and tests interoperability.

### Target-runtime/environment

The intended architecture, kernel, runtime, registry, identity system, or cloud environment exercises the integration. Emulated execution remains labelled as emulated.

### Operated evidence

Retention, recovery, rotation, capacity, support, incident response, and long-lived behavior are demonstrated over time under real ownership. A one-time deployment is not operated evidence.

## Categorical outcomes

Every gate reports:

- **passed** — the required evidence supports the bounded claim;
- **rejected** — a non-compensable rule failed;
- **review-required** — evidence exists but needs an owned human decision;
- **not-executed** — the required environment/tool was unavailable or intentionally out of scope;
- **failed experiment** — the mechanism did not behave as expected and needs diagnosis.

`not-executed` must never be silently converted to `passed`. `review-required` must name the owner and missing decision.

## Evidence chain

```text
claim
  ↓ requires
subject + mechanism + environment
  ↓ observed by
oracle capable of rejecting the claim
  ↓ preserved as
exact evidence with tool/version/time
  ↓ interpreted into
bounded conclusion + residual risk
```

Example:

> Claim: Atlas API runs with a read-only root and only declared writable paths.

- Subject: exact API/probe image and runtime profile.
- Mechanism: mount namespace/rootfs/mount configuration.
- Oracle: writes to `/etc`, `/tmp`, and `/var/lib/atlas`; `/proc` mount evidence.
- Evidence: normalized config and probe output under the checked harness.
- Conclusion: profile behavior passed in the root-managed course harness.
- Boundary: not proof of fully rootless operation, maintained seccomp/LSM, or hostile multi-tenant safety.

## Non-compensable gates

The release cannot pass when any of these fail:

- immutable subject identity;
- object-graph integrity;
- required platform truth;
- secret-history hygiene;
- runtime authority profile;
- subject-bound inventory/provenance/signature;
- authorized builder/signer/source;
- honest evidence classification;
- consistent successor handoff.

A weighted average is inappropriate. A clean scanner result cannot offset a mutable tag or root runtime.

## Evidence journal fields

For every experiment record candidate digest, source/material identity, tool/version, host/environment, start/end time, configuration, controlled fault, expected oracle, raw output location, interpretation, cleanup, and strongest/nearest-unproved claim. Use the [release evidence journal](guides/release-evidence-journal.md) as a template.
