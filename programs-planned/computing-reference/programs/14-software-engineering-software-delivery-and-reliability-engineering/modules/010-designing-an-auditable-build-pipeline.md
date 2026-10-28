---
module_id: SDRE-010
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 10
title: Designing an Auditable Build Pipeline
status: complete
last_verified: 2026-09-06
---

# Designing an Auditable Build Pipeline

## One-Page Review

### Governing question

How should a build pipeline transform an admitted source revision into one immutable release candidate while producing enough trustworthy evidence to reconstruct every consequential decision?

### Essential definitions

- a **pipeline** is a governed sequence of transformations and decisions, not merely a script runner;
- a **candidate** is an immutable artifact digest plus its bound evidence;
- a **stage** groups work with one durable responsibility; a **transition** changes pipeline state only when its guard passes;
- a **gate** evaluates explicit evidence against a versioned policy;
- an **event** records an attempted or completed action with actor, subject, time, inputs, outcome, and causation;
- an **evidence graph** connects source, dependencies, build, tests, provenance, SBOM, signatures, approvals, publication, and release through digests and identities;
- **auditability** is the ability to reconstruct who or what did which action, to which exact subject, under which policy and inputs, with what result and reason;
- **replay safety** means retrying an already accepted operation cannot silently create a different release fact;
- **separation of duty** prevents one authority from unilaterally producing and approving a high-risk release;
- **break glass** is a narrow, authenticated, time-bounded exception whose use and later review remain visible.

### Central model, mechanism, or theorem

Model a candidate as $c=(d_s,d_a,E,v)$: source digest, artifact digest, immutable evidence set, and pipeline-policy version. A transition from state $q_i$ to $q_j$ is accepted only when

$$
Allowed(q_i,q_j,v)\land SubjectBound(E,d_a)\land Guards(E,v)\land Fresh(E,v).
$$

The useful release path is `proposed → admitted → resolved → built → verified → published → released`. Every accepted transition appends a decision event; no transition rewrites prior evidence.

### Critical invariants

- resolve mutable source and dependencies to immutable identifiers before building;
- build once, then promote the same artifact digest;
- make pipeline and policy revisions identifiable inputs;
- isolate trusted control-plane decisions from tenant-controlled workload steps;
- bind evidence and approvals to exact artifact, source, parameters, and policy;
- sign only after finalization and outside an untrusted workload;
- make gate failures closed for release while retaining safe diagnostic evidence;
- use idempotency keys and compare prior subjects before accepting retries;
- preserve append-only causation, including failed and exceptional decisions;
- redact secrets without destroying identity, subject, outcome, or reason fields;
- retain evidence according to release support, incident, legal, and privacy needs;
- test recovery and break-glass controls before an emergency.

### Common failures

Common failures include rebuilding per environment, approving a tag rather than a digest, letting tests mutate the artifact, trusting job success without evidence, allowing workloads to sign their own claims, overwriting logs on retry, recording a manual approval only in chat, accepting stale policy evaluations, treating timestamps as causal order, leaking secrets in logs, deleting failed evidence, granting broad break-glass access, and retaining data forever without purpose or access control.

### Compact example

A pipeline admits commit `s1`, resolves lockfile digest `l1`, builds artifact `a1`, records tests and SBOM against `a1`, obtains provenance from the trusted builder, and publishes `a1`. An authenticated approver accepts candidate `a1` under policy `p7`; production promotes `a1` without rebuilding. An audit can traverse `release → approval → a1 → build → {s1,l1}`. A retry carrying the same operation key and `a1` is a no-op; the same key with `a2` is rejected as a conflict.

### Connections

[SDRE-001](001-from-source-change-to-deployable-artifact.md) introduced the source-to-artifact chain, and [SDRE-002](002-dependency-resolution-and-locking.md) made resolved inputs explicit. [SDRE-007](007-build-metadata-and-provenance.md), [SDRE-008](008-generating-and-verifying-software-bills-of-materials.md), and [SDRE-009](009-artifact-signing-and-verification.md) supply evidence mechanisms. [SDRE-011](../ROADMAP.md) next establishes continuous integration as a working practice.

## Governing Question

A build that exits successfully answers a narrow question: a process returned zero in some environment. A release decision needs more. Which source revision and dependencies entered? Which pipeline and policy applied? Which identity performed each trusted action? Did tests examine the exact bytes later released? Were exceptions used? Can an investigator reproduce the decision without trusting a mutable dashboard?

An auditable build pipeline makes those questions properties of its architecture. It transforms immutable subjects through guarded states, emits authenticated and digest-bound evidence, separates production from authorization, and retains an append-only decision trail. Auditability does not mean logging everything. It means retaining the minimum sufficient, trustworthy facts and their causal relationships.

## Why This Matters

Delivery pipelines are part of the software supply chain and part of the security boundary. A compromised source repository, dependency resolver, runner, policy file, artifact store, approver account, or orchestration service can change what reaches users. NIST SP 800-204D describes integrating software-supply-chain security measures into CI/CD pipelines and emphasizes artifacts, attestations, provenance, repositories, and SBOMs as connected controls [1].

SLSA 1.2 treats the build platform as the transitive closure of systems, people, and organizations able to influence a build, and requires useful provenance to be distributed and verified against expectations [2] [3]. The in-toto specification similarly models authorized supply-chain steps and signed link metadata connecting materials to products [4]. These sources support a common conclusion: evidence must be generated at the boundary capable of observing the fact, then independently checked before use.

Auditability also improves operations. A coherent event chain answers why a gate rejected a candidate, which releases used a vulnerable input, whether an emergency exception escaped its time limit, and whether a retry duplicated a side effect. It reduces the temptation to reconstruct incidents from screenshots, mutable job names, and partial service logs.

## Prerequisites and Retrieval

Retrieve source revision, content digest, immutable identifier, dependency lock, build environment, artifact, repository, stage, job, dependency graph, gate, policy, principal, workload identity, authentication, authorization, attestation, provenance, SBOM, signature, trust anchor, timestamp, event, causation, idempotency, retry, retention, redaction, least privilege, separation of duty, failure domain, recovery point, and recovery time.

From SDRE-001 through SDRE-009 retrieve the delivery value stream, directed acyclic job graph, clean source capture, dependency locking, reproducible-build limits, immutable artifacts, release identity, provenance, SBOMs, and signature verification. This module integrates those mechanisms into one pipeline design. Security Engineering owns deep credential and cryptographic analysis; Platform Engineering owns multi-tenant execution infrastructure; Software Architecture owns system-wide boundary design.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish execution success, evidentiary sufficiency, and release authorization;
2. model a build pipeline as guarded state transitions over immutable subjects;
3. design a digest-connected evidence graph from source to release;
4. place evidence generation at trustworthy observation boundaries;
5. isolate tenant workloads from trusted signing, policy, and publication controls;
6. make retries idempotent and conflicting replays visible;
7. bind manual approvals and exceptions to exact candidates and policies;
8. retain useful events while controlling secrets and personal data;
9. reconstruct an incident despite partial service failure or clock uncertainty;
10. review a pipeline for bypasses, confused authority, and unverifiable transitions.

## Core Exposition

**Begin with subjects and states.** A pipeline should not pass an ambiguous thing called “the build” between jobs. Define stable subjects: source digest, dependency-set digest, build definition digest, artifact digest, evidence digests, and release identity. A mutable branch or tag may trigger work, but admission resolves it to an immutable revision before any release-relevant transition.

Represent the lifecycle explicitly. `Proposed` means a request exists. `Admitted` means identity, source, and allowed parameters passed admission policy. `Resolved` means dependency and tool inputs have immutable coordinates. `Built` means a trusted builder produced artifact digest and provenance. `Verified` means required tests and evidence checks passed for that digest. `Published` means the digest is stored immutably. `Released` means an authorized policy decision promotes that same digest to a release identity.

Not every real pipeline needs these exact names, but every consequential state must have a defined meaning, allowed predecessor, required evidence, and accountable owner. A visual green box without a specified transition contract is user-interface state, not a guarantee.

**Design an evidence graph, not a folder of logs.** Let nodes represent immutable subjects and evidence objects. Let edges express typed relationships such as `built-from`, `tested`, `describes`, `signed-by`, `approved-under`, `published-as`, and `released-as`. Every edge should be supported by an authenticated record and exact digests. An SBOM that names `a1` and a test report for mutable tag `latest` are not equivalent evidence.

An investigator should be able to walk backward from a release identity to its artifact digest, approval, policy version, verification results, provenance, source, dependencies, builder identity, and pipeline definition. Forward traversal should answer which candidates and releases depend on an affected source or package. Store indexes for navigation, but treat signed or digest-addressed evidence as the durable facts.

**Put observation at the right boundary.** A tenant job can honestly report what it attempted, but it cannot independently attest that the platform isolated it or captured all inputs. A trusted build control plane can observe the admitted request, provisioned environment, resolved parameters, subject digests, workload outcome, and collected outputs. It should generate provenance without allowing the tenant to choose protected fields.

The same rule governs gates. A test process may emit results; a gate service decides whether the authenticated result, test identity, artifact digest, policy version, and freshness satisfy release policy. Signing belongs after artifact finalization and policy checks, under a service identity scoped to the artifact namespace. Putting the release key inside the build container collapses producer and authorizer into one compromised boundary.

**Make the pipeline definition an input.** Pipeline code, reusable actions, runner images, policy bundles, and verifier versions influence the result. Pin or digest them where practical, review their changes, and record the effective versions. A source commit built under policy `p6` is not the same decision as the same commit built under `p7`. Do not let a dashboard silently reevaluate old evidence under today's rules and present it as the original decision.

**Use conjunctive, fail-closed gates.** A gate is a predicate over explicit facts. For example, publication may require artifact digest equality, successful required tests, accepted provenance, accepted SBOM binding, approved builder identity, and current policy. Missing or unparsable evidence is a failed decision, not implicit success. Unknown critical fields should fail closed.

Fail closed does not mean destroy diagnostics. Record the candidate, gate, policy, missing fact, safe error category, and causal event. Quarantine outputs if investigation needs them, but deny publication or release. Keep the diagnostic channel from leaking credentials or attacker-controlled terminal escapes.

**Build once and promote.** Rebuilding for staging and production creates two artifacts with only an assumed relationship. A correct promotion path verifies and moves the exact immutable digest through environment-specific policy. Configuration that legitimately varies by environment should be supplied and governed at deployment, not baked by an undocumented rebuild. If platform constraints require rebuilding, model it as a new candidate with new provenance and verification, never as promotion of the earlier bytes.

**Treat retries as protocol operations.** Distributed orchestrators retry after timeouts, worker loss, and ambiguous acknowledgments. Assign an idempotency key to each side-effecting operation and bind it to its subject and parameters. If a retry repeats the same key and same subject, return the durable prior result. If it repeats the key with a different digest or policy, reject and alert. Do not infer uniqueness from a job name or timestamp.

At-least-once event delivery can coexist with exactly-once logical decisions when consumers deduplicate by stable event identifier and verify subject equality. There is no general exactly-once execution guarantee across arbitrary failures. The narrower invariant is that duplicate execution cannot silently create two contradictory publication or release facts.

**Record causal events.** Each event needs a stable identifier, event type and schema version, authenticated actor, exact subject digests, pipeline and policy versions, attempt identifier, outcome, reason category, parent or correlation identifiers, and trustworthy time evidence where available. Record both the decision time and the time claimed by an upstream producer if they differ.

Wall clocks do not establish causal order across machines. Use explicit parent relationships and local sequence numbers for causality; use synchronized timestamps for search and bounded-time policy only with stated uncertainty. Preserve original events and append corrections. Mutating an old “failed” record into “passed” erases the very fact an audit needs.

**Govern manual decisions.** Manual approval must be an authenticated structured event, not a chat message or screenshot. Bind actor, role, candidate digest, release scope, policy version, decision, reason, and expiry. Reauthentication and two-person approval may be appropriate for high-risk production. An approval for `a1` must not float to later `a2` merely because both use version label `2.4.0`.

Break-glass design is part of the normal system. Define which gate can be bypassed, who can request and approve it, maximum duration, affected scope, mandatory rationale, monitoring, and retrospective review. Never implement “admin can skip everything.” An exception should add evidence and visibility, not delete the failed gate from history.

**Balance retention, privacy, and secrecy.** Retain enough evidence for the supported lifetime of released software, vulnerability response, contractual obligations, and incident investigation. Longer is not automatically better: logs can contain personal data, repository paths, dependency URLs, proprietary source fragments, or secrets. Classify fields, minimize collection, encrypt at rest and in transit, restrict access, log access, define deletion holds, and test restoration.

Redaction must happen before broad distribution. Replace secrets with stable non-secret identifiers where correlation is necessary. Do not redact the artifact digest, actor identity class, policy version, outcome, or reason so aggressively that the decision becomes irreconstructable. NIST SSDF 1.1 includes protecting software and retaining release information as part of secure development practice [5].

**Design for partial failure and recovery.** If the event store is unavailable, a high-assurance release transition should stop rather than create an unrecorded fact. If optional telemetry is unavailable, the pipeline may continue only under an explicit policy that distinguishes telemetry from required evidence. Buffer signed events locally with bounded storage and replay controls when appropriate.

Back up trust roots, policies, evidence indexes, and immutable evidence objects. Test restoration and verify digests afterward. A backup that restores a dashboard but loses identity mappings or policy versions cannot reconstruct old decisions. Define how investigators obtain evidence if the normal control plane is itself suspect.

**Measure the design honestly.** Useful measures include percentage of releases whose evidence graph is complete, median time to reconstruct a release, rate of denied conflicting retries, age of unresolved exceptions, and restore-test success. “Number of log lines” and “percentage of green builds” do not measure auditability. Sample completed releases and independently traverse their evidence chains.

## Definitions and Notation

Let:

- $S=\{proposed,admitted,resolved,built,verified,published,released,rejected\}$ be pipeline states;
- $c=(d_s,d_a,E,v)$ be a candidate with source digest $d_s$, artifact digest $d_a$, evidence set $E$, and pipeline-policy version $v$;
- $T\subseteq S\times S$ be allowed transitions;
- $g_{ij}(c)$ be the guard for transition $(q_i,q_j)$;
- $e=(id,type,actor,subject,parent,v,outcome,time)$ be a decision event;
- $K(op)$ be the idempotency key for side-effecting operation $op$.

A transition is acceptable when

$$
Transition(c,q_i,q_j)=((q_i,q_j)\in T)\land g_{ij}(c)\land Append(e).
$$

Here `Append` means the decision event becomes durably visible without overwriting earlier events. It is a system requirement, not a mathematical guarantee supplied by notation.

Evidence completeness for required relation set $R_v$ is

$$
Complete(c,v)=\forall r\in R_v,\ \exists e\in E:\ Supports(e,r,c,v).
$$

Completeness says every required relationship has evidence. It does not say the evidence producer was honest; identity, trust, and authorization checks remain necessary.

## Mechanisms, Invariants, or Proof Structure

**State monotonicity.** Successful progression adds facts and never changes the candidate artifact digest. If verification discovers a mismatch, the candidate enters `rejected`; producing new bytes creates a new candidate. Therefore `released(c)` implies the released bytes equal the artifact digest fixed at `built(c)`, assuming every guard recomputes or securely carries the digest.

**Evidence closure.** For every accepted transition, the pipeline records its guard inputs, effective policy, actor, subject, outcome, and parent decision. Induction over the transition path then yields a backward chain from `released` to `proposed`. The claim depends on append durability and unique parent references; timestamps alone are insufficient.

**Idempotency invariant.** Maintain a durable mapping $M[K]=(subject,parameters,result)$. On retry, return `result` only when both subject and parameters match. Reject otherwise. This prevents an ambiguous timeout from turning the same logical release request into authorization for different bytes.

**Executable state-machine model.** This model evaluates guards and retry conflicts. It does not build, sign, publish, authenticate identities, or provide a durable event store.

<!-- bijux-verify: {"id":"audit-pipeline-state-machine","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"happy_path=released\nwrong_digest=rejected\nmissing_provenance=rejected\nstale_policy=rejected\nreplay_idempotent=True\nconflicting_replay=rejected\nskipped_gate=rejected\naudit_reconstructable=True\n","stderr":""}} -->
```python
required = {
    "admitted": {"source", "identity"},
    "resolved": {"dependencies"},
    "built": {"source", "artifact", "provenance"},
    "verified": {"tests", "sbom"},
    "published": {"signature"},
    "released": {"approval"},
}
order = ["admitted", "resolved", "built", "verified", "published", "released"]

def run(candidate):
    events = [{"state": "proposed", "parent": None}]
    if candidate["policy"] != "p7":
        return "rejected", events
    if candidate["artifact"] != candidate["evidence_subject"]:
        return "rejected", events
    for state in order:
        if not required[state] <= candidate["evidence"]:
            return "rejected", events
        events.append({"state": state, "parent": events[-1]["state"]})
    return "released", events

base = {
    "artifact": "sha256:a1",
    "evidence_subject": "sha256:a1",
    "policy": "p7",
    "evidence": {"source", "identity", "dependencies", "artifact", "provenance", "tests", "sbom", "signature", "approval"},
}

status, trail = run(base)
print(f"happy_path={status}")
print(f"wrong_digest={run(base | {'evidence_subject': 'sha256:a2'})[0]}")
print(f"missing_provenance={run(base | {'evidence': base['evidence'] - {'provenance'}})[0]}")
print(f"stale_policy={run(base | {'policy': 'p6'})[0]}")

operations = {"release-42": ("sha256:a1", "released")}
print(f"replay_idempotent={operations['release-42'] == ('sha256:a1', 'released')}")
conflict = operations["release-42"][0] != "sha256:a2"
print(f"conflicting_replay={'rejected' if conflict else 'accepted'}")
print(f"skipped_gate={run(base | {'evidence': base['evidence'] - {'tests'}})[0]}")
expected = ["proposed", "admitted", "resolved", "built", "verified", "published", "released"]
print(f"audit_reconstructable={status == 'released' and [event['state'] for event in trail] == expected}")
```

## Alternatives and Trade-Offs

**Central orchestration versus event choreography.** A central orchestrator makes transition order and policy visible but is a high-value control-plane dependency. Event choreography scales ownership and fault isolation but makes global causality and duplicate handling harder. Both require stable subjects, authenticated events, and explicit state semantics.

**One pipeline versus composable attestations.** One monolithic pipeline is easy to visualize but couples teams and infrastructure. Independently operated steps can publish attestations into an evidence graph, enabling separation and reuse, but require common schemas, identity policy, and verification. in-toto layouts demonstrate how authorized steps and material/product rules can connect such evidence [4].

**Synchronous gates versus deferred monitoring.** Synchronous verification blocks known-bad candidates before use but adds latency and availability dependencies. Deferred monitors detect drift and newly understood risk but cannot undo exposure. Use blocking gates for required preconditions and monitoring for continuously changing knowledge, with explicit response paths.

**Full event capture versus selective evidence.** Capturing every command and byte may help diagnosis but increases cost, secrecy, and privacy risk. Selective structured evidence is easier to govern but can omit unexpected forensic clues. Separate required decision evidence from access-controlled diagnostic telemetry and set retention independently.

**Hosted versus self-managed control planes.** Hosted systems reduce operational burden and can provide hardened isolation; they add provider, identity, availability, and evidence-export dependencies. Self-managed systems offer control but make patching, isolation, key custody, and audit-store integrity the operator's responsibility.

**Strict stop versus degraded operation.** Stopping on required-evidence failure preserves the release invariant. Continuing may protect availability during telemetry outages but risks unaudited release. Classify dependencies beforehand: required evidence fails closed; optional observability may degrade under a recorded, bounded policy.

## Failure Modes and Misconceptions

- **“Green means auditable.”** A status lacks subjects, policy, and reasons.
- **“More logs create stronger evidence.”** Volume does not create authenticity or binding.
- **“The branch identifies the source.”** Resolve it to an immutable revision.
- **“Tests ran on this version.”** Bind results to the exact artifact or source digest.
- **“Promotion can rebuild.”** Rebuilding creates a different candidate.
- **“The workload can attest to platform isolation.”** It cannot independently observe that boundary.
- **“A signature repairs weak evidence.”** It authenticates claims; it does not make them complete or true.
- **“The latest policy explains an old release.”** Record the effective historical version.
- **“Retries are harmless.”** Side effects need subject-bound idempotency.
- **“Timestamps determine order.”** Clock skew and delay break causal inference.
- **“Manual approval is in chat.”** Chat is not a structured digest-bound authorization record.
- **“Break glass should be invisible to reduce noise.”** Exceptions need greater visibility.
- **“Failed builds need no retention.”** They can reveal attacks, recurring defects, and bypass attempts.
- **“Keep every log forever.”** Unbounded retention creates security, privacy, and cost risks.
- **“Redact the whole record.”** Preserve non-secret decision facts needed for reconstruction.
- **“The dashboard is the source of truth.”** Durable evidence must survive interface and vendor changes.

## Worked Examples

### Example 1

**Situation.** A branch `main` triggers a release while a new commit arrives during the build. Which source is the subject?

**Reasoning.** Admission resolves `main` to commit digest `s17` and records both the trigger name and immutable revision. Checkout verifies `s17`; provenance names `s17`. The later branch movement does not alter the candidate. If a job checks out `main` again, its subject may differ and the pipeline must reject the mixed run.

**Conclusion.** Mutable references initiate work; immutable revisions define auditable source identity.

### Example 2

**Situation.** Tests pass on artifact `a1`, but a packaging job adds a file and produces `a2` before publication.

**Reasoning.** The test evidence binds `a1`, so it cannot satisfy the verification guard for `a2`. Either package before tests or treat packaging as a new build transition and test `a2`. Copying the old green status would break subject binding.

**Conclusion.** Any byte-changing step creates a new subject requiring its own applicable evidence.

### Example 3

**Situation.** The publication request times out after the repository stores `a1`; the orchestrator retries.

**Reasoning.** Operation key `publish-82` maps durably to subject `a1` and repository result `r44`. A retry with the same parameters returns `r44` without republishing. A retry with `a2` conflicts and alerts because one logical operation cannot name two subjects.

**Conclusion.** Idempotency requires a durable key-to-subject mapping, not optimistic retry behavior.

### Example 4

**Situation.** Provenance is missing because the trusted builder's evidence exporter failed, although compilation succeeded.

**Reasoning.** The `built` or `verified` guard requires provenance. The candidate is quarantined and marked rejected with reason `required-evidence-missing`. Safe diagnostics and output digests remain available for investigation; publication is denied. A later evidence repair must be authenticated and causally linked, not silently injected.

**Conclusion.** Fail closed for release while preserving a visible diagnostic trail.

### Example 5

**Situation.** An approver accepts version label `2.4.0`; the tag is later moved from `a1` to `a2`.

**Reasoning.** A valid approval record includes artifact digest `a1`, release scope, policy `p7`, actor, and expiry. It authorizes only `a1`. Publishing `a2` under the same label requires a new decision and may violate immutable release-identity policy.

**Conclusion.** Human decisions must bind immutable candidates, not presentation labels alone.

### Example 6

**Situation.** Two services report events at 10:00:01 and 09:59:59. Did the second happen first?

**Reasoning.** Their clocks may differ. The provenance event names the admission event as parent, and the verification event names provenance as an input. Those causal links establish order despite timestamp inversion. Timestamps remain useful for time windows when uncertainty is bounded.

**Conclusion.** Use explicit causation for order and clocks for qualified temporal evidence.

### Example 7

**Situation.** A high-severity outage requires deployment before a slow integration suite finishes.

**Reasoning.** A predefined exception permits bypass of only that suite for one digest and environment, requires an incident commander plus independent approver, expires in 60 minutes, and creates an alert and retrospective-review obligation. Signature, provenance, basic safety checks, and immutable promotion remain required.

**Conclusion.** Break glass narrows a named control under stronger evidence; it is not universal administrator bypass.

### Example 8

**Situation.** A command prints an access token into logs later attached to the release record.

**Reasoning.** The token must be revoked, access to affected logs constrained, and exposure investigated. Future capture redacts known secret formats before distribution and prevents raw environment dumps. The event retains non-secret workload identity, command identity, subject digest, outcome, and reason.

**Conclusion.** Evidence systems need data minimization and secret handling without erasing decision facts.

### Example 9

**Situation.** An audit store backup restores events but not policy bundle `p6`, used for last year's supported release.

**Reasoning.** The events prove that `p6` was named but cannot show which guards it contained. The evidence closure is incomplete. Recovery must include immutable policy definitions, trust-root history, schemas, and identity mappings, with restore tests that traverse old releases.

**Conclusion.** A recoverable audit trail includes decision context, not event rows alone.

### Example 10

**Situation.** A team claims a pipeline is auditable because it retains 90 days of console logs.

**Reasoning.** Sample a release and attempt backward traversal. The logs name a mutable job, omit the artifact digest, contain no effective policy version, and record approval only as “clicked by admin.” They cannot establish subject continuity or authority. A structured evidence graph would retain far less text yet answer the audit questions.

**Conclusion.** Auditability is tested by reconstruction of exact decisions, not by retention volume.

## Cross-Program Connections

- Systems Engineering owns system boundaries, hazards, assurance cases, and whole-system traceability; this module applies traceability to delivery transitions.
- Software Architecture owns component and trust-boundary structure; pipeline control plane, workload plane, repositories, identity services, and evidence store are architectural components.
- Software Engineering Patterns owns reusable design forms; state machines, append-only logs, idempotent receivers, and policy decision points are applied here under delivery constraints.
- Testing & Quality Engineering owns test design and evidence interpretation; this module binds test results to candidates and release gates.
- Security Engineering owns credential threats, least privilege, cryptographic choices, and incident response; this module places those controls in a delivery chain.
- Platform Engineering owns execution isolation, workload identity, runner lifecycle, and shared pipeline services; this module specifies the evidence and authority those services must expose.
- API & Service Engineering owns reliable service contracts; idempotency, authenticated events, schemas, and failure semantics are API concerns inside a distributed pipeline.

## References

1. National Institute of Standards and Technology, [NIST SP 800-204D: Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines](https://doi.org/10.6028/NIST.SP.800-204D), final, February 2024. Retrieved 2026-09-06.
2. SLSA, [SLSA Specification 1.2](https://slsa.dev/spec/v1.2/), approved specification, accessed 2026-09-06.
3. SLSA, [Build: Requirements for Producing Artifacts](https://slsa.dev/spec/v1.2/build-requirements) and [Build: Verifying Artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts), version 1.2, accessed 2026-09-06.
4. in-toto Project, [in-toto Specification](https://github.com/in-toto/docs/blob/master/in-toto-spec.md), layout, link, material, product, and inspection model, accessed 2026-09-06.
5. National Institute of Standards and Technology, [NIST SP 800-218: Secure Software Development Framework (SSDF) Version 1.1](https://doi.org/10.6028/NIST.SP.800-218), final, February 2022. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Distinguish execution success, evidence completeness, and release authorization. Give one fact each establishes and one fact it does not.

### Exercise 2

A candidate passes states `proposed → admitted → built → published → released`. Its record contains source `s1`, artifact `a1`, test report for `a1`, signature for `a1`, and approval for tag `stable`, but no dependency resolution, provenance, SBOM, or policy version. Trace the missing or invalid transitions.

### Exercise 3

A publisher receives two requests with idempotency key `deploy-7`: first `(a1, production, p7)`, then `(a2, production, p7)`. Diagnose the correct behavior and specify the minimum durable record.

### Exercise 4

Design a manual production gate for a high-risk service. Include subject binding, authority, separation of duty, expiry, failure behavior, and break-glass governance.

### Exercise 5

A regulated product must support releases for ten years, while privacy policy permits ordinary job telemetry for only 30 days. Design an evidence and recovery strategy that supports later incident reconstruction without retaining every console log.

## Answers to the Exercises

### Answer 1

Execution success establishes that a named process reported its success condition in an observed environment; it does not establish that it used authorized inputs. Evidence completeness establishes that every relation required by a named policy has a corresponding record; it does not establish that every producer was trustworthy or honest. Release authorization establishes that authenticated authorities accepted an exact candidate under a policy and scope; it does not establish that the artifact is defect-free. A sound release requires all three judgments plus subject, identity, and trust validation.

### Answer 2

`Admitted → resolved` is absent because immutable dependency and tool inputs were never recorded. `Resolved → built` lacks trusted provenance connecting `s1` and resolved inputs to `a1`. `Built → verified` lacks required SBOM evidence even though one test report exists. `Verified → published` may have signature evidence but cannot skip the failed verification guard. `Published → released` is invalid because approval binds mutable tag `stable`, not `a1`, and no effective policy version exists. The candidate must be rejected or reprocessed with new authenticated evidence; the missing records must not be fabricated retrospectively.

### Answer 3

The first accepted request durably maps `deploy-7` to the tuple `(a1, production, p7)` and its result. An exact retry returns that result. The second request is a conflicting replay and must be rejected and alerted because it changes the subject under the same logical operation. The record needs the idempotency key, exact artifact digest, destination scope, policy version, authenticated requester, outcome, result identifier, and creation event. A timestamp or job name alone is insufficient.

### Answer 4

A model gate accepts only a digest-addressed candidate with complete required evidence. The requester and approvers authenticate with role-constrained identities; two distinct authorized principals approve, and neither is the producing workload identity. The record binds digest, release scope, policy, decision, rationale, and expiry. Missing or expired approval fails closed and records a safe reason. Break glass can bypass only named non-fundamental checks for one digest and environment, requires separate request and approval, expires quickly, alerts responders, and creates a mandatory retrospective review. Acceptable alternatives may vary thresholds by risk, but evaluation should require immutable subject binding, distinct authority, bounded scope, visible failure, and governed exception use.

### Answer 5

Retain a compact immutable evidence graph for the supported release lifetime: source and artifact digests, resolved-input inventory, build and policy definitions, provenance, SBOM, verification summaries, signatures, trust-root history, approvals, publication and release events, identities, schemas, and typed causal links. Keep verbose console telemetry in a separately controlled 30-day store after secret filtering. Apply legal holds narrowly. Encrypt evidence, restrict and audit access, preserve integrity proofs, and document field-level privacy purpose. Back up evidence objects, indexes, policies, identity mappings, and trust roots; regularly restore a sample old release and traverse it in both directions. This supports reconstruction without treating raw logs as the durable audit record.
