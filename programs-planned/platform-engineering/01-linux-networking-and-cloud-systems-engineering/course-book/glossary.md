# Glossary

**Address family** — The protocol family of a socket address, commonly IPv4 (`AF_INET`), IPv6 (`AF_INET6`), or Unix-domain (`AF_UNIX`).

**Atomic publication** — A transition in which readers observe either the previous complete object or the new complete object, not a partially written object. It is not automatically a durability guarantee.

**Availability zone** — A provider-defined failure domain within a region. Exact power, network, service, and dependency semantics are provider-specific.

**Backlog** — A bounded queue associated with connection establishment or application admission. Kernel handshake, accept, proxy, and worker queues are distinct.

**Block device** — A random-access storage device abstraction on which a filesystem or database may be built.

**Capability** — A Linux mechanism that divides selected root privileges into named kernel-authority units. A capability remains privilege.

**cgroup** — A Linux control-group hierarchy used to account for and control process resources.

**Cloud control plane** — Provider APIs and controllers that create or modify resources. It is distinct from the data path serving application traffic.

**Connection tracking** — Stateful firewall/NAT record of observed flows, used to classify return and related traffic.

**Controlling terminal** — A terminal associated with a session that affects job control and delivery of terminal-generated signals.

**Descriptor** — A process-local integer reference to an open file description, socket, pipe, device, or similar kernel object.

**Directory durability** — Persistence of directory-entry changes such as rename or creation across the declared crash boundary, often requiring synchronization of the parent directory.

**DNS authority** — The authoritative source for a DNS zone's records, distinct from recursive resolvers and caches.

**Effective identity** — The user/group credentials used for many access checks, distinct from real and saved identities.

**Evidence class** — The course category describing which environment exercised a claim: static, local runtime, privileged VM, real cloud, or sustained operation.

**Failure domain** — A set of components likely to fail together because they share power, network, control, location, or another dependency.

**File descriptor leak** — An open descriptor that remains reachable longer than intended, retaining kernel or storage resources and sometimes authority.

**Filesystem** — A data structure and implementation that maps names and metadata to file contents on a storage substrate.

**Forward proxy** — An intermediary selected by a client to reach other destinations.

**Graceful shutdown** — A bounded lifecycle that stops admission, completes or safely records in-flight work, releases resources, and exits with truthful evidence.

**Hostname verification** — Checking that the requested DNS name or IP address matches an allowed certificate Subject Alternative Name.

**HTTP authority** — The target host and optional port identifying the application endpoint, commonly carried by the Host field or HTTP/2/3 `:authority` pseudo-header.

**Hypervisor** — Software or firmware that creates and manages virtual machines and their virtual hardware.

**Idempotent operation** — An operation for which repeating the same intended request does not change the final effect beyond the first successful application. It does not mean every retry is safe without context.

**Image** — An immutable or versioned machine or workload artifact used to create runtime instances; its exact meaning depends on VM or OCI context.

**Init system** — The first userspace process and service-lifecycle framework; systemd is the reference implementation in this course.

**inode** — A filesystem object containing metadata and references to file data, separate from directory names.

**Listener** — A socket bound to a local address and prepared to accept incoming connections.

**Load balancer** — An intermediary that selects among backends; it does not create application correctness or state consistency by itself.

**Metadata service** — A cloud link-local or provider-named endpoint exposing instance, identity, and configuration data under provider-specific request policy.

**Mount** — Attachment of a filesystem or subtree at a path in a mount namespace.

**Namespace** — A Linux mechanism that gives a process a scoped view of selected kernel resources. Namespaces alone are not a complete security boundary.

**NAT** — Translation of network addresses or ports while maintaining forwarding state.

**Negative caching** — Caching that a DNS name or other lookup does not exist, usually for a bounded lifetime.

**Oracle** — The observation that determines whether an experimental hypothesis is supported or falsified.

**Page cache** — Kernel memory caching file data; it affects I/O and memory accounting but is not equivalent to durable storage.

**PKI** — Public key infrastructure: trust anchors, certificate issuers, leaf identities, validation rules, rotation, and revocation processes.

**Pressure Stall Information (PSI)** — Linux metrics describing time tasks are stalled due to CPU, memory, or I/O pressure.

**Process group** — A collection of processes used for job control and group signal delivery.

**Readiness** — Whether a process should receive new traffic or work under its declared prerequisites, distinct from liveness.

**Recursive resolver** — A DNS service that follows delegations or uses upstreams and caches answers for clients.

**Reverse proxy** — An intermediary that accepts client traffic on behalf of backend services.

**Route** — A rule selecting next hop, interface, and related properties for a destination; the most specific applicable route generally wins.

**SNI** — TLS Server Name Indication, sent during handshake so a server can select a certificate or virtual endpoint.

**Session** — A POSIX process grouping that contains process groups and may own a controlling terminal.

**Signal** — An asynchronous process notification with defined dispositions; `SIGKILL` and `SIGSTOP` cannot be caught or ignored.

**Socket** — A kernel communication endpoint with address, protocol, state, buffers, and ownership.

**Spool** — Durable or semi-durable queued files representing work transitions. Atlas uses a file spool to expose host mechanics.

**Stateful firewall** — A firewall whose decisions use connection-tracking state in addition to packet fields.

**Subject Alternative Name (SAN)** — Certificate extension containing identities permitted for hostname/IP verification.

**Supervisor** — A component such as systemd that owns process lifecycle, restart policy, resource controls, and dependency ordering.

**System call** — A controlled transition through which a userspace process requests a kernel operation.

**TIME_WAIT** — TCP state retained after close to handle delayed segments and ensure sequence-space safety.

**TLS termination** — The point at which an encrypted TLS connection ends and plaintext application protocol becomes available.

**TTL** — Time to live; in DNS, the caching lifetime supplied with resource records or negative answers.

**umask** — A process mask that clears permission bits requested during file creation; it is a default, not a complete policy.

**Virtual machine** — A guest execution environment with virtual CPU, memory, devices, and firmware managed by a hypervisor or cloud platform.

**Workload identity** — Short-lived or platform-bound identity made available to a workload, preferred over embedded long-lived static credentials.

**Writeback** — Kernel transfer of dirty cached data toward backing storage; visibility in memory is not the same as completed writeback or durable persistence.
