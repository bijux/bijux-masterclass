---
module_id: PLAT-035
program: Platform Engineering
level: 1
module_number: 35
title: Configuration Management
status: complete
last_verified: 2026-09-02
---

# Configuration Management

## One-Page Review

### Governing question

How should a platform define, validate, compose, version, deliver, activate, observe, roll back, and retire application configuration so that teams can change behavior without creating hidden code, secret, deployment, or runtime state?

### Essential definitions

- **configuration** is non-secret data that selects behavior expected to vary independently of application artifact bytes.
- A **configuration contract** defines keys, types, constraints, defaults, compatibility, ownership, sensitivity, delivery, reload, and failure semantics.
- A **configuration revision** is an immutable canonical value plus schema/policy versions, provenance, and digest.
- A **source** contributes values or constraints; the **effective configuration** is the fully resolved value actually consumed by one workload revision.
- **precedence** is an explicit ordered rule for resolving duplicate keys; **unification** combines compatible constraints and fails on contradiction rather than silently overriding.
- **static configuration** is read at process start or build/deploy realization; **dynamic configuration** can change while a process serves.
- A **feature flag** is a named, typed, observable runtime decision evaluated with context; it is not a substitute for arbitrary configuration.
- **activation** makes a validated revision effective for a target population; publication alone does not prove consumption.
- **drift** is a relevant difference among declared, delivered, loaded, and evaluated values.
- **configuration debt** is obsolete, ownerless, duplicated, unobserved, or permanently transitional configuration that increases behavioral state space.

### Central model, mechanism, or theorem

Let sources $S_1,\ldots,S_n$ and schema/policy $\Sigma_v$ resolve under declared composition rule $\rho$ to canonical configuration $C=\rho_{\Sigma_v}(S_1,\ldots,S_n)$. Publish immutable revision $r=(d(C),v,p)$, where $p$ records provenance. For workload revision $w$ and target $t$, safe activation requires schema/policy validity, compatibility $K(w,r)$, authorized target binding, successful delivery, process acknowledgement of $d(C)$, and outcome evidence. The effective value is not whatever the control plane stores; it is what the process actually loaded or evaluated.

### Critical invariants

- Every setting has one durable meaning, type, owner, default, sensitivity classification, compatibility rule, and retirement plan.
- Secrets and credentials are references governed by the secret-delivery capability, never ordinary configuration values.
- Sources, precedence/unification, defaults, environment inputs, rendering tool/version, and output digest are deterministic and explainable.
- Schemas validate structure and cross-field constraints before publication; semantic and environment preconditions run before activation.
- Published revisions are immutable and addressable by digest/version; mutable aliases record history but are not runtime identity.
- A deployment binds artifact and configuration revision explicitly; dynamic changes bind revision, target population, time, actor, and reason.
- Delivery method matches application semantics: environment variables are startup snapshots; mounted files require atomic update/read/reload design; APIs/watchers require cache and outage behavior.
- Activation is progressive where blast radius warrants it and verifies loaded/evaluated revision plus user outcomes.
- Missing, stale, invalid, partial, or unauthorized configuration fails according to a declared safe policy, never an accidental library default.
- Configuration revisions, flags, exceptions, aliases, and schemas are retired after usage proves no consumers remain.

### Common failures

Putting credentials in ConfigMaps or repositories; encoding behavior as undocumented strings; grouping every value into giant `dev/stage/prod` files; layering overrides until origin is unknowable; relying on YAML type inference; validating syntax but not cross-field semantics; changing a mutable object without a rollout/reload contract; assuming mounted file update means process reload; using environment variables for dynamic control; making every setting a feature flag; evaluating flags without stable targeting keys; logging personal evaluation context; changing code and configuration without attribution; using silent defaults during provider outage; rolling back code without compatible configuration; and never removing old flags or keys.

### Compact example

A payments service defines schema revision 5 for `authorization.timeout_ms`, `retry.max_attempts`, and feature flag `new_risk_model`; database credentials remain secret references. Team values, production constraints, and region data unify into canonical JSON digest $c_9$. Validation proves timeout/retry bounds and their combined worst-case budget. Deployment binds artifact $a_7$ to $c_9$; pods receive an immutable versioned ConfigMap file and report loaded digest $c_9$ after atomic read and validation. The risk flag uses stable account targeting, begins at 1%, emits variant/reason/revision telemetry without personal context, and progresses on payment outcomes. Rollback restores flag/config revision while both code paths remain compatible. Usage inventory later proves the flag and old schema field removable.

### Connections

This capability provides explicit configuration inputs to [PLAT-034](034-deployment-capability.md), uses environment ownership from [PLAT-033](033-environment-provisioning.md), and builds on Kubernetes delivery semantics from [PLAT-026](026-configuration-and-secrets.md). PLAT-036 separates confidential secret delivery; observability, policy, reliability, and incident modules consume configuration identity and change records.

## Governing Question

What product contract lets teams change non-secret behavior safely and quickly while ensuring that every effective value is typed, owned, reproducible, compatible, observable, and removable?

Configuration is executable influence expressed as data. A one-character timeout change can cause more production harm than a large code change. A feature flag can create two behavioral systems inside one binary. A default can silently determine behavior precisely when the configuration service fails.

The platform should make configuration boring in the best sense: predictable composition, early validation, immutable identity, controlled activation, loaded-state evidence, and fast recovery. Flexibility without those properties becomes hidden programming.

## Why This Matters

Separating deploy-varying values from artifact bytes allows one verified artifact to move through environments without rebuilding. It improves audit, rollback, promotion, and reproducibility. But externalizing values creates new sources, delivery paths, schemas, permissions, caches, and failure modes.

Configuration often has broader blast radius than code because one global setting changes every instance immediately. Dynamic control can bypass deployment gates and progressive exposure. It must receive comparable identity, authorization, validation, observation, and incident treatment.

Poor layering makes behavior impossible to explain. A value may originate in a default, repository file, environment overlay, template, command line, ConfigMap, runtime service, or emergency override. When precedence is implicit, the same inputs can produce different outputs across tools or versions.

Configuration also accumulates. Flags become permanent, aliases conflict, old clients constrain schemas, and copied environment files diverge. A capability must own retirement, not merely creation.

## Prerequisites and Retrieval

Retrieve data types, schemas, validation, canonical serialization, hashes, versioning, backward/forward compatibility, environment variables, filesystems and atomic rename, Kubernetes ConfigMaps and volume projection, API/watch semantics, caches, feature flags, deterministic targeting, policy, RBAC, GitOps, deployment rollouts, telemetry, privacy, and incident response.

You should distinguish code-internal constants from deploy-varying configuration; configuration from secrets; source values from defaults/constraints; validation from normalization; publication from delivery from activation; control-plane desired value from process-loaded value; dynamic configuration from feature flags; flag key from variant; rollback from deletion; and syntactic validity from operational safety.

## Learning Objectives

After completing this module, you should be able to:

1. classify settings and define complete configuration contracts;
2. design typed schemas with cross-field and environment constraints;
3. compose defaults, team, environment, region, and emergency inputs deterministically;
4. canonicalize, version, attest, and bind effective configuration to deployments;
5. choose environment-variable, file, API, watcher, or flag delivery from semantics;
6. implement safe reload, cache, outage, and fallback behavior;
7. activate and roll back configuration progressively with loaded-state evidence;
8. observe effective configuration without leaking secrets or sensitive targeting context; and
9. migrate schemas and retire flags, settings, aliases, and exceptions safely.

## Core Exposition

### Classify before externalizing

Not every constant is configuration. Algorithm structure, routes wired by code, and invariant protocol behavior usually belong in the artifact. Externalize values that legitimately vary by deployment, region, tenant, controlled experiment, capacity, or operational policy without changing program implementation.

Classify each candidate setting by variability, consumer, owner, sensitivity, blast radius, update frequency, consistency need, startup/runtime use, compatibility, and failure behavior. A value that changes per request belongs in request/domain data, not global configuration.

Separate confidential material. Configuration may contain a logical secret reference, audience, and reload policy; actual passwords, private keys, tokens, and credential payloads belong in secret systems with narrower authority and redaction.

Avoid a generic `options` map. Named fields with documented units and semantics allow validation, migration, search, ownership, and observability.

### Write a configuration contract

For each field define stable path/key, description, type, units, required/optional state, default and where it is applied, allowed range/enumeration/pattern, cross-field constraints, sensitivity, mutability, delivery/reload semantics, compatible application versions, target scope, owner, and deprecation date.

Defaults are behavior. Put safe universal defaults with the application/schema when they truly apply everywhere. Environment policy can narrow a range but should not silently change an unspecified setting into a surprising behavior.

Use explicit units in keys or typed structures: `timeout_ms`, not `timeout=5`. Avoid ambiguous strings such as `on`, `yes`, or numeric-looking YAML values when the consumer expects precise types.

Document invalid-state behavior. Reject startup, keep last-known-good, use an explicit safe value, disable a feature, or degrade. “Library default” is not an operational policy unless deliberately selected and tested.

### Design schema as an evolving API

Configuration is an interface between producers and application versions. Version its schema, define compatibility, and validate both producers and consumers. JSON Schema can constrain types, required fields, ranges, patterns, composition, and unevaluated properties; other languages can express richer cross-field constraints.

Structure validation catches `"5"` where integer is required. Cross-field validation catches `retry_count * timeout` exceeding a request budget. Environment validation catches a region endpoint not allowed in a production boundary. Runtime validation catches a referenced dependency currently absent.

Choose open versus closed schemas deliberately. Allowing unknown fields helps staged compatibility but hides misspellings. Rejecting them catches errors but requires coordinated rollout. A migration window can allow old/new fields with explicit deprecation warnings.

Schemas also require ownership and tests: valid/invalid examples, boundary values, defaults, upgrade/downgrade, old/new binaries, and serialized round trips.

### Compose sources deterministically

Common sources include application defaults, platform policy, team/application values, environment class, region/cell facts, deployment parameters, and time-bounded emergency overrides. List them in the public contract.

An override model uses precedence: later or more specific values replace earlier ones. It is simple but can hide origin. Record the winning source and overwritten candidates for every field.

A constraint/unification model combines requirements and fails if values contradict. Platform can require replicas at least three while the application requests five; a request of one conflicts instead of being silently changed. CUE demonstrates this model by treating types, values, and constraints uniformly.

Do not deep-merge arbitrarily. Arrays may replace, append, merge by key, or forbid composition; null may mean explicit null or deletion. State the rule per structure. RFC 6902 JSON Patch provides ordered operations, but patches remain dependent on exact base structure and should be reviewed as transformations.

Render once with pinned tool/schema/policy/source revisions. Do not let each workload instance independently combine remote sources if identical behavior is required.

### Canonicalize and identify the effective value

Normalize values only through documented rules: units, case, ordering where semantically irrelevant, default expansion, and canonical serialization. Validation should not unexpectedly rewrite meaning.

Compute digest $d(C)$ over canonical non-secret effective configuration. Record source revisions, schema/policy/tool versions, default application, normalization, and target scope. This provenance answers why a value exists.

Publish immutable configuration revisions. A friendly alias such as `production-current` may move, but deployments resolve and record the revision/digest. Never overwrite a revision in place.

If configuration includes secret references, digest the reference identity/version and non-secret metadata, not secret payloads copied into a broad catalog. Define how secret rotation affects effective identity separately.

### Bind configuration to deployment

A release candidate declares supported configuration schema range. Deployment preflight validates exact configuration revision against artifact version, environment policy, dependency existence, and rollout strategy.

Record artifact digest $a$ and configuration digest $c$ as one effective deployment tuple. If configuration changes dynamically after deployment, append a distinct activation event; do not mutate history to imply the artifact always ran with the new value.

Separate configuration rollout from code rollout where it improves attribution. When both must change, use an expand-contract sequence and record ordering. A code revision can first accept old/new configuration, then new configuration activates, then old support is retired.

Test rollback compatibility. A previous binary may reject a new schema or interpret a value differently. Retain prior configuration revisions and schema/tool support through the rollback window.

### Choose environment variables for startup snapshots

Environment variables are language/OS-neutral and useful for small scalar startup configuration. They are inherited by child processes, often visible to debugging/process tooling, stringly typed, size-limited by execution environment, and fixed for a running process.

Parse and validate them once at startup. Report field-specific errors without echoing sensitive values. Do not periodically reread the parent environment; changing a Pod template triggers a rollout, while changing an external value does not alter an existing process environment.

Explicitly map keys instead of importing an entire object. Broad imports make new keys acquire application authority unexpectedly and increase collision risk.

Use environment variables for dynamic behavior only by restarting/rolling processes under a deployment contract. If runtime reload is required, select another mechanism.

### Choose files for structured snapshots and reload

Files support structured and larger configuration, schema validation, atomic replacement, permissions, and application-controlled reload. A process should read a complete file, validate it, construct a new in-memory configuration, then atomically swap only on success.

Watching filesystem events is subtle: projected volumes may replace symlinks/files, editors emit several events, and remote filesystems differ. Debounce, reopen by path, verify revision/digest, and tolerate duplicate/missed events with periodic reconciliation.

Kubernetes ConfigMap volumes eventually project updates under kubelet synchronization. A `subPath` mount does not receive updates. Environment-variable consumption also does not update. An immutable ConfigMap cannot change and pairs naturally with versioned names plus workload rollout.

File update is not process acknowledgement. Expose desired/delivered/loaded revisions separately. Keep last-known-good when a new file is partial, unreadable, invalid, incompatible, or fails semantic probes.

### Choose APIs/watchers for coordinated dynamic control

A configuration service supports runtime changes, targeting, audit, leases, and large fleets, but adds network, identity, cache, consistency, and availability dependencies. Define whether the source is authoritative, cached, or advisory.

Clients need bootstrap defaults, authentication, deadlines, backoff/jitter, watch resumption/revision tokens, snapshot reconciliation, bounded staleness, last-known-good persistence, and safe behavior when no valid value ever loaded.

Watch streams are hints to refresh state, not necessarily complete event logs. Reconnect from revision where supported and periodically compare full snapshots. Do not apply fields independently if the configuration requires atomic cross-field consistency.

Server availability should not sit on every request's critical path. Evaluate from a local validated snapshot/SDK cache and observe staleness. Decide how long last-known-good remains acceptable per setting.

### Use feature flags for bounded decisions

Feature flags are appropriate for release control, experiments, operations kill switches, entitlements, or migration stages when typed evaluation, targeting, audit, and removal are needed. They are poor substitutes for arbitrary structured configuration, secrets, or durable business data.

Define flag key, type, variants, default, owner, purpose, targeting attributes, privacy classification, start/expiry, expected telemetry, failure behavior, and removal issue. Code must supply a type-matching safe default for abnormal evaluation.

Evaluation context merging and precedence are part of behavior. Use a stable non-sensitive targeting key for fractional evaluation so a subject remains in one cohort. Avoid email, raw personal data, or high-cardinality sensitive context unless justified and protected.

Record flag revision, variant, reason, provider, and safe context identifier in telemetry. Sampling may be necessary; never log full evaluation context by default.

Flags multiply test states. Test defaults, each variant, targeting boundaries, provider unavailable/error, stale values, and interactions. Limit simultaneous interacting flags.

### Define safe reload semantics

Dynamic configuration updates are mini-deployments. Validate and authorize a revision, stage it, expose to a small population, observe, progress, and retain reversal. Do not let a global mutable key change every instance simultaneously unless the risk is explicitly accepted.

Applications should expose loaded revision and last successful/failed reload time. Reload constructs a complete candidate object, validates internal and external preconditions, swaps atomically, and drains or preserves state as needed.

Some fields cannot reload safely: listen addresses, thread/process topology, storage format, allocator limits, or cryptographic identity may require restart. The schema declares `restart_required`, `reloadable`, or `immutable_for_process`.

Concurrent requests should observe one coherent revision. Protect shared configuration with immutable snapshots, read-copy-update, locks, or language-appropriate atomic references. Avoid mutating a shared map field by field.

### Progressive activation and evidence

Target by environment, region/cell, workload revision, instance cohort, tenant/user key, or percentage according to risk. Preserve stable holdouts and define maximum mixed-version duration.

Before progression, verify delivery and loaded/evaluated revision, then infrastructure/app/dependency/business outcomes. A control-plane “updated” count is not evidence that processes use the value.

Analysis binds revision, population, time window, minimum evaluations/requests, baseline, telemetry freshness, thresholds, and missing-data action. Configuration can change traffic shape, retry rate, resource use, and external spend, so include downstream and cost signals.

Rollback activates the prior compatible revision and verifies processes acknowledge it. If the setting caused irreversible effects, roll-forward or compensation may be safer.

### Separate desired, delivered, loaded, and evaluated state

Let $C_d$ be desired/published configuration, $C_x$ delivered to a process boundary, $C_l$ loaded in memory, and $C_e(q)$ evaluated for request/context $q$. These can differ during propagation, failures, targeting, or stale caches.

Expose hashes/versions at each boundary without exposing values. A status endpoint can report schema and loaded digest; telemetry can attribute requests to a revision/variant. Catalogs map revisions back to owners and provenance.

Do not place full configuration values in metric labels. Digests and bounded variants support aggregation; detailed values belong in access-controlled audit stores with redaction.

Alert on invalid/rejected revision, excessive propagation or loaded-version skew, stale caches, provider error/default use, unknown consumers, expired overrides, and unowned settings.

### Govern access and audit

Separate author, reviewer, publisher, target activator, flag operator, schema owner, and emergency roles. Scope write authority by application, environment, field/flag namespace, and risk tier. Production global flags deserve stronger control than preview values.

Audit old/new revision digests, changed paths with sensitive values redacted, source/actor, reason, target, validation/policy results, approvals, activation steps, loaded acknowledgements, and rollback. Preserve immutable history.

Validate untrusted configuration as hostile input. Bound size, depth, aliases/references, regex complexity, numbers, decompression, parsing time, and rendered resource count. Schema-valid data can still cause denial of service.

Sign or otherwise authenticate high-value published revisions where crossing trust boundaries. Authorization still depends on target and setting policy.

### Migrate schemas and retire debt

Use additive schema evolution where possible. Readers accept old/new; producers stop old; inventory confirms no old readers/producers; then constraints tighten and fields are removed. Renames temporarily support both with conflict rejection and deprecation telemetry.

For type/semantic changes, introduce a new key rather than silently reinterpreting an old one. Convert explicitly and record which representation won. Avoid permanent aliases.

Inventory consumers through loaded/evaluation telemetry and source search, recognizing that telemetry absence is not proof of no use. Set owner and deadline; warn, then reject after evidence and communication.

Delete flags after rollout/experiment/migration completes: choose final code path, remove targeting/rules, deploy removal, observe, then delete control-plane flag. Deleting first can activate application defaults unexpectedly.

### Operate the capability

Measure validation latency/failures, render determinism, publish/activation latency, propagation and loaded skew, reload failures, provider/cache staleness, default/error evaluation, rollback time, configuration-caused incidents, expired overrides, unowned keys, flag age, and removal rate.

Service objectives differ by static and dynamic modes. Static publication can tolerate short outage if deployments pause. Kill-switch evaluation/control may require high availability, local caching, and tested emergency paths.

Capacity includes object size/count, watch fan-out, update rate, cache memory, audit volume, schema computation, feature evaluation latency, and telemetry cardinality. Rate-limit global changes and prevent thundering-herd reloads with staged rollout/jitter.

The following synthetic inventory demonstrates configuration-control coverage.

<!-- bijux-verify: {"id":"configuration-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"configurations=10\nschema_validated=9\nimmutable_versioned=8\ndynamic_reload=4\nfeature_flagged=3\nsecret_free=9\nowned=10\nobserved=8\nrollback_ready=8\n","stderr":""}} -->
```python
configurations = [
    {"name":"api-timeouts",   "schema_validated":True,  "immutable_versioned":True,  "dynamic_reload":True,  "feature_flagged":False, "secret_free":True,  "owned":True, "observed":True,  "rollback_ready":True},
    {"name":"retry-policy",   "schema_validated":True,  "immutable_versioned":True,  "dynamic_reload":True,  "feature_flagged":False, "secret_free":True,  "owned":True, "observed":True,  "rollback_ready":True},
    {"name":"risk-model",     "schema_validated":True,  "immutable_versioned":True,  "dynamic_reload":True,  "feature_flagged":True,  "secret_free":True,  "owned":True, "observed":True,  "rollback_ready":True},
    {"name":"checkout-ui",    "schema_validated":True,  "immutable_versioned":True,  "dynamic_reload":True,  "feature_flagged":True,  "secret_free":True,  "owned":True, "observed":True,  "rollback_ready":True},
    {"name":"worker-limits",  "schema_validated":True,  "immutable_versioned":True,  "dynamic_reload":False, "feature_flagged":False, "secret_free":True,  "owned":True, "observed":True,  "rollback_ready":True},
    {"name":"region-routing", "schema_validated":True,  "immutable_versioned":True,  "dynamic_reload":False, "feature_flagged":False, "secret_free":True,  "owned":True, "observed":True,  "rollback_ready":True},
    {"name":"search-v2",      "schema_validated":True,  "immutable_versioned":True,  "dynamic_reload":False, "feature_flagged":True,  "secret_free":True,  "owned":True, "observed":True,  "rollback_ready":True},
    {"name":"batch-schedule", "schema_validated":True,  "immutable_versioned":True,  "dynamic_reload":False, "feature_flagged":False, "secret_free":True,  "owned":True, "observed":True,  "rollback_ready":True},
    {"name":"preview-theme",  "schema_validated":True,  "immutable_versioned":False, "dynamic_reload":False, "feature_flagged":False, "secret_free":True,  "owned":True, "observed":False, "rollback_ready":False},
    {"name":"legacy-bundle",  "schema_validated":False, "immutable_versioned":False, "dynamic_reload":False, "feature_flagged":False, "secret_free":False, "owned":True, "observed":False, "rollback_ready":False},
]

print(f"configurations={len(configurations)}")
for field in ("schema_validated", "immutable_versioned", "dynamic_reload", "feature_flagged", "secret_free", "owned", "observed", "rollback_ready"):
    print(f"{field}={sum(configuration[field] for configuration in configurations)}")
```

The counts reveal gaps; they do not prove schema quality, immutability, secret separation, reload atomicity, observation, or rollback safety.

## Definitions and Notation

Let $S_1,\ldots,S_n$ be input values or constraints, $\Sigma_v$ schema/policy revision $v$, and $\rho$ the declared precedence, merge, patch, or unification rule. Effective canonical configuration is $C=\rho_{\Sigma_v}(S_1,\ldots,S_n)$ when all constraints hold.

Let revision $r=(d(C),v,p)$ contain canonical configuration digest, schema version, and provenance $p$ identifying sources, rendering tool/rules, owner, and target scope.

For workload artifact/revision $w$, compatibility predicate $K(w,r)$ states whether it can parse and correctly interpret revision $r$ under declared assumptions. Structural validation alone does not establish $K$.

Let $C_d(t)$ be desired configuration, $C_x(i,t)$ delivered content for instance $i$, $C_l(i,t)$ loaded in-memory snapshot, and $C_e(i,q,t)$ value evaluated for request/context $q$. Convergence is observed equality of applicable revision identities, not assumed from publication.

For flag $f$, evaluator $F(f,q,r)$ returns typed value/variant plus reason and metadata under revision $r$ and context $q$. Stable fractional targeting requires a stable targeting key and deterministic provider rule; it does not guarantee representative cohorts.

## Mechanisms, Invariants, or Proof Structure

The configuration assurance chain is:

1. classify a setting and separate secret/domain/code concerns;
2. define typed ownership, defaults, constraints, compatibility, delivery, and retirement;
3. collect declared sources and compose them under explicit deterministic rules;
4. validate schema, cross-field, policy, target, and resource constraints;
5. canonicalize and publish an immutable digest-bound revision with provenance;
6. bind it to an artifact/target or dynamic activation event;
7. deliver through a mechanism matching snapshot/reload/evaluation semantics;
8. verify delivered, loaded, and evaluated revision identities;
9. progress and analyze outcomes, then roll back/forward if needed; and
10. migrate consumers and retire obsolete revisions, keys, flags, aliases, and exceptions.

This is not proof of safe behavior. Schemas can omit semantic constraints; composition rules, parsers, delivery systems, processes, targeting, telemetry, and humans can fail. The chain makes behavior and assumptions attributable.

The invariants are one meaning/owner, secret separation, deterministic explainable composition, pre-publication validation, immutable revision identity, artifact/activation binding, delivery-contract fidelity, progressive loaded-state evidence, explicit failure policy, and lifecycle retirement.

## Alternatives and Trade-Offs

**Environment variables versus files:** environment variables are simple startup scalars but stringly typed and immutable per process. Files support structure and atomic reload but require filesystem/watch/reopen design.

**Repository/GitOps versus configuration service:** repositories offer reviewable version history and deterministic deployment-bound snapshots. Services enable low-latency targeting/dynamic control but add runtime availability, identity, caching, and audit complexity.

**Overrides versus unification:** precedence is familiar and supports deliberate replacement but can hide value origin. Unification detects contradictions and combines constraints but requires different modeling and tooling.

**Immutable revisions versus mutable objects:** immutable versions improve identity, rollback, and cache safety at object/cleanup cost. Mutable objects are convenient for dynamic control but demand history, acknowledgement, and attribution.

**Restart versus reload:** restart reuses deployment/lifecycle safety and resets process state, but costs availability/time. Reload is faster but needs atomic in-process transitions, compatibility, concurrency, and failure handling.

**Feature flags versus configuration rollout:** flags support per-context decisions and progressive exposure. Ordinary revisions suit coherent environment/workload snapshots. Using flags for structured config creates opaque behavioral combinations.

**Open versus closed schemas:** open schemas improve rolling compatibility; closed schemas catch unknown/misspelled fields. Evolve through explicit windows rather than choosing accidentally.

## Failure Modes and Misconceptions

- **“Configuration is harmless because it is data.”** applications execute its influence.
- **“Anything outside code is configuration.”** secrets, domain data, request data, and invariant program structure have different owners/lifecycles.
- **“Environment variables are dynamic.”** a running process has a startup snapshot.
- **“The mounted file changed, so the app reloaded.”** projection, watch, read, validation, and atomic swap are separate.
- **“A ConfigMap is a database.”** size, transactions, query, update rate, and coordination semantics are limited.
- **“Schema valid means operationally safe.”** cross-resource budgets, dependencies, environment policy, and outcomes remain.
- **“Later overlays are more authoritative.”** precedence is a design choice and can hide policy violations.
- **“A feature flag is just a boolean.”** variants, context, targeting, provider state, errors, telemetry, and removal matter.
- **“Missing flag provider means off.”** only the explicit application default defines abnormal behavior.
- **“Control-plane revision equals effective revision.”** delivered, loaded, cached, and per-request evaluated states can differ.
- **“Config rollback restores all effects.”** retries, traffic, data, and external actions may persist.
- **“Logging config helps debugging.”** values/context may contain credentials or personal/sensitive data.
- **“Old flags can remain disabled forever.”** they preserve dead code, authority, and combinatorial tests.
- **“Deleting the flag completes cleanup.”** remove code paths and prove consumers first, or defaults may activate unexpectedly.

## Worked Examples

### Example 1

A `timeout` value is `5`, but one service interprets seconds and another milliseconds. The contract replaces it with `timeout_ms`, integer bounds, owner, default, and schema migration. Conclusion: keys and types must encode stable units and meaning.

### Example 2

Platform policy requires at least three production replicas while a team overlay sets one. Last-write-wins silently accepts one; constraint unification reports contradiction. Conclusion: policy constraints should not be modeled as ordinary defaults.

### Example 3

A ConfigMap consumed as environment variables is edited. Existing pods retain old values; new pods receive new ones, creating unrecorded mixed state. The capability uses an immutable versioned ConfigMap and deployment-bound rollout. Conclusion: delivery semantics determine activation.

### Example 4

A projected file updates, but the app watches the original inode and never reopens the path. Loaded digest remains old. The app reconciles periodically, reopens, validates, atomically swaps, and reports revision. Conclusion: filesystem notification is not reload acknowledgement.

### Example 5

Two fields `timeout_ms=1000` and `attempts=10` validate independently but violate a five-second request budget. Cross-field constraint rejects the revision. Conclusion: schemas must express semantic relationships, not only field types.

### Example 6

A global dynamic retry change reaches every instance simultaneously and overloads a dependency. The replacement activates by cell, observes actual loaded revision and downstream saturation, then progresses. Conclusion: configuration changes need blast-radius controls like code deployments.

### Example 7

A 10% flag uses a random value on every evaluation, so users switch variants per request. Stable non-sensitive account targeting makes cohort assignment deterministic and telemetry attributes outcomes by variant/revision. Conclusion: fractional percentage requires stable subject identity.

### Example 8

The flag provider is unavailable. One SDK returns the application-supplied safe default and emits error metadata; cached last-known-good is accepted for only the declared staleness window. Conclusion: outage behavior must be designed at each setting.

### Example 9

Code rollback restores an older binary that cannot parse a newly renamed field. Expand-contract had retained both old/new keys, so rollback succeeds; conflicting simultaneous values would have failed validation. Conclusion: configuration compatibility is part of release recovery.

### Example 10

A completed experiment flag remains disabled for two years. Inventory finds one old code path and unknown consumers. The team selects the winning path, deploys code removal, observes zero evaluations, then deletes the control-plane flag. Conclusion: retirement proceeds from consumers to control state.

## Cross-Program Connections

- **Programming Languages:** types, evaluation, defaults, scoping, and semantics explain why configuration behaves like a small language.
- **Formal Methods:** constraints, satisfiability, invariants, and refinement support composition and validation.
- **API Engineering:** schemas, compatibility, versioning, deprecation, and consumer contracts apply directly.
- **Distributed Systems:** propagation, caching, watches, consistency, partial failure, and convergence shape dynamic configuration.
- **Computer Security:** least privilege, sensitive classification, authenticated publication, and hostile parsing govern trust.
- **Statistics and Experimentation:** stable cohorts, exposure, attribution, and interaction effects govern flags.
- **Reliability Engineering:** progressive activation, last-known-good, fallback, telemetry freshness, and rollback bound incidents.
- **Data Engineering:** lineage, canonicalization, schema evolution, catalogs, and retention make configuration explainable.

## References

1. Kubernetes, “ConfigMaps,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/configuration/configmap/
2. Kubernetes, “ConfigMap v1 API,” official reference, retrieved 2026-09-02. https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/config-map-v1/
3. Kubernetes, “Configure a Pod to Use a ConfigMap,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
4. JSON Schema, “Draft 2020-12,” specification, published 2022-06-16. https://json-schema.org/draft/2020-12
5. IETF, “JSON Patch,” RFC 6902, April 2013. https://www.rfc-editor.org/rfc/rfc6902
6. CUE, “How CUE Enables Configuration,” official documentation, retrieved 2026-09-02. https://cuelang.org/docs/concept/how-cue-enables-configuration/
7. CUE, “How CUE Enables Data Validation,” official documentation, retrieved 2026-09-02. https://cuelang.org/docs/concept/how-cue-enables-data-validation/
8. OpenFeature, “Specification,” current project specification, retrieved 2026-09-02. https://openfeature.dev/specification/
9. OpenFeature, “Flag Evaluation API,” current project specification, retrieved 2026-09-02. https://openfeature.dev/specification/sections/flag-evaluation/
10. OpenFeature, “Evaluation Context,” current project specification, retrieved 2026-09-02. https://openfeature.dev/specification/sections/evaluation-context/
11. OpenFeature, “Hooks,” current project specification, retrieved 2026-09-02. https://openfeature.dev/specification/sections/hooks/
12. Adam Wiggins, “The Twelve-Factor App: Config,” project guidance, retrieved 2026-09-02. https://www.12factor.net/config

## Exercises

### Exercise 1

Define configuration, contract, source, schema, effective configuration, revision, activation, loaded state, feature flag, drift, and configuration debt. State one non-guarantee for each.

### Exercise 2

Trace one configuration change from authored sources through composition, schema/policy validation, canonicalization, publication, deployment binding, delivery, loaded acknowledgement, progressive activation, outcome analysis, rollback, and retirement.

### Exercise 3

A service imports an entire mutable ConfigMap as environment variables, stores a database password beside timeouts, uses undocumented YAML overlays, accepts unknown keys, changes a global retry flag instantly, treats missing provider data as enabled, and logs full evaluation contexts. Diagnose at least ten failures and correct them.

### Exercise 4

Design configuration for a multi-region API with static listener settings, reloadable timeout/retry budgets, rotating database credentials, tenant-specific experimental behavior, intermittent control-plane connectivity, and a 30-second rollback objective. Choose contracts, delivery, caching, activation, observation, and recovery.

### Exercise 5

A team must rename `max_retries` to `attempt_limit`, change its meaning from total attempts to retries-after-first-attempt, and remove a three-year-old flag that selects legacy retry behavior. Design a compatible schema/code/telemetry rollout and prove when old state can be removed.

## Answers to the Exercises

### Answer 1

Configuration is non-secret deploy-varying behavior data but is not automatically safe. A contract specifies meaning/lifecycle but cannot prove implementation. A source contributes values/constraints but is not necessarily authoritative. A schema validates declared rules but can omit semantics. Effective configuration is resolved canonical data but differs from what a process loaded. A revision gives immutable identity but not compatibility. Activation targets a revision but does not prove consumption/outcomes. Loaded state reports in-memory identity but not every request's targeted value. A feature flag is typed contextual control but not arbitrary configuration or business data. Drift is a relevant difference but not always harmful. Configuration debt names obsolete/ambiguous control state but inventory alone does not remove it.

### Answer 2

The author identity changes an owned source; composition records all source revisions and precedence/unification. Schema validates types/bounds/cross-fields, policy validates target and sensitivity, and semantic preflight checks dependencies. Canonical rendering with pinned tool/schema produces digest and provenance; publication creates immutable revision. Deployment binds artifact/configuration/environment digests. Delivery reports desired and delivered identity; the process reads a complete snapshot, validates compatibility, swaps atomically, and reports loaded digest. Activation progresses by cohort/cell, observes actual evaluated revision, application/dependency/business outcomes, samples, and telemetry freshness. Failure reactivates a compatible prior revision and verifies acknowledgement/effects. History remains immutable. Retirement inventories consumers, migrates old readers/writers, warns/rejects deprecated use, removes code paths, observes zero use, then deletes aliases/flags and eventually old revisions under retention policy.

### Answer 3

Whole-object environment import grants new keys accidental authority and risks collision; map explicit fields. Existing processes never receive mutable ConfigMap environment changes; use versioned immutable objects plus rollout or designed file/API reload. The database password violates secret separation; store a secret reference and deliver it narrowly. Undocumented overlays make origin/merge ambiguous; declare deterministic rules and field provenance. Unknown keys hide typos; use a closed schema or explicit compatibility window. Retry fields need types, units, bounds, and cross-field/dependency budget. Instant global flag activation has maximal blast radius; progress by stable cohorts with downstream evidence. Missing provider data is unknown/error and should return a safe explicit default or bounded last-known-good, not enabled. Full contexts can leak personal/sensitive data and create cardinality; record safe identifiers/variant/reason/revision with opt-in protected details. Further corrections include owners, immutable revision identity, artifact compatibility, loaded acknowledgement, rollback, audit, expiry, and flag retirement.

### Answer 4

Listener address/port are typed startup-only fields delivered in an immutable deployment-bound revision and changed by rolling restart. Timeout and retry form one cross-field budget, delivered as a versioned structured file or local SDK snapshot; reload validates complete data, atomically swaps, reports digest, and progresses by region/cell with dependency saturation evidence. Database configuration stores only credential reference/audience/version; secret delivery performs dual-credential rotation and process acknowledgement. Tenant experiment uses a typed flag with stable non-sensitive tenant key, privacy-reviewed context, explicit default, variant telemetry, owner/expiry, and limited interactions. Clients cache validated last-known-good revisions locally, reconnect with backoff/revision, reconcile snapshots, and define maximum staleness; the control plane is not per-request. Keep the prior loaded snapshot and compatible code path for at least the rollback window. A rollback activation targets the old revision, completes within 30 seconds by local cached snapshot, verifies acknowledgements, and checks user/downstream outcomes.

### Answer 5

Introduce `attempt_limit` as a new field with explicit total-attempt semantics rather than silently reinterpreting `max_retries`. Release code that accepts both: if only old exists, derive `attempt_limit=max_retries+1`; if only new exists, use it; if both exist, require equality under conversion or reject. Emit deprecation and source/loaded telemetry without values. Keep the legacy flag and both retry implementations while cohorts move to the new key/behavior; validate boundaries including zero, overflow, and total time budget. Update producers/templates and activate progressively with retry count, latency, load, and outcome evidence. Inventory old field readers/writers and flag evaluations. Once all supported binaries understand the new key, all producers emit it, rollback binaries remain compatible, no old-key reads or legacy-variant evaluations occur for the required observation/retention window, select the final code path and remove legacy branches. Deploy that removal first; then reject old key in the schema and delete the flag/control rule. Preserve historical revisions/audit according to retention.
