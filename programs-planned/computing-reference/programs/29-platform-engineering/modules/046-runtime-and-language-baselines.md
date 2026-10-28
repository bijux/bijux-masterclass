---
module_id: PLAT-046
program: Platform Engineering
level: 1
module_number: 46
title: Runtime and Language Baselines
status: complete
last_verified: 2026-09-02
---

# Runtime and Language Baselines

## One-Page Review

### Governing question

How should a platform define, build, secure, test, observe, upgrade, deprecate, and retire language/runtime baselines so teams receive useful portability and support without freezing obsolete versions, hiding dependency risk, multiplying untested combinations, or mistaking a container image for an application contract?

### Essential definitions

- A **runtime baseline** is a versioned, tested compatibility envelope joining language/runtime, build toolchain, dependency policy, artifact/image, architecture, workload archetype, execution behavior, security, telemetry, operations, and lifecycle.
- A **runtime profile** specializes a baseline for a supported behavior such as request service, event consumer, batch job, or stateful member; it is not a team-specific fork.
- A **support channel** is a published lifecycle state with admission, update, response, compatibility, and end-date consequences, such as recommended, supported, maintenance, experimental, deprecated, or retired.
- A **compatibility matrix** records combinations the platform has actually admitted and tested; absence is unsupported, not implicit compatibility.
- A **toolchain lock** identifies compilers/interpreters, package managers, plugins, build images, dependencies, and configuration sufficiently to explain and repeat a build.
- A **base image** is the governed lower filesystem/config layer on which an application image is built; its digest, contents, user, certificates, and update policy are part of the artifact contract.
- An **SBOM** identifies software components and relationships in an artifact; it is inventory evidence, not proof of absence of vulnerabilities or malicious behavior.
- **provenance** is verifiable information about where, when, and how an artifact was produced; it is distinct from a signature over opaque bytes.
- **current conformance** is evidence that a workload now satisfies a baseline revision; generation ancestry or a passing build from last year is insufficient.
- A **runtime exception** is a time-bounded, owned deviation with rationale, compensating controls, evidence, migration trigger, and expiry—not a permanent unsupported path.

### Central model, mechanism, or theorem

Represent baseline $b$ by compatibility envelope $E_b\subseteq L\times T\times D\times I\times A\times W\times P$: language/runtime revision $L$, build toolchain $T$, dependency state $D$, artifact/image $I$, architecture $A$, workload profile $W$, and policy revision $P$. A workload configuration $x$ is supported only if $x\in E_b$ and current conformance evidence passes. If dimensions have supported cardinalities $n_1,\ldots,n_k$, naive full testing grows as $N=\prod_i n_i$; baseline design must intentionally reduce combinations and use risk-based interaction tests without claiming untested tuples.

### Critical invariants

- Baselines are derived from supported workload behavior and user outcomes, not language popularity, team preference, or one Dockerfile.
- Every admitted tuple names exact compatible revisions or bounded rules; mutable `latest`, floating toolchains, and unspecified architecture are not reproducible support contracts.
- Source, toolchain, dependencies, base layers, build steps, artifact digest, SBOM, provenance, policy, and deployment remain traceable without embedding secrets.
- Builds use isolated least-privilege identities, controlled inputs/egress, deterministic practices where feasible, and independently verifiable outputs; reproducibility is measured, not assumed.
- Runtime processes handle PID 1, signals, deadlines, shutdown, exit codes, temporary files, filesystem permissions, clocks/locales, DNS/TLS, resource limits, and health according to their archetype.
- Non-root execution, minimal privileges, read-only roots where compatible, explicit writable paths, trusted certificates, and secret references are defaults with tested exceptions.
- Memory/CPU/concurrency/threads/GC/event loops honor container/cgroup limits and shutdown budgets; host observations are not trusted blindly.
- Dependency inventory, vulnerability/exploitability review, license/policy, update automation, and emergency rebuild reach both new and existing consumers.
- Telemetry libraries, context propagation, logs, metrics, traces, profiles, and crash evidence are versioned and privacy/cardinality constrained.
- Baseline changes pass source, build, supply-chain, architecture, runtime, security, integration, performance, failure, upgrade, rollback, and retirement tests for every supported profile.
- Deprecation starts before upstream end of support, inventories consumers, supplies tested migration, and removes admission, builders, images, credentials, caches, docs, and exceptions after migration.
- A platform may support a narrow safe set and an exception path; it must not claim arbitrary runtimes are supported merely because Kubernetes can start their containers.

### Common failures

Publishing a list of allowed languages without runtime contracts; pinning source dependencies but floating the builder or base image; using `latest`; rebuilding an old tag to different bytes; generating an SBOM but never correlating it to the deployed digest; treating a vulnerability scanner score as risk truth; running builders with production credentials; copying secrets into image layers; assuming a signed artifact came from a trusted build; using shell-form entrypoints that swallow signals; forcing abrupt shutdown; letting runtimes size memory from the host; permitting unbounded threads or connection pools; writing to an undeclared root filesystem; mixing architecture variants under one unverified tag; changing telemetry semantics fleet-wide without compatibility; declaring end-of-life only after upstream support ends; and deleting a template while old images, toolchains, caches, workloads, and exceptions remain.

### Compact example

A request-service baseline supports one language release line, one package-manager range, pinned build image/action digests, two tested CPU architectures, a minimal non-root base image, a maintained HTTP/telemetry library set, resource and signal behavior, SBOM/provenance, and three lifecycle channels. A service lock file and normalized source build into an OCI image indexed by architecture; each manifest digest is scanned, signed/attested, deployed to conformance tests, and correlated to evidence. The runtime reads cgroup limits, bounds worker concurrency and memory, writes only `/tmp` and a declared cache, stops admission on termination, drains within budget, and emits redacted telemetry. A new runtime revision enters canary fixtures, then supported consumers receive reviewable upgrades. Old revision admission stops before upstream end of support; exceptions expire and the builder/base/cache are removed only after the last workload migrates.

### Connections

Runtime baselines implement the workload archetypes and service-template contracts from [PLAT-041](041-workload-archetypes.md) and [PLAT-042](042-service-templates.md), specialize batch, event-driven, and stateful behavior from [PLAT-043](043-batch-and-scheduled-workload-templates.md) through [PLAT-045](045-stateful-workload-standards.md), and compose build/artifact/deployment/configuration/secret/telemetry capabilities from earlier modules. The next modules standardize health, telemetry, security, upgrades, and golden-path governance across these profiles.

## Governing Question

What bounded compatibility and lifecycle contract lets a platform say “we support this application runtime here” and back that statement with current build, supply-chain, execution, security, performance, operations, upgrade, and retirement evidence?

Languages do not run in isolation. A production process depends on compiler/interpreter, standard library, package manager, native libraries, OS/CA/timezone data, CPU architecture, container entrypoint, kernel features, resource limits, workload controller, configuration, telemetry, dependencies, and update policy.

A baseline makes these dependencies intentional. It does not require identical applications or ban domain choice. It supplies a narrow, well-tested platform-owned envelope and explicit customization boundaries while leaving product logic with the team.

The platform must also serve existing workloads. A perfect starter template that does not patch or migrate yesterday’s services is a copying mechanism, not a support system. Baseline value is measured over current deployed state and recovery, not scaffold adoption.

## Why This Matters

Runtime defects scale across the fleet. A vulnerable base layer, broken certificate bundle, bad signal handler, incorrect memory heuristic, or telemetry incompatibility can affect every service generated from the path.

Support combinations grow quickly. Four languages, three active versions, two architectures, five archetypes, and two base families already yield 240 tuples before frameworks and dependencies. Claiming all are supported without a matrix makes incidents discover the real boundary.

Containers increase portability only within a contract. OCI specifications standardize image and runtime formats, but application behavior still depends on architecture, kernel, filesystem, clocks, DNS, certificates, signals, resources, and external services.

Supply-chain evidence is layered. A lock file identifies resolved dependencies but not the builder. A signature authenticates a signer but not build inputs. An SBOM inventories components but can be incomplete. Provenance describes production but must be verified and tied to policy. None independently proves artifact safety.

Lifecycle delay converts convenience into exposure. Once upstream stops security maintenance, every exception consumes scarce response capacity. Migration must begin while both old and new toolchains still build, test, and run.

## Prerequisites and Retrieval

Retrieve compilers, interpreters, linking, ABIs, standard libraries, package managers, dependency resolution/lock files, semantic versioning, native extensions, cross-compilation, CPU architectures, operating-system processes, PID 1, signals, exit codes, filesystems, clocks/locales/timezones, DNS/TLS/certificates, container images/runtimes, OCI manifests/indexes, cgroups, CPU/memory/IO limits, garbage collection, event loops, concurrency, health, graceful shutdown, configuration/secrets, builds/caches, hashes/signatures, SBOMs, provenance, reproducible builds, vulnerability and license analysis, artifact registries, admission policy, telemetry, SLOs, performance testing, canaries, migrations, and deprecation.

You should distinguish language from runtime; runtime from framework; toolchain from dependency graph; source lock from build reproducibility; image tag from digest; image manifest from multi-platform index; artifact signature from provenance; SBOM presence from completeness; vulnerability presence from exploitability and remediation priority; host memory from cgroup limit; process responsiveness from service readiness; runtime telemetry from product semantics; upstream support from platform support; compatibility claim from tested tuple; and template ancestry from current conformance.

## Learning Objectives

After completing this module, you should be able to:

1. specify a runtime baseline and profile as a bounded compatibility/lifecycle product;
2. construct a risk-based compatibility matrix across runtime, toolchain, dependencies, image, architecture, archetype, and policy;
3. build traceable artifacts with controlled inputs, SBOM, provenance, signatures/attestations, and independent verification;
4. define portable process, signal, filesystem, configuration, certificate, clock, and resource behavior;
5. size memory, concurrency, threads, pools, and shutdown for container limits and workload objectives;
6. govern dependency, vulnerability, license, telemetry, and base-image updates across the installed fleet;
7. test architecture, security, performance, failure, upgrade, rollback, and emergency rebuild paths;
8. manage recommended, supported, maintenance, experimental, deprecated, retired, and exception channels; and
9. migrate brownfield consumers and retire builders, images, credentials, caches, tooling, and documentation safely.

## Core Exposition

### Define support as an outcome

Begin with a workload archetype and user cohort. A request service needs bounded startup, concurrent request handling, deadlines, graceful drain, health, and telemetry. A batch job needs terminal results, retry/idempotency, checkpoint, and exit semantics. One “language image” cannot prove both.

Define terminal outcomes: source builds through an authorized path; a digest-addressed artifact is admitted; it deploys under the selected profile; acceptance behavior and telemetry pass; upgrades and rollback are available; on-call can diagnose it; and retirement is owned.

State who owns language expertise, build adapter, base image, common libraries, runtime profile, security response, observability, application code, dependency updates, and migration. Support needs a contact and response objective, not merely documentation.

Publish non-guarantees. A baseline does not prove domain correctness, every third-party package is safe, performance for arbitrary workloads, portability to every kernel, or compatibility with unsupported flags/native extensions.

Include existing services from the beginning. Inventory runtime version, toolchain, dependencies, image digest, architecture, profile, owner, deployment, conformance, exceptions, and end-of-support risk.

### Write the baseline specification

Record stable ID/revision, owner/support, intended archetypes, language/runtime release policy, package manager/build system, source/layout/customization, dependency/lock policy, native toolchain, build environment, base image, architectures, artifact format, entrypoint, OS/runtime requirements, configuration/secrets, filesystem, network/TLS, resources/concurrency, signals/shutdown, health, telemetry, security controls, supply-chain evidence, test matrix, performance envelope, compatibility, support channel, upgrades, exceptions, deprecation, and retirement.

Separate contract revision from component versions. Updating a patched compiler may preserve contract behavior; changing default concurrency, filesystem ownership, telemetry schema, or minimum TLS can change the baseline contract.

Express exact approved versions or machine-checkable bounded ranges with immutable resolution. “Current LTS” is human guidance, not an artifact identity. Record resolution time, source, and digest.

Document customization surfaces. Teams own application packages, domain code, tests, and supported runtime settings. Platform-owned build actions, base policy, entrypoint adapter, telemetry hooks, and deployment contracts evolve through versioned interfaces.

Reject arbitrary escape hatches such as raw build shell, untrusted package registry, unrestricted base image, or arbitrary runtime flags inside the supported path. Route material needs to an exception/review.

### Define support channels and time

Use a small lifecycle model. **Recommended** is the default for new work. **Supported** receives normal security/operational response. **Maintenance** receives critical fixes while migration is expected. **Experimental** has bounded non-production or explicitly limited guarantees. **Deprecated** has stopped new admission and has a deadline. **Retired** has no supported execution path.

Define dates and triggers for every revision: upstream release/support, platform qualification, recommended transition, new-admission stop, maintenance end, exception expiry, builder/base removal, and evidence retention.

Platform support may be shorter than upstream support when integration or expertise is absent. It may not safely be longer unless the organization accepts source-level patching, rebuild, security response, and legal obligations.

Start migration before upstream end of security fixes. Leave time for dependency compatibility, code change, performance tests, canaries, regulated approval, and rollback.

Publish emergency rules. A critical compromise may skip ordinary cadence, pause builds/deployments, revoke artifacts, rebuild consumers, and accelerate retirement under incident authority.

### Bound the compatibility envelope

Define dimensions: language/runtime, toolchain/package manager, framework/common library, native ABI, base/OS, architecture, artifact format, workload archetype, Kubernetes/runtime class, policy, telemetry, and storage/network dependencies.

Record supported tuples explicitly. A language version that builds for `amd64` but lacks a tested native dependency on `arm64` is not multi-architecture supported. A framework compatible with a runtime in unit tests may still violate shutdown or memory behavior.

The Cartesian product grows as $N=\prod_i n_i$. Reduce it by choosing one recommended toolchain/base per release, controlling profiles, sharing common libraries, and removing obsolete options. Do not hide combinations through a universal template full of conditionals.

Use equivalence/risk reasoning for tests. Pure bytecode modules may share some evidence across architectures; native crypto, compression, database drivers, JITs, and filesystem watchers require targeted tests. Record why a dimension is considered equivalent.

Absence from the matrix means unsupported or experimental, not “probably works.” Support claims are positive evidence.

### Control build inputs and identity

Pin source commit, submodules, compiler/interpreter, package manager, plugins, build image/action, dependency registries, resolved dependencies, OS/native packages, configuration, and build instructions. Avoid hidden downloads during tests or package install.

Use lock files according to ecosystem semantics and verify hashes/signatures where available. Lock files can omit build tools, native system packages, generated sources, and remote scripts; capture the whole input graph.

Isolate builds from developer machines and production authority. Use ephemeral least-privilege workload identity, controlled network egress, clean workspaces, explicit clocks/locales, and separated signing/attestation authority.

Never pass secrets as build arguments that become image history, layers, caches, logs, or provenance. Use ephemeral secret mounts/brokers excluded from outputs and prove redaction.

Give each build an operation ID and record inputs, builder identity/revision, commands/policy, timestamps, outputs/digests, SBOM, tests, and provenance. Unknown external upload status is reconciled by digest rather than blindly overwriting tags.

### Pursue reproducibility without overclaiming

The reproducible-builds definition requires that given the same source, build environment, and instructions, parties can reproduce bit-for-bit identical artifacts. Each of those inputs must be defined.

Remove uncontrolled timestamps, locale, file ordering, random seeds, absolute paths, user/host names, network responses, and non-deterministic archive metadata where feasible. Use canonical generation and stable dependency sources.

Perform independent rebuilds on representative or high-risk baselines and compare digests. A single deterministic-looking CI run does not establish reproducibility.

Some artifacts include legitimate signatures, build IDs, or provider metadata that prevent byte equality. Separate deterministic core from nondeterministic envelope, document it, and compare normalized/semantic evidence rather than falsely claiming reproducibility.

Reproducibility detects unexplained difference; it does not prove both builds are free from malicious source, compiler backdoors, or shared compromised inputs.

### Produce and verify supply-chain evidence

Generate an SBOM from final artifact contents and build metadata, including language and OS packages plus relationships where tooling supports them. Bind it to the immutable artifact digest and retain its format/tool revision.

Generate provenance describing source, builder, inputs, parameters, process, and outputs according to an adopted schema such as SLSA provenance. Verify issuer/identity, subject digest, source/revision, builder policy, timestamps, and expected parameters at admission.

Sign or attest through protected workload identity and transparency/verification policy where appropriate. A valid signature only proves possession/use of a key under its trust policy; it does not make content safe.

Scan source, dependencies, secrets, licenses, artifacts, and deployment configuration at suitable stages. Correlate results to exact revisions and preserve raw evidence under access/retention policy.

Admission combines evidence: approved builder/base, provenance, signature, SBOM, known-risk policy, tests, owner, runtime profile, and exception. Scanners are fallible; response includes exploitability, reachability, exposure, compensating controls, and deadlines rather than score-only decisions.

### Build OCI artifacts deliberately

OCI image specifications define content-addressed manifests, configurations, layers, descriptors, and multi-platform indexes; the runtime specification defines the configuration/interface for running a filesystem bundle. Use released supported revisions and verify implementation compatibility.

Build minimal application images from governed base digests. Minimal means all required runtime libraries, certificates, timezone/locale data, diagnostics or approved debugging path, and licenses are present—no more, no less.

Use multi-stage builds so compilers, package caches, test credentials, and source do not enter the runtime image. Inspect layers, history, config, permissions, user, capabilities, entrypoint, environment, and labels.

Publish immutable digests. Tags are human references that can move; deployment and evidence bind to digest. Do not rebuild the same release tag to different bytes. Issue a new artifact identity and supersession record.

For multi-platform images, build and test each platform manifest and the index that selects them. Equal source does not prove equal native libraries, performance, or behavior.

### Make the process a good runtime citizen

Use an exec-form entrypoint or a verified init/launcher so the application receives signals as intended and reaps child processes when needed. Shell wrappers can change quoting, PID, signal, and exit behavior.

Define startup stages, readiness, liveness, and terminal exit codes. Slow initialization belongs behind startup evidence; dependency outages should not cause endless liveness restart when restart cannot help.

On termination, stop accepting work, propagate cancellation, drain bounded in-flight operations, flush required buffers/checkpoints/telemetry, release leases, and exit before the platform deadline. Forced termination remains a tested failure case.

Treat shutdown budget as an end-to-end contract. If grace is $G$, reserve time for load-balancer/consumer removal, drain $D$, cleanup $C$, and safety margin $S$ such that $D+C+S\leq G$ after admission stops.

Do not run background work whose ownership disappears at request completion unless the archetype provides durable scheduling/queueing. Process exit loses in-memory tasks.

### Standardize filesystem and process privilege

Run as a non-root, non-privileged identity with a known UID/GID strategy. Drop capabilities, disable privilege escalation, use a default-seccomp posture, and avoid host namespaces/devices unless a reviewed profile requires them.

Use a read-only root filesystem where the runtime/ecosystem supports it. Declare writable paths for temporary files, caches, sockets, dumps, and application data with capacity, permissions, lifetime, backup, and cleanup.

Do not write authoritative data to ephemeral container filesystems. Do not assume `/tmp` is unlimited, executable, persistent, private across containers, or cleaned on application schedule.

Set a predictable working directory and file creation mask. Handle read-only package/home directories; many runtimes attempt to create caches, histories, or certificate stores on first use.

Kubernetes Pod Security Standards provide baseline/restricted control definitions, but conformance to them does not prove application authorization, dependency safety, or data handling.

### Normalize clocks, locale, DNS, and TLS

Use UTC internally for timestamps and explicit business timezones/calendars where required. Do not depend on container local timezone or host locale. Test daylight-saving, locale formatting, Unicode, and clock skew.

Use monotonic clocks for elapsed durations/deadlines where the runtime supports them; wall clocks can jump. Propagate absolute deadlines carefully across systems with bounded skew.

Include maintained trust roots and define certificate rotation/reload. A minimal image without necessary CA data breaks TLS; an old base can trust obsolete roots. Do not disable verification to repair image defects.

Resolve DNS with bounded timeout/retry and respect provider caching semantics. Language runtimes may cache positive or negative results beyond service changes; test failover and connection refresh.

Specify proxy and no-proxy behavior, IPv4/IPv6 support, TLS versions/ciphers, hostname verification, and outbound destination policy by profile rather than inherited developer environment.

### Read container resource limits correctly

Runtimes historically inferred CPU and memory from the host. A baseline verifies the selected runtime/toolchain observes the active cgroup/container limits and records exceptions.

Let container memory limit be $M$, fixed runtime/native overhead $H$, per-concurrent-operation memory $m$, concurrency $c$, and reserve $R$ for variance, buffers, telemetry, and kernel-accounted use. A feasibility condition is

$$
H+c m+R\leq M.
$$

This is a budgeting model, not a proof: allocation distributions, fragmentation, JIT, GC, native extensions, mmap, page cache, and bursts need measurement.

CPU limits/requests affect scheduling and throttling; language “available processor” counts may drive thread pools, parallel GC, or workers. Define explicit bounded defaults and observe throttling/latency rather than blindly using host cores.

Ephemeral storage, open files, processes/threads, sockets, connections, and outbound rate also need limits. A memory-safe language can still exhaust every other resource.

### Bound concurrency, pools, and backpressure

Choose concurrency from workload deadline, service time, memory, CPU, downstream capacity, and fairness. A default of one worker per core can be wrong for blocking IO, event loops, native parallelism, or constrained dependencies.

Bound request queues, worker pools, event-loop work, background executors, connection pools, retry concurrency, and batch sizes. Unbounded queues convert overload into memory exhaustion and stale work.

For average concurrency $L$, arrival rate $\lambda$, and average time in system $W$, Little’s Law gives $L=\lambda W$ under stable long-run conditions. Use it to cross-check measurements, not to size variable tail behavior alone.

Coordinate application concurrency with replica autoscaling and downstream limits. Ten replicas each opening 100 database connections may exceed a 300-connection service even if every instance passes local tests.

Backpressure should reject, shed, pause, or queue durably according to the archetype. Silent in-memory accumulation is not resilience.

### Tune garbage collection and native memory from evidence

Managed runtimes trade allocation throughput, pause time, CPU, and heap size. Start with runtime-supported container awareness and conservative profile defaults; tune only against representative workloads and objectives.

Heap is not total memory. Account for stacks, JIT/code cache, direct buffers, native libraries, TLS, compression, allocator arenas, mmap, page cache, sidecars, and diagnostic dumps.

Avoid setting heap equal to container limit. Preserve reserve and test burst, startup, compaction, large payload, profiling, and shutdown. Observe OOM kills and application allocation separately.

Native runtimes need allocator/fragmentation and sanitizer considerations; interpreted runtimes may need worker-process rather than thread behavior. Baseline documentation explains per-ecosystem mechanisms without pretending one tuning flag is universal.

Performance defaults are hypotheses. Record benchmark hardware/limits, workload/data, version, warmup, sample distribution, and confidence; validate canaries in real environments.

### Handle dependencies as a continuous fleet problem

Use approved registries/proxies, namespace controls, integrity verification, lock files, review, and dependency minimization. Defend against confusion, typosquatting, compromised maintainers, malicious install scripts, and abandoned packages.

Track direct, transitive, generated, vendored, native, OS, build-only, test, and runtime dependencies. SBOM and lock evidence should reconcile with final artifact contents; explain gaps.

Automate update proposals with changelog/advisory context, compatibility tests, risk, and rollback. Group related ecosystem updates when that improves compatibility evidence; avoid giant unauditable upgrades.

Vulnerability response maps advisory/component/version to actual artifacts and deployments, evaluates reachability/exposure, defines remediation/compensating controls, rebuilds from trusted inputs, and verifies rollout. “Base fixed” does not update already published application images.

Inventory consumers by digest and current deployment. Rebuild even unchanged application source when base/runtime dependencies need remediation; issue new immutable artifacts and provenance.

### Make telemetry a baseline interface

Provide maintained logging, metrics, trace/context, error, and profiling integrations appropriate to the language and archetype. Standardize resource/service identity and correlation while leaving domain telemetry with product teams.

Pin OpenTelemetry API/SDK/instrumentation and semantic-convention behavior. Language support and convention stability differ; validate actual emitted signals and migration rather than assuming identical feature maturity.

Default logs to structured stdout/stderr or another platform contract, with severity, timestamp, service/revision, trace correlation, and redaction. Do not log request bodies, tokens, environment dumps, or high-cardinality fields by default.

Bound buffers, exporters, retries, sampling, and shutdown flush. Telemetry must not block the service indefinitely, amplify an outage, exceed memory, or lose all terminal evidence on graceful shutdown.

Profiles and crash dumps can expose secrets and personal data. Gate collection, storage, access, retention, and deletion. Provide an approved ephemeral debugging route instead of bloating every production image.

### Define configuration and secret behavior

Configuration is typed, validated at startup or controlled reload, documented, and separated from secrets. Unknown or contradictory fields fail clearly rather than silently taking defaults.

Accept secret references/delivery through the platform; do not bake values into source, layers, SBOM, provenance, config files, command arguments, or broad environment diagnostics.

Define reload versus restart for config, credentials, certificates, trust stores, and feature flags. Watchers, signal handlers, polling, and SDK refresh have different failure modes and platform dependencies.

Record effective non-secret configuration revision in status/telemetry. Secret values and sensitive topology remain excluded; presence/version may be exposed through safe identifiers.

Test missing, malformed, expired, rotated, revoked, and permission-denied inputs plus provider outage. Startup success from cached credentials must not conceal imminent expiry.

### Test the complete matrix

Test source layout/generation, lock resolution, clean/offline build where intended, reproducibility checks, SBOM/provenance/signature, layer content, architecture, admission, and registry promotion.

Runtime tests cover non-root/read-only filesystem, writable paths, PID/signals/children, startup/readiness/liveness, graceful and forced shutdown, exit codes, cgroup memory/CPU, thread/pool limits, temp storage, clock/locale/timezone, DNS/TLS/proxy, configuration/secrets, telemetry, and network policy.

Archetype integration tests exercise request overload/drain, consumer duplicate/rebalance, job retry/result, and stateful identity/recovery as applicable. Test real provider boundaries, not only mocked libraries.

Performance tests cover cold/warm startup, throughput, tail latency, allocation/GC, memory total, CPU throttling, native behavior, payload/data distributions, and downstream saturation. Record regressions with thresholds and variance.

Upgrade tests cover supported predecessor paths, dependency/schema/config/telemetry compatibility, canary, rollback boundary, and emergency rebuild. Retirement tests prove old builders/images/admission cannot create new consumers after removal.

### Verify current conformance

Conformance evaluates source/build config, current toolchain and dependencies, artifact digest/evidence, runtime profile, deployed configuration, security policy, telemetry, ownership, support channel, update state, and exception expiry.

An image initially generated from baseline revision 3 may drift through copied workflows, disabled updates, base rebuilds, runtime flags, or untracked dependencies. Origin is useful provenance, not compliance.

Continuously inventory deployed artifact digests and compare with registry/provenance/SBOM/advisory data. Find untracked workloads, mutable tags, unsupported architectures, missing owners, and expired versions.

Offer brownfield assessment and migration that can adopt build, artifact, deployment, telemetry, or dependency capabilities incrementally. Do not require destructive repository regeneration.

Report conformance age and evidence limitations. A scan from six months ago cannot support today’s vulnerability or runtime-lifecycle claim.

### Govern exceptions

An exception identifies owner, exact unsupported tuple, business need, risk, affected environments/data, compensating controls, tests, monitoring, incident/support path, cost, expiry, and removal/migration trigger.

Isolate unsupported builders, registries, images, runtime classes, or privileges from the normal trusted path. Do not let one exception broaden every team’s parameter schema.

Exceptions cannot manufacture expertise. High-risk production runtimes without on-call, patch source, recovery, or diagnostic capability may need rejection regardless of compensating controls.

Review exceptions on change and before expiry. Repeated demand with evidence may justify a new supported profile; repeated unowned bypasses justify stronger admission.

Emergency exceptions are narrower and shorter, with incident authority and retrospective. They are not a shortcut around baseline product work.

### Upgrade and deprecate the installed fleet

Publish release cadence, compatibility window, migration guides, automated proposals, test evidence, security impact, deadline, support, and exception route. Prioritize security/end-of-support and high-exposure workloads.

Use adapters or dual-compatible common libraries when runtime upgrades change APIs, telemetry, TLS, packaging, or base behavior. Avoid hiding breaking changes behind a base tag that moves underneath consumers.

Canary baseline changes on platform-owned fixtures and willing workloads by archetype, architecture, and resource profile. Observe build success, artifact diff, startup, behavior, performance, telemetry, and rollback.

Track migrations to terminal deployed conformance, not merged pull request. A repository can merge an upgrade and fail to release or retain old replicas.

Escalate before deadline with accountable owners. Stop new deployment/admission of deprecated artifacts where policy permits while preserving controlled recovery and rollback during the evidence window.

### Retire every runtime surface

Retirement requires no admitted consumers or valid exceptions, no active builds/releases, and a deliberate decision for historical recovery. Preserve source/lock/provenance/SBOM/evidence as policy requires.

Remove template/profile discovery, new-admission rules, builders/actions, toolchain distributions, base images/tags, signing identities, registry permissions, package proxy rules, caches, test fixtures, telemetry adapters, dashboards, docs, and support rotations in dependency order.

Do not delete artifacts still required for rollback, incident forensics, reproducible legal release, or disaster recovery. Quarantine them from new deployment and define retention/access.

Revoke credentials and network paths after final migration/recovery needs. Verify negative tests: old runtime tuple cannot enter build, promotion, or deployment through an unguarded path.

Record a retirement tombstone with baseline/revisions, consumer inventory result, evidence disposition, remaining historical artifacts, owner, date, and restoration prohibition or controlled route.

### Operate baselines as products

Catalog baselines, profiles, channels, versions, owners, component matrices, consumers, exceptions, CVEs/advisories, build evidence, SLOs, costs, incidents, migration, and retirement.

Measure time to first verified deployment, build/rebuild success, supply-chain evidence completeness, runtime conformance, vulnerability remediation, upgrade lead time, fleet currency, performance regression, incident recovery, user effort, exception age, and retirement completion.

Adoption alone can reward easy but unsafe paths. Balance usage with terminal outcomes, security, reliability, performance, support load, and migration health.

The following executable inventory is synthetic review evidence. It counts declared controls and does not prove build reproducibility, artifact safety, dependency completeness, vulnerability absence, runtime portability, performance, telemetry correctness, migration safety, or production reliability.

<!-- bijux-verify: {"id":"runtime-baseline-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baselines 10\ncompatibility_bounded 10\nbuild_traceable 9\nartifact_evidence 9\nruntime_contract 9\nresource_bounded 8\nsecurity_defaults 9\ntelemetry_supported 8\nupgrade_brownfield 8\nretirement_owned 8\n","stderr":""}} -->
```python
baselines = [
    ("request-managed-a", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("request-native-b", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("event-managed-a", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("event-native-b", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("batch-managed-c", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("batch-native-b", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("stateful-managed-a", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("legacy-interpreter", 1, 1, 1, 1, 0, 1, 1, 1, 0),
    ("specialized-compiler", 1, 1, 1, 1, 1, 1, 0, 0, 1),
    ("experimental-runtime", 1, 0, 0, 0, 0, 0, 0, 0, 0),
]
fields = [
    "compatibility_bounded", "build_traceable", "artifact_evidence",
    "runtime_contract", "resource_bounded", "security_defaults",
    "telemetry_supported", "upgrade_brownfield", "retirement_owned",
]
print("baselines", len(baselines))
for index, field in enumerate(fields, start=1):
    print(field, sum(row[index] for row in baselines))
```

## Definitions and Notation

Let compatibility tuple $x=(l,t,d,i,a,w,p)$ contain language/runtime revision $l$, toolchain $t$, dependency state $d$, artifact/image $i$, architecture $a$, workload profile $w$, and policy revision $p$. Baseline $b$ supports set $E_b$; $x\in E_b$ is necessary but current conformance evidence is also required.

For $k$ compatibility dimensions with supported cardinalities $n_i$, naive exhaustive combinations total $N=\prod_{i=1}^{k}n_i$. Reduction through fixed defaults or equivalence assumptions must be documented and tested at interaction boundaries.

Let memory limit $M$, fixed runtime/native overhead $H$, per-concurrent-operation memory $m$, concurrency $c$, and reserve $R$ require $H+cm+R\leq M$ as a feasibility budget. Measurements determine distributions and safe reserve.

For stable average arrival rate $\lambda$, average time in system $W$, and average in-system concurrency $L$, Little’s Law gives $L=\lambda W$. It is an observation relation under stability, not an overload-control policy.

Let baseline lifecycle state $z\in\{recommended,supported,maintenance,experimental,deprecated,retired\}$ map to admission, security response, migration, and deadline rules. State alone is incomplete without dates, owners, consumers, and evidence.

## Mechanisms, Invariants, or Proof Structure

The runtime-baseline assurance chain is:

1. derive terminal support outcomes from a workload archetype, user cohort, installed fleet, and explicit non-guarantees;
2. specify a versioned compatibility envelope, ownership, support channels/dates, customization, evidence, exception, and retirement;
3. pin source/toolchain/dependency/build inputs, isolate least-privilege builds, prevent secret persistence, and record operation identity;
4. produce immutable OCI artifacts with inspected layers/config, architecture-specific tests, SBOM, provenance, signatures/attestations, scans, and policy verification;
5. enforce process, signal, shutdown, health, filesystem, privilege, clock, DNS/TLS, configuration/secret, resource, concurrency, and telemetry contracts;
6. validate every supported archetype/architecture interaction through build, security, integration, failure, performance, upgrade, rollback, and emergency-rebuild tests;
7. continuously map evidence and advisories to exact deployed digests, current owners, support state, and exception expiry;
8. update new and brownfield consumers through maintained dependencies/workflows and reviewable, terminally verified migrations;
9. stop new admission before support ends, canary replacements, constrain exceptions, and retain controlled recovery during transition; and
10. remove builders, images, authority, caches, tooling, telemetry, and docs after consumer/evidence obligations are resolved and negative admission passes.

The combination-count argument proves only that naive exhaustive testing can grow multiplicatively. Pairwise or risk-based tests reduce cost but do not logically prove all higher-order interactions. The platform must narrow the envelope and explicitly label residual evidence limits.

The invariants are archetype-derived support, immutable resolution, end-to-end traceability, controlled build, honest reproducibility, layered artifact evidence, portable process behavior, least privilege, resource bounds, fleet-wide dependency/telemetry updates, complete matrix testing, early deprecation, and bounded exceptions.

## Alternatives and Trade-Offs

**One baseline per language versus per archetype profile:** language-only products reduce count but hide behavioral differences. Profiles share one runtime core while adding tested request, consumer, batch, or stateful contracts.

**Broad matrix versus narrow paved set:** breadth serves more teams but multiplies test/support/security load. A narrow set improves evidence while requiring a fair exception and adoption process.

**Source builds versus upstream binaries:** source builds increase control and reproducibility potential but add compiler and patch burden. Verified upstream artifacts reduce toil while extending trust dependencies.

**Full OS versus minimal/distroless base:** full images ease debugging and compatibility but add packages/exposure. Minimal images reduce surface but require deliberate certificates, timezone data, diagnostics, and emergency tooling.

**Static versus dynamic linking:** static artifacts simplify runtime dependencies but can duplicate vulnerable libraries and complicate patching/licensing. Dynamic linking centralizes some updates but adds ABI/runtime dependencies.

**Single architecture versus multi-platform index:** one architecture narrows testing and operations. Multiple architectures improve placement/cost options while duplicating native build, dependency, performance, and incident evidence.

**Hermetic/offline versus networked build:** hermetic inputs improve repeatability and supply-chain control. Networked resolution is simpler and fresher but can change, disappear, or be compromised; controlled proxies bridge some trade-offs.

**Automatic versus reviewable updates:** automation shortens exposure and toil but can mass-break consumers. Reviewable proposals preserve ownership while deadlines and escalation prevent indefinite deferral.

**Runtime auto-tuning versus explicit profile defaults:** auto-tuning adapts to resources but can change across versions and misread containers. Explicit bounds are predictable but need maintenance and workload measurement.

**Built-in diagnostics versus ephemeral debugging:** bundled tools help incidents but enlarge images and attack surface. Ephemeral signed tools preserve minimal runtime while depending on operational access and training.

**In-place major upgrade versus parallel migration:** in-place is cheaper but couples rollback to data/config changes. Parallel environments enable comparison and fallback at additional capacity and routing complexity.

**Extended exception versus platform adoption:** exception avoids central support cost for rare needs but leaves team risk. Repeated demand may justify a supported baseline only after ownership and evidence exist.

## Failure Modes and Misconceptions

- **“Supporting a language means allowing its image.”** support spans build, execution, operations, updates, and retirement.
- **“LTS means the platform supports it.”** upstream lifecycle and platform qualification are separate.
- **“A container is portable.”** architecture, kernel, resources, filesystems, clocks, DNS, TLS, and dependencies remain.
- **“Pinned application dependencies make builds reproducible.”** builders, plugins, system packages, clocks, and instructions also matter.
- **“A tag identifies bytes.”** tags can move; digests identify content.
- **“Rebuilding the same version is harmless.”** changed bytes need new immutable identity and evidence.
- **“A signature proves a trusted build.”** it authenticates a signer under policy; provenance and verification describe production.
- **“An SBOM proves no vulnerabilities.”** inventory can be incomplete and says nothing alone about exploitability or malicious logic.
- **“A clean scanner means safe.”** databases, detection, configuration, and scope are incomplete.
- **“Minimal means remove certificates and timezone data.”** required runtime correctness remains part of minimality.
- **“PID 1 receives signals normally.”** wrappers and process trees can change signal/reaping behavior.
- **“Read-only root means the app needs no writable state.”** temporary/cache/socket/dump paths need explicit contracts.
- **“The runtime sees container memory.”** verify cgroup awareness for each revision and configuration.
- **“Heap equals memory.”** native, stack, JIT, buffers, page cache, sidecars, and diagnostics consume more.
- **“More worker threads improve throughput.”** memory, CPU, downstream capacity, and contention bound concurrency.
- **“Telemetry libraries are behavior-neutral.”** instrumentation changes context, memory, latency, cardinality, and emitted semantics.
- **“Merged upgrade means migrated.”** deployed digest and terminal conformance determine completion.
- **“Exceptions are support.”** they are bounded deviations with explicit reduced guarantees.
- **“Deleting the template retires a runtime.”** builders, images, workloads, caches, credentials, and recovery remain.
- **“Generated-from proves compliant.”** current artifact and runtime evidence, not ancestry, determines conformance.

## Worked Examples

### Example 1

A matrix supports four languages, three versions, two architectures, five profiles, and two bases: $4\cdot3\cdot2\cdot5\cdot2=240$ tuples before frameworks. Choosing one recommended base per language line and admitting only evidenced profile/architecture pairs cuts the matrix. Conclusion: explicit narrowing is a support mechanism, not arbitrary restriction.

### Example 2

A service pins packages but downloads `builder:latest`. A compiler update changes generated code while the application tag stays `1.4.0`. Pinning builder/action/base digests and issuing a new artifact identity exposes the change. Conclusion: source locks do not lock the build system.

### Example 3

An image has a valid signature from a broad CI key but no subject/source provenance; an attacker used the key to sign arbitrary bytes. Admission requires protected workload identity, expected builder, subject digest, source revision, parameters, SBOM, and tests. Conclusion: signature and provenance answer different trust questions.

### Example 4

A shell entrypoint launches the server without `exec`; termination reaches the shell, not the child. Kubernetes kills it after grace while requests remain partial. An exec-form launcher forwards signals, marks readiness false, drains, flushes bounded evidence, and exits. Conclusion: container process semantics are part of the runtime baseline.

### Example 5

A container has $M=1024$ MiB, fixed/native overhead $H=280$ MiB, reserve $R=200$ MiB, and measured per-request memory $m=8$ MiB. The budget gives $c\leq(1024-280-200)/8=68$. A default concurrency of 200 is infeasible before tail variance. Conclusion: concurrency must respect total memory, not heap or CPU alone.

### Example 6

At stable load $\lambda=80$ requests/s and mean time $W=0.25$ seconds, Little’s Law predicts average $L=20$ in-system requests. Observed average concurrency 75 reveals hidden queueing/retry or measurement mismatch. Conclusion: simple invariants can diagnose baseline behavior, but tail objectives still need distributions.

### Example 7

One multi-platform tag contains `amd64` and `arm64`, but a native compression dependency exists only for `amd64`; `arm64` silently uses a slow fallback and misses deadlines. Per-manifest dependency and performance tests catch it before index promotion. Conclusion: a multi-platform index is routing metadata, not behavioral equivalence.

### Example 8

A critical base-library advisory is fixed in the base registry. Hundreds of existing application images still contain the old layer. Digest inventory maps affected deployments, trusted rebuild produces new immutable artifacts/provenance, canaries validate behavior, and rollout is tracked to terminal state. Conclusion: fixing the source base does not remediate the fleet.

### Example 9

An OpenTelemetry instrumentation update changes attributes and doubles memory from high-cardinality labels. Treating it as a baseline change triggers semantic compatibility, redaction, cardinality, performance, and dashboard tests before canary. Conclusion: telemetry is runtime behavior, not decoration.

### Example 10

After a language line is retired, its builder still runs from an old workflow, registry tags remain deployable, a signing credential exists, two exceptions expired, and disaster-recovery docs recreate it. Negative admission, inventory, credential revocation, artifact quarantine, recovery decision, and tombstone complete retirement. Conclusion: removing discovery is only the first lifecycle step.

## Cross-Program Connections

- **Programming languages:** compilation, interpretation, type/runtime systems, ABI, memory management, concurrency, and package semantics define baseline differences.
- **Operating systems:** processes, PID 1, signals, filesystems, privileges, clocks, resource accounting, and architectures shape container behavior.
- **Software engineering:** dependency management, semantic compatibility, testing, code generation, ownership, and maintainability govern evolution.
- **Security engineering:** least privilege, supply-chain trust, vulnerability response, secrets, signatures, provenance, and artifact admission constrain risk.
- **API and service engineering:** deadlines, cancellation, health, graceful drain, idempotency, telemetry, and versioning turn runtime mechanics into service contracts.
- **Distributed systems:** partial failure, retries, clocks, DNS, connection refresh, and rollout compatibility explain why container portability is bounded.
- **Reliability engineering:** resource budgets, overload, tail latency, canaries, rollback, fleet currency, and incident response validate support outcomes.
- **Data engineering:** native dependencies, batch profiles, schema/data compatibility, and reproducible processing connect runtime state to pipeline correctness.
- **Systems engineering:** compatibility matrices, configuration control, assurance evidence, lifecycle gates, and retirement prevent unsupported complexity from hiding.
- **Economics and governance:** support breadth, build capacity, architecture choice, maintenance debt, exception cost, license policy, and end-of-life allocate organizational effort.

## References

1. Open Container Initiative, “OCI Image Format Specification,” version 1.1.1, March 2026. https://github.com/opencontainers/image-spec/releases/tag/v1.1.1
2. Open Container Initiative, “OCI Runtime Specification,” current releases, retrieved 2026-09-02. https://github.com/opencontainers/runtime-spec/releases
3. SLSA, “Supply-chain Levels for Software Artifacts Specification,” version 1.2, retrieved 2026-09-02. https://slsa.dev/spec/v1.2/
4. NIST, “Secure Software Development Framework (SSDF) Version 1.1,” SP 800-218, February 2022. https://csrc.nist.gov/pubs/sp/800/218/final
5. Reproducible Builds Project, “Definitions,” current documentation, retrieved 2026-09-02. https://reproducible-builds.org/docs/definition/
6. OpenSSF, “OpenSSF Scorecard,” current project documentation, retrieved 2026-09-02. https://scorecard.dev/
7. SPDX Workgroup, “SPDX Specification,” version 3.0.1, April 2025. https://spdx.github.io/spdx-spec/v3.0.1/
8. OWASP Foundation, “CycloneDX Specification,” version 1.6, retrieved 2026-09-02. https://cyclonedx.org/specification/overview/
9. OpenTelemetry Authors, “Language APIs and SDKs,” current documentation, retrieved 2026-09-02. https://opentelemetry.io/docs/languages/
10. Kubernetes Authors, “Pod Security Standards,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/pod-security-standards/
11. Kubernetes Authors, “Resource Management for Pods and Containers,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
12. Semantic Versioning, “Semantic Versioning 2.0.0,” June 2013. https://semver.org/spec/v2.0.0.html
13. CNCF Platforms Working Group, “Platforms White Paper,” April 2023. https://tag-app-delivery.cncf.io/whitepapers/platforms/

## Exercises

### Exercise 1

Define runtime baseline, runtime profile, support channel, compatibility matrix, toolchain lock, base image, SBOM, provenance, current conformance, and runtime exception. For each, give one adjacent concept it must not be confused with.

### Exercise 2

A platform proposes five languages, three active releases each, two package managers, two bases, two architectures, and four archetypes. Calculate the naive combinations, then design an evidence-backed matrix reduction without silently claiming compatibility for omitted interactions.

### Exercise 3

A baseline uses mutable builders/tags, downloads dependencies from the internet, embeds registry credentials, signs with a shared key, creates no provenance, runs as root, writes everywhere, ignores signals/cgroups, sets heap equal to memory limit, uses unbounded pools, logs environment variables, and lacks migration. Diagnose at least twenty defects and correct them.

### Exercise 4

Design a runtime-baseline portfolio for request services, event consumers, batch jobs, and stateful operators across managed/interpreted and native/compiled ecosystems on two architectures. Define shared contracts, profile differences, build/evidence, security, resources, telemetry, tests, support channels, brownfield migration, and exception boundaries.

### Exercise 5

A language runtime and telemetry library are compromised while the base image certificate bundle is also expiring; 300 services span supported, maintenance, and expired-exception states, and recovery archives contain old images. Produce a containment, inventory, rebuild, verification, rollout, migration, evidence-retention, and retirement sequence.

## Answers to the Exercises

### Answer 1

A runtime baseline is a maintained compatibility/lifecycle envelope and differs from a language allowlist. A runtime profile specializes archetype behavior and differs from a team fork. A support channel maps lifecycle state to concrete guarantees/deadlines and differs from upstream marketing. A compatibility matrix records evidenced tuples and differs from all combinations a template can render. A toolchain lock identifies complete build inputs and differs from only an application dependency lock. A base image is governed lower artifact/config and differs from an arbitrary tag. An SBOM inventories components/relationships and differs from a security verdict. Provenance describes artifact production and differs from a signature alone. Current conformance evaluates present source/artifact/runtime evidence and differs from generation ancestry. A runtime exception is an expiring owned deviation with compensating controls and differs from ordinary support.

### Answer 2

Naive combinations are $5\cdot3\cdot2\cdot2\cdot2\cdot4=480$. Do not announce support for 480. Select one recommended package manager and base per language release unless a second combination has a demonstrated user/semantic need. Qualify only runtime releases inside platform support windows. Define a shared runtime-core contract plus archetype profiles rather than four independent image families. Test both architectures for native runtimes/extensions; bytecode-only paths may reuse some evidence only after architecture-sensitive OS/native/TLS behavior is checked. Publish the exact admitted tuple set and mark other tuples unsupported/experimental. Use representative interaction tests for shared pure components, targeted tests for native ABI, GC/JIT, signal, filesystem, telemetry, and performance, and full end-to-end fixtures for every admitted archetype/profile. Track the rationale and residual risk of any equivalence assumption. Remove obsolete combinations as consumers migrate. Matrix reduction is a product decision backed by demand, ownership, and evidence—not an assertion that omitted tests would pass.

### Answer 3

Mutable builders and tags make outputs untraceable; pin source, builder/action, base, and deployment digests and issue immutable identities. Uncontrolled internet resolution changes/disappears and enables dependency confusion; use locks, hashes, approved proxies, egress policy, and captured inputs. Embedded credentials leak through layers/cache/history/logs; use ephemeral brokered build secrets and inspect outputs. A shared signing key cannot strongly identify expected workload/builder and may sign arbitrary bytes; use protected workload identity, provenance with subject/source/builder/parameters, independent admission verification, and scoped revocation. Missing provenance hides production context; generate and bind it with SBOM/scans/tests. Root and broad writable filesystem violate least privilege; set non-root UID/GID, drop capabilities/escalation, seccomp, read-only root, and explicit bounded writable paths. Ignoring signals causes forced partial termination; use exec/verified init, readiness withdrawal, drain, flush, and exit budget. Ignoring cgroups sizes threads/GC/memory from host; verify runtime container awareness and set bounded profile defaults. Heap equal to limit omits native/stacks/JIT/buffers/page cache/telemetry; reserve and measure total memory. Unbounded pools/queues exhaust memory/downstreams; cap concurrency, connections, retries, and buffers with backpressure. Environment logging exposes secrets/topology; structured redacted telemetry uses safe fields and cardinality. Missing migration strands vulnerabilities; inventory brownfield consumers, publish channels/dates, automate tested proposals, canary, verify deployed conformance, constrain exceptions, and retire builders/images/credentials/caches. Further corrections include architecture-specific tests, reproducibility checks, certificate/timezone/DNS behavior, vulnerability/license response, health, performance, rollback, emergency rebuild, ownership/support, and negative retirement admission.

### Answer 4

Create shared contracts for immutable source/toolchain/dependency resolution, OCI artifact identity, SBOM/provenance/signature/scans, non-root/read-only execution, signals/shutdown, configuration/secrets, cgroup resources, DNS/TLS/time, telemetry, ownership, channels, conformance, exceptions, and retirement. Managed/interpreted and native/compiled runtime cores have ecosystem-owned adapters; the latter adds compiler/linker/ABI/cross-architecture and static/dynamic library evidence, while managed runtimes add interpreter/JIT/GC/heap/native-extension evidence. Request profiles test startup, readiness, deadline, bounded concurrency, overload and drain. Event profiles test lease/ack/rebalance/backpressure. Batch profiles test terminal exit, retry, checkpoint/result. Stateful operator profiles test stable identity, membership-aware shutdown/upgrade, recovery, and privileged operator controls. Build and test each admitted architecture manifest before index promotion, especially native dependencies and performance. Channels publish recommended/supported/maintenance/deprecated dates, upstream relationship, response, and migration. Brownfield assessment adopts builds, artifacts, telemetry, or deployment incrementally and tracks actual deployed digests. Exceptions isolate exact unsupported tuples with owner, controls, tests, expiry, and migration; arbitrary base, builder shell, secret values, privileges, or architecture remain outside the supported form.

### Answer 5

Pause affected baseline promotion and new deployments while preserving read-only inventory/evidence and safe unaffected operation. Identify compromised runtime/toolchain and telemetry revisions, builders, base/certificate revisions, source, provenance subjects, SBOMs, registry digests, deployed replicas/jobs, environments, owners, channels, exceptions, credentials, and recovery archives. Revoke compromised signing/build/registry authority, rotate trust roots and workload credentials, isolate suspect artifacts, and retain forensic evidence without broad secret exposure. Establish new trusted source/toolchain/builder roots; pin a valid certificate bundle; remove or replace compromised instrumentation; rebuild every affected application from reviewed source and locked inputs even if its code is unchanged. Generate new immutable digests, SBOM/provenance/attestations and independently verify architecture, layers, TLS, process/security/resource behavior, telemetry redaction/cardinality, application tests, and vulnerability findings. Canary by archetype/architecture/risk, compare behavior/performance/telemetry, then roll out with terminal deployed-digest tracking and rollback only to artifacts proven outside the compromise. Maintenance consumers receive the same risk-based response; expired exceptions do not bypass containment—owners migrate immediately or service is isolated/stopped under incident authority. Recovery archives retain quarantined old artifacts only if required, marked non-deployable with controlled restoration and compensating reconstruction instructions; otherwise delete by policy. After coverage proves no active affected digest, remove old builders/bases/actions/caches, revoke identities, close exceptions, run negative admission, preserve incident/provenance/migration evidence, and record retirement tombstones.
