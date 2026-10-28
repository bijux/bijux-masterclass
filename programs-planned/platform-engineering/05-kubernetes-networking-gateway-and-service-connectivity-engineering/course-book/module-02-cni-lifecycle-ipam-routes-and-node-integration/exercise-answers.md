# Worked answers — CNI lifecycle, IPAM, routes, and Node integration

The answers focus on lifecycle and recovery. A plugin that succeeds only on the happy path is not a correct attachment system.

## 1. What does a successful CNI ADD prove?

It proves that the invoked plugin chain accepted the runtime context and returned a successful attachment result for that invocation. Depending on the plugin, that can include address allocation, interface creation, local routes, MTU, and host-side state. It does not prove remote-Node routing, Service forwarding, DNS, NetworkPolicy enforcement, application readiness, or end-to-end MTU. The proof is also time-bounded: later drift can invalidate the attachment. A strong result records the sandbox identity, interface, address, route set, allocation generation, plugin versions, and returned result so a retry can be compared for equivalence.

## 2. Why must DEL tolerate a missing network namespace?

Deletion often arrives after the runtime has already removed the sandbox or after a previous cleanup partially succeeded. Requiring the namespace to exist would prevent release of IPAM records, host routes, tunnel state, or policy objects and would create permanent leaks after ordinary crash sequences. `DEL` should use stable allocation and attachment identity to remove whatever plugin-owned state remains, while treating already-absent state as a successful idempotent outcome. The negative control is repeating `DEL`: it should not release another attachment or fail merely because the original namespace and interface no longer exist.

## 3. Which stable identities should bind an allocation record?

Use a tuple that survives retries but does not collide across recreated workloads: network/configuration identity, sandbox or container ID, interface name, attachment identity where multiple attachments exist, and an allocation generation or lease identity. Pod name alone is insufficient because it can be recreated; namespace path disappears; address alone can later belong to another sandbox. Kubernetes UID can be additional context but should not replace runtime attachment identity. Evidence should show that repeated `ADD` for the same tuple returns the same allocation, while a new generation cannot accidentally claim the old record without an explicit recovery decision.

## 4. What risk does GC introduce if the runtime provides an incomplete known-good set?

Garbage collection may classify a valid attachment as orphaned and free its address or remove routes while the workload is still running. That can create immediate loss of connectivity and later duplicate address assignment. Destructive GC therefore needs authoritative, fresh, generation-aware known-good input, plus a grace or quarantine policy for ambiguous records. Test a partitioned but active sandbox as a negative control: temporary inability to observe it must not be enough to release the allocation. The GC report should state which authority supplied the live set and why each removed record was conclusively stale.

## 5. Why can CHECK pass while the application is unreachable from another Node?

`CHECK` can validate the local attachment—interface, address, local route, and plugin state—without testing remote route distribution, tunnel reachability, policy on another Node, Service programming, DNS, or application sockets. Its scope is deliberately narrower than end-to-end health. Distinguish the claims by running `CHECK`, then a direct cross-Node Pod-address test and packet capture. If local attachment evidence is correct but the packet never arrives on the destination Node, the failure belongs to cluster routing or an intermediate data plane, not the local CNI attachment.

## 6. How does a chained CNI configuration complicate rollback?

Several plugins can mutate different parts of the same attachment. An earlier plugin may allocate an address and create an interface before a later tuning or policy plugin fails. Cleanup must know which stages completed, in which order they own state, and how the previous result was transformed. Blindly rerunning the chain can duplicate or overwrite state; cleaning everything can delete another owner’s objects. A robust design uses named ownership, idempotent reverse cleanup where applicable, and durable stage evidence. Test failure after each stage and prove that a retry converges to one attachment.

## 7. Compare host-local and cluster-coordinated IPAM during a control-plane partition.

Host-local IPAM can continue allocating from a Node-owned pool if its local state and pool assignment remain valid, preserving Node-level availability. Its risks are stranded capacity, local-state loss, overlapping Node pools, and weaker global visibility. Cluster-coordinated IPAM can use capacity flexibly and maintain one ownership view, but a partition forces an availability decision: stop allocation, use pre-leased blocks, or risk conflicting ownership. The correct choice depends on the platform’s failure model. Evidence should test partition behavior, duplicate prevention, recovery, and reconciliation rather than comparing only allocation latency.

## 8. Why is address-pool exhaustion a capacity signal rather than an ordinary retry?

Retrying cannot manufacture addresses and can amplify controller or cloud API load. Exhaustion may indicate leaked allocations, undersized pools, fragmented free space, subnet or interface quotas, or scaling beyond planned headroom. The system should surface a bounded, attributable capacity failure and stop unproductive retry. Diagnose allocated-versus-active records, per-Node and subnet availability, leak age, cloud quotas, and growth rate. A repair might reclaim proven leaks or expand capacity, but expansion without fixing recovery defects merely postpones recurrence.

## 9. What evidence distinguishes a leaked allocation from a still-running partitioned sandbox?

Join several sources: runtime sandbox inventory, Node liveness and fencing state, network namespace and interface presence, host routes, cloud attachment state, allocation generation, and last authoritative observation. A record is not leaked merely because the control plane cannot reach its Node. A safe process quarantines the candidate, verifies that the workload cannot still use the address, and observes a grace period before reuse. The decisive negative control is an active but temporarily partitioned sandbox that remains allocated throughout GC.

## 10. Why should CNI and host firewall automation not share anonymous nftables chains?

Anonymous or ambiguously owned chains allow one reconciler to reorder, flush, or delete another component’s rules. That breaks idempotency, makes rollback unsafe, and leaves operators unable to attribute a packet verdict. Each owner should use distinct tables, chains, comments, handles, or managed objects with a documented handoff. During upgrades, prove that one component can rebuild its state without altering the other’s rules. A correct packet path is not enough; ownership must survive cleanup and failure.

## 11. What does STATUS need to evaluate beyond binary existence?

It should evaluate whether the plugin can safely accept new lifecycle operations: configuration validity, access to IPAM state, required mounts/maps, route or tunnel agent health, address capacity, cloud API prerequisites, and critical kernel features. The exact set depends on architecture. It should not include every downstream application dependency, because that would turn plugin readiness into a platform-wide health check. Test a present binary with unavailable IPAM or exhausted capacity; `STATUS` should expose the inability to attach safely.

## 12. Why is CNI not the correct place to model HTTP routing?

CNI owns network attachment and related L3/L4 state. HTTP hostnames, paths, methods, headers, TLS listener behavior, retries, and backend protocol semantics belong to Gateway and application layers. Putting HTTP decisions into attachment logic couples Pod creation to application routing and obscures ownership. CNI can make the Gateway and backend reachable and may enforce network policy; it cannot decide whether `/analysis-runs` should route to one Service or whether a `POST` retry is safe. The layer boundary is proved by naming the distinct API objects and owners.
