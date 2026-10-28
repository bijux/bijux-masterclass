# Module 10 — Security Operations and Incident Response

> **Program stage:** Course 3 of 6 — Defend the promise.

> **Central question:** How is a suspected compromise detected, contained, investigated, rotated, patched, and converted into improved requirements?

## Where this module fits

Run a controlled security incident from detection through containment, recovery, compatible release, and post-incident learning. You arrive from Module 09 with all earlier checkpoints still green. API 1.2 and its durable service behavior are fixed. This course adds controls derived from explicit threats; it does not redefine successful business outcomes or treat middleware configuration as proof of security. The result closes the course and produces the handoff to **API Reliability and Observability Engineering**.

## Learning outcomes

- Design actionable security events and audit records.
- Revoke tokens and API keys deliberately.
- Rotate webhook and signing keys with overlap.
- Preserve timelines and confidence levels.
- Update threats, controls, and tests after the incident.

## Capstone result

Run a controlled credential and cross-tenant incident with timelines, revocation, rotation, release, and threat-model revision.

Course 3 ends with security profile 1.0, migrations 006–007, and a closed compromise exercise.

## Core security model

> How does the team detect, contain, recover from, and learn from credential compromise or security-control failure without destroying evidence or breaking the API?

Incident readiness is an engineered capability: event vocabulary, revocation, rotation, compatible releases, evidence preservation, decision ownership, and proof reruns exist before the crisis. Recovery includes updating the security case, not only restoring service.

Separate public behavior, control decision, authoritative state, evidence, and operating assumption for every concept.

### 1. Security event

A structured, minimized record that may support detection or investigation; not every application log is a security event.

A rule or analysis that turns events into a reviewable alert with threshold, context, and false-positive expectations.

Confirm scope, confidence, assets, attacker capability, and immediate risk before broad destructive action.

Reduce ongoing harm through revocation, key disablement, destination blocking, budget changes, or feature restriction while preserving evidence.

Remove root cause, issue a compatible fix, restore trusted operation, validate data/state, and monitor for recurrence.

Record source, timestamps, hashes, access, and uncertainty; avoid modifying original artifacts unnecessarily.

Security changes preserve public behavior where possible and carry explicit contract/database compatibility evidence.

Revise threats, assumptions, controls, tests, runbooks, ownership, and residual risk based on observed facts.

## Incident response preserves truth while reducing harm

A security incident is not complete when a patch merges. Response must detect, triage, contain, eradicate, recover, verify, communicate, and feed the result back into the security case. The order can overlap, but each action needs an owner and evidence.

Build the timeline from immutable or independently preserved observations: credential issuance and revocation records, authorization decisions, artifact-access events, webhook deliveries, configuration revisions, deployment identifiers, and database facts. Record event time, observation time, source, confidence, and who made the statement. Do not rewrite uncertain early entries; append corrections.

Containment should target the compromised capability. A leaked webhook secret requires key activation, receiver overlap, sender switch, retry verification, and retirement of the compromised key. A suspected token may require token-ID revocation, session or issuer action, and examination of operations performed under that subject. Rotating every secret and shutting down every operation can destroy availability and evidence without containing the actual path.

### Recovery is a verified state transition

Use an incident state machine with explicit legal transitions. “Contained” means the active attack path is blocked and the scope is sufficiently understood to proceed; it does not mean every root cause is fixed. “Recovered” means normal service has resumed under verified controls and monitoring. “Closed” requires completed follow-up ownership, not fatigue.

Key rotation must respect verification overlap unless compromise requires immediate retirement. Token revocation must remain available for the token’s remaining lifetime. Replay records and audit evidence must survive application rollback. A security release still follows contract compatibility rules: emergency pressure does not justify breaking all clients if a compatible deny rule, configuration change, or additive response can contain the issue.

Preserve evidence before destructive remediation. Snapshot relevant configuration and dependency manifests, hash exported logs, record queries and commands, and restrict access. Do not copy live secrets or personal data into a broadly shared incident document. The evidence package should be sufficient to reproduce decisions without becoming a new breach.

Verification repeats the adversarial scenario with repaired controls and checks for side effects: valid tenants still retrieve artifacts, unexpired unaffected tokens remain valid, webhook retries succeed with the new key, old signatures fail after retirement, and generated clients still satisfy API 1.2.

The post-incident review updates threats, assumptions, requirements, tests, runbooks, ownership, and deadlines. Avoid a generic action such as “be more careful.” Prefer a falsifiable change: “unknown webhook key IDs are rejected and the overlap schedule is tested at both boundary timestamps.”

The course incident combines a leaked webhook key, suspected stolen access token, cross-tenant artifact probe, and vulnerable dependency. The objective is not dramatic simulation. It is disciplined containment that preserves durable truth, compatible behavior, and evidence while proving the repaired security profile.

## Security requirements and standards

1. The service MUST satisfy **Security event**: A structured, minimized record that may support detection or investigation; not every application log is a security event.
2. The service MUST satisfy **Detection signal**: A rule or analysis that turns events into a reviewable alert with threshold, context, and false-positive expectations.
3. The service MUST satisfy **Triage**: Confirm scope, confidence, assets, attacker capability, and immediate risk before broad destructive action.
4. The service MUST satisfy **Containment**: Reduce ongoing harm through revocation, key disablement, destination blocking, budget changes, or feature restriction while preserving evidence.
5. The service MUST satisfy **Eradication and recovery**: Remove root cause, issue a compatible fix, restore trusted operation, validate data/state, and monitor for recurrence.
6. The service MUST satisfy **Evidence preservation**: Record source, timestamps, hashes, access, and uncertainty; avoid modifying original artifacts unnecessarily.
7. The service MUST satisfy **Compatible emergency release**: Security changes preserve public behavior where possible and carry explicit contract/database compatibility evidence.
8. The service MUST satisfy **Post-incident learning**: Revise threats, assumptions, controls, tests, runbooks, ownership, and residual risk based on observed facts.

## Worked attacks and defenses

Run only against course fixtures. The goal is to understand control boundaries, not to maximize payload novelty.

### Attack 1 — Leaked webhook secret

A current signing key appears in a build log and forged delivery attempts begin.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 2 — Suspected stolen access token

A valid `jti` shows impossible travel or abnormal run submissions before expiry.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 3 — Cross-tenant artifact probe

Audit shows repeated denied identifiers followed by one anomalous success candidate.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 4 — Vulnerable dependency

A security advisory affects a parsing dependency used at the raw-message boundary.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 5 — Over-broad containment

Operators disable all identity verification or delete logs to restore availability quickly.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 6 — Incomplete rotation

The secret is changed for new deliveries but old verification remains indefinitely or one receiver is missed.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.

### Prioritization

Rank these attacks using explicit asset impact, caller capability, exposure, and confidence in controls. Record which require environment-backed evidence.

## Python implementation

### Reference design

Implement incident state transitions, revocation entries, key-version activation/retirement, evidence records, and a deterministic drill runner. The runner must not mutate predecessor history or include secret values in its report. Generate a compatible release note and rerun requirement-linked tests.

### Work method

Use explicit immutable inputs, narrow exception taxonomies, and standard-library/PyJWT cryptography through named profiles.

## TypeScript implementation

### Reference design

Mirror the incident state machine with exhaustive status handling. Use immutable timeline records and verify sequence/causality separately from wall-clock ordering. The comparison track reviews whether Node process/config reload semantics could leave stale keys or revocation state.

## Failure patterns

### 1. Rotating every secret without identifying which one is compromised, causing unnecessary outage and evidence loss.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 2. Deleting or rewriting logs before preserving hashes and access records.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 3. Treating token expiry as sufficient containment for an actively abused long-lived token.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 4. Patching code but not revoking issued credentials or replay state.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 5. Releasing a breaking API change under emergency pressure without compatibility review.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 6. Closing the incident without updating threats, tests, and assumptions.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

## What you add to the capstone

### Objective

Run the combined compromise scenario: leaked webhook secret, suspected stolen token, cross-tenant artifact attempt, and vulnerable dependency. Detect, triage, contain, rotate/revoke, preserve evidence, release compatibly, rerun proofs, and update threats/residual risks.

### Required artifacts

Do not modify predecessor bytes or convert missing environment capabilities into passes.

## Representative implementation

These are the smallest useful entry points for **Security Operations and Incident Response**.

### Python — `capstone/tracks/python-fastapi/src/api_security/incident.py`

```python
from typing import Iterable


class IncidentStatus(str, Enum):
    DETECTED = "detected"
    TRIAGED = "triaged"
    CONTAINED = "contained"
    RECOVERED = "recovered"
    CLOSED = "closed"


_ALLOWED = {
    IncidentStatus.DETECTED: {IncidentStatus.TRIAGED},
    IncidentStatus.TRIAGED: {IncidentStatus.CONTAINED},
    IncidentStatus.CONTAINED: {IncidentStatus.RECOVERED},
    IncidentStatus.RECOVERED: {IncidentStatus.CLOSED},
    IncidentStatus.CLOSED: set(),
}


@dataclass(frozen=True, slots=True)
class TimelineEntry:
    at: str
    source: str
    statement: str
    confidence: str


@dataclass(slots=True)
class Incident:
    incident_id: str
    status: IncidentStatus = IncidentStatus.DETECTED
    timeline: list[TimelineEntry] = field(default_factory=list)
    revoked_token_ids: set[str] = field(default_factory=set)
    active_webhook_key: str = "whk-2026-01"
    verification_keys: set[str] = field(default_factory=lambda: {"whk-2026-01"})

    def transition(self, target: IncidentStatus) -> None:
        if target not in _ALLOWED[self.status]:
            raise ValueError(f"illegal incident transition {self.status} -> {target}")
        self.status = target

    def record(self, entry: TimelineEntry) -> None:
        self.timeline.append(entry)

    def revoke_token(self, token_id: str) -> None:
        self.revoked_token_ids.add(token_id)

    def rotate_webhook_key(self, new_key_id: str, *, keep_old_for_verification: bool = True) -> None:
        old = self.active_webhook_key
        self.active_webhook_key = new_key_id
        self.verification_keys.add(new_key_id)
        if not keep_old_for_verification:
            self.verification_keys.discard(old)

    def retire_webhook_key(self, key_id: str) -> None:
        if key_id == self.active_webhook_key:
            raise ValueError("cannot retire the active signing key")
        self.verification_keys.discard(key_id)
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/incident.ts`

```typescript
export type IncidentStatus="detected"|"triaged"|"contained"|"recovered"|"closed";
const allowed:Record<IncidentStatus,readonly IncidentStatus[]>={detected:["triaged"],triaged:["contained"],contained:["recovered"],recovered:["closed"],closed:[]};
export interface TimelineEntry{readonly at:string;readonly source:string;readonly statement:string;readonly confidence:string}
export class Incident { status:IncidentStatus="detected"; readonly timeline:TimelineEntry[]=[]; readonly revokedTokenIds=new Set<string>(); activeWebhookKey="whk-2026-01"; readonly verificationKeys=new Set(["whk-2026-01"]); constructor(readonly incidentId:string){} transition(target:IncidentStatus):void{if(!allowed[this.status].includes(target))throw new Error(`illegal incident transition ${this.status} -> ${target}`);this.status=target;} record(entry:TimelineEntry):void{this.timeline.push(Object.freeze({...entry}));} revokeToken(id:string):void{this.revokedTokenIds.add(id);} rotateWebhookKey(id:string,keepOld=true):void{const old=this.activeWebhookKey;this.activeWebhookKey=id;this.verificationKeys.add(id);if(!keepOld)this.verificationKeys.delete(old);} retireWebhookKey(id:string):void{if(id===this.activeWebhookKey)throw new Error("cannot retire active signing key");this.verificationKeys.delete(id);} }
```

Compare the two tracks by this invariant: **revocation, key overlap, evidence preservation, compatible release, verification, and threat-model revision form one controlled timeline**. The intended implementation difference is: state-machine syntax differs; illegal transitions and premature key retirement must fail in both tracks.

## Module synthesis

The module answer to “When a credential, key, or dependency is compromised, how do we contain the event without destroying evidence or breaking the API?” is now executable in the capstone: Course 3 ends with security profile 1.0, migrations 006–007, and a closed compromise exercise.

## Course exit

The ten module results now satisfy this course promise: A threat-driven security profile with hardened edge, identity, authorization, input, outbound, secret, abuse, supply-chain, and incident controls. The next course is **API Reliability and Observability Engineering**; it consumes the outgoing handoff rather than reinterpreting completed work.

## Next in the story

This course now has the mechanism needed for its final defense. The outgoing handoff becomes the immutable starting point for **Course 4 — API Reliability and Observability Engineering**, where the responsibility becomes: Detect, diagnose, contain, reconcile, and recover when processes, dependencies, networks, or operators fail.
