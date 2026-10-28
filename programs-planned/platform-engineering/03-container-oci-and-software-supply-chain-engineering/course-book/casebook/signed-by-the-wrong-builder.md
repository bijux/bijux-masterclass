# Incident case — signed by the wrong builder

## Situation

A pull-request workflow built an Atlas image and obtained a valid keyless signing certificate. Signature verification succeeded, the transparency entry was present, and the release was promoted. The workflow identity, however, was authorized only for test artifacts. The source revision was an unreviewed pull-request merge commit rather than a protected release ref.

The cryptography worked exactly as designed. The authorization policy did not.

## Why “valid signature” was insufficient

A signature answers whether a particular key or certified identity authenticated particular bytes. Release trust adds more questions:

- Is the issuer accepted?
- Is this exact repository/workflow/ref/environment identity authorized?
- Did the expected builder produce the subject?
- Does provenance identify the protected source revision and materials?
- Are completeness claims sufficient for this environment?
- Is the signer/build identity revoked or under incident response?

The original verifier trusted a broad issuer and repository. It did not constrain workflow file, protected branch/tag, environment, or builder ID. It therefore authenticated an identity that was genuine but outside production authority.

## Correct verification order

1. Resolve the candidate by immutable digest.
2. Verify the attestation subject equals that digest.
3. Verify envelope/signature/certificate and transparency evidence.
4. Constrain issuer and exact workload identity.
5. Constrain repository, workflow, ref, and protected environment.
6. Evaluate provenance builder ID, source revision, materials, parameters, and completeness.
7. Apply vulnerability, inventory, runtime, platform, and target-environment gates.
8. Record the final decision independently from the signature result.

## Response

Promotions from the broad identity were frozen. All subjects signed by it were enumerated. Running releases were reviewed for source and builder authority, not automatically declared malicious. Policy was narrowed; protected release workflows were re-established; replacement releases were issued where origin could not be proven.

## Transfer lesson

Cryptographic validity is necessary evidence. Authorization is a separate organizational decision over identity, subject, origin, environment, and time. A release system that reports only “signature verified” hides the most important part of the trust argument.
