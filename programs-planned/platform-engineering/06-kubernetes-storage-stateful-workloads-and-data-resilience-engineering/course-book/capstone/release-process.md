# Atlas Data Plane release process

Release evaluation is ordered so that a later score cannot hide a missing safety property.

```text
predecessor integrity
→ data authority
→ manifest and API validity
→ binding/topology feasibility
→ CSI capability and lifecycle
→ single-writer fencing
→ snapshot consistency
→ backup and empty-destination restore
→ capacity/performance headroom
→ migration and rollback
→ security/network obligations
→ evidence classification
→ Course 7 handoff
```

## Decision states

- **accepted** — every non-compensable gate passes at the required evidence level;
- **review-required** — the design is coherent but one bounded decision or evidence gap needs accountable approval;
- **rejected** — a correctness, authority, recoverability, or compatibility gate fails;
- **not-executed** — the required environment was unavailable, so no pass claim is made.

## Release meeting

The learner presents the critical data journey from write acknowledgement through failure and restore. Reviewers challenge deletion authority, stale-writer behavior, missing keys, topology loss, partial expansion, and rollback after cutover. The final decision names residual risks and owners rather than declaring the platform generically “production ready.”
