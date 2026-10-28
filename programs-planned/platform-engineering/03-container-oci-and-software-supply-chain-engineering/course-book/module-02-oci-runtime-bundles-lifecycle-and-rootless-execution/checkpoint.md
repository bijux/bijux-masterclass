# Checkpoint — Runtime bundle and lifecycle

## Required evidence

- accepted API, worker, and probe runtime profiles;
- executed probe bundle;
- lifecycle-state report;
- workload identity, user-namespace mapping, and writable-path proof;
- interrupted-create cleanup proof;
- rejected unsafe mount/profile example.

## Decision defense

Explain why the mandatory course lane avoids privileged lifecycle hooks, and state a case where adding one would be justified.

## Progression gate

Proceed only when you can construct a bundle without an image. Module 3 will explain how a portable OCI image graph becomes the rootfs and process defaults from which such a bundle can be prepared.

## Continue

- [Next stage](../module-03-oci-images-layers-content-addressability-and-whiteouts/index.md)
- [Course index](../index.md)
