# Course contents

## Reader-facing product

The finalized course contains:

- 107 navigated course-book pages;
- approximately 56,000 course-book words;
- one substantial orientation module;
- ten complete teaching modules;
- 120 numbered exercises;
- 120 matching worked solutions, each with mechanism and evidence reasoning;
- ten controlled failure laboratories;
- ten non-compensable checkpoints;
- eight practical guides;
- six integrated incident cases;
- twenty-three reference and capstone-manual chapters;
- final assessment and instructor material.

Every numbered module contains exactly:

```text
index.md
exercises.md
exercise-answers.md
lab.md
checkpoint.md
```

The main chapters are self-contained. The learner does not need to search implementation directories to reconstruct the concepts.

## Ten-module progression

1. **Kubernetes network model, address domains, and packet paths**
2. **CNI lifecycle, IPAM, routes, and Node integration**
3. **Services, EndpointSlices, and Service data planes**
4. **DNS and Service discovery**
5. **NetworkPolicy and L3/L4 segmentation**
6. **Traffic locality, source identity, and dual stack**
7. **Gateway API architecture and Route ownership**
8. **TLS, HTTP semantics, and backend protocol integrity**
9. **Egress, external services, and service-mesh boundaries**
10. **Network operations, conformance, and release**

## Executable capstone

```text
capstone/
├── predecessor/handoff/
├── architecture/
├── atlas_net/
├── cni-go/
├── netprobe-go/
├── manifests/
│   ├── base/
│   ├── frontier/
│   ├── labs/
│   └── observability/
├── kind/
├── cilium/
├── pki/
├── shared/vectors/
├── releases/
├── planted-defects/
├── runbooks/
├── tests/
├── scripts/
├── reports/
└── handoff/
```

The dependency-light implementation includes Python semantic models, two Go modules, a real loopback DNS/Service/TLS network laboratory, exact PKI fixtures, release classification, and handoff verification.

## Native and environment-backed lanes

The optional native lane is designed for:

- kind;
- Kubernetes 1.36;
- Cilium 1.20;
- Gateway API 1.6;
- CoreDNS observation;
- native NetworkPolicy enforcement;
- packet capture and flow evidence.

Cloud load balancers, managed DNS, cloud NAT, private endpoints, and multi-zone behavior require a real environment and are never inferred from local proof.
