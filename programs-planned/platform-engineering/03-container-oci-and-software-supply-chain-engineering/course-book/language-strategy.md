# Language and tool strategy

The course uses the language that best exposes each responsibility rather than forcing every mechanism into one general-purpose language.

## Python — transparent semantic core

Python implements canonical JSON, digest logic, deterministic archives, OCI object construction, safe rootfs reconstruction, registry protocol subset, runtime-profile normalization, vulnerability/VEX logic, provenance/signing, policy, and handoff generation. The code is compact enough to read alongside the specification.

Python is not presented as a production container runtime or registry implementation. Its role is executable explanation and negative testing.

## Go — real workload artifacts

Atlas API, worker, and probe are real Go programs. They are cross-compiled for amd64 and arm64 and inspected as ELF executables. Go makes it possible to produce small static workload artifacts while still teaching architecture labels, entrypoints, health, signals, and process behavior.

The learner is not expected to become a Go specialist. Read the programs for runtime semantics and modify them only when a lab requires it.

## Shell — orchestration and independent lanes

Shell scripts express guarded native-tool workflows. They fail when required tools/environment are absent. They do not contain the conceptual explanation; the course book does.

## Containerfiles — build frontend examples

Containerfiles show how a real builder might express multi-stage, multi-platform builds. They are not the image format. The course always inspects resulting OCI objects.

## Native products — comparison evidence

BuildKit/Docker/Podman, runc/crun, ORAS/Skopeo, Cosign/Sigstore, and Syft/Grype are optional independent lanes. Use one primary tool per lane and compare mechanisms, not command aesthetics.

## What not to duplicate

Do not reimplement the full builder, runtime, registry, scanner, and signing stack in multiple languages. The learning target is stable invariants across implementations:

- exact subject identity;
- graph integrity;
- platform truth;
- effective runtime authority;
- subject-bound evidence;
- categorical release policy.

One transparent implementation plus one independent comparison is stronger than two shallow copies.
