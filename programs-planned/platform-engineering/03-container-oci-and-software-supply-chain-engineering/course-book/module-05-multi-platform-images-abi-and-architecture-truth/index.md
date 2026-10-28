# Module 5 — Multi-platform images, ABI compatibility, and architecture truth

A multi-platform image index is a promise: when a client selects the descriptor for its platform, the referenced image can execute correctly in that environment. The index does not enforce the promise. It carries publisher-supplied labels.

This module turns platform metadata into independently checked evidence.

## Learning outcomes

By the end of the module you can:

- distinguish OS, architecture, variant, ABI, libc, kernel, and CPU-feature compatibility;
- compare native builds, cross-compilation, and emulated builds;
- inspect ELF headers and dynamic dependencies;
- design a correct OCI image index for amd64 and arm64;
- detect platform-label lies before publication;
- reason about QEMU/binfmt emulation evidence and limitations;
- define platform-specific test matrices and fallback behavior;
- decide when separate platform variants should not share one release version.

## “Architecture” is only one compatibility axis

OCI platform descriptors commonly name:

```text
os
architecture
variant
```

This is necessary but not always sufficient. A binary can match `linux/amd64` and still fail because it requires:

- a newer glibc symbol version;
- a dynamic loader absent from the image;
- a kernel syscall unavailable on the host;
- an x86 CPU instruction extension not present on the node;
- a particular endianness or ARM variant;
- an incompatible device or driver.

A release profile should state the minimum execution contract it actually depends on.

Atlas uses statically linked Go binaries with `CGO_ENABLED=0`, reducing libc dependencies. It still depends on Linux kernel behavior and the target instruction set. Static linking simplifies the lesson; it does not make the executable universally portable.

## OCI architecture names and executable reality

For Atlas:

```text
OCI architecture amd64 -> ELF machine EM_X86_64
OCI architecture arm64 -> ELF machine EM_AARCH64
```

The course parser reads the ELF identification bytes, endianness, class, and machine field. Publication fails if the executable machine does not match the descriptor.

This check catches the common “copied cached binary” failure. It does not prove the binary will run: dynamic dependencies and CPU features still matter.

## Native, cross, and emulated builds

### Native build

The compiler runs on the target architecture. This gives strong execution realism for architecture-specific tools and tests, but requires target hardware or a native runner.

### Cross-compilation

The compiler runs on one architecture and emits another. Go supports this well for pure-Go static programs. Native extensions, CGO, assembly, and platform-specific generators can complicate the path.

### Emulated build

Target executables run under an emulator such as QEMU, often registered through `binfmt_misc`. This enables flexible build graphs but can be slower and can differ from native CPU/kernel behavior.

A mature pipeline may cross-compile deterministic binaries, assemble images without executing target code, then run platform-specific tests on native hardware. “The build completed under emulation” is weaker than “the release passed its native target tests.”

## Index selection and fallback

An OCI image index lists descriptors. Clients select the best compatible platform according to implementation rules. Do not assume every client handles variants and annotations identically.

A release should avoid ambiguous duplicate descriptors for the same platform unless there is a governed selection mechanism. Feature-specific variants such as `amd64/v3` need an explicit compatibility and fallback strategy; otherwise an image can work on build hosts and fail on older nodes.

Atlas 1.0 publishes one `linux/amd64` and one `linux/arm64` descriptor. It does not claim Windows, ARMv7, or feature-tier variants.

## Dynamic linking changes the image contract

Inspect an ELF binary with:

```text
readelf -h
readelf -l
readelf -d
```

A dynamically linked executable names an interpreter such as `/lib64/ld-linux-x86-64.so.2` and records shared-library dependencies. The final image must include compatible versions at expected paths.

Copying a binary from a glibc build stage into a minimal musl runtime can produce an image that builds successfully and fails at startup. Likewise, copying only the executable may omit CA roots, timezone data, locale data, or NSS configuration it expects.

The final-stage review must therefore follow runtime dependencies, not only binary size.

## Kernel compatibility is not encoded in the image index

The image config can carry labels, but OCI platform descriptors do not provide a complete minimum-kernel contract. If the application requires a specific syscall or cgroup feature, the platform must enforce compatible nodes or the application must detect and degrade.

Course 4 will make node capabilities and scheduling explicit. Course 3 records requirements in the handoff:

- Linux kernel with required namespace/cgroup features;
- user-namespace and subordinate-ID availability for the optional native rootless proof lane;
- no architecture-specific device requirement;
- statically linked Atlas binaries;
- no unsupported CPU feature tier.

## Platform-specific evidence must remain attached

A multi-platform index has one top-level digest, but each platform manifest has distinct layers, configuration, and test results. Promotion policy needs both levels:

```text
top-level index evidence
+ per-platform manifest evidence
= multi-platform release decision
```

A single amd64 test cannot authorize arm64. A single SBOM may describe common source dependencies but still needs to reconcile platform-specific packages and binaries.

Atlas provenance records the index as subject and includes platform-specific outputs/materials. The release report lists each selected manifest digest and its architecture verification.

## Worked failure: the index lied

The pipeline builds amd64 first and stores `/out/atlas-api`. The arm64 stage reuses the directory through a shared cache volume. It packages the amd64 binary but labels the manifest `linux/arm64`.

The index and manifest JSON validate. Registry push succeeds. An amd64 node pulls and runs correctly. An arm64 node selects the arm64 descriptor, downloads valid blobs, and receives `exec format error`.

A robust gate detects the defect before push by comparing:

- build target;
- artifact metadata;
- ELF machine;
- manifest platform;
- target-specific runtime test.

No single field is accepted as self-authenticating.

## Cross-platform reproducibility

Do not expect amd64 and arm64 image digests to match. Their executable bytes differ, so layers, DiffIDs, manifests, and configuration may differ. Reproducibility is evaluated **within** a platform for the same controlled inputs.

The image index digest can remain stable only when all referenced platform descriptors and index metadata remain stable. Adding a new platform intentionally changes the index digest even if existing platform manifests are unchanged.

This matters for release identity. “Atlas 1.0” can refer to a version label, but adding a platform creates a new immutable index subject that requires a new promotion decision.

## Atlas capstone increment

You will:

- cross-compile API and worker for amd64 and arm64;
- inspect ELF machine/type and static-linking properties;
- build platform-specific OCI manifests;
- assemble a deterministic image index;
- run the host-compatible variant natively;
- use emulation only as optional evidence;
- inject an architecture mislabel and reject it;
- produce a per-platform evidence matrix.

The matrix records:

```text
platform label
binary machine
build method
runtime test class
SBOM subject
provenance subject
known execution assumptions
```

## Platform review questions

1. What exactly does the descriptor claim?
2. Which executable and libraries determine reality?
3. How was the target built?
4. Which tests ran natively, cross, or under emulation?
5. Which kernel/CPU/ABI assumptions remain?
6. Is evidence complete for every platform?
7. Does adding or removing a platform create a new release subject?

These questions stop a multi-platform index from becoming decorative metadata.


## Compatibility matrix — labels are necessary but incomplete

For each released platform, record more than `os/architecture`:

| Dimension | Example evidence |
|---|---|
| operating system | OCI platform `linux`; executable format and syscall model |
| architecture | `amd64` or `arm64`; ELF `e_machine` |
| variant | ARM variant where relevant |
| ABI/libc | static Go binary, or glibc/musl version and loader path |
| CPU features | baseline ISA or required extensions |
| kernel features | namespaces, seccomp, cgroup v2, required syscalls/filesystems |
| endianness/word size | executable metadata and runtime target |
| device expectations | none for Atlas, or explicit accelerator contract |
| runtime evidence | native, cross-build-only, emulated, or target integration |

An OCI index cannot encode every constraint. Runtime and release metadata must carry the rest.

## Cross-compilation evidence chain

Atlas cross-compiles Go binaries with:

```text
GOOS=linux
GOARCH=amd64 or arm64
CGO_ENABLED=0
-trimpath
empty build ID
```

The compiler output is inspected independently. For an ELF binary, `e_machine` must match the manifest architecture. Static linkage avoids a runtime loader/libc contract, but the binary still depends on the Linux syscall/kernel interface and Go runtime assumptions.

Cross-compilation proves that the compiler emitted target bytes. It does not prove those bytes run correctly on real target hardware. The release evidence matrix therefore distinguishes:

```text
B — built for target
S — statically inspected
E — executed under emulator
N — executed on native hardware
I — integrated on target-like environment
```

A production policy might require `N` or `I`; the dependency-light course lane can produce `B` and `S` for arm64 and native evidence only for the current host architecture.

## Emulation without evidence laundering

QEMU user-mode execution can detect immediate instruction/loader incompatibility and exercise application behavior. It also changes timing, syscall translation paths, CPU feature exposure, and failure behavior. Record emulator version, registration, target, and test scope. Do not relabel emulated results as native.

Full-system emulation gives a target kernel/userspace environment but is still not target hardware. Cloud arm64 instances or CI runners provide stronger native evidence.

## Dynamic images and ABI drift

If Atlas later enables CGO, the image contract grows. Record:

- ELF interpreter (`PT_INTERP`);
- shared libraries from `DT_NEEDED`;
- symbol-version requirements;
- NSS, timezone, certificate, and locale files;
- architecture-specific library paths;
- libc and distribution support windows.

Copying one dynamically linked binary into `scratch` produces a valid image graph and an unstartable process. Multi-stage builds must copy the complete runtime closure or choose a compatible runtime base.

## Index evolution and rollback

Adding a new platform changes the index digest while existing child manifests can remain byte-identical. Deployment records that pin the old index do not automatically gain the new platform. That is useful: the old release remains exact. Promotion of the new index needs a new release decision and evidence for the added child.

Removing a platform likewise changes the index. Existing nodes may still have the old child manifest cached, but a new pull by the old index remains possible only if retention preserved all referenced objects. Garbage collection must understand rollback graphs.

## Atlas platform review

For every child manifest, the capstone verifies:

1. descriptor platform fields;
2. config `os` and `architecture`;
3. entrypoint existence after unpack;
4. executable architecture;
5. identical runtime-profile semantics where intended;
6. per-platform SBOM/provenance relationship;
7. evidence class.

This prevents a common failure where one correct amd64 scan or test is attached to the top-level index and treated as evidence for arm64 without checking platform-specific bytes.

## Platform identity has more dimensions than `GOARCH`

An OCI platform descriptor commonly names operating system, architecture, and optional variant. Runtime success can additionally depend on:

- executable format and machine type;
- dynamic loader path and libc ABI;
- kernel version and enabled features;
- CPU instruction-set extensions;
- endianness and word size;
- filesystem and syscall availability;
- rootless/user-namespace support;
- runtime security profile.

The descriptor is a selection hint and release promise, not proof. Atlas verifies each Go binary’s ELF machine field before publishing the platform label. Because the binaries are statically linked with `CGO_ENABLED=0`, the dynamic-loader surface is intentionally smaller. The course still does not claim compatibility with every arm64 or amd64 machine.

### Cross-compilation, emulation, and native execution answer different questions

Cross-compilation proves that the compiler can emit a target artifact. Static inspection proves selected properties of those bytes. Emulation can exercise application logic while introducing an emulator and host-kernel translation layer. Native target execution is stronger for CPU and ABI behavior but still covers only the recorded hardware, kernel, and runtime.

A mature matrix records each lane separately:

| Target | Build | Static inspection | Emulated smoke | Native smoke |
|---|---|---|---|---|
| linux/amd64 | pass | pass | optional | current host |
| linux/arm64 | pass | pass | environment-backed | environment-backed |

Do not turn a blank cell into a pass.

### Index design and fallback

A multi-platform index should contain exactly one intended descriptor for each selection tuple. Duplicate `linux/arm64` entries without distinct variants make resolution ambiguous. A missing variant can cause a runtime to select an incompatible binary. An annotation does not repair a wrong platform object.

If the platform cannot supply a required target, fail release policy or publish a deliberately narrower index. Never copy the amd64 descriptor, relabel it arm64, and defer the failure to scheduling.

### Platform-specific dependencies belong below the index

Shared source does not imply identical layers. CA bundles, native libraries, runtime shims, and compiled binaries may differ by platform. The child manifest is the correct place for those dependencies. Top-level release policy can require that every child receives equivalent SBOM, provenance, vulnerability, and runtime evidence, even when the exact component inventory differs.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-04-build-graphs-cache-reproducibility-and-secret-hygiene/index.md)
- [Next stage](../module-06-registries-distribution-digests-tags-and-referrers/index.md)
