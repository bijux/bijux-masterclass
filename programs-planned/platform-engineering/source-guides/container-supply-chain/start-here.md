# Start here — Platform Engineering

Platform engineering is the design and operation of **trusted capabilities** that let other teams deliver and run software without rediscovering every systems problem. This program does not begin with Kubernetes. It first establishes the layers that Kubernetes, cloud services, and internal developer platforms later hide.

The learner follows one Atlas workload through ten courses. Each course accepts a versioned handoff, changes one major responsibility, and exports evidence for the next course. A later abstraction may automate an earlier mechanism; it may not erase the mechanism's failure modes.

## The first three courses

### Course 1 — operate the substrate

**Linux, Networking, and Cloud Systems Engineering** establishes the machine-level contract: processes, identities, files, signals, CPU and memory controls, durable file transitions, sockets, DNS, TLS, proxies, virtual machines, workload identity, storage classes, and failure domains.

The result is **Atlas Host Runtime 1.0**. It says what the workload needs from a host and which evidence distinguishes a working process from a merely running process.

### Course 2 — codify the cloud foundation

**Infrastructure as Code and Cloud Foundation Engineering** maps those host requirements into governed cloud state. It separates configuration intent, recorded infrastructure state, and provider-observed reality. The learner designs account boundaries, remote state, networks, identity, compute, encryption, data protection, edge routing, migrations, and recovery.

The result is **Atlas Cloud Foundation 1.0**. It can provide a host environment, but the workload package is still machine-oriented.

### Course 3 — make the workload a verifiable release

**Container, OCI, and Software Supply Chain Engineering** changes the release boundary. Atlas becomes exact OCI object graphs selected by immutable digest rather than a mutable host directory or tag. The course then binds runtime requirements, inventory, vulnerability decisions, provenance, signatures, and promotion policy to those subjects.

The result is **Atlas Workload Release 1.0**:

```text
source identity
      ↓ controlled build
multi-platform OCI image indexes
      ↓ immutable distribution
runtime profile + SBOM + provenance + signature
      ↓ verification policy
Course 4 workload handoff
```

Three identities remain separate throughout:

```text
source identity     commit or source digest
artifact identity   OCI manifest or index digest
runtime identity    workload principal and effective process credentials
```

A signature over an image digest does not authenticate the running workload. A runtime UID does not identify the source revision. A tag does not become immutable because a release document mentions it.

## How to study the program

For every mechanism, answer six questions:

1. **What object is being changed?** A process, state snapshot, image graph, registry reference, runtime configuration, or policy decision?
2. **Who owns the desired state?** Which identity may create, mutate, approve, or revoke it?
3. **Which identity is stable?** A pathname, tag, digest, key identity, workload identity, or database key?
4. **What failure can leave a dangerous half-state?** Partial apply, partial upload, stale tag, orphaned blob, leaked secret, or unclean runtime teardown?
5. **What is the strongest evidence available?** Static structure, semantic test, local mechanism proof, native-tool proof, cloud proof, or operated production evidence?
6. **What remains unproved?** Every strong claim needs a boundary.

## Evidence ladder

The program distinguishes evidence classes rather than treating all green checks as equivalent:

- **Dependency-light evidence:** deterministic models, parsers, fixtures, policy tests, and local process experiments.
- **Native-tool evidence:** the relevant implementation—OpenTofu, BuildKit, an OCI runtime, registry tools, or later Kubernetes tooling—executes the mechanism.
- **Environment-backed evidence:** a VM, cloud account, registry, cluster, or target architecture exercises the integration.
- **Operated evidence:** retention, recovery, rotation, capacity, support, and incident behavior are demonstrated over time.

A dependency-light OCI graph test can prove descriptor integrity rules. It cannot certify an OCI runtime or production registry. The course books name that difference explicitly.

## Current reading path

Begin Course 3 at:

```text
03-container-oci-and-software-supply-chain-engineering/
course-book/start-here.md
```

Read the numbered modules in order. Complete each exercise set before opening its worked answers. Treat the laboratory as an investigation: establish a baseline, state a hypothesis, introduce one controlled fault, observe the oracle, preserve the evidence, and clean the environment. Do not advance past a checkpoint by substituting reading completion for demonstrated behavior.
