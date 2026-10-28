# Module 9 — Provenance, signatures, attestations, and verification policy

A signature answers a narrow question: did the holder of a particular signing identity authorize these bytes or this statement? It does not explain how the artifact was built, whether the signer was allowed to release Atlas, whether the source was reviewed, or whether vulnerabilities are acceptable.

Provenance describes origin and build process. Attestations package signed claims. Verification policy decides which claims and identities are sufficient for a particular action.

## Learning outcomes

By the end of the module you can:

- distinguish artifact signatures, signed attestations, provenance, certificates, and transparency records;
- read an in-toto Statement and SLSA provenance predicate;
- verify subject, builder identity, source/materials, parameters, and build completeness;
- explain DSSE’s role in signing typed payloads;
- compare long-lived key and keyless signing models;
- define trust roots, identity constraints, and revocation/rotation behavior;
- reject valid signatures from unauthorized builders or over wrong subjects;
- write verification policy that composes provenance, SBOM, VEX, and runtime evidence.

## Claims need envelopes and subjects

An in-toto Statement identifies:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{"name": "atlas-api", "digest": {"sha256": "..."}}],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {...}
}
```

The subject binds the claim to exact output bytes. `predicateType` names the claim schema. The predicate contains build details.

If the subject digest differs from the candidate release, the statement is irrelevant even when its signature is valid.

## SLSA provenance describes a build, not a moral verdict

SLSA provenance can record:

- builder identity;
- build type;
- invocation/configuration source;
- parameters;
- resolved dependencies/materials;
- build timing;
- completeness flags;
- reproducibility metadata.

Verification asks whether these fields satisfy policy. A provenance document can honestly show that an untrusted laptop built the image from an unreviewed branch. That is useful evidence and an unacceptable release.

Course 3 uses the approved SLSA 1.2 specification concepts and the provenance v1 predicate. It does not claim a SLSA level merely because a JSON object resembles the schema. Level claims require builder and process properties beyond document generation.

## DSSE separates signing from payload type

Dead Simple Signing Envelope (DSSE) signs a pre-authentication encoding that includes payload type and payload bytes. This prevents a signature over one payload type from being reinterpreted as another.

Conceptually:

```text
PAE(payloadType, payload)
→ signature algorithm
→ signature bytes
→ envelope with key ID, payload type, payload
```

Verification must:

1. decode the envelope;
2. reconstruct the exact PAE;
3. verify the signature with an accepted key/identity;
4. parse the declared payload type;
5. verify statement subject and predicate policy.

The Atlas fixture uses Ed25519 because it is compact and supported by the local environment. The private key is a public course fixture and has no production trust value.

## Long-lived keys and keyless identity

### Long-lived signing key

Advantages:

- works offline;
- simple verification root;
- predictable tooling.

Risks:

- secret storage and rotation;
- broad or ambiguous use;
- compromise window;
- unclear human/service attribution.

### Keyless workflow

A short-lived certificate binds an ephemeral key to an identity asserted by an identity provider. A transparency log can record the signing event. Verification constrains issuer, subject identity, workflow/repository, certificate validity, and log inclusion.

Keyless does not mean trustless. It moves trust to identity provider, certificate authority, transparency service, workflow controls, and verifier policy.

The course teaches Sigstore/Cosign concepts in the native-tool lane but keeps the dependency-light lane local and explicit.

## Builder identity must be constrained

A policy that accepts “any valid signature” is nearly useless. Define:

- accepted key fingerprint or certificate issuer;
- accepted subject/workflow identity;
- repository and ref/branch constraints;
- builder ID/build type;
- expected source URI and commit digest;
- expected materials and base digests;
- parameter allowlist;
- whether build finished successfully;
- evidence freshness and transparency requirements.

The “signed by the wrong builder” case is central. A developer signs an image locally using a valid organization key. Signature verification passes, but release policy rejects it because only the isolated release builder is authorized to produce production provenance.

## Source identity and review

Provenance can bind output to a source commit. Source-track evidence can add controls around authorship, review, branch protection, and source-system integrity.

A release policy might require:

```text
repository = expected Atlas repository
commit = immutable digest
ref = protected release branch or tag
review = required approvals recorded
builder = trusted release builder
materials = pinned and allowed
```

Do not put human review claims into provenance unless the evidence system actually supplies and authenticates them. Link separate source-review attestations if necessary.

## Completeness fields are claims

Provenance may state that parameters or materials are complete. The producer makes that claim; the verifier decides whether it trusts the builder to know and report the full set.

A build with undeclared network access cannot credibly claim complete materials unless the builder captures every relevant fetch. The course release policy rejects provenance whose declared build mode conflicts with material-completeness claims.

## Signature storage and artifact relationships

Signatures and attestations can be stored as OCI artifacts/referrers associated with an image digest. Verification still treats registry storage as untrusted transport:

- retrieve by subject;
- verify descriptor integrity;
- verify signature/certificate;
- verify payload type;
- verify statement subject;
- evaluate predicate policy.

An attacker who can add a new signature artifact cannot make it trusted unless the signer identity/policy is accepted. An attacker who can delete evidence can cause availability failure, so evidence retention and replication matter.

## Rotation, revocation, and compromise

Key rotation requires overlap and a bounded trust transition:

```text
old key accepted
→ new key introduced and independently distributed
→ releases may carry new signature
→ verifier accepts both during overlap
→ old key removed after migration
```

Compromise response must identify:

- which artifacts were signed by the key;
- signing time and identity evidence;
- whether transparency records exist;
- which releases remain trusted through independent provenance/rebuild;
- which keys/certificates/verifier policies must change;
- whether content digests need replacement or only authorization changes.

Revoking a key does not change image bytes. It changes which signatures are accepted. A previously deployed digest may need admission/deployment blocking and rollback even though its integrity remains intact.

## Verification policy composes evidence

Atlas promotion policy evaluates:

```text
structural OCI validity
+ platform truth
+ runtime profile
+ SBOM completeness
+ vulnerability/VEX/license disposition
+ provenance subject/source/builder/materials
+ signature identity
+ controlled rebuild evidence
= release decision
```

A failure in a non-compensable dimension cannot be averaged away by a score. An unsigned image with excellent scan results is still unauthorized. A perfectly signed image with a secret in a layer still fails.

## Worked case: signed by the wrong builder

Candidate A:

- exact Atlas source commit;
- structurally valid multi-platform image;
- complete SBOM;
- no blocked vulnerabilities;
- valid Ed25519 signature;
- provenance builder ID `developer-laptop`.

Policy requires `atlas-release-builder-v1`. Candidate A is rejected.

The signature proves possession of an accepted key only if the key policy allows it. If the same key is shared across laptop and release builder, the policy cannot distinguish origins. The key architecture is defective. Builder identities should be isolated and narrowly scoped.

## Atlas capstone increment

You will:

- generate in-toto/SLSA provenance for the accepted API index;
- package it in a DSSE envelope;
- sign and verify with the course Ed25519 key;
- tamper with payload and subject;
- substitute a valid but unauthorized builder ID;
- test key fingerprint mismatch;
- compare one controlled rebuild;
- evaluate the complete release policy.

The output is a cryptographically verified and policy-authorized candidate, subject to the bounded course evidence class.

## Verification questions

1. What exact bytes or statement are signed?
2. Which key or identity is accepted, and for what purpose?
3. What subject does the statement name?
4. Which source, builder, parameters, and materials are declared?
5. Which claims are complete, and why is the producer trusted to say so?
6. Was source review proven separately?
7. Is the signature/release within validity and revocation policy?
8. Which required evidence is missing, stale, or not executed?
9. Does policy authorize promotion, not merely verify syntax?


## Verification walkthrough — from bytes to authorized release

Consider a DSSE envelope returned as an OCI referrer.

1. **Verify the artifact manifest.** Recompute its digest and ensure its subject is the candidate image/index digest.
2. **Read the declared artifact/payload type.** Do not parse arbitrary bytes under the expected provenance schema.
3. **Verify the DSSE signature.** Reconstruct PAE from the exact payload type and payload bytes. Select a trust root and validate the cryptographic signature.
4. **Authorize the signing identity.** A valid key or certificate must match the expected builder/release identity, issuer, repository/workflow, branch/tag, environment, and validity policy.
5. **Parse the in-toto Statement.** Confirm `_type`, subject name/digest, and predicate type.
6. **Evaluate provenance.** Check source URI and immutable revision, builder ID, build type, parameters, materials, dependency identities, and completeness claims.
7. **Compare independent release evidence.** Ensure the image graph, SBOM, tests, runtime profile, and provenance describe the same subject/platforms.
8. **Record the policy version and decision.** Verification is reproducible only when trust roots, identity rules, time, revocation data, and policy are known.

Cryptographic success at step 3 cannot compensate for a subject mismatch at step 1 or an unauthorized builder at step 4.

## Keyless signing trust chain

A typical keyless workflow binds an ephemeral public key to an identity asserted by an OIDC issuer, obtains a short-lived certificate from a signing CA, and records signing material in a transparency service. Verification then needs:

- trusted certificate/root and issuer;
- certificate validity and intended use;
- subject alternative name/identity constraints;
- repository/workflow/ref/environment claims;
- transparency inclusion/consistency evidence according to policy;
- artifact/statement signature;
- subject and provenance policy.

“Signed with Sigstore” is not enough. A public pull-request workflow can obtain a valid certificate. Policy must restrict which identity is allowed to release Atlas.

## Long-lived key operations

For a managed key, define:

- generation and storage boundary;
- allowed signing purpose;
- online/offline exposure;
- rotation overlap;
- key identifier/fingerprint;
- approvers and audit trail;
- revocation distribution;
- response to lost availability versus suspected compromise.

Course fixture keys are intentionally public and useful only for deterministic exercises. Their presence proves implementation mechanics, not trustworthy custody.

## Provenance completeness and materials

Completeness booleans or equivalent fields are producer claims. Verify them against builder design. If the builder permits unrecorded network access, a claim that materials are complete is not credible. If a build parameter can alter output but is omitted, consumers cannot reproduce or evaluate the decision.

For Atlas, materials include source and toolchain identities. A native build lane should also capture frontend/builder images, base image digests, module lock inputs, and relevant build parameters. Do not invent digests for unavailable tools to make the document look complete.

## Policy composition

A release policy should express non-compensable predicates, for example:

```text
subject digest matches candidate
AND builder identity is authorized
AND source revision is immutable and approved
AND required materials are present
AND platform set is complete
AND SBOM subject/completeness passes
AND vulnerability/VEX disposition passes
AND runtime profile passes
AND required test/evidence classes exist
```

An aggregate score can summarize review but must not allow nine weak successes to compensate for the wrong subject or builder.

## Revocation and historical truth

A later key compromise can make a previously accepted release unauthorized for new deployment. Preserve the original signature and decision for audit, then create a revocation/authorization record with effective time and scope. Do not rewrite historical provenance or delete the old evidence.

The release system should answer separately:

- Was this signature valid under policy at decision time?
- Is the release authorized now?
- May it remain running?
- May it be used for rollback?
- Which replacement or mitigation is required?

## Verification is a trust-graph traversal

A signature verifies that a key authorized exact bytes. Release authorization asks a larger chain of questions:

```text
Which envelope format and payload type?
Which key or certificate verified it?
Why is that identity trusted for this repository and workflow?
What subject digest does the statement name?
Which builder produced the subject?
Which source and materials were resolved?
Which parameters and build type were allowed?
Which independent evidence classes are required?
```

Stopping after cryptographic verification is a common error. An attacker with an untrusted key can create a perfectly valid signature. A trusted key can sign a statement about the wrong subject. A trusted builder can be invoked with an unreviewed source.

### DSSE separates envelope from predicate

DSSE signs a pre-authentication encoding of payload type and payload bytes. Policy must constrain the payload type before interpreting the JSON. Course policy now rejects a valid Ed25519 signature whose envelope advertises `application/json` instead of the expected in-toto payload type. This prevents type confusion from being hidden behind signature success.

The in-toto statement then identifies the subject. SLSA provenance supplies a predicate for build definition and run details. These layers solve different problems; do not flatten them into one “attestation valid” flag.

### Keyless systems move trust; they do not remove it

A keyless signing flow can bind an ephemeral key to an identity-provider claim and publish verification material to a transparency service. Verification still needs issuer policy, subject/workflow constraints, time validity, transparency inclusion, and compromise response. The trust root has moved from a long-lived private key to an identity and logging system.

Course fixtures use a deterministic public Ed25519 key so every learner can reproduce verification. That key is intentionally incapable of providing production identity assurance.

### Policy order matters

Evaluate cheap structural and subject checks before expensive or external work, but do not let an early green check authorize the release. A non-compensable gate can be expressed as conjunction:

```text
digest selected
AND required platforms present
AND runtime profile accepted
AND SBOM subject/coverage accepted
AND vulnerability/VEX policy accepted
AND provenance signature and payload type valid
AND builder/source/material policy accepted
AND evidence class allowed
```

A score cannot compensate for a missing subject match or untrusted builder.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-08-sboms-vulnerabilities-licenses-and-vex/index.md)
- [Next stage](../module-10-release-promotion-revocation-and-kubernetes-handoff/index.md)
