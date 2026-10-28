# Final defense — Atlas Workload Release 1.0

Defend one exact Atlas API and worker release from source to Kubernetes handoff. The defense is an engineering review, not a slide summary.

## Required demonstrations

1. Verify the Course 2 predecessor handoff and name one requirement packaging is forbidden to weaken.
2. Traverse the API image index, both platform manifests, configs, and layers by digest.
3. Recompute at least one compressed layer digest and DiffID; explain why both exist.
4. Demonstrate a secret hidden from the merged rootfs but recoverable from a historical layer, then show the gate that rejects it.
5. Verify amd64 and arm64 executable identities and classify target execution evidence.
6. Resolve/pull the accepted release by digest and show two subject-bound referrers.
7. Run the bounded runtime proof and state exactly what it does and does not establish.
8. Compare SBOM contents with an independent inventory source and defend one VEX decision.
9. Verify provenance/signature, then separately authorize builder/source/subject under policy.
10. Present the categorical release decision, rollback/revocation plan, and exact Course 4 handoff.

## Cross-examination

Be prepared to answer:

- What would still be true if the tag moved?
- What would remain unproved if both controlled builds had equal digests?
- Which evidence must be regenerated when the image index gains a platform?
- Why can a valid signature be rejected?
- What must happen after signing-key compromise?
- Why is the checked mini-runtime not production sandbox evidence?
- Which resource values are hypotheses rather than capacity claims?

## Completion gate

The defense passes only if every non-compensable gate is supported by an exact subject and a rerunnable oracle. Missing native/production evidence may be reported as not-executed; it may not be relabelled as passed.
