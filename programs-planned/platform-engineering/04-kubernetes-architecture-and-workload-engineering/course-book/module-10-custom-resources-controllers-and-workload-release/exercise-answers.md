# Worked answers

## 1. When is a custom resource justified?

When users need a stable domain-oriented declarative API, several lower-level objects must be composed consistently, status must summarize the capability, and a controller owns reconciliation/lifecycle. YAML abbreviation alone is not sufficient. Built-ins and configuration should be preferred where they express the invariant.

## 2. Why must a CRD schema be structural and specific?

Clients, API validation, pruning, defaulting, conversion, and tools need a predictable shape. A loose object with arbitrary fields moves errors into controller code and makes compatibility impossible to reason about. Preserve unknown fields only in a narrow intentionally opaque subtree.

## 3. What is the purpose of observedGeneration in AtlasWorkload status?

It states which spec generation the controller evaluated. Without it, Available=True could refer to an older image/configuration. The controller sets it only after processing the current generation and calculates conditions from current children.

## 4. Why should the controller not copy every child status field?

It creates duplication, staleness, and a large unstable API. Custom-resource status should summarize domain-relevant state and link to children for detail. The child objects remain authoritative for controller-specific fields.

## 5. Why must reconciliation be idempotent?

Queue items and watch events repeat, controllers restart, and partial effects occur. Reprocessing the same desired state must converge on the same child set and external effects. Stable names, owner references, apply ownership, and inspectable external state support this property.

## 6. How does status timestamp churn create a loop?

Each reconcile writes a new timestamp even though semantic state is unchanged. That update generates another event, causing another reconcile and write. Compare semantic status and update transition time only when condition state changes.

## 7. Which fields should the Atlas controller own?

Generated child selectors, template fields derived from the CR, owner references, and AtlasWorkload status. It should not own user spec, external ConfigMap/Secret content, independently managed PVCs, or future autoscaler fields unless the API contract explicitly transfers ownership.

## 8. Why is cluster-admin inappropriate for the controller?

The controller reconciles namespaced Atlas resources and selected child types. Cluster-admin would allow unrelated mutation and turn compromise into cluster-wide control. RBAC should enumerate required verbs/resources/subresources and be tested negatively. Course 8 deepens this threat model.

## 9. When should a finalizer be used?

Only for a real obligation that must complete before object deletion and is not already represented by owner references/garbage collection. Cleanup must be idempotent, observable, and support break-glass. Ordinary child deletion does not justify a custom finalizer.

## 10. Why is a single controller replica honest in Course 4?

It proves reconciliation semantics without pretending operated high availability. Multiple replicas require leader election or safe concurrent processing, lease handling, upgrades, and availability evidence. Course 9 owns that operational proof.

## 11. Why does the Course 5 handoff include unresolved evidence?

Course 4 can declare port, selector, readiness, DNS, exposure, and egress requirements but has not exercised CNI, Gateway API, network policy, TLS, cloud load balancers, or real failure domains. Marking those unexecuted prevents manifests from being mistaken for connectivity proof.

## 12. What is the strongest final proof in this course?

A complete object/control path tied to exact artifact digests, field ownership, controller idempotency, scheduling/lifecycle evidence, current-generation status, release decision, and successor handoff. Even a kind proof remains local-cluster evidence rather than production fleet proof.
