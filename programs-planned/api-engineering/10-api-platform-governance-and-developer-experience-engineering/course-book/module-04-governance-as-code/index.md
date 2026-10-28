# Module 04 — Governance as Code, Evidence, Scorecards, and Exceptions

> **Program stage:** Course 10 of 10 — Operate APIs as an organizational platform.

> **Central question:** How can governance scale without becoming either a rubber stamp or a centralized release bottleneck?

## Where this module fits

Module 03 produced **Register the four inherited interface releases by digest and publication evidence**. This module extends that result by asking: **How can governance scale without becoming either a rubber stamp or a centralized release bottleneck?**

The new capstone increment is **Publish the policy pack, evidence ledger, exception register, and release scorecards**. It becomes the prerequisite for **Lifecycle, Compatibility, Deprecation, and Retirement**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Design deterministic policy rules around authoritative evidence.
- Preserve pass, review, and fail semantics.
- Build evidence-backed scorecards without vanity averages.
- Model temporary exceptions and compensating controls.
- Federate policy ownership across platform and domain teams.

## Capstone increment

Publish the policy pack, evidence ledger, exception register, and release scorecards.

## Governance is a decision system

Governance should protect organization-wide invariants while allowing domains to move independently. It needs a policy contract: inputs, rule version, evidence, outcome, owner, and escalation. A style guide alone is advice; a portal badge alone is presentation; a committee calendar alone is coordination. A decision system connects evidence to release and lifecycle actions.

## Pass, review, and fail

The capstone uses three outcomes. `pass` means automatic rules are satisfied. `fail` means a non-negotiable blocker such as missing ownership, mutable release bytes, or unsafe retirement. `review` means the machine has found an allowed but contextual condition: an expiring exception, an additive enum with strict consumers, or a protocol-specific documentation alternative.

This model prevents two common errors. First, a numeric score cannot average a critical failure into apparent health. Second, uncertainty is not silently converted into approval. Review names the human decision still required.

## Rule design

Automate facts that are authoritative and deterministic: owner exists, digest matches, evidence file exists and is fresh, deprecation has a consumer inventory, SDK publication has a provenance subject. Avoid pretending that a parser can decide whether a service boundary is organizationally justified or a migration guide is genuinely usable. Those need structured human review with visible criteria.

## Evidence ledger

Each evidence record has a subject, kind, status, source, collection time, expiry, and evidence class. Scorecards are projections over this ledger. The ledger remains the auditable source; the scorecard is a decision view. When an evidence item expires, the projection changes even if the API contract did not.

## Exceptions are bounded objects

A valid exception names the rule, subject, owner, reason, compensating control, approver, creation time, expiry, and status. The Course 10 RPC example has no browser-based interactive sample because bidirectional worker streams are not naturally exercised that way. The exception requires checked grpcurl and client transcripts instead and expires for review. “Not applicable” without a reason and alternative evidence is not an exception model.

## Scorecards without gamification

The capstone scorecard reports dimensions and blockers. It deliberately avoids a single 87/100. One team cannot compensate for missing security evidence by writing extra documentation. A scorecard should answer: Can this API advance? What evidence is missing? Who acts next? When does the evidence expire? It should not rank teams for managerial theater.

## Federated policy

Organization-wide rules cover ownership, immutable releases, incident contact, and supply-chain evidence. Protocol owners contribute specialized compatibility checks. Domain teams may add business constraints. The platform provides execution, schemas, evidence storage, and exception workflow. This division allows local expertise without each team inventing a different governance mechanism.

## Worked release review

Analysis RPC API lacks a browser console example. `DOC-002` would normally be major. The owner provides a scoped exception with tested client transcripts and an expiry. The resulting platform decision is `review`, not `pass`. A reviewer confirms that the alternative meets the consumer need. If the exception expires, the scorecard returns to review or failure.

## Implementation review

The policy core evaluates findings in severity order. The first blocker failure determines rejection. Exception validation is separate and requires scope and expiry. The scorecard projects evidence by dimension and preserves blocker identity.

## Policy architecture

Separate policy into layers:

1. **Input adapters** read catalog, registry, evidence, lifecycle, and runtime
   facts.
2. **Pure rules** evaluate one versioned condition against explicit inputs.
3. **Decision aggregation** preserves blocker, review, and pass semantics.
4. **Exception processing** applies only valid grants to matching subjects and
   rules.
5. **Workflow** routes failures, reviews, approvals, and expiry notifications.
6. **Presentation** renders scorecards and remediation guidance.

This separation prevents a user interface from becoming the only place where a
rule exists. It also permits the same policy to run in pull requests, release
pipelines, scheduled freshness checks, and lifecycle reviews.

## Rule contract

A good rule declares:

- stable ID and version;
- purpose and protected invariant;
- subjects and lifecycle states in scope;
- authoritative inputs;
- deterministic result or review trigger;
- severity and release consequence;
- remediation guidance;
- known false-positive and false-negative boundaries;
- owner and review cadence.

`CAT-001` protects accountable ownership. `REG-001` protects immutable releases.
`LFC-002` protects active consumers from unsafe retirement. These rules have
clear machine inputs. “Architecture is good” does not and therefore belongs in a
structured human review, not a boolean parser.

## Evidence freshness and invalidation

Evidence can become invalid because time passes, the subject changes, or the
verifier changes. Bind evidence to a subject digest or entity revision. A
security test for API 1.1 should not automatically satisfy API 1.2. Reliability
evidence can remain relevant across a documentation-only contract release if the
runtime subject is unchanged, but that reuse should be explicit.

When a tool discovers a defect in its own validator, invalidate affected evidence
and rerun. Governance must support evidence revocation, not only creation.

## Exception lifecycle

An exception workflow includes request, review, approval, active monitoring,
expiry warning, renewal or closure, and retrospective. Renewal is not automatic.
Repeated renewal can mean the rule is wrong, the paved path is incomplete, or
the owner is avoiding work. The platform product review should analyze exception
patterns.

Compensating controls need proof. If an API lacks an interactive browser example,
checked client transcripts can compensate. “Team will manually test” without a
repeatable artifact is weak.

## Scorecard design

A scorecard should show:

- subject and release;
- dimension status;
- blocker list;
- evidence age and source;
- active exceptions and expiry;
- owner and next action;
- trend where it supports a decision.

Avoid team rankings and one total score. If leadership needs portfolio views,
aggregate counts of blocked, review, expired, and stale evidence without
pretending a 94 is objectively better than a 91 across unlike APIs.

## Feedback quality

A failed rule should explain what was inspected, why it failed, how to reproduce,
and the smallest valid remediation. “Policy check failed” creates support load
and encourages bypass. Early feedback in the owner workflow is more valuable
than a final release-board rejection.

## Governance performance

Measure governance itself:

- time from candidate to decision;
- percentage resolved automatically;
- review queue age;
- repeated failure categories;
- exception count and expiry compliance;
- false-positive appeals;
- late defects that policy should have caught.

If review latency grows while risk does not change, improve delegation,
automation, or rule clarity. Governance is an operable service, not a timeless
set of commandments.

## Example rule evaluation

Consider an active API candidate:

- owner exists — pass;
- immutable digest — pass;
- compatibility report — pass;
- security evidence expired yesterday — fail/blocker;
- documentation complete — pass;
- sandbox available — pass.

A weighted score might produce 83 percent and a green threshold. The course
returns `fail` because active publication would rely on stale security evidence.
The result names `SEC-001`, the expired item, owner, and remediation. This is the
practical reason to preserve categorical decisions.

## Policy changes as releases

A policy-pack change can block many teams at once. Treat it as a release:

```text
proposal
→ impact simulation against current portfolio
→ false-positive review
→ documentation and remediation path
→ staged warning mode
→ enforcement date
→ exception migration
→ operational monitoring
```

Immediate enforcement is justified only for urgent risk and still needs incident
or risk authority. Run historical portfolio data against the candidate pack to
estimate impact before rollout.

## Human review quality

A review form should present the subject, exact automated findings, consumer
impact, precedent, residual risk, and proposed decision. Avoid asking reviewers
to rediscover evidence across ten tools. Record the rationale and expiry of
conditions. Reviewers should be selected by decision authority, not merely by
availability.

Calibrate reviewers with example cases and periodic retrospective. If similar
cases receive different outcomes, clarify policy or delegation. Consistency does
not mean ignoring context; it means differences are explainable.

## Appeal and correction

Owners need a way to challenge wrong metadata or a bad rule. An appeal should
pause only the disputed consequence, preserve audit, and identify who resolves
it. Repeated successful appeals indicate a policy or input-quality problem. A
platform that offers no correction path encourages teams to bypass it.

## Governance security

Protect policy repositories, exception approvals, and evidence stores. An
attacker who can create a fake exception or overwrite evidence can bypass every
API control without touching service code. Apply access control, review,
immutable history, and audit to governance artifacts themselves.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## Decision semantics

Governance automation needs more than pass and fail. The capstone uses four
evidence states: `pass`, `review`, `fail`, and `not-executed`. A blocker failure
rejects the release. A review state identifies a decision that automation cannot
make safely. `not-executed` is not a weak pass; it exposes an evidence gap and
policy decides whether that gap blocks the requested lifecycle state.

Do not average dimensions. Ownership, compatibility, security, and reliability
are non-compensable for an active release. Perfect documentation does not offset
an authorization defect. A scorecard is a structured view over dimensions and
blockers, not a grade that permits compensation. Numeric summaries may help a
portfolio owner find patterns, but release decisions retain categorical gates.

## Evidence quality

An evidence record should state the claim, subject, producer, collection time,
expiry, source, and result. Freshness depends on the claim. A contract digest is
stable for immutable bytes. A vulnerability scan, load result, owner mapping, or
runbook exercise becomes stale. Expiry is therefore not paperwork; it expresses
how long the evidence remains a reasonable basis for action.

Evidence should be reproducible where possible. Link the exact contract digest,
tool version, configuration, fixture, and report. When a check is
environment-backed, state what was not executed. “Pipeline green” is not a
portable evidence record because the pipeline definition and inputs can change.

## Exception discipline

An exception is a time-bounded decision to accept a named residual risk. It
requires the rule, subject, reason, owner, approver, compensating control,
creation time, expiry, and closure path. The Course 10 RPC documentation
exception is valid because an interactive browser example is inappropriate for
a bidirectional worker stream; checked command-line and Python transcripts are
the compensating evidence. The exception does not remove all documentation
requirements and it expires.

An exception without expiry becomes an alternative policy. Repeated exceptions
for the same condition indicate one of three things: the rule is wrong, the
paved road is missing a capability, or teams are avoiding necessary work. The
platform product review must decide which, rather than automatically renewing.

## Policy rollout

New policies should begin in observation mode against a representative
portfolio. Measure false positives, missing metadata, remediation cost, and
owner understanding. Then introduce warning, review, and blocker phases with a
published effective date. Emergency blocker rules are justified for immediate
organization-wide risk, but still require clear remediation and ownership.

Policy changes are contracts with API owners. Version the policy pack, publish a
changelog, test it against known fixtures, and provide a way to reproduce the
decision locally. A centralized rule that changes unpredictably creates release
instability. Governance as code is valuable because it can be reviewed and
replayed, not because code is automatically objective.

## Implementation drill: categorical blockers

A scorecard may summarize dimensions, but a blocker cannot be averaged away.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Finding:
    severity: str
    status: str


def policy_decision(findings: list[Finding]) -> str:
    if any(x.severity == "blocker" and x.status == "fail" for x in findings):
        return "fail"
    if any(x.status in {"review", "not-executed"} for x in findings):
        return "review"
    return "pass"
```

```typescript
interface Finding {
  severity: "blocker" | "major" | "minor";
  status: "pass" | "review" | "fail" | "not-executed";
}

function policyDecision(findings: Finding[]): string {
  if (findings.some(x => x.severity === "blocker" && x.status === "fail")) {
    return "fail";
  }
  if (findings.some(x => ["review", "not-executed"].includes(x.status))) {
    return "review";
  }
  return "pass";
}
```

The next step is not to assign weights. It is to attach each finding to a
subject, rule, fresh evidence record, remediation, and—where allowed—an expiring
exception.

## Module synthesis

You are ready to leave this module when you can **design deterministic policy rules around authoritative evidence, preserve pass, review, and fail semantics, and build evidence-backed scorecards without vanity averages** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **The first passes, the second requires review, the security failure rejects, and the expiry-free exception is invalid.**

The cumulative platform now includes **Publish the policy pack, evidence ledger, exception register, and release scorecards**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Lifecycle, Compatibility, Deprecation, and Retirement](../module-05-lifecycle-deprecation-and-retirement/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
