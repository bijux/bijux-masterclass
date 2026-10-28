# Start here

The quickest way to waste this course is to treat it as a Docker tutorial. Docker, Podman, BuildKit, containerd, CRI-O, runc, crun, ORAS, Cosign, Syft, and registries are important implementations. None is the conceptual spine.

The spine is a sequence of objects and authority decisions:

```text
source and materials
        ↓ build graph
filesystem changes + execution defaults
        ↓ OCI image manifest/index
content-addressed registry objects
        ↓ runtime preparation
rootfs + config.json bundle
        ↓ Linux execution
isolated and resource-bounded process tree
        ↓ supply-chain evidence
inventory + provenance + signature + policy
        ↓ release decision
exact digest authorized for Course 4
```

When this sequence is clear, product commands become interpretable. When it is not, a green build, scanner, signature, or runtime command can support the wrong conclusion.

## Prerequisite contract

Course 3 does not redesign Atlas. It consumes the exact Course 2 handoff:

```bash
make predecessor-proof
```

Read `capstone/predecessor/`. It fixes process roles, non-root identity, port 8080, durable and ephemeral paths, runtime configuration/secret boundaries, shutdown behavior, workload identity, and resource hypotheses. Packaging may express those requirements. It may not weaken them to make an image easier to build.

Examples of forbidden “fixes”:

- run as UID 0 because a volume is owned incorrectly;
- copy a cloud key into an image because workload identity is inconvenient;
- write durable state to the container writable layer;
- redefine readiness as “the process exists”;
- use a mutable tag because a deployment system cannot consume digests;
- remove an arm64 child rather than repair its build evidence.

## What you need

The mandatory dependency-light lane uses:

- Python 3.11 or newer;
- Go with linux/amd64 and linux/arm64 cross-compilation;
- OpenSSL;
- modern Linux for the full namespace/rootfs observation;
- standard shell/filesystem utilities.

Optional independent lanes use BuildKit or Docker/Podman, runc/crun, ORAS/Skopeo, Cosign/Sigstore, Syft/Grype, and a production-like registry. The course remains conceptually complete without them. Their absence is reported as `not-executed`; no fixture pretends to be a production service.

Run:

```bash
make doctor
make predecessor-proof
make test
make capstone-tour
```

The tour is a map, not the course. Read the report and identify at least one check for image structure, platform truth, registry distribution, runtime observation, inventory/risk, provenance/signature, and release policy. Then list the stronger claims it does **not** prove.

## Five distinctions you must keep

### Image and container

An image is immutable distribution content and execution defaults. A container is a runtime-created process environment. A secure image can be launched with dangerous authority; a runtime profile cannot erase a secret preserved in an image layer.

### Tag and digest

A tag is mutable repository state used for discovery. A digest identifies exact bytes. Review and deployment decisions authorize digests.

### Integrity and trust

A digest proves retrieved bytes match the descriptor. It does not prove those bytes were built from reviewed source, by an authorized builder, or are allowed in production.

### Inventory and affectability

An SBOM inventories declared components. Vulnerability matching, reachability, VEX, license policy, and release authorization are later decisions with different owners and evidence.

### Signature and release

A signature authenticates bytes or a statement under an identity. A release decision evaluates whether the subject, signer, builder, source, materials, runtime profile, inventory, and target environment are authorized together.

## How to study one module

1. Read the chapter without executing anything.
2. Draw the object and authority graph from memory.
3. Inspect the linked capstone implementation and data.
4. Answer all twelve exercises before opening the worked solutions.
5. Run the lab with one controlled fault at a time.
6. Preserve exact evidence and clean the environment.
7. Defend the checkpoint aloud or in writing.

A complete answer identifies the subject, mechanism, failure excluded, oracle, evidence boundary, decision, and residual risk. “Use Docker best practices” is not an engineering answer.

## Primary route and comparison route

The dependency-light Python implementation and real Go workloads are the primary learning lane because they expose bytes and state directly. Native tools are comparison evidence. Do not rewrite every mechanism twice; use the independent lane to challenge assumptions and find where two implementations differ.

## Begin

Complete [Orientation](module-00-orientation/index.md), then proceed to [Module 1](module-01-containers-as-linux-process-isolation/index.md). Keep the [incident casebook](casebook/index.md) nearby when a mechanism feels abstract, and use the [reference atlas](reference/index.md) during labs and reviews.
