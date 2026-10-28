---
module_id: SDRE-021
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 21
title: Continuous Delivery Versus Continuous Deployment
status: complete
last_verified: 2026-09-06
---

# Continuous Delivery Versus Continuous Deployment

## One-Page Review

### Governing question

What guarantees distinguish continuous delivery from continuous deployment, and where should technical readiness, deployment authorization, and user-facing release remain separate?

### Essential definitions

- **continuous integration** keeps changes frequently integrated and verified in a shared codebase;
- **continuous delivery** keeps the product in a deployable state and makes deployment of an authorized version routine and on demand;
- **continuous deployment** automatically deploys every qualifying change to production without a separate routine human release decision;
- a **deployment** changes software or configuration running in an environment;
- a **release** makes behavior available to intended users or consumers;
- a **deployment pipeline** transforms and verifies an exact candidate through ordered evidence stages;
- a **release candidate** is an artifact proposed for production, not an artifact guaranteed correct;
- **readiness** means the exact candidate satisfies currently required technical and policy evidence;
- an **approval** authorizes a bound subject and action; it is not evidence that the subject works;
- a **manual gate** requires human action before progress; an **automated gate** evaluates machine-readable policy;
- **progressive delivery** limits exposure while observing a production change before expansion;
- a **feature flag** separates code deployment from activation of behavior;
- **rollback** restores an earlier known artifact or state; **roll forward** deploys a correcting version;
- a **release train** deploys or releases accumulated changes on a schedule.

### Central model, mechanism, or theorem

For artifact $a$ at time $t$, define readiness

$$
Ready(a,t)=Identity(a)\land Evidence(a,t)\land Policy(a,t)\land Recoverable(a,t).
$$

Continuous delivery maintains the capability to deploy a ready artifact on demand. A deployment policy $D(a,t,c)$ then decides whether to deploy, using readiness plus context $c$ such as business timing, change window, capacity, or incident state. Continuous deployment makes this decision automatically for every qualifying change. Neither discipline removes the need to validate identity, observe rollout, or recover from failure.

### Critical invariants

- bind every decision to an immutable artifact and source revision;
- keep technical evidence separate from business authorization;
- never call an artifact ready while required evidence is missing, stale, waived invisibly, or for another subject;
- use the same rehearsed deployment mechanism for routine, urgent, and rollback operations;
- preserve a deployable mainline even when business chooses not to release;
- distinguish deployment of code from activation of behavior;
- make environment, configuration, schema, and data transitions part of readiness;
- require observation and bounded exposure after production change;
- stop or reverse automatically when explicit rollout criteria fail;
- preserve approval, policy, artifact, environment, and rollout evidence;
- do not equate deployment frequency with continuous delivery capability;
- choose delivery versus deployment according to system risk and organizational authority, not fashion.

### Common failures

Common failures include calling artifact upload “delivery,” calling a nightly batch “continuous deployment,” treating a manual test phase as deployable-on-demand, rebuilding after approval, approving a mutable branch, deploying code and enabling all users simultaneously, using different emergency scripts, ignoring migrations and configuration, automating a weak gate, counting staging as production, claiming every production update is released, and optimizing deployment frequency while recovery remains manual.

### Compact example

Revision `r17` produces artifact digest `sha256:x`, passes required evidence, and is deployable through a rehearsed pipeline. Under continuous delivery, a product owner may wait until Tuesday, then authorize that exact digest. Under continuous deployment, policy automatically starts a one-percent production rollout as soon as `r17` qualifies. In either case, a feature flag can keep the new user behavior disabled until a separate release decision.

### Connections

[SDRE-017](017-quality-gates.md) defines readiness evidence, [SDRE-019](019-ci-secrets-and-untrusted-contributions.md) separates privileged deployment, and [SDRE-020](020-optimizing-feedback-time-without-hiding-risk.md) protects evidence while shortening feedback. [SDRE-022](../ROADMAP.md) next develops environment promotion.

## Governing Question

“CI/CD” often compresses three different practices into one label. That shorthand obscures who is authorized to act and what the system guarantees. Continuous integration concerns frequent integration and feedback. Continuous delivery concerns sustained deployability and on-demand execution. Continuous deployment concerns automatic production deployment of qualifying changes.

The distinction is not whether a button exists. It is whether the exact product is continually ready, whether deployment is routine and rehearsed, and whether a separate routine human release decision remains in the path. A manual decision can be legitimate governance; manual repair, bespoke commands, or days of stabilization are evidence that delivery is not continuous.

## Why This Matters

Fowler defines continuous delivery as keeping software releasable at any time and continuous deployment as automatically placing every qualifying change into production [1]. Humble and Farley's foundational treatment centers a deployment pipeline that makes release reliable, repeatable, and low risk [2]. The first discipline is a prerequisite capability; the second chooses an automatic production policy on top of it.

Confusing them causes bad design. A regulated system may have excellent continuous delivery with an authorized human production decision. Calling it immature because it is not continuously deployed mistakes governance for technical debt. Conversely, a system that automatically copies a poorly tested nightly artifact to production is automated deployment, not a trustworthy continuous-delivery capability.

Google's SRE release-engineering chapter illustrates that high automation can coexist with different deployment policies: some teams select from frequent builds, others push on green, and rollout pace is matched to service risk [3]. The durable lesson is to separate readiness, authorization, execution, and exposure while automating every repeatable mechanism.

## Prerequisites and Retrieval

Retrieve artifact, revision, environment, pipeline, gate, policy, approval, deployment, release, rollback, migration, configuration, observability, canary, feature flag, blast radius, incident, audit trail, and least privilege.

From SDRE-001 through SDRE-010 retrieve artifact identity, reproducibility, repositories, provenance, signing, and supply-chain evidence. From SDRE-011 through SDRE-020 retrieve CI, exact candidates, gates, untrusted boundaries, and complete feedback. Software Architecture owns deployability boundaries; Platform Engineering owns deployment mechanisms; Security Engineering owns authorization and credential depth; Product and organizational governance own legitimate release authority.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish continuous integration, delivery, deployment, and release;
2. state the continuous-delivery capability independently of deployment frequency;
3. model readiness, authorization, deployment, and exposure as separate decisions;
4. bind approvals and rollouts to exact artifacts and revisions;
5. identify manual decisions that are policy and manual work that is delivery debt;
6. design automated and human gates with honest evidence semantics;
7. decouple deployment from release using progressive exposure and feature controls;
8. include configuration, schema, data, observation, and recovery in readiness;
9. select a delivery policy appropriate to risk and authority;
10. audit whether claimed continuous practices survive failure and urgency.

## Core Exposition

**Separate the three continuous practices.** Continuous integration makes integration frequent and observable. It should produce an exact, tested candidate rather than a collection of unbound job results. Continuous delivery extends that chain until a production deployment is a routine, low-drama operation available on demand. Continuous deployment applies an automatic policy that sends every qualifying change through that operation.

These are capability and policy definitions, not tool products. A hosted pipeline does not establish continuous delivery if releases require a spreadsheet, custom shell session, manually assembled bundle, or multi-day stabilization branch. Conversely, one production deployment per month can coexist with continuous delivery if the product remains deployable and business intentionally chooses that cadence.

“Every change” in continuous deployment refers to every change that qualifies under declared policy, not every keystroke or failed candidate. Integration may combine related commits; a candidate may be superseded before reaching production; emergency stop policy may pause automation. Those exceptions must be explicit rather than used to label a scheduled batch as continuous.

**Define the delivery unit.** The unit might be a service image, signed package, mobile binary, infrastructure plan, configuration bundle, model, database migration set, or coordinated release manifest. Identify source revision, build recipe, dependencies, artifact digest, configuration schema, migration compatibility, and target environment.

Build once and promote the same identified artifact when possible. Rebuilding after approval creates a new subject and invalidates prior evidence unless reproducibility and policy explicitly re-establish equivalence. A release manifest can bind multiple service artifacts when compatibility requires a coordinated unit.

A release candidate is a proposal. The name does not imply safety. Evidence makes it ready under a policy, and later observation can invalidate confidence. Preserve the ability to halt, roll back, or roll forward.

**Make readiness a predicate.** Readiness combines identity, valid current evidence, policy satisfaction, and recoverability. Identity asks exactly what will change. Evidence includes build, test, security, compatibility, and environment-specific claims. Policy evaluates ownership, approvals, windows, risk class, and separation of duties. Recoverability checks rollback or roll-forward plan, backups where applicable, compatibility windows, and operational capacity.

Readiness is time-dependent. A vulnerability disclosure, expired approval, changed target configuration, stale test result, failed dependency, or active incident can make yesterday's candidate not ready today. Record policy and evidence versions with the artifact.

Do not make readiness a vague green badge. Report each claim and non-pass state: failed, pending, unavailable, unstable, waived, or expired. A waiver is an explicit authorization with scope and expiry, not a hidden pass.

**Separate evidence from authorization.** Automated tests answer technical questions within their assumptions. A business approval may answer whether a launch date, contract, market, communication, or operational window is acceptable. A security or change authority may accept residual risk. These decisions consume evidence but do not create missing evidence.

A manual gate is legitimate when human judgment or accountable authority is genuinely required. It is waste when a person merely transfers values, follows deterministic instructions, or clicks because automation is distrusted. Automate the mechanism and retain the smallest meaningful decision.

Bind approval to artifact digest, revision, target environment, policy, configuration, migration, and time. Approval of “latest” or a moving branch is not a controlled authorization. If the subject changes, request a new decision.

**Automate the deployment mechanism.** The same versioned mechanism should deploy to test, staging, canary, and production with environment data supplied through controlled configuration. Differences in scale and policy are expected; differences in undocumented procedure create rehearsal gaps.

Automation includes preconditions, credential acquisition, artifact verification, configuration resolution, migration ordering, rollout, health observation, halt, recovery, and audit. A script that copies bytes but leaves database and traffic changes to operators is incomplete.

Make operations idempotent where feasible. A retry after uncertain network failure should converge on the intended state or detect that human judgment is required. Store operation and attempt identity so two controllers cannot deploy the same mutable target inconsistently.

Emergency deployment uses the ordinary path with a defined expedited policy. If urgency requires an untested alternative command, that command will be least reliable when risk is highest. Rehearse rollback and break-glass authorization before incidents.

**Distinguish deploy from release.** Deploying code changes the production environment. Releasing exposes behavior to users. They often coincide, but feature flags, entitlements, configuration, API routing, and staged cohorts can separate them.

This separation reduces the size of one decision. Code may be deployed disabled, observed for operational regressions, enabled for staff, expanded to a cohort, and then released broadly. Each transition has its own subject, authority, evidence, metric, and recovery action.

Feature flags introduce inventory and state. Record owner, purpose, default, targeting, dependencies, expiry, and behavior when the control service fails. A flag is not a substitute for testing both enabled and disabled paths. Remove stale flags after rollout or they become permanent complexity.

Database schemas and externally visible APIs constrain separation. Old and new versions may coexist during rollout and rollback. Expand-and-contract migrations, backward-compatible readers, and bounded compatibility windows belong to readiness. A flag cannot undo destructive data loss.

**Use progressive exposure.** Continuous deployment does not require instantly sending every change to every user. Begin with a bounded canary, cell, region, tenant group, or traffic percentage; compare declared signals; halt on thresholds; then expand. Google's SRE Workbook describes canary analysis as comparing a partial deployment and warns that a stop signal may reveal a problem without proving the canary change caused it [4].

Define hypothesis, baseline, population, duration, metrics, thresholds, missing-data behavior, and decision authority before rollout. Guard against low traffic, novelty, delayed failure, selection bias, and correlated dependencies. A successful one-percent interval supports expansion under its conditions, not universal correctness.

Automated rollback is appropriate only when rollback is safe and the signal is trustworthy. Some schema or external side effects are irreversible; roll forward or disable behavior may be safer. Prevent oscillation with bounded attempts and escalation.

**Continuous delivery with a manual release decision.** A manual production decision can express product timing, legal approval, customer coordination, or operational risk. Everything after authorization should still be automated, quick, and repeatable. The current ready artifact should be deployable without a stabilization project.

Avoid release queues that accumulate dozens of unrelated changes. Even if technically deployable, large batches increase diagnosis and rollback ambiguity. Keep candidates small, preserve individual artifact identity, and permit selection only when dependency compatibility is known.

Release trains can be appropriate for devices, app stores, contractual windows, coordinated ecosystems, or user communication. Continuous delivery improves the train by keeping each included change ready, automating assembly and evidence, and allowing urgent deployment through the same mechanism. A train is not continuous deployment because qualifying changes wait for schedule or selection.

**Continuous deployment with automatic authorization.** An automatic policy evaluates readiness and starts production rollout without a routine person deciding “deploy now.” Humans design policy, review code, handle exceptions, and respond to anomalies. Automation does not remove accountability.

This requires strong gates, fast feedback, safe small changes, progressive exposure, observability, reliable rollback or roll-forward, and disciplined ownership. If the system cannot determine whether production is healthy, automatic deployment multiplies uncertainty.

Stop conditions include active incidents, exhausted error budgets, dependency degradation, missing telemetry, capacity risk, policy-service failure, and anomalous rollout signals. Fail closed or enter an explicitly safe holding state; do not deploy merely because the decision service is unavailable.

Not every domain should continuously deploy. Safety-critical, irreversible, jointly coordinated, offline, or legally controlled systems may require accountable authorization and longer observation. Continuous delivery is still valuable because it makes the authorized change reproducible and routine.

**Preserve environments without creating a fantasy staging world.** Pre-production environments establish integration and operational claims, but cannot reproduce all production traffic, data, scale, dependencies, or failure. Use them for controlled verification, then use bounded production exposure and observation.

Promote artifact identity rather than copying mutable environment state. Environment configuration is a separate versioned input. Record effective configuration and secret identifiers without exposing values. Detect drift between declared and running state.

Do not require a candidate to sit untouched in staging for arbitrary days as a substitute for exercised evidence. Time without representative workload provides weak information. Design specific soak hypotheses when duration matters, such as leaks, compaction, certificate refresh, or delayed jobs.

**Observe the complete change.** A deployment is not successful when the orchestrator returns zero. Observe service-level indicators, correctness signals, dependency behavior, resource saturation, logs, traces, and business invariants over a bounded window. Distinguish deployment completion from verification completion and release completion.

Bind telemetry to artifact version, configuration, cohort, and time. Aggregate metrics can hide a failed small cohort; sparse cohorts can generate noise. Preserve pre-change baseline and concurrent control where possible.

Close the loop with change-failure rate, recovery time, escaped-defect linkage, rollback outcomes, and policy exceptions. Deployment frequency alone can be gamed by deploying trivial changes or splitting operations without improving delivery capability.

**Test the delivery system.** Exercise success, failure, cancellation, duplicate request, stale approval, wrong artifact, unavailable dependency, partial rollout, telemetry loss, failed migration, rollback, and break-glass paths. Run non-destructive rehearsals and controlled recovery exercises.

Verify that a failed or unavailable gate cannot become ready, that a new artifact invalidates approval, and that continuous-deployment automation pauses safely. Audit production state against declared subject. The pipeline is software and receives version control, review, tests, and least privilege.

## Definitions and Notation

Let $A$ be artifacts, $T$ time, and $C$ deployment contexts. For artifact $a\in A$ at time $t\in T$ define

$$
Ready(a,t)=I(a)\land E(a,t)\land P(a,t)\land R(a,t),
$$

where $I$ establishes immutable identity, $E$ valid required evidence, $P$ policy satisfaction, and $R$ recoverability for the intended transition.

Let

$$
D:A\times T\times C\rightarrow\{deploy,hold,deny\}
$$

be deployment policy. Every `deploy` outcome requires $Ready(a,t)$. Continuous delivery ensures an authorized caller can evaluate $D$ and execute deployment on demand through the rehearsed mechanism. Continuous deployment configures $D$ to issue `deploy` automatically for every qualifying candidate, subject to explicit safety holds.

Let $Deploy(a,e)$ mean artifact $a$ becomes running state in environment $e$, and $Release(f,U)$ mean feature or behavior $f$ becomes available to user set $U$. In general,

$$
Deploy(a,e)\not\Rightarrow Release(f,U)
$$

because deployed code may remain disabled, and a release may be a configuration or entitlement change without new code deployment.

Represent authorization as $g=(a,e,c,p,t)$ for artifact, environment, configuration, policy version, and decision time. A change to any bound component requires re-evaluation.

## Mechanisms, Invariants, or Proof Structure

**Capability implication.** Continuous deployment requires a product to be ready and deployable before automation can safely choose production rollout; therefore trustworthy continuous deployment builds on continuous delivery. Continuous delivery does not imply continuous deployment because policy may return `hold` pending a legitimate decision.

**Subject-binding invariant.** Evidence and approval for artifact $a$ cannot authorize artifact $b$ when immutable identities differ. Rebuilding, retagging a mutable name, or changing effective configuration creates a different subject even if a label remains unchanged.

**Deployment-release counterexample.** Deploy code containing feature $f$ with the flag disabled for all users. `Deploy` is true while `Release` is false, disproving equivalence. Conversely, enabling an already deployed flag releases behavior without deploying new code.

**Readiness non-monotonicity.** Evidence expiration, new vulnerability information, target drift, incident state, or policy change can turn readiness from true to false over time. Therefore a past green result cannot authorize indefinitely.

**Executable state model.** The model distinguishes ready artifacts, manual authorization, automatic deployment, release activation, and redeployment rollback. It is intentionally small and does not control a real environment.

<!-- bijux-verify: {"id":"delivery-deployment-state-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"delivery_ready=r17,r19\nmanual_release_required=True\ndeployed_after_approval=True\ncontinuous_deployment_count=2\nfailed_candidate_deployed=False\nfeature_release_equals_deployment=False\nrollback_is_same_as_redeploy=True\n","stderr":""}} -->
```python
candidates = [
    {"id": "r17", "evidence": True, "policy": True, "recoverable": True},
    {"id": "r18", "evidence": False, "policy": True, "recoverable": True},
    {"id": "r19", "evidence": True, "policy": True, "recoverable": True},
]

def ready(candidate):
    return candidate["evidence"] and candidate["policy"] and candidate["recoverable"]

ready_ids = [candidate["id"] for candidate in candidates if ready(candidate)]
print("delivery_ready=" + ",".join(ready_ids))
manual_approval = {"r17": True}
print("manual_release_required=True")
print(f"deployed_after_approval={ready(candidates[0]) and manual_approval['r17']}")
automatically_deployed = [candidate["id"] for candidate in candidates if ready(candidate)]
print(f"continuous_deployment_count={len(automatically_deployed)}")
print(f"failed_candidate_deployed={'r18' in automatically_deployed}")
deployed_code = True
feature_enabled = False
print(f"feature_release_equals_deployment={deployed_code == feature_enabled}")
rollback = {"operation": "deploy", "artifact": "r16"}
print(f"rollback_is_same_as_redeploy={rollback['operation'] == 'deploy'}")
```

## Alternatives and Trade-Offs

**Continuous delivery versus continuous deployment.** Delivery retains an explicit release decision and suits external coordination or accountable risk acceptance. Deployment reduces waiting and batch size but requires machine-evaluable policy and strong recovery.

**Manual versus automated gate.** Human judgment handles ambiguous context and formal authority. Automation is consistent and fast. Keep humans for judgment, not deterministic mechanics.

**Deploy-and-release versus decoupled activation.** Coupling is simpler and reduces flag state. Decoupling limits exposure and separates operational from product decisions, but requires flag governance and compatibility.

**All-at-once versus progressive rollout.** Immediate rollout is fast and operationally simple. Progressive rollout limits blast radius and creates evidence, while prolonging coexistence and requiring attribution.

**Rollback versus roll forward.** Rollback is quick when state is compatible. Roll forward preserves irreversible migrations and accumulated fixes but requires rapid diagnosis and build capability.

**Artifact promotion versus rebuild.** Promotion preserves exact bytes and evidence. Rebuild can satisfy environment or trust constraints but creates a new subject requiring equivalence evidence.

**Independent services versus coordinated manifest.** Independent deployment reduces batch size. A manifest handles compatibility across components but increases coordination and rollback complexity.

**Release train versus on-demand release.** Trains support external schedules and joint communication. On-demand release minimizes waiting and batch size. Continuous delivery can support either; only automatic qualification-to-production is continuous deployment.

## Failure Modes and Misconceptions

- **“CI/CD is one practice.”** integration, delivery, and deployment have distinct guarantees.
- **“Artifact published means delivered.”** production readiness and deployability may remain untested.
- **“Frequent deployment proves continuous delivery.”** bespoke or fragile mechanisms can deploy often temporarily.
- **“Manual approval means delivery is not continuous.”** legitimate authorization can remain while mechanisms are continuous.
- **“Manual testing for days is approval.”** missing repeatable evidence is delivery debt.
- **“Continuous deployment sends every commit instantly.”** only qualifying exact candidates proceed under policy.
- **“Automation makes a weak gate safe.”** it repeats weak decisions faster.
- **“Green once means ready forever.”** evidence and context expire or change.
- **“Staging proves production.”** scale, traffic, data, and dependencies differ.
- **“Deployment equals release.”** feature controls and entitlements separate them.
- **“Feature flags eliminate risk.”** state, compatibility, cleanup, and control failure add risks.
- **“Canary success proves correctness.”** it supports bounded expansion under observed conditions.
- **“Rollback is always safe.”** schemas and external effects may be irreversible.
- **“Rebuild is the same candidate.”** new bytes require new identity and evidence.
- **“Release trains cannot use continuous delivery.”** deployability can be continuous while timing is scheduled.
- **“Continuous deployment is universally superior.”** authority and irreversibility may require a human decision.
- **“Production update success ends verification.”** observation and release outcomes remain.
- **“Deployment frequency alone measures capability.”** trivial changes and failed recovery can game it.

## Worked Examples

### Example 1

**Situation.** A team builds daily, spends two days on manual regression, and deploys monthly. **Reasoning.** The product is not continually ready; deployment depends on a stabilization activity. Automate and shift evidence into the pipeline before debating automatic production policy. **Conclusion.** Scheduled automation is not continuous delivery.

### Example 2

**Situation.** Every passing artifact can be deployed by one authorized action, but finance chooses a quarterly customer launch. **Reasoning.** If deployability is genuinely maintained and rehearsed, the team practices continuous delivery with scheduled release policy. It does not practice continuous deployment. **Conclusion.** Business cadence does not negate delivery capability.

### Example 3

**Situation.** Every qualifying service change automatically starts a one-percent production canary and expands on healthy signals. **Reasoning.** No routine person chooses when to deploy, while automatic gates and safety holds govern rollout. **Conclusion.** Progressive rollout is compatible with continuous deployment.

### Example 4

**Situation.** Approval names tag `latest`; the pipeline rebuilds after approval. **Reasoning.** Both the tag and bytes can change, so evidence and authorization do not identify the deployed subject. Bind revision, artifact digest, configuration, target, and policy; promote exact bytes or revalidate the rebuild. **Conclusion.** Mutable approval breaks delivery integrity.

### Example 5

**Situation.** Code for a redesigned checkout is deployed with its flag disabled, then enabled for employees the next day. **Reasoning.** Deployment occurred first; release occurred when the audience gained access. Test both paths, record the two decisions, observe cohorts, and plan flag removal. **Conclusion.** Deployment and release are independent transitions.

### Example 6

**Situation.** A migration drops a column before old instances stop reading it. **Reasoning.** Progressive code rollout cannot make the destructive schema compatible. Expand first, deploy readers that tolerate both schemas, migrate data, then contract after the rollback window. **Conclusion.** Data compatibility is part of readiness.

### Example 7

**Situation.** A canary's error rate rises while its upstream dependency simultaneously degrades. **Reasoning.** Halt expansion because the risk threshold failed, but do not claim the candidate caused the signal. Compare controls, dependency metrics, version labels, and timing before deciding rollback. **Conclusion.** Stop decisions need not imply causal proof.

### Example 8

**Situation.** An emergency patch requires operators to bypass the normal system with an unreviewed script. **Reasoning.** The organization has not rehearsed urgent delivery. Add an expedited policy to the ordinary pipeline with bound approval, required minimum evidence, narrow credentials, canary, observation, and follow-up. **Conclusion.** Emergency reliability comes from practiced mechanisms.

### Example 9

**Situation.** A mobile application cannot force rapid client rollback. **Reasoning.** Maintain continuous delivery of signed candidates, but use staged store release, server-compatible APIs, remotely disableable behavior, and roll-forward plans. Automatic deployment policy must respect irreversible distribution. **Conclusion.** Platform constraints shape policy without removing delivery discipline.

### Example 10

**Situation.** A team doubles deployments by sending separate no-op configuration updates. **Reasoning.** Frequency rose without improving lead time, readiness, change failure, recovery, or user value. Audit meaningful change units and complete outcomes. **Conclusion.** Activity count is not a delivery capability measure.

## Cross-Program Connections

- Software Architecture owns deployability, compatibility boundaries, and independently changeable components.
- Platform Engineering owns deployment controllers, environments, credentials, feature-control services, and audit infrastructure.
- Security Engineering owns authorization, separation of duties, artifact verification, and break-glass controls.
- Database Engineering owns migration correctness, transactional boundaries, and rollback constraints.
- Distributed Systems owns partial rollout, controller idempotence, retries, convergence, and uncertain outcomes.
- Testing & Quality Engineering owns evidence adequacy, environment-specific checks, and release validation.
- API & Service Engineering owns compatibility, version negotiation, contract rollout, and consumer coordination.
- Cloud Engineering owns infrastructure changes, identity, region rollout, and declared-versus-running state.

## References

1. Martin Fowler, [Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html), 2013, updated 2014, definition and distinction from continuous deployment.
2. Jez Humble and David Farley, *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*, Addison-Wesley, 2010.
3. Dinah McNutt, [Release Engineering](https://sre.google/sre-book/release-engineering/), *Site Reliability Engineering*, 2016, automated release systems, policy, artifact identity, and risk-matched rollout.
4. Carlos Arilla, Nand Kishore, and Brendan McAdams, [Canarying Releases](https://sre.google/workbook/canarying-releases/), *The Site Reliability Workbook*, 2018, bounded rollout and canary-analysis reasoning.
5. Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate*, IT Revolution, 2018, continuous-delivery capabilities and software-delivery performance research.
6. Continuous Delivery Foundation, [Glossary definitions](https://github.com/cdfoundation/glossary/blob/main/definitions.md), community-maintained continuous delivery and deployment terminology. Retrieved 2026-09-06.
7. National Institute of Standards and Technology, [Secure Software Development Framework, SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final), Version 1.1, 2022, secure release and provenance practices.
8. Martin Fowler, [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html), 2024 revision, integration frequency, automated evidence, and delivery distinctions.

## Exercises

### Exercise 1

Define continuous integration, continuous delivery, continuous deployment, deployment, release, readiness, approval, progressive delivery, rollback, and release train. State the implication relationships among the first three.

### Exercise 2

For artifact `a7`, build and tests pass, policy approval is current, but rollback has not been tested after a destructive migration. Evaluate the readiness predicate. Then show how a feature flag changes deployment and release truth values.

### Exercise 3

A company has automated nightly production copies, manual database commands, mutable `latest` tags, and no version-linked telemetry. Diagnose its claimed continuous deployment and design the minimum credible continuous-delivery path.

### Exercise 4

Compare continuous delivery with a manual production decision against continuous deployment for a payment service. Include evidence, authorization, batch size, progressive exposure, observability, data compatibility, rollback, incident holds, and audit.

### Exercise 5

Design a delivery model for industrial devices that may be offline for months and cannot safely roll back firmware after a one-way data conversion. Show how continuous-delivery principles apply even if continuous deployment is rejected.

## Answers to the Exercises

### Answer 1

Continuous integration frequently combines and verifies changes in shared code. Continuous delivery keeps exact products deployable on demand through a routine pipeline. Continuous deployment automatically deploys every qualifying change without a separate routine human release decision. Deployment changes running software or configuration; release exposes behavior to consumers. Readiness is current identity-bound evidence, policy, and recoverability. Approval authorizes a bound action and subject. Progressive delivery expands production exposure based on observation. Rollback redeploys or restores an earlier state. A release train accumulates changes for a schedule. Trustworthy continuous deployment requires continuous-delivery capability, which builds on continuous integration; neither reverse implication holds because delivery may retain a manual decision and integration may stop before deployability.

### Answer 2

$I(a7)$, $E(a7,t)$, and $P(a7,t)$ may be true, but $R(a7,t)$ is false or unestablished because recovery after the destructive migration is not verified. The conjunction is therefore not ready. Repair may require backward-compatible expansion, backup and restore evidence, roll-forward procedure, or explicit non-rollback containment before new authorization. If code is deployed with a feature flag disabled, `Deploy(a7,production)` is true while `Release(feature,users)` is false. Enabling the already deployed flag can make release true without a new code deployment. Neither transition repairs irreversible data risk by itself.

### Answer 3

Nightly automation is scheduled deployment, not automatically every qualifying change, and manual database commands mean the product is not deployable by one rehearsed mechanism. `latest` breaks subject binding; missing version telemetry prevents rollout verification. First produce immutable versioned artifacts and configuration, automate database transitions with compatibility and recovery checks, build an evidence pipeline for the exact artifact, and create an idempotent deployment mechanism used across environments. Bind approval to artifact, environment, configuration, migration, and policy. Add version-linked health and correctness telemetry, progressive exposure, halt, and recovery. Once current mainline remains ready and an authorized artifact can deploy on demand, continuous delivery is credible. Only then consider replacing the release decision with automatic policy.

### Answer 4

Both models require exact artifacts, complete payment-integrity and security evidence, narrow deployment authority, backward-compatible data transitions, version-linked telemetry, canary cohorts, explicit halt criteria, recovery, and immutable audit records. Manual-decision delivery lets an accountable payment or risk owner consider settlement windows, incidents, partner readiness, and residual risk; everything after that decision should be automated. Continuous deployment encodes those conditions and automatically rolls out each qualifier, reducing waiting and batch size but demanding trustworthy machine-evaluable signals and safe hold behavior. Neither should auto-rollback irreversible ledger changes; disablement or roll forward may be safer. Choose continuous deployment only where automatic policy represents legitimate authority and observability detects harm within the bounded exposure.

### Answer 5

Continuously integrate firmware and produce signed, immutable candidates with source, toolchain, dependency, hardware-revision, configuration, and migration provenance. Test on emulators, representative devices, power-loss points, old and new data, upgrade chains, secure-boot paths, and long-offline versions. Maintain backward readers or a transactional one-way conversion with recovery partition and verified roll-forward image. Automate packaging, staged fleet targeting, bandwidth and power preconditions, signature verification, installation, health report, and quarantine. Keep every accepted candidate deployable on demand, but require accountable authorization by device class and maintenance window. Roll out to instrumented internal devices and cohorts before expansion, and never assume silent offline devices are healthy. Reject continuous deployment if automatic policy cannot safely handle irreversible state or sparse feedback; that choice still preserves continuous-delivery discipline.
