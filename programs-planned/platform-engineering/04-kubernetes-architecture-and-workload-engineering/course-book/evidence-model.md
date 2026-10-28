# Evidence model

Kubernetes presents many observations, but they do not have equal strength and they do not answer the same question. This course uses an explicit evidence ladder to prevent a successful command or screenshot from becoming an unsupported production claim.

## Evidence classes

### E0 — design reasoning

Diagrams, calculations, and written decisions can prove internal consistency of an argument. They cannot prove executable behavior.

### E1 — dependency-light executable evidence

Python and Go tests exercise the course's explicit semantic models and controller core. Static manifest parsing and policy checks verify the files shipped in the release. E1 is deterministic and required.

It proves that the specified model rejects the planted defects. It does not prove that an independent Kubernetes implementation behaves identically in every detail.

### E2 — disposable local Kubernetes evidence

A pinned kind cluster supplies an independent API server, etcd, scheduler, controller manager, kubelets, and runtime. It can demonstrate admission, defaulting, control-loop timing, scheduling, container state, and events.

It is still one local topology. It does not prove managed identity, cloud load balancing, CSI durability, multi-zone failure, target admission policy, representative load, or upgrades.

### E3 — target-environment evidence

An identified managed or self-operated cluster can prove environment-specific behavior. Evidence must include cluster version, provider, node images, feature gates, admission configuration, CNI/CSI/Gateway versions, topology, workload digest, test population, time window, and cleanup.

### E4 — operated production evidence

Repeated real operation can support availability, capacity, recovery, cost, and incident-response claims. Course 4 does not produce E4 evidence.

## Observation map

| Evidence | Strongest supported conclusion | Does not establish |
|---|---|---|
| submitted manifest | client intent | admission or convergence |
| server-returned object | admitted/defaulted state and API identity | child realization |
| managed fields | field ownership record | correct ownership design |
| owner reference | lifecycle relationship | authorization or business ownership |
| generation/observedGeneration | whether a controller reports processing current intent | that the observation is truthful |
| conditions | controller's current summarized observation | original root cause without child evidence |
| events | time-bounded diagnostic clues | durable audit history |
| scheduling condition | placement failure/assignment evidence | node realization |
| container status | local runtime state | service reachability |
| readiness | endpoint-eligibility input | successful end-user journey |
| PDB status | current voluntary-disruption allowance | protection from involuntary failure |
| semantic test | course invariant under model inputs | Kubernetes conformance |
| kind transcript | local Kubernetes behavior | managed multi-zone production behavior |

## Evidence packet requirements

Every lab packet should record:

- evidence class;
- UTC time;
- tool and cluster versions;
- exact object UID/generation/resource version;
- exact image digest;
- desired state and controller owner;
- baseline observation;
- one controlled fault;
- earliest failed transition;
- repair and rejected alternatives;
- cleanup result;
- residual and deferred risk.

A green result without those identities is hard to reproduce. A failure result without preserved pre-repair state is hard to diagnose.
