# `atlas_container` semantic implementation

This package implements the smallest inspectable set of mechanisms needed to explain the Course 3 object model:

- canonical JSON and digest helpers;
- deterministic layer archives and whiteouts;
- OCI descriptors, configs, manifests, indexes, layouts, and artifact subjects;
- safe rootfs reconstruction;
- platform-to-ELF verification;
- normalized runtime configuration and bounded execution;
- loopback registry push/pull/tag/referrers;
- CycloneDX, vulnerability/VEX, provenance, DSSE signing, and policy;
- exact Course 4 handoff generation.

Read the corresponding course chapter before treating a module as an API. The package is intentionally dependency-light and pedagogical. It is not a replacement for BuildKit, containerd, runc/crun, a production registry, Syft/Grype, or Sigstore.
