# Study guides

These guides explain how to use the course as an engineering apprenticeship rather than a sequence of tool demonstrations. Read them when you need a method: how to read a specification, review a build graph, preserve release evidence, or debug a failed promotion.

## Begin here

- [Self-learning method](self-learning-method.md) explains the read–model–inspect–falsify–defend cycle used throughout the course.
- [Laboratory safety](laboratory-safety.md) defines which experiments are safe locally and which require an isolated host or disposable environment.
- [Reading OCI specifications](reading-oci-specifications.md) shows how to move from normative object definitions to testable implementation claims.
- [Native-tool lanes](native-tool-lanes.md) separates the dependency-light semantic implementation from BuildKit, Docker/Podman, runc/crun, registry, and Sigstore evidence.

## Review and diagnosis

- [Containerfile review method](containerfile-review-method.md) treats a build file as a graph of authorities and outputs, not as a list of commands.
- [Debugging container releases](debugging-container-releases.md) starts from the earliest broken identity edge: source, layer, manifest, index, registry, runtime, or attestation.
- [Release evidence journal](release-evidence-journal.md) gives a durable record format for subject, toolchain, environment, policy, and residual risk.
- [Worked Atlas release walkthrough](worked-atlas-release-walkthrough.md) follows one exact API image from source tree through layer bytes, OCI graph, registry publication, runtime observation, evidence attachment, and promotion.

Use these pages selectively. The numbered chapters remain authoritative. The guides provide reusable methods when the same reasoning must be applied to another ecosystem, builder, registry, runtime, or workload.
