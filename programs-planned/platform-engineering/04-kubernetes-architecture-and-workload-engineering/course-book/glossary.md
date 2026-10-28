# Glossary

This glossary defines terms as they are used in Course 4. Several words have broader meanings outside Kubernetes; the definitions here preserve the ownership and evidence model of the course.

**Admission** — The API-server stage after authentication and authorization where mutating and validating policy can change or reject a request.

**Available replica** — A ready replica that has remained ready for the Deployment's configured minimum-ready duration.

**Condition** — A typed observation on an API object, normally containing status, reason, message, observed generation, and transition time.

**Controller** — A process that observes API and external state and repeatedly acts to move current state toward declared desired state.

**Controller owner reference** — The single controlling lifecycle relationship used by garbage collection and controller adoption rules.

**Custom resource** — An API resource added to Kubernetes through a CRD or aggregated API server.

**Desired state** — The intent declared by an authorized actor, usually under `spec`.

**Disruption** — Interruption of a workload instance. Kubernetes distinguishes voluntary disruption, which PDBs can constrain, from involuntary failure.

**Field manager** — An identity recorded by Server-Side Apply as owning selected object fields.

**Finalizer** — A string that keeps deletion pending until the responsible actor completes or deliberately abandons cleanup.

**Generation** — A monotonically changing number associated with changes to desired-state fields for resources that implement it.

**Idempotent reconciliation** — Reprocessing the same desired and observed state without multiplying effects beyond the intended target.

**Image identity** — In this course, repository plus immutable digest, not a mutable tag.

**Kubelet** — The node agent that realizes Pods assigned to its Node and reports local observations.

**Level-triggered reconciliation** — Reconciliation based on current state, not reliance on receiving every individual transition event.

**Liveness** — Evidence that restarting a container is a plausible repair for an irrecoverably unhealthy process.

**Managed fields** — API metadata describing declarative field ownership by field manager and operation.

**Observed generation** — The desired generation a controller reports having processed.

**Owner reference** — Metadata linking a dependent object to an owner for lifecycle and garbage-collection purposes.

**Pod** — Kubernetes' smallest schedulable workload object: one or more containers sharing selected namespaces, lifecycle, and placement.

**Pod phase** — A coarse lifecycle summary such as Pending, Running, Succeeded, Failed, or Unknown; not an application-health verdict.

**Readiness** — Evidence that an instance is eligible for normal traffic or work assignment under the declared service model.

**Reconciliation** — The repeated comparison and action process by which a controller tries to converge current state on desired state.

**ReplicaSet** — A controller-owned resource that maintains a selected population of Pod replicas, normally managed by a Deployment.

**Request** — CPU or memory amount used by scheduling and resource accounting as declared workload demand.

**Resource version** — An opaque version used for optimistic concurrency and consistent watch/list semantics; it is not a timestamp.

**Rollout** — Controlled transition between workload templates, including creation, availability assessment, and old-replica removal.

**Scheduler** — The control-plane component that assigns unscheduled Pods to feasible Nodes.

**Selector** — A label query defining an object population. Controller selectors are ownership boundaries and should not overlap accidentally.

**Server-Side Apply** — Declarative API change mechanism that records field ownership and reports conflicts.

**ServiceAccount** — A namespaced Kubernetes identity selected by Pods and used for API or workload-identity projection.

**Startup probe** — A probe that delays liveness and readiness processing until startup is declared complete.

**Status** — Server- and controller-owned observations of current state. Status is not a second desired-state channel.

**StatefulSet** — A workload controller for replicas requiring stable ordinal identity, stable network identity, stable per-replica storage association, or ordered lifecycle.

**Topology spread** — Scheduling constraints that control skew across labelled topology domains.

**UID** — Server-assigned object identity that distinguishes two resources with the same name across deletion and recreation.

**Watch** — A stream of API changes after a list/resource-version boundary. Controllers must recover when watches close or events are missed.

**Workload identity** — Short-lived, narrowly scoped authority projected to a workload, distinct from Node identity and image identity.
