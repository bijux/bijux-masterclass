# Worked Answers — Module 10: Security Operations and Incident Response

Use these solutions to audit your reasoning for **Security Operations and Incident Response**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What is the first goal of triage?

Establish credible scope, current harm, affected assets/identities, and immediate containment needs without destroying evidence.

**Capstone check.** Use `capstone/incident/scenario.yaml` to identify the compromised secret before rotating unrelated credentials; preserve a time-stamped action record.

The chapter’s decisive distinction is this: Containment should target the compromised capability. A leaked webhook secret requires key activation, receiver overlap, sender switch, retry verification, and retirement of the compromised key. A suspected token may require token-ID revocation, session or issuer action, and examination of operations performed under that subject. Rotating every secret and shutting down every operation can destroy availability and evidence without containing the actual path.

## 2. When revoke a token `jti` versus a subject?

Revoke the specific token when compromise is isolated; broaden to subject/session/client when evidence suggests wider credential control.

**Capstone check.** Revoke the suspected token identifier and verify subsequent API access fails while unrelated principals remain available.

In the cumulative capstone, the rule becomes concrete: Key rotation must respect verification overlap unless compromise requires immediate retirement. Token revocation must remain available for the token’s remaining lifetime. Replay records and audit evidence must survive application rollback. A security release still follows contract compatibility rules: emergency pressure does not justify breaking all clients if a compatible deny rule, configuration change, or additive response can contain the issue.

## 3. How does webhook key containment work?

Mark the compromised version non-signing, introduce a new active version, update receivers, keep only justified overlap, block/review replay IDs, then retire old verification.

**Capstone check.** Run the cross-tenant artifact probe and preserve request, policy decision, durable access facts, and redacted audit evidence.

A useful way to reason about the boundary is: The course incident combines a leaked webhook key, suspected stolen access token, cross-tenant artifact probe, and vulnerable dependency. The objective is not dramatic simulation. It is disciplined containment that preserves durable truth, compatible behavior, and evidence while proving the repaired security profile.

## 4. Why preserve compatibility during a security release?

Breaking clients can worsen outage and drive unsafe workarounds; security fixes should alter only what is necessary and provide migration evidence.

**Capstone check.** Record the vulnerable component, reachable path, temporary mitigation, fixed version, and rebuild evidence; scanner output alone does not close the incident.

The implementation consequence is: Incident readiness is an engineered capability: event vocabulary, revocation, rotation, compatible releases, evidence preservation, decision ownership, and proof reruns exist before the crisis. Recovery includes updating the security case, not only restoring service.

## 5. What belongs in an incident timeline?

Observed event, source, timestamp and clock basis, confidence, actor/action, decision, owner, and links to preserved evidence; distinguish inference.

**Capstone check.** Contain the smallest affected boundary first; the exercise must show why shutting down every tenant would add avoidable impact.

The important nuance is: Build the timeline from immutable or independently preserved observations: credential issuance and revocation records, authorization decisions, artifact-access events, webhook deliveries, configuration revisions, deployment identifiers, and database facts. Record event time, observation time, source, confidence, and who made the statement. Do not rewrite uncertain early entries; append corrections.

## 6. Why not log the leaked secret as evidence?

It increases exposure; preserve secure references, hashes where useful, source location, and controlled access instead.

**Capstone check.** Exercise webhook-key overlap and retirement; deliveries signed by the compromised key must fail after the bounded transition.

Under concurrency or failure, the distinction becomes: The post-incident review updates threats, assumptions, requirements, tests, runbooks, ownership, and deadlines. Avoid a generic action such as “be more careful.” Prefer a falsifiable change: “unknown webhook key IDs are rejected and the overlap schedule is tested at both boundary timestamps.”

## 7. What proves containment?

The compromised credential/key no longer succeeds, replacement paths function, malicious behavior stops or is bounded, and relevant proofs pass.

**Capstone check.** Hash and preserve evidence before cleanup; the timeline distinguishes observed fact, inference, and decision.

The design remains honest only if: Preserve evidence before destructive remediation. Snapshot relevant configuration and dependency manifests, hash exported logs, record queries and commands, and restrict access. Do not copy live secrets or personal data into a broadly shared incident document. The evidence package should be sufficient to reproduce decisions without becoming a new breach.

## 8. What proves recovery?

Trusted service behavior, data integrity, compatible clients, updated monitoring, and no recurrence under the defined observation window.

**Capstone check.** Ship a compatible security release and rerun Courses 1–3 proofs; emergency pressure does not justify an undocumented contract break.

The consumer-facing consequence is: Use an incident state machine with explicit legal transitions. “Contained” means the active attack path is blocked and the scope is sufficiently understood to proceed; it does not mean every root cause is fixed. “Recovered” means normal service has resumed under verified controls and monitoring. “Closed” requires completed follow-up ownership, not fatigue.

## 9. How should a vulnerable dependency be handled?

Establish affected version and reachability, apply/update or compensate, rebuild reproducibly, rerun security proof, and record disposition/provenance.

**Capstone check.** Close only after revocation/rotation, attack regression, durable-state review, and monitoring evidence agree.

The operational consequence is: Implement incident state transitions, revocation entries, key-version activation/retirement, evidence records, and a deterministic drill runner. The runner must not mutate predecessor history or include secret values in its report. Generate a compatible release note and rerun requirement-linked tests.

## 10. Why update the threat model?

Observed attacker capability or control failure changes assumptions, priority, and required evidence.

**Capstone check.** Update the threat, requirement, control, and regression that failed; a post-incident narrative without changed engineering evidence is incomplete.

The strongest engineering interpretation is: The ten module results now satisfy this course promise: A threat-driven security profile with hardened edge, identity, authorization, input, outbound, secret, abuse, supply-chain, and incident controls. The next course is API Reliability and Observability Engineering ; it consumes the outgoing handoff rather than reinterpreting completed work.

## 11. Trace security incident containment and recovery in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/incident.py` and `capstone/tracks/typescript-fastify/src/security/incident.ts`. The required invariant is that revocation, key overlap, evidence preservation, compatible release, verification, and threat-model revision form one controlled timeline.

The defect-oriented view is: A security incident is not complete when a patch merges. Response must detect, triage, contain, eradicate, recover, verify, communicate, and feed the result back into the security case. The order can overlap, but each action needs an owner and evidence.

## 12. Compare security incident containment and recovery across Python and TypeScript

Both tracks must preserve this invariant: revocation, key overlap, evidence preservation, compatible release, verification, and threat-model revision form one controlled timeline. The intentional difference is that state-machine syntax differs; illegal transitions and premature key retirement must fail in both tracks.

Across the Python and TypeScript tracks, the invariant is: Mirror the incident state machine with exhaustive status handling. Use immutable timeline records and verify sequence/causality separately from wall-clock ordering. The comparison track reviews whether Node process/config reload semantics could leave stale keys or revocation state.
