# Capstone architecture and ownership

```text
Go source + locked course inputs
             |
             v
    controlled cross-compile
             |
             v
 deterministic filesystem layer
             |
             v
 platform manifest + image config
             |
             v
       multi-platform index -----------------------+
             |                                     |
             v                                     v
 loopback Distribution subset             SBOM / provenance
             |                                     |
             +------------ subject/referrers ------+
                             |
                             v
                     verification policy
                             |
                   +---------+----------+
                   |                    |
                   v                    v
             accepted release     rejected/review cases
                   |
                   v
          bounded runtime observation
                   |
                   v
             Course 4 handoff
```

## State owners

### Source and workload owner

`workload/` owns the actual Atlas API, worker, and probe behavior. It does not own cloud identity, environment secrets, durable storage implementation, or scheduling. Those remain external contracts inherited from Course 2 and passed to Course 4.

### Semantic builder

`atlas_container.image`, `archive`, and `layout` own deterministic object construction in the dependency-light lane. They normalize file metadata, produce layer/config/manifest/index bytes, and retain content-addressed blobs. This owner can create objects; it cannot authorize them for an environment.

### Registry

`atlas_container.registry` owns blob/manifest storage, repository references, and referrer discovery for the loopback exercise. Tags are mutable registry state. The registry does not decide whether a subject is trusted or deployable.

### Runtime

`mini_runtime` owns the temporary bundle/process lifecycle used by the probe proof. It is responsible for mapping identity, setting namespace/rootfs behavior, starting PID 1, collecting output, and cleaning resources. It does not build images or approve releases.

### Evidence producers

`sbom`, `vulnerability`, `provenance`, and `signing` produce typed claims. Their output is data presented to policy. A producer must not set the final release decision simply because it generated evidence successfully.

### Release policy

`policy.evaluate_release` owns the dependency-light authorization decision. It requires immutable subjects, platform coverage, approved runtime identity, subject-bound inventory/provenance/signature, trusted builder/signer fixture identity, and accepted vulnerability/VEX state. It cannot upgrade missing production evidence into a pass.

### Handoff writer

`handoff.write_handoff` publishes the bounded successor interface. It intentionally exports capabilities and constraints rather than Kubernetes manifests.

## Failure containment

Every phase writes into temporary/generated paths until checks pass. Manifests are published after blobs. Handoff generation replaces only its owned directory and writes a fresh manifest. The runtime cleans its temporary tree. The loopback registry is deleted after the proof.

A real production implementation needs stronger transactional storage, concurrency, authentication, retention, replication, availability, audit, key custody, and recovery. The capstone’s value is that those missing responsibilities are visible rather than hidden behind one product command.
