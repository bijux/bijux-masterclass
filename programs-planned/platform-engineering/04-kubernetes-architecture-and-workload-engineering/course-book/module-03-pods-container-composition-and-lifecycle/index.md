# Module 3 — Pods, container composition, and lifecycle

A Pod is the smallest Kubernetes scheduling unit. It is not just a container wrapper and not a durable application identity. It is an API object that groups one or more containers into one placement, network, and lifecycle boundary. Controllers normally create Pods from templates because Pods are disposable realizations of higher-level desired state.

The central design decision is what must share fate closely enough to belong in one Pod.

## The Pod as an atomic placement unit

All regular containers in a Pod are scheduled to the same Node. They share a network namespace and can communicate through loopback. They can share volumes. They are created and terminated under one Pod lifecycle.

This co-location is useful when components must share:

- one network identity;
- one mounted volume with tightly coupled lifecycle;
- one scheduling decision;
- one termination boundary.

It is harmful when components need independent scaling, release, availability, or security policy. Atlas API and worker are separate Deployments, not two containers in one Pod, because they scale and fail independently.

## The sandbox and runtime realization

After scheduling, the kubelet creates a Pod sandbox through the container runtime. The sandbox anchors shared namespaces and networking. Containers are then created from the declared image, commands, environment, mounts, resources, and security context.

Course 3 already released exact images. Course 4 uses:

```yaml
image: platform/atlas-api@sha256:6e3b...
imagePullPolicy: IfNotPresent
```

The digest is release identity. `imagePullPolicy` affects retrieval behavior; it does not make a tag immutable. If a registry cannot resolve or authorize the digest, the Pod should fail visibly rather than substitute another artifact.

## Pod composition: init, sidecar, application, ephemeral

### Init containers

Regular init containers run sequentially to completion before application containers start. They are appropriate for bounded setup that is safe to retry. They should not perform a schema migration merely because the Pod started; multiple replicas can run the init concurrently and restarts can repeat it.

### Native sidecar containers

A Kubernetes-native sidecar is expressed as an init container with container-level `restartPolicy: Always`. It starts during initialization and remains running alongside application containers. Sidecars can provide tightly coupled support such as a local proxy or log shipper, but they increase startup, shutdown, resource, and failure complexity.

Do not add a sidecar because “the platform normally has one.” Name the shared-fate requirement. Course 4's base Atlas workload has no mandatory sidecar.

### Application containers

Application containers carry the main Pod work. Pod-level `restartPolicy` governs their container restart behavior. Deployments require `Always`; Jobs use `OnFailure` or `Never` depending on retry evidence.

### Ephemeral containers

Ephemeral containers are added for debugging running Pods. They are not restartable application components and cannot define ordinary ports or probes. Their authority and audit implications matter. Course 8 will govern debug access; Course 4 uses them only as an evidence tool.

## Pod phase is not a complete diagnosis

Pod phases are coarse:

```text
Pending
Running
Succeeded
Failed
Unknown
```

`Running` means the Pod is bound and at least one primary container is running, starting, or restarting. It does not mean ready or healthy. `CrashLoopBackOff` is commonly shown by kubectl as a status summary, but it is not a Pod phase; inspect container state and last termination state.

Useful observations include:

- Pod conditions: `PodScheduled`, `Initialized`, `ContainersReady`, `Ready`;
- container waiting/running/terminated state;
- restart count;
- last termination reason and exit code;
- image and image ID;
- start and finish times;
- events from scheduler and kubelet.

## Restarting a container is not replacing a Pod

The kubelet can restart a failed container inside the same Pod according to restart policy and backoff. The Pod UID, IP, volumes, and node assignment remain.

A workload controller can create a replacement Pod after Pod deletion, eviction, node loss, or template change. The new Pod has a new UID and usually a new IP. Local ephemeral state is not carried automatically.

This distinction changes debugging and idempotency. A worker process may restart several times inside one Pod before the controller ever creates a replacement. The application must tolerate both.

## Pod specifications are intentionally constrained after creation

Many Pod fields are effectively immutable because changing placement, containers, or volume topology in place would make lifecycle and ownership ambiguous. Higher-level controllers replace Pods from a new template instead.

When the Atlas image digest changes, the Deployment creates a new ReplicaSet and new Pods. Editing a live Pod is not the release path.

## Security context preserves the Course 3 runtime contract

The Atlas Pod template declares:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 65532
  runAsGroup: 65532
  seccompProfile:
    type: RuntimeDefault
containers:
- securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities:
      drop: ["ALL"]
```

This preserves known runtime requirements. It does not prove the node's runtime, kernel, LSM, or seccomp implementation is hardened. Course 8 adds admission enforcement; Course 4 verifies that the workload requests the right boundary.

## Writable filesystems must be declared by class

Course 3 identifies:

```text
configuration: /etc/atlas
ephemeral:     /tmp, /run/atlas
durable:       /var/lib/atlas/spool, /var/lib/atlas/results
```

Course 4 maps configuration to read-only projected data, ephemeral paths to `emptyDir`, and durable paths to a PVC interface. It does not use the image writable layer and does not label `emptyDir` durable.

The production-intent worker template uses a PVC. A kind-only controller lab can use `emptyDir` to avoid introducing Course 6 storage machinery, but the overlay is explicitly non-durable and cannot become the release artifact.

## Startup ordering and retry safety

Init containers are retried according to Pod restart behavior. Their actions must therefore be idempotent. Downloading configuration to an `emptyDir` can be safe if content identity is verified and overwrite is atomic. Creating an external database or sending a billing event is not safe without a durable idempotency protocol.

Atlas uses no init container for database migration. Migration ownership belongs to the release workflow, not every Pod startup.

## Termination is a protocol

Pod termination usually involves:

1. deletion or controller replacement begins;
2. the kubelet starts graceful termination;
3. preStop hooks run if configured and time remains;
4. the runtime sends the stop signal, normally SIGTERM;
5. the process drains or stops;
6. after the grace period, remaining processes are killed;
7. Pod status and object deletion complete.

The application must handle SIGTERM, stop accepting new work, finish or checkpoint bounded work, and exit within the declared thirty seconds. A preStop hook does not replace application signal handling; it consumes the same grace budget.

For Atlas API, readiness should become false before long drain work so later networking layers can stop selecting it. Course 5 will examine propagation timing. Course 4 proves the local lifecycle contract.

## Native sidecar shutdown ordering

Native sidecars have lifecycle ordering intended to let application containers finish before sidecars terminate. This is useful for proxies or telemetry helpers, but only when the sidecar model is explicit. A legacy “ordinary container used as sidecar” does not receive the same ordering guarantees.

## Pod failure does not imply application failure—and vice versa

A kubelet can restart a process after OOM or liveness failure even if the external business operation succeeded. Conversely, a process can return successful probes while its durable queue is unavailable if probes are poorly designed. Pod status is platform evidence; application truth still needs a correct contract.

## Atlas Pod templates

The base manifests define separate templates:

- `atlas-api`: port 8080, startup/liveness/readiness probes, three replicas through a Deployment;
- `atlas-worker`: no public port, one replica until Course 6 resolves durable shared state, heartbeat and queue-access readiness;
- `atlas-probe`: diagnostic image used only in bounded labs.

Each template carries digest annotations, release identity, standard labels, resource hypotheses, non-root security context, read-only root, and explicit mounts.

## Worked failure: the migration init container

A team adds a database migration init container to the API Deployment. Three replicas roll out. Each Pod begins the same migration. One process acquires a lock, one waits, and one times out. The Deployment stalls; an operator raises the startup timeout.

The timeout is not the root problem. Migration is a release-scoped finite operation with its own authority, idempotency, rollback, and evidence. It should be a Job or external release step, not an implicit side effect of every Pod creation.

## Capstone increment

`capstone/manifests/base/` receives Atlas Pod templates through Deployments. `atlas_kube/lifecycle.py` models initialization, container restart, Pod replacement, and termination. The lab breaks init ordering and signal cooperation, then distinguishes the object and process identities that survive each transition.

## Further reading

- Pods: <https://kubernetes.io/docs/concepts/workloads/pods/>
- Pod lifecycle: <https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/>
- Init containers: <https://kubernetes.io/docs/concepts/workloads/pods/init-containers/>
- Sidecar containers: <https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/>

## Transition

A Pod template describes one disposable realization. Module 4 studies the Deployment and ReplicaSet controllers that maintain replicas and replace one template revision with another under a calculable availability bound.

## Worked investigation — the Pod is Running and the release is still broken

A new Atlas API Pod shows phase `Running`. One container has restarted six times. Readiness is false, but liveness is true. The Deployment has one updated replica and zero available replicas.

The Pod phase is a coarse summary, not a service-level conclusion. Inspect the hierarchy:

```text
Pod object
├── assigned Node
├── sandbox and network namespace
├── init-container outcomes
├── application container current state
├── application container last termination state
├── restart count and backoff
├── readiness gates and container readiness
└── Pod conditions
```

The last termination reason is `OOMKilled`, while the current container has restarted and is running. A phase-only check reports “Running”; a rollout check correctly reports no available new replica. Increasing the liveness initial delay would not repair memory exhaustion. Deleting the Pod would reproduce it.

### Restart and replacement are different recovery actions

The kubelet can restart a container inside the same Pod according to restart policy. The Pod retains identity, volumes, and scheduling assignment. A controller can replace the entire Pod with a new UID. Replacement recreates projected data and scheduling decisions; restart does not.

This distinction explains several operational surprises:

- environment-variable configuration remains unchanged across container restart because it was captured when the container was created;
- a projected ConfigMap volume may update eventually without Pod replacement, but the application must reread it;
- a Pod replacement can land on another Node and expose topology or volume assumptions;
- a container restart preserves an `emptyDir` volume because the Pod remains; Pod replacement does not;
- a Pod-level termination grace period is relevant to replacement/deletion, not to every internal crash.

### Sidecars require a lifecycle contract

Adding a sidecar is an architectural decision, not a packaging convenience. Containers in one Pod share fate and placement, but they may have different startup and shutdown needs. The Pod contract must answer:

- Must the sidecar be ready before the application is eligible?
- Which container owns a shared file or socket?
- What happens when the sidecar exits permanently?
- Can the application terminate while the sidecar drains data?
- Does the sidecar require credentials broader than the application?
- Is the combined resource request schedulable?

Atlas keeps its baseline Pod single-container unless a shared-fate requirement justifies another container. This avoids turning the Pod into an ungoverned mini-host.

## Common false conclusions

- **“Running means healthy.”** A running process can be unready, restarting, or serving incorrect behavior.
- **“Container restart is the same as Pod recreation.”** Identity, scheduling, and volume consequences differ.
- **“A sidecar is free.”** It changes resource, security, lifecycle, and failure boundaries.
- **“Init containers are migrations.”** Retried Pod initialization is not a safe owner for one-time global schema mutation.
- **“Ephemeral debugging proves the original image contained tools.”** Debug containers are separate injected containers.
