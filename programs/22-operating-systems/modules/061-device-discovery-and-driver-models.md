---
module_id: OS-061
program: Operating Systems
level: 2
module_number: 61
title: Device Discovery and Driver Models
status: complete
last_verified: 2026-09-04
---

# Device Discovery and Driver Models

## One-Page Review

### Governing question

How should an operating system discover hardware and logical devices, establish stable identity and dependencies, select and bind drivers, manage resources and lifetime, and coordinate hotplug and power transitions without confusing enumeration with readiness or leaking partially initialized state?

### Essential definitions

- A **device** is a kernel object representing a hardware or logical instance with identity, parentage, lifetime, resources, and state.
- A **driver** is code and metadata capable of controlling a compatible set of devices on a bus.
- A **bus type** defines bus-specific enumeration, identifiers, matching, probing, removal, and power behavior.
- **Enumeration** creates device instances from self-describing hardware, firmware descriptions, fixed platform knowledge, or another subsystem.
- **Matching** decides whether a registered driver is a candidate for a registered device; it is not proof that probe will succeed.
- **Binding** associates one device instance with one controlling driver after successful probe.
- **Probe** validates the instance, claims resources, initializes hardware and software state, and either commits a binding or unwinds.
- **Deferred probe** reports that a compatible device cannot initialize yet because a required supplier is not ready.
- A **device link** represents a supplier-consumer dependency for driver presence, power ordering, or both.
- A **device class** groups devices by function for userspace without replacing their physical bus and parent topology.

### Central model, mechanism, or theorem

Treat discovery and binding as a state machine over two graphs. The containment graph records parent-child topology and lifetime; the dependency graph records suppliers that must be present or powered before consumers. A device can move through `absent -> enumerated -> registered -> matched -> probing -> bound -> quiescing -> unbound -> released`, with deferred and failed branches. Every transition owns a defined set of references, resources, callbacks, and observable events.

Binding is correct only when identity matches under bus rules, all required suppliers satisfy their readiness contract, probe acquires resources in an unwindable order, and successful publication occurs after the device can serve its exposed interfaces. Removal reverses reachability before resources: stop new use, detach users, quiesce hardware and asynchronous work, unbind dependents, release resources, drop final references, then destroy state.

### Critical invariants

- One device instance has one authoritative identity and one parent in the containment graph at a time.
- At most one ordinary driver owns a device binding, even when several drivers match its identifiers.
- A successful probe publishes no interface that can observe uninitialized hardware or missing required suppliers.
- Every failed or deferred probe releases all resources and references acquired by that attempt.
- Supplier-consumer and parent-child graphs remain acyclic under the ordering semantics the core enforces.
- Userspace-visible names and attributes describe observed state and do not become accidental permanent hardware identity.
- Removal prevents new operations and drains interrupts, work, DMA, timers, callbacks, and open users before backing state is freed.
- Suspend, resume, shutdown, unbind, hot-unplug, and failed-probe paths preserve dependency and lifetime order.

### Common failures

Common mistakes are probing hardware before the bus or firmware has enumerated it, treating a match as proof of compatibility, using a display name as immutable identity, exposing userspace nodes before initialization commits, returning deferred probe after leaking clocks or mappings, retrying permanent failure forever, encoding supplier order only through driver registration timing, adding device links after a consumer already relied on the supplier, assuming parentage captures every dependency, freeing device memory directly instead of through final release, accepting new I/O during removal, and testing cold boot while omitting module reload, rebinding, suspend, hotplug, surprise loss, and partial failure.

### Compact example

An enumerated UART matches its driver but depends on a clock device that is not yet bound, so its first probe defers and unwinds. The clock then binds successfully. The core retries the UART, whose supplier is now ready, and binds it. Registration order did not become the dependency contract; readiness and retry state did.

### Connections

[OS-006](006-boot-process-and-kernel-initialization.md), [OS-007](007-kernel-data-structures.md), [OS-009](009-kernel-modules-and-drivers.md), [OS-054](054-kernel-read-copy-update.md), and [OS-058](058-timer-and-interrupt-scalability.md) connect device discovery to boot, object models, loadable code, lifetime, and asynchronous events.

## Governing Question

Hardware reaches an operating system through many paths. PCI and USB can enumerate themselves through bus protocols. Integrated peripherals can be described by ACPI or a device tree. Virtual and logical devices can be created by software. The driver core must turn all of these into one coherent lifecycle without erasing bus-specific semantics.

The governing question is how to separate description, discovery, identity, compatibility, initialization, dependency, ownership, publication, power, and removal. A design that handles successful boot but cannot unwind partial probe or survive hot-unplug is incomplete.

## Why This Matters

Driver initialization touches privileged resources: register ranges, interrupt lines, DMA, clocks, resets, regulators, firmware, memory, queues, and userspace interfaces. Incorrect ordering can hang hardware, corrupt memory, call freed callbacks, or expose a device before it is safe.

The device graph also drives system-wide behavior. Suspend and resume must respect power dependencies. Module loading and userspace policy depend on reliable identifiers and events. Hotplug can race open files and I/O. A missing supplier can postpone dozens of consumers.

Uniform core abstractions reduce duplicated lifetime code, but abstraction does not make every bus identical. Durable drivers use the bus's matching and resource APIs, the core's reference and dependency model, and subsystem-specific registration rather than guessing from raw topology.

## Prerequisites and Retrieval

Review [OS-003](003-system-calls-and-user-kernel-transitions.md), [OS-004](004-interrupts-and-exceptions.md), [OS-006](006-boot-process-and-kernel-initialization.md), [OS-007](007-kernel-data-structures.md), [OS-009](009-kernel-modules-and-drivers.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-025](025-deadlock-conditions-and-avoidance.md), [OS-028](028-signals-and-notifications.md), [OS-037](037-copy-on-write.md), [OS-049](049-virtual-filesystem-layers.md), [OS-054](054-kernel-read-copy-update.md), [OS-058](058-timer-and-interrupt-scalability.md), and [OS-060](060-diagnosing-multiprocessor-kernel-contention.md).

Retrieve these distinctions:

- physical discovery, firmware description, kernel object registration, driver matching, probe, and userspace publication are separate events;
- a parent-child containment edge and a supplier-consumer functional dependency express different relationships;
- device identity, driver compatibility, functional class, and userspace name have different stability requirements;
- successful allocation, requested resource, enabled hardware, published interface, and active I/O require ordered rollback;
- object removal and final memory release can be separated by outstanding references;
- graceful unbind and surprise physical disappearance provide different opportunities to quiesce hardware;
- hotplug events are notifications of state, not transactions that make userspace policy instantaneous;
- managed resources simplify reverse cleanup but do not decide the semantic order of all teardown actions.

## Learning Objectives

After this module, you should be able to:

1. distinguish self-enumerating buses, firmware enumeration, platform devices, logical devices, and userspace-created devices;
2. model device, driver, bus, class, parent, supplier, reference, resource, and state relationships;
3. trace registration, matching, probe, deferred probe, successful binding, failure unwind, unbind, and release;
4. design driver probe around staged acquisition, validation, publication, rollback, and managed resources;
5. coordinate supplier dependencies, power management, module loading, sysfs, uevents, and userspace policy;
6. handle hot-add, orderly removal, surprise loss, suspend, resume, shutdown, and concurrent operations;
7. validate driver-model behavior with fault injection, race tests, graph invariants, and lifecycle evidence.

## Core Exposition

### Sources of device discovery

Devices can be found by probing a standardized bus, parsing firmware tables, traversing a device tree, registering board knowledge, receiving a hypervisor description, or creating a logical instance in software. Each source has its own authority and update behavior.

Do not rescan unsafe address ranges merely because an instance is absent. Modern discovery relies on defined enumeration protocols or trusted descriptions that specify which resources exist.

### Self-enumerating buses

A self-enumerating bus provides a protocol for discovering functions and reading identifiers or descriptors. Its bus driver creates one device object per discovered function and assigns parentage and resources.

Enumeration establishes presence according to the bus. It does not prove the function is healthy, compatible with one driver revision, or ready for service.

### Firmware-described devices

ACPI, device tree, and other firmware descriptions enumerate components that may not advertise themselves. They describe compatible identities, addresses, interrupts, clocks, reset lines, power resources, and relationships.

Firmware is an input with version and quality risks. Validate required properties, reject inconsistent resources, and preserve enough provenance to diagnose platform-specific behavior.

### Platform devices

Platform devices represent integrated or legacy components whose registers are directly addressable but which lack a rich self-enumerating bus. Firmware or board code normally creates the instance; the driver controls it.

A driver should not invent its own platform device merely to make probing happen. Separating enumeration from control enables coldplug, hotplug, power ordering, and reuse across platforms.

### Logical devices

Software can create virtual network devices, loop devices, pseudo terminals, composite child functions, and other logical instances. Their discovery authority is a kernel subsystem or privileged userspace request rather than physical hardware.

Logical does not mean lifetime-free. Parent references, namespace visibility, open users, work, queues, and teardown follow the same reachability discipline.

### The common device object

The generic device object gives the core a common identity, parent, bus, class, driver, reference count, release callback, power state, attributes, and links. Bus-specific structures embed or refer to it.

Drivers use supported conversions rather than assuming memory layout. The common object belongs to the core lifecycle even when bus-specific state surrounds it.

### Containment hierarchy

Parent-child edges reflect physical or logical containment and default lifetime and power ordering. A bus controller can parent the devices it enumerates; a multifunction function can parent child functions it creates.

Containment is a tree-like ownership view, not a complete functional graph. A display controller can depend on a regulator or clock outside its ancestor chain.

### Device classes

Classes organize devices by function such as block, network, input, or graphics for userspace and subsystem APIs. The same device remains attached to its physical bus and parent.

Class membership must not replace bus identity in matching. A class says what service an initialized device exposes, while the bus determines how the instance is discovered and controlled.

### Bus types

A bus type registers common matching, probing, removal, shutdown, power, and iteration behavior for devices and drivers on that interconnect. Bus-specific types preserve type safety and identifiers.

The core coordinates lists and lifecycle; the bus defines compatibility semantics. PCI vendor and device IDs, USB descriptors, ACPI IDs, and device-tree compatible strings are not interchangeable.

### Device registration

Registration initializes core state, takes required references, attaches the object to its hierarchy and bus, and makes it eligible for matching and observation. The object must be fully initialized for every callback registration can trigger.

Registration failure unwinds all visibility and references established by the attempt. The caller does not free embedded device memory until the final release callback owns that action.

### Driver registration

A driver registers its name, bus, identifier tables, callbacks, owner, and power behavior. Registration makes it eligible to match every currently unbound device on that bus.

Driver code can arrive before or after devices. Correctness cannot depend on a fixed registration order because modules, hotplug, and deferred suppliers make ordering dynamic.

### Matching

The bus match callback compares device identity and driver support metadata. A positive result selects a candidate and can support module aliasing.

Matching is side-effect-light and does not claim hardware. Probe still verifies revision, resources, firmware, state, and dependencies and can fail or defer.

### Binding state

Binding associates one driver with one device after probe returns success. The core serializes competing attempts and records the association for removal, power callbacks, and observation.

Several drivers may match broadly, but at most one ordinary driver controls the instance. Overrides are explicit administrative policy and remain subject to safe unbind and reprobe.

### Probe context

Probe normally runs in a sleepable kernel context but under driver-core serialization and subsystem constraints. It can allocate memory, request firmware, and wait where APIs permit.

It must not assume no other device probes run concurrently. Global driver state uses synchronization, and long work avoids blocking unrelated core paths unnecessarily.

### Staged probe

A robust probe validates identity and mandatory descriptions, allocates private state, claims address and interrupt resources, acquires suppliers, configures DMA, initializes hardware, creates queues, and publishes subsystem interfaces last.

Each stage has an inverse. Write the unwind path alongside acquisition so every error injection leaves the device unbound and retryable or permanently failed by policy.

### Resource ownership

Register windows, I/O ports, IRQs, DMA masks, clocks, resets, regulators, GPIOs, firmware, memory, worker threads, timers, and subsystem identifiers have distinct release rules.

Claim exclusive physical resources before touching them. Resource reservation prevents two drivers from controlling the same range even if both matched through incorrect descriptions.

### Managed resources

Device-managed resources register cleanup actions tied to device binding lifetime. If probe fails or the driver detaches, the core invokes cleanup in reverse order.

Managed allocation reduces goto-heavy unwind and leaks. It does not know semantic needs such as stopping new I/O before disabling interrupts, so explicit actions and grouping remain necessary.

### Cleanup ordering

Reverse allocation order is a useful default only when acquisition order reflects dependencies. If a worker uses a mapped register and IRQ, teardown must stop arrivals and join the worker before unmapping or freeing state.

Use managed cleanup actions at deliberate points, or retain explicit remove steps for semantic quiescence. Verify the actual action stack rather than assuming “managed” means correct.

### Driver private state

Probe associates instance-specific private state with the device. Interrupts, work, file operations, power callbacks, and remove retrieve that state under lifetime rules.

Do not use one global structure for multiple devices unless it represents intentionally shared driver-wide policy. Per-device state enables independent hotplug and failure.

### Deferred probe

Probe defers when a compatible device requires a supplier that may become available later. The attempt releases acquired resources and returns the distinguished deferred result.

The core retries after supplier or driver activity. Defer early to reduce repeated work, preserve the reason for diagnostics, and distinguish “not ready yet” from invalid firmware or unsupported hardware.

### Permanent failure

Invalid identifiers, impossible resources, corrupt firmware, unsupported revisions, or hardware self-test failure are not necessarily transient. Returning deferred status forever hides the cause and delays boot completion.

Classify each error. Transient dependencies defer; retriable I/O can use bounded retry; permanent incompatibility returns a precise failure and leaves useful diagnostics.

### Supplier-consumer dependencies

Consumers can require clocks, regulators, interconnects, IOMMUs, power domains, firmware providers, buses, PHYs, or other devices. Readiness and runtime power often depend on those suppliers.

Record dependencies in discoverable metadata or device links before the consumer needs them. Driver registration order is not a durable substitute for an edge.

### Device links

Device links extend parent-child ordering with supplier-consumer relationships. Managed links can enforce supplier driver presence, consumer-first unbind, supplier-first resume, and runtime power relationships.

Links have lifecycle and state. Adding one late while suspend or unbind runs can create inconsistent order; adding a cycle is rejected because no valid dependency order exists.

### Dependency graph

Treat parent and supplier edges as one ordering graph for probe, power, shutdown, and unbind while retaining their distinct semantics. Every new edge is checked for cycles and publication timing.

Optional suppliers need an explicit absent state. Waiting forever for hardware that legitimately does not exist is not dependency management.

### Probe ordering

The driver core can trigger probe when either a device or driver registers. Dependencies decide readiness, not a hand-maintained global initialization sequence.

Asynchronous probing can shorten boot by running independent devices concurrently. Shared resources, logs, error paths, and dependency state must tolerate that concurrency.

### Module loading

Bus-specific modalias data lets userspace request a module whose supported identifier table matches a device. Loading registers a driver, which triggers ordinary matching and probe.

Module loading does not bypass signature, trust, policy, or compatibility checks. Failure to load and failure to probe are different diagnostics.

### Userspace events

Device registration, change, binding, and removal can generate uevents carrying identifiers and state for userspace policy. A device manager can load modules, set permissions, and create links.

Events are asynchronous notifications. Userspace must tolerate duplicates, reordering across independent devices, missing historical context, and state changing before action completes; current sysfs state remains authoritative.

### Sysfs representation

Sysfs exports device, bus, driver, class, attribute, and relationship objects. Each attribute should represent one coherent value or operation with explicit permissions and lifetime.

Directory names and symlinks help navigation but are not automatically stable application identity. Userspace uses documented subsystem identifiers and handles disappearance between lookup and access.

### Naming and identity

Physical path, serial number, firmware handle, bus address, function ID, and class name answer different identity questions. Hotplug can reuse an address, and topology paths can change after firmware or cabling changes.

Define which identifier scopes one boot, one port, one physical unit, or one logical configuration. Avoid encoding accidental enumeration order in durable policy.

### Firmware properties

Property APIs present ACPI, device-tree, software-node, or platform data through common access where semantics align. Drivers validate type, count, range, units, and required-versus-optional meaning.

Defaults are safe only when the binding defines them. Silently guessing clock frequency, DMA coherence, interrupt polarity, or register size can damage hardware.

### Resource translation

Firmware and bus layers translate addresses and interrupts through bridges and controllers into kernel resources. A child's numeric address is meaningful within its bus domain, not automatically a CPU physical address.

Use resource and mapping APIs so architecture ordering, endianness, reservation, and translation are preserved. The next module develops memory-mapped and port-mapped I/O.

### Multifunction devices

One physical package can expose several bus functions or child devices with shared resets, power, firmware, and interrupt resources. Separate child drivers improve modularity but add cross-function dependencies.

A parent or auxiliary coordination driver owns truly shared state. Children cannot independently reset hardware while siblings perform I/O.

### Composite and child creation

A bound parent can discover internal functions and register child devices. Child registration happens only after the parent can support their operations and is reversed before parent teardown.

Partial child creation unwinds already registered children in dependency order. References keep the parent alive while any child remains reachable.

### Reference counting

References separate removal from memory release. A lookup, open handle, queued callback, child, link, or subsystem registration can keep an object alive after it disappears from discovery.

Reference counting prevents use-after-free but does not make operations valid after disconnect. State checks reject new work while existing users drain.

### Release callbacks

The final device reference invokes the release callback responsible for containing-object memory. Every registered device must have a valid release plan.

Do not free the object manually after unregistering unless ownership rules prove no references remain and the core API specifies it. Final release can occur later and in another context.

### Publication order

Publish class devices, character nodes, network interfaces, queues, and sysfs controls only after every operation they expose can handle concurrent use. Memory barriers and subsystem registration rules establish visibility.

On failure or removal, unpublish first so no new caller enters, then drain operations, then dismantle hardware and resources.

### Open users and active I/O

Unbind can race file descriptors, mappings, network sockets, requests, and control operations. Each subsystem decides whether removal blocks, marks disconnected, waits, or lets handles survive with failing operations.

Drivers maintain per-open references and a disconnected state. User memory is never allowed to retain a live path into freed device state.

### Interrupt lifecycle

Request an IRQ only after its handler state is initialized, or keep the hardware source masked until ready. Removal blocks new device interrupts, synchronizes handlers, drains threaded and deferred work, then frees the IRQ.

Freeing handler data before interrupt synchronization creates a direct use-after-free. Disabling an IRQ while holding a lock needed by its handler can deadlock.

### DMA lifecycle

Configure DMA capability before allocating or mapping buffers under that contract. Start engines only after descriptors and completion paths are visible.

Removal stops submission, quiesces hardware, waits for or aborts transfers, synchronizes device and CPU ownership, unmaps buffers, and only then frees memory. Surprise loss needs timeout and containment because the device may not acknowledge stop.

### Work, timers, and callbacks

Drivers schedule workqueues, timers, tasklets, threaded handlers, and completion callbacks that outlive the initiating call. Every asynchronous source holds or can reach valid state.

Teardown sets a stopping state, prevents new scheduling, cancels and joins each source under its synchronization contract, and verifies no callback can rearm itself.

### Graceful unbind

Orderly unbind gives the driver a live device long enough to stop interfaces and hardware. The core prevents new binding, consumers unbind before suppliers, and remove releases binding-scoped state.

Remove should leave the physical device in a safe quiescent state for another compatible driver or shutdown. It does not destroy core memory while references remain.

### Surprise removal

Hot-unplug can make register access fail and DMA completion disappear before remove begins. The driver detects disconnect, blocks new I/O, avoids unsafe hardware access, completes users with defined errors, and contains outstanding DMA.

Every wait on hardware has a timeout and recovery rule. Assuming the device will answer during teardown turns physical loss into an unbounded kernel stall.

### Driver rebinding

Administrative unbind and bind exercise the same lifecycle without reboot. All global, per-device, sysfs, IRQ, DMA, worker, and firmware state must be reusable.

Test repeated cycles and alternate compatible drivers where policy allows. A successful first probe can hide leaked identifiers or stale hardware state that breaks the second.

### Power management

Runtime and system power callbacks coordinate device state with consumers, suppliers, parent buses, interrupts, and wakeup sources. A consumer resumes only after required suppliers can serve it.

Power state is reference-counted or otherwise synchronized with I/O. Autosuspend cannot race a new request that assumes registers and clocks are active.

### Suspend and resume ordering

System suspend generally quiesces consumers before suppliers and children before parents; resume reverses that order. Device links add non-hierarchical dependencies.

Late and noirq phases impose stricter execution constraints. Drivers place actions in the correct phase rather than doing all shutdown work in one callback.

### Shutdown

Shutdown prepares hardware for poweroff or reboot and may differ from reusable remove. It stops DMA, masks interrupts, persists required state, and leaves firmware or the next kernel a defined device condition.

Do not assume userspace teardown completed. Shutdown must be idempotent enough for partially quiesced and failure states.

### Hot-add

Hot-add discovers and registers a new instance while the rest of the system is active. Matching, module loading, dependency discovery, resource allocation, and userspace policy occur concurrently.

Capacity and naming decisions account for existing instances. Global arrays sized only at boot or singleton assumptions fail under legitimate additions.

### Unbind races

Probe, deferred retry, bind, unbind, supplier loss, power transitions, and hotplug can overlap. Core locks establish broad state, while drivers synchronize their own operations and async callbacks.

Callbacks recheck device state after sleeping. A pointer acquired before unbind is insufficient evidence that the hardware remains usable.

### Error reporting

Errors identify device, bus address, driver, operation, resource, dependency, and stable errno without flooding repeated deferred attempts. Diagnostic state remains accessible where safe.

Rate-limit hardware storms but retain first and aggregate evidence. Messages distinguish no match, module absence, probe defer, permanent probe failure, disconnect, and policy denial.

### Security and trust

Device descriptions and identifiers can come from firmware, removable buses, virtual machines, or userspace-mediated protocols. Treat lengths, counts, capabilities, and offsets as untrusted inputs.

Driver binding grants privileged hardware access. Module trust, IOMMU policy, device authorization, firmware validation, and least-privilege sysfs controls limit damage from malicious or faulty devices.

### Observability

Record enumeration source, stable and bus identifiers, parent and supplier graph, registration, match candidates, probe start and result, defer reason, resource acquisitions, binding, publications, power state, events, references, I/O, removal, and release.

Correlate kernel state with current sysfs rather than relying only on logs. Include timestamps, topology generation, module version, firmware, retries, dropped events, and userspace actions.

### Experiment design

Test device-before-driver and driver-before-device registration, independent parallel probes, missing and late suppliers, permanent invalid firmware, every acquisition failure, repeated bind cycles, class publication races, and reference retention.

Exercise hot-add, orderly unbind, surprise removal during I/O, suspend at every probe state, resume failure, shutdown, module removal, multifunction dependencies, interrupt and DMA activity, and hostile descriptors.

### Assurance

Model the lifecycle state machine and both graphs, then map every transition to required references, resources, callbacks, visible interfaces, inverses, and fault tests. Prove cycles are rejected and final release follows last reachability.

Reviewers include bus, driver-core, firmware, power, interrupt, DMA, subsystem, hotplug, security, performance, and userspace-policy specialists. Unsupported hardware and firmware behavior remain explicit limitations.

## Definitions and Notation

Let `D` be device instances, `R` drivers, `B` bus types, `P` parent edges, and `S` supplier-to-consumer dependency edges. A candidate binding `(d,r)` requires `bus(d)=bus(r)` and bus-specific `match(d,r)=true`; successful binding additionally requires probe completion and all mandatory suppliers ready.

Let each probe acquisition produce a resource token in ordered stack `Q=[q_1,...,q_n]`. Failure at stage `k` releases every acquired token whose ownership did not transfer, in a dependency-valid reverse or explicitly registered action order. Successful publication is a commit boundary, not an excuse to omit later removal.

The combined ordering graph used for a lifecycle transition must be acyclic under that transition's edge directions. Containment, driver presence, runtime power, suspend, resume, shutdown, and release can require related but distinct orderings.

## Mechanisms, Invariants, or Proof Structure

1. **Establish discovery authority.** Identify bus, firmware, platform, subsystem or userspace source and validate its descriptors.
2. **Create identity.** Assign bus-specific identifiers, parent, resources, firmware node and stable provenance without relying on enumeration order.
3. **Register safely.** Initialize references, release, attributes and callback-visible state before core registration.
4. **Match by bus rules.** Compare explicit support tables and keep matching distinct from hardware commitment.
5. **Resolve dependencies.** Record suppliers and parentage early, reject graph cycles, and defer only genuinely transient readiness.
6. **Probe transactionally.** Validate, acquire, initialize and publish in stages with a tested inverse for every failure.
7. **Bind and expose.** Commit one driver association only after operational interfaces can safely accept concurrent use.
8. **Coordinate operation.** Maintain power, interrupts, DMA, queues, workers, users, references and dependency state.
9. **Remove reachability first.** Reject new work, unpublish, drain consumers and callbacks, quiesce hardware, then release resources.
10. **Separate unregister and release.** Preserve memory until children, opens, links, async work and all references are gone.
11. **Test lifecycle adversarially.** Cover order variations, failures, deferral, hotplug, surprise loss, power, rebind and shutdown.
12. **Retain evidence.** Preserve graph, states, identifiers, resources, events, faults, timings, reviewers and limitations.

<!-- bijux-verify: {"id":"device-probe-dependency","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"probe=uart0 result=defer missing=clk0\nprobe=clk0 driver=clock result=bound\nretry=uart0 driver=uart result=bound\nbound=clk0,uart0\n","stderr":""}} -->
```python
devices = [
    {"name": "uart0", "compatible": "acme,uart-v2", "supplier": "clk0"},
    {"name": "clk0", "compatible": "acme,clock-v1", "supplier": None},
]
drivers = {"acme,uart-v2": "uart", "acme,clock-v1": "clock"}
bound = set()
deferred = []

for device in devices:
    supplier = device["supplier"]
    if supplier and supplier not in bound:
        deferred.append(device)
        print(f"probe={device['name']} result=defer missing={supplier}")
        continue
    bound.add(device["name"])
    print(f"probe={device['name']} driver={drivers[device['compatible']]} result=bound")

for device in deferred:
    bound.add(device["name"])
    print(f"retry={device['name']} driver={drivers[device['compatible']]} result=bound")
print("bound=" + ",".join(sorted(bound)))
```

The executable example checks one deterministic dependency and retry sequence. It does not call driver-core APIs, validate graph cycles, acquire hardware resources, model concurrent removal, prove cleanup, or establish a general probe scheduler.

## Alternatives and Trade-Offs

- Self-enumeration reflects live bus state but requires protocol access; firmware enumeration covers fixed devices and depends on description quality.
- One common device model centralizes lifetime and power behavior but cannot replace bus-specific identifiers and operations.
- Synchronous probe simplifies ordering but lengthens boot and serializes independent work; asynchronous probe improves concurrency and exposes races.
- Deferred probe handles late suppliers but can hide permanent errors; explicit failure is diagnosable and cannot recover from legitimate late readiness.
- Parent-child ordering is simple but omits sibling dependencies; device links express suppliers and add graph state and cycle checks.
- Managed resources reduce leaks and boilerplate but reverse only registered actions; explicit cleanup makes semantic order visible and verbose.
- Publishing early improves apparent availability but exposes partial state; publish-last gives a strong commit boundary and delays discovery by userspace.
- Stable logical names simplify policy but require persistent identity mapping; topology-derived names are automatic and can change.
- Broad identifier matches support device families but increase false candidates; narrow revision matches are safe and fragment support metadata.
- One multifunction driver coordinates shared state easily but grows coupling; child drivers isolate functions and need parent-mediated resources.
- Blocking remove gives simple quiescence but can hang on failed hardware; disconnected handles and timeout recovery complicate user semantics.
- Runtime power management saves energy but adds supplier and I/O races; permanently active devices simplify operation and waste power.
- Global driver state saves memory but couples instances and hotplug; per-device state enables independence with repeated allocations.
- Userspace policy offers flexible module and permission decisions but is asynchronous; kernel defaults act immediately and are less adaptable.

## Failure Modes and Misconceptions

- **“Discovery means the device is usable.”** Registration, matching, probe and publication remain.
- **“A matching ID proves the driver works.”** Probe validates resources, revision, state and dependencies.
- **“Driver registration order expresses dependencies.”** Modules and hotplug invalidate that assumption.
- **“Parentage captures every supplier.”** Functional dependencies can cross the containment tree.
- **“Deferred probe is a generic retry.”** It is for plausibly unavailable suppliers, not permanent failure.
- **“Managed resources make teardown automatically correct.”** Semantic quiescence order still belongs to the driver.
- **“Unregister frees the object immediately.”** Outstanding references delay final release.
- **“Reference counting permits operations after disconnect.”** It preserves memory, not hardware availability.
- **“Sysfs names are permanent physical identity.”** topology and enumeration can change.
- **“A uevent is a committed userspace transaction.”** State can change before policy acts.
- **“Removing the device stops DMA.”** Hardware must be quiesced or contained first.
- **“Freeing the IRQ stops an executing handler.”** Synchronization and handler-state lifetime are required.
- **“Suspend order is just reverse registration order.”** Parent and supplier graphs determine it.
- **“Cold-boot success proves lifecycle correctness.”** rebind, failure, hotplug and power paths differ.
- **“Surprise removal can use the graceful path unchanged.”** Hardware may already be inaccessible.

## Worked Examples

### Example 1

A PCI function enumerates before its module loads. Its modalias triggers userspace module policy; driver registration then matches and probes the existing device.

### Example 2

An integrated UART is described by firmware. Probe defers until its clock provider binds, then retries and publishes the character interface only after the clock and IRQ work.

### Example 3

Probe fails after requesting an IRQ but before class registration. The action stack frees the IRQ, disables the clock, unmaps registers, and releases memory without leaving a visible node.

### Example 4

A display consumer and regulator supplier are siblings. A device link supplies probe readiness and consumer-first suspend or unbind order that parentage alone lacks.

### Example 5

Two drivers match a family ID. The first candidate rejects an unsupported revision during probe and unwinds; policy selects the explicitly supported driver rather than sharing ownership.

### Example 6

A USB device disappears during writes. The driver marks disconnected, blocks submission, completes queued users with errors, synchronizes callbacks, and releases memory only after open handles close.

### Example 7

A multifunction parent owns reset and power while child network and storage functions bind independently. The parent serializes reset and refuses it while either child has active I/O.

### Example 8

An administrator repeatedly unbinds and rebinds a driver. The second cycle exposes a leaked queue identifier, leading to a cleanup action added at the correct reverse stage.

### Example 9

Suspend begins while a late dependency link is being added. Lifecycle serialization ensures the new graph is either fully included in ordering or rejected and retried after resume.

### Example 10

A malicious virtual device advertises an oversized descriptor count. Probe validates length and multiplication before allocation and rejects the device without publishing interfaces.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects buses, firmware, interrupts, DMA, register interfaces, power, reset, topology, and virtualization. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects module trust, hostile peripherals, descriptor validation, DMA isolation, firmware, authorization, and least privilege.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes state machines, dependency graphs, lifecycle hazards, fault injection, traceability, and assurance. [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects resource acquisition, adapters, dependency injection, object lifetime, publication, rollback, and observers. Within this program, [OS-062](../ROADMAP.md) develops register I/O and [OS-063](../ROADMAP.md) develops DMA.

## References

- Linux kernel documentation, [The Linux Kernel Device Model](https://docs.kernel.org/driver-api/driver-model/overview.html), current page checked 2026-09-04. Common device model, hierarchy, buses, classes, callbacks, hotplug, power and userspace view.
- Linux kernel documentation, [Driver Binding](https://docs.kernel.org/driver-api/driver-model/binding.html), current page checked 2026-09-04. Device and driver registration, bus matching, probing, binding and class association.
- Linux kernel documentation, [Bus Types](https://docs.kernel.org/driver-api/driver-model/bus.html), current page checked 2026-09-04. Bus registration, match callbacks, device and driver lists, iteration, references and sysfs.
- Linux kernel documentation, [The Basic Device Structure](https://docs.kernel.org/driver-api/driver-model/device.html), current page checked 2026-09-04. Device registration, parentage, naming, reference counting, attributes and release.
- Linux kernel documentation, [Device Drivers](https://docs.kernel.org/driver-api/driver-model/driver.html), current page checked 2026-09-04. Driver registration, probe, remove, shutdown, iteration, binding and deferred probe.
- Linux kernel documentation, [Device Links](https://docs.kernel.org/driver-api/device_link.html), current page checked 2026-09-04. Supplier-consumer dependencies, power ordering, presence, link lifecycle, state machine, flags and cycles.
- Linux kernel documentation, [Platform Devices and Drivers](https://docs.kernel.org/driver-api/driver-model/platform.html), current page checked 2026-09-04. Integrated-device representation, resources, firmware creation, matching, probing and legacy limitations.
- Linux kernel documentation, [Devres](https://docs.kernel.org/driver-api/driver-model/devres.html), current page checked 2026-09-04. Device-managed resources, release, groups, rollback, single-instance resources and lifecycle trade-offs.
- Linux kernel documentation, [ACPI Based Device Enumeration](https://docs.kernel.org/firmware-guide/acpi/enumeration.html), current page checked 2026-09-04. Firmware device discovery, identifiers, platform devices, dependencies, serial buses and properties.
- Linux kernel documentation, [Device drivers infrastructure](https://docs.kernel.org/driver-api/infrastructure.html), current page checked 2026-09-04. Driver-core structures, registration, probing, deferred reasons, attributes, power callbacks, binding and resource helpers.

## Exercises

### Exercise 1

Design discovery and binding for an SoC sensor that depends on an I2C controller, regulator, clock, GPIO interrupt, firmware calibration, and userspace class interface.

### Exercise 2

Specify a transactional probe with twelve acquisition stages. Show how managed resources and explicit quiescence actions compose for every failure point.

### Exercise 3

Model parent-child and supplier-consumer graphs for a multifunction PCI device with network and storage children, shared firmware, power, reset, IOMMU, and hotplug.

### Exercise 4

Trace orderly unbind and surprise removal while files are open, DMA and interrupts are active, timers can rearm, and a supplier begins suspend.

### Exercise 5

Build a verification and assurance plan for a new driver model integration. Include identity, concurrency, dependencies, userspace, power, security, fault injection, and reproducibility.

## Answers to the Exercises

### Answer 1

Firmware enumerates the sensor with bus address, compatible ID, regulator, clock, GPIO interrupt and calibration references beneath the I2C client hierarchy. The I2C controller is a containment parent; regulator, clock and possibly calibration provider are supplier edges. Validate property types, sizes, units and optionality before allocation. If a mandatory supplier is not registered, defer early with a recorded reason; invalid calibration fails permanently.

Probe allocates private state, acquires regulator and clock, reserves and maps bus resources through I2C, parses calibration, initializes locks and async state, powers and identifies the sensor, requests the interrupt while masked, registers buffers, and publishes the class interface last. Every stage has reverse cleanup. Runtime power links keep suppliers active during samples. Removal unpublishes userspace access, marks stopping, drains opens and reads, masks and synchronizes the IRQ, cancels timers and work, powers down, releases resources, drops links and lets the release callback free final state.

### Answer 2

List each resource as a token with dependency and inverse: private memory, parent reference, register reservation, mapping, DMA contract, regulator, clock, reset, IRQ state, workers, subsystem identifier and userspace publication. Acquire only after all prerequisites for that stage. Register device-managed cleanup immediately after each managed acquisition; use a devres group to roll back a subtransaction such as optional queue creation.

Explicit quiescence precedes mechanical reverse release: block new I/O and unpublish, stop the hardware producer, synchronize IRQ and DMA, cancel and join work and timers, then let managed actions free IRQs, disable suppliers, unmap, release reservations and free memory. Inject failure after every acquisition and inside initialization, assert no interface or resource remains, and retry probe. Successful probe closes the initialization transaction but retains the same ordered remove plan. Managed reverse order is inspected rather than assumed to encode semantic shutdown.

### Answer 3

The PCI function is parent to logical network and storage child devices. A shared coordination object owned by the parent controls firmware image, power state, reset serialization and physical removal. Both children are consumers of parent firmware and power readiness; the parent or each child is a consumer of the IOMMU according to the platform representation. Device links encode non-parent suppliers and runtime power.

Probe the parent far enough to load and validate firmware and establish shared resources before registering children. Children bind independently but hold parent and coordination references. Reset requires both to quiesce or uses a generation protocol that makes in-flight operations fail safely. Unbind children before the parent and consumers before IOMMU or power suppliers. Reject dependency cycles. On partial child creation, unregister created children and wait for final references. Hot-unplug marks the parent disconnected once, fans out stop to both functions, contains DMA, drains callbacks and releases physical resources after both detach.

### Answer 4

Orderly unbind first serializes against probe, power transitions and new opens, marks quiescing, removes userspace reachability and waits or causes current operations to finish under the subsystem contract. Stop device production, mask interrupts, cancel submissions, wait for or abort DMA, synchronize hard and threaded handlers, publish stopped state, cancel timers synchronously so callbacks cannot rearm, drain workers, release queues and identifiers, power down, detach suppliers and return from remove. Open files retain object references but operations observe disconnected state until close triggers final release.

Surprise removal begins with hardware already inaccessible. Mark disconnected without requiring register acknowledgement, stop software submission, contain DMA through the bus and IOMMU, complete users with defined errors, and use bounded timeouts for missing completions. Synchronize callbacks before freeing state. A supplier suspend racing either path is held off by device-link and core lifecycle serialization or sees consumers already inactive. Test every interleaving, including callback rearm, late IRQ, late DMA completion, close after unbind, and a device reappearing at the same bus address with a new identity generation.

### Answer 5

Specify authoritative enumeration source, identifier scopes, match tables, containment and supplier graphs, lifecycle states, resource tokens, interfaces, callback contexts, power phases, error classes and trust boundaries. Test device-first and driver-first order, parallel probes, multiple matches, optional and missing suppliers, graph cycles, deferred retry, permanent errors, every allocation and hardware failure, partial publication, repeated bind and module cycles, retained references, hostile descriptors and userspace event races.

Exercise normal I/O, concurrency, runtime suspend during arrival, system suspend at each state, resume failure, shutdown, orderly removal, surprise loss, interrupt storms, DMA in flight, callback rearming, hot-add, multifunction reset and final release. Assert exclusive resource ownership, one driver binding, complete failure unwind, supplier order, no new work after disconnect, no callback or DMA after free, and exact reference balance. Preserve kernel, module, firmware, hardware, topology, sysfs and event snapshots, fault seeds, traces, timing, lost events, negative results, reviewers and limitations.
