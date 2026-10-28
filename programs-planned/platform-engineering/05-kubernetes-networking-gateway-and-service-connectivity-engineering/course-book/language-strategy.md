# Language and tool strategy

Platform networking is expressed through several native forms. The course uses each where it is strongest.

## Python

Python is the primary executable explanation. The `atlas_net` package models ownership and invariants without hiding them behind a vendor SDK. It also drives the loopback DNS, Service, TLS Gateway, release, and failure laboratories.

The Python model is not a CNI plugin, kube-proxy replacement, DNS server for production, or Gateway controller. Its purpose is to make decisions deterministic and testable before the native environment adds implementation complexity.

## Go

Go is used for a compact CNI lifecycle implementation because CNI and Kubernetes networking ecosystems are commonly implemented in Go. The course does not require a second full implementation of every mechanism. Learners read and test the Go lifecycle model to compare state ownership and error handling with Python.

## YAML

Kubernetes, Gateway API, and Cilium configuration are written in YAML. YAML is declarative input to APIs, not proof of accepted or programmed behavior. Every important resource is paired with the status, dataplane, or negative evidence needed to evaluate it.

## Shell and native tools

Shell scripts coordinate guarded environment work. Native evidence can involve:

```text
kubectl
ip
ss
tcpdump
dig
openssl
curl
kind
cilium
```

Commands appear after the ownership model. Memorizing command sequences is not the learning objective.

## Implementation policy

The concept order is:

```text
contract
→ owner
→ mechanism
→ failure model
→ evidence
→ implementation
```

Cilium is the pinned local-cluster reference lane because it can exercise CNI, Service handling, NetworkPolicy, Gateway API, and observability in one bounded environment. It is not presented as the only valid architecture. Gateway API is the primary edge contract; legacy Ingress is comparative, not the final abstraction. A service mesh is introduced only when a named requirement justifies it.
