# Lifecycle, Compatibility, Deprecation, and Retirement

**Module 05 of 10**

> **Governing question:** How can an API evolve and eventually disappear without transferring hidden cost to consumers?

## Place in the program

Module 04 established release decisions. Module 05 governs an API across time, including the most neglected part of the lifecycle: safe removal.

## Learning outcomes

- model lifecycle as evidence-gated transitions
- build a multi-source consumer inventory
- design migration and notice workflows
- block unsafe retirement
- preserve historical contract truth

## Capstone result

Publish the lifecycle policy, consumer inventory, deprecation impact report, and retirement decision.

## Lifecycle is a state machine

The capstone defines `proposed`, `experimental`, `active`, `deprecated`, and `retired`. Each transition has required evidence. A proposed API needs an owner and contract before experiment. Active publication requires compatibility, security, reliability, documentation, and support evidence. Deprecation requires a replacement or exit plan, consumer inventory, migration guide, and notice end. Retirement requires zero blocking consumers, approval, runtime removal, and archival plan.

## Deprecation is a consumer program

Adding `deprecated: true` or `@deprecated` is useful communication but insufficient governance. The owner must identify consumers, explain the replacement, publish a timeline, support migration, measure old-version use, and make impact visible. The platform coordinates this workflow and preserves evidence; it does not decide that a consumer’s business risk is irrelevant.

## Consumer inventory

A consumer record identifies owner, API, version, environment, criticality, contact, last seen, and migration status. Registration alone can be stale. Runtime telemetry alone can miss dormant or offline use. Package download counts do not identify deployment. Use multiple evidence sources and expose uncertainty.

The capstone has a legacy CLI on Analysis HTTP API 1.1. It is active in production and migration is scheduled, so retirement remains blocked even though API 1.2 has been available for months.

## Notice and compatibility

Notice begins only when consumers have a usable migration route. A long notice with no replacement documentation is delay, not support. A shorter notice can be adequate for a low-criticality experimental API with no consumers. The policy sets a minimum baseline, while criticality and contractual commitments can require more.

## Retirement sequence

A safe sequence is: stop new adoption, announce deprecation, publish migration material, track consumers, provide parallel operation, reduce old-version traffic, confirm blockers, freeze changes, remove runtime routes, monitor failures, and archive artifacts and evidence. Rollback remains possible until the runtime removal and data changes become irreversible.

## Emergency change

A severe security issue may make continued operation riskier than rapid removal. Emergency policy still requires an incident record, affected-consumer analysis, approved risk decision, containment path, and communication. “Security” is not a magic word that bypasses accountability.

## Historical truth

Retired contracts, docs, changelogs, SDK versions, and migration records remain discoverable as historical artifacts. A consumer debugging an old event or audit record needs the semantics that existed then. The catalog marks retired state; the registry preserves identity.

## Worked decision

The lifecycle engine evaluates Analysis HTTP 1.1. Required retirement documents exist, but one blocking consumer remains. The result is `blocked`. A committee cannot override the machine by changing the status field; it must resolve the consumer, approve an explicit exception, or accept emergency risk through the designated path.

## Implementation review

`evaluate_transition` checks allowed edges and required evidence. `deprecation_impact` calculates affected and blocking consumers from the inventory. These functions are intentionally separate: lifecycle policy defines what is required, while consumer data supplies current impact.


## Lifecycle records as products

A lifecycle record should be machine-readable and human-understandable. For a
deprecation, record:

```text
API and version
owner and approver
replacement or exit path
announcement date
minimum and contractual notice
consumer inventory snapshot
migration guide and test path
runtime traffic evidence
support commitment
planned route removal
archive and rollback plan
```

The snapshot matters. Consumer state can change after approval. Re-evaluate at
retirement rather than relying on a report from the announcement date.

## Discovering consumers

Use several methods:

- explicit subscription or registration;
- API keys, OAuth clients, service identities, and package telemetry;
- gateway and service traffic;
- broker consumer groups and RPC callers;
- support tickets and integration repositories;
- owner attestation for offline or seasonal use.

Each method has gaps. For privacy and cardinality reasons, not every runtime
request belongs in the platform catalog. Aggregate evidence while preserving an
accountable consumer identity for lifecycle communication.

## Migration campaigns

A migration campaign has cohorts, milestones, and escalation. Start with willing
low-risk consumers to validate guides and tooling. Address critical consumers
early because they may need longer lead time. Track states such as discovered,
contacted, planned, testing, complete, exception, and unknown.

The platform can generate reminders and dashboards, but the API owner answers
semantic questions and the consumer owner decides deployment timing. A migration
is a collaboration, not a broadcast email.

## Dual operation and behavioral evidence

During migration, run old and new versions in parallel when possible. Compare
contract tests, business outcomes, error rates, and performance. A consumer can
report “complete” only after production or representative evidence, not merely
a successful code generation. Keep rollback until irreversible data or routing
changes occur.

## Runtime removal

Retirement has multiple control planes:

- remove or reject gateway routes;
- disable broker publication or subscriptions according to event policy;
- stop RPC method serving or package resolution;
- remove GraphQL fields after compatibility gates;
- revoke credentials and environment access;
- update catalog lifecycle and active channels;
- retain registry artifacts and archival docs.

A lifecycle status update without runtime removal is false retirement. Runtime
removal without catalog history is undiscoverable breakage.

## Event and data retention

For event APIs, historical messages may outlive the producer contract release.
Retain schemas and upcasters for the retention period. For SDKs and generated
clients, retain packages needed for reproducible builds and incident analysis.
For public HTTP APIs, preserve old reference and migration pages even after
routes disappear.

## Retirement rollback

Define the last safe rollback point. Re-enabling a route may be easy; restoring a
removed database column or replaying discarded messages may not. A retirement
plan should distinguish reversible control-plane actions from irreversible data
changes. Delay irreversible changes until consumer and monitoring evidence is
strong.

## Lifecycle debt

APIs stuck indefinitely in experimental or deprecated states create platform
debt. Review them periodically. An experiment with production critical consumers
is mislabeled. A deprecated version with no migration effort is abandoned, not
governed. The platform should surface state age and require owner action.


## Interface-specific retirement concerns

**HTTP/OpenAPI:** preserve old documentation and SDKs; remove routes only after
consumer migration; decide error behavior for old paths.

**Events/AsyncAPI:** retained messages and replay may require old schemas long
after publication stops. Consumers can remain on an old event version even when
no new producers use it.

**gRPC/Protobuf:** removed fields and methods need reserved identifiers and wire
compatibility history. Old binaries may run without appearing in gateway logs.

**GraphQL:** field deprecation is discoverable through schema introspection, but
active persisted operations and unknown ad hoc clients still require analysis.
Removing a field can cause null or validation failure in composite workflows.

The platform lifecycle engine normalizes state and evidence while protocol
owners define these specialized obligations.

## Consumer communication record

For each affected consumer, record contact attempts, acknowledged plan, target
version, test status, production completion, and exception. Broadcast messages
are evidence of sending, not of receipt or migration. Critical consumers need an
owner-to-owner confirmation path.

Provide machine-readable notices through catalogs, SDK metadata, response
headers where appropriate, event or registry notifications, and portal alerts.
No one channel reaches every consumer.

## Unknown and shadow consumers

Unknown traffic can come from shared credentials, NAT, scripts, or unregistered
services. Improve identity before retirement. If uncertainty remains, decide
through explicit risk authority. Do not fabricate “zero consumers” by limiting
the query to registered records.

## Sunset behavior

Decide what an old consumer experiences after removal. Options include a clear
HTTP retirement response, broker rejection, RPC unimplemented status, or GraphQL
validation error. Preserve a stable support and migration link where protocol
allows. Silent connection reset or generic 500 wastes incident time.

## Post-retirement verification

After cutover:

- monitor old-route or old-version attempts;
- verify no shadow runtime remains;
- check support and incident volume;
- confirm new-version outcome and performance;
- preserve rollback within the declared window;
- close or investigate residual consumers;
- archive final evidence and approval.

Retirement is complete only after the system and consumers demonstrate the
expected state, not when a project ticket closes.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## Consumer inventory quality

Retirement depends on knowing who uses a version. No single discovery source is
complete. Explicit registrations provide ownership and criticality but can
become stale. Runtime observation reveals recent use but may miss batch jobs,
disaster-recovery clients, or environments outside the observation window.
Support records and package downloads are clues, not proof of active use.
Combine sources and attach confidence.

The capstone blocks retirement of `analysis-http@1.1.0` because
`consumer-legacy-cli` remains active and its migration is only scheduled. The
fact that the replacement has existed for months is irrelevant. The notice
period is a minimum, not a timer that authorizes breaking an identified
consumer.

## Deprecation as a managed migration

A deprecation record names the affected version, replacement or exit path,
behavioral differences, owner, notice dates, consumers, migration status,
support plan, runtime removal plan, and archive plan. Consumers need a way to
verify migration before production cutover. Owners need a feedback loop for
blocking defects in the replacement.

Track migration as states such as `uncontacted`, `acknowledged`, `planning`,
`testing`, `complete`, and `waived-with-risk-acceptance`. “Email sent” is not
migration. Critical consumers may need rehearsals, dual-read comparison, or
rollback plans. The platform coordinates evidence; each consumer and API owner
remain accountable for their work.

## Emergency change

A severe security incident can require a shorter path, but it does not erase
consumer impact. The emergency record should link the incident, compromised
behavior, affected consumers, containment options, approvers, residual risk, and
communication. Prefer scoped revocation, credential rotation, or feature
disabling over abrupt interface removal when those controls address the threat.
After the emergency, reconcile temporary routes and exceptions so they do not
become permanent undocumented behavior.

## Retirement mechanics

Retirement is more than changing a catalog label. Remove or disable runtime
routes, revoke publication and credential paths, freeze the final artifacts,
retain documentation and migration history, preserve audit evidence, and define
how late traffic is observed. A retired API should not vanish from history;
consumers and incident responders need to know what existed and why it ended.

If a request arrives after retirement, behavior must be intentional. A public
HTTP route might return a stable retirement problem with migration information
for a bounded period. An event consumer might be disabled after the retention
window. An SDK package may remain resolvable but deprecated and unsupported.
These choices belong in the lifecycle plan, not in an operator’s ad hoc response.

## Implementation drill: consumer-safe retirement

A completed notice period does not override known consumers.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RetirementDecision:
    allowed: bool
    reason: str


def retire(*, evidence: set[str], blocking_consumers: int) -> RetirementDecision:
    required = {
        "zeroBlockingConsumers",
        "retirementApproval",
        "runtimeRemovalPlan",
        "archivePlan",
    }
    missing = required - evidence
    if missing:
        return RetirementDecision(False, "missing-evidence")
    if blocking_consumers:
        return RetirementDecision(False, "blocking-consumers")
    return RetirementDecision(True, "allowed")
```

```typescript
interface RetirementDecision { allowed: boolean; reason: string; }

function retire(evidence: Set<string>, blockingConsumers: number): RetirementDecision {
  const required = [
    "zeroBlockingConsumers",
    "retirementApproval",
    "runtimeRemovalPlan",
    "archivePlan",
  ];
  if (required.some(item => !evidence.has(item))) {
    return { allowed: false, reason: "missing-evidence" };
  }
  if (blockingConsumers > 0) {
    return { allowed: false, reason: "blocking-consumers" };
  }
  return { allowed: true, reason: "allowed" };
}
```

In the capstone, the legacy CLI keeps the decision blocked. Removing it from the
inventory is not remediation; completing or explicitly waiving its migration is.
