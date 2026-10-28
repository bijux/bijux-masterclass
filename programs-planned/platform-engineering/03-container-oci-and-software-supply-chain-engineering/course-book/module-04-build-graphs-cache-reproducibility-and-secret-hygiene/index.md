# Module 4 — Build graphs, cache correctness, reproducibility, and secret hygiene

An image graph can be internally consistent and still be the product of an unsafe build. Module 3 proved that bytes agree with their descriptors. This module asks where those bytes came from, which inputs influenced them, what the cache reused, and whether the same declared build can be repeated without leaking authority.

A Containerfile is a frontend program. A modern builder translates it into a lower-level build graph, schedules graph vertices, resolves external materials, mounts transient inputs, and exports OCI objects. Treating the file as a linear shell script hides the actual data dependencies.

## Learning outcomes

By the end of the module you can:

- model a container build as a graph of inputs, operations, and exported artifacts;
- explain how context, frontend, builder, platform, base image, network, time, and secrets influence output;
- distinguish cache validity from semantic correctness;
- design multi-stage builds that minimize release content without hiding evidence;
- prevent credentials from entering contexts, layers, logs, cache exports, or provenance;
- define a reproducibility claim with a controlled input envelope;
- use deterministic builds without confusing identical bytes with trustworthy origin;
- audit a Containerfile for runtime, supply-chain, and maintenance consequences.

## The real build input is larger than the repository

A useful build identity is not just a Git commit:

```text
source tree digest
+ build-context selection
+ Containerfile/frontend version
+ build arguments
+ target platform
+ base image digests
+ package/module lock data
+ network-fetched materials
+ builder implementation and policy
+ environment that remains observable
= build input envelope
```

If any material is selected by a mutable name, the same source can produce different bytes tomorrow. If the builder accepts undeclared network content, the source tree is not a sufficient reconstruction recipe. If a secret changes output bytes, it is an input even when policy says it should not be recorded verbatim.

The Atlas build profile freezes base image digests, compiler version, target platform, source digest, archive metadata, and build parameters. It records native-tool execution separately from the course’s deterministic semantic builder.

## Build context is an authority boundary

The build context is the set of files the builder can read. A broad context grants unnecessary authority even if the Containerfile never intentionally copies every file.

Common accidents include:

- `.git/` history containing removed credentials;
- local environment files;
- SSH keys;
- cloud credentials;
- test fixtures with personal data;
- build output from another architecture;
- large caches that slow transfer and poison cache keys.

`.dockerignore` or `.containerignore` is not just a speed optimization. It is a security and reproducibility policy. The Atlas context allowlist includes source, module metadata, and Containerfiles. Release proof fails if high-risk patterns are present in the effective context.

A file outside the context cannot be copied by ordinary build instructions. That is a meaningful reduction of authority.

## Containerfile instructions create graph vertices

Consider:

```dockerfile
FROM golang@sha256:<digest> AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -trimpath -o /out/atlas-api ./cmd/atlas-api

FROM scratch
COPY --from=build /out/atlas-api /usr/local/bin/atlas-api
USER 65532:65532
ENTRYPOINT ["/usr/local/bin/atlas-api"]
```

The first `COPY` and dependency download can be cached independently of application source. The second `COPY` invalidates only later vertices when source changes. The final stage contains only the binary and metadata required at runtime.

This arrangement improves cache reuse and shrinks the release. It does not automatically make the build hermetic. `go mod download` may contact the network; the base image digest says which base manifest was selected, not whether the registry served it through a trustworthy channel; compiler behavior can depend on version and environment.

## Cache keys are claims about equivalence

A cache hit says: “The builder believes this vertex’s result is reusable for these inputs.” It does not say the output is secure, current, or correct for the operator’s unstated intent.

A sound cache key includes every input that can influence output. Missing inputs create false hits. Overly broad inputs create false misses.

Examples:

- If the target architecture is omitted, an amd64 binary can be reused for an arm64 build.
- If a secret value is included in a cache key, cache metadata can reveal sensitive change patterns and prevent useful reuse.
- If a package index is fetched without pinning but the network response is not represented, a cached install result hides mutable external input.
- If build arguments control compiler flags but are not included, two different intended builds can share one result.

BuildKit’s secret and SSH mounts are designed so sensitive material can be available to a step without being copied into the resulting filesystem snapshot. Policy must still ensure the command does not write the secret into another path or log it.

## Multi-stage builds separate build authority from runtime content

Build stages often need compilers, package managers, certificates, and source. Runtime stages often need only the executable, selected data files, trust roots, and identity metadata.

The security value of multi-stage builds is not “fewer layers.” It is the ability to expose broad build authority without exporting all of it into the runtime filesystem.

Review the cross-stage copy boundary carefully:

- Is the source path exact?
- Could a compromised build step place extra files under a copied directory?
- Are ownership and modes set intentionally?
- Are debug symbols or source paths included?
- Does the binary require dynamic libraries omitted from the final stage?
- Are CA certificates or timezone data required?

The Atlas final stage uses `scratch` for statically linked Go binaries. That removes package-manager metadata and shell utilities, but it also removes tools that operators might expect during debugging. Course 4 must therefore rely on external debugging and ephemeral tooling rather than mutating production images.

## Secret hygiene begins before the build

There are several distinct leak channels:

```text
source control
build context
Containerfile arguments
process environment
command line
build logs
filesystem snapshots/layers
cache metadata/export
provenance parameters
SBOM properties
registry annotations
```

`ARG TOKEN` is not a safe secret mechanism. Arguments can appear in history, logs, provenance, and cache metadata. Environment variables are not automatically safer.

A secure pattern uses a transient secret mount:

```dockerfile
RUN --mount=type=secret,id=registry_token \
    token_path=/run/secrets/registry_token && \
    use-token-without-copying "$token_path"
```

Then test that:

- the secret path does not exist after the step;
- no layer contains the secret bytes;
- logs redact it;
- provenance identifies the secret *slot* or requirement without exposing the value;
- cache export does not contain it;
- the credential is scoped and short-lived.

If the build tool cannot provide these properties, move the sensitive operation outside the image build or redesign the dependency flow.

## Pinning and freshness are different concerns

Pinning a base image by digest gives repeatability and protects against tag movement:

```dockerfile
FROM cgr.dev/chainguard/static@sha256:<exact>
```

It also freezes known vulnerabilities until the digest is deliberately updated. A good release process combines:

- digest pinning for deterministic selection;
- automated discovery of newer acceptable digests;
- SBOM/vulnerability comparison;
- controlled rebuild;
- runtime and regression evidence;
- deliberate promotion.

“Always pull latest” sacrifices review. “Never update pinned bases” sacrifices maintenance. The correct workflow separates discovery from release.

## Reproducibility is a scoped experiment

A strong reproducibility record states:

- which source digest;
- which materials and digests;
- which builder/frontend versions;
- which target platform;
- which parameters;
- which clock/locale/path normalization;
- whether network was disabled or mirrored;
- which output digest was compared;
- how many independent rebuilders/environments participated.

One builder running twice in the same workspace can detect accidental nondeterminism. It is not independent reproducibility. A second builder under a separately provisioned environment gives stronger evidence. Different implementations producing semantically equivalent but byte-different layers may still be correct, but they do not satisfy byte reproducibility.

Atlas makes a precise claim: the course semantic builder produces byte-identical OCI indexes for controlled source, toolchain, and metadata inputs. The native-tool lane records its own result and never inherits that claim automatically.

## Deterministic does not mean trustworthy

Malware can be reproducibly built. A compromised builder can deterministically emit a backdoor. A malicious source commit can have perfect provenance.

Reproducibility helps detect hidden inputs and compare independent outputs. Trust requires additional decisions about:

- source authorization and review;
- builder identity and isolation;
- dependency policy;
- secret handling;
- signing authority;
- vulnerability and license policy;
- release approval.

This is why the course keeps digest proof, provenance, and policy as separate gates.

## Worked case: cache hit for the wrong architecture

A build graph compiles Atlas using:

```bash
go build -o /out/atlas-api
```

The cache key includes source and `go.mod` but omits `GOARCH`. The amd64 build runs first. The arm64 export reuses the cached binary, labels the manifest arm64, and publishes a valid multi-platform index.

Every OCI digest is correct. The image index is structurally valid. The release is wrong.

The fix has three layers:

1. make target OS/architecture explicit build inputs;
2. include them in the compilation vertex/cache key;
3. independently inspect the resulting executable before publication.

Cache correctness and platform truth reinforce each other; neither should be assumed from the other.

## Atlas capstone increment

You will review and build three Containerfiles:

- API;
- worker;
- probe.

The lab establishes:

- minimal allowlisted contexts;
- pinned base/toolchain identities;
- multi-stage boundaries;
- exec-form runtime metadata;
- non-root identity;
- no embedded secrets;
- controlled reproducibility;
- architecture-aware cache inputs.

You will generate a build-input record that later becomes part of provenance. You will also create a deliberately unsafe secret-layer candidate and prove that deleting the final file does not repair the release.

## A build-review sequence that scales

Review a build in this order:

1. What is the effective context?
2. Which external materials are selected, and are they immutable?
3. Which build stage has network and secret authority?
4. Which instructions define cache boundaries?
5. Which parameters can alter output?
6. Which files cross into the final stage?
7. Which runtime defaults are exported?
8. Which platform is being built?
9. What reproducibility claim is being made?
10. What evidence will later bind this build to the released digest?

This sequence keeps optimization secondary to correctness and authority.


## Build threat model — who can influence the output?

A build is an authority boundary. List every actor and input that can affect the result:

- source authors and reviewers;
- dependency and base-image publishers;
- build frontend and builder implementation;
- CI controller and worker image;
- network endpoints reached during the build;
- cache exporter/importer;
- secret provider;
- registry used for materials and output;
- clock, locale, filesystem, CPU architecture, and kernel behavior;
- release metadata injected by the pipeline.

The graph is trustworthy only to the extent that these influences are controlled and recorded. A hermetic build reduces undeclared influence; it does not make an unreviewed source or malicious pinned dependency safe.

## Containerfile review as a graph review

Read each instruction as a node with inputs and outputs.

```dockerfile
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download
COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -trimpath -o /out/atlas-api ./cmd/atlas-api
```

The first `COPY` narrows the dependency-download key. The second exposes the remaining context. Cache mounts improve performance without becoming output layers, but the cache content can still influence the build if the tool accepts corrupted entries. Network use during dependency resolution is an input and needs immutable checksums and policy. The final binary should not inherit the module cache or compiler credentials.

Review questions:

1. Which paths enter the context despite not being copied?
2. Which instructions can access secrets or network?
3. Are remote materials pinned by digest and verified?
4. Which cache scopes can cross repository, tenant, or architecture boundaries?
5. Which values affect bytes but are absent from provenance?
6. Does the runtime stage contain only declared output?

## Secret exposure paths

Secrets leak through more than `COPY`:

- build arguments recorded in history or provenance;
- environment variables visible to child processes;
- shell tracing and command output;
- package-manager configuration copied into a later stage;
- cache mounts shared beyond the intended build;
- error archives and test reports;
- compiler embeds, source maps, or debug sections;
- accidental context inclusion;
- base layers already containing credentials.

A secret mount limits persistence only when the build instruction and tool avoid copying or logging it. The lab scans every layer, configuration/history, generated artifact, and evidence record—not only the final rootfs.

## A reproducibility protocol

A defensible experiment defines:

```text
subject           exact output being compared
source            immutable source identity
materials         exact base/dependency identities
builder           implementation and version
parameters        target, flags, frontend syntax, environment
network policy    disabled or recorded immutable fetches
cache policy      empty/warm; scope and trust
normalization     timestamps, paths, locale, ownership, compression
comparison        byte digest plus structured diagnostics on mismatch
repetitions       enough to detect intermittent nondeterminism
```

Run at least:

- two clean builds on the same worker class;
- one warm-cache build;
- one independent worker or builder implementation where feasible;
- each target architecture separately.

If output differs, compare layer, config, manifest, and index digests to localize the first divergence. Do not label the entire project “non-reproducible” before identifying which object changed.

## Cache poisoning and scope

Cache identity is a security property. A cache entry should be reusable only when every input relevant to the output is equivalent. Scope caches by repository, trusted builder, platform, frontend, and dependency context. Verify content-addressed cache objects. Do not allow untrusted pull requests to publish cache state consumed by protected releases without an isolation or promotion step.

Atlas’s dependency-light builder starts from controlled source bytes and does not use a remote cache. The native BuildKit lane is required to test real frontend/cache semantics. Its absence remains an explicit evidence gap.

## Hermeticity is a claim about undeclared influence

A build is hermetic when its result depends only on declared inputs available through controlled interfaces. Network access, wall-clock time, host locale, host architecture, mutable package indexes, undeclared environment variables, and shared caches can all influence output.

A practical audit asks the builder to run with increasingly strict boundaries:

```text
normal build
→ network disabled after dependency acquisition
→ empty ambient environment
→ clean isolated cache
→ fixed timestamps and locale
→ second builder instance
→ second host architecture
```

Matching outputs in one lane prove only that lane. They do not prove universal reproducibility. Conversely, a mismatch is useful: recursively compare manifests, configs, layers, tar headers, file content, and compiler metadata until the first divergent input is identified.

### Cache correctness precedes cache speed

A cache key must cover every input that can change an output. If a build step reads `go.mod`, `go.sum`, source files, target architecture, compiler version, flags, and a secret-derived response, omitting any relevant value can reuse an incompatible result.

Do not hash secrets directly into portable cache metadata. A secret should authorize retrieval during the vertex and should not become an output, log, layer, provenance parameter, or reusable shared-cache key. Prefer a secret mount whose bytes are absent from the build context and final filesystem. Then test non-interference: changing the secret without changing the authorized dependency should not alter the release bytes.

### Multi-stage builds reduce transfer, not automatically risk

A final `FROM scratch` stage can be excellent, but only if the copied output set is known. `COPY --from=build /out/ /` transfers every file under `/out`, including accidental debug files, credentials, test databases, and architecture variants. Treat the stage boundary as an API:

```text
/out/atlas-api
/out/NOTICE
/out/ca-certificates.crt   # only if required
```

Assert the inventory, ownership, modes, architecture, and hashes before copying. A minimal image is not one with few megabytes; it is one whose runtime contents and omissions are intentional.

### Build provenance must describe the real builder

A handcrafted provenance statement can be structurally valid and still false. The trusted builder must generate evidence from its own execution boundary, bind the output subject, record resolved source and materials, and prevent the caller from substituting arbitrary claims. Course-generated provenance is useful for learning verification order, but it is labelled fixture evidence. An operated builder is a different assurance class.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-03-oci-images-layers-content-addressability-and-whiteouts/index.md)
- [Next stage](../module-05-multi-platform-images-abi-and-architecture-truth/index.md)
