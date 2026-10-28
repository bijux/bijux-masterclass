# Module 09 — Adversarial Verification and Supply-Chain Assurance

> **Program stage:** Course 3 of 6 — Defend the promise.

> **Central question:** How do adversarial tests and supply-chain evidence show that controls fail closed and that the proof is sensitive?

## Where this module fits

Combine negative tests, property-based input, fuzz boundaries, planted vulnerabilities, dependency evidence, and build integrity. You arrive from Module 08 with all earlier checkpoints still green. API 1.2 and its durable service behavior are fixed. This course adds controls derived from explicit threats; it does not redefine successful business outcomes or treat middleware configuration as proof of security. The result is the baseline for **Security Operations and Incident Response**.

## Learning outcomes

- Trace tests to threats and requirements.
- Remove or mutate controls and confirm the proof fails.
- Use shared hostile vectors across languages.
- Pin direct and transitive dependencies and produce an SBOM.
- Interpret scanner output instead of treating tools as authorities.

## Capstone result

Build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition.

Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.

## Core security model

> How do we prove the controls detect realistic defects, and how do we reason about the code and dependencies that supply those controls?

Security evidence must be sensitive to control removal, reproducible, scoped, and linked to requirements. Scanners and dependency reports are useful inputs, but only interpreted findings, lock integrity, provenance, and executable counterexamples support a defensible claim.

Separate public behavior, control decision, authoritative state, evidence, and operating assumption for every concept.

### 1. Negative test

Supplies an invalid or malicious case and asserts the safe public/internal outcome.

Generates a range of representations around an invariant instead of enumerating a few examples.

Targets a parser or protocol surface with a clear crash, hang, divergence, or acceptance oracle.

Deliberately removes or weakens one control to prove the evidence route fails for the intended reason.

Measures whether tests detect meaningful security-control changes rather than only preserving implementation shape.

Dependency resolution is captured and verified; direct pins without transitive resolution are incomplete.

Inventory and build origin support response and traceability; neither proves absence of vulnerabilities.

Each alert is confirmed, rejected with evidence, mitigated, accepted with expiry, or deferred with owner; raw scanner counts are not conclusions.

## A security test needs an adversary and an oracle

Calling an input `malicious` does not make a test adversarial. State the attacker capability, the control being challenged, and the prohibited outcome. Then construct the smallest input that would produce that outcome if the control were absent.

Negative tests should cover boundary combinations, not only isolated invalid values. A valid token with the wrong audience, a correct scope for the wrong owner, a public webhook hostname that resolves partly private, and a safe archive member combined with an excessive cumulative size are more informative than random malformed strings.

Property-based generation is useful when invariants are explicit: every accepted path resolves beneath the root; every rejected JWT profile violation remains rejected under irrelevant claim ordering; every permit acquisition is balanced by release; every canonical JSON value has identical bytes in both languages. Fuzzing without an oracle mostly measures crashes. A crash oracle is valuable, but it is not proof of authorization or confidentiality.

### Prove that the proof can fail

Keep controlled mutants or planted defects outside the release path. Remove one audience check, reverse one ownership predicate, permit one private address range, omit one replay write, or log one secret. The relevant test must fail for the predicted reason. If the entire suite stays green, the security claim was not actually covered. If hundreds of unrelated tests fail, minimize the oracle so future regressions remain diagnosable.

Shared hostile vectors prevent the Python and TypeScript tracks from quietly defining different security profiles. Each vector should name the expected category and public outcome; framework-specific exception text is not a parity requirement.

Supply-chain evidence begins with deterministic dependency inputs. Pin direct dependencies and retain the ecosystem lockfile that resolves transitives. Separate build, development, and runtime dependencies. Generate an SBOM from the resolved graph and artifact, record provenance for the build, scan source and artifacts for secrets, and review licenses or policy restrictions where relevant.

A scanner result is a lead, not a verdict. Triage affected component and version, reachability, exploit preconditions, available fix, compensating controls, and deadline. False positives must be documented; false negatives remain possible. “The scanner passed” is not a security case.

Reproducibility claims need a clean, network-controlled build and byte or semantic comparison of produced artifacts. A dependency install performed against a changing registry during the proof does not establish the same input graph. Signing a non-reproducible artifact can establish origin, not correctness.

The final proof ladder links threat, requirement, code, negative vector, mutant sensitivity, dependency evidence, and residual limitation. That is stronger than a long list of tools because it explains which security property each result supports.

## Security requirements and standards

1. The service MUST satisfy **Negative test**: Supplies an invalid or malicious case and asserts the safe public/internal outcome.
2. The service MUST satisfy **Property test**: Generates a range of representations around an invariant instead of enumerating a few examples.
3. The service MUST satisfy **Fuzz boundary**: Targets a parser or protocol surface with a clear crash, hang, divergence, or acceptance oracle.
4. The service MUST satisfy **Planted defect**: Deliberately removes or weakens one control to prove the evidence route fails for the intended reason.
5. The service MUST satisfy **Mutation sensitivity**: Measures whether tests detect meaningful security-control changes rather than only preserving implementation shape.
6. The service MUST satisfy **Lock integrity**: Dependency resolution is captured and verified; direct pins without transitive resolution are incomplete.
7. The service MUST satisfy **SBOM and provenance**: Inventory and build origin support response and traceability; neither proves absence of vulnerabilities.
8. The service MUST satisfy **Finding disposition**: Each alert is confirmed, rejected with evidence, mitigated, accepted with expiry, or deferred with owner; raw scanner counts are not conclusions.

## Worked attacks and defenses

Run only against course fixtures. The goal is to understand control boundaries, not to maximize payload novelty.

### Attack 1 — Oracle-free fuzzing

A fuzzer produces inputs but the test treats every non-crash response as acceptable, missing authorization bypasses.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 2 — Assertion weakening

A planted defect is “fixed” by accepting both deny and allow responses.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 3 — Fixture-only coverage

All tests use one issuer, key, tenant, and path shape; boundary variants remain untested.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 4 — Unpinned transitive update

A clean install resolves different security-critical code than the reviewed build.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 5 — Secret in test artifact

Reports, snapshots, or failing assertions archive fixture-private material into release outputs.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 6 — Scanner substitution

A green dependency scan is presented as proof of authorization, SSRF, or token validation.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.

### Prioritization

Rank these attacks using explicit asset impact, caller capability, exposure, and confidence in controls. Record which require environment-backed evidence.

## Python implementation

### Reference design

Use pytest parameterization over shared vectors, hypothesis where available behind an optional target, and explicit control-mutation fixtures. Generate deterministic JSON reports. Inspect installed/pinned dependency metadata without fetching during core proof.

### Work method

Use explicit immutable inputs, narrow exception taxonomies, and standard-library/PyJWT cryptography through named profiles.

## TypeScript implementation

### Reference design

Use Node test for local vectors and Vitest/fast-check in the full profile. Compile core security modules separately from Fastify. Add source guards for unsafe parser/auth shortcuts, but label them structural checks rather than semantic proof.

## Failure patterns

### 1. Calling a test adversarial because the input has a suspicious name but no harmful property.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 2. Keeping planted defects only in prose, so proof sensitivity is never executed.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 3. Allowing network installs during a reproducibility proof.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 4. Failing the build on every scanner alert without triage or exploitability context.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 5. Ignoring vulnerabilities in development/build tools that affect released artifacts.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 6. Publishing private keys, tokens, or peppers in test evidence and SBOM attachments.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

## What you add to the capstone

### Objective

Assemble the complete adversarial proof ladder. Execute at least six planted defects, minimize failures, generate dependency/SBOM evidence with available tools, triage a fixture vulnerability, and prove private fixture material is absent from release staging.

### Required artifacts

Do not modify predecessor bytes or convert missing environment capabilities into passes.

## Representative implementation

These are the smallest useful entry points for **Adversarial Verification and Supply-Chain Assurance**.

### Python — `capstone/tracks/python-fastapi/tests_security/test_gateway.py`

```python
P = Principal("u1", "t1", frozenset({"projects:read"}))


def validator(_value: str) -> Principal:
    return P


def test_exactly_one_credential_channel():
    assert authenticate_exactly_one(CredentialInputs(bearer_token="x"), bearer_validator=validator, api_key_validator=validator) == P
    with pytest.raises(SecurityControlError) as caught:
        authenticate_exactly_one(CredentialInputs(), bearer_validator=validator, api_key_validator=validator)
    assert caught.value.code == "credential-required"
    with pytest.raises(SecurityControlError) as caught:
        authenticate_exactly_one(CredentialInputs("x", "y"), bearer_validator=validator, api_key_validator=validator)
    assert caught.value.code == "credential-ambiguous"


def test_integrated_authentication_and_authorization():
    policies = {"getProject": Policy("getProject", frozenset({"projects:read"}), relationship="owner", conceal=True)}
    principal, decision = security_decision("getProject", inputs=CredentialInputs(bearer_token="x"), resource=ResourceFacts(tenant="t1", owner="u1"), policies=policies, bearer_validator=validator, api_key_validator=validator)
    assert principal == P and decision.allowed
    _, denied = security_decision("getProject", inputs=CredentialInputs(bearer_token="x"), resource=ResourceFacts(tenant="t2", owner="u2"), policies=policies, bearer_validator=validator, api_key_validator=validator)
    assert not denied.allowed and denied.conceal
```

### TypeScript — `capstone/tracks/typescript-fastify/test-security-core/gateway.test.mjs`

```yaml
import assert from "node:assert/strict";
import { authenticateExactlyOne, securityDecision } from "../dist-security/security/gateway.js";

const principal={subject:"u1",tenant:"t1",scopes:new Set(["projects:read"]),roles:new Set(),assurance:"baseline",authAgeSeconds:0};
const validator=()=>principal;

test("exactly one credential and integrated policy",()=>{
  assert.equal(authenticateExactlyOne({bearerToken:"x"},validator,validator),principal);
  assert.throws(()=>authenticateExactlyOne({},validator,validator),(e)=>e.code==="credential-required");
  assert.throws(()=>authenticateExactlyOne({bearerToken:"x",apiKey:"y"},validator,validator),(e)=>e.code==="credential-ambiguous");
  const policies=new Map([["getProject",{operationId:"getProject",scopes:new Set(["projects:read"]),roles:new Set(),relationship:"owner",tenantBound:true,conceal:true,requiredAssurance:"baseline"}]]);
  const allowed=securityDecision({operationId:"getProject",credentials:{bearerToken:"x"},resource:{tenant:"t1",owner:"u1",members:new Set()},policies,bearerValidator:validator,apiKeyValidator:validator});
  assert.equal(allowed.decision.allowed,true);
  const denied=securityDecision({operationId:"getProject",credentials:{bearerToken:"x"},resource:{tenant:"t2",owner:"u2",members:new Set()},policies,bearerValidator:validator,apiKeyValidator:validator});
  assert.equal(denied.decision.allowed,false); assert.equal(denied.decision.conceal,true);
});
```

Compare the two tracks by this invariant: **negative vectors, mutants, locks, SBOM/provenance evidence, and vulnerability disposition prove controls and build inputs**. The intended implementation difference is: testing ecosystems differ; shared hostile cases and planted vulnerabilities must produce equivalent outcomes.

## Module synthesis

The module answer to “How do we know a security check detects a missing control rather than merely confirming the control is present?” is now executable in the capstone: Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.

## Next in the story

Module 10, [Security Operations and Incident Response](../module-10-security-operations-and-incident-response/index.md), asks: *When a credential, key, or dependency is compromised, how do we contain the event without destroying evidence or breaking the API?* The current checkpoint must remain green while that new responsibility is added.
