# Worked answers

## 1. What condition should liveness detect?

A process-local condition likely repaired by restarting that container, such as deadlock or irrecoverable internal progress failure. Shared dependency outages should normally affect readiness or degraded behavior, not trigger synchronized restarts. The proof should show that restart changes the failing condition.

## 2. How does a startup probe change liveness behavior?

Until startup succeeds, kubelet does not run liveness or readiness probes. This protects slow initialization from premature restart. The startup budget must still be bounded; otherwise permanent failure remains hidden. After success, normal health semantics begin.

## 3. Why is readiness not the same as liveness?

Readiness controls eligibility for new traffic or work while keeping the process running. Liveness requests a restart. A temporarily unavailable dependency may make Atlas unready but not locally dead. Conflating them can create restart storms and erase useful state.

## 4. What does a PodDisruptionBudget protect?

It constrains selected voluntary disruptions that use the Eviction API when the selected Pod population would fall below the budget. It does not protect node failure, node-pressure eviction, direct deletion, OOM, application crash, or network outage. Availability needs additional controls.

## 5. Why can a PDB block maintenance?

If current ready Pods already equal minAvailable, another voluntary eviction is refused. The platform must restore health or add capacity before draining. This is often correct: the budget expresses a real availability constraint. Bypassing it transfers risk and needs explicit authority.

## 6. How do maxUnavailable and a PDB differ?

Deployment maxUnavailable governs rollout population under the Deployment controller. A PDB governs voluntary evictions across its selector. They may overlap in outcomes but act on different workflows. Both must be analyzed with replicas, readiness, capacity, and topology.

## 7. Why can traffic still arrive after SIGTERM?

Endpoint updates, proxies, load balancers, connection pools, and clients observe termination on different timelines. Existing connections can persist. The application should stop accepting new work, drain safely, and tolerate late requests. Course 5 measures actual connectivity propagation.

## 8. When is preStop useful and what is its limit?

It can perform a small bounded action such as marking local drain state or waiting briefly for propagation. It uses the same termination grace period and does not replace SIGTERM handling. An unbounded remote call in preStop increases forced-kill risk.

## 9. Why did the PDB not save replicas after a Node failed?

Node failure is involuntary and does not use the Eviction API. The PDB is not consulted. Replica distribution and spare capacity determine how much availability remains and how quickly replacements can appear. The report should not call this a PDB bug.

## 10. What evidence distinguishes readiness failure from connectivity failure?

Readiness evidence comes from kubelet probe results and Pod conditions. Endpoint eligibility comes from EndpointSlice/controller state. Packet reachability and routing belong to Course 5. A ready Pod can still be unreachable due to networking, and an unready Pod can be directly reachable by IP.

## 11. Why is an ephemeral container not a durable fix?

It is a debugging tool attached to one Pod instance. Changes are not part of the Pod template and disappear on replacement. It may have sensitive namespace access. Use it to gather evidence, then repair the owning desired state through the proper release/controller path.

## 12. What makes an availability claim honest?

It combines replica/controller policy, truthful readiness, topology distribution, disruption policy, capacity, replacement time, dependency behavior, termination, and evidence from the relevant environment. No single green condition or object is sufficient.
