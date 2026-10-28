# Laboratory — Publish an index that tells the truth

## Goal

Build amd64 and arm64 Atlas binaries, assemble a multi-platform index, and prove platform labels against executable bytes.

## Safety boundary

Cross-compilation is mandatory; emulated execution is optional and must be labelled. Do not claim native arm64 evidence from QEMU on amd64.

## Baseline

Compile Atlas API and worker for both targets with the pinned Go toolchain. Inspect each ELF header and linkage.

## Hypothesis

Every platform descriptor selects a manifest whose entrypoint binary matches the declared architecture, and controlled same-platform rebuilds are byte-identical.

## Controlled action

1. create correct platform manifests and index;
2. swap the amd64 binary into the arm64 rootfs while keeping the arm64 label;
3. add an unsupported fake platform descriptor;
4. add a third correct platform descriptor and observe the new index identity;
5. if QEMU is available, execute the non-native probe and mark evidence as emulated.

## Oracle

The correct index passes. The swapped binary and unsupported platform fail policy. Adding a platform changes only the top-level index and new platform objects, not existing manifests.

## Evidence

Submit ELF outputs, descriptor matrix, index digests before/after addition, runtime evidence class, and mislabel rejection.

## Interpretation

Explain why manifest structural validity and executable compatibility are separate gates.

## Cleanup

Delete the defect layouts and optional emulation registrations created only for the lab.

## Completion gate

Every released platform has independent build, binary, and runtime evidence, and no platform claim is inferred solely from labels.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
