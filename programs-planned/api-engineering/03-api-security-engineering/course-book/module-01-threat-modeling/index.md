# Module 01 — Threat Modeling and Security Requirements

> **Program stage:** Course 3 of 10 — Defend the promise.

> **Central question:** Which assets, actors, trust boundaries, abuse cases, and assumptions define the real security problem?

## Where this module fits

Course 3 begins from this incoming boundary: **The Course 2 API 1.2 durable-service handoff and migrations 001–005.**

This module establishes the course’s first new responsibility by asking: **Which assets, actors, trust boundaries, abuse cases, and assumptions define the real security problem?** Its capstone increment is **Create a security case that traces threats to requirements, control owners, tests, and residual risk**. That result is required before **HTTP Edge and Canonicalization** can be studied honestly.

## Learning outcomes

- Identify assets, actors, entry points, and trust boundaries.
- Write concrete abuse cases and security invariants.
- Use STRIDE as a prompt rather than a substitute for analysis.
- Rank risk with explicit assumptions.
- Trace every control to a threat, requirement, owner, and test.

## Capstone increment

Create a security case that traces threats to requirements, control owners, tests, and residual risk.

## Core security model

### Driving question

> What must be protected, from whom, across which trust boundaries, and how will the course prove it?

Security work begins with an explicit argument about assets, attacker capabilities, trust changes, requirements, assumptions, and residual risk. A long vulnerability list without prioritization or proof ownership is not a security model.

### 1. Asset and security property

Name the data or behavior and the property at risk: confidentiality, integrity, availability, authenticity, accountability, privacy, or safe control.

Describe what the attacker can access or control. “A hacker” is not a usable model; a tenant user with a valid write token is.

Mark where identity, interpretation, privilege, process, host, or administrative ownership changes.

State precondition, attacker action, affected asset, and harmful outcome. Keep it concrete enough to test.

Convert accepted risk into a falsifiable invariant using `must`, actor, object, condition, and observable result.

Record facts the course does not enforce, such as private-key custody or proxy configuration. An assumption is not a control.

State what remains possible after controls and why it is accepted, transferred, monitored, or deferred.

Link threat → requirement → control owner → proof → residual risk. Missing links are visible defects.

### Synthesis

Draw the capstone data flow and annotate where each concept is owned. Any concept with no owner becomes a Module 01 defect.

## From threat list to security case

A useful threat model is a set of claims that can be revised, not a diagram created once and archived. Begin with an asset and the security property that matters. “Artifact” is an asset category; “a principal cannot read an artifact owned by another tenant” is a security property. The second statement can drive an authorization rule, a database-query constraint, an adversarial test, an audit event, and an incident signal. The first cannot.

Model the system through data flows. For each flow, record the sender, receiver, protocol, credential, mutable fields, durable effect, and trust transition. In the Analysis Runs platform, the transition from public API to application use case is different from the transition from worker to artifact store, even when both execute inside one repository. A trust boundary is not synonymous with a network hop. It is any point where the system begins relying on an assertion made under a different authority.

Write abuse cases in operational language:

```text
Given: a valid read token for tenant A
When: the caller substitutes an artifact identifier owned by tenant B
Then: no body, metadata, timing distinction, list count, or audit detail reveals tenant B's artifact
Evidence: owner-constrained query + shared negative scenario + audit record without foreign metadata
```

This format forces four decisions. It states attacker capability, action, prohibited observation, and decisive evidence. “Prevent BOLA” is weaker because it does not identify which caller, resource, or observation matters.

### Threat, requirement, control, and proof are different objects

Keep the chain explicit:

```text
Threat T-004: cross-tenant artifact retrieval
Requirement SR-014: every artifact read is tenant- and relationship-bound
Control: owner-aware repository query plus default-deny operation policy
Proof: valid-token/wrong-owner scenario against both providers
Residual risk: database administrator or compromised service identity remains outside this control
```

A control may mitigate several threats, and one threat may require several controls. Do not collapse the chain into one row called “OAuth.” OAuth can establish or transport authorization information; it does not by itself constrain object ownership, filenames, webhook destinations, or storage paths.

Risk ranking should change sequencing, not create false precision. Use likelihood and impact descriptions tied to assumptions: whether identifiers are guessable, whether the endpoint is Internet-reachable, whether a credential already exists, and whether compromise crosses tenants. Revisit the rank when an assumption changes. A low-ranked internal webhook threat becomes different after a proxy route exposes registration publicly.

### Residual risk is part of the design

A passed unit test does not erase risk. The local course issuer does not prove production identity assurance. An in-process rate limiter does not prove multi-replica enforcement. A hash-chained local audit file does not prevent a privileged operator from replacing both the file and its anchor. Record those boundaries rather than hiding them.

The final security case should allow a reviewer to choose any accepted threat and answer five questions without searching through prose: What is protected? Which boundary is exposed? Which requirement is active? Which implementation owns the control? Which test or live exercise can falsify the claim?

### Keep the model alive

Version the security case with the service. Re-review it when an operation, credential type, trust boundary, dependency, data classification, administrative capability, or deployment route changes. A release diff should state which threats were added, retired, re-ranked, or left unchanged and which assumptions were invalidated. “No security impact” is a conclusion that needs evidence, not a default label.

Accepted residual risk also needs an owner and review trigger. A risk accepted for a local single-tenant fixture may become unacceptable after multi-tenant exposure; a control considered sufficient before public webhook registration may no longer cover the new egress path. Incidents and planted defects feed back into the model: update the failed assumption or requirement, add the minimized counterexample, and preserve the new regression. A threat model that cannot change the implementation or proof plan is documentation, not engineering.

## Security requirements and standards

The course profile turns the mental model into enforceable requirements. `MUST` denotes a non-compensable course invariant; `SHOULD` requires a recorded exception.

1. The implementation MUST satisfy **Asset and security property**: Name the data or behavior and the property at risk: confidentiality, integrity, availability, authenticity, accountability, privacy, or safe control.
2. The implementation MUST satisfy **Actor and capability**: Describe what the attacker can access or control. “A hacker” is not a usable model; a tenant user with a valid write token is.
3. The implementation MUST satisfy **Trust boundary**: Mark where identity, interpretation, privilege, process, host, or administrative ownership changes.
4. The implementation MUST satisfy **Threat scenario**: State precondition, attacker action, affected asset, and harmful outcome. Keep it concrete enough to test.
5. The implementation MUST satisfy **Security requirement**: Convert accepted risk into a falsifiable invariant using `must`, actor, object, condition, and observable result.
6. The implementation MUST satisfy **Assumption**: Record facts the course does not enforce, such as private-key custody or proxy configuration. An assumption is not a control.
7. The implementation MUST satisfy **Residual risk**: State what remains possible after controls and why it is accepted, transferred, monitored, or deferred.
8. The implementation MUST satisfy **Traceability**: Link threat → requirement → control owner → proof → residual risk. Missing links are visible defects.

## Worked attacks and defenses

The Threat Modeling and Security Requirements cases are bounded course fixtures. Trace the attacker-controlled value through every interpreter, then identify the policy decision and smallest rejection evidence; do not target external systems.

### Attack 1 — Cross-tenant artifact read

A valid tenant A token supplies an artifact identifier belonging to tenant B; operation scope alone must not authorize it.

### Attack 2 — Stolen writer token

An attacker obtains a short-lived token with run-write scope and submits expensive analyses until revocation or expiry.

### Attack 3 — Webhook SSRF

A tenant registers a completion URL resolving to a private address and attempts to reach internal infrastructure.

### Attack 4 — Malicious upload

A declared CSV contains oversized data, path-like filenames, or archive members intended to escape staging.

### Attack 5 — Secret in diagnostics

A validation failure includes a bearer token or webhook secret in exception text and structured logs.

### Attack 6 — Queue exhaustion

Many individually valid analysis submissions consume worker and storage capacity for other tenants.

## Python implementation

Use dataclasses or frozen Pydantic models for assets, threats, requirements, and proof links. The checker must reject duplicate IDs, unknown references, requirements without proof, and accepted threats without disposition. Keep the model independent from FastAPI.

## TypeScript implementation

Use discriminated TypeScript types for threat disposition and proof status. A `never` exhaustiveness check should make a newly introduced disposition fail compilation until handling is added. Parse machine-readable files into unknown values before validation.

## Failure patterns

For each pattern, explain why it can look reasonable, construct the smallest counterexample, and identify the missing authoritative boundary.

### 1. Treating STRIDE categories as completed analysis rather than prompts.


### 2. Ranking every threat “high,” which avoids prioritization.


### 3. Writing controls such as “use OAuth” without a testable requirement.


### 4. Assuming the reverse proxy strips malicious headers without deployment evidence.


### 5. Creating tests not linked to any accepted threat.


### 6. Deleting residual-risk text after a unit test passes.

## What you add to the capstone

### Objective

Build the complete capstone security case from the actual data flow. Plant one orphan threat and one requirement with no proof, demonstrate that the checker fails, then repair both.

## Representative implementation

These are the smallest useful entry points for **Threat Modeling and Security Requirements**.

### Python — `capstone/tracks/python-fastapi/src/api_security/models.py`

```python


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    tenant: str
    scopes: FrozenSet[str]
    roles: FrozenSet[str] = frozenset()
    client_id: str | None = None
    token_id: str | None = None
    assurance: str = "baseline"
    auth_age_seconds: int = 0


@dataclass(frozen=True, slots=True)
class ResourceFacts:
    tenant: str | None = None
    owner: str | None = None
    members: FrozenSet[str] = frozenset()
    creator: str | None = None
    status: str | None = None
    attributes: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Decision:
    allowed: bool
    reason: str
    conceal: bool = False
    obligations: tuple[str, ...] = ()
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/models.ts`

```typescript
export interface Principal {
  readonly subject: string;
  readonly tenant: string;
  readonly scopes: ReadonlySet<string>;
  readonly roles: ReadonlySet<string>;
  readonly clientId?: string;
  readonly tokenId?: string;
  readonly assurance: "baseline" | "high" | string;
  readonly authAgeSeconds: number;
}

export interface ResourceFacts {
  readonly tenant?: string;
  readonly owner?: string;
  readonly members: ReadonlySet<string>;
  readonly creator?: string;
  readonly status?: string;
  readonly attributes?: Readonly<Record<string, unknown>>;
}

export interface Decision {
  readonly allowed: boolean;
  readonly reason: string;
  readonly conceal: boolean;
  readonly obligations: readonly string[];
}
```

Compare the two tracks by this invariant: **every accepted threat names an asset, boundary, security requirement, control owner, test, and residual risk**. The intended implementation difference is: Python dataclasses and TypeScript interfaces differ; threat identifiers and policy facts are shared artifacts.

## Module synthesis

You are ready to leave this module when you can **Identify assets, actors, entry points, and trust boundaries, Write concrete abuse cases and security invariants, and Use STRIDE as a prompt rather than a substitute for analysis** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Remove or bypass the central control and prove the predicted oracle fails** and requiring the following oracle: **Identify assets, actors, entry points, and trust boundaries; Write concrete abuse cases and security invariants; Use STRIDE as a prompt rather than a substitute for analysis; Rank risk with explicit assumptions.**

The cumulative platform now includes **Create a security case that traces threats to requirements, control owners, tests, and residual risk**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [HTTP Edge and Canonicalization](../module-02-http-edge-and-canonicalization/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
