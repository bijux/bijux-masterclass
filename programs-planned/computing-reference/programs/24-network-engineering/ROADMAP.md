# 24. Network Engineering

**Program code:** `NET`

**Purpose:** Develop protocol-level and operational command of how packets move through local, wide-area, wireless, datacenter, and cloud networks, including routing, transport, security, automation, and failure diagnosis.

**Level-II professional outcome:** Ready to design, configure, automate, troubleshoot, secure, and performance-engineer production networks and networked systems.

**Prerequisites:** systems fundamentals; basic probability; command-line and scripting skills.

**Primary ownership:** layered networking; Ethernet and switching; IP addressing and routing; transport protocols; DNS and application protocols; routing protocols; datacenter and cloud networking; wireless networking; SDN and automation; network operations and performance.

**Explicit exclusions:** kernel network-stack implementation (Program 22); application API semantics (Program 28); cloud provider service design (Program 30); general security engineering (Program 25).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Signals, Links, and Layered Communication

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Network Requirements: Reachability, Capacity, Delay, and Loss** | `001-network-requirements-reachability-capacity-delay-and-loss.md` |
| 002 | **Layering, Encapsulation, and Protocol Data Units** | `002-layering-encapsulation-and-protocol-data-units.md` |
| 003 | **Bits, Symbols, Bandwidth, and Encoding** | `003-bits-symbols-bandwidth-and-encoding.md` |
| 004 | **Propagation, Transmission, Queueing, and Processing Delay** | `004-propagation-transmission-queueing-and-processing-delay.md` |
| 005 | **Error Detection and Correction** | `005-error-detection-and-correction.md` |
| 006 | **Framing** | `006-framing.md` |
| 007 | **Multiplexing** | `007-multiplexing.md` |
| 008 | **Shared Media and Medium Access** | `008-shared-media-and-medium-access.md` |
| 009 | **Packet Switching and Circuit Switching** | `009-packet-switching-and-circuit-switching.md` |
| 010 | **Following a Packet Across the Protocol Stack** | `010-following-a-packet-across-the-protocol-stack.md` |

### Block 02 — Ethernet and Local Networks

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Ethernet Frames and MAC Addresses** | `011-ethernet-frames-and-mac-addresses.md` |
| 012 | **Switch Learning and Forwarding** | `012-switch-learning-and-forwarding.md` |
| 013 | **Broadcast and Collision Domains** | `013-broadcast-and-collision-domains.md` |
| 014 | **Virtual LANs and Trunking** | `014-virtual-lans-and-trunking.md` |
| 015 | **Spanning Tree Protocol** | `015-spanning-tree-protocol.md` |
| 016 | **Link Aggregation** | `016-link-aggregation.md` |
| 017 | **ARP and Neighbor Discovery** | `017-arp-and-neighbor-discovery.md` |
| 018 | **Power over Ethernet** | `018-power-over-ethernet.md` |
| 019 | **Local Network Redundancy** | `019-local-network-redundancy.md` |
| 020 | **Diagnosing Loops, Flooding, and Layer-Two Failure** | `020-diagnosing-loops-flooding-and-layer-two-failure.md` |

### Block 03 — Internet Protocol and Routing Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **IPv4 Addressing** | `021-ipv4-addressing.md` |
| 022 | **CIDR and Subnetting** | `022-cidr-and-subnetting.md` |
| 023 | **IPv6 Addressing** | `023-ipv6-addressing.md` |
| 024 | **IP Packet Forwarding** | `024-ip-packet-forwarding.md` |
| 025 | **Routing Tables and Longest-Prefix Match** | `025-routing-tables-and-longest-prefix-match.md` |
| 026 | **ICMP** | `026-icmp.md` |
| 027 | **Fragmentation and Path MTU** | `027-fragmentation-and-path-mtu.md` |
| 028 | **Network Address Translation** | `028-network-address-translation.md` |
| 029 | **Static and Default Routes** | `029-static-and-default-routes.md` |
| 030 | **Tracing a Routed Packet Across Multiple Networks** | `030-tracing-a-routed-packet-across-multiple-networks.md` |

### Block 04 — Transport Protocols

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Ports, Sockets, and Demultiplexing** | `031-ports-sockets-and-demultiplexing.md` |
| 032 | **UDP** | `032-udp.md` |
| 033 | **TCP Connection Establishment and Teardown** | `033-tcp-connection-establishment-and-teardown.md` |
| 034 | **Reliable Delivery and Sequence Numbers** | `034-reliable-delivery-and-sequence-numbers.md` |
| 035 | **Flow Control** | `035-flow-control.md` |
| 036 | **Retransmission and Timers** | `036-retransmission-and-timers.md` |
| 037 | **Congestion Control** | `037-congestion-control.md` |
| 038 | **TCP State and Failure** | `038-tcp-state-and-failure.md` |
| 039 | **QUIC Transport Foundations** | `039-quic-transport-foundations.md` |
| 040 | **Diagnosing Throughput and Connection Problems from Packet Traces** | `040-diagnosing-throughput-and-connection-problems-from-packet-traces.md` |

### Block 05 — Core Network Services and Application Protocols

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Domain Name System** | `041-domain-name-system.md` |
| 042 | **Dynamic Host Configuration** | `042-dynamic-host-configuration.md` |
| 043 | **Network Time** | `043-network-time.md` |
| 044 | **HTTP over Network Transports** | `044-http-over-network-transports.md` |
| 045 | **TLS Handshake and Certificate Transport** | `045-tls-handshake-and-certificate-transport.md` |
| 046 | **Email Transport Foundations** | `046-email-transport-foundations.md` |
| 047 | **SSH and Remote Administration** | `047-ssh-and-remote-administration.md` |
| 048 | **Proxies and Load Balancers** | `048-proxies-and-load-balancers.md` |
| 049 | **Content Delivery Networks** | `049-content-delivery-networks.md` |
| 050 | **Mapping Application Latency to Network Interactions** | `050-mapping-application-latency-to-network-interactions.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Routing Protocols and Internet Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Distance-Vector Routing** | `051-distance-vector-routing.md` |
| 052 | **Link-State Routing** | `052-link-state-routing.md` |
| 053 | **OSPF Areas and Convergence** | `053-ospf-areas-and-convergence.md` |
| 054 | **IS-IS Concepts** | `054-is-is-concepts.md` |
| 055 | **Border Gateway Protocol** | `055-border-gateway-protocol.md` |
| 056 | **Path Selection and Policy** | `056-path-selection-and-policy.md` |
| 057 | **Route Aggregation, Summarization, and Route Reflectors** | `057-route-aggregation-summarization-and-route-reflectors.md` |
| 058 | **MPLS, Label Switching, and Traffic Engineering** | `058-mpls-label-switching-and-traffic-engineering.md` |
| 059 | **Anycast and Fast Reroute** | `059-anycast-and-fast-reroute.md` |
| 060 | **Diagnosing Routing Leaks, Loops, and Slow Convergence** | `060-diagnosing-routing-leaks-loops-and-slow-convergence.md` |

### Block 07 — Datacenter and Cloud Networking

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Leaf-Spine Fabrics** | `061-leaf-spine-fabrics.md` |
| 062 | **Equal-Cost Multipath Routing** | `062-equal-cost-multipath-routing.md` |
| 063 | **Overlay and Underlay Networks** | `063-overlay-and-underlay-networks.md` |
| 064 | **VXLAN and Network Virtualization** | `064-vxlan-and-network-virtualization.md` |
| 065 | **EVPN Control Planes** | `065-evpn-control-planes.md` |
| 066 | **Virtual Routing and Forwarding** | `066-virtual-routing-and-forwarding.md` |
| 067 | **Cloud Virtual Networks** | `067-cloud-virtual-networks.md` |
| 068 | **Service Load Balancing** | `068-service-load-balancing.md` |
| 069 | **Container and Kubernetes Networking** | `069-container-and-kubernetes-networking.md` |
| 070 | **Designing a Failure-Tolerant Datacenter Network** | `070-designing-a-failure-tolerant-datacenter-network.md` |

### Block 08 — Wireless, Mobile, and Edge Networks

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Radio Propagation and Link Budgets** | `071-radio-propagation-and-link-budgets.md` |
| 072 | **Wi-Fi Medium Access** | `072-wi-fi-medium-access.md` |
| 073 | **Wi-Fi Association, Roaming, and Security** | `073-wi-fi-association-roaming-and-security.md` |
| 074 | **Cellular Network Architecture** | `074-cellular-network-architecture.md` |
| 075 | **Mobility and Handover** | `075-mobility-and-handover.md` |
| 076 | **Low-Power and IoT Networking** | `076-low-power-and-iot-networking.md` |
| 077 | **Mesh Networks** | `077-mesh-networks.md` |
| 078 | **Satellite Networking** | `078-satellite-networking.md` |
| 079 | **Edge Connectivity** | `079-edge-connectivity.md` |
| 080 | **Troubleshooting a Congested and Interference-Limited Wireless Network** | `080-troubleshooting-a-congested-and-interference-limited-wireless-network.md` |

### Block 09 — Software-Defined, Programmable, and Automated Networks

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Control Plane and Data Plane Separation** | `081-control-plane-and-data-plane-separation.md` |
| 082 | **Software-Defined Networking** | `082-software-defined-networking.md` |
| 083 | **OpenFlow Concepts** | `083-openflow-concepts.md` |
| 084 | **Programmable Packet Processing** | `084-programmable-packet-processing.md` |
| 085 | **Network Function Virtualization** | `085-network-function-virtualization.md` |
| 086 | **Intent-Based Networking** | `086-intent-based-networking.md` |
| 087 | **Network Configuration Models** | `087-network-configuration-models.md` |
| 088 | **Network Automation and Idempotency** | `088-network-automation-and-idempotency.md` |
| 089 | **Validation and Digital-Twin Testing** | `089-validation-and-digital-twin-testing.md` |
| 090 | **Building a Safe Automated Network-Change Workflow** | `090-building-a-safe-automated-network-change-workflow.md` |

### Block 10 — Network Security, Reliability, and Performance

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Network Threat Models** | `091-network-threat-models.md` |
| 092 | **Firewalls and Stateful Filtering** | `092-firewalls-and-stateful-filtering.md` |
| 093 | **Virtual Private Networks** | `093-virtual-private-networks.md` |
| 094 | **Routing Security and RPKI** | `094-routing-security-and-rpki.md` |
| 095 | **DDoS Defense** | `095-ddos-defense.md` |
| 096 | **Network Telemetry and Flow Records** | `096-network-telemetry-and-flow-records.md` |
| 097 | **Packet Capture and Protocol Analysis** | `097-packet-capture-and-protocol-analysis.md` |
| 098 | **Latency, Jitter, Loss, and Capacity Measurement** | `098-latency-jitter-loss-and-capacity-measurement.md` |
| 099 | **Quality of Service, Queuing, and Traffic Shaping** | `099-quality-of-service-queuing-and-traffic-shaping.md` |
| 100 | **Conducting a Redundancy, Performance, and Operations Review** | `100-conducting-a-redundancy-performance-and-operations-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
