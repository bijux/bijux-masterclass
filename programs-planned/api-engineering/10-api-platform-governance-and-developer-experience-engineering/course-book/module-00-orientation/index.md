# Orientation and the Platform Boundary

**Module 00 of 10**

> **Governing question:** What is Course 10 allowed to centralize, and what must remain with the API owners?

## Place in the program

Course 9 published the exact boundary that Course 10 is allowed to catalogue and govern. Orientation locks that boundary, establishes the language-track strategy, and distinguishes platform mechanisms from business ownership.

## Learning outcomes

- lock the exact Course 9 handoff
- identify the authority of every inherited interface
- choose a primary language track
- classify local, environment-backed, and operational evidence
- state the platform team’s allowed and forbidden responsibilities

## Capstone result

Verify the predecessor handoff and publish the initial platform-boundary statement.

## The platform boundary

The platform may make trusted API work easier. It may ingest metadata, publish immutable artifacts, run policy, generate documentation, issue sandbox sessions, and route support. It may not redefine project ownership, analysis state, artifact integrity, or notification delivery. If a portal becomes the only place where a business rule exists, the platform has stolen domain authority.

## Verify before extending

Run predecessor proof before modifying any capstone file. Then inspect the four contract releases copied from Courses 2, 6, 7, and 9. Their different formats are intentional. A platform registry must preserve protocol-specific evidence rather than flatten every contract into one lowest-common-denominator model.

## Evidence discipline

The course uses small executable cores so that catalog, policy, lifecycle, and publication decisions remain visible. Optional Backstage, gateway, and hosted-registry routes are integration exercises. The core is not advertised as a replacement product; it is the place where the learner can see the governing semantics without vendor internals.

## A reader-first route

Do not begin by exploring hundreds of capstone files. Start with the course book, then open only the implementation paths named by the chapter. The repository is organized to support reasoning, not to reward archaeology.


## The inherited version ledger

Course 10 does not begin from a blank repository. It inherits a public HTTP API,
an event API, an RPC API, and a GraphQL API, plus service, security, reliability,
and performance profiles. These versions belong to different axes. The platform
must preserve that distinction:

| Axis | Inherited value | Authority |
|---|---|---|
| Public Analysis HTTP API | 1.2 | Analysis Control owner |
| OpenAPI description format | 3.1.2 baseline | OpenAPI specification |
| Analysis Events API | 1.0 | Analysis Control owner |
| AsyncAPI format | 3.1.0 | AsyncAPI specification |
| Analysis RPC API | 1.0 | Analysis Control owner |
| Protobuf syntax/profile | proto3 baseline | Protobuf specification and owner policy |
| Analysis Graph API | 1.0 | Graph gateway and source owners |
| GraphQL specification | September 2025 | GraphQL specification |
| Platform profile | proposed 1.0 | API Platform team |

A common platform mistake is to display one field named `version` and thereby
mix all of these. A consumer asking for Graph API 1.0 does not mean GraphQL 1.0.
An SDK 1.2.1 does not imply HTTP API 1.2.1. The course registry and catalog use
explicit field names so a lifecycle action affects the correct subject.

## Inspect the boundary as a reviewer

Open the Course 9 boundary file before the GraphQL schema. It states what the
next course may and may not do. Then inspect field ownership, active persisted
operations, query budgets, and client records. This order matters. A platform
engineer who begins by parsing a schema can miss the organizational contract
around it.

Next inspect the actual HTTP, event, and RPC artifacts copied into the Course 10
contract directory. Their digests are computed from the original release bytes.
The course does not translate them into a new universal schema. A registry entry
points at a native artifact and records a normalized publication envelope around
it.

## Build an evidence map

For every platform claim, write four fields:

1. **Subject** — the entity, release, template, package, route, or consumer.
2. **Claim** — for example, “HTTP API 1.2 bytes are immutable.”
3. **Evidence** — digest record, compatibility report, test, runtime observation,
   or human approval.
4. **Evidence class** — course-executed, environment-backed, or operational.

This prevents a common substitution. A course-executed test can prove the local
registry rejects an overwrite. It cannot prove a cloud registry’s authorization
or durability until that environment is exercised. Conversely, an operational
screenshot cannot replace a deterministic test of the release invariant.

## Primary and comparative tracks

Implement the full laboratory in one language. In the comparative track, read
the API, run shared vectors, and review one mechanism where language design
changes the implementation. For example, Python’s dataclasses and TypeScript’s
structural types express catalog records differently, but both must reject the
same orphan API. This strategy develops transfer rather than duplicate typing.

## Orientation failure modes

- **Portal-first exploration:** browsing screens before learning authorities.
- **Version collapse:** treating API, format, package, and platform versions as
  one number.
- **Tool conformance inflation:** claiming a bounded parser proves full external
  specification compliance.
- **Handoff mutation:** “fixing” a predecessor contract inside the platform
  course instead of publishing a new owner-approved release.
- **Evidence laundering:** presenting a generated report as operational proof
  merely because its JSON shape looks formal.

The orientation checkpoint exists to catch these errors before the learner builds
anything on top of them.


## Orientation design review

Before moving on, perform a verbal boundary review using one sentence per layer:

- **Domain:** Analysis Control owns run truth and legal transitions.
- **Interface owner:** each HTTP, event, RPC, and graph release has named semantic
  authority.
- **Platform:** Course 10 indexes, verifies, publishes, and supports these
  releases.
- **Runtime:** gateways, brokers, servers, and registries expose approved
  subjects.
- **Consumer:** integrations choose and pin released subjects.

Now test the sentence “the platform owns the API.” It is too broad. The platform
may own the graph gateway or publication mechanism, while Analysis Control owns
the HTTP and event semantics. Always name the exact subject and responsibility.

Create a personal evidence notebook with one row for each course proof. Include
the command, subject, expected failure, and cleanup. This turns the course into a
repeatable learning system: when a proof fails, you can identify whether the
cause is contract, code, metadata, environment, or packaging rather than rerun
random commands.

Finally, decide what you will not learn through tool installation. Course 10 can
teach catalog and governance semantics without a large portal deployment. Once
the invariants are understood, a Backstage or commercial platform integration
becomes an implementation choice instead of the source of the mental model.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## How to read platform evidence

A platform course can easily become a tour of screenshots, products, and policy
files. This course uses a stricter evidence ladder. First identify the
**authoritative fact**: for example, an API owner, a released contract digest, a
consumer relationship, or an approved runtime route. Then identify the
**mechanism** that stores or derives it. Next identify the **failure** that could
make the mechanism lie. Finally choose a proof that would detect that failure.
A catalog page is therefore not evidence that an API is owned; the source
metadata, relation validation, and accountable group are the evidence. A green
scorecard is not evidence that a release is safe; the individual, fresh,
traceable evidence records are.

Use three labels throughout the course:

- **authoritative** — the system or team allowed to create or change a fact;
- **derived** — a projection computed from authoritative facts and safe to
  rebuild;
- **advisory** — information that helps a decision but cannot make it alone.

The contract registry is authoritative for released bytes and digests. The
portal search index is derived from source documentation. A numerical product
metric is advisory: it can reveal friction, but it cannot decide whether a
security blocker may be ignored. Confusing these labels is one of the fastest
ways to build a polished but unsafe platform.

## A disciplined ten-day route

Each day begins with the chapter because the book defines the engineering
problem. The exercises then force transfer: you must apply the model to cases
that differ from the capstone. The laboratory changes one controlled variable
and records an oracle. The checkpoint is a gate, not a summary. Do not move on
because the command is green if you cannot explain why the proof would fail
when the mechanism is broken.

Keep one notebook or Markdown log with five columns:

```text
claim | authority | mechanism | failure | decisive evidence
```

For `analysis-http@1.2.0`, a row might state that the released bytes are
immutable; the registry owns the release record; content addressing and a
primary key enforce the mechanism; version reuse with different bytes is the
failure; digest comparison and an overwrite attempt are the evidence. By the
final defense, the notebook becomes a compact map of the entire platform.

## Primary and comparative language tracks

Choose Python or TypeScript as the implementation track you read line by line.
Run the other track against the shared vectors after you understand the primary
implementation. The goal is not line-for-line symmetry. Python may use data
classes and pathlib while TypeScript uses interfaces and ESM modules. The parity
boundary is the outcome: canonical entity references, immutable releases,
blocking policy, consumer-safe retirement, deterministic templates, isolated
sandboxes, and the same release decisions.

When the two languages disagree, do not immediately patch one to imitate the
other. First identify whether the difference is internal representation or an
observable platform guarantee. Only the latter is a parity defect.
