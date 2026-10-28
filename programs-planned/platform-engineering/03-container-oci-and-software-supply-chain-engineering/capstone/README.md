# Atlas Workload Release 1.0 — executable capstone

The capstone is the executable companion to the course book. It exists to make OCI objects, runtime authority, registry behavior, and supply-chain evidence inspectable. It is not a production builder, registry, runtime, scanner, or signing service.

Begin with:

```bash
make capstone-tour
```

The tour cross-compiles Atlas API, worker, and probe binaries for `linux/amd64` and `linux/arm64`; constructs deterministic OCI image layouts; verifies platform labels; publishes API and worker graphs to a loopback registry; attaches subject-bound SBOM and provenance artifacts; evaluates release policy; runs the probe through a bounded namespace/rootfs harness; and writes the Course 4 handoff.

## Directory map

```text
atlas_container/   dependency-light OCI/runtime/registry/evidence mechanisms
workload/          real Go API, worker, and probe source plus Containerfiles
contracts/         Atlas build, runtime, artifact, and release-policy profiles
runtime/           reviewed effective runtime profiles
registry/          retention policy and generated local storage boundary
sbom/              deterministic inventory, vulnerability, and VEX fixtures
security/          course trust/profile documentation
releases/          one checked release plus deliberately rejected/review cases
planted-defects/   defects that prove gates can fail
native/            guarded independent-tool evidence lanes
scripts/           tour and checked-release generation
runbooks/          operational response procedures
handoff/           exact Course 3 → Course 4 interface
tests/             semantic, negative, and cross-object regressions
reports/           checked release-mechanism evidence
```

## Design principles

### Exact subjects before labels

Every authorization decision ultimately selects a digest. Tags are used only for discovery. Evidence is attached to the subject it describes, and a valid artifact for another digest is rejected.

### Graph verification before execution

The image index, platform manifest, config, compressed layers, uncompressed DiffIDs, and rootfs application are checked before a runtime is allowed to consume the result. The implementation rejects traversal and unsafe layer paths.

### Runtime profile is separate from image defaults

The image declares entrypoint and user defaults. `runtime/profiles/` records the approved execution contract. The mini-runtime observes effective UID/GID, PID, hostname, and writable paths. It intentionally does not claim complete OCI conformance, full rootless operation, seccomp/LSM hardening, or hostile multi-tenant safety.

### Evidence objects remain typed

Inventory, vulnerability/VEX, provenance, signature, runtime observation, and promotion decisions are separate objects. A release passes only when every non-compensable gate succeeds for the same subject.

### Failure sensitivity

The accepted path is not enough. Tests and planted defects show the release gates reject mutable tags, root execution, platform mismatch, secret history, incomplete inventory, wrong subjects, unauthorized builders, and missing environment evidence.

## Evidence classes

The capstone reports:

- `dependency-light-local` for mechanisms executed by the checked Python/Go implementation;
- independent native-tool evidence only when an optional lane actually runs;
- `not-executed` for production registry, operated identity, target hardware, capacity, or Kubernetes enforcement not available locally;
- `review-required` when policy needs human evidence/judgment;
- `rejected` for non-compensable failure.

Read [architecture.md](architecture.md) for state ownership and [evidence-map.md](evidence-map.md) for claim-to-oracle mapping. Then use the relevant runbook when a release or runtime gate fails.
