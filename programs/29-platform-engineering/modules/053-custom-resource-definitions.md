---
module_id: PLAT-053
program: Platform Engineering
level: 2
module_number: 53
title: Custom Resource Definitions
status: complete
last_verified: 2026-09-02
---

# Custom Resource Definitions

## One-Page Review

### Governing question

When should a platform publish a Kubernetes CustomResourceDefinition, and how should it design, validate, version, convert, operate, migrate, and retire that API so stored intent survives controller and cluster evolution without surprising clients?

### Essential definitions

- A **custom resource** is an instance of an API resource added to Kubernetes; a **CustomResourceDefinition (CRD)** declaratively registers its group, versions, names, scope, schemas, subresources, and conversion.
- A **resource** is a REST endpoint/collection such as `databaseclaims`; a **kind** is the serialized object type such as `DatabaseClaim`.
- A **structural schema** gives every field a defined structural shape and obeys Kubernetes extension rules needed for pruning, defaulting, conversion, and validation behavior.
- **pruning** removes unspecified fields at defined API-processing points unless preservation is explicitly requested for a subtree.
- **defaulting** fills absent fields according to a version's schema; a default is stored only when the object passes through a write path.
- **validation** restricts acceptable representations and transitions; OpenAPI constraints validate shape while CEL rules can express cross-field and old/new-state predicates.
- A **served version** is available to clients; the single **storage version** is the representation used for new writes.
- **conversion** maps an object between served and storage representations; `None` changes `apiVersion` only, while webhook conversion can transform fields.
- **round-trip preservation** means converting an object through another simultaneously served version and back does not lose information expressible in the original version.
- The **status subresource** separates controller-owned observation from desired spec updates; the **scale subresource** provides a standard replica interface when its paths have valid semantics.
- **storedVersions** records versions in which objects may remain persisted; changing the storage marker does not rewrite existing objects automatically.

### Central model, mechanism, or theorem

For API version $v$, let $V_v$ be the set of schema-valid representations and $C_{a\rightarrow b}:V_a\rightarrow V_b$ a conversion. While versions $a$ and $b$ are concurrently served, compatibility requires defined conversion for reachable objects and, for information promised by $a$, $C_{b\rightarrow a}(C_{a\rightarrow b}(x))=x$ up to documented canonicalization. If a schema change narrows $V_{new}\subset V_{old}$, some already stored objects can fail new validation or conversion; installing the schema does not migrate them. With $N$ objects, sustainable rewrite rate $r$, and effective deadline $D$, a storage migration needs $N/r\leq D$ before retry, throttling, conversion cost, or concurrent writes are added.

### Critical invariants

- A CRD represents durable domain intent with Kubernetes-like resource semantics, not arbitrary application data, logs, secrets, or an imperative command queue.
- Group, plural resource, kind, scope, identity, ownership, and deletion semantics are chosen for long-lived meaning and collision avoidance.
- Every served version has a structural, bounded, reviewed schema with explicit object/array/map, required/nullability, list/map topology, formats, and unknown-field policy.
- Admission accepts only states and transitions the controllers, converters, clients, storage, backup, and recovery paths can handle.
- Defaults are safe, deterministic, version-aware, and do not retroactively appear in old objects merely because the CRD changed.
- Conversion is deterministic, side-effect-free, batch-safe, available on the API critical path, and round-trip tested across every supported version pair.
- Exactly one version is storage; storage-version changes include object migration and proof that the retired version left `status.storedVersions`.
- Spec/status ownership, `generation`, conditions, and scale behavior remain coherent across versions and subresources.
- Authorization, admission, quotas, object/count/size bounds, watch/list load, audit, backup, restore, and tenant scope are designed with the API.
- Removing a served version, conversion endpoint, CRD, or controller follows measured client migration and stored/effect disposition, never file deletion alone.

### Common failures

Creating a CRD for every configuration document; using the API server as high-volume telemetry or application storage; choosing cluster scope for convenience; vague `spec.config` blobs; preserving all unknown fields; omitting array bounds or list topology; treating `required` as non-empty; confusing absent with null or zero; adding unsafe defaults; tightening validation before auditing stored objects; using admission to repair incompatible storage; assuming `None` conversion renames fields; making conversion depend on the object it is converting or an unavailable service; changing storage version without rewriting objects; dropping an old version while it remains in `storedVersions`; changing kind/group as a rename; exposing status through spec; implementing `/scale` for non-replica semantics; broad RBAC over every custom resource; deleting a CRD and unexpectedly deleting its instances; and claiming compatibility because YAML still applies.

### Compact example

A platform proposes `DatabaseClaim` in `data.platform.example/v1beta1`, namespaced because ownership and policy are namespace-scoped. The schema exposes outcome fields—class, engine family, region policy, recovery tier, parameters with a bounded typed map—and rejects provider credentials and free-form manifests. Lists declare map keys; strings/numbers have bounds; CEL enforces immutable identity and valid old/new size transitions. Status is a subresource with observed generation, conditions, endpoint reference, and active revision; no secret value is copied. Before `v1`, fixtures cover every stored beta shape. A conversion webhook maps renamed fields through a hub representation and round-trips them, without provider calls. Both versions are served, clients migrate, `v1` becomes storage, an explicit storage migration rewrites all objects, `storedVersions` is verified, beta requests fall to zero, and only then is beta serving and conversion support removed.

### Connections

This module builds on platform API and declarative-resource design from [PLAT-015](015-apis-and-declarative-resources.md) and [PLAT-023](023-kubernetes-declarative-resources.md), workload/controller architecture from [PLAT-024](024-pods-workloads-and-controllers.md), upgrades from [PLAT-049](049-upgrade-and-deprecation-policies.md), and reconciliation from [PLAT-052](052-desired-state-and-reconciliation.md). PLAT-054 through PLAT-060 add operator workflows, idempotency, deletion, status/drift, dependencies, recovery, and a complete domain-specific API.

## Governing Question

How do you decide that a platform concept belongs in the Kubernetes API, then give it a stable semantic identity, schema, validation, version-conversion, storage, authorization, observability, and retirement contract that remains safe under real clients and stored data?

A CRD is easy to install. That convenience can disguise a serious commitment: the cluster API begins storing user intent, clients cache discovery and generate code, RBAC grants access, controllers attach effects and finalizers, backups capture objects, policies match group/resource paths, and automation depends on field meanings. The YAML definition is the start of a distributed public API lifecycle.

The design objective is not “make `kubectl get` work.” It is to publish a small, comprehensible, durable resource whose states can be admitted, stored, converted, reconciled, authorized, observed, upgraded, restored, and removed. Kubernetes supplies machinery; the platform still owns domain semantics and operations.

## Why This Matters

CRDs inherit valuable Kubernetes behavior: discovery, CRUD, watch, optimistic concurrency, metadata, labels, namespaces, RBAC integration, admission, audit, finalizers, and tooling. A platform can expose durable intent without building an API server from scratch.

They also join the Kubernetes control plane's fate. Large objects, high write rates, expensive validation, conversion outages, broad watches, explosive cardinality, or huge CRD counts consume shared API-server and storage resources. A noisy extension can harm unrelated workloads.

Schemas become storage and client contracts. Unknown-field pruning, default changes, list topology, nullability, and conversion can silently change meaning. The object visible to a controller may not be byte-for-byte what a client submitted.

Versioning creates a matrix, not a label. Clients can write one served version, storage can contain another, watches can request a third, and conversion can be called on reads, writes, and lists. Removing one version prematurely can block access to every object.

CRD deletion is destructive. Controllers and external effects may outlive API records, while backups can restore mismatched CRDs and objects. Lifecycle planning must precede installation.

## Prerequisites and Retrieval

Retrieve REST resources and representations, Kubernetes API groups/versions/kinds, discovery, metadata, spec/status, namespaces and cluster scope, OpenAPI v3 and JSON Schema concepts, structural typing, pruning, defaulting, validation, CEL, immutability, list/map/set semantics, serialization, optimistic concurrency, Server-Side Apply, field ownership, watch/list, admission, RBAC, quotas, finalizers, conversion functions, round-trip properties, storage versions/migration, compatibility/deprecation, backup/restore, controllers, and distributed-system failure.

You should distinguish resource from kind; API group/version from CRD object's own `apiextensions.k8s.io/v1`; served from preferred from storage version; schema validation from admission policy; default from required; absent from null and zero; structural from permissive; pruning from validation; atomic list from set/map list; conversion from migration; representation compatibility from behavioral compatibility; status from spec; namespace scope from tenant isolation; CRD deletion from instance cleanup; and API availability from controller outcome availability.

## Learning Objectives

After completing this module, you should be able to:

1. choose among CRD, built-in resource/configuration, aggregated API, external API/database, and durable work resource;
2. define durable group, resource/kind, scope, identity, ownership, and lifecycle semantics;
3. construct bounded structural schemas with deliberate required, nullability, default, pruning, list, map, and embedded-object behavior;
4. layer OpenAPI and CEL validation without making safe upgrades or recovery impossible;
5. design status, scale, printer columns, categories, and selectable fields as public API surfaces;
6. model served/storage versions, conversion round trips, webhook failure, and storage migration;
7. control RBAC, admission, tenant scope, size/cardinality, list/watch and conversion load, audit, backup, and restore;
8. test clients, controllers, schemas, conversion, mixed versions, stored fixtures, downgrade, and deletion; and
9. deprecate and retire versions and CRDs without losing intent or orphaning effects.

## Core Exposition

### Decide whether the concept belongs in a CRD

Use a CRD when consumers need durable declarative intent integrated with Kubernetes identity, namespace, authorization, discovery, watch, admission, and reconciliation. Good candidates are comparatively low-write control resources with meaningful lifecycle: database claims, delivery policies, environment bindings, or application abstractions.

Prefer built-in resources and configuration when they already express the job. Creating a parallel `PlatformDeployment` that mirrors every Deployment field adds translation and compatibility cost without a stable abstraction.

Consider an aggregated API when you need custom storage, request semantics, protocol behavior, or subresources beyond CRD machinery and can operate an API server. Use an external API/database for high-volume application records, telemetry, large blobs, end-user data, complex query, or transactions. Kubernetes documentation explicitly cautions against using custom resources as application, end-user, or monitoring data storage.

If every object represents a one-time command that must be processed independently, model a durable operation/work resource with immutable intent and terminal outcome, or use an event/work system. A mutable singleton CRD plus event watch is not a lossless command log.

State the ownership trade: a CRD couples availability and lifecycle to cluster API machinery. That can be correct for cluster/platform control, but not merely because controller libraries make it easy.

### Name the domain for long-lived meaning

Choose a DNS-qualified API group controlled by the owning organization or product, not a vendor implementation you expect to replace. Group and plural form part of REST paths, RBAC rules, policy matches, audit, discovery, and client code. Renaming them later creates a new resource migration.

Choose a singular CamelCase kind and lower-case plural resource with unambiguous domain meaning. Short names are convenience and can collide across installed APIs; do not make automation depend on them. Categories affect broad CLI queries and should not unexpectedly expose or load expensive resources.

Namespaced scope works when identity, ownership, authorization, quota, policy, and lifecycle align with namespaces. Cluster scope is appropriate for genuinely cluster-wide concepts. It is not a shortcut around cross-namespace references. Namespace boundaries alone are not full tenant isolation, but they integrate useful authorization and lifecycle controls.

Define object identity and recreation. Kubernetes `metadata.uid` distinguishes incarnations with the same namespace/name. Controllers and external tags should preserve UID-based ownership so deletion/recreation cannot accidentally adopt an old effect.

### Model intent rather than implementation syntax

Expose decisions the consumer owns and the controller can honor: service class, availability/recovery objective, location constraint, capacity intent, data disposition, dependency reference, or policy choice. Avoid embedding raw provider manifests, shell fragments, connection credentials, or controller workflow steps.

For each field document meaning, units, allowed states, ownership, default, mutability, interaction, security consequence, status/effect mapping, and version lifecycle. A schema can prove `integer`; it cannot explain whether `0` means disabled, automatic, or invalid.

Keep `spec` small and cohesive. A free-form `spec.config` preserves implementation coupling and defeats typed clients, validation, field ownership, conversion, discoverability, and compatibility analysis. If limited extensibility is necessary, bound and namespace it, declare support, and preserve unknown data only in the narrow subtree that genuinely requires it.

References should carry group/kind where polymorphism is allowed, name, optional namespace under safe rules, and documented authorization. A reference is not proof the target exists, is ready, or consents to use; admission and reconciliation must implement those semantics.

### Build a structural and bounded schema

Use `apiextensions.k8s.io/v1` and define an OpenAPI v3 schema per served version. Structural schemas specify types at the core shape and follow permitted extension placement. They enable predictable pruning, defaulting, validation, and field-management topology.

Define `type: object`, properties, array items, scalar formats, and constraints. Add string length/pattern, numeric range, array item bounds, and object property bounds according to domain limits. Unbounded lists or maps can inflate objects, CEL cost, conversion batches, watches, memory, and etcd.

`required` means a property must be present; it does not necessarily mean a string is non-empty, a list has members, or a number is positive. Add the appropriate `minLength`, `minItems`, or numeric bound. Treat absence, explicit `null`, empty, zero, and default as separate semantic states. Nullable fields should be rare and justified.

Use formats for syntactic interoperability where supported, but validate domain meaning too. Avoid overly clever regular expressions and schema combinations that client generators or Kubernetes structural rules cannot represent consistently.

### Declare list and map topology deliberately

Kubernetes merge and Server-Side Apply semantics depend on structural topology. A list may be atomic, set-like, or map-like keyed by declared fields. A map/object may be atomic or granular. Choose based on ownership and identity, not serialization convenience.

Use a map list for named subobjects such as conditions or ports only when key fields are stable, required, unique, and sufficient for element identity. Use set semantics only when element equality is meaningful and order is irrelevant. Atomic collections transfer/replace ownership as a whole.

Changing topology after clients own fields can alter merge and conflict behavior. Moving atomic to granular does not reconstruct historical fine-grained ownership; reverse changes can consolidate ownership and create conflicts. Treat topology as compatibility surface and migration work.

Document ordering. Set/map lists should not carry semantic order. If priority/order matters, model an explicit numeric key or use an atomic ordered list with single ownership and bounds.

### Choose pruning and unknown-field behavior

By default under v1 structural schemas, fields not specified by the schema are pruned at API processing points. This catches misspellings and prevents unvalidated data from silently becoming controller input. Test the object retrieved after create, not only client-side YAML.

`x-kubernetes-preserve-unknown-fields: true` opts a subtree out of pruning until a nested schema restarts pruning. Use it for a genuinely opaque extension/provider payload only after defining size, security, conversion, ownership, compatibility, and controller handling. It is not a substitute for designing fields.

Unknown preserved data is harder to validate, convert, query, generate clients for, and manage granularly. CEL cannot access unknown data. A controller that deserializes it into arbitrary runtime types inherits injection and resource-exhaustion risks.

When replacing an opaque subtree with typed fields, inventory real stored shapes first. Introducing a schema can prune data on future writes; conversion and migration must preserve or explicitly disposition it.

### Design defaults as API behavior

Defaults reduce repetitive intent but change semantic interpretation. Apply only deterministic, context-free schema defaults that are safe for every object in the version. User/tenant/policy-dependent choices belong in admission or reconciliation with recorded provenance, not static schema defaults.

Defaulting occurs when objects are processed by the API, and defaulted values are persisted on write. Updating a CRD default does not automatically rewrite existing objects. Reads of older stored objects and controller decoding can therefore encounter absent fields.

Controllers must handle absent legacy values consistently with version semantics. If absence means “automatic,” do not default it to a fixed value merely for code convenience. If zero is valid, pointer/nullable modeling may be needed in generated types to distinguish omission.

Changing a default for new writes can be compatible syntactically while producing different cost, security, or availability. Version or explicitly migrate consequential defaults, and show effective state in status or preview.

### Layer validation by cost and authority

Use schema constraints first for local type, enum, range, pattern, length, collection, and required-field rules. They are discoverable through OpenAPI and avoid an external availability dependency.

Use CRD CEL validation for cross-field invariants and old/new transition rules that can be evaluated from the admitted object. CEL is non-Turing complete and subject to estimated/runtime cost budgets, but expressions still need bounded input schemas and review. Give rules stable, actionable messages and test boundary inputs.

Transition rules using `oldSelf` can enforce immutability, monotonic changes, or safe state transitions. Account for create, deletion, old objects, defaulting, and version conversion. Do not freeze a field that operators must repair during disaster recovery without an authorized recovery route.

Use validating admission policies/webhooks for policy depending on request identity, namespace policy, other resources, or external decision. Prefer in-process schema/CEL where it expresses the invariant. A webhook adds latency and failure behavior to API writes; scope it narrowly, use short timeouts, define failure policy from risk, and avoid recursive dependencies.

Mutation should be deterministic and idempotent. Multiple mutators may interact or reinvoke. Never rely on webhook order for a safety invariant; validate the final admitted object.

### Evolve validation without trapping stored objects

Let $V_{old}$ and $V_{new}$ be valid representation sets. Adding a required field without a default, narrowing an enum/range, making a transition immutable, or changing list keys can make $V_{new}\subset V_{old}$. Stored objects accepted under the old schema may then be unwriteable or unconvertible.

Before tightening, list and evaluate every stored object plus representative backups. Remediate invalid objects under the old rules, add a compatible version/default/conversion, or use validation-ratcheting behavior only after understanding its precise support and limits. Do not assume it covers every CEL or structural change.

Preserve an emergency repair path. Validation that rejects both current invalid state and any incremental move toward valid state creates a trap. Transition rules can allow monotonic repair while blocking new regression.

Test clients that omit new optional fields, old controllers writing old shapes, apply/patch ownership, delete/finalizer updates, status writes, restore, and downgrade. Admission compatibility includes every lifecycle verb, not only create.

### Separate spec and status

Enable the status subresource when controllers report observation. Writes to `/status` should not change consumer spec, and ordinary spec updates should not let clients overwrite controller status. Define RBAC separately.

Status should include conditions with observed generation, stable reasons, active/effective revision, references to non-secret results, and bounded summaries. It should be reconstructable from the world where practical; avoid storing large histories or authoritative user input only in status.

Understand generation behavior for the resource and subresource. A consumer spec change should advance desired generation; a status update should not create apparent new intent. Conversion must preserve spec/status meaning across versions.

Do not copy secret values, provider credentials, large logs, or unbounded child inventories into status. Reference protected resources and use events/logs/traces or separate bounded resources for history.

### Expose standard auxiliary surfaces only when semantic

Enable `/scale` only if the resource truly has desired replicas, observed replicas, and optionally a label selector with compatible paths. This integrates autoscaling and generic clients, but it also creates another writer and ownership handoff for replicas. Do not map “capacity tier” or database nodes to replicas when scaling has non-equivalent semantics.

Additional printer columns improve diagnosis but are a display contract. Use stable JSONPaths, bounded values, meaningful type/priority, and columns that remain correct across versions. Do not expose secrets or ambiguous green summaries.

Selectable fields can reduce broad client lists for declared scalar paths. Choose stable, low-surprise fields and measure index/storage/API cost. Field selectors support a limited operator set; they are not a general query language. Labels remain appropriate for mutable grouping controlled by users/controllers under clear ownership.

Categories and short names affect discovery and human tooling. Treat them as shared namespace with collision and load implications rather than cosmetics.

### Design version representations around a hub model

An API version is a complete external representation and stability promise, not just a schema copy. During evolution, several versions may be served while exactly one is marked storage. The preferred discovery version follows version ordering rules and may influence client behavior.

Define a semantic hub/internal model even if conversion code directly maps pairs. For every field record its meaning in each version, default, losslessness, and canonical representation. Conversion should be deterministic, side-effect-free, and independent of mutable cluster/provider state.

`None` conversion only changes `apiVersion` and is safe only when representations have identical compatible structure/meaning. Renaming `spec.hostPort` to `spec.host` plus `spec.port` requires real conversion. A webhook receives batches and must preserve order and immutable identity metadata according to the API contract.

Round-trip fixtures cover all valid and historically stored shapes, including unknown/preserved fields, null/absent/default, list ordering/topology, status, deletion timestamp/finalizers, and future-version data. Canonicalization may normalize representation, but must not lose promised information.

### Operate conversion as a control-plane dependency

The API server can call conversion for reads, writes, lists, and watches when requested and storage versions differ. An unavailable or incorrect webhook can prevent clients from reading, updating, or deleting custom resources. Validation rejection does not belong in conversion.

Deploy conversion before configuring the CRD to need it. Provide highly available endpoints, TLS trust rotation, narrow network reachability, authentication appropriate to the environment, short predictable execution, bounded object/batch cost, metrics, alerts, and disaster-recovery bootstrap.

Do not have conversion fetch the same custom resource, call its controller, query a provider, or depend on optional workload infrastructure. Such recursion and mutable lookups make identical stored bytes convert differently and can deadlock recovery.

Test API-server skew and `ConversionReview` versions supported by the current/previous server. Preserve request UID, batch order, kind/name/namespace/UID, and return the requested API version. Fail explicitly rather than returning partially transformed objects.

### Migrate storage explicitly

Changing `storage: true` affects future writes. Existing objects remain encoded at versions in which they were last stored. Kubernetes records possible historical storage versions in CRD `status.storedVersions`.

After the new served version and conversion are proven, set it as the sole storage version and run Storage Version Migration or a controlled read/rewrite procedure. Bound concurrency, rate, retries, conflict handling, conversion load, API/etcd capacity, and backup windows.

For $N$ objects and sustained successful rewrite rate $r$, ideal duration is $N/r$. At 600,000 objects and 250 successful rewrites per second, the lower-bound time is 2,400 seconds, or 40 minutes. Real time includes list, conversion, conflicts, throttling, retries, and concurrent writes; validate with production-like load.

Verify every object, migration condition, error, and `storedVersions` result. Do not manually remove an old stored version merely to pass a check unless the objects have actually been migrated. Backups can still contain old bytes, so restore tests must include the conversion/version support needed at recovery time.

### Engineer API-server and storage economics

Estimate object count, serialized size, update rate, watch count/fan-out, list frequency/size, label/selectable indexes, validation/conversion cost, status write rate, and retention/backup impact. Multiply by tenants, clusters, and controllers.

One 500 KiB object updated each second can generate far more shared load than thousands of small mostly static claims. Keep bulky configuration/artifacts in an appropriate store with immutable reference, digest, authorization, and lifecycle; keep the CRD as control metadata.

Bound cardinality with quota/admission and garbage collection. A CRD per tenant or schema per instance multiplies discovery/OpenAPI/controller and operational complexity. Prefer one stable resource with namespaced instances when semantics align.

Controllers should watch narrowly, use indexes, suppress no-op status writes, paginate/resync with jitter, and avoid relisting all objects for one dependency. Measure API request latency/errors, etcd/object size, watch terminations, conversion latency/errors, validation rejection/cost, list payload, and storage-migration progress.

### Secure and govern the API surface

Define RBAC by API group, plural resource, verbs, namespace/cluster scope, and subresources. Grant controllers status and finalizer/effect permissions narrowly. Remember that anyone allowed to write desired state may indirectly invoke powerful provider effects.

Admission should enforce tenant/reference boundaries, quotas, high-consequence choices, and immutable ownership. Avoid secrets in objects, printer columns, status, audit-visible fields, labels, and error messages. Encrypting etcd at rest does not make broad read RBAC safe.

Audit CRD definition/version changes, conversion configuration, high-consequence custom-resource writes, status/scale access where needed, finalizer override, and deletion. Pin ownership, review, support, compatibility, and incident response for both CRD and controller.

Supply-chain review includes generated CRD YAML, controller types/markers, conversion image, certificates, deployment and RBAC. Detect drift between source types, generated manifests, installed CRD, and controller expectations.

### Test the API as clients will experience it

Validate CRD installation against every supported Kubernetes release. Create, get, list, watch, update, patch, apply, status, scale, delete, and recreate objects using dynamic and generated clients. Verify discovery, OpenAPI, printer output, selectors, ownership conflicts, and error messages.

Build golden fixtures from every released version and real stored edge shape. Test defaulting/pruning round trips through the API server, not only schema libraries. Exercise maximum sizes/collections, Unicode, null/absent/zero, invalid transitions, unknown fields, and malicious CEL/input cost.

Test conversion pairwise and through the hub, batch behavior, webhook outage/latency/TLS rotation, API-server restart/skew, storage migration, backup/restore, and rollback/forward recovery. A fake client cannot reproduce all API-server schema, default, pruning, apply, generation, or subresource behavior.

Run controller compatibility tests: old object/new controller, new served version/current controller, status conversion, finalizers/deletion, and external effects. API-schema success without behavioral support is not compatibility.

### Deprecate versions with evidence

Publish stability level, support window, behavioral differences, migration guide, and removal conditions. Avoid promising Kubernetes' own deprecation lifetime automatically applies to your CRDs; adopt and document a platform policy appropriate to consumers.

Serve old and new versions concurrently with working conversion. Inventory manifests, Git repositories, clients, controllers, admission/policy rules, RBAC, dashboards, backups, and live API request metrics/audit. Absence from one source does not prove no client exists.

Migrate stored objects and verify the old entry is absent from `status.storedVersions`. Then set old `served:false` while retaining a rollback window, observe breakage, and only later remove the version and its conversion tests/code.

Never use conversion failure as a deprecation enforcement mechanism. It can block reads and deletion, including recovery from the deprecation itself.

### Retire a CRD as a destructive migration

Deleting a CRD removes its API endpoint and can delete stored custom-resource instances. It does not prove controllers stopped, external effects were removed, backups were updated, RBAC/policies disappeared, or clients no longer submit objects.

Stop new creation, inventory every instance/effect/finalizer/dependency, and choose migrate, delete, or explicitly orphan for each. Complete reconciliation and export required records before removing the controller or API. Test restore into the intended successor environment.

Remove instances under verified disposition, then controllers, webhooks/conversion, admission, RBAC, quotas, policies, discovery-dependent clients, dashboards/alerts, backups/restore rules, certificates, images, and finally the CRD. Retain non-executable audit evidence as required.

Confirm no GitOps source or disaster-recovery bundle will reinstall the CRD and recreate effects. Retirement is a system property, not `kubectl delete crd` succeeding.

### Use an executable CRD lifecycle inventory

The following synthetic inventory counts foundational properties across ten API lifecycle scenarios. It does not validate a real schema, CEL expression, conversion function, cluster, controller, authorization policy, performance limit, migration, or recovery plan.

<!-- bijux-verify: {"id":"custom-resource-definition-lifecycle-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scenarios 10\ndomain_fit 10\nstructural_bounded 9\nsemantics_documented 9\nvalidation_evolvable 9\nconversion_roundtrip 8\nstorage_migrated 8\nsubresources_owned 9\nauthorization_scoped 9\nload_tested 8\nretirement_tested 8\n","stderr":""}} -->
```python
scenarios = [
    ("initial-install", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("create-update", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("status-scale", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("field-apply", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("schema-tightening", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("version-conversion", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("storage-migration", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("backup-restore", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("legacy-opaque-field", 1, 0, 0, 0, 0, 0, 1, 1, 0, 0),
    ("forced-retirement", 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
]
fields = [
    "domain_fit", "structural_bounded", "semantics_documented",
    "validation_evolvable", "conversion_roundtrip", "storage_migrated",
    "subresources_owned", "authorization_scoped", "load_tested",
    "retirement_tested",
]
print("scenarios", len(scenarios))
for index, field in enumerate(fields, start=1):
    print(field, sum(scenario[index] for scenario in scenarios))
```

The opaque legacy field must not be silently pruned or promoted to a stable contract. Forced retirement remains incomplete until version/storage, subresource, authorization, load, effect, backup, and resurrection consequences are explicitly dispositioned.

## Definitions and Notation

- $v$: an external API version such as `v1beta1` or `v1`.
- $V_v$: set of representations accepted by version $v$ under schema, defaulting, and admission assumptions.
- $C_{a\rightarrow b}$: deterministic conversion from representation/version $a$ to $b$.
- $x$: one custom-resource object representation, including relevant spec, status, metadata, and preserved data.
- $N$: number of objects to inventory or rewrite during storage migration.
- $r$: sustainable successful rewrite rate in objects per second after limits.
- $D$: effective migration deadline or available window; ideal feasibility requires $N/r\leq D$.
- $s$: mean serialized object size; $Ns$ is a lower-bound snapshot payload before indexes, revisions, and backups.
- $u$: object update rate; $Nu$ is aggregate base update rate only under a homogeneous population.
- **served version**: client-addressable representation exposed at its API path.
- **storage version**: sole version chosen for new persistence writes.
- **structural schema**: OpenAPI schema shape satisfying Kubernetes structural requirements and extensions.
- **canonicalization**: documented normalization that preserves semantics even when bytes/order differ.
- **behavioral compatibility**: controllers and policies preserve promised outcomes, beyond schema acceptance and conversion.

## Mechanisms, Invariants, or Proof Structure

1. Establish that the domain object is low-rate durable control intent suited to Kubernetes rather than application data or a command stream.
2. Choose durable group/resource/kind, namespaced or cluster scope, UID-based identity, ownership, and lifecycle.
3. Specify consumer-owned intent and references without provider manifests, secrets, or workflow commands.
4. Build a structural bounded schema with explicit presence/null/zero, collection topology, pruning, and narrow unknown preservation.
5. Add deterministic defaults and schema/CEL/admission validation with stored-object and recovery compatibility.
6. Define status and optional scale/printer/selectable surfaces with separate ownership and stable semantics.
7. Model each version against a semantic hub; prove fixture round trips and operate conversion as a critical API dependency.
8. Change storage only with bounded object rewrite, conflict/error evidence, `storedVersions` verification, and backup/restore support.
9. Scope RBAC/admission/quota/audit and capacity-test object count/size, writes, lists, watches, validation, conversion, and migration.
10. Test real API-server behavior and old/new clients/controllers across CRUD, watch, apply, subresources, deletion, skew, outage, restore, and downgrade.
11. Deprecate from measured client/storage migration and retire instances/effects/controllers/webhooks/policy/recovery before deleting the CRD.

For concurrently served $a$ and $b$, round-trip equality $C_{b\rightarrow a}(C_{a\rightarrow b}(x))=x$ is required only up to documented canonicalization and for information promised in $a$. If $b$ contains fields that $a$ cannot represent, losslessness needs an equivalent representation or preserved carrier; merely dropping those fields violates the promise for a $b\rightarrow a\rightarrow b$ path.

The migration expression $N/r$ is an ideal lower-bound duration at sustained successful throughput. It omits enumeration, object size, conversion, conflicts, throttling, retry, status writes, concurrent mutation, API/etcd headroom, and verification.

## Alternatives and Trade-Offs

- **CRD versus aggregated API:** CRDs reuse API machinery and storage; aggregation enables custom semantics/storage with a larger operated API-server surface.
- **CRD versus external service API:** Kubernetes integration simplifies control resources; external services better fit high-rate data, queries, transactions, and independent availability.
- **Namespaced versus cluster scope:** namespace scope composes with ownership/RBAC/quota; cluster scope fits genuine cluster singletons but concentrates privilege and lifecycle.
- **Typed fields versus opaque extension:** typed schemas improve validation, clients, ownership, and conversion; opaque data preserves flexibility at safety/evolution cost.
- **Prune versus preserve unknown:** pruning catches mistakes and bounds interpretation; preservation supports plugins/pass-through but hides semantics from validation.
- **Static default versus policy derivation:** schema defaults are fast/deterministic; admission/reconciliation can use context but adds provenance and availability concerns.
- **OpenAPI versus CEL versus webhook:** local constraints are simplest; CEL expresses cross-field/transition logic; webhooks reach external context but join the critical path.
- **Atomic versus granular collection ownership:** atomic topology simplifies single-owner replacement; map/set/granular topology supports collaboration with stable identity complexity.
- **One stable version versus simultaneous versions:** one reduces matrices; overlap permits migration and compatibility evidence.
- **None versus webhook conversion:** `None` avoids dependency when shapes are identical; webhook supports semantic transformation at API availability/correctness cost.
- **Eager versus gradual storage migration:** eager rewrite shortens old-format exposure; gradual migration reduces peak load but prolongs conversion/recovery obligations.
- **Status summary versus detailed history:** bounded status aids automation; history belongs in events/logs/operation resources to protect API size/write load.
- **Labels versus selectable fields:** labels provide flexible grouping with ownership; selectable fields query stable schema paths but expand indexing/API commitments.
- **Immediate version removal versus observed deprecation:** removal reduces code; measured overlap protects unknown clients, stored data, backups, and recovery.

## Failure Modes and Misconceptions

- **“A CRD is just a YAML schema.”** It creates a REST, storage, discovery, RBAC, admission, watch, conversion, backup, and lifecycle contract.
- **“Put any data in Kubernetes for consistency.”** High-rate or bulky application/telemetry data harms shared control-plane economics and usually needs different storage semantics.
- **“Cluster-scoped means globally reusable.”** It also means cluster-wide identity/authorization/lifecycle and can weaken tenant boundaries.
- **“Required means meaningful.”** Present empty strings, empty lists, zero, or null may still violate domain meaning without constraints.
- **“Unknown fields are future compatibility.”** They can hide misspellings and unvalidated controller inputs; preservation needs a bounded extension contract.
- **“Defaults update old objects.”** CRD changes do not rewrite stored instances; absent legacy fields remain a controller/conversion concern.
- **“CEL replaces schema bounds.”** Runtime and estimated cost controls help, but bounded typed inputs and simple rules remain necessary.
- **“A webhook can validate conversion.”** Conversion failures can block reads/deletes; validation belongs at admission with compatible version design.
- **“None conversion works if JSON is valid.”** It only changes `apiVersion`; renamed or semantically changed fields need transformation.
- **“Changing storage migrates objects.”** It changes subsequent writes; existing encodings remain until rewritten.
- **“`storedVersions` can be patched away.”** That status should reflect completed migration, not substitute for it.
- **“Schema compatibility proves API compatibility.”** Controllers, policies, defaults, field ownership, errors, and outcomes can still change.
- **“Status is harmless metadata.”** Clients automate from it; stale, secret, unbounded, or version-losing status causes real harm.
- **“Scale fits every capacity field.”** Generic replica semantics can be false for databases, shards, or tiers and introduce conflicting writers.
- **“Namespaces provide complete multi-tenancy.”** They help scope names/RBAC/quota but do not alone isolate shared controllers/providers or cross-namespace references.
- **“Deleting the controller is safe if the CRD remains.”** Finalizers and effects can strand; status and lifecycle promises stop being fulfilled.
- **“Deleting the CRD cleans everything.”** API records may disappear while external effects, credentials, policies, backups, and clients remain.
- **“No live requests means no old clients.”** Git sources, dormant automation, disaster recovery, and backups can reintroduce the version.

## Worked Examples

### Example 1

A team proposes one CR per log event. Estimated writes and retention would dominate the cluster API, so the design keeps a low-rate `LogSink` intent CRD and sends events to a log system. Conclusion: control intent and application data need different stores.

### Example 2

`spec.region` is marked required but accepts `""`. Adding `minLength: 1` and an enum/policy validation closes the semantic hole. Conclusion: presence is not validity.

### Example 3

A user misspells `recoveryTier` as `recoveryTeir`; pruning removes it and the retrieved object shows the default tier. Server-side dry run and strict client validation expose the error before production. Conclusion: verify admitted state, not submitted bytes.

### Example 4

Two managers edit an atomic list of endpoints and conflict over the whole list. Redesigning it as a map list keyed by stable endpoint name enables granular ownership. Conclusion: schema topology determines merge authority.

### Example 5

A new maximum rejects legacy objects above the limit, including attempts to reduce them. An audited transition rule allows decreases until valid while blocking increases. Conclusion: validation evolution needs a repair path.

### Example 6

`v1beta1.spec.hostPort` becomes `v1.spec.host` and `port`. `None` conversion loses meaning, so a side-effect-free webhook and fixtures implement both directions. Conclusion: version labels do not transform data.

### Example 7

Conversion calls a provider to infer region; provider outage makes `kubectl get` and deletion fail. The mapping is redesigned to use only object data with explicit region preserved across versions. Conclusion: conversion is an API critical path, not reconciliation.

### Example 8

Six hundred thousand objects migrate at a measured 250 successful rewrites per second. The ideal 40 minutes becomes 58 under conflicts and throttling; canary rate limits preserve API headroom. Conclusion: $N/r$ is only a lower-bound plan.

### Example 9

An autoscaler writes `/scale`, while the controller also defaults replicas on every reconcile. Field ownership oscillates. An explicit handoff makes the autoscaler the replica owner while enabled. Conclusion: standard subresources create real multi-writer contracts.

### Example 10

A CRD is deleted before its instances and controller are dispositioned. API objects vanish, but cloud databases continue billing and backups later reinstall the CRD. Conclusion: CRD retirement must cover effects and resurrection paths.

## Cross-Program Connections

- **API engineering:** resources, representations, schemas, compatibility, deprecation, errors, idempotency, and long-running operations define the public contract.
- **Programming languages/type systems:** structural types, optionality, nullability, sums/enums, refinement predicates, and canonicalization shape safe representations.
- **Database systems:** storage schemas, online migration, indexes, optimistic concurrency, serialization, backup, and restore govern persisted objects.
- **Distributed systems:** conversion availability, mixed versions, watches, partial failure, stale clients, retries, and eventual migration create cross-node state.
- **Data structures:** atomic/set/map lists and stable keys determine merge behavior, indexing, traversal, and payload bounds.
- **Security engineering:** RBAC, admission, tenant/reference scope, indirect effect authority, secrets, audit, and supply chain protect extension power.
- **Reliability engineering:** API critical paths, overload, bounded cost, canaries, rollback/forward recovery, and disaster restore keep extension failure contained.
- **Platform engineering:** CRDs can provide a common declarative capability contract, but provider fields and controller steps leak the abstraction.
- **Systems engineering:** requirements, interface control, configuration baselines, verification matrices, change control, lifecycle, and disposal apply directly.
- **Organizational design:** API group ownership, review, support, field authority, deprecation communication, and incident roles must match team boundaries.

## References

1. Kubernetes Authors, “Custom Resources,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
2. Kubernetes Authors, “Extend the Kubernetes API with CustomResourceDefinitions,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/
3. Kubernetes Authors, “Versions in CustomResourceDefinitions,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/
4. Kubernetes Authors, “Migrate Kubernetes Objects Using Storage Version Migration,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/tasks/manage-kubernetes-objects/storage-version-migration/
5. Kubernetes Authors, “Storage Versions,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/overview/working-with-objects/storage-version/
6. Kubernetes Authors, “CustomResourceDefinition,” current API reference, retrieved 2026-09-02. https://kubernetes.io/docs/reference/kubernetes-api/apiextensions/custom-resource-definition-v1/
7. Kubernetes Authors, “Common Expression Language in Kubernetes,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/cel/
8. Kubernetes Authors, “Dynamic Admission Control,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/
9. Kubernetes Authors, “Admission Webhook Good Practices,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/
10. Kubernetes Authors, “Server-Side Apply,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/server-side-apply/
11. Kubernetes Authors, “Field Selectors,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/
12. Kubernetes Authors, “Kubernetes Deprecation Policy,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/deprecation-policy/
13. Kubernetes SIG Architecture, “API Conventions,” current repository documentation, retrieved 2026-09-02. https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
14. JSON Schema Project, “JSON Schema Validation: A Vocabulary for Structural Validation of JSON,” Draft 2020-12, June 2022. https://json-schema.org/draft/2020-12/json-schema-validation

## Exercises

### Exercise 1

Decide whether each belongs in a CRD: database intent, individual audit events, a reusable network policy profile, 10 MiB application configuration blobs, deployment operations, and global platform policy. Justify scope, storage, lifecycle, and alternatives.

### Exercise 2

Design the structural schema for a namespaced `DatabaseClaim` with engine, region policy, recovery tier, capacity, maintenance windows, parameters, and dependency references. Address bounds, required/empty/null, list topology, pruning, defaults, validation, status, and secrets.

### Exercise 3

Plan `v1beta1` to `v1` evolution where `hostPort` splits into `host` and `port`, a field becomes immutable, and a new optional policy appears. Specify hub semantics, round trips, conversion operation, webhook failure, client overlap, and downgrade.

### Exercise 4

A cluster holds 900,000 objects. A tested migration sustains 300 successful rewrites per second, with 20% additional time reserved for conflicts/throttling and a two-hour window. Compute ideal and reserved duration and headroom; list omitted capacity risks.

### Exercise 5

Design a deprecation and retirement plan for a CRD with two served versions, an old storage version, conversion and admission webhooks, finalizers, external resources, GitOps clients, RBAC/policies, and backup/restore bundles.

## Answers to the Exercises

### Answer 1

Database intent fits a CRD when it is low-rate, durable, namespaced control state reconciled to a provider. Individual audit events do not: use an append-only audit/event store and perhaps a low-rate `AuditSink` CRD. A network policy profile can fit a CRD if it has durable reusable semantics and a controller/policy consumer; first check whether built-in NetworkPolicy or policy configuration suffices. Ten-mebibyte application blobs belong in object/artifact/config storage with immutable digest/reference; a CRD may hold the small authorized reference. Deployment operations can be immutable durable operation resources if each attempt/outcome must be independently tracked, but ordinary desired deployment belongs in a long-lived resource rather than a watch-command edge. Global platform policy may be cluster-scoped only when genuinely cluster-wide; organizational/global policy may need an external authority distributed into clusters. Each choice includes owner, rate/size, authorization, backup, reconciliation, deletion, and alternative API analysis.

### Answer 2

Use a DNS-owned group, namespaced scope, and a structural object schema. Require non-empty engine and recovery tier with supported enums; model region as a bounded policy enum plus a bounded non-empty allowed-region set/map rather than provider syntax. Capacity uses explicit units and numeric minima/maxima; distinguish omitted automatic sizing from zero, which is rejected. Maintenance windows form a bounded map list keyed by stable name, with validated day/time/duration and a CEL non-overlap rule only if cost remains bounded. Parameters are a bounded typed map of documented keys or a narrowly preserved opaque subtree only if a real extension contract exists. References include kind/group/name and restricted namespace behavior. Safe context-free defaults may select a low-risk recovery tier, but consequential cost/region policy is previewed and admitted with provenance. CEL enforces cross-field engine/capacity and immutable identity transitions with a repair path. Prune unknown top-level fields. Status subresource reports observed generation, conditions, active class/revision, provider ID and secret endpoint reference—not credentials. Bound object/collection sizes and test maximum CEL/conversion cost.

### Answer 3

Define a hub with separate host string and bounded integer port plus optional policy whose absence retains beta behavior. Beta-to-hub parses `hostPort` unambiguously; hub-to-beta joins it canonically and preserves the new policy through an equivalent beta field or an explicitly supported preserved carrier if beta round trips must retain it. If no lossless carrier exists, do not claim full round-trip support for new objects through beta; delay the field, extend beta compatibly, or restrict the supported path. Enforce immutability at admission after conversion with create/old-object and emergency-repair tests. Deploy a deterministic side-effect-free highly available conversion webhook before enabling `v1`; test batch order, UID/metadata preservation, TLS, timeout, current/previous `ConversionReview`, outage, and API reads/deletes. Serve both versions, migrate clients, then storage. Old clients remain supported during the published overlap. Downgrade tests prove old API servers/controllers and conversion code can read state already written, or the plan declares forward recovery instead.

### Answer 4

Ideal duration is $900{,}000/300=3{,}000$ seconds, or 50 minutes. Reserving 20% additional time gives $3{,}600$ seconds, or 60 minutes. A two-hour window therefore has 60 minutes of nominal headroom. This is not capacity proof: listing and pagination, object size, conversion/CEL CPU, API/etcd latency, watch amplification, concurrent writes, conflicts beyond reserve, provider/controller status writes, throttling, retry synchronization, backups, storage compaction, admission webhooks, API-server skew, failures, and post-migration verification are omitted. Canary the rate, preserve control-plane headroom, monitor tail latency/errors and `storedVersions`, and define stop/resume.

### Answer 5

Inventory live/dormant clients through API metrics/audit, Git sources, generated clients, controllers, policies, RBAC, dashboards, automation, and recovery bundles. Introduce the replacement version with structural schema and proven round-trip conversion; deploy conversion independently and keep admission compatible. Migrate clients/controllers while both are served. Mark the new version storage and perform a bounded verified rewrite of every object; prove the old version left `status.storedVersions`, including restored-backup tests. Set old `served:false` during a reversible observation window, then remove it only after no valid consumer remains. Stop new instance creation before CRD retirement. For every instance, complete or explicitly transfer/delete/orphan external effects and finalizers while controllers still have authority. Remove GitOps sources, controllers, conversion/admission webhooks, RBAC, quotas/policies, alerts, certificates, images, backups/restore rules, and recovery manifests in dependency order. Delete the CRD last, verify its API/instances are absent and external inventories are dispositioned, and ensure old backups cannot reinstall it or recreate effects.
