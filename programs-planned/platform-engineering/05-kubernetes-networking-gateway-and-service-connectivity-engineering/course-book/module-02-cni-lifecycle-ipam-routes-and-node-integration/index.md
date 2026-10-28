# Module 2 — CNI lifecycle, IPAM, routes, and Node integration

A Pod network attachment is not created by the Pod object alone. The container runtime establishes a sandbox and invokes a CNI configuration. One or more plugins allocate addresses, create interfaces, install routes, configure host state, and return a structured result. If any step crashes, the runtime and plugins must recover without allocating the same address twice or leaking state forever.

The engineering question is:

> How can a network attachment remain correct when operations are retried, partially completed, delivered after state has disappeared, or executed while the cluster control plane is unavailable?

## Learning outcomes

By the end of this module, you can:

- explain the runtime-to-CNI contract without reducing CNI to one vendor;
- distinguish `ADD`, `CHECK`, `DEL`, `GC`, and `STATUS` responsibilities;
- design idempotent attachment and cleanup behavior;
- compare host-local, cluster-coordinated, and cloud-integrated IPAM;
- reason about chained plugins and ownership of routes, sysctls, and firewall state;
- diagnose leaked allocations, duplicate addresses, exhausted pools, and partial attachment;
- state exactly what a successful CNI operation proves—and what it does not.

## CNI is a lifecycle contract

The CNI specification defines how a runtime invokes plugins with configuration and execution context. It does not prescribe an overlay, underlay, policy engine, routing protocol, or Service implementation.

A runtime commonly provides:

- command (`ADD`, `CHECK`, `DEL`, `GC`, or `STATUS`);
- container/sandbox identity;
- network namespace path when available;
- interface name;
- network configuration;
- runtime arguments;
- previous result for chained plugins.

A plugin returns a result or a structured error. Correctness depends on the lifecycle across several invocations, not only one successful `ADD`.

## `ADD`: establish or converge attachment state

`ADD` typically needs to ensure that:

1. the allocation identity maps to at most one active address;
2. the address is not simultaneously owned by another active sandbox;
3. the intended interface exists in the target namespace;
4. addresses, routes, MTU, and link state match configuration;
5. host-side routes or tunnel state exist where required;
6. chained plugins receive a valid previous result;
7. durable allocation state is committed consistently with observable attachment state.

Retries are normal. A runtime may repeat `ADD` after a timeout even if the plugin completed. A correct implementation either returns the equivalent attachment or converges safely; it does not allocate a second address simply because the caller did not receive the first response.

A successful `ADD` proves only that the plugin accepted and completed its attachment responsibilities at that moment. It does not prove:

- cross-Node routing;
- Service forwarding;
- DNS;
- NetworkPolicy enforcement;
- application listening state;
- end-to-end MTU;
- external connectivity.

## `CHECK`: verify current attachment expectations

`CHECK` inspects whether existing attachment state still satisfies the declared configuration. It can verify interfaces, addresses, routes, and plugin-specific state.

It is not an end-to-end application probe. `CHECK` can pass while remote Nodes lack routes, Service programming is stale, DNS is broken, or the application is not listening. Its scope must be documented so operators do not treat it as a general network-health endpoint.

A useful `CHECK` result identifies the violated invariant rather than reporting only “network unavailable.”

## `DEL`: cleanup must tolerate missing context

Deletion is frequently delivered after part of the original state has vanished. The sandbox may already be gone. The network namespace path may no longer exist. A previous `DEL` may have completed while its response was lost.

Therefore `DEL` must be idempotent and should release every state element whose stable identity can still be established. It must not require the namespace to exist merely to free an allocation or remove host-side state.

This creates an important design question: which stable keys bind the allocation?

A robust record may use a tuple such as:

```text
network identity
+ sandbox/container identity
+ interface name
+ allocation generation
```

Pod name alone is weak because Pods can be recreated. Namespace path alone disappears. Address alone risks releasing another attachment after reuse.

## `GC`: reconcile leaked state with an authoritative set

Garbage collection compares plugin-owned allocation or attachment state with a runtime-provided set of known-good attachments. It can recover leaks created by crashes that never reached `DEL`.

GC is dangerous when its authority is misunderstood. If the runtime supplies an incomplete set during a partition or bug, destructive GC can release addresses still used by active sandboxes. A safe design records:

- source and freshness of the known-good set;
- generation or observation time;
- grace period;
- evidence that an attachment is absent, not merely unreachable;
- whether cleanup is immediate, quarantined, or review-gated.

The Course 5 semantic model requires a generation-aware known-good set before destructive cleanup.

## `STATUS`: readiness of the plugin system

`STATUS` should answer whether the plugin is ready to perform new work. Binary existence is not enough. Depending on the architecture, readiness may depend on:

- configuration validity;
- access to allocation state;
- route or tunnel prerequisites;
- cloud API or control-plane connectivity;
- available address capacity;
- required kernel features;
- policy or agent health.

Do not make `STATUS` depend on every application endpoint. It reports plugin readiness, not platform-wide network success.

## Chained plugins and result ownership

A CNI configuration may invoke several plugins. One creates the base interface and address; another configures port mappings, bandwidth, tuning, or policy. Each plugin receives and may transform the previous result.

Chaining introduces partial-failure questions:

- Which plugin rolls back if a later plugin fails?
- Can a repeated invocation distinguish completed from incomplete stages?
- Who owns shared host state such as routes, sysctls, or nftables objects?
- How is version compatibility handled across result schemas?
- Can plugins safely execute in reverse for cleanup?

Avoid anonymous shared state. If both CNI and host firewall automation write unnamed chains or routes, cleanup by one component can delete the other’s state. Ownership should be visible in names, labels, handles, or dedicated tables.

## IPAM is an authority and recovery system

IP address management is not “pick a free address.” It owns uniqueness, release, exhaustion, recovery, and often topology.

### Host-local allocation

Each Node allocates from a Node-specific pool. Advantages include low dependency on a central service and predictable local ownership. Risks include stranded capacity, duplicated Node pools, local state loss, and difficult rebalancing.

During a control-plane partition, a Node may continue allocating if its local authority remains valid. That improves availability but increases the need for careful Node-pool assignment and recovery.

### Cluster-coordinated allocation

A central or distributed cluster data store coordinates allocations. It can use capacity more flexibly and provide a global ownership view. It also introduces availability, latency, locking, and partition-consistency decisions.

During a partition, the system must choose whether to stop allocation, lease bounded ranges, or risk conflicting ownership. The choice is part of the platform availability model.

### Cloud-integrated allocation

A cloud CNI may attach provider interfaces or secondary addresses to Nodes. It inherits cloud API rate limits, interface/address quotas, subnet capacity, propagation delays, and provider-specific failure modes. “No Pod IP available” may be a subnet, account, interface, or API-throttling incident rather than a local plugin bug.

## Address exhaustion is capacity failure

When a pool is exhausted, blind retry creates noise and delay. The incident may involve:

- leaked allocations;
- undersized Node pools;
- fragmented free space;
- cloud interface limits;
- subnet exhaustion;
- excessive warm-address targets;
- a scaling event that exceeded planned headroom.

Useful evidence includes allocated versus active counts, age of unreconciled records, pool fragmentation, per-Node capacity, cloud quotas, and rate of new attachments. Capacity alarms should occur before the final address is consumed.

## Node integration: routes, tunnels, neighbors, and sysctls

Attachment correctness extends beyond the Pod namespace. Depending on the design, the Node may need:

- a host-side veth or device;
- a route to the Pod address;
- routes or tunnel state for remote Pod prefixes;
- neighbor entries;
- forwarding sysctls;
- MTU configuration;
- policy programs or hooks;
- cloud route or interface state.

A valid Pod interface on one Node does not prove that another Node can reach it. Module 1’s transition ledger should therefore separate local attachment from cluster reachability.

## MTU belongs in the attachment contract

The plugin chooses or propagates the Pod-interface MTU. If it ignores encapsulation or encryption overhead, large cross-Node traffic can fail while local traffic succeeds.

Validate:

- Pod interface MTU;
- host-side device MTU;
- tunnel or encryption overhead;
- underlay MTU;
- IPv4 and IPv6 behavior;
- ICMP Packet Too Big / fragmentation-needed handling;
- application MSS behavior where relevant.

The correct value is an architectural decision, not a tuning number copied from another cluster.

## Crash recovery model

Treat attachment as a small distributed transaction among runtime, plugin state, namespace state, host state, and possibly cloud state.

Consider this failure:

```text
1. IPAM reserves address A.
2. interface and route are created.
3. plugin returns success.
4. runtime crashes before recording completion.
5. runtime retries ADD.
```

The retry must discover or reconstruct the existing attachment and return an equivalent result. Allocating address B would leak A and create ambiguous ownership.

Now consider:

```text
1. IPAM reserves address A.
2. process crashes before interface creation.
3. sandbox is later removed.
4. DEL arrives without a namespace.
```

Cleanup must release A based on stable allocation identity. GC should later detect the record if DEL never arrives.

## Worked investigation — the deleted Pod still owns an address

A Node reports address-pool exhaustion even though only half its expected Pods are running. The allocation database contains records for sandboxes that no longer exist. Several records correspond to a period when the runtime repeatedly crashed during deletion.

Investigation proceeds in this order:

1. Compare allocation records with runtime-known sandboxes.
2. Check record generation and last-observed times.
3. Verify that the suspect namespace and interface are absent.
4. Confirm no route, neighbor, or cloud attachment still uses the address.
5. Quarantine the records before release.
6. Run bounded GC with a complete known-good set.
7. Prove that a still-active but temporarily unreachable sandbox is not removed.

The defect is not solved by expanding the pool. Expansion would hide a recovery failure and increase future leak capacity.

## Capstone implementation

Module 2 uses:

- `capstone/atlas_net/cni.py` for deterministic lifecycle and generation behavior;
- `capstone/cni-go/lifecycle.go` for a second-language lifecycle implementation;
- `capstone/architecture/network-ownership.yaml` for state ownership;
- `capstone/scripts/cni_lifecycle_lab.py` for crash, replay, and GC experiments.

The model proves the Atlas lifecycle contract. It does not claim conformance of a production CNI binary or real cloud IPAM.

## The network namespace lifecycle is the real transaction boundary

A runtime creates a sandbox, obtains or opens its network namespace, and invokes configured plugins with a command, environment, and JSON configuration. Several resources may be changed before the call returns:

- an address may be reserved in local or remote IPAM state;
- a host-side interface may be created;
- one end may be moved into the target namespace;
- routes and addresses may be configured;
- policy or datapath entries may be installed;
- DNS data may be returned to the runtime;
- a checkpoint may be written for later `CHECK`, `DEL`, or garbage collection.

There is no single kernel transaction covering all of these effects. Crash consistency is therefore a first-class design problem. If the process dies after allocation but before the runtime records success, the next invocation must distinguish a safe replay from a conflicting attachment. If `DEL` arrives after the namespace is already gone, cleanup must use stable attachment identity rather than depending on entering that namespace again.

The Atlas model gives an attachment its own identifier, Pod UID, container identity, interface name, generation, address, and active state. Repeating `ADD` with the same identity returns the same result. Reusing the attachment identifier with different immutable inputs is rejected. This is the same reasoning used for durable idempotency in application services, applied to node networking.

## Configuration lists create ownership between plugins

A CNI configuration list may chain several plugins. Each plugin receives a prior result and may add or transform interfaces, addresses, routes, DNS settings, port mappings, bandwidth controls, or policy state. The durable review question is:

> Which plugin owns creation, verification, and deletion of each effect?

A chain is unsafe when one plugin assumes another will remove state but that ownership is not expressed or tested. It is also unsafe when an upgrade changes the result version or field interpretation between adjacent plugins.

For each chain, record:

- configuration name and CNI version;
- plugin order;
- delegated IPAM owner;
- fields consumed from the prior result;
- effects created by each plugin;
- cleanup behavior when a later plugin fails;
- `CHECK`, `STATUS`, and `GC` support;
- upgrade and rollback compatibility.

Do not treat `conflist` order as an implementation detail. It is an execution graph with failure semantics.

## IPAM is allocation plus reconciliation

An allocator must prevent duplicate live addresses, but that is only the first invariant. It also needs to answer:

- What proves an allocation is still attached to a live sandbox?
- How is a reservation recovered after a node or plugin crash?
- Can two node agents race for the same address?
- How is an address pool expanded or migrated?
- Which generation prevents an old attachment from deleting a new one?
- What evidence shows exhaustion versus allocator unavailability?

Capacity should be calculated from usable addresses, fragmentation, per-Node reservations, warm pools, dual-stack requirements, and replacement surges. A `/24` does not provide 256 safely usable Pod addresses in every design. Node-level prefix delegation and cloud-interface limits can become the binding constraint before the abstract CIDR is full.

Address exhaustion should produce a recognizable, bounded failure. Retrying without backoff can turn exhaustion into API or datastore pressure. Releasing arbitrary “old-looking” records can create duplicate ownership. The recovery path needs a liveness oracle and an audit trail.

## Node integration determines the packet path

CNI does not require one architecture. Common designs include:

- a bridge with local switching and host routes;
- routed veth pairs with per-Pod routes;
- overlay encapsulation between Nodes;
- cloud-native interfaces that place Pod addresses in the VPC/VNet domain;
- eBPF programs attached at host, container, or device hooks;
- chained designs combining a base network with policy or encryption.

The architecture changes where to observe:

- route ownership;
- neighbor entries;
- tunnel endpoints;
- policy enforcement;
- source-address translation;
- MTU overhead;
- host-firewall interaction;
- Node readiness and agent health.

A Pod address that appears in the network namespace proves only local configuration. Cross-Node reachability also requires the remote network to associate that prefix or address with the correct Node and the return path to do the inverse.

## Upgrade one state owner at a time

A CNI upgrade changes executable code that owns live kernel and datastore state. The release plan should identify which old and new versions coexist and which operations each may perform during the overlap.

A credible upgrade experiment includes:

1. an attachment created by the old version and checked by the new version;
2. a new attachment created while Nodes run mixed versions;
3. deletion of old- and new-created attachments;
4. restart of the node agent with existing Pods;
5. route, MTU, policy, and encryption consistency;
6. address exhaustion and recovery behavior;
7. rollback while new-format state exists;
8. garbage collection that cannot delete current-generation attachments.

“DaemonSet rollout completed” is not enough. The workload-visible contract is attachment continuity and correct packet paths, not merely process replacement.

## Transition

Module 2 establishes Pod attachments and address ownership. Module 3 moves one layer upward: how a stable Service identity is translated into a changing set of eligible Pod endpoints, and how that state converges into the data plane.
