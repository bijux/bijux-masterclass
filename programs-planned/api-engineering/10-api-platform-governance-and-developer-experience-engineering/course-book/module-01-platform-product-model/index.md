# Platform Product Model and Operating Boundaries

**Module 01 of 10**

> **Governing question:** Which recurring problems should an API platform own, and which decisions must stay with domain teams?

## Place in the program

Courses 1–9 optimized individual interfaces and services. Course 10 begins by treating the platform itself as a product with users, outcomes, boundaries, and operating cost.

## Learning outcomes

- define the platform as a product with distinct users
- separate essential domain decisions from accidental repeated work
- establish platform, domain, and governance ownership
- evaluate paved roads and justified exceptions
- choose outcome metrics instead of feature counts

## Capstone result

Publish the platform product charter, user journeys, ownership boundary, and initial outcome model.

## A platform is a product, not a tool collection

An API platform coordinates repeated work across teams. Its product surface may include a catalog, registry, portal, templates, SDKs, gateways, and policy engines, but those are means. The product promise is that a consumer can find and trust an interface, while an owner can publish and evolve it without recreating the same controls. Starting from a vendor feature list reverses causality: the organization adapts its work to tools before deciding which problem deserves central support.

Analysis API Platform 1.0 begins with four user journeys: discover an API, publish a release, onboard a consumer, and deprecate a version. Every capstone mechanism must improve one of these journeys or protect an invariant established in earlier courses.

## Users and jobs to be done

Consumers ask: Which interface solves my problem? Who owns it? Which version is active? How do I authenticate? How can I try it safely? Owners ask: How do I publish? Which evidence is missing? Who consumes the old version? Reviewers ask: Which automated rule failed, what exception exists, and who accepted residual risk? Operators ask: Which runtime route implements this release, which team responds, and what happens when catalog and runtime diverge?

These are different users. A single “developer” persona hides conflicting needs. A policy reviewer needs traceability; a new consumer needs a minimal successful path; an API owner needs fast feedback. The platform must serve each without forcing everyone through the same screen.

## Essential decisions versus accidental work

The platform should remove accidental work: copying CI, inventing metadata, guessing owners, hand-writing package publication, finding support contacts, or rebuilding sandbox setup. It must not remove essential decisions: service ownership, public semantics, authorization, compatibility, reliability objectives, or retirement risk. Golden paths encode defaults, but the owner still declares why an API exists and what it promises.

## Platform boundaries

The API platform team owns the catalog schema, release registry, policy engine, lifecycle workflow, templates, portal, sandbox control plane, artifact publication, and platform support. Domain teams own their contracts, business facts, authorization decisions, operational objectives, and consumer commitments. Governance bodies own organization-wide invariants and risk acceptance. This three-way model prevents both an unaccountable free-for-all and a central architecture board that becomes the release bottleneck.

## Outcome metrics

Measure time from discovery to first successful sandbox use, publication lead time, percentage of active APIs with valid ownership, percentage of deprecated traffic, failed support handoffs, and expired exceptions. Page views, catalog entity counts, and template executions are inputs, not proof of value. A thousand registered APIs with unknown owners is worse than a smaller trustworthy inventory.

## Worked capstone decision

A request proposes that the platform gateway decide whether a user owns a project. It would reduce one network call, but it duplicates domain policy, introduces stale authorization state, and makes the gateway a business owner. The platform rejects the feature. It may authenticate the caller and route to Analysis Control; ownership remains with the service. By contrast, central digest verification for contract artifacts is accepted because the rule is protocol-independent, repeated, and does not change business meaning.

## Python and TypeScript implications

Both tracks expose a release decision as explicit inputs rather than as a portal button. The implementation is intentionally small: catalog validity, registry validity, policy decision, lifecycle safety, documentation, SDK traceability, runtime boundary, and sandbox safety. This makes the product contract visible and testable before any user interface is attached.

## Standards anchors

Backstage describes a software catalog as a centralized inventory of software and ownership metadata, and models APIs as first-class boundaries. The course adopts those useful ideas without claiming that the dependency-light catalog core is Backstage itself. Read the official [Software Catalog](https://backstage.io/docs/features/software-catalog/) and [system model](https://backstage.io/docs/features/software-catalog/system-model/) after you understand the product boundary.


## Write a platform product charter

A useful charter fits on one page and answers seven questions:

1. Which users does the platform serve?
2. Which repeated problems are expensive or risky today?
3. Which outcomes should improve?
4. Which capabilities does the platform own?
5. Which domain decisions remain explicitly outside its authority?
6. How is the platform funded, operated, and supported?
7. Which evidence would justify changing or retiring a capability?

For Analysis API Platform 1.0, the primary problems are fragmented discovery,
repeated publication machinery, untraceable lifecycle decisions, slow onboarding,
and inconsistent support routing. The charter does not promise to “standardize
all APIs.” It promises to standardize the machinery around trustworthy API
ownership while preserving protocol and domain differences.

## Map the current value stream

Trace a real owner journey before designing a platform feature:

```text
idea
→ find an owner and system
→ choose an interface
→ create a contract
→ collect compatibility/security/reliability evidence
→ publish docs and client assets
→ obtain review
→ deploy
→ register consumers
→ support and evolve
```

At each step record elapsed time, active work, waiting, handoffs, rework, and
failure. A portal may reduce search time but do nothing for a two-week review
queue caused by missing evidence. A template may reduce initial setup while
creating later upgrade debt. Value-stream evidence prevents local optimization.

Do the same for a consumer journey:

```text
express need
→ discover candidate APIs
→ compare ownership and lifecycle
→ obtain access
→ try safely
→ integrate
→ receive change notices
→ get support
```

The platform must improve both sides. A publication workflow that is convenient
for owners but hides breaking changes from consumers is not successful.

## Platform capability decision matrix

Evaluate a proposed shared capability across these dimensions:

| Dimension | Question |
|---|---|
| Recurrence | Do multiple teams repeat the work? |
| Invariance | Is there an organization-wide guarantee? |
| Authority | Can the platform act without owning domain meaning? |
| Economies of scale | Does central operation materially reduce cost or risk? |
| Variability | How much legitimate domain variation exists? |
| Supportability | Can the platform team operate and evolve it? |
| Exit | Can users migrate if the capability is retired? |

Contract digest verification scores high on recurrence, invariance, and
central economies. Domain authorization scores low on platform authority and
high on legitimate variation. This matrix turns “platform or team?” into a
reasoned decision.

## Paved road maturity

A paved road can mature through four levels:

1. **Documented:** a recommended process exists.
2. **Automated:** repeated steps are executable.
3. **Observable:** outcomes and failure reasons are measured.
4. **Adaptive:** evidence changes defaults and roadmap.

Do not jump directly to enforcement. A poorly understood process automated at
scale produces faster mistakes. Course 10 first makes rules and evidence
explicit, then adds templates and gates.

## Operating cost and support promise

Every platform capability adds dependencies, upgrades, security surface,
telemetry, incident response, and user support. Record an operating owner and a
support class before adopting it. A feature with no support promise becomes an
organizational trap: teams rely on it while nobody is responsible for failure.

A platform roadmap should include removal. If an integration has low use, high
maintenance, and a viable alternative, retire it through the same lifecycle the
platform requires of API owners. “Platform” is not an exemption from product
discipline.

## Product review questions

At a quarterly platform review, ask:

- Did median time to first success improve for a representative consumer?
- Which release failures were caught early, and which produced late rework?
- Which exceptions recur and therefore signal a missing paved path or a bad rule?
- Which support tickets bounced because ownership was unclear?
- Which capabilities have no active users or no operating evidence?
- Did domain teams retain authority, or did the platform quietly absorb business
  decisions?

These questions lead to product action. “We registered 200 APIs” does not.


## Case study: the rejected universal gateway

A leadership proposal asks the API Platform team to make one gateway endpoint
for all project, artifact, event, RPC, and graph interactions. The stated goal is
“one place for developers.” Evaluate it against the capability matrix.

Recurrence and discoverability are real. Yet the gateway would need to own
protocol translation, domain authorization, long-running state, event retention,
stream flow control, and GraphQL composition. It would become a new distributed
monolith and a bottleneck for every owner. The platform should instead provide a
single discovery and onboarding experience while preserving native interface
endpoints. One front door for information does not require one runtime path for
all semantics.

## Product hypothesis format

Write platform work as a testable hypothesis:

> For **new Analysis API consumers** who currently spend time finding owners and
> credentials, a **catalog-linked sandbox quickstart** will reduce **median time
> to first successful workflow** from the observed baseline, while preserving
> tenant isolation and support ownership.

The hypothesis names user, problem, intervention, outcome, and guardrails. It can
fail. “Build a portal” cannot.

## Platform responsibility map

Use four categories:

- **Own:** catalog schema, registry API, template releases, platform SLOs.
- **Enable:** domain contract checks, documentation publication, SDK pipelines.
- **Verify:** ownership, evidence freshness, release digest, retirement inputs.
- **Observe only:** domain business state, consumer business value, service
  implementation details not needed for platform decisions.

This map prevents “enable” from slowly becoming “own.” Revisit it whenever a
support escalation or automation proposal crosses a boundary.

## Decision review checklist

Before adding a capability, ask:

1. Is the user problem observed more than once?
2. Is the proposed central mechanism more reliable than team-local solutions?
3. Does it require domain data or decisions the platform cannot authoritatively
   hold?
4. Can the platform support it for years, including upgrades and incidents?
5. What happens to existing users if the capability is removed?
6. What metric can worsen even if usage rises?
7. Is a simpler documentation or policy improvement enough?

A mature platform says no frequently. Scope is a reliability control.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## Worked product charter: Analysis API Platform 1.0

The capstone charter can be expressed without naming a vendor. Its users are API
consumers, API owners, reviewers, operators, and platform maintainers. Its first
four critical journeys are discovery, publication, onboarding, and retirement.
Its non-negotiable boundaries are that domain teams retain contract semantics,
business authorization, service objectives, and business-state repair. The
platform owns repeated organizational mechanisms around those facts.

A useful charter also names what the platform will not optimize. Analysis API
Platform 1.0 does not maximize the number of registered entities, generated
repositories, or portal visits. It seeks to reduce time to a trustworthy first
success, reduce repeated release work, increase the proportion of releases with
fresh evidence, and reduce unsafe deprecated use. These measures can still be
gamed, so they are reviewed together. A low onboarding time achieved by issuing
overpowered credentials is not success. A high adoption count achieved by
mandating registration without useful workflows is not product value.

## Capability economics

Every proposed platform capability creates three costs:

1. **build cost** — design, implementation, migration, and documentation;
2. **operating cost** — availability, upgrades, support, security, and data
   stewardship;
3. **coordination cost** — rules, ownership, review, and integration work imposed
   on teams.

Compare those costs with repeated organizational waste. Contract digest
publication is a good central capability because every team needs the same
immutable-release property and central operation is bounded. Project-owner
authorization is a poor platform capability because the meaning changes with
domain state and would force the platform into every business transaction.
Search is a platform capability because it projects published documentation;
domain-state repair is not because it mutates authoritative service facts.

A proposal should answer: How often does the problem occur? How many teams bear
it? Is the required decision generic or domain-specific? Can the capability be
operated with a clear service level? What happens when it is unavailable? Is
there a safe escape route? A capability without an owner, cost estimate, user
journey, and falsifiable outcome remains an idea, not a platform commitment.

## Choosing a paved road

A paved road combines defaults, maintained integration, and evidence. It should
be easier than assembling the same controls independently. It should also expose
its seams. The golden path creates metadata, docs, tests, and policy hooks, but
it cannot decide resource semantics or acceptable risk. Teams may leave the
road when a real architectural need exists, provided they preserve the
organization-wide invariants and accept the support cost.

The platform product owner reviews adoption as a portfolio. If teams repeatedly
leave at the same point, the paved road may be wrong. If one team leaves because
its protocol is genuinely different, an exception may be enough. If every
special case becomes a permanent supported path, the platform becomes a tool
museum. Product maturity is the ability to say both “this repeated work belongs
here” and “this decision must remain local.”

## Implementation drill: reject capability-shaped centralization

A product boundary can be made executable before a tool is selected. This
minimal decision function rejects proposals that require the platform to own
business state and requires a user outcome and operating owner for everything it
accepts.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CapabilityProposal:
    name: str
    repeated_problem: bool
    owns_business_state: bool
    operating_owner: str | None
    outcome_metric: str | None

def decide(proposal: CapabilityProposal) -> str:
    if proposal.owns_business_state:
        return "reject-domain-authority"
    if not proposal.repeated_problem:
        return "reject-insufficient-reuse"
    if not proposal.operating_owner or not proposal.outcome_metric:
        return "incomplete-proposal"
    return "candidate-platform-capability"
```

```typescript
interface CapabilityProposal {
  name: string;
  repeatedProblem: boolean;
  ownsBusinessState: boolean;
  operatingOwner?: string;
  outcomeMetric?: string;
}

function decide(proposal: CapabilityProposal): string {
  if (proposal.ownsBusinessState) return "reject-domain-authority";
  if (!proposal.repeatedProblem) return "reject-insufficient-reuse";
  if (!proposal.operatingOwner || !proposal.outcomeMetric) {
    return "incomplete-proposal";
  }
  return "candidate-platform-capability";
}
```

The function is intentionally not a product roadmap algorithm. It encodes only
objective incompleteness and one authority boundary. Human product judgment
still decides whether the recurring problem is valuable enough to operate.
