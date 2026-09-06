---
module_id: SARCH-059
program: Software Engineering: Software Architecture
level: 2
module_number: 59
title: Edge and Hybrid Architectures
status: complete
last_verified: 2026-09-06
---

# Edge and Hybrid Architectures

## One-Page Review

### Governing question

Which decisions, data, and controls must remain near devices and physical processes, which belong in regional or cloud systems, and how can the whole system preserve bounded safety, authority, security, and convergence across intermittent links and heterogeneous ownership?

### Essential definitions

- The **edge** is computation and storage placed near data sources, users, networks, or physical processes to meet locality, latency, autonomy, bandwidth, privacy, or availability needs.
- A **device edge** runs on or beside a sensor, actuator, vehicle, or user device; an **edge site** aggregates one facility or local network; a **regional edge** serves several sites before a central cloud or data center.
- **hybrid architecture** integrates resources across on-premises, edge, hosted, and cloud environments under explicit authority and operating boundaries.
- A **gateway** mediates protocol, identity, buffering, policy, aggregation, or translation; it is not automatically the system of record.
- **disconnected operation** continues a declared subset of service without upstream communication.
- **store-and-forward** durably buffers information for later transmission; **synchronization** exchanges state or operations; **reconciliation** resolves their meaning and outcomes.
- A **digital twin** is a digital representation of an identified physical entity or process under a defined authority and freshness contract; it is not the physical entity.
- **command authority** identifies who may cause an actuator or operational change at a given epoch.
- **fleet management** provisions, configures, updates, observes, rotates, quarantines, and retires edge nodes.
- A **trust anchor** is a protected root used to establish identity or software/configuration trust.

### Central model, mechanism, or theorem

An offline buffer must cover admitted production during the isolation interval. For event rate $\lambda$, mean encoded size $s$, and disconnection duration $T$, a lower-bound byte requirement is

$$
B_{min}=\lambda sT.
$$

At 500 events/s, 200 bytes/event, and six hours, $B_{min}=500\cdot200\cdot21{,}600=2.16\times10^9$ bytes, or 2.16 GB using decimal units. Indexes, metadata, filesystem reserve, retries, burst, compression variability, and safe shutdown require additional capacity.

An end-to-end control deadline $D$ must cover sensing, communication, queueing, decision, actuation, and safety margin. If required remote communication can exceed $D$, cloud control cannot be on the safety-critical loop; local bounded authority or a fail-safe mechanism is necessary.

### Critical invariants

- every physical command names authenticated actor, target, authority epoch, validity interval, preconditions, and observable acknowledgement;
- safety-critical behavior does not depend on a network path whose delay or availability lies outside its deadline;
- edge autonomy is bounded by explicit capability, policy age, resource rights, and fail-safe state;
- upstream acceptance, local execution, physical effect, and reconciliation are distinct outcomes;
- buffers are bounded by bytes, age, priority, privacy, endurance, and drain capacity, not record count alone;
- device, event, command, software, model, configuration, and schema identities are durable and versioned;
- duplicates, reorder, clock error, intermittent delivery, and replay cannot silently violate invariants;
- gateways authenticate both directions and do not turn legacy trust into transitive global trust;
- fleet updates are signed or authenticated, compatible, staged, reversible or forward-repairable, and independently stoppable;
- secrets and private data are minimized and protected against physical capture;
- quarantine limits compromised or anomalous nodes without erasing essential local safety;
- bandwidth reduction preserves required evidence, not just averages;
- reconnect traffic, updates, repair, and replay fit upstream and local capacity;
- retirement revokes identity, erases governed data, and removes authority.

### Common failures

Common failures include putting a hard real-time safety loop behind a cloud round trip; treating a gateway cache as authoritative; assuming site clocks order events globally; buffering until disk full; replaying stale commands after reconnection; granting every edge node one fleet-wide credential; shipping unsigned updates; depending on warm network bootstrap; aggregating away evidence required for diagnosis or regulation; connecting an unauthenticated legacy protocol to a trusted event bus; accepting offline inventory without allocated rights; updating every remote site at once; using remote reset as the only response to compromise; and declaring synchronization complete when bytes match but physical and business outcomes do not.

### Compact example

A refrigerated depot samples 500 measurements/s at 200 bytes. Six disconnected hours require at least 2.16 GB before overhead. The site keeps local temperature alarms and compressor interlocks, aggregates ordinary readings, retains excursions losslessly, signs batches with device identity, and drains with priority and rate limits after reconnection. The cloud holds fleet analytics, not the immediate food-safety loop.

### Connections

[SARCH-053](053-partitioning-and-data-placement.md) supplies placement, [SARCH-054](054-multi-region-topologies.md) supplies regional authority, and [SARCH-058](058-serverless-and-event-native-architecture.md) supplies event-driven execution. [SARCH-060](../ROADMAP.md) next examines service meshes and traffic policy. Systems Engineering owns physical-system integration; this module owns architectural distribution and hybrid consequences.

## Governing Question

Central clouds concentrate capacity, data, and operational control, but physical systems exist where networks are finite, delayed, costly, regulated, or absent. Some decisions lose value after milliseconds; some sites must operate for days while isolated; some raw data should never leave the source.

Moving computation outward does not remove distributed-systems problems. It adds device diversity, physical access, limited storage and power, clock uncertainty, long-lived software, ownership boundaries, and reconciliation with the real world. Architecture must allocate authority, not just workloads.

## Why This Matters

Edge failure can affect machines, medicine, vehicles, energy, and public safety. A stale cloud representation may look healthy while a valve is stuck or a shipment is warming. Conversely, an isolated local controller can act on obsolete global policy and conflict with later central commands.

Hybrid systems also persist for decades. Legacy protocols, on-premises constraints, and cloud services evolve at different speeds. Durable boundaries, signed identities, compatible schemas, staged updates, and operational evidence matter more than one uniform platform.

## Prerequisites and Retrieval

Retrieve latency budget, jitter, deadline, sensor, actuator, control loop, gateway, event, command, authority, epoch, fencing, queue, store-and-forward, idempotency, conflict, clock drift, schema, digital twin, region, residency, trust anchor, secure boot, attestation, update, rollback, quarantine, and reconciliation.

From SARCH-035 and SARCH-044 retrieve event and message semantics; SARCH-049 provides environment topology; SARCH-051 provides partial failure; SARCH-052 provides consistency trade-offs; SARCH-053 through SARCH-054 provide placement and regional structure; and SARCH-055 through SARCH-058 provide control, cells, queues, and event-native execution.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish device, site, regional, on-premises, and central responsibilities;
2. allocate control authority from latency, safety, connectivity, and domain invariants;
3. size simple offline buffers and reconnect drain while stating limitations;
4. design local autonomy, rights, expiry, and fail-safe behavior;
5. reconcile events, commands, twins, and physical observations under clock uncertainty;
6. preserve security under physical access, credential theft, and long-lived fleet software;
7. evolve software, configuration, models, and schemas across intermittent fleets;
8. integrate legacy and cloud systems without extending implicit trust;
9. govern bandwidth reduction, residency, privacy, and evidentiary retention;
10. test disconnected, degraded, reconnect, compromise, and retirement behavior.

## Core Exposition

**Begin with physical deadlines and authority.** Enumerate sensing, decisions, commands, actuators, and consequences. For each, state maximum useful or safe delay, behavior on missing data, authorized actor, and physical acknowledgement.

If the network cannot meet the deadline under declared faults, place the decision locally or design an independent fail-safe. Remote optimization can propose targets while a local controller enforces pressure, speed, temperature, or dosage bounds. Central convenience never outranks physical timing evidence.

**Separate layers by responsibility.** A device performs direct sensing or actuation. A site gateway can translate protocols, buffer, aggregate, and enforce local policy. A regional layer coordinates several sites. Central systems manage fleet policy, global optimization, long-term analytics, and cross-site authority where latency permits.

These are logical roles, not mandatory products. A rugged computer may host device and site roles; a cloud region may host regional and central roles. Name fault, trust, ownership, and data boundaries explicitly.

**Design bounded disconnected operation.** List what continues, pauses, rejects, or enters emergency mode when upstream is absent. Local capability needs valid configuration, credentials, time assumptions, resource capacity, and a way to expose degradation.

Autonomy is not unlimited delegation. Use allocated inventory rights, bounded operating envelopes, cached deny rules, expiring permits, and local human authority. Stop or fail safe when evidence or policy becomes too old for the harm model.

**Distinguish commands from facts.** A command can expire and should not execute merely because it eventually arrives. An event records what an authority observed or decided. Physical acknowledgement records observed actuation, not perfect physical truth.

Give commands stable identity, target, authority epoch, issued time, not-before/expiry, preconditions, and desired acknowledgement. Reject duplicates and stale epochs. Events carry device identity, source sequence, schema, event time, observation uncertainty, and ingestion time.

**Treat the twin as a model.** A digital twin may contain last observation, inferred state, desired state, and command status. Label each with source, version, time, and uncertainty. “Valve open” may mean commanded open, actuator acknowledged, or independent sensor confirmed; these are different.

Never use a stale twin as unqualified authority for a physical safety decision. Reconcile on reconnect by comparing command history, device log, independent observation, and domain rules. Preserve disagreements rather than overwriting them by last timestamp.

**Model clock uncertainty.** Edge clocks drift, reset, lose synchronization, and may be malicious. Wall-clock order from different devices is not a causal or authority order. Use device sequences, causation identities, authority epochs, and bounded clock uncertainty where time matters.

Event time supports physical analysis; ingestion time supports pipeline behavior. Record both. If a deadline depends on trusted time, define the time source, maximum error, holdover, and expiry behavior.

**Size store-and-forward honestly.** Multiply admitted rate, encoded size, and isolation duration for a lower bound. Add burst, index, metadata, transaction log, encryption, filesystem reserve, wear, and failure reserve. Segment priorities and privacy classes.

Define full behavior before capacity ends: aggregate, sample, compress, overwrite low-value history, stop acquisition, or degrade the physical process. Never let audit or safety events be crowded out by bulk telemetry. Monitor remaining time at current rate, not only free bytes.

**Plan reconnect drain.** When a site reconnects, new data continues while backlog drains. If upstream service rate does not exceed ongoing production, backlog cannot clear. Software updates, certificate renewal, configuration, and operator queries compete for the same link.

Prioritize current safety policy and command reconciliation before bulk history. Add randomized reconnect, bandwidth caps, checkpointed transfer, deduplication, and resumable batches. Avoid fleet-wide thundering herds after a carrier outage.

**Reduce bandwidth under domain policy.** Filter, aggregate, compress, detect changes, or run inference locally when raw data is costly or private. Preserve raw evidence around anomalies and maintain enough provenance to audit the derived result.

An average can erase a short hazardous excursion. A model classification may drift or fail out of distribution. State what is discarded, sampling bias, error bounds, model/version, retrievability, and who approved the trade-off.

**Place data by lifecycle.** Some data stays on device; some reaches a site record; some is summarized centrally. Define system of record, retention, deletion, residency, backup, restore, and legal access at every tier.

Replication to cloud does not make the device disposable if the latest state is offline. A restored device must not resurrect deleted personal data or accept obsolete commands. Apply deletion and revocation epochs before ordinary synchronization.

**Use rights for offline bounded resources.** Inventory, quotas, reservations, energy budgets, or controlled actions can be divided into non-overlapping local rights. An isolated site consumes only its allocation, preserving the global bound.

Rights trade utilization for autonomy. One site may exhaust its share while another holds unused capacity. Transfer requires safe communication, identity, and conservation evidence. Emergency override is a distinct accountable policy.

**Secure device identity.** Provision each device or site with unique scoped identity rooted in protected manufacturing, enrollment, or installation. Support rotation, revocation, replacement, and retirement. Shared fleet secrets make one extraction a fleet compromise.

Secure boot and attestation can support software trust under their documented hardware and service assumptions. They do not prove application correctness or physical integrity. Define behavior when attestation or identity service is unavailable.

**Assume physical access.** Attackers may capture storage, probe buses, replace sensors, clone credentials, or interrupt power. Minimize secrets and private data locally, encrypt where threat and key custody support it, detect tamper where useful, and constrain what one node can authorize.

Quarantine anomalous nodes from global systems while retaining necessary local fail-safe behavior. Remote wipe may fail precisely when a device is offline; revocation and server-side authorization must contain it.

**Protect the software supply chain.** Authenticate firmware, applications, configuration, models, and schema. Bind artifact identity to compatible hardware and state. Prevent downgrade below a security or safety floor.

Updates use staged cohorts, health and capability probes, power and connectivity preconditions, atomic activation where possible, and rollback or forward repair. Dual-bank firmware can recover some failures; irreversible data migrations need compatibility and backup.

**Manage heterogeneous fleets.** Hardware revisions, operating systems, accelerators, carrier networks, and local regulations differ. Maintain an inventory of device identity, capabilities, owner, location, software, configuration, model, certificates, storage, and support horizon.

Compatibility policy maps desired features to capability classes. Avoid silently leaving old devices on insecure versions. Define replace, isolate, degrade, or retire decisions with owners and customer communication.

**Integrate legacy protocols at a trust boundary.** Industrial and building protocols may lack modern identity, encryption, replay protection, or multi-tenant separation. A gateway validates ranges, rate, direction, device mapping, and command authority before translating.

Do not expose the legacy network directly to a cloud bus. Separate read telemetry from actuator commands. Constrain egress and ingress, preserve protocol-specific semantics, and test malformed, replayed, and out-of-range messages.

**Design hybrid connectivity as partial failure.** Private links, VPNs, carrier networks, satellite, public Internet, DNS, certificates, firewalls, and routes can fail asymmetrically. One direction may work while acknowledgement does not.

Use durable identity and explicit connection state, not reachability as trust. Timeouts do not prove remote non-execution. Gateways reconnect with bounded retry, and central services tolerate duplicate sessions and stale sites.

**Separate control and data planes.** Devices may continue data-plane operation from installed valid policy while fleet control is unavailable. New provisioning, privilege, update, and routing changes stop or use bounded regional authority.

Model cold bootstrap: identity, trust roots, time, configuration, software, network, and local safety state. A warm site surviving cloud loss does not prove a power-restored site can restart safely.

**Design edge analytics and inference.** Local inference reduces latency and raw-data transfer but consumes power, memory, and accelerator capacity. Models need identity, training-data lineage, validation scope, drift observation, rollback, and fallback.

Confidence alone may be poorly calibrated. High-risk decisions need thresholds, independent rules, human review, or safe default. Record model input provenance and result without retaining prohibited raw data.

**Observe across gaps.** Record device/site identity, boot and authority epoch, software/config/model/schema version, local sequence, event and ingestion time, clock status, connectivity, buffer age and bytes, command state, physical acknowledgement, security posture, and reconciliation outcome.

Telemetry absence can mean network failure, power loss, sensor failure, or a compromised node. Do not infer a healthy quiet process. Preserve local audit and retrieve it securely after reconnection.

**Retire deliberately.** Remove command authority, revoke credentials, drain or archive governed data, erase secrets and personal data, update directory and routing, record physical disposition, and prevent a returned old device from reenrolling silently.

Lost devices need revocation without remote contact. Replacement receives a new identity and reconciles authoritative state; cloning the old identity destroys provenance.

**Test the whole lifecycle.** Exercise high delay, loss, asymmetric partition, clock reset, buffer full, power cycle, stale command, duplicate event, compromised credential, malicious update, model failure, legacy protocol replay, reconnect herd, central outage, and retirement.

Verify physical and business outcomes, not only message delivery. Hardware, firmware, network, environmental, and safety tests require recorded versions and conditions. Simulation supports but does not replace appropriate field and physical verification.

## Definitions and Notation

Let:

- $\lambda$ be admitted event rate and $s$ mean encoded bytes per event;
- $T$ be planned disconnected duration and $B_{min}=\lambda sT$ the storage lower bound;
- $\mu$ be sustainable upstream drain rate after reconnection;
- $D$ be end-to-end action deadline;
- $t_s,t_n,t_q,t_d,t_a,t_m$ be sensing, network, queue, decision, actuation, and safety-margin times;
- $e$ be command authority epoch and $q_i$ a device-local monotonic sequence;
- $\epsilon_i$ be the declared clock-error bound for device $i$ when such a bound is valid;
- $R=b_{raw}/b_{sent}$ be a bandwidth-reduction ratio over a named interval;
- $r_i$ be locally allocated right balance for bounded resource $i$;
- **holdover** mean operation using a local time source after reference synchronization is lost;
- **quarantine** mean restricted interaction imposed on a suspected or compromised node;
- **physical reconciliation** mean comparing digital intent and evidence with observed real-world state.

A simple deadline budget requires $t_s+t_n+t_q+t_d+t_a+t_m\le D$. The inequality is meaningful only when bounds, not averages, match the safety claim and relevant parallel or conditional paths are modeled correctly.

## Mechanisms, Invariants, or Proof Structure

### Edge allocation procedure

1. Name physical assets, actors, authorities, hazards, invariants, and deadlines.
2. Classify device, site, regional, on-premises, and central responsibilities and records.
3. Define normal, disconnected, stale-policy, resource-exhausted, compromised, and fail-safe behavior.
4. Define command/event identities, epochs, sequences, time uncertainty, acknowledgement, and reconciliation.
5. Size compute, power, storage, bandwidth, buffer, drain, and local rights with reserve.
6. Define device trust, credentials, updates, secrets, privacy, residency, legacy boundaries, and quarantine.
7. Define schema, configuration, model, hardware compatibility, staged rollout, rollback, and support horizon.
8. Observe locally and centrally; reconcile digital, business, and physical outcomes.
9. Test bootstrap, isolation, overload, compromise, reconnection, recovery, and retirement.

### Buffer and drain derivation

Constant admitted production creates $\lambda T$ events over isolation $T$, requiring $\lambda sT$ encoded bytes before overhead. If production continues at $\lambda$ events/s and reconnect transmission/ingestion sustains $\mu>\lambda$, event backlog drains ideally at $\mu-\lambda$. If $\mu\le\lambda$, it never clears without reducing admitted work, increasing capacity, aggregating validly, or changing the contract.

### Architectural invariants

- no remote dependency sits on a safety path it cannot bound;
- no edge command executes outside its authority epoch, target, validity, and preconditions;
- no full buffer silently destroys higher-priority safety or audit evidence;
- no reconnect replay treats stale commands as current facts;
- no captured node gains fleet-wide authority;
- no byte-level synchronization substitutes for physical and business reconciliation.

## Alternatives and Trade-Offs

| Choice | Strength | Cost or risk | Required evidence |
|---|---|---|---|
| central decision | global context and simpler policy | network latency and outage dependency | deadline and degraded behavior |
| device-local control | lowest latency and autonomy | constrained compute and fleet risk | safety bounds and update tests |
| site gateway | protocol mediation and aggregation | concentrated local failure/trust | redundancy and bypass behavior |
| regional edge | cross-site coordination | another control/data tier | placement and failure model |
| raw upload | complete central evidence | bandwidth, privacy, storage | retention and access policy |
| local aggregation | lower bandwidth and latency | lost detail and bias | error/evidence analysis |
| store-and-forward | disconnected capture | storage, age, and drain debt | full and reconnect tests |
| offline rights | bounded local action | stranded capacity and transfer | conservation audit |
| remote fleet update | scalable maintenance | widespread bad rollout | signing, cohorts, rollback |
| legacy gateway | bounded modernization | semantic and trust translation | protocol and adversarial tests |

## Failure Modes and Misconceptions

1. **“Edge means low latency.”** placement helps only if the full decision path is local and bounded.
2. **“Hybrid means portable.”** interfaces, identity, operations, and data semantics may remain coupled.
3. **“The gateway is the authority.”** mediation does not create domain ownership.
4. **“Offline means eventually sync.”** conflicts, expiry, rights, and physical effects require policy.
5. **“A twin is the asset.”** it is a versioned observation and intent model.
6. **“Device timestamps give global order.”** drift and reset defeat naive comparison.
7. **“Buffer capacity solves disconnection.”** age, drain, endurance, and full behavior remain.
8. **“Aggregation loses nothing important.”** rare excursions and provenance can disappear.
9. **“One device credential simplifies fleet trust.”** compromise then becomes fleet-wide.
10. **“Secure boot proves safe software.”** it authenticates a chain under assumptions, not behavior.
11. **“Remote wipe contains capture.”** the captured device may remain offline.
12. **“Signed updates cannot harm.”** authorized faulty software is still faulty.
13. **“Cloud health means site health.”** physical and connectivity state can diverge.
14. **“Reconnection should upload everything immediately.”** herd and backlog can overload recovery.
15. **“Legacy protocol behind a firewall is trusted.”** identity and semantic controls are still needed.
16. **“Decommission means delete from dashboard.”** authority, credentials, data, and hardware persist.

## Worked Examples

### Example 1

**Situation.** A machine interlock must stop motion within 20 ms, while the measured cloud round trip sometimes exceeds 80 ms.

**Reasoning.** Remote decision cannot meet the deadline even before queue and actuation. Put the interlock in local hardware or bounded local control; let cloud systems set approved operating envelopes and collect evidence. Loss of cloud must not disable the stop.

**Conclusion.** Physical deadline places safety authority locally.

### Example 2

**Situation.** A depot emits 500 records/s at 200 bytes and must survive six disconnected hours.

**Reasoning.** Lower bound is $500\cdot200\cdot21{,}600=2.16$ GB decimal. Add index, transaction log, encryption, burst, filesystem, wear, and safety reserve. Preserve alarm excursions ahead of routine samples and define behavior before full.

**Conclusion.** Offline capacity begins with rate-size-time arithmetic and ends with priority and failure policy.

### Example 3

**Situation.** A clinic has ten vaccine doses and operates offline while a central system also advertises them.

**Reasoning.** Allocate non-overlapping local rights before disconnection; the clinic administers only its local balance and records immutable identities. Central availability reflects transferred rights. On reconnect, reconcile physical stock, administrations, spoilage, and reservations.

**Conclusion.** Offline invariant-safe action needs conserved rights, not a stale replicated count.

### Example 4

**Situation.** A cloud command says open a valve, but it arrives after a newer local emergency close.

**Reasoning.** The close has later authority epoch and safety state. The device rejects the stale open regardless of wall-clock timestamp, records the rejection, and reports current physical observation. Replaying every queued command in receipt order would be unsafe.

**Conclusion.** Commands require authority, validity, and precondition checks at execution.

### Example 5

**Situation.** A gateway reports `door=open`, but the dashboard cannot distinguish command from sensor state.

**Reasoning.** Represent desired command, actuator acknowledgement, independent contact sensor, times, sequences, and uncertainty separately. If they disagree, surface conflict and follow physical safety policy rather than overwriting by latest arrival.

**Conclusion.** A digital twin must preserve provenance and epistemic status.

### Example 6

**Situation.** Local aggregation sends one-minute temperature averages and hides a ten-second dangerous excursion.

**Reasoning.** Average is insufficient for the safety requirement. Send min/max and excursion events, preserve raw windows around threshold crossings, identify sensor and algorithm version, and validate false-negative behavior under noise.

**Conclusion.** Bandwidth optimization must preserve domain-relevant evidence.

### Example 7

**Situation.** A carrier outage ends and 30,000 sites reconnect simultaneously.

**Reasoning.** If each uploads backlog, renews certificates, fetches updates, and reports inventory at once, central services and links can fail. Randomize reconnect, prioritize current safety policy and command reconciliation, cap upload, checkpoint batches, and drain by age/value.

**Conclusion.** Reconnection is a fleet-scale recovery workload requiring admission and priority.

### Example 8

**Situation.** One field device is stolen and contains a credential shared by the fleet.

**Reasoning.** Remote wipe may never arrive, and revoking the secret disables all devices. Use unique scoped device identities, server-side revocation, limited rights, protected keys, replacement identity, and anomaly detection. Quarantine the device without granting it neighbor access.

**Conclusion.** Physical capture must have device-sized, not fleet-sized, authority.

### Example 9

**Situation.** An update works on recent hardware but exhausts memory on an older revision at remote sites.

**Reasoning.** Inventory capability classes, validate artifacts against each, canary representative old hardware, require power/storage preconditions, cap rollout, and retain a compatible rollback or forward repair. Sites report activated version and capability behavior.

**Conclusion.** Fleet updates require hardware-aware compatibility and staged evidence.

### Example 10

**Situation.** A legacy building bus accepts unauthenticated actuator frames, and a gateway connects it to a cloud event bus.

**Reasoning.** Separate telemetry and command paths. Authenticate cloud actor, validate device mapping, ranges, rate, epoch, and expiry at the gateway; constrain network direction; record translation; and reject replay. Local mechanical interlocks remain authoritative.

**Conclusion.** A hybrid gateway terminates and rebuilds trust rather than extending it transitively.

## Cross-Program Connections

- **Systems Engineering:** owns physical requirements, hazards, control loops, human operation, and lifecycle assurance.
- **Platform Engineering:** owns fleet enrollment, configuration, update, observability, quarantine, and developer interfaces.
- **Cloud Engineering:** owns regional/cloud services, hybrid connectivity, identity, cost, and shared responsibility.
- **Distributed Systems Engineering:** owns replication, clocks, partitions, consensus, epochs, and reconciliation protocols.
- **Security Engineering:** owns device trust, physical capture, supply chain, credentials, attestation, and incident containment.
- **Data Engineering:** owns event-time ingestion, late data, aggregation, buffering, replay, and analytical quality.
- **Data Architecture Engineering:** owns authority, residency, retention, deletion, lineage, and twin governance.
- **Software Delivery and Reliability Engineering:** owns fleet rollout, SLOs, incident response, recovery tests, and evidence.

## References

1. Mahadev Satyanarayanan, “The Emergence of Edge Computing,” *Computer* 50(1), 2017. <https://doi.org/10.1109/MC.2017.9>
2. Weisong Shi et al., “Edge Computing: Vision and Challenges,” *IEEE Internet of Things Journal* 3(5), 2016. <https://doi.org/10.1109/JIOT.2016.2579198>
3. Mahadev Satyanarayanan et al., “The Case for VM-Based Cloudlets in Mobile Computing,” *IEEE Pervasive Computing* 8(4), 2009. <https://doi.org/10.1109/MPRV.2009.82>
4. Michaela Iorga et al., *Fog Computing Conceptual Model*, NIST Special Publication 500-325, 2018. <https://doi.org/10.6028/NIST.SP.500-325>
5. RFC 7228, “Terminology for Constrained-Node Networks,” IETF, May 2014. <https://www.rfc-editor.org/rfc/rfc7228>
6. Edward A. Lee, *Plato and the Nerd: The Creative Partnership of Humans and Technology*, MIT Press, 2017.
7. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
8. Betsy Beyer et al., eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>

## Exercises

### Exercise 1

Define edge, device edge, edge site, regional edge, hybrid architecture, gateway, disconnected operation, store-and-forward, synchronization, reconciliation, digital twin, command authority, fleet management, trust anchor, holdover, quarantine, and physical reconciliation.

### Exercise 2

A site produces 1,200 events/s averaging 350 bytes and must buffer 18 hours. Calculate the decimal byte lower bound. After reconnect, sustainable upload is 2,000 events/s while production continues. Calculate ideal event-backlog drain time. State omitted capacity and correctness factors.

### Exercise 3

Diagnose an edge fleet that uses one shared secret, trusts device timestamps, executes every queued command after reconnect, stores until disk full, updates all sites simultaneously, and treats gateway state as physical truth. Provide a safe architecture and evidence.

### Exercise 4

Compare cloud-central, device-local, site-gateway, regional-edge, and hybrid legacy/cloud placement for industrial interlock, retail inventory, video analytics, software updates, and long-term reporting. Address deadlines, authority, bandwidth, privacy, failure, and operation.

### Exercise 5

Design edge and hybrid architecture for an international coastal flood-warning and barrier-control network with tide gauges, weather feeds, pumps, gates, sirens, municipalities, intermittent islands, legacy controllers, public alerts, environmental rules, and emergency crews. Cover authority, deadlines, local autonomy, buffers, clocks, rights, security, updates, data governance, reconnect, physical reconciliation, and human control.

## Answers to the Exercises

### Answer 1

The **edge** places compute or storage near source, user, network, or physical process. **Device edge** runs on or beside an asset; an **edge site** aggregates one facility; a **regional edge** coordinates several sites. **Hybrid architecture** spans on-premises, edge, hosted, and cloud ownership. A **gateway** mediates protocol or policy. **Disconnected operation** continues bounded service without upstream. **Store-and-forward** buffers for later transfer; **synchronization** exchanges state; **reconciliation** resolves meaning and outcomes. A **digital twin** is a versioned digital representation, not the asset. **Command authority** grants actuation scope. **Fleet management** controls device lifecycle. A **trust anchor** roots identity or artifact trust. **Holdover** uses local time after losing reference. **Quarantine** restricts a suspect node. **Physical reconciliation** compares digital records with observed reality.

### Answer 2

Eighteen hours is 64,800 seconds. The lower bound is $1{,}200\cdot350\cdot64{,}800=27{,}216{,}000{,}000$ bytes, or 27.216 GB decimal. The event backlog is $1{,}200\cdot64{,}800=77{,}760{,}000$ events. Net drain after reconnect is $2{,}000-1{,}200=800$ events/s, so ideal drain takes $77{,}760{,}000/800=97{,}200$ seconds, or 27 hours. Omitted factors include burst, size distribution, compression, metadata, indexes, filesystem reserve, endurance, failed records, retries, priority, bandwidth variation, upstream processing, privacy retention, event expiry, schema compatibility, and reconciliation.

### Answer 3

Enroll unique scoped device identities rooted in protected trust, with independent rotation, revocation, replacement, and retirement; one extraction must not compromise the fleet. Treat wall clocks as uncertain: preserve device sequence, event and ingestion time, authority epoch, causation, and declared time-source error. Commands carry identity, target, epoch, validity, preconditions, and expected acknowledgement; devices reject stale, duplicate, expired, or unsafe commands rather than replaying blindly.

Bound storage by bytes, age, priority, privacy, endurance, and drain. Reserve safety and audit evidence; define aggregation, shedding, and fail-safe behavior before full. Roll updates through hardware-representative cohorts with authenticated artifacts, compatibility checks, stop conditions, and rollback or forward repair. Model the twin as desired state, command acknowledgement, and independent physical observations with provenance, never one gateway field. Evidence includes identity, boot/authority epoch, versions, sequences, clocks, buffer, connectivity, command lifecycle, physical sensors, update cohort, security posture, and reconciled business/physical outcome. Test capture, clock reset, full disk, reconnect, bad update, stale command, and retirement.

### Answer 4

Industrial interlocks belong in local hardware or bounded device/site control; cloud supplies policy and evidence outside the hard deadline. Retail inventory can use site-local allocated rights and central reconciliation; pure central authority sacrifices offline sales. Video analytics may filter or infer at device/site to reduce bandwidth and privacy exposure, with regional aggregation and selected governed raw evidence. Fleet updates use central desired state, regional caches, and local authenticated atomic activation. Long-term reporting generally belongs centrally but accepts delayed, versioned events.

Central placement provides global capacity and context but adds link dependency. Device placement minimizes latency and maximizes autonomy but faces power, compute, physical security, and fleet complexity. Gateways mediate legacy protocols and buffer but concentrate site trust. Regional edge balances cross-site coordination and backhaul use while adding another tier. Hybrid placement is often required; it succeeds only with explicit authority, identity, time, failure, compatibility, and reconciliation boundaries.

### Answer 5

Local gate and pump controllers own hard safety interlocks and bounded water-level rules; municipal incident command owns operating epochs within national environmental constraints. Central forecasting proposes plans but cannot bypass physical limits. Commands carry asset, epoch, issue/expiry, preconditions, range, and acknowledgement. Islands retain signed valid envelopes, local sensor fusion, siren authority, allocated fuel/energy rights, and named crew override; when evidence ages beyond limits, gates enter engineered fail-safe states.

Gateways separate legacy telemetry from commands, authenticate cloud and municipal actors, validate ranges and replay, and keep mechanical interlocks independent. Gauge events carry identity, boot sequence, event/ingestion times, clock status, schema, and quality. Buffers reserve alarms, commands, and audit before bulk samples; local aggregation preserves extrema and raw flood windows. Drain prioritizes current policy and reconciliation, then history, with randomized reconnect and capacity caps.

Unique device identities, protected trust anchors, signed artifacts, scoped network access, physical-capture containment, revocation, and quarantine limit compromise. Updates canary every hardware and island class, require safe water/power/connectivity state, and support rollback. Residency, public-alert privacy, environmental evidence, logs, backup, deletion, and support access follow jurisdiction. Twins distinguish forecast, desired gate, acknowledgement, independent position sensor, and observed water.

On restoration, reject stale epochs, deduplicate events, compare commands with physical gate/pump state, reconcile fuel and maintenance, and investigate gaps before ordinary automation resumes. Evidence records model/forecast, authority, device and artifact versions, sensor provenance, buffer age, command and physical acknowledgement, crew action, public-alert supersession, environmental outcome, and recovery decision. Tests include asymmetric island partition, clock loss, false gauge, stuck gate, full buffer, stolen node, bad update, carrier-wide reconnect, central compromise, and manual operation. Independent local stops and named municipal/emergency authorities remain available when remote control fails.
