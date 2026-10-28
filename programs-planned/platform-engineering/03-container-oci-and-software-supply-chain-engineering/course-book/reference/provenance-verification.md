# Provenance verification

Provenance is a signed or otherwise authenticated claim about how subjects were produced. Verification must progress from bytes to authorization; skipping an early step can authenticate the wrong object.

## Verification sequence

1. **Select immutable subject.** Resolve the candidate image index/manifest digest.
2. **Fetch evidence by digest.** A referrer listing is only discovery.
3. **Verify envelope bytes.** Check DSSE/signature/certificate/transparency evidence according to the signing profile.
4. **Check predicate type.** Parse only the expected provenance schema/version.
5. **Match subjects.** Every authorized image digest must be present exactly; unexpected or missing subjects require policy treatment.
6. **Authorize builder identity.** Compare builder ID and signing identity with an allowlist scoped to repository, workflow, environment, and release role.
7. **Verify source identity.** Require exact repository and revision; enforce protected ref/review rules separately.
8. **Inspect materials.** Compare base images, dependencies, toolchain, and other declared inputs with locks or policy.
9. **Inspect invocation.** Evaluate build type, parameters, target platform, network/cache/secret profile, and invocation identity.
10. **Evaluate completeness and evidence class.** Completeness fields are claims; independently corroborate where required.
11. **Check revocation and time.** A once-valid identity or builder may no longer be authorized.
12. **Compose with other gates.** Provenance does not replace image structure, runtime, vulnerability, license, or target policy.

## Keyless and long-lived keys

Keyless verification needs issuer, workload identity, certificate validity, transparency evidence, and exact identity constraints. Long-lived-key verification needs key custody, authorized use, rotation, revocation, and historical validity. Neither model makes a signature self-authorizing.

## Common false positives

- valid signature over evidence whose subject is the previous image;
- trusted issuer with overly broad repository/workflow match;
- correct source repository but unreviewed revision;
- authorized builder with undeclared network/material input;
- top-level index provenance that silently omits one platform child;
- provenance generated after the fact by a system that did not observe the build.

The verifier’s output should be a structured decision explaining which predicates passed, failed, remained unexecuted, or required review—not a single green “verified” label.
