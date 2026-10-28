# Module 8 — Health, lifecycle, disruption, and availability

Kubernetes has several mechanisms that respond to different failure questions:

- **startup:** has initialization completed?
- **liveness:** should this container be restarted?
- **readiness:** should this Pod receive new traffic or count as ready?
- **termination:** can this Pod stop cooperatively?
- **disruption:** may an operator voluntarily evict this Pod now?
- **controller availability:** how many ready/available replacements exist?

Collapsing these into one `/health` endpoint creates restart loops, false traffic eligibility, and misleading availability claims.

## Startup probes protect slow initialization

If a startup probe is configured, kubelet delays liveness and readiness processing until startup succeeds. This prevents a slow but healthy initialization from being killed by liveness.

The startup budget is:

```text
failureThreshold × periodSeconds
```

plus execution timing effects. It should reflect a measured upper bound with margin, not an arbitrarily huge number that hides permanent failure.

Atlas startup validates local configuration and initializes internal state. It does not wait indefinitely for every remote dependency.

## Liveness asks whether restart can help

A liveness failure causes kubelet to restart the container. Therefore the check should identify a condition likely repaired by restarting that process.

Good liveness candidates:

- event loop or main process deadlock;
- irrecoverably corrupted internal state;
- inability to make local progress despite bounded self-recovery.

Poor liveness candidates:

- database temporarily unavailable;
- downstream rate limit;
- network partition;
- overloaded dependency;
- migration not yet complete.

Restarting every replica during a shared dependency outage amplifies the incident and destroys diagnostic state.

Atlas liveness checks the local process progress marker and does not require durable queue access.

## Readiness asks whether new work is safe

A readiness failure keeps the container running but marks the Pod not ready. Workload controllers report reduced readiness/availability, and networking controllers later remove or de-prioritize the Pod from endpoint selection.

Atlas API readiness requires valid configuration and the bounded dependencies needed to accept new requests. Atlas worker readiness requires a fresh heartbeat plus durable queue access, matching the Course 3 contract.

Readiness is not a universal dependency tree. If a downstream optional feature is unavailable, the API may remain ready and expose truthful partial capability. The contract should reflect user-visible behavior.

## Probe mechanics can create load

HTTP, TCP, gRPC, and exec probes have different costs and failure meanings. Exec probes spawn processes and can increase resource pressure. Very frequent probes across many Pods can become significant traffic. Timeouts and thresholds should consider normal latency and failure detection objectives.

Probe endpoints should not perform unbounded work, leak sensitive diagnostics, or mutate state.

## Readiness gates extend Pod readiness

Readiness gates allow custom Pod conditions to participate in readiness. They are useful when an external controller must confirm a condition not visible to kubelet. The responsible controller must reliably set the condition and handle absence as false. A forgotten readiness-gate controller can hold every Pod unready.

Atlas does not require a custom readiness gate in the base release, but the custom controller lab demonstrates the pattern.

## Termination and traffic removal race

When a Pod is deleted, object and endpoint controllers, kubelet, proxies, and clients observe the change on different timelines. A process can receive SIGTERM while some traffic still arrives through stale endpoint or connection state.

The application should:

1. mark itself unready or stop accepting new work;
2. drain in-flight work within a bounded period;
3. checkpoint durable work if needed;
4. close listeners and exit;
5. tolerate late arrivals according to protocol.

A `preStop` delay can create time for endpoint propagation, but it is a heuristic inside the termination budget. Course 5 measures actual network propagation.

## PodDisruptionBudgets govern a narrow class of disruption

A PDB limits how many selected Pods may be unavailable during **voluntary disruptions that use the Eviction API**, such as many node-drain workflows.

It does not prevent:

- node failure;
- kubelet node-pressure eviction;
- direct Pod deletion;
- Deployment rolling update decisions in all cases;
- application crash;
- container OOM;
- cluster/network outage.

A PDB is not a replica controller and not a capacity guarantee.

For Atlas API with three replicas, `minAvailable: 2` allows one voluntary disruption if at least two selected Pods are healthy. If only two Pods are ready, another eviction should be blocked. This can also block node maintenance until capacity or health is restored.

## PDB selectors and rounding matter

A PDB selector must match the intended Pods. An empty selector has API-version-specific semantics historically, so explicit selectors are safer. Percentage values round according to policy and can produce surprising results for small replica counts.

The PDB and Deployment strategy must be analyzed together. A strict PDB, maxUnavailable zero, and no surge capacity can make maintenance impossible. That may be correct if the availability requirement is non-negotiable; the platform must then provide capacity.

## Eviction types differ

### API-initiated eviction

Respects PDB and returns a refusal when disruption budget is exhausted.

### Node-pressure eviction

Kubelet reclaims resources and does not honor PDB. Hard thresholds may provide no normal termination grace.

### Node failure

The control plane eventually marks the Node and Pods unhealthy; replacement timing depends on controller and eviction behavior.

### Graceful node shutdown

Kubelet can participate in shutdown handling when configured, but evidence depends on node configuration and is deferred to later fleet operation.

## Deployment rollout and PDB are not identical controls

Deployment maxUnavailable constrains the rollout controller's population behavior. PDB constrains selected voluntary evictions. They can interact during a rollout or node drain but do not replace each other.

Availability review should combine:

- desired replicas;
- rollout surge/unavailable;
- minReadySeconds;
- readiness semantics;
- PDB min/max;
- topology placement;
- spare capacity;
- node-failure assumptions;
- termination time.

## Ephemeral containers and debug evidence

When a Pod is running but lacks diagnostic tools, an ephemeral container can join selected namespaces for debugging. It changes the security and evidence boundary. It should use a digest-pinned diagnostic image, restricted operator authority, time-bounded access, and an audit record.

A debug container cannot repair desired state. Changes made inside a running Pod disappear on replacement and can make the observed instance differ from the declared template.

## Worked failure: liveness death spiral

Atlas liveness checks the database. The database has a five-minute outage. Every API container fails liveness and restarts. Startup creates new database connections and loads configuration. Readiness never stabilizes. The Deployment shows zero available replicas even though the API could have returned a bounded dependency-unavailable response.

The fix is not a larger restart backoff alone. Liveness should measure local progress; readiness should represent ability to accept work. Retry and degradation policy belongs in the application and Course 4/5/9 operational model.

## Worked failure: PDB expectation after node loss

A team expects `minAvailable: 2` to keep two Pods after a Node dies. Two of three replicas were co-located on that Node because topology policy was only preferred. Both disappear. The PDB was never consulted because node failure is involuntary.

The correct availability design combines distribution, capacity, replacement time, and PDB for maintenance. No single object creates high availability.

## Atlas availability contract

Atlas API declares:

- startup probe with bounded initialization budget;
- liveness based on local progress;
- readiness based on safe request acceptance;
- termination grace thirty seconds;
- preStop limited to a small readiness/drain action;
- three replicas;
- PDB `minAvailable: 2`;
- topology spread policy from Module 7.

Atlas worker readiness includes durable queue access but liveness remains local. Worker has no PDB in Course 4 because one replica plus unresolved durable concurrency cannot support a meaningful voluntary-disruption guarantee. Course 6/9 must revise that design.

## Capstone increment

`atlas_kube/lifecycle.py` and `disruption.py` model probe thresholds, restart, readiness, graceful termination, API eviction, node pressure, and PDB arithmetic. The lab produces a liveness death spiral, then repairs probe semantics and demonstrates a PDB-protected voluntary eviction plus an unprotected node-pressure loss.

## Further reading

- Probes: <https://kubernetes.io/docs/concepts/workloads/pods/probes/>
- Pod lifecycle: <https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/>
- Disruptions: <https://kubernetes.io/docs/concepts/workloads/pods/disruptions/>
- Node-pressure eviction: <https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/>

## Transition

Module 8 establishes availability for interchangeable replicas. Module 9 examines workloads whose members need stable ordinal identity and why identity alone still does not create durable state.

## Worked failure — a protective probe creates an outage

Atlas API depends on an external database. A liveness probe calls a handler that fails whenever the database is unavailable. During a five-minute database incident, kubelet repeatedly restarts every API container. Startup work increases load, in-flight requests are abandoned, and the Pods never remain stable long enough to expose useful diagnostics.

The liveness question should have been narrower: **Is this process irrecoverably stuck such that restarting it is a plausible repair?** External dependency failure is usually not that condition.

Readiness can answer a different question: **Should new traffic be sent to this instance now?** Even readiness must reflect the desired degradation model. If the API can serve reads from durable local state while writes require the database, one binary readiness bit may be too coarse; endpoint or application design may need capability-specific behavior.

Startup probes protect slow initialization from premature liveness failure. They do not make startup healthy or improve capacity. Their time budget should be derived from measured startup distribution and release objectives.

### Shutdown is a protocol

A controlled Pod termination involves several concurrent transitions:

1. deletion timestamp is recorded;
2. endpoint eligibility begins changing;
3. `preStop` may run;
4. the runtime sends the termination signal;
5. the application stops accepting new work and drains;
6. the grace period expires or completion occurs;
7. remaining processes may be killed.

A safe application must tolerate overlap: some clients may still reach the Pod during propagation, and long requests need deadlines. A long `preStop` consumes the same grace budget; it does not extend it automatically.

### PDBs govern voluntary disruption only

For three healthy API replicas with `minAvailable: 2`, one voluntary eviction may be allowed. If one replica is already unready, no further voluntary eviction is permitted. Node failure, OOM termination, and involuntary eviction are outside the PDB guarantee.

An overly strict PDB can block node drains and upgrades indefinitely. An overly weak PDB can permit maintenance to remove too much capacity. The policy must align with replica count, rollout strategy, and failure-domain capacity.

## Common false conclusions

- **“Liveness should test every dependency.”** That can transform dependency outage into restart storm.
- **“Readiness false means the process should restart.”** It means the instance should not receive normal traffic.
- **“PDB preserves replicas during every failure.”** It constrains selected voluntary disruptions.
- **“A longer grace period guarantees draining.”** The application must implement and expose drain progress.
- **“Ready endpoints disappear instantly everywhere.”** Control-plane and data-plane propagation take time.
