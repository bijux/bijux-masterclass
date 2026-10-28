# Reference Answers — Module 10: Security Operations and Incident Response

Read after attempting all twelve Security Operations and Incident Response exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. What is the first goal of triage?

**Answer.** Establish credible scope, current harm, affected assets/identities, and immediate containment needs without destroying evidence.

**Capstone check.** Use `capstone/incident/scenario.yaml` to identify the compromised secret before rotating unrelated credentials; preserve a time-stamped action record.

## 2. When revoke a token `jti` versus a subject?

**Answer.** Revoke the specific token when compromise is isolated; broaden to subject/session/client when evidence suggests wider credential control.

**Capstone check.** Revoke the suspected token identifier and verify subsequent API access fails while unrelated principals remain available.

## 3. How does webhook key containment work?

**Answer.** Mark the compromised version non-signing, introduce a new active version, update receivers, keep only justified overlap, block/review replay IDs, then retire old verification.

**Capstone check.** Run the cross-tenant artifact probe and preserve request, policy decision, durable access facts, and redacted audit evidence.

## 4. Why preserve compatibility during a security release?

**Answer.** Breaking clients can worsen outage and drive unsafe workarounds; security fixes should alter only what is necessary and provide migration evidence.

**Capstone check.** Record the vulnerable component, reachable path, temporary mitigation, fixed version, and rebuild evidence; scanner output alone does not close the incident.

## 5. What belongs in an incident timeline?

**Answer.** Observed event, source, timestamp and clock basis, confidence, actor/action, decision, owner, and links to preserved evidence; distinguish inference.

**Capstone check.** Contain the smallest affected boundary first; the exercise must show why shutting down every tenant would add avoidable impact.

## 6. Why not log the leaked secret as evidence?

**Answer.** It increases exposure; preserve secure references, hashes where useful, source location, and controlled access instead.

**Capstone check.** Exercise webhook-key overlap and retirement; deliveries signed by the compromised key must fail after the bounded transition.

## 7. What proves containment?

**Answer.** The compromised credential/key no longer succeeds, replacement paths function, malicious behavior stops or is bounded, and relevant proofs pass.

**Capstone check.** Hash and preserve evidence before cleanup; the timeline distinguishes observed fact, inference, and decision.

## 8. What proves recovery?

**Answer.** Trusted service behavior, data integrity, compatible clients, updated monitoring, and no recurrence under the defined observation window.

**Capstone check.** Ship a compatible security release and rerun Courses 1–3 proofs; emergency pressure does not justify an undocumented contract break.

## 9. How should a vulnerable dependency be handled?

**Answer.** Establish affected version and reachability, apply/update or compensate, rebuild reproducibly, rerun security proof, and record disposition/provenance.

**Capstone check.** Close only after revocation/rotation, attack regression, durable-state review, and monitoring evidence agree.

## 10. Why update the threat model?

**Answer.** Observed attacker capability or control failure changes assumptions, priority, and required evidence.

**Capstone check.** Update the threat, requirement, control, and regression that failed; a post-incident narrative without changed engineering evidence is incomplete.

## 11. Trace security incident containment and recovery in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/incident.py` and `capstone/tracks/typescript-fastify/src/security/incident.ts`. The required invariant is that revocation, key overlap, evidence preservation, compatible release, verification, and threat-model revision form one controlled timeline.

## 12. Compare security incident containment and recovery across Python and TypeScript

Both tracks must preserve this invariant: revocation, key overlap, evidence preservation, compatible release, verification, and threat-model revision form one controlled timeline. The intentional difference is that state-machine syntax differs; illegal transitions and premature key retirement must fail in both tracks.
