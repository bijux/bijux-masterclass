# Orientation — From a cloud workload contract to an OCI release

Course 2 ended with a cloud foundation and a workload contract. It did **not** end with a container image. The handoff says what Atlas requires at runtime: two long-running processes, a non-root identity, port `8080`, durable spool and result directories, ephemeral runtime state, runtime-injected secrets, bounded shutdown, and resource hypotheses that still need measurement.

This course asks a narrower and harder question:

> How can source code become a portable, content-addressed release whose bytes, runtime behavior, platform claims, inventory, provenance, and promotion decision can all be verified independently?

A Dockerfile alone cannot answer that question. Neither can a successful `docker run`.

## What you inherit

The predecessor handoff under `capstone/predecessor/` is immutable input. Read it as an interface between courses, not as background prose. It fixes these constraints:

- the API and worker run without root authority;
- the API listens on `8080`;
- `/var/lib/atlas/spool` and `/var/lib/atlas/results` survive process replacement;
- `/run/atlas` is ephemeral;
- secrets arrive at runtime and must not enter image history;
- SIGTERM begins a bounded shutdown of at most thirty seconds;
- the root filesystem may be replaced at any time;
- workload identity is short-lived and external to the image;
- CPU and memory values are hypotheses, not proven capacity.

Course 3 may package these requirements. It may not silently weaken them to make the image easier to build.

## What you will produce

The capstone, **Atlas Workload Release 1.0**, contains three multi-platform images:

```text
atlas-api
atlas-worker
atlas-probe
```

Each release is identified by an OCI image-index digest rather than a tag. Every platform-specific manifest points to a configuration object and immutable filesystem layers. The release also carries subject-bound evidence:

```text
image index digest
├── platform manifests
├── SBOM artifact
├── provenance artifact
├── vulnerability/VEX evidence
└── signature envelope
```

The final release gate must answer all of these questions:

1. Are the image and evidence objects structurally valid?
2. Do the platform labels match the executable bytes?
3. Can a runtime satisfy the inherited filesystem, identity, network, signal, and resource contract?
4. Was the release rebuilt from the declared source and materials?
5. Is the evidence bound to the exact digest being promoted?
6. Does policy authorize this candidate for the next environment?

## The three evidence lanes

This course deliberately separates evidence that is often blurred together.

### Dependency-light semantic lane

Runs with Python, Go, and ordinary filesystem/process permissions. It constructs OCI layouts, compiles two architectures, verifies digests, serves a bounded registry API, checks SBOM and provenance records, and evaluates release policy.

### Native OCI-tool lane

Uses tools such as BuildKit, Podman, Docker, `skopeo`, `oras`, `cosign`, `syft`, and `grype` when installed. These tools provide independent implementation evidence. The course never converts their absence into a pass.

### Privileged runtime lane

Uses user, mount, PID, UTS, IPC, and network namespaces; cgroup v2; seccomp; and capability controls where the host permits them. The included mini-runtime demonstrates a bounded subset. A successful local namespace experiment is not evidence of a hardened production sandbox.

## Primary and comparative implementation languages

Python is the primary explanatory language because it makes byte construction, hashing, tar archives, HTTP distribution, policy evaluation, and evidence generation inspectable. Go supplies the workload binaries because static cross-compilation makes architecture truth visible. Shell is used only where the operating-system boundary is itself the lesson.

You are not asked to reimplement a production container engine. The small implementations exist so that important objects cannot hide behind a CLI.

## Orientation tasks

Before Module 1:

1. Read every predecessor JSON file and write a one-page runtime obligation map.
2. Run `python -m unittest discover -s capstone/tests -v`.
3. Run `python capstone/scripts/run_capstone_tour.py`.
4. Locate the three different identities called a “digest” in the capstone: compressed layer digest, uncompressed layer DiffID, and image/index digest.
5. Explain why `atlas-api:1.0` is not a release identity.
6. Open `capstone/releases/accepted/release.json` and trace every evidence reference to the subject digest it authorizes.

Do not proceed because the commands printed green text. Proceed when you can explain what each command did **not** prove.

## Continue

- [Orientation laboratory](lab.md)
- [Orientation checkpoint](checkpoint.md)
- [Module 1](../module-01-containers-as-linux-process-isolation/index.md)
