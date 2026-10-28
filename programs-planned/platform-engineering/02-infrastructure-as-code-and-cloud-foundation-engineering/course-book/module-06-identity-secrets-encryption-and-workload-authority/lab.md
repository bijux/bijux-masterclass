# Lab — Prove Least Privilege with Denials

## Goal

Demonstrate that the Atlas workload identity has the minimum authority required for runtime behavior, that trust and permission policies are evaluated separately, and that forbidden actions fail for explainable reasons.

## Safety boundary

The required path uses a bounded local policy evaluator, checked trust profiles, launch-template fixtures, and secret-pattern scans. The evaluator intentionally models only the policy features used by Atlas and must not be represented as the complete AWS IAM engine. The optional cloud path may use only a disposable role, instance profile, and sandbox resources.

## Baseline

Inspect:

```text
capstone/fixtures/identity/atlas-instance-policy.json
capstone/fixtures/identity/atlas-instance-vectors.json
capstone/fixtures/identity/ci-trust-profile.json
capstone/fixtures/compute/launch-template-v1.json
```

Create an authority matrix for configuration reads, secret reads, backup-object operations, KMS use, logging, and metadata access.

## Hypothesis

A policy is not least privilege because it is short. Useful proof requires successful necessary actions and failed unnecessary actions. Role trust answers *who may obtain the role*; permission policy answers *what the role may do*. Resource policy, key policy, organization guardrails, permission boundaries, and session policy may also affect a decision. Bootstrap data must contain references rather than durable secrets, and the instance metadata path must reject legacy unauthenticated access.

## Controlled action

1. Evaluate every allow and deny vector in `atlas-instance-vectors.json`.
2. Attempt wildcard resource mutation and unrelated-prefix access; retain the denials.
3. Evaluate `bad-administrator-policy.json` and explain why apparent convenience destroys the workload boundary.
4. Inspect the workload trust policy separately from action permissions.
5. Evaluate the CI OIDC trust profile using an untrusted fork or pull-request subject and retain the rejection.
6. Inspect `launch-template-v1.json` and reject any configuration permitting IMDSv1 or exposing sensitive user data.
7. Evaluate `bad-bootstrap-secret.json` and scan HCL, fixtures, outputs, and user data for embedded secret patterns.
8. For one denied action, walk through organization policy, trust, identity policy, resource policy, KMS key policy, permission boundary, and session policy. Mark layers absent from the fixture rather than inventing them.
9. Optional Level C: attach the role to a disposable sandbox instance and execute both allowed and denied API calls. Record request identifiers, not credentials.

## Oracle

- required configuration, secret, backup, and key-use actions pass only on declared resources;
- IAM mutation, network mutation, state-backend mutation, unrelated-prefix access, and secret enumeration fail;
- broad administrator policy is rejected;
- role trust excludes untrusted CI subjects;
- IMDSv1 is disabled and token use is required;
- bootstrap material contains no durable secret value;
- every denial is attributable to a decisive explicit deny or missing allow within the bounded model.

## Evidence

Retain the action/resource/condition matrix, trust-policy analysis, positive and negative decision records, metadata-profile result, secret scan, and one complete multi-layer authorization explanation. Redact all credentials and secret values.

## Interpretation

Explain why a successful required call is as important as a denied forbidden call: a policy that denies everything is not a useful workload policy. Distinguish encryption permission from data authorization, and explain why access to a KMS key alone does not grant access to ciphertext stored elsewhere.

## Cleanup

Delete any sandbox instance profile, role session, test object, secret version, and temporary KMS grant. Remove local generated evidence containing identifiers or request payloads, then run `make clean`.

## Completion gate

You pass only when all required operations succeed, all forbidden operations fail, the trust and permission paths are analyzed separately, and one denial is traced through every applicable policy layer without relying on the phrase “IAM blocks it.”
