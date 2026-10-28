# Worked answers — Release promotion and handoff

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. Distinguish build record, registry record, and release record.

A build record describes transformation inputs, builder, and outputs. A registry record describes where immutable objects and mutable references were stored/distributed. A release record authorizes exact subjects for an environment after evaluating required evidence. None substitutes for the others.

## 2. Why should target-environment promotion reevaluate policy even for the same digest?

Production may require stronger identity, native-platform, retention, rollback, or vulnerability evidence than development. Evidence can expire or be revoked. The digest stays immutable, but authorization context changes. Reuse evidence where valid; rerun target-specific gates.

## 3. Explain why gate ordering matters.

Early gates establish subject identity and applicability. Evaluating vulnerability or signature evidence before confirming the subject can launder evidence from another artifact. Non-compensable failures must stop the decision before attractive later signals create false confidence.

## 4. Design an expiring exception record for a review-required vulnerability.

Include exact digest/CVE/rule, current finding status, risk analysis, owner and approver, affected environments, compensating controls, monitoring, remediation issue, creation and expiry, automatic revocation triggers, and evidence required to close. It must not silently apply to future digests.

## 5. A previous image digest exists, but the database schema changed incompatibly. Is rollback ready?

No. Artifact availability is necessary but application/data compatibility is missing. A rollback plan needs schema compatibility, down-migration or forward-compatible old code, configuration/key compatibility, and tested operational steps. Otherwise the old image may start and corrupt or fail against current state.

## 6. Distinguish image, signing-key, evidence, and tag revocation.

Image revocation blocks a digest. Key revocation removes trust in signatures/identity and triggers reevaluation of subjects. Evidence revocation withdraws an SBOM/VEX/provenance claim. Tag revocation moves/deletes a mutable pointer. Actions and blast radius differ.

## 7. Why must registry garbage collection understand release holds and referrers?

Untagged manifests may still be approved by digest, referenced by referrer subjects, required for rollback, or retained for incident investigation. Naive GC can delete evidence or child blobs while records remain. Release holds and graph reachability must inform deletion.

## 8. Which Course 3 facts belong in the Kubernetes handoff, and which decisions must wait for Course 4?

Course 3 supplies exact digests, platforms, entrypoints, port, identity, capabilities, mounts, health semantics, shutdown, resource hypotheses, evidence/admission expectations, configuration/secret/storage/network contracts. Course 4 decides Pod specs, controllers, Services, probes, volumes, scheduling, rollout, and cluster policy.

## 9. A candidate passed semantic builds but native arm64 execution was unavailable. How should production release classify it?

Classify arm64 target execution as not executed and block production if native evidence is mandatory. The multi-platform structure can be accepted for a lower environment or review state according to policy, but cross-compile/ELF evidence must not be mislabeled native runtime proof.

## 10. The signing key is compromised, but independent rebuild matches. Outline the response.

Revoke key acceptance, identify subjects and signing times, freeze promotions, validate independent provenance/source/rebuild evidence, provision a new signing identity, decide which exact digests can be reauthorized, update admission/deployments, rotate automation credentials, and preserve incident evidence. Distinguish artifact compromise from signer compromise.

## 11. Explain why re-signing an old digest can be legitimate or dangerous.

Legitimate when independent evidence establishes the immutable digest and a newly authorized signer intentionally reauthorizes it under current policy. Dangerous when re-signing is used to erase uncertainty about the original build, vulnerability state, or compromise. Record why the digest remains trustworthy and retain old history.

## 12. Write the final Atlas release claim with an explicit evidence boundary.

“Atlas Workload Release 1.0 selects the recorded API, worker, and probe multi-platform index digests; passes course structural, platform, runtime-profile, inventory, vulnerability/VEX, provenance, signature, and controlled-rebuild gates; and publishes exact Course 4 contracts. Native external-tool, production-registry, cloud-identity, and Kubernetes admission evidence remains not executed unless separately recorded.”

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
