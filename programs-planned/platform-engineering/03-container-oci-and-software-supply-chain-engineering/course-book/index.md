# Container, OCI, and Software Supply Chain Engineering

Course 1 established what an Atlas process needs from Linux. Course 2 expressed those requirements as a replaceable cloud workload contract. Course 3 changes the release boundary: instead of shipping an opaque machine image or copying application files during bootstrap, you will publish a content-addressed workload release that can be inspected, transferred, executed, and authorized independently of a particular container product.

The course is organized around one claim:

> Source becomes a release only when the image graph, platform binaries, runtime contract, inventory, origin evidence, signer identity, and promotion decision all agree on the same immutable subject.

A Containerfile that builds is not enough. A process that starts is not enough. A clean vulnerability scan is not enough. A signature is not enough. The course follows the relationships among those facts until one exact Atlas API and worker release can be handed to Kubernetes without weakening the previous courses.

## Product of the course

**Atlas Workload Release 1.0** contains:

- multi-platform API and worker image indexes for `linux/amd64` and `linux/arm64`;
- a verification-only probe image that reports runtime facts;
- deterministic OCI layouts and exact digest records;
- runtime profiles for identity, mounts, resources, signals, and health;
- registry publication and subject/referrer evidence;
- CycloneDX inventory plus bounded vulnerability, VEX, and license decisions;
- SLSA-shaped provenance in an in-toto statement and signed DSSE envelope;
- a non-compensable release-policy decision;
- a manifested handoff for Kubernetes Course 4.

## Reading path

Begin with [Start here](start-here.md) and [Orientation](module-00-orientation/index.md). Then work through the modules in order:

- [1. Containers as Linux process isolation](module-01-containers-as-linux-process-isolation/index.md)
- [2. OCI runtime bundles, lifecycle, and rootless execution](module-02-oci-runtime-bundles-lifecycle-and-rootless-execution/index.md)
- [3. OCI images, layers, content identity, and whiteouts](module-03-oci-images-layers-content-addressability-and-whiteouts/index.md)
- [4. Build graphs, cache, reproducibility, and secret hygiene](module-04-build-graphs-cache-reproducibility-and-secret-hygiene/index.md)
- [5. Multi-platform images, ABI, and architecture truth](module-05-multi-platform-images-abi-and-architecture-truth/index.md)
- [6. Registries, distribution, digests, tags, and referrers](module-06-registries-distribution-digests-tags-and-referrers/index.md)
- [7. Runtime hardening, resource control, and operational contracts](module-07-runtime-hardening-resource-control-and-operational-contracts/index.md)
- [8. SBOMs, vulnerabilities, licenses, and VEX](module-08-sboms-vulnerabilities-licenses-and-vex/index.md)
- [9. Provenance, signatures, attestations, and verification policy](module-09-provenance-signatures-attestations-and-verification-policy/index.md)
- [10. Promotion, revocation, and the Kubernetes handoff](module-10-release-promotion-revocation-and-kubernetes-handoff/index.md)

## Supporting paths

- [Study plan](study-plan.md)
- [Capstone guide](capstone.md)
- [Evidence model](evidence-model.md)
- [Language and tool strategy](language-strategy.md)
- [Standards profile](standards.md)
- [Glossary](glossary.md)
- [Study guides](guides/index.md)
- [Incident casebook](casebook/index.md)
- [Reference atlas](reference/index.md)
- [Assessment](assessment/index.md)

## How the book teaches

Every numbered module contains a complete chapter, twelve transfer problems, matching worked solutions, one controlled falsification laboratory, and a non-compensable checkpoint. The capstone code exposes the mechanisms; it does not replace the explanation. Reports and manifests are evidence; they are not the curriculum.

Every claim is labelled by evidence class: dependency-light, native-tool, target-runtime, environment-backed/not-executed, failed, or review-required. A missing external tool never becomes a pass.
