# Module 06 — Authorization, Tenancy, and Schema Exposure

> **Program stage:** Course 9 of 10 — Compose governed client-shaped capabilities.

> **Central question:** How can clients select flexible fields without gaining flexible authority?

## Where this module fits

Module 05 produced **Expose idempotent create/start/cancel mutations over owning services**. This module extends that result by asking: **How can clients select flexible fields without gaining flexible authority?**

The new capstone increment is **Prove field, tenant, collection, and sensitive-output authorization**. It becomes the prerequisite for **Demand Control, Persisted Operations, and Caching**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Enforce field and tenant authorization.
- Filter collections at the source.
- Protect sensitive output fields.
- Delegate state-dependent policy.
- Choose an introspection and trusted-document policy.

## Capstone increment

Prove field, tenant, collection, and sensitive-output authorization.

## Authentication establishes context; fields enforce authority

The HTTP layer authenticates the request and creates a principal. GraphQL validation proves that fields exist; it does not prove the caller may use them. Authorization is evaluated at root and nested fields because a caller may read a run but not artifact download URLs or delivery details.

The resolver receives a principal and resource tenant. It requires both permission and tenant match. Parent visibility is not inherited authorization: selecting `analysisRun` successfully does not automatically authorize every nested field.

## Collection authorization belongs in the source query

Filtering a fully loaded cross-tenant collection in the gateway is unsafe and inefficient. Analysis Control receives the principal and applies tenant ownership while selecting runs. The graph only sees authorized rows. This prevents count, timing, and pagination leakage.

Nested batch calls also carry tenant context. Batch keys cannot mix principals, and loaders cannot survive beyond the request.

## Field-level output policy

Sensitive fields such as `downloadUrl` require their own permission. Redacting after serialization is too late because the resolver may already have fetched or logged the secret. Authorization precedes source access.

When a field is denied, the policy must decide between explicit `FORBIDDEN`, concealment as null, or omission through client-specific schema visibility. The decision should be consistent and should not reveal resource existence across tenants.

## Input and mutation policy

Authorization also constrains input. A support operator may cancel a run only under a recorded support context; a tenant administrator may manage webhooks but not change artifact retention. GraphQL input coercion does not express these contextual rules.

The gateway delegates business authorization to the owner where the decision depends on current state. Edge policy can reject obviously missing permission, but the source service remains authoritative to avoid time-of-check/time-of-use defects.

## Introspection and schema visibility

Introspection is a powerful development capability, not the primary security boundary. Disabling it does not stop known operations and can harm legitimate tooling. Production policy may expose one schema to trusted clients, client-specific schema views, or a published registry while restricting ad hoc exploration.

Trusted documents reduce arbitrary operation execution. They do not make field authorization optional, because a trusted document can still be executed by the wrong principal or with another tenant's identifier.

## Authorization is selection-dependent

A GraphQL operation can select fields with different sensitivity under one root object. Authentication creates a principal and tenant context, but authorization must be evaluated for the actual selection. Granting access to `AnalysisRun.id` does not imply access to `artifacts`, `downloadUrl`, or delivery details.

The course separates four policy locations:

- **root admission** — may this caller execute the operation or root field at all?
- **source query** — which objects belong in the authorized population?
- **field output** — may this caller observe this field on this object?
- **mutation command** — may this caller request this state change now?

A single middleware check cannot replace these layers. Conversely, scattering arbitrary `if user...` checks through resolvers makes policy inconsistent and unreviewable. The capstone uses declared field coordinates and a policy decision function with structured context.

## Tenant isolation begins before object loading

Collection authorization must be part of the source query. The wrong sequence is:

```text
load twenty newest runs across all tenants
        ↓
filter unauthorized objects in the gateway
```

That approach produces timing and count leaks, sparse pages, incorrect cursors, and unnecessary exposure inside the graph process. The correct source method accepts tenant and policy scope and returns an already authorized ordered population.

Singular lookups require the same care. An unauthorized global ID should not reveal whether an object exists through different errors, timing, type names, or cache behavior. The course policy uses consistent concealment for ordinary callers while allowing carefully audited administrative diagnostics through a separate capability.

## Field-level policy and nullability

Suppose a caller may view a run but not its artifacts. There are several possible contracts:

- omit the field from a client-specific schema;
- return null with a `FORBIDDEN` execution error;
- expose an explicit access-state object;
- deny the entire parent object.

The choice is product and security policy, but it must agree with nullability. A non-null sensitive field cannot be redacted to null without bubbling. Making it nullable creates room for policy denial but also requires clients to distinguish forbidden, unavailable, and absent through error codes or explicit state.

The capstone keeps artifact fields nullable at the distributed boundary and attaches stable error extensions. It never returns an empty list for “forbidden,” because that claims the authorized set is authoritatively empty.

## Authorization and batching

Batching must not erase policy dimensions. A loader keyed only by `runId` can leak a value loaded for a privileged field to an unprivileged selection later in the same request, or across requests if the loader is incorrectly global.

Safer approaches include:

- create loaders after authentication and keep them request-scoped;
- include tenant and relevant policy class in the key;
- load source objects, then apply field policy before returning sensitive fields;
- use separate loaders for materially different authorization contexts;
- never cache an authorization denial beyond the scope where its assumptions hold.

The module lab creates two principals selecting the same object with different permissions and attempts to reuse a loader. The proof must show different authorized results and zero cross-request cache sharing.

## Introspection and schema exposure

Introspection is a type-system capability, not an authorization system. Disabling introspection does not make fields secret; clients can still observe network behavior, documentation, generated clients, and error messages. The primary defenses are correct authorization, demand control, and removal of capabilities that should not exist.

Production environments may restrict arbitrary introspection for untrusted callers or expose a client-specific registry view. If so, the policy must account for IDEs, CI validation, incident debugging, and supported clients. The course favours trusted operations for public clients while retaining controlled schema inspection for development and governance.

Schema descriptions can leak internal architecture, sensitive vocabulary, or operational details. Write descriptions for consumers, not for internal debugging. Do not include database names, hidden roles, private hostnames, or instructions that reveal bypass paths.

## Side channels in GraphQL

Graph flexibility creates side channels beyond returned data:

- different error codes for foreign and missing IDs;
- `__typename` revealing a concealed object's type;
- page counts or `hasNextPage` changing after post-filtering;
- timing differences between authorization denial and source lookup;
- cache hits that vary by another tenant's activity;
- cost errors revealing hidden field weights;
- subscription closure revealing a resource transition.

Absolute elimination of timing differences is difficult, but design can avoid obvious oracles. Authorize populations at the source, normalize concealment behavior, partition caches, and keep error metadata bounded.

## Schema exposure and client audiences

A single schema can contain fields unavailable to many callers, provided runtime authorization is complete. In some systems, audience-specific schemas reduce accidental discovery and simplify client generation. They also create composition and release complexity.

The course keeps one canonical schema and governs operations by client identity. Course 10 may publish platform-specific audience views, but those views must derive from the canonical registry and may not become divergent hand-edited schemas.

## Authorization review checklist

For every field and operation, record:

- required permission and tenant relationship;
- source-service enforcement point;
- collection filtering strategy;
- concealment behavior;
- field-level redaction contract;
- loader and cache partitioning;
- administrative exception and audit requirements;
- subscription reauthorization policy;
- error and telemetry privacy;
- tests for same-scope/wrong-owner and right-owner/wrong-scope cases.

The decisive proof is adversarial traversal: a caller with a valid token and plausible identifiers attempts to reach foreign project, run, artifact, delivery, and subscription data through every available root and nested path. All paths must preserve the same authority model.

## Worked capstone review

A principal with `RUN_READ` can read run status but lacks `ARTIFACT_READ`. Selecting `artifacts` produces a field authorization outcome; the gateway never calls Artifact Service. A tenant-B identifier for a tenant-A run is concealed at the Analysis Control query boundary.

## Python and TypeScript implications

Both tracks use one field-coordinate policy and explicit resource tenant. Framework directives may improve declaration but do not replace runtime enforcement.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-06-*.json`; prose claims without its oracle do not pass.

## Module synthesis

You are ready to leave this module when you can **enforce field and tenant authorization, filter collections at the source, and protect sensitive output fields** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **correct scope without resource authority is insufficient;; resource relationship without required permission is insufficient;; collection membership is filtered at the owner;; denied fields do not call protected sources unnecessarily;.**

The cumulative platform now includes **Prove field, tenant, collection, and sensitive-output authorization**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Demand Control, Persisted Operations, and Caching](../module-07-demand-control-persisted-operations-and-caching/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
