---
module_id: NET-001
program: Network Engineering
level: 1
module_number: 1
title: Network Requirements: Reachability, Capacity, Delay, and Loss
status: complete
last_verified: 2026-08-29
---

# Network Requirements: Reachability, Capacity, Delay, and Loss

## One-Page Review

### Governing question

How should an engineer turn “the network must connect our systems and be fast and reliable” into directional, workload-bound, measurable requirements for reachability, capacity, delay, variation, and loss?

### Essential definitions

- **Reachability** is the ability of a specified source to deliver a specified traffic type to a destination under stated time and policy conditions. It is directional and is not identical to application success.
- **Capacity** is an upper bound on a defined layer's transfer rate over a link or path under stated conditions. Nominal link rate, IP-layer capacity, available capacity, throughput, and application goodput are different quantities.
- **Offered load** is traffic presented for delivery; **carried load** is traffic successfully transported at the measurement point.
- **Delay** is elapsed time between defined events. One-way delay needs clocks and measurement points; round-trip time combines forward and reverse paths plus remote processing.
- **Packet delay variation** describes variation among packet delays under a named definition. “Jitter” is too overloaded to stand alone as a requirement.
- **Loss** occurs when a packet in the measurement population is not observed at the destination within the declared waiting interval and rules.
- A **service-level objective** is a target for a metric over a population and evaluation window, not a promise that every packet or request succeeds.
- A **traffic matrix** identifies source, destination, direction, traffic class, offered rate, packet-size distribution, concurrency, and time pattern.

### Central model, mechanism, or theorem

A usable network requirement is a tuple

$$
R=(S,D,P,W,F,M,\theta,E),
$$

where $S,D$ are endpoints or sets, $P$ is traffic type and direction, $W$ is workload, $F$ is failure/maintenance condition, $M$ is a precisely defined metric and method, $\theta$ is its threshold and statistical scope, and $E$ is required evidence. Requirements form a vector, not one “speed”: reachability, sustainable goodput, delay quantiles, delay variation, loss, availability, recovery, and security policy can constrain one another.

### Critical invariants

Every metric names source, destination, direction, protocol/packet population, layer, time interval, units, statistic, threshold, and measurement method. Offered load is representative and below or intentionally above the declared operating envelope. Loss and delay share a consistent population and timeout rule. Averages never replace required tail quantiles. Measurements distinguish network behavior from endpoint, application, and test-tool limits. Failure-mode requirements name the failed component and convergence/recovery window.

### Common failures

Frequent mistakes include treating a successful ping as universal reachability, reading interface line rate as application capacity, specifying “latency under 20 ms” without direction or percentile, averaging away outages, reporting zero loss from a tiny sample, measuring round-trip time and dividing by two, ignoring packet size and cross traffic, testing only an idle network, demanding mutually inconsistent load and delay thresholds, or interpreting a speed-test result as a topology-independent guarantee.

### Compact example

A replication flow from site A to site B offers 400 Mbit/s during a two-hour window. Its requirement might say: over approved encrypted transport and production-size packets, sustain at least 500 Mbit/s application goodput at p95 five-minute intervals, keep one-way network delay p99 below 35 ms and packet loss below 0.05%, and restore these bounds within 60 seconds after any single edge-link failure. This is testable; “provide a 1-Gbit/s connection” is not an equivalent service requirement.

### Connections

Later network modules explain signals, layering, propagation, transmission, queueing, switching, routing, transport, DNS, wireless behavior, and operations. Distributed systems turn network delay and loss into partial failure and protocol uncertainty. Cloud and platform engineering consume network service contracts. Security determines allowed reachability, not only possible reachability. Systems engineering traces stakeholder outcomes to verification and validation evidence.

## Governing Question

Which endpoints must exchange which traffic, at what volume and time scale, with what delay and loss distribution, during which failures, and how will independent observers decide whether the network meets those needs?

This formulation begins with workload and outcome rather than a device model. It also makes disagreement productive: application owners can challenge the traffic assumptions, network engineers can challenge impossible thresholds, security can challenge reachability scope, and operators can challenge evidence that cannot be sustained in production.

## Why This Matters

Networks are shared systems whose behavior varies with direction, time, route, traffic class, packet size, competing load, radio conditions, failures, and endpoint behavior. A single number cannot represent them. Poor requirements lead to predictable disputes: a carrier shows an interface is up, an application shows requests time out, and both claim their evidence proves the other side wrong.

Precise metrics create a common language without pretending measurement is effortless. The IETF IP Performance Metrics framework emphasizes concrete, well-defined, repeatable methods and warns against metrics that induce artificial goals. Capacity work distinguishes nominal physical rate from IP-layer and available capacity. Current one-way delay and loss specifications bind results to packet type, endpoints, time, clocks, timeout, and sampling. These distinctions are operational tools, not academic decoration.

## Prerequisites and Retrieval

Retrieve units and prefixes, ratios, percentages, basic probability, quantiles, rates, time intervals, and the distinction between a sample and a population. Be able to convert bytes to bits and seconds to milliseconds. You need no prior protocol configuration experience. Keep a units ledger; most early capacity errors are dimensional errors disguised as networking opinions.

## Learning Objectives

By the end of this module, you should be able to:

1. derive a traffic matrix from application and operational behavior;
2. specify directional reachability for a traffic type, policy, interval, and failure condition;
3. distinguish nominal rate, capacity, available capacity, throughput, and goodput;
4. compute offered rate, utilization, headroom, serialization lower bounds, loss ratio, and quantiles;
5. distinguish one-way delay, round-trip time, and remote processing time;
6. state delay and delay-variation requirements with unambiguous populations and statistics;
7. design measurements that avoid tool, endpoint, clock, sampling, and workload confounders;
8. reason about overload, tails, bursts, asymmetric paths, failures, and recovery; and
9. identify when safety, regulation, privacy, or public-service consequences require named human review.

## Core Exposition

Begin with communication intent. For each flow, identify producer and consumer, direction, address or identity scope, protocol behavior, request/response dependency, payload distribution, session count, burst pattern, deadline, criticality, confidentiality, and failure tolerance. A database query, voice stream, backup, interactive shell, telemetry feed, and bulk model transfer can share a path yet require different evidence.

Reachability is typed and directional. A response to an ICMP echo request demonstrates one probe type between particular observation points at particular times. It does not prove DNS resolution, TCP establishment, UDP delivery, application authorization, return-path symmetry, maximum-size packet delivery, or continued connectivity. Conversely, an ICMP failure does not necessarily prove the required application traffic is unreachable. Firewalls, policy routing, overlays, translation, and service listeners make “can reach” incomplete without traffic type and success semantics.

Distinguish **possible reachability** from **permitted reachability**. A route and forwarding path may exist while policy intentionally blocks a flow. A secure design often requires both positive and negative requirements: authorized sources can reach the service; unauthorized segments cannot. Evidence includes successful allowed probes and failed denied probes at the enforcement layer, plus configuration and logging evidence. Absence of a successful probe alone cannot distinguish policy, routing, endpoint, or measurement failure.

Capacity must name a layer and interval. A nominal 1-Gbit/s link is a physical or link technology claim. Headers, framing, inter-packet gaps, retransmissions, encryption overhead, competing traffic, device processing, and endpoint limits reduce what an application observes. RFC 5136 defines capacity and available capacity relative to IP traffic and time. Application goodput counts useful payload accepted by the application per unit time; it excludes protocol overhead and often excludes duplicates or retransmitted bytes.

For a measurement interval $I$, a simple carried rate is

$$
G=\frac{8B_{\text{useful}}}{I}.
$$

If offered rate is $O$ and sustainable service capacity is $C$, utilization is $U=O/C$. Headroom is often expressed as $1-U$, but the calculation is meaningful only when $O$ and $C$ use consistent layers, populations, and time scales. A daily average can hide a five-minute saturation window. Bursty arrivals can build queues even when long-run utilization looks moderate.

Along a series path, the smallest relevant available capacity commonly constrains steady flow, but end-to-end throughput can be lower because of transport dynamics, loss, window limits, server/storage speed, packet processing, and traffic policing. Parallel links do not automatically sum for one flow: hashing, ordering, unequal members, failure, and flow granularity matter. Capacity planning therefore combines topology bounds with representative end-to-end measurement.

Delay must define start and stop events. One-way packet delay measures from a source event to a destination event and requires suitable clock synchronization or a method that accounts for error. Round-trip time measures a complete forward-and-return exchange plus any remote response time. Dividing RTT by two assumes symmetry and negligible or known processing; those assumptions often fail.

Later modules decompose delay into propagation, transmission, queueing, and processing. Here the requirements lesson is that different workloads care about different statistics. Interactive control may care about a high percentile and deadline miss rate. Bulk transfer may care mainly about completion time and sustainable goodput. Voice may care about one-way delay, delay variation, and loss bursts. Report sample count, sampling schedule, packet size/type, path condition, and clock uncertainty with the statistic.

An average is rarely a tail objective. Sort $n$ observed values and define the quantile convention. A nearest-rank p99 selects rank $\lceil0.99n\rceil$. With only 100 observations, it is the maximum; that sample gives weak information about rarer events. Long windows can blend incidents with normal periods. Use separate distributions by direction, traffic class, site, route, and operating condition when aggregation would conceal actionable behavior.

Packet delay variation is not one universal number. It may mean differences between successive packet delays, deviation from minimum delay, a percentile spread, or an application-specific playout measure. Name the metric and reference. Variation can force buffers or deadline misses even when average delay is acceptable. Reordering, duplication, and loss need separate accounting rather than being silently folded into “jitter.”

For sent count $N_s$ and qualifying received count $N_r$, a basic sample loss ratio is

$$
L=\frac{N_s-N_r}{N_s},\quad N_s>0.
$$

But matching packets, duplicates, corruption, reordering, fragmentation, late arrival, capture loss, and timeout determine the counts. Zero observed loss among 1,000 packets does not prove zero true loss. Loss patterns matter: ten consecutive losses can be more damaging than ten isolated losses. Retransmission can hide packet loss from an application while increasing delay and consuming capacity.

Availability adds time. “99.9% reachable” must name observation points, probe population, interval, allowed exclusions, minimum outage duration, and aggregation. Monthly availability can obscure repeated short outages. A service may be reachable but outside delay or loss objectives; define whether degraded performance counts unavailable. Maintenance exclusions must be bounded and governed, not used to erase bad results.

Failure requirements name the event: one access link, device, power domain, route, site, or provider. State whether existing sessions survive, when new traffic resumes, how much loss is allowed, and which capacity/delay bounds apply in degraded mode. Redundancy without failure-domain independence, sufficient remaining capacity, convergent control, and tested state transfer is only inventory.

Measurement itself changes and samples the system. Active probes consume capacity and may receive special treatment. Passive observations see production traffic but may lack controlled inputs or end-to-end correlation. Endpoint clocks drift; capture points drop packets; generators and receivers saturate; routes change mid-test. Preserve raw timestamps and counters, tool versions, configuration, topology, offered load, and anomalies. Repeat at representative and adversarial times.

The executable example below evaluates two declared flow samples. It uses nearest-rank p95 delay, received useful bytes, sent/received counts, and a required-goodput threshold. The values are synthetic and deterministic.

<!-- bijux-verify: {"id":"network-requirement-evaluator","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"replication goodput_mbps=520.00 p95_ms=34 loss_pct=0.040 status=pass\ntelemetry goodput_mbps=7.20 p95_ms=121 loss_pct=0.500 status=fail\nflows_passing=1/2\n","stderr":""}} -->
```python
from math import ceil


def nearest_rank(values, percentile):
    ordered = sorted(values)
    return ordered[ceil(percentile * len(ordered)) - 1]


flows = [
    {
        "name": "replication",
        "useful_bytes": 3_900_000_000,
        "seconds": 60,
        "sent": 50_000,
        "received": 49_980,
        "delays_ms": [24, 25, 25, 26, 27, 27, 28, 29, 31, 34],
        "min_goodput_mbps": 500,
        "max_p95_ms": 35,
        "max_loss_pct": 0.05,
    },
    {
        "name": "telemetry",
        "useful_bytes": 54_000_000,
        "seconds": 60,
        "sent": 20_000,
        "received": 19_900,
        "delays_ms": [35, 38, 40, 44, 48, 51, 55, 61, 88, 121],
        "min_goodput_mbps": 8,
        "max_p95_ms": 75,
        "max_loss_pct": 0.1,
    },
]

passing = 0
for flow in flows:
    goodput = 8 * flow["useful_bytes"] / flow["seconds"] / 1_000_000
    p95 = nearest_rank(flow["delays_ms"], 0.95)
    loss = 100 * (flow["sent"] - flow["received"]) / flow["sent"]
    ok = (
        goodput >= flow["min_goodput_mbps"]
        and p95 <= flow["max_p95_ms"]
        and loss <= flow["max_loss_pct"]
    )
    passing += ok
    print(
        f"{flow['name']} goodput_mbps={goodput:.2f} p95_ms={p95} "
        f"loss_pct={loss:.3f} status={'pass' if ok else 'fail'}"
    )

print(f"flows_passing={passing}/{len(flows)}")
```

Execution verifies arithmetic and threshold comparison for two synthetic samples. It does not generate traffic, discover routes, validate clocks, distinguish network from endpoint bottlenecks, estimate population quantiles, prove availability, authorize policy, or demonstrate behavior during a real failure.

## Definitions and Notation

Let $S$ and $D$ be source and destination observation points. **Type-P** denotes a fully described packet population, including relevant protocol fields, size, markings, and addressing. Let $[T,T+I]$ be the observation interval. Direction is always $S\rightarrow D$; the reverse is a separate path and metric.

Let $N_s$ be packets sent, $N_r$ qualifying packets received before timeout $T_{max}$, and $B_u$ useful application bytes delivered. Offered rate is $O$, capacity $C$, utilization $U=O/C$, available capacity $A$, and goodput $G=8B_u/I$. Units use bit/s or byte/s explicitly; `Mb` and `MB` are not interchangeable.

For received packet $i$, one-way delay is $d_i=t_{D,i}-t_{S,i}$ under a stated clock-error model. A sample quantile is $Q_p(d)$ under a named convention. Loss ratio is $L=(N_s-N_r)/N_s$ for $N_s>0$. Availability $A_v$ is qualifying time divided by eligible time under a declared interval and exclusion policy. These symbols describe observations, not causal attribution.

## Mechanisms, Invariants, or Proof Structure

Build requirements and evidence in this order:

1. **Define outcomes and endpoints.** Identify users, applications, sites, trust zones, and observation points.
2. **Construct the traffic matrix.** Record direction, type, size distribution, concurrency, rate, burst, duration, priority, and deadline.
3. **Define reachability policy.** List required allows and required denies, normal and failure conditions, and application-level success semantics.
4. **Define metric tuples.** Name layer, population, interval, units, statistic, threshold, timeout, clock needs, and exclusions.
5. **Check feasibility.** Compare simultaneous offered loads with topology and endpoint bounds, including overhead, headroom, and degraded capacity.
6. **Design independent evidence.** Combine active/passive measurement, configuration/topology inspection, endpoint resource data, and application outcomes.
7. **Test representative conditions.** Include normal peak, bursts, maintenance, route changes, component loss, overload, recovery, and negative policy cases.
8. **Preserve reproducibility.** Retain raw results, method, tools, clocks, topology, configuration, traffic, dates, and limitations.

The primary invariant is metric identity: values are comparable only when their defining tuples are compatible. A p99 delay for 64-byte probes on an idle path is not evidence for p99 delay of maximum-size encrypted packets under peak traffic. A link counter and an application payload counter answer different questions. Before calculating deltas or trends, establish the same units, layer, population, endpoints, direction, and interval.

Capacity feasibility is a necessary-bound argument. For simultaneous flows $j$ sharing a constrained resource, $\sum_j O_j$ plus overhead and reserve must fit the resource's sustainable capacity under the required failure condition. This does not prove the targets will be met because queueing, burst synchronization, per-flow hashing, endpoint limits, control traffic, transport behavior, and policy can dominate.

Loss and delay accounting must partition every sent identifier into received on time, received late, duplicated, corrupted/invalid, or unobserved, with rules preventing double counting. Capture loss and clock uncertainty are evidence-quality fields. Otherwise the measurement can report network loss that occurred in the observer or precise delay that the clocks cannot support.

## Alternatives and Trade-Offs

**One-way versus round-trip measurements.** One-way metrics expose direction and asymmetric paths but require clock discipline. Round-trip metrics need only one clock but combine two directions and remote behavior. Use the metric aligned with the requirement.

**Active versus passive observation.** Active probes control type and schedule and can test absent user traffic. They add traffic and may not resemble production. Passive measurement reflects real flows but inherits uncontrolled workloads and privacy constraints. Combining them often gives stronger diagnosis.

**Synthetic versus application transactions.** Synthetic packets isolate network behavior. Application transactions validate user-visible paths but include DNS, transport, TLS, server, storage, and client time. Maintain both rather than calling end-to-end response time “network latency.”

**Reserved capacity versus statistical sharing.** Reservation can protect critical flows but reduce utilization and still fail if enforcement or failure capacity is wrong. Statistical sharing improves efficiency but needs admission, prioritization, queue management, and overload behavior.

**Mean versus tail objectives.** Means are stable summaries for some planning. Tail quantiles and deadline-miss ratios expose rare harmful delay but need much larger samples and careful windows. Report both when each supports a decision.

**Per-path versus aggregate reporting.** Aggregates are compact but hide one bad site, direction, class, or hour. Per-path results are actionable but expensive and high-cardinality. Define aggregation only after preserving enough dimensions for diagnosis.

**Strict loss target versus recovery above the network.** Some applications tolerate loss using retransmission or coding; others cannot tolerate retransmission delay. Relaxing packet loss may be economical, but the complete application deadline and capacity costs must still pass.

## Failure Modes and Misconceptions

- **“Ping works, so the service is reachable.”** The probe may use a different protocol, policy, size, direction, or endpoint.
- **“The interface is 10 Gbit/s, so we have 10 Gbit/s.”** Nominal rate is not available path capacity or goodput.
- **“RTT/2 is one-way delay.”** Path and processing asymmetry invalidate the inference.
- **“Average latency is within target.”** Averages can hide tails and outages.
- **“Zero observed loss means lossless.”** Finite samples support an upper-confidence argument, not zero population loss.
- **“Jitter is 5 ms.”** Without a definition, packet population, statistic, and reference, the number is ambiguous.
- **“More bandwidth fixes latency.”** It may reduce queueing at a bottleneck, but not propagation, endpoint work, policy, loss recovery, or another bottleneck.
- **“Redundant links double capacity.”** One flow may use one member, and remaining capacity during failure may be half or less.
- **“A firewall deny proves no route exists.”** Policy and reachability are different layers of explanation.
- **“The tool says network.”** Load generators, clocks, capture systems, servers, and storage can be the bottleneck.
- **“Monthly availability represents experience.”** Aggregation can conceal correlated or repeated short outages.
- **“A benchmark is a production guarantee.”** It is evidence only for its topology, frame sizes, configuration, traffic, duration, and method.

## Worked Examples

### Example 1

**Question:** What does a successful ICMP echo from host A to server B establish?

**Reasoning:** At that time, matching echo request/reply traffic traversed the relevant forward and return paths and B or an intermediary responded. It does not establish TCP port 443 service, DNS, authorization, large-packet delivery, application health, or future availability.

**Conclusion:** Reachability evidence is traffic-type, endpoint, direction, and time specific.

### Example 2

**Question:** A transfer delivers 900 MB of useful data in 12 seconds. What is application goodput?

**Reasoning:** Using decimal units, $8\times900\text{ MB}/12\text{ s}=600\text{ Mbit/s}$. This excludes headers and retransmitted bytes and says nothing about unused path capacity.

**Conclusion:** Useful-byte goodput is 600 Mbit/s under the declared unit convention.

### Example 3

**Question:** Three simultaneous flows offer 300, 250, and 150 Mbit/s to a 1-Gbit/s constrained path. What simple headroom remains?

**Reasoning:** Aggregate offered load is 700 Mbit/s, utilization is 0.70, and arithmetic headroom is 30%. Protocol overhead, bursts, other traffic, failure capacity, and endpoint limits are omitted.

**Conclusion:** Thirty percent is a necessary planning estimate, not proof of acceptable tails.

### Example 4

**Question:** Delays are `10, 11, 12, 13, 14, 15, 16, 18, 25, 80` ms. What is nearest-rank p95?

**Reasoning:** For ten values, rank is $\lceil0.95\times10\rceil=10$; p95 is 80 ms. The small sample makes this effectively the maximum and provides weak tail resolution.

**Conclusion:** Quantile convention and sample size are part of the result.

### Example 5

**Question:** A sender transmits 200,000 identified packets and 199,900 arrive before the timeout. What is observed loss?

**Reasoning:** Missing count is 100. Ratio is $100/200000=0.0005$, or 0.05%. Validate capture completeness, duplicates, late packets, and identifier matching before attributing the loss to the path.

**Conclusion:** The observed sample loss is 0.05% under the declared accounting rule.

### Example 6

**Question:** A video path averages 20 ms but freezes periodically. Is the mean enough?

**Reasoning:** No. Inspect delay distribution, variation definition, consecutive-loss bursts, reordering, bitrate bursts, buffer behavior, direction, and time correlation. A few multi-second stalls barely affect a long-run mean yet dominate user experience.

**Conclusion:** Requirements need tail and burst behavior aligned with application buffering.

### Example 7

**Question:** A dual-link site passes steady-state tests. What is missing?

**Reasoning:** Remove each link and relevant device/power domain; observe loss, convergence, session survival, route correctness, remaining capacity, delay, and recovery. Test restoration too, because route churn or asymmetric policy can occur when the link returns.

**Conclusion:** Redundancy becomes resilience only with failure-domain and degraded-mode evidence.

### Example 8

**Question:** A remote user reports 200-ms application response time while a probe reports 15-ms RTT. Are the measurements inconsistent?

**Reasoning:** Not necessarily. Application time includes name resolution, connection setup, encryption, server queueing, computation, storage, payload transfer, client work, and perhaps multiple round trips. The probe uses a different traffic type and size.

**Conclusion:** Decompose end-to-end time before assigning a network cause.

### Example 9

**Question:** A tele-stroke consultation requires interactive video and image transfer between rural clinics and specialists. Can this chapter certify a network design?

**Reasoning:** No. Clinical deadlines, image fidelity, call control, identity, privacy, failure escalation, degraded modes, human communication, regional access, device behavior, and patient risk require named neurology/clinical, emergency-care, biomedical, network, application, cybersecurity, privacy/legal, safety, human-factors/accessibility, operations, telecom-provider, regulator, and independent assurance review. No external review is claimed.

**Conclusion:** Metrics contribute evidence but do not authorize high-stakes service.

### Example 10

**Question:** A path meets p99 delay and loss during an idle midnight test. Is the requirement satisfied?

**Reasoning:** Only if midnight idle traffic is the specified population. Otherwise measure representative peak mix, bursts, packet sizes, routing, failure states, maintenance, and endpoint load. Preserve the idle result as a baseline, not as production acceptance.

**Conclusion:** A result inherits the workload and conditions of its method.

## Cross-Program Connections

[Operating Systems](../../22-operating-systems/ROADMAP.md) owns kernel network-stack mechanisms and endpoint scheduling that can confound measurements. [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) turns movement, shuffle, replication, and locality into traffic demands. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) reasons about partial failure when messages are delayed or lost.

[Security Engineering](../../25-security-engineering/ROADMAP.md) defines trust and policy, making required denies as important as allows. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns application interaction semantics and deadlines. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) and [Cloud Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) consume connectivity and performance as platform capabilities while adding overlays, service boundaries, provider quotas, and shared responsibility.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) traces stakeholder outcomes, hazards, interfaces, verification, validation, and lifecycle conditions. Network evidence must remain connected to those system claims rather than optimizing isolated metrics that users do not need.

## References

- Vern Paxson et al., [*RFC 2330 — Framework for IP Performance Metrics*](https://www.rfc-editor.org/info/rfc2330), IETF, 1998. Foundational metric criteria, path terminology, sampling, measurement, and interpretation discipline.
- Jamshid Mahdavi and Vern Paxson, [*RFC 2678 — IPPM Metrics for Measuring Connectivity*](https://www.rfc-editor.org/info/rfc2678), IETF Proposed Standard, 1999. Directional and temporal connectivity definitions and measurement considerations.
- Paul Chimento and Joseph Ishac, [*RFC 5136 — Defining Network Capacity*](https://www.rfc-editor.org/info/rfc5136), IETF Informational, 2008. Distinctions among nominal physical, IP-layer, used, available-link, and available-path capacity.
- Guy Almes et al., [*RFC 7679 — A One-Way Delay Metric for IPPM*](https://www.rfc-editor.org/info/rfc7679), IETF Standards Track, 2016. Current one-way delay singleton, sample, timeout, clock, and reporting semantics; obsoletes RFC 2679.
- Guy Almes et al., [*RFC 7680 — A One-Way Loss Metric for IPPM*](https://www.rfc-editor.org/info/rfc7680), IETF Standards Track, 2016. Current one-way packet-loss metric and methodology; obsoletes RFC 2680.
- Benoit Claise, [*RFC 6390 — Guidelines for Considering New Performance Metric Development*](https://www.rfc-editor.org/info/rfc6390), IETF Best Current Practice, 2011. Metric definition, measurement method, units, context, and composition guidance.
- Al Morton, [*RFC 6703 — Reporting IP Network Performance Metrics: Different Points of View*](https://www.rfc-editor.org/info/rfc6703), IETF Informational, 2012. Measurement design and reporting for user and provider viewpoints.
- Scott Bradner and Jim McQuaid, [*RFC 2544 — Benchmarking Methodology for Network Interconnect Devices*](https://www.rfc-editor.org/info/rfc2544), IETF Informational, 1999. Controlled device throughput, latency, frame-loss, burst, recovery, and reset methods; not a production-service guarantee.
- Al Morton and Rüdiger Geib, [*RFC 9097 — Metrics and Methods for One-Way IP Capacity*](https://www.rfc-editor.org/info/rfc9097), IETF Standards Track, 2021. Modern one-way IP capacity metric and method framework.

## Exercises

### Exercise 1

Rewrite “branches need a reliable 500-Mbit/s link to headquarters” as a metric tuple with endpoints, directions, traffic, workload, goodput, delay, loss, availability, failure condition, and evidence. State three questions that must be answered by stakeholders.

### Exercise 2

A backup sends 1.8 TB of useful data in eight hours. Compute decimal application goodput. If its path requirement is 650 Mbit/s goodput, compute the shortfall and name at least five possible non-network or non-capacity explanations.

### Exercise 3

For delays `12, 12, 13, 13, 14, 15, 15, 16, 18, 19, 22, 45` ms, compute the nearest-rank p50, p90, and p99. Explain why the sample cannot support a strong population p99 claim.

### Exercise 4

Design a measurement plan to distinguish route/policy failure, packet loss, endpoint saturation, and application delay for intermittent checkout timeouts across three regions. Include negative reachability tests and evidence preservation.

### Exercise 5

A national emergency-call platform will move signaling, audio, text, and caller-location flows onto a shared IP network. Define the required traffic matrix, normal and degraded metrics, fault and recovery tests, security/privacy evidence, and named human-review roles. State what automated probes cannot establish.

## Answers to the Exercises

### Answer 1

One defensible form is: from each named branch edge to named headquarters services and the reverse, for approved encrypted application traffic with production packet-size/session distributions, sustain at peak-hour p95 five-minute intervals at least 500 Mbit/s useful goodput; keep one-way delay p99 below an agreed bound and one-way loss below an agreed ratio; meet the bounds for an agreed percentage of eligible monthly intervals; and after any single access-link or edge-device failure, restore reachability within a stated time and meet a stated degraded goodput. Evidence includes synchronized endpoint measurements, raw packet/counter data, topology/configuration, endpoint-resource observations, allowed and denied probes, failure exercises, and application outcomes. Stakeholders must define simultaneous branch demand, actual application deadline/tolerance, failure scope, maintenance exclusions, security policy, and whether 500 Mbit/s is per branch or aggregate; any three are essential.

### Answer 2

Using decimal units, $1.8\text{ TB}=1.8\times10^{12}$ bytes and eight hours is 28,800 seconds. Goodput is $8\times1.8\times10^{12}/28800=500,000,000$ bit/s, or 500 Mbit/s. Shortfall is 150 Mbit/s, about 23.1% below the 650-Mbit/s target. Possible explanations include source disk read rate, destination write/commit rate, backup software serialization, compression or encryption CPU, small I/O, transport window/implementation, endpoint packet processing, application throttling, competing traffic, retransmissions, path policing, measurement-unit error, or counting only a subset of time. Attribute only after correlated evidence.

### Answer 3

With 12 sorted values, nearest-rank p50 uses rank $\lceil6\rceil=6$, giving 15 ms. p90 uses rank $\lceil10.8\rceil=11$, giving 22 ms. p99 uses rank $\lceil11.88\rceil=12$, giving 45 ms. Twelve observations make p99 simply the maximum and provide almost no resolution of a one-percent tail. The schedule, workload, path conditions, clock error, and independence are also unknown. Report the sample statistics without extrapolating a strong population objective.

### Answer 4

Define the checkout dependency graph and instrument client, regional edge, application, and dependency timestamps with correlation identifiers. From each region, run approved positive probes for DNS, transport, TLS, and application transactions plus negative probes from unauthorized sources. Preserve route and policy snapshots, flow and firewall logs, packet captures where lawful, loss/delay active metrics, endpoint CPU/queue/socket counters, server and database timings, deployment/configuration events, clock health, and tool versions. During an incident, determine whether packets lack a route or are denied, are sent but not received, arrive late or retransmit, reach a saturated endpoint, or complete network exchange before application delay. Repeat under representative load and controlled route/failure changes. Avoid one tool's diagnosis as the oracle; reconcile independent observation points.

### Answer 5

Inventory every signaling, bidirectional audio, real-time text, caller-location, recording, dispatch, monitoring, time, identity, and management flow by source/destination class, direction, protocol, packet/payload distribution, concurrency, burst, precedence, privacy class, and deadline. Define reachability allows and denies; one-way delay, delay variation, loss burst, reorder, setup time, goodput/capacity, availability, and time-synchronization metrics for normal peak and major-incident demand. Define degraded targets and recovery for access, device, power, route, site, provider, identity, timing, and control-plane failures; test overload, reroute, restoration, backlog and operator fallback. Evidence must cover encryption, authentication, segmentation, least privilege, logging, location/privacy handling, retention, lawful access, abuse resistance, configuration control, supply chain, and incident response. Named reviewers include emergency-call and dispatch authorities, telecom/network and voice engineers, public-safety agencies, accessibility and real-time-text experts, location specialists, human factors, safety/reliability, cybersecurity, privacy/legal and records authorities, operations/incident management, field and carrier operators, quality/configuration management, regulator, emergency-service representatives, and independent assurance. Automated probes cannot validate caller understanding, dispatch outcome, legal authority, accessibility in real use, safety of degraded procedures, organizational readiness, or public-service acceptance; no external review is claimed here.
