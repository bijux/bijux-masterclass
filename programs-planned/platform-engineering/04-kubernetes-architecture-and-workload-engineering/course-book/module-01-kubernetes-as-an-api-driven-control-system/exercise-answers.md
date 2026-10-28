# Worked answers

## 1. A Deployment exists but no ReplicaSet appears. Where should diagnosis begin?

Begin with the Deployment object and the Deployment-controller transition. Confirm the admitted Deployment, generation, selector, and conditions, then verify that the controller manager is running and authorized. Pod logs are irrelevant because no Pod-producing child exists. The decisive evidence is the server-returned Deployment plus controller-manager logs or metrics showing whether reconciliation occurred. A healthy API server proves persistence only; it does not prove the Deployment controller is operating.

## 2. Why is a Kubernetes controller expected to be level-triggered rather than dependent on every watch event?

Watches are delivery optimizations, not durable event logs. Connections close, events can be compacted, processes restart, and duplicate notifications occur. A level-triggered controller re-lists current state and computes the difference from desired state, so missing or repeated notifications do not corrupt the result. The residual risk is an external side effect that cannot be inspected or made idempotent; that effect needs its own durable identity and reconciliation record.

## 3. Which component starts an Atlas container after a Pod is created?

The API server persists the Pod, the scheduler selects and binds a Node if no node is assigned, and the kubelet on that Node asks the container runtime to realize the Pod. Saying “the Deployment starts the container” collapses several ownership boundaries. The evidence should show Pod creation, binding, kubelet observation, image resolution, and container state. Failure at each stage produces different conditions and events.

## 4. What continues if the scheduler is unavailable?

Already bound Pods can continue under their kubelets, and controllers can still create new unscheduled Pods. Those Pods remain Pending because no scheduler records a binding. Existing application availability may therefore look normal while replacement capacity silently degrades. The decisive evidence is Pods with no `spec.nodeName` and scheduling conditions/events, not merely the scheduler process status.

## 5. Why should application code never read etcd directly?

etcd is storage behind the Kubernetes API, not an application integration surface. Direct access bypasses API validation, authorization, admission, version conversion, watch semantics, and compatibility guarantees. It also couples the application to internal key layout. The supported object is the Kubernetes API resource. etcd backup and restore are cluster-operator responsibilities, not a shortcut for workload state access.

## 6. How can desired and observed state differ without indicating a bug?

Reconciliation is asynchronous. After a desired replica change, controllers, scheduler, image pulls, startup, and readiness take time. The gap becomes a failure when it exceeds a declared budget, violates a terminal constraint, or produces a stalled condition. Evidence must include timestamps, generation, controller observations, and the specific transition still pending. Immediate equality is not the contract.

## 7. What is wrong with a controller that creates one child on every event?

Events may be duplicated, replayed, or observed after restart. An event-driven “create one” action multiplies children. A reconciler should count or identify owned children and create only the missing target. The object graph and stable child identity are the oracle. External effects need the same treatment: inspect current effect state or use a durable idempotency key.

## 8. Why are owner references and managed fields different?

Owner references describe lifecycle and garbage-collection relationships between objects, including the controlling owner. Managed fields describe which actor owns individual fields on one object under server-side apply. A Deployment can own a ReplicaSet while a GitOps manager owns the Deployment image field and an autoscaler owns replicas. Confusing the two leads either to orphaned children or field conflicts.

## 9. The API server accepted a Pod. What has not yet been proved?

Acceptance proves the object passed the API boundary and was persisted. It does not prove scheduling, node availability, image pull, mount success, container startup, probe success, readiness, or connectivity. The next decisive evidence is the Pod scheduling condition and binding, followed by kubelet-reported container states and probe outcomes.

## 10. Why can deleting a Pod hide the cause of a workload failure?

Deletion destroys or shortens access to the exact object status, container termination details, events, scheduling condition, and owner graph that explain the failure. A controller may immediately replace the Pod, producing a different object and UID. Preserve YAML/JSON, events, logs, and timestamps first. Deletion is a state mutation, not a diagnostic method.

## 11. What does a kind proof establish and what does it not establish?

A pinned kind cluster exercises a real API server, etcd, scheduler, controllers, kubelets, and container runtime in a local containerized topology. It can prove actual object admission and controller behavior for that version. It does not prove managed-cloud integrations, multi-zone failure, production CNI/CSI behavior, representative capacity, or operated upgrades. Those limitations must remain in the evidence record.

## 12. Why does Course 4 include a ClusterIP Service but defer networking?

A stable workload handoff needs a named port and service identity, and controllers may need a Service reference. Creating the object does not teach how packets traverse CNI, kube-proxy or eBPF dataplanes, DNS, Gateway API, TLS, NetworkPolicy, egress, or cloud load balancers. Course 4 records the contract; Course 5 owns the connectivity mechanisms and their failure evidence.
