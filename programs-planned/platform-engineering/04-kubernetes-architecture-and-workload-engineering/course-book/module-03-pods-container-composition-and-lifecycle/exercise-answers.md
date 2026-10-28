# Worked answers

## 1. Why are Atlas API and worker separate Pods?

They have different scaling, lifecycle, ports, readiness, resource use, and failure boundaries. Putting them in one Pod forces co-scheduling and replacement even when only one role needs change. Shared fate is justified only when components require the same placement and lifecycle. Loopback convenience is not enough to sacrifice independent control.

## 2. What does Pod phase Running fail to prove?

It does not prove all containers are healthy, readiness is true, traffic can reach the workload, durable dependencies are available, or the application is correct. Inspect Pod conditions, container states, restart history, probes, and later endpoint/network evidence. Running is a coarse lifecycle phase, not an availability verdict.

## 3. How does a container restart differ from Pod replacement?

A kubelet restart occurs within the same Pod UID, node assignment, sandbox, and mounted volumes. A controller replacement creates a new Pod object and UID and may choose another Node. Applications must tolerate both. Evidence should distinguish container restart count from owner-created replacement Pods.

## 4. Why is a database migration a poor generic init container?

Every Pod creation can repeat it, replicas can run it concurrently, kubelet retries can replay it, and rollout health becomes coupled to an external schema operation. Migrations need release-level authority, idempotency, compatibility, and rollback evidence. A dedicated Job or release workflow is a clearer owner.

## 5. What does readOnlyRootFilesystem protect and what does it not protect?

It prevents writes to the container root filesystem mounted read-only. It does not protect writable volumes, secrets exposed to the process, kernel vulnerabilities, network authority, or host mounts. The Pod must declare each writable path and its data class. Node/runtime enforcement remains environment-backed evidence.

## 6. Why must the Course 3 image digest remain in the Pod template?

The digest binds deployment to exact released bytes. A tag can move and would sever the connection to SBOM, provenance, signature, and approval evidence. Kubernetes image pull behavior does not make tags immutable. The admitted Pod spec and runtime image ID are the decisive artifact evidence.

## 7. What is special about a native sidecar container?

It is declared under initContainers with container-level `restartPolicy: Always`, so it starts during initialization and remains running with application containers. Kubernetes can apply lifecycle ordering distinct from ordinary app containers. The design still needs a shared-fate justification and resource/health policy.

## 8. Why is an emptyDir not acceptable for Atlas durable spool in the production-intent base?

emptyDir follows the Pod lifetime and is lost when the Pod is removed from a Node. Course 3 explicitly classifies spool/results as durable. Course 4 therefore declares a PVC interface and defers storage implementation to Course 6. A kind-only emptyDir overlay is a labeled mechanism test, not release evidence.

## 9. What should a preStop hook not be used for?

It should not substitute for application SIGTERM handling or perform unbounded remote work. It consumes the same termination grace period and may be retried only through another Pod lifecycle. The application must own draining and durable checkpoints; the hook may provide a small preparatory action with a bounded timeout.

## 10. Why should Pods usually be created by controllers rather than directly?

Controllers preserve a higher-level desired state and replace failed or deleted Pods. A direct Pod has no replica or rollout owner and is easy to leave absent after failure. Direct Pods remain useful for narrow debugging or static control-plane scenarios, but they are not the normal Atlas workload release unit.

## 11. How can an init container corrupt retry safety?

If it performs an append-only or non-idempotent external effect, kubelet retries can repeat the effect after partial failure. Safe init work either derives a target state, uses durable idempotency identity, or limits itself to local disposable preparation. Evidence must show what happens after crash between effect and completion.

## 12. Which evidence proves graceful termination?

A manifest proves only the declared grace period and hooks. Stronger evidence includes the deletion timestamp, readiness transition, signal receipt, stop-accepting-work event, completed or checkpointed work, process exit time, and absence of SIGKILL. A kind or environment lane is needed to exercise actual kubelet/runtime behavior.
