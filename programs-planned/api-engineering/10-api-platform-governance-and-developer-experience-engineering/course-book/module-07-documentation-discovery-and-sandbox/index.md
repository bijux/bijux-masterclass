# Documentation, Discovery, Sandboxes, and Consumer Onboarding

**Module 07 of 10**

> **Governing question:** Can a new consumer find the right interface, trust it, and complete a useful workflow safely without private organizational knowledge?

## Place in the program

Module 06 created a safe starting point for owners. Module 07 serves consumers: discovery must lead to a successful and correctly understood interaction, not merely to a rendered reference page.

## Learning outcomes

- organize documentation around tasks and interface choice
- publish trustworthy discovery metadata
- build executable version-bound examples
- design isolated synthetic sandboxes
- measure onboarding outcomes and route support

## Capstone result

Publish the task-oriented portal source, search index, sandbox profile, and first-success evidence.

## Documentation is part of the interface product

Machine-readable contracts are essential, but consumers begin with a goal: submit an analysis, observe progress, download an artifact, or subscribe to completion. The portal should organize around those tasks and explain which interface fits. Protocol reference remains available after the reader has context.

The capstone documentation set includes overview, quickstart, task guides, interface selection, migration, and support. Each example declares the API reference, contract version, environment, language, and expected outcome.

## Discovery needs trust signals

A search result should show owner, lifecycle, active release, last evidence refresh, support route, and audience. A result without lifecycle may direct consumers to an experiment or deprecated API. A result without ownership may be impossible to support. Ranking purely by page views can amplify old or confusing content.

## Time to first success

Measure the interval from credential issue or onboarding start to a predefined successful workflow. The capstone records four minutes for the reference CLI. The metric is meaningful only when success is defined: a `202 Accepted` with a valid status monitor, not any HTTP response. Track failure reasons and abandonment so the platform can distinguish docs, credentials, sandbox, contract, and service problems.

## Sandboxes are security products

An isolated sandbox uses synthetic data, tenant-scoped state, short-lived credentials, quotas, deny-by-default egress, and deterministic reset. It must not share production data or secrets. The platform owns sandbox control; domain owners supply synthetic scenarios and behavior.

A sandbox that behaves nothing like production is misleading, but copying production is unsafe. Preserve public contract semantics and representative failure modes while substituting controlled data and dependencies.

## Examples as executable assets

Examples should run against the sandbox and fail when the contract changes. They need version identity, expected output class, and cleanup. Generated snippets without tests may be syntactically correct and semantically wrong—for example, retrying a non-idempotent command with a new key.

## Search and documentation quality

Track zero-result rate, repeated reformulation, selected result, task completion, and stale-version use. The capstone search fixture has one zero-result query out of four; that 25 percent is deliberately above the five-percent budget and creates a product backlog item. Page views alone would not reveal it.

## Support routing

Platform support handles portal, registry, template, sandbox, and publication failures. API owners handle semantics and domain behavior. Security and runtime incidents follow the escalation model from earlier courses. The catalog supplies ownership; support routes supply response expectations. A consumer should not need private organizational knowledge to find help.

## Worked onboarding

A consumer searches “submit analysis,” chooses Analysis HTTP API 1.2, reads the task guide, creates an isolated session, receives short-lived credentials, executes the example, and records first success. If the result is `409`, the guide explains idempotency conflict rather than treating it as generic failure. The portal measures the complete journey.

## Implementation review

The portal core builds a deterministic search index from Markdown and contract metadata. The sandbox core derives stable fixture identity, enforces synthetic-only data, and records expiry. These small mechanisms make discovery and isolation testable without pretending to be a complete commercial portal.

## Standards anchor

Backstage TechDocs follows a docs-like-code model that keeps Markdown near software and makes it discoverable with catalog entities. The course uses the same useful separation: owners maintain semantics near code; the platform publishes and searches. See [TechDocs](https://backstage.io/docs/features/techdocs/) and [creating and publishing docs](https://backstage.io/docs/features/techdocs/creating-and-publishing/).


## Information architecture

Organize the portal around questions:

- What can I accomplish?
- Which interface should I use?
- Is it active and supported?
- Who owns it?
- How do I authenticate and try it?
- What are the limits and failure modes?
- How do I migrate or get help?

Protocol and team filters are secondary. A consumer should not need to know that
“analysis completion” is an AsyncAPI operation name before discovering it.

## Documentation layers

A complete API product commonly needs:

1. **Overview:** purpose, audience, owner, lifecycle, boundaries.
2. **Concepts:** domain terms and interface-selection guidance.
3. **Quickstart:** smallest safe successful workflow.
4. **Task guides:** common end-to-end outcomes.
5. **Reference:** generated or authored protocol detail.
6. **Failure guide:** errors, retries, limits, and troubleshooting.
7. **Migration:** version and deprecation changes.
8. **Support:** contact, expected response, incident route.
9. **Changelog:** released behavior and evidence.

Generating reference from a contract is valuable but covers only layer five.

## Executable examples

An example record should bind:

```text
example ID
API and contract version
language and SDK version
authentication profile
sandbox environment
input fixture
expected status or message
important response assertions
cleanup
```

Run examples during release and periodically. If a sandbox change breaks them,
that is a platform incident or documentation defect. Store outputs carefully so
secrets and personal data never enter generated docs.

## Sandbox fidelity model

Decide which production properties the sandbox preserves:

- contract shape and validation;
- authentication and authorization semantics;
- idempotency and concurrency behavior;
- representative asynchronous delay and failure;
- rate and resource limits scaled for learning;
- synthetic data relationships.

Declare what differs: capacity, external delivery, retention, cost, and some
operational dependencies. A consumer should know which conclusions can transfer
to production.

## Credential lifecycle

Issue sandbox credentials for one user or automation identity, one tenant, one
audience, bounded scopes, and short expiry. Provide revocation and reset. Never
put a reusable token in documentation. The portal can automate issuance only
through the identity authority; it should not become an ungoverned identity
provider.

## Onboarding funnel

Instrument stages:

```text
discovered API
→ opened quickstart
→ requested sandbox
→ received credentials
→ sent first request/message
→ achieved defined success
→ integrated representative workflow
```

Count exits and failure categories. A consumer who cannot obtain credentials has
a different problem from one whose contract use fails. Product work should
address the largest meaningful bottleneck, not optimize the easiest page.

## Documentation ownership and review

Domain owners approve semantics and examples. Platform editors maintain
structure, publishing, search, accessibility, and common style. Consumer feedback
can open issues. For critical APIs, include a freshness review tied to each
release and a periodic task-run check.

## Search relevance and trust

Index titles, task vocabulary, protocol, owner, lifecycle, and released versions.
Down-rank deprecated content unless the query is migration-related. Show why a
result is recommended. A search system that sends new users to a retired version
because it has historical traffic undermines lifecycle governance.


## Interface-selection decision table

A consumer task may have several valid surfaces:

| Need | Prefer | Reason |
|---|---|---|
| Public project and run resources | HTTP/OpenAPI | Stable resource semantics and broad tooling |
| Durable completion integration | Events/AsyncAPI | Temporal decoupling and replay |
| Internal worker streaming | gRPC/Protobuf | Typed streaming, deadlines, cancellation |
| Client-shaped multi-service view | GraphQL | Governed selection and composition |

Document trade-offs and alternatives. Do not advertise GraphQL merely because a
client wants fewer HTTP calls, or events when the consumer needs an immediate
answer.

## Documentation tests

Automate:

- local and external link checks;
- code and command syntax;
- contract-version references;
- example execution against sandbox;
- expected status and body assertions;
- owner and lifecycle metadata;
- deprecation banners and replacement links;
- search indexing;
- secret and personal-data scans;
- reading-level or structure checks where useful.

Human review still verifies conceptual accuracy and task clarity. A syntactically
valid tutorial can teach an unsafe retry.

## Sandbox reset and determinism

A consumer should be able to recreate a known initial state. Provide fixture
version, reset operation, seed identity, and bounded asynchronous timing. If a
workflow depends on random data, record the seed. Cleanup must revoke credentials
and destroy tenant state even after failed experiments.

## Failure-mode onboarding

After the happy path, teach at least one expected failure: invalid token,
idempotency conflict, stale version, rate limit, unavailable dependency, or
subscription gap. Consumers who have never seen a controlled failure will build
poor retry and support behavior.

## Accessibility and international teams

Use clear headings, descriptive links, text alternatives, copyable code, and
consistent terminology. Avoid relying on color badges alone. Define domain terms
and timestamps precisely. A platform for a large organization must support
readers with different languages, accessibility needs, and levels of local
context.

## Feedback loop

Put feedback next to the task and API version. Route semantic feedback to the
owner and portal defects to the platform. Track whether feedback leads to changes
and whether the same confusion recurs. Documentation is maintained product code,
not a publication event at launch.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## Documentation architecture

Consumers need different document types. An overview explains purpose,
audience, owner, and boundaries. A quickstart reaches one smallest successful
outcome. Task guides solve recurring goals. Reference describes complete
contract details. Concepts explain models and trade-offs. Support and changelog
material explain what happens when the happy path ends or changes.

Reference alone is not onboarding. A rendered OpenAPI page may list every
operation yet leave a consumer unable to choose an interface, obtain safe
credentials, or interpret asynchronous completion. Conversely, a quickstart
without version-bound reference can succeed once and mislead later. The coverage
record links every active API product to all required document roles.

## Search quality

Search is a product surface. Index titles, task language, API names, protocol
terms, error codes, and common consumer vocabulary. Log queries, result count,
selection, and subsequent outcome without collecting sensitive payloads. A zero
result is useful evidence; repeated reformulation and rapid support escalation
also indicate failure.

The capstone preserves a baseline in which one of four queries returned no
result, then publishes an improved corpus with zero failures in the small
fixture. This is mechanism evidence, not a production claim. In a real platform,
measure a larger window, segment by user journey, inspect false positives, and
avoid optimizing search clicks without checking first success.

## Sandbox threat model

A sandbox is a controlled product environment, not a copy of production. It
uses synthetic data, short-lived credentials, bounded quotas, isolated tenants,
non-production endpoints, visible reset behavior, and no route to import
production records. Examples must be deterministic enough to teach while still
exercising real contract behavior.

Define expiry and cleanup. Abandoned sandboxes consume storage and credentials.
A reset should remove state without affecting other sessions. If outbound
webhooks or events are supported, route them to controlled receivers. The
sandbox should make dangerous capabilities obviously unavailable rather than
quietly simulating success.

## Time to first successful outcome

Measure from a meaningful start event—such as credential issuance or sandbox
creation—to a contract-valid successful workflow. Distinguish waiting on access,
reading, coding, and platform failure where possible. Median alone can hide a
long tail, but a single sample cannot support a percentile. Pair quantitative
data with support themes and failed tasks.

A fast first call is not enough if the consumer cannot reach production safely.
Track progression from discovery to sandbox success, integration test, approved
production credential, and stable use. The platform improves these stages while
the API owner preserves the semantics of the underlying capability.

## Implementation drill: isolated sandbox identity

A sandbox tenant is derived from a subject and nonce, but it is explicitly
classified as synthetic and expires.

```python
from datetime import datetime, timedelta
from hashlib import sha256


def sandbox(subject: str, nonce: str, now: datetime) -> dict[str, object]:
    digest = sha256(f"{subject}\\0{nonce}".encode()).hexdigest()[:16]
    return {
        "id": f"sbx-{digest}",
        "tenant": f"sandbox-{digest[:10]}",
        "dataClass": "synthetic-only",
        "expiresAt": now + timedelta(hours=2),
    }
```

```typescript
interface SandboxSession {
  id: string;
  tenant: string;
  dataClass: "synthetic-only";
  expiresAt: Date;
}

function sandboxFromDigest(digest: string, now: Date): SandboxSession {
  return {
    id: `sbx-${digest.slice(0, 16)}`,
    tenant: `sandbox-${digest.slice(0, 10)}`,
    dataClass: "synthetic-only",
    expiresAt: new Date(now.getTime() + 2 * 60 * 60 * 1000),
  };
}
```

The TypeScript course implementation computes the same SHA-256 digest. The
sandbox boundary also rejects production-data import, limits credentials, and
uses controlled endpoints. Identity alone is not isolation.
