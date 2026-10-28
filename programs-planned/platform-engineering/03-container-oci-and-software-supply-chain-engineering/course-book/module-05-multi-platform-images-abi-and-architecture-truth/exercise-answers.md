# Worked answers — Multi-platform images

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. Why does `linux/amd64` not fully describe executable compatibility?

It omits libc/ABI, dynamic loader, minimum kernel, CPU feature level, device/driver, and application-specific dependencies. It is a coarse selection key. Publishers must record and test additional execution assumptions where relevant.

## 2. Map OCI `amd64` and `arm64` to ELF machine identifiers and explain what the check proves.

OCI `amd64` maps to ELF `EM_X86_64`; `arm64` maps to `EM_AARCH64`. Matching proves the executable’s declared machine architecture agrees with the manifest label. It does not prove dynamic libraries, kernel features, CPU extensions, configuration, or application behavior.

## 3. Compare native, cross, and emulated build evidence for a CGO-enabled application.

Native builds use target compiler, libc, headers, and execution environment, giving strongest target realism. Cross builds require a cross C toolchain and target sysroot; configuration mistakes can select host libraries. Emulated builds execute target tools under emulation, improving compatibility but adding performance and emulator-behavior differences. Final confidence should include native target tests.

## 4. A binary is x86-64 but requires AVX2. What additional release/scheduling concern exists?

The generic amd64 descriptor may be selected on nodes lacking AVX2. The platform needs CPU-feature-aware scheduling/selection or a baseline binary with runtime dispatch. Publishing the variant under a generic descriptor creates hidden incompatibility.

## 5. Why can a glibc-linked binary fail in a musl runtime stage?

The executable may request a glibc dynamic loader path and symbol versions unavailable in a musl image. The kernel finds the ELF but cannot load its interpreter or shared libraries. Build-stage and runtime-stage ABI must match, or the binary must be statically linked appropriately.

## 6. Does adding an arm64 manifest to an existing amd64 index preserve the index digest? Why?

No. `index.json` bytes include the descriptor list. Adding arm64 changes the list, index bytes, and digest. Existing amd64 manifest digest can remain unchanged. The new top-level digest requires fresh subject-bound evidence and promotion.

## 7. Design a per-platform release matrix for Atlas.

Include OCI tuple, manifest digest, executable machine, compiler/toolchain, build method, dynamic/static dependencies, native/emulated test result, runtime profile result, SBOM/provenance artifact digests, and known kernel/CPU assumptions. Missing platform evidence should block full multi-platform promotion.

## 8. An arm64 image passes under QEMU on amd64. What remains unproven?

Native hardware behavior, performance, CPU-feature compatibility, kernel and driver interactions, and some timing or concurrency paths remain unproven. QEMU may also normalize or emulate instructions differently from the target machine. The result is useful execution evidence, but it must be labelled as emulated evidence and should not silently satisfy a policy that requires native target validation.

## 9. Why should one amd64 SBOM not automatically authorize the arm64 manifest?

Compiled dependencies, included shared libraries, package selection, and binary hashes can differ by architecture. A source-level component list may be shared, but the release must reconcile what each manifest actually contains and bind evidence to each subject or the top-level release with explicit platform coverage.

## 10. Explain when separate version lines may be preferable for platform variants.

Use them when platform capabilities or release cadence differ materially, compatibility cannot be maintained, or one platform requires behavior-changing patches. A unified version is valuable only if the semantic contract and support policy remain coherent across variants.

## 11. A statically linked Go binary has the correct ELF machine. Name four remaining runtime dependencies.

Linux syscall and minimum-kernel compatibility, CA roots, timezone and configuration data, DNS and network reachability, mounted storage and permissions, environment and secret injection, CPU feature availability, and resource limits can still determine success. Static linking removes one dynamic-library dependency class; it does not make the program independent of the operating environment.

## 12. Write policy pseudocode that rejects a mislabelled platform manifest.

For each index descriptor: fetch and verify manifest; reconstruct rootfs or locate declared entrypoint; parse ELF machine; map OCI platform to accepted machine IDs; reject on mismatch; then require platform-specific runtime/evidence records. Never infer truth solely from the descriptor label.

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
