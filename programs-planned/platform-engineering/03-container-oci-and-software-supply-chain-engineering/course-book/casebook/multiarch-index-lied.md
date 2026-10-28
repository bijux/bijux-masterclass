# Incident case — the multi-platform index lied

## Situation

An Atlas image index advertised `linux/amd64` and `linux/arm64`. Both child manifests were valid, all referenced blobs existed, and the top-level digest had been signed. The arm64 deployment failed immediately with `exec format error`.

The arm64 manifest’s rootfs contained the amd64 executable. A build cache key included source and compiler version but omitted target architecture, so the arm64 build reused an amd64 output. The publisher trusted the OCI platform descriptor as though it were measured truth.

## Why ordinary checks passed

Digest verification proved every downloaded byte matched its descriptor. Schema validation proved the index and manifests were structurally well formed. The signature authenticated the top-level index. None of those checks compared the selected platform label with the machine identity of the executable inside the child rootfs.

A single integration test had run on amd64 and was attached to the index as “multi-platform test evidence.” That result covered only one child and one runtime environment.

## Diagnosis

- Resolve the top-level index by digest.
- Select each child descriptor explicitly rather than using host-default selection.
- Pull and unpack each child manifest.
- Locate the configured entrypoint.
- Inspect ELF `e_machine`, dynamic loader, linked libraries, and any CPU-feature assumptions.
- Compare build parameters and cache scope recorded in provenance.
- Identify which architecture actually executed in every test result.

The immediate mismatch was `EM_X86_64` under an `arm64` descriptor. Further review found that platform-specific SBOMs had also been collapsed into one generic document.

## Corrective design

Build and cache identity now include OS, architecture, variant, compiler/toolchain, and ABI-relevant inputs. Release policy verifies executable machine identity for every required child, requires subject-bound inventory and provenance, and records whether execution was native, emulated, or not executed. A top-level index is promotable only when all required child manifests satisfy their own gates.

## Transfer lesson

A descriptor is a claim. Content integrity can faithfully preserve incorrectly labelled bytes. Multi-platform truth requires inspecting both the graph edge and the target-specific content/evidence behind it.
