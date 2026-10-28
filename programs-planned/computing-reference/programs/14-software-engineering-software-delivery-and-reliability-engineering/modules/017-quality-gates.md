---
module_id: SDRE-017
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 17
title: Quality Gates
status: complete
last_verified: 2026-09-06
---

# Quality Gates

## One-Page Review

### Governing question

How should a delivery system turn explicit quality and risk policy into a reproducible admission decision without confusing tool output, numerical thresholds, or human approval with proof of software quality?

### Essential definitions

- a **quality gate** is a policy decision that admits, rejects, defers, or explicitly waives a candidate based on bounded claims and evidence;
- a **claim** is a precise property the gate is intended to establish for a named subject;
- **evidence** is an observation, result, attestation, or approval relevant to a claim;
- the **subject** is the exact revision, artifact, environment, or release being judged;
- a **predicate** maps accepted evidence and context to true, false, or unknown;
- **pass** means every mandatory predicate is true for the exact subject;
- **fail** means at least one mandatory predicate is false;
- **incomplete** means required evidence is missing, stale, unavailable, unverifiable, or ambiguous;
- a **waiver** is an authorized, scoped, expiring exception with rationale and compensating controls;
- a **threshold** is a declared decision boundary over a measured quantity;
- a **baseline** is an approved reference against which change is compared;
- **policy as code** stores reviewable, versioned, executable decision rules;
- **provenance** records where, when, how, and from which inputs an artifact or result was produced;
- a **false acceptance** admits a subject that violates the intended property; a **false rejection** blocks one that satisfies it.

### Central model, mechanism, or theorem

For subject $s$, policy $P$, mandatory claims $C_P$, and evidence bundle $E$, define each predicate

$$
g_c(s,E,P)\in\{true,false,unknown\}.
$$

The unwaived gate passes exactly when every mandatory predicate is true, fails when at least one is false, and is incomplete otherwise. Unknown is not true. A valid waiver changes the policy decision for named claims; it does not change the underlying evidence or claim truth.

### Critical invariants

- name the exact subject before evaluating evidence;
- state every mandatory claim and its owner;
- bind evidence to subject, producer, method, environment, policy, and time;
- distinguish test completion from test adequacy;
- treat missing and unverifiable evidence as incomplete, not pass;
- define thresholds with units, population, direction, and boundary behavior;
- version policy and evaluate the version intended for the decision;
- separate absolute risk limits from change-relative regression limits;
- authenticate evidence producers and protect policy from candidate-controlled writes;
- make waivers scoped, authorized, expiring, visible, and reviewable;
- preserve the original failure beneath a waiver;
- keep decision latency compatible with rapid feedback;
- audit outcomes and recalibrate gates against escaped defects and needless blocks.

### Common failures

Common failures include gating on a status name without revision identity, equating code coverage with correctness, using arbitrary round-number thresholds, letting skipped checks pass, trusting self-reported provenance, applying one risk policy to every subsystem, waiving without expiry, changing policy mid-run without recording it, counting flaky retries as independent proof, blocking on unactionable metrics, and adding so many slow gates that developers batch changes or bypass the system.

### Compact example

A release gate requires unit tests for artifact digest `a7`, zero known critical vulnerabilities under scanner policy `v3`, and authenticated build provenance linking `a7` to revision `r9`. Tests pass and the scan reports zero, but provenance names artifact `a6`. The gate is incomplete for `a7`; it does not average two good results and one mismatch into a pass. An authorized temporary waiver may permit a bounded decision, but the provenance claim remains unmet.

### Connections

[SDRE-016](016-merge-queues.md) ensures gates evaluate the exact integration revision. [SDRE-018](../ROADMAP.md) next treats nondeterministic gate evidence, and [SDRE-019](../ROADMAP.md) protects secrets and trust boundaries in CI.

## Governing Question

A delivery pipeline produces many signals: tests, analyzers, scans, reviews, benchmarks, manifests, signatures, and operational approvals. A quality gate converts some of those signals into a decision. The conversion is policy, not a natural property of the tools. It must say what subject is judged, what claims matter, what evidence is acceptable, how uncertainty is handled, and who may override the result.

The goal is neither “block everything risky” nor “make the pipeline green.” It is to create a fast, explainable control whose false-acceptance and false-rejection risks match the system. A gate that developers routinely bypass, cannot diagnose, or can forge is weaker than its dashboard suggests.

## Why This Matters

Without gates, passing observations may never affect admission. With badly designed gates, proxies become targets: teams add superficial tests to reach a coverage percentage, suppress findings to meet a count, or split changes to evade size limits. The control can reduce visible warnings while leaving actual risk unchanged.

NIST SP 800-218 defines a Secure Software Development Framework of high-level practices to integrate into each software-development lifecycle rather than prescribing one universal pipeline [1]. This supports risk-based tailoring: a gate should implement an owned control and its evidence, not copy a generic checklist.

Current GitHub ruleset documentation allows required status checks and an expected application as the status source, and distinguishes strict from loose base synchronization [2]. Current SLSA 1.2 documentation treats provenance as verifiable information about how an artifact was produced and requires verification against expectations [3]. These sources illustrate two separate needs: enforce a decision at the protected boundary, and authenticate evidence about the exact subject.

DORA's current continuous-delivery guidance emphasizes fast feedback, reliable tests, pervasive security, and deployability rather than a single score [4]. A good gate supports that feedback loop. A slow, noisy control that creates large batches can increase the risk it intended to reduce.

## Prerequisites and Retrieval

Retrieve Boolean logic, three-valued logic, predicate, set, threshold, unit, percentile, confidence, false positive, false negative, test oracle, code coverage, static analysis, dynamic analysis, vulnerability, severity, exploitability, artifact digest, signature, provenance, authentication, authorization, policy, audit log, exception, expiry, compensating control, and risk acceptance.

From SDRE-003 through SDRE-010 retrieve artifact identity, build reproducibility, testing layers, and release evidence. From SDRE-014 retrieve selected-work limitations; from SDRE-015 retrieve latency and cancellation; from SDRE-016 retrieve exact integration subjects and status authenticity. Security Engineering owns threat and vulnerability models; Testing & Quality Engineering owns test adequacy; this chapter owns their use in delivery admission.

## Learning Objectives

After completing this module, you should be able to:

1. express a gate as claims, predicates, evidence, and outcomes;
2. distinguish pass, fail, incomplete, and waived;
3. bind results to exact revisions and artifact digests;
4. design meaningful absolute and change-relative thresholds;
5. explain why coverage and finding counts are proxies;
6. authenticate evidence producers and version policy;
7. define a safe waiver lifecycle;
8. order gates for useful feedback without weakening claims;
9. tailor controls to risk while retaining consistent governance;
10. evaluate gate effectiveness through outcome and process evidence.

## Core Exposition

**Begin with claims, not tools.** “Run scanner X” is an activity. “No dependency with a known critical vulnerability under advisory snapshot D may enter release R without an approved exception” is a claim and policy boundary. The latter states subject, classification, time-dependent data, outcome, and exception path.

For each gate, maintain a contract: identifier, purpose, subject type, mandatory claims, evidence schemas, trusted issuers, evaluation logic, policy version, owners, failure messages, timeout behavior, waiver authority, and audit retention. Tool configuration implements this contract; it is not the contract itself.

**Identify the subject exactly.** A source gate may judge a commit or merge revision. A build gate may judge an artifact digest. A deployment gate may judge an artifact-environment pair. Results for one subject do not transfer merely because names or branches match.

Bind an artifact check to both artifact digest and source provenance. A source test can pass while packaging introduces an unsafe dependency or wrong files. Conversely, an artifact scan does not prove the source review process occurred. Multiple claims require appropriately scoped evidence.

**Use explicit outcome states.** A Boolean API often collapses important uncertainty. Use at least pass, fail, and incomplete. Pass means all mandatory predicates true. Fail means a mandatory predicate evaluated false. Incomplete covers missing report, expired attestation, unknown scanner version, lost worker, malformed output, unavailable platform, or unverifiable signature.

A waiver is not a fourth truth value for the claim. It is a policy decision to accept a known fail or incomplete state under named authority and controls. Preserve both the underlying outcome and the waiver. A dashboard showing only green after waiver destroys risk visibility.

Distinguish not-applicable from skipped. Not-applicable follows a versioned scope rule, such as no mobile package being produced. Skipped means expected work did not run. The first can satisfy policy if justified; the second is incomplete.

**Accept evidence, not labels.** An evidence envelope should contain subject identity, claim or check identity, producer identity, method and configuration, tool and rule versions, environment, inputs or dependency snapshot, start and finish time, raw result digest, normalized conclusion, and limitations. Authenticate the producer and verify schema before evaluating values.

Candidate-controlled code must not be able to forge the evidence that approves itself. Separate untrusted execution from control-plane signing or status publication. SLSA 1.2 distinguishes provenance existence, authenticity, and stronger resistance to tenant forgery [3]; merely creating JSON called `provenance` does not establish trust.

Current data matters. Vulnerability databases, revocation status, policy, dependencies, and platform support change. Record retrieval or snapshot identities and define freshness. Re-evaluate when a decision occurs after the evidence window or when material inputs change.

**Design predicates precisely.** Every threshold needs quantity, unit, population, comparison direction, aggregation, and boundary. “Coverage must be 80” is incomplete. Is that 80 percent of statements, branches, changed lines, or weighted critical paths? Is exactly 80 accepted? How are generated and unreachable lines handled? Which tool version defines the denominator?

Thresholds should follow a risk model or empirically calibrated operating policy. A critical-service latency gate might require the 99th percentile under a defined load to remain below a service objective with stated measurement uncertainty. A library might require all supported ABI fixtures. A safety-relevant component may require named independent approval.

Avoid arbitrary universal gates. A 75% coverage floor can block a well-tested parser with defensive unreachable branches while passing a trivial module with assertions that execute lines without checking outcomes. Coverage locates unexecuted structure; it does not prove oracle quality, input adequacy, concurrency safety, or requirement satisfaction.

**Combine absolute and relative limits.** An absolute gate enforces a maximum risk, such as zero known unwaived critical findings. A relative gate prevents regression from an approved baseline, such as no new high-severity finding in changed code. Relative-only policy can preserve a dangerously poor baseline; absolute-only policy can make an inherited backlog block every improvement.

Use a governed remediation plan when existing debt exceeds the target: freeze new debt, assign owners and dates, and reduce the baseline. Do not silently reset the baseline after every failure. Store baseline identity and change history.

Counts also hide severity and reachability. Ten informational findings are not necessarily worse than one remotely exploitable critical flaw. Risk scoring must state sources, assumptions, asset exposure, exploit preconditions, and confidence. Human judgment may be needed, but it too becomes recorded evidence with bounded authority.

**Compose gates with three-valued logic.** For mandatory claims, conjunction is appropriate: every claim must be true. One false makes the gate fail; if none is false but at least one is unknown, the gate is incomplete. Do not average heterogeneous controls into a score unless policy explicitly accepts compensation and can defend the weights.

Some claims are alternatives: either two independent reviewers or one named safety board may authorize a class of change. Encode the disjunction and its trust assumptions. Short-circuit execution can save time after decisive failure, but the decision record should still say which predicates were unevaluated.

Dependencies among gates matter. An artifact scan requires an artifact. A provenance verifier needs provenance and expectations. A deployment exercise needs an environment. Model this as evidence prerequisites, not arbitrary stage order.

**Order for feedback and cost.** Run fast, high-signal, low-cost checks early, while preserving parallelism for independent work. A syntax error should be reported before a 40-minute performance suite finishes. But early checks must not become the only checks because they are convenient.

Use risk-based selection from SDRE-014 and dependency-aware scheduling from SDRE-015. Mandatory baselines remain mandatory. Fail-fast is useful for negative admission but may reduce diagnostic coverage; periodic or nightly collect-all workflows can surface secondary issues without redefining the release gate.

Gate latency is part of control effectiveness. If a required manual review has a two-day median wait, teams will batch more work or seek exceptions. Improve ownership, automation, and architecture rather than quietly weakening the rule.

**Treat policy as governed code.** Store policy in version control with tests for pass, fail, incomplete, boundary values, malformed evidence, stale evidence, conflicting reports, and waiver expiry. Require review from control owners. Deploy policy changes through an observable process and support rollback.

Bind each decision to the policy version actually evaluated. If policy changes while a candidate waits, define whether current policy or entry policy governs. Security emergency rules may require immediate reevaluation; compatibility migrations may need a scheduled transition. Hidden behavior creates inconsistent admissions.

Separate policy authoring from candidate input. A proposal must not lower its own threshold, remove a required check, change trusted issuers, or grant itself a waiver without independent authorization. Policy changes may be ordinary repository changes only when the repository's protection prevents this circular approval.

**Design waivers as expiring risk records.** A waiver names subject or bounded subject class, failed or incomplete claim, rationale, risk owner, approving authority, issue, compensating controls, start and expiry, maximum uses, and revocation conditions. The gate verifies scope and time at decision.

Prefer narrow waivers. “Ignore scanner until fixed” is unbounded. “Allow artifact digest a7 despite finding F until 2026-09-08 for internal staging only, with network isolation and no customer data” is reviewable. A release or new digest requires new evaluation unless the waiver explicitly covers it.

Expiration should fail visibly before the last safe moment. Track waiver age and repeated renewals. Repeated exceptions often reveal an unusable gate, missing capacity, poor ownership, or accepted risk that should be encoded transparently in policy.

**Preserve explainability and actionability.** A failure response identifies claim, subject, observed value, expected predicate, evidence source, policy version, likely owner, and safe next actions. Avoid “quality gate failed” without details. Developers should reproduce deterministic evaluation locally when secrets and trusted issuance are not required.

Do not expose secrets or sensitive vulnerability detail to unauthorized contributors. Provide enough explanation to remediate while maintaining access controls. Record full evidence in the governed system.

**Evaluate the gate itself.** Track decision counts by outcome, incomplete reasons, evaluation latency, false rejections, escaped defects relevant to gated claims, waiver volume and age, repeated manual overrides, rework, and time to remediation. Sample accepted candidates for deeper review and seed known violations to test enforcement.

An escape does not automatically prove one predicate was wrong; the claim set may have omitted the risk. A block does not automatically prove value; it may be noisy or unactionable. Conduct causal review: which claim should have covered the event, what evidence existed, how policy evaluated it, and whether the boundary needs change.

Beware Goodhart effects: once a proxy is a target, behavior can optimize the number rather than the quality. Rotate semantic review, inspect distributions rather than only thresholds, and retain qualitative design judgment. Gates support engineering judgment; they do not replace it.

## Definitions and Notation

Let subject $s$ have policy $P$ and evidence bundle $E$. Policy declares mandatory claims $C_P$. For each claim $c\in C_P$, evaluator

$$
g_c(s,E,P)\in\{T,F,U\}
$$

returns true, false, or unknown. Without a waiver, aggregate outcome $G$ is

$$
G(s,E,P)=
\begin{cases}
fail & \text{if }\exists c:g_c=F,\\
pass & \text{if }\forall c:g_c=T,\\
incomplete & \text{otherwise.}
\end{cases}
$$

This is a policy definition, not a statistical theorem. Precedence ensures a known false is not hidden by unknown evidence.

For evidence produced at $t_e$ and decision time $t_d$, a freshness predicate with allowed age $\Delta_c$ is

$$
t_d-t_e\le\Delta_c.
$$

The policy must define time source, clock assumptions, and whether equality passes. For an observed metric $x$ with upper limit $\theta$, predicate $x\le\theta$ differs at the boundary from $x<\theta$.

Let $A$ be accepted subjects and $V$ the subjects that truly violate the intended property under a later evaluation oracle. False-acceptance observations are $A\cap V$. The oracle is incomplete in practice, so observed escapes are a lower bound on all false acceptances, not a measured universal rate.

## Mechanisms, Invariants, or Proof Structure

**Aggregation proof.** If every mandatory evaluator is total over $\{T,F,U\}$, the rule has three disjoint outcomes: any false; otherwise all true; otherwise at least one unknown. Thus missing evidence cannot produce pass. This proves decision consistency for supplied evaluators, not correctness of their claims.

**Subject-binding counterexample.** Tests and scan pass for artifact `a6`, while release points to `a7`. Even identical filenames do not make the subjects equal. A gate accepting the reports for `a7` violates its own evidence premise.

**Threshold-boundary invariant.** For an upper inclusive limit $x\le\theta$, $x=\theta$ passes and any $x>\theta$ fails when measurement is known. Tests must cover both sides and exact equality. Measurement uncertainty may require an interval rule rather than pretending $x$ is exact.

**Waiver preservation.** A waiver transforms a policy decision while retaining original $g_c$. If storage overwrites `fail` with `pass`, the system cannot audit accepted risk, revoke correctly, or distinguish remediation from exception.

**Executable gate model.** This deterministic evaluator demonstrates pass, incomplete, fail, stale evidence, and waiver behavior. It does not scan code or authenticate real provenance.

<!-- bijux-verify: {"id":"quality-gate-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"healthy=pass\nmissing_provenance=incomplete\ncritical_vulnerability=fail\nexpired_evidence=incomplete\nvalid_waiver=waived\ncoverage_percentage_proves_quality=False\nsame_revision_required=True\n","stderr":""}} -->
```python
policy = {"max_critical": 0, "max_age": 60, "revision": "r9"}

def evaluate(evidence, now, waiver=None):
    required = {"tests", "critical", "provenance", "revision", "observed_at"}
    if not required <= evidence.keys():
        outcome = "incomplete"
    elif evidence["revision"] != policy["revision"]:
        outcome = "incomplete"
    elif now - evidence["observed_at"] > policy["max_age"]:
        outcome = "incomplete"
    elif not evidence["provenance"]:
        outcome = "incomplete"
    elif evidence["critical"] > policy["max_critical"] or not evidence["tests"]:
        outcome = "fail"
    else:
        outcome = "pass"
    if outcome != "pass" and waiver is not None:
        in_scope = waiver["revision"] == evidence.get("revision")
        if in_scope and now <= waiver["expires"] and waiver["authorized"]:
            return "waived"
    return outcome

healthy = {
    "tests": True, "critical": 0, "provenance": True,
    "revision": "r9", "observed_at": 100,
}
print(f"healthy={evaluate(healthy, 120)}")
missing = {key: value for key, value in healthy.items() if key != "provenance"}
print(f"missing_provenance={evaluate(missing, 120)}")
critical = {key: value for key, value in healthy.items()}
critical["critical"] = 1
print(f"critical_vulnerability={evaluate(critical, 120)}")
print(f"expired_evidence={evaluate(healthy, 200)}")
waiver = {"revision": "r9", "expires": 130, "authorized": True}
print(f"valid_waiver={evaluate(critical, 120, waiver)}")
print("coverage_percentage_proves_quality=False")
print(f"same_revision_required={policy['revision'] == healthy['revision']}")
```

## Alternatives and Trade-Offs

**Hard gate versus advisory signal.** A hard gate enforces policy but imposes false-rejection and latency costs. An advisory signal supports judgment without prevention. Start advisory while calibrating only if risk permits and activation criteria are explicit.

**Universal versus risk-tiered policy.** Universal rules are consistent and easy to audit. Risk tiers match control strength to exposure but can be gamed through classification. Govern tier ownership and audit downgrades.

**Absolute versus relative threshold.** Absolute limits bound total risk but can freeze legacy systems. Relative limits prevent regression but preserve debt. Combine them with a remediation trajectory where appropriate.

**Automated versus human decision.** Automation is fast and consistent for machine-observable predicates. Humans can evaluate context and ambiguity but introduce wait and variability. Record structured rationale and authority for manual evidence.

**Fail-fast versus collect-all.** Fail-fast shortens a negative decision and saves capacity. Collect-all gives fuller diagnosis. Preserve unevaluated status and run broader diagnostics on a separate cadence if needed.

**Central policy versus repository-owned policy.** Central policy gives organization-wide consistency. Local ownership improves context and actionability. Use centrally governed minimum claims with narrower repository extensions and clear precedence.

**Current policy versus entry policy.** Current policy responds immediately to new risk but can surprise queued work. Entry policy gives predictability but may admit newly forbidden subjects. Define transition classes and re-evaluation rules.

**Block versus waiver.** Blocking preserves the declared boundary. A waiver supports exceptional delivery with accepted risk but can normalize bypass. Scope, expiry, compensating controls, and renewal review make the trade visible.

## Failure Modes and Misconceptions

- **“A green check means high quality.”** It means one declared evaluator reported an accepted result.
- **“More gates always reduce risk.”** Slow, noisy gates encourage batching and bypass.
- **“Coverage measures correctness.”** It measures executed structure under a particular definition.
- **“Zero findings means no vulnerabilities.”** Tools, rules, reachability, and data are incomplete.
- **“All findings have equal risk.”** Severity, exploitability, exposure, and confidence differ.
- **“Relative improvement is safe.”** A better but still unacceptable baseline remains unacceptable.
- **“An absolute threshold works everywhere.”** Context and inherited debt vary.
- **“Skipped equals not applicable.”** Skipped required work is incomplete.
- **“Missing means fail.”** It blocks admission, but the diagnosis differs from a false predicate.
- **“Retrying creates stronger evidence.”** Correlated repeats do not establish independence.
- **“Policy names identify policy.”** Decisions require immutable policy versions.
- **“Anyone who can run a check may attest it.”** Producer authority and tamper resistance matter.
- **“Provenance exists, therefore it is trustworthy.”** Existence, authenticity, and accuracy differ.
- **“A waiver fixes the failure.”** It records accepted risk; the claim remains unmet.
- **“Permanent exceptions are simpler.”** They silently redefine policy without governance.
- **“Manual approval is self-explanatory.”** Scope, rationale, identity, and time must be recorded.
- **“A gate needs no tests.”** Boundary, unknown, stale, malformed, and waiver cases are software behavior.
- **“No observed escape proves effectiveness.”** Detection and sampling are incomplete.

## Worked Examples

### Example 1

**Situation.** Tests pass for commit `r8`, but the merge queue asks to admit `r9`. **Reasoning.** The report's subject differs from the decision subject. Mark test evidence incomplete for `r9` and run or safely reuse only through a complete matching key. **Conclusion.** Status names never replace revision binding.

### Example 2

**Situation.** Coverage rises from 78% to 82%, but assertions were removed. **Reasoning.** More lines execute while oracle strength declined. Review mutation results, assertions, requirements, and risk-specific tests; do not infer quality from coverage alone. **Conclusion.** A proxy threshold needs semantic review.

### Example 3

**Situation.** A policy allows at most zero critical vulnerabilities; the scanner reports one high and twelve medium findings. **Reasoning.** The critical predicate is true, but other mandatory severity predicates must be evaluated separately. Counts cannot be averaged into one quality score. **Conclusion.** Gate only the claims policy actually defines.

### Example 4

**Situation.** The scan report is signed and names the right artifact, but its advisory snapshot is 45 days old under a seven-day freshness rule. **Reasoning.** Authentic stale evidence remains stale. Mark incomplete and rescan against an accepted snapshot. **Conclusion.** Authenticity does not imply currency.

### Example 5

**Situation.** A benchmark limit is `p99 <= 200 ms`, and measured p99 is exactly 200 ms. **Reasoning.** The inclusive boundary passes if measurement protocol and uncertainty rule accept the value. Tests should also cover just above 200. **Conclusion.** Operators and boundary semantics belong in policy.

### Example 6

**Situation.** A legacy service has 400 approved warnings, and an absolute zero-warning gate blocks a security fix. **Reasoning.** Preserve a governed baseline, forbid new warnings, define severity-specific absolute limits, and schedule debt reduction. Do not reset the baseline after regressions. **Conclusion.** Combine non-regression with an explicit target state.

### Example 7

**Situation.** A trusted build service emits provenance, but candidate code can read the signing key. **Reasoning.** The attestation can be forged by the subject it approves. Move issuance and keys into a protected control plane and verify the issuer. **Conclusion.** Self-reported evidence is not a security boundary.

### Example 8

**Situation.** An internal staging release needs a two-day exception for finding F. **Reasoning.** Bind the waiver to exact artifact, environment, claim, owner, expiry, and network-isolation control. Preserve the failure and prohibit production promotion. **Conclusion.** Narrow waivers make accepted risk auditable.

### Example 9

**Situation.** A mandatory check times out because its only runner is unavailable. **Reasoning.** The claim did not evaluate false; evidence is unavailable. Outcome is incomplete, the gate blocks, and operations diagnoses capacity separately from product repair. **Conclusion.** Decision and diagnosis need distinct states.

### Example 10

**Situation.** Gate blocks fall 70% after teams add suppressions, but escaped defects rise. **Reasoning.** The proxy was optimized. Audit suppression ownership, seeded violation detection, claim coverage, and downstream incidents; recalibrate policy and incentives. **Conclusion.** Evaluate control outcomes, not dashboard greenness.

## Cross-Program Connections

- Testing & Quality Engineering owns oracle quality, coverage meaning, statistical evidence, and test design.
- Security Engineering owns threat models, vulnerability policy, trusted issuers, and exception risk.
- Software Engineering Patterns owns modular policy evaluators and separation of decision from mechanism.
- Software Architecture owns quality attributes and system-specific trade-offs behind gate claims.
- API & Service Engineering owns authenticated status and evidence contracts.
- Platform Engineering owns policy engines, protected boundaries, runners, attestations, and observability.
- Data Engineering owns evidence lineage, schema quality, freshness, and completeness.
- Systems Engineering owns feedback loops, risk trade-offs, bottlenecks, and control evaluation.
- Distributed Systems owns time, retries, identity, and consistency limits in evidence collection.

## References

1. Murugiah Souppaya, Karen Scarfone, and Donna Dodson, [NIST SP 800-218: Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218), February 2022.
2. GitHub, [Available Rules for Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), official documentation for required checks, expected sources, reviews, and branch policy. Retrieved 2026-09-06.
3. SLSA Project, [SLSA Specification 1.2: Provenance](https://slsa.dev/spec/v1.2/provenance), [Build Requirements](https://slsa.dev/spec/v1.2/build-requirements), and [Verifying Artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts), approved specification. Retrieved 2026-09-06.
4. DORA, [Continuous Delivery](https://dora.dev/capabilities/continuous-delivery/), current research-based capability guidance. Retrieved 2026-09-06.
5. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, deployment-pipeline and feedback foundations.
6. Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, test-result trustworthiness and diagnostic foundations.

## Exercises

### Exercise 1

Define claim, evidence, predicate, pass, fail, incomplete, and waiver. Explain why a waiver does not turn a false claim true.

### Exercise 2

A gate requires passing tests, zero critical findings, and provenance no older than 24 hours. Tests pass; critical count is zero; provenance is 30 hours old. Derive the outcome. Repeat when the critical count is one and provenance is missing.

### Exercise 3

A repository requires status `quality`, accepts it from any writer, keys it only by branch name, and lets candidate code edit thresholds. Diagnose the trust failures and design minimum corrections.

### Exercise 4

Design gates for a low-risk documentation site and a payment authorization service. Define common minimum controls, risk-specific claims, evidence, thresholds, latency targets, and waiver authorities without using one undifferentiated score.

### Exercise 5

A coverage gate causes many blocks, suppressions are rising, and teams report slower delivery. Design an evaluation that determines whether to retain, modify, replace, or remove the gate while protecting against false acceptance.

## Answers to the Exercises

### Answer 1

A claim is a precise property about a subject. Evidence is an observation or attestation relevant to it. A predicate evaluates accepted evidence as true, false, or unknown under policy. Pass means all mandatory predicates are true; fail means at least one is false; incomplete means no mandatory predicate is false but at least one lacks an accepted truth value. A waiver is an authorized, scoped, expiring policy exception. It permits a decision despite fail or incomplete while preserving that underlying outcome, so it cannot honestly relabel the claim true.

### Answer 2

With passing tests and zero critical findings, those two predicates are true. Thirty-hour provenance violates the 24-hour freshness predicate, so the gate fails if stale is defined as false, or is incomplete if policy models currency as unavailable acceptable evidence; the policy must choose and diagnose consistently. This chapter's model classifies stale evidence as incomplete, so the result is incomplete. With one critical finding, a mandatory predicate is false, so the aggregate is fail even if provenance is missing. The record still reports provenance unknown; the known false takes decision precedence without erasing other state.

### Answer 3

A status name does not identify subject, method, or producer. Any writer can forge approval; a moving branch can associate old evidence with new content; candidate code can lower the rule that judges itself. Require an authenticated expected producer, immutable revision or artifact-digest binding, structured evidence containing tool and configuration versions, and policy stored behind independent review and protection. Record the evaluated policy digest and reject missing, malformed, stale, wrong-subject, or wrong-issuer evidence as incomplete. Test both the policy and enforcement path.

### Answer 4

Common minimums can include exact subject identity, successful deterministic build, required tests, dependency inventory, no exposed secrets, authenticated evidence, and an audited waiver process. The documentation site may require link, rendering, accessibility, and content-security checks with fast automated latency and a content-owner waiver for bounded non-security issues. The payment service adds transaction invariants, authorization tests, supported-database migrations, high-severity vulnerability and dependency limits, artifact provenance verification, performance objectives under defined load, separation-of-duty review, and production-readiness evidence. Its security owner and service risk owner authorize narrow waivers; critical authentication or integrity claims may be non-waivable. Each predicate reports separately. Targets derive from risk and measured capability, not an averaged quality score.

### Answer 5

First reconstruct the gate contract: intended claim, coverage definition, threshold origin, subject, and known limitations. Correlate blocks and accepted changes with mutation results, escaped defects, review findings, change type, test quality, suppression volume, and remediation time. Seed untested and weak-oracle mutations to see whether the gate detects relevant risk. Sample cases just below and above the threshold for semantic review. Measure queue and feedback percentiles, false rejections, workarounds, and risk by subsystem. Retain the gate if it adds timely, actionable detection; change it to risk-tiered or changed-code rules if the universal threshold is the defect; replace it with stronger mutation, requirement, or critical-path evidence if coverage is a poor proxy; remove it only with documented replacement or accepted risk. Run the revised rule advisory on historical and live samples before hard enforcement, and keep exact outcome audit data.
