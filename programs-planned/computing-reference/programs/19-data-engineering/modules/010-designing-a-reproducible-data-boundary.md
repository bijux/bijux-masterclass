---
module_id: DE-010
program: Data Engineering
level: 1
module_number: 10
title: Designing a Reproducible Data Boundary
status: complete
last_verified: 2026-09-02
---

# Designing a Reproducible Data Boundary

## One-Page Review

### Governing question

How should a data engineer design a boundary so that an independent operator can identify the exact inputs, reconstruct the governed execution, compare outputs under a declared equivalence and explain any difference?

### Essential definitions

- A **data boundary** is an owned interface where data is admitted, interpreted, validated, transformed and published under an explicit contract.
- **Determinism** means the declared output is a function of the declared inputs and controlled context; repeating that context selects the same result under the chosen equivalence.
- **Repeatability** is obtaining the declared result again under the same operator and environment. **Reproducibility** additionally makes the reconstruction possible from an independently provisioned conforming environment.
- A **snapshot** is an immutable, bounded view of source data with identity, scope and consistency semantics.
- A **manifest** enumerates inputs, schemas, code, dependencies, configuration, execution context, outputs and digests required to verify a run.
- **Provenance** records entities, activities and responsible agents or systems that produced an artifact. Provenance explains lineage; it does not by itself prove correctness or reproducibility.
- A **content digest** identifies a particular byte sequence under a named hash algorithm. It does not identify semantic content unless serialization is fixed.
- **Canonicalization** maps allowed equivalent representations to one defined byte representation before comparison or signing.
- A **replay** executes the declared transformation again from retained inputs and context.
- An **equivalence relation** defines success: byte identity, canonical semantic equality, ordered-record equality, set/multiset equality or a justified numerical tolerance.
- A **hidden input** is any undeclared influence on output, such as current time, mutable network state, locale, filesystem order, implicit default, random generator, thread schedule or unpinned dependency.
- An **attestation** is a signed or otherwise authenticated statement about artifacts and their production. Authentication strengthens trust in a claim but does not make the transformation correct.

### Central model, mechanism, or theorem

Model a boundary run as

$$
Y=F(X,S,C,E,N),
$$

where $X$ is input bytes/snapshots, $S$ schemas and interpretation rules, $C$ code and configuration, $E$ execution environment, and $N$ explicitly modeled nondeterministic choices. A run record is

$$
M=(id_X,id_S,id_C,id_E,N,id_Y,Q,P),
$$

with content identities, output equivalence $Q$ and provenance $P$.

Reproducibility is not “the job succeeded twice.” An independent replay must resolve every identifier, execute the declared procedure and establish $Y'\sim_Q Y$. If an unrecorded hidden input $h$ can change the result, the recorded manifest cannot uniquely determine the expected output.

### Critical invariants

- Every consumed byte is immutable, content-identified or captured into a declared consistent snapshot.
- Schema, encoding, logical types, null/time policy and parser behavior are versioned with the input.
- Code, dependencies, configuration, feature flags, query text and environment are resolved to immutable identities.
- Current time, randomness, locale, timezone, concurrency, file/map order and external services are eliminated, injected or recorded at the correct semantic level.
- Record order is either semantically irrelevant or produced by a total order with a deterministic tie-breaker.
- Output equivalence and tolerances are declared before replay; a loose post-hoc comparison cannot rescue a failed claim.
- Digests name exact bytes and always record algorithm, canonicalization and object scope.
- The manifest and provenance are stored separately from mutable logs and are themselves schema-versioned, integrity-protected and retained.
- Secrets, personal data and credentials are referenced safely rather than leaked into evidence packages.
- A clean-room replay starts without unrecorded caches and verifies resolved inputs before executing.
- Differences are localized to input, schema, code, configuration, environment, nondeterministic choice or comparator rather than overwritten.
- Reproducibility claims state their boundary, retention horizon, platform assumptions and limitations.

### Common failures

Calling a retry a reproduction; naming an input by `latest`; retaining a query but not its snapshot/isolation semantics; hashing a mutable path; hashing parsed objects without canonical bytes; assuming JSON key order or whitespace is irrelevant to byte digests; pinning application code but not dependencies; capturing a container tag rather than image digest; recording a random seed without generator/version/partitioning; depending on filesystem or map order; using current time or implicit timezone; performing parallel floating reductions and expecting identical low bits; sorting on a non-unique key; embedding run time or absolute paths in outputs; comparing only row counts; choosing tolerance after seeing a mismatch; treating a digest as authenticity; treating provenance as proof of correct execution; omitting rejected records; losing incremental checkpoint state; and storing credentials or sensitive rows in a public manifest.

### Compact example

Three input records arrive in different orders. A boundary validates a fixed schema, sorts by the total key `(id,event_ms)`, uses an explicit `rounding=half_even` configuration and emits a newline-delimited canonical representation. Two runs produce identical bytes and the same SHA-256 digest. Changing the configuration changes the bytes even when the rows do not. The digest is meaningful only because input order, serialization, schema and configuration are in the contract.

### Connections

[DE-001](001-data-producers-consumers-and-lifecycle.md) defines ownership and lifecycle; [DE-003](003-csv-json-and-line-oriented-formats.md) covers lexical interchange; [DE-004](004-avro-protocol-buffers-and-schema-aware-serialization.md) through [DE-007](007-compression-and-encoding-choices.md) define representations; [DE-008](008-schemas-nullability-and-type-fidelity.md) and [DE-009](009-time-time-zones-and-event-timestamps.md) preserve semantic distinctions. Supply-chain evidence connects to [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md), integrity to [Security Engineering](../../25-security-engineering/ROADMAP.md), and execution environments to [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

What evidence would let another operator reconstruct this result without relying on the original machine, mutable upstream state or undocumented knowledge?

A reproducible data boundary is a product contract plus a replay contract. It states what entered, how bytes were interpreted, what logic ran, which environment and controlled choices influenced execution, what emerged, and how equivalence is decided. It also retains enough material for that statement to remain actionable.

The [Reproducible Builds definition](https://reproducible-builds.org/docs/definition/) provides a useful analogy: given the same source, environment and instructions, another party can recreate bit-for-bit identical specified artifacts. Data pipelines add mutable sources, snapshots, semantic schemas, rejected records, ordering, external services and stateful/incremental execution. Those influences must join the perimeter.

Provenance is related but different. [W3C PROV-O](https://www.w3.org/TR/prov-o/) models entities, activities and agents so systems can exchange lineage. A provenance graph can say output `Y` was generated by activity `A` using input `X`; reproducibility additionally requires resolvable identities, executable instructions, controlled context and a comparison protocol.

The target is not universal identical behavior on every computer. Declare the supported replay environment and equivalence. A text export may require byte identity. A relational result without semantic order may require multiset equality after canonical row encoding. A numerical model may require a predeclared, domain-justified tolerance and stronger statistical checks. The claim is rigorous when its perimeter and comparator are explicit.

## Why This Matters

Data results often outlive the job that produced them. Auditors ask which source rows and rules generated a figure. Engineers need to replay a defect after upstream tables changed. Scientists need to distinguish a result difference caused by code from one caused by environment. Incident responders need to trace a compromised dependency. Consumers need to verify that a published object is the one described by its manifest.

Without input identity, rerunning the same query tomorrow uses different data. Without schema identity, the same bytes can parse differently. Without dependency identity, the same source code can behave differently. Without ordering and numerical policy, parallel execution can yield unstable bytes. Without a comparator, “same result” becomes an argument after the fact.

Reproducibility also improves ordinary operations. An immutable run identity supports idempotency, cache keys, rollback, backfill planning and differential tests. A complete manifest localizes failures. Content digests detect accidental substitution and enable efficient reuse. Clean-room replay tests expose hidden dependencies before an emergency.

However, evidence creates risk. Manifests can leak source locations, user identifiers, secrets, query literals or sensitive statistics. Retained raw snapshots increase privacy and security exposure. Reproducibility must be scoped with access control, minimization, encryption, retention and deletion obligations. “Keep everything forever” is not a responsible design.

## Prerequisites and Retrieval

Retrieve the boundary owner and consumers; business grain and semantic contract; all source systems and query/API/file inputs; snapshot consistency and isolation; source object versions, offsets or transaction positions; raw byte lengths and digests; accepted and rejected record counts; encodings, delimiters and normalization; schema IDs and exact definitions; parser/serializer names, versions and options; code repository and revision; build artifact/image digest; dependency locks and transitive resolution; transformation graph; SQL/query text and engine version; configuration and feature flags; locale, timezone and environment variables; CPU/architecture/runtime details where relevant; random algorithms, seeds and partition streams; current-time inputs; concurrency and ordering policy; floating/decimal behavior; external service responses; credentials and secret references; caches and checkpoints; output paths, media types, sizes and digests; canonicalization rules; equivalence/comparison procedure; provenance format; signature/attestation policy; storage, replication, access and retention; deletion/legal constraints; replay instructions; prior replay results; and ownership for repairing unavailable artifacts.

Distinguish mutable location from immutable identity; snapshot time from event time; query text from query result; source rows from rejected rows; raw bytes from parsed values; parsing from validation; schema ID from registry alias; code commit from built executable; image tag from image digest; direct dependency lock from complete runtime closure; configuration default from explicit value; deterministic algorithm from one successful repeat; random seed from full random stream definition; logical order from incidental iteration order; numeric tolerance from byte equality; canonicalization from pretty-printing; digest from signature; integrity from authenticity; provenance from correctness; replay from recomputation on current data; output artifact from logs/byproducts; data retention from reproducibility horizon; and a declared limitation from missing evidence.

Inspect the repository's existing execution path rather than designing an imaginary one. Capture effective configuration after default resolution, but also retain source configuration and tool versions. Verify that identifiers are resolvable from the replay environment—not merely meaningful on the original host.

## Learning Objectives

After completing this module, you should be able to:

1. define a reproducibility perimeter and output equivalence for a data boundary;
2. content-identify immutable inputs, schemas, code, environment and outputs;
3. capture consistent snapshots from files, tables, streams and external services;
4. expose and control time, randomness, locale, order, concurrency and numerical variation;
5. design a versioned manifest and provenance graph without leaking secrets;
6. distinguish canonicalization, hashing, signing, attestation and semantic comparison;
7. make batch, streaming, incremental and stateful computations replayable;
8. execute clean-room and variation-based reproducibility tests;
9. diagnose differences by layer and preserve failure evidence; and
10. operate retention, migration, access and decommissioning for replay assets.

## Core Exposition

### Define the boundary and claim

Name the incoming interface, transformation responsibility and published artifact. State which components are inside the reproducibility perimeter. A team cannot control the whole world, but it can capture an external response as an input entity and begin its claim there.

Define who should reproduce the result, on what supported platforms and for how long. A 30-day operational replay and a seven-year regulatory reconstruction have different storage and dependency requirements.

State the comparator. “Same” can mean exact bytes, same canonical record multiset, same ordered values, or domain equivalence. Avoid a claim broader than the evidence package.

### Freeze input identity

An input location is not an identity. Object-store keys can be overwritten; database tables change; URLs return new content; branches and tags move. Resolve each input to immutable bytes, a generation/version ID, a transactionally consistent snapshot or an append-log range.

Record content digest, algorithm, byte length, media type, schema and retrieval semantics. Verify the digest before replay. For multipart datasets, manifest every part and a canonical collection identity rather than hashing only a directory listing.

If the source cannot provide immutable identity, copy it into governed snapshot storage before transformation. Mark the capture boundary and its limitations.

### Capture database snapshots correctly

A SQL query alone is not a reproducible input. Store exact text, bound parameters, engine/version, session settings and a snapshot/transaction identity or materialized result.

Isolation semantics matter. Multiple reads without a consistent snapshot can observe different database states in one run. A timestamp filter does not necessarily reproduce transaction visibility, late corrections or deletes.

For long-term replay, a materialized extract with schema and digest is usually stronger than a database-specific snapshot token that expires. Balance this against sensitive-data retention.

### Bound streaming inputs

Streams need deterministic start/end positions per partition, source identity and record-byte/schema preservation. Wall-clock intervals alone can change with late arrivals and retention.

Record broker/topic identity, partition map, inclusive/exclusive offsets, transaction/isolation mode and relevant compaction/deletion behavior. Snapshot reference data used during stream processing.

For unbounded production, reproduce a finite run segment or checkpoint transition. Define input range plus initial state; otherwise the computation has no closed replay unit.

### Capture external services as inputs

An API call depends on request bytes, endpoint/version, authentication context, response, status, headers and timing. Calling it again is not replay if the service is mutable.

Record a safe request description and capture the exact response used, subject to privacy and licensing. Replace credentials with versioned secret references or redacted identities; never store bearer tokens in manifests.

If contractual restrictions prohibit response retention, state that limitation and retain the strongest permitted digest/receipt. Do not claim independent replay beyond what remains resolvable.

### Bind schemas and interpretation

The same bytes can yield different values under another encoding, delimiter, null policy, timezone or schema version. Bind exact schema content or immutable registry identity to every input/output.

Record parser and serializer implementation/version/options because specifications can permit variants and libraries contain behavior. Include malformed-input policy, coercions, rejected records and repair lineage.

Schema aliases such as “current” are mutable. Resolve them when the run starts and record the immutable version and digest.

### Identify code and build artifacts

A source revision helps review but does not fully identify executed bytes. Record repository, commit, dirty-state policy, build instructions and the actual executable/container digest.

Tags are discoverable labels, not immutable content identities. Resolve container images and packages to digests. Retain or make dependencies retrievable for the claim horizon.

SLSA [provenance](https://slsa.dev/spec/v1.2/provenance) describes verifiable information about where, when and how software artifacts were produced. Reuse established attestations where they cover the execution artifact, while extending the data-run manifest for datasets and transformation parameters.

### Close the dependency graph

Pin transitive libraries, runtimes, plugins, database extensions, native packages and model/data dependencies. A lockfile is evidence only if the resolver honors it and referenced artifacts remain available.

Record platform/architecture when output can vary. A container image does not automatically fix kernel, CPU instructions, accelerator drivers or external mounts. Include only relevant assumptions, but test that the chosen perimeter is sufficient.

Mirror or escrow dependencies needed beyond ordinary registry retention. Verify their digests at installation.

### Capture effective configuration

Record command, parameters, feature flags, environment variables, config files and defaults after resolution. Also retain the human-reviewed source configuration so effective values remain explainable.

Redact secrets without losing semantic identity. For example, record the secret name/version or a nonreversible policy-approved fingerprint, not its plaintext. If secret contents affect output, acknowledge the replay access requirement.

Separate configuration from observations. A `run_id` or output location may vary without affecting semantic output; declare excluded byproducts instead of pretending every byte is invariant.

### Control time

Calls to “now,” filesystem modification times, generated UUIDs and expiring reference data are hidden inputs. Inject a declared logical run time or capture every time-dependent value used.

Do not overwrite domain event timestamps with the fixed run time. The injected clock controls computation metadata and time-sensitive rules; source time remains input data.

Normalize timestamps only under the schema's timezone and precision contract. Generated artifact timestamps should be fixed, excluded by a documented comparator or moved to separate provenance.

### Control randomness

Record algorithm, implementation/version, seed, initialization and how streams are split across partitions/threads. A seed alone does not guarantee the same sequence across libraries, versions or parallel schedules.

Prefer counter-based or explicitly partitioned streams when parallel execution requires stable assignment. Sort or key work before deriving per-record randomness.

Distinguish pseudorandom reproducibility from security randomness. Never make credentials, nonces or cryptographic keys predictable merely to reproduce analytical output; capture safe derived evidence or exclude those byproducts.

### Control locale and timezone

Locale influences collation, number/date parsing, case conversion and formatting. Timezone influences local timestamp interpretation. Set both explicitly or eliminate their effect.

Record Unicode/locale data versions if comparison or normalization can change. Avoid host defaults. Test with a contrasting locale and timezone to reveal hidden dependency.

Keep human presentation outside canonical data representation where possible. A localized report can be a derived artifact with its own contract.

### Define deterministic order

Filesystems, object listings, maps, database rows without `ORDER BY` and parallel task completion have no reliable semantic order. If order matters to bytes or algorithms, define it.

Use a total key. Sorting only by a non-unique date leaves ties unstable. Add a stable unique tie-breaker derived from the record identity or canonical bytes. Define null, text collation, numeric and NaN order.

If order is irrelevant, compare sets or multisets under canonical row identities rather than imposing costly global sorting. Preserve multiplicity when duplicates matter.

### Address parallel and numerical variation

Associative algebra in mathematics does not imply identical finite floating-point reduction under regrouping. Parallel partitions and hardware can change low bits. Libraries may select different algorithms.

For byte-identical numerical outputs, use fixed partitioning and reduction trees, exact/decimal arithmetic where appropriate, pinned libraries and constrained hardware assumptions. Otherwise declare a domain tolerance in advance and test important invariants beyond elementwise closeness.

Tolerance must include units, absolute/relative behavior, exceptional values and aggregate constraints. It is not permission for arbitrary drift.

### Canonicalize deliberately

Equivalent structured values can have different bytes because of property order, whitespace, number formatting or Unicode representation. Hashing raw bytes distinguishes them. That may be correct for transport integrity but not semantic identity.

[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) defines a JSON Canonicalization Scheme that produces a hashable representation for a constrained JSON domain. [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949.html) defines core deterministic CBOR encoding requirements. Use a specified scheme rather than inventing “sort keys and remove spaces.”

Canonicalization has a domain and version. It does not validate business semantics, fix lossy parsing or make two different values equal. Preserve original bytes when they are evidence.

### Use digests with exact scope

A digest statement needs algorithm, encoded digest, and exact byte scope. Hash raw input, canonical representation, compressed object or manifest as distinct artifacts; never compare digests computed over different layers.

[RFC 6920](https://www.rfc-editor.org/rfc/rfc6920.html) specifies ways to name digital objects using hash outputs. Content addressing makes immutable lookup and substitution detection practical.

A digest is not proof of origin by itself. An attacker can replace both object and unauthenticated manifest. Sign or attest the manifest when authenticity is required and protect keys/builders accordingly.

### Design the run manifest

Give the manifest a schema version and stable run ID derived from immutable intent where possible. Include:

- boundary and transformation identity;
- input resources with digests, sizes, schemas and ranges;
- code/build/dependency identities;
- effective configuration and controlled nondeterminism;
- environment assumptions;
- output artifacts and digests;
- comparator/equivalence contract;
- provenance references, timestamps and responsible system;
- validation, rejection and reconciliation summaries;
- retention, access and known limitations.

Canonicalize and digest the manifest. Keep operational logs as referenced byproducts rather than mixing mutable log streams into the identity.

### Represent provenance

Model inputs and outputs as entities, execution as an activity and responsible service/operator as an agent. Link generated outputs to used inputs and the activity. Assign stable identifiers.

Record derived datasets through multiple runs as a graph, not a single free-text lineage field. Preserve schema and code identities on edges or activities.

Provenance supports traceability and trust assessment. It does not establish that inputs were truthful, logic was correct, or an agent was authorized; those require validation and authenticated policy evidence.

### Preserve rejected and side-output evidence

Two runs are not equivalent if one silently drops more invalid rows even when successful outputs match. Record counts and reason categories for accepted, rejected, coerced, duplicated and late records.

Retain quarantined raw data according to access/retention policy or at least immutable identities and authorized reconstruction references. Version error taxonomies.

Logs, metrics, profiles and rejected rows can be byproducts necessary for diagnosis without being primary reproducible outputs. Name that distinction.

### Make incremental computation replayable

An incremental run depends on prior state. Identify the initial checkpoint/state artifact plus the bounded new inputs. Record state format/schema, watermarks, offsets and deduplication keys.

Checkpoint files are inputs to the next transition and need digests. A replay from raw history may use a different procedure from replay of a checkpoint transition; document both and compare their results.

Compaction, late-data revisions and tombstones must be included. Retaining only current rows can make historical outputs unreconstructable.

### Handle caches and retries

Caches may conceal undeclared network access or reuse stale results. Clean-room replay starts with empty caches or verifies every cached artifact by immutable identity.

Use a run-intent identity as an idempotency key when the same inputs/configuration should yield one published artifact. Retrying should not generate duplicate externally visible effects.

Separate pure transformation from publication. Stage outputs, verify them, then atomically publish or reference them by content identity.

### Define comparison protocols

Byte comparison is simple and strong when serialization is deterministic. For semantic comparison, specify parsing, canonicalization, order/multiplicity, null/NaN treatment, type/precision and tolerance.

Compare more than row count: schema, accepted/rejected counts, keys, column digests, distributions and domain invariants. A layered comparator localizes differences.

Version the comparator and include its own executable/digest. Never change the comparator merely to make an unexpected result pass without a reviewed contract change.

### Execute clean-room replays

Provision a supported environment from the evidence package on a separate worker without original mutable caches. Resolve and digest-check all materials. Disable undeclared network access where practical.

Run the exact command with effective configuration and controlled clocks/random streams. Compare outputs and byproduct invariants. Record the replay as new provenance linked to the original manifest.

Independent operators provide stronger evidence than repeating on the same warm host, but independence must be accurately described rather than assumed.

### Vary the environment to find hidden inputs

Run tests under different timezone, locale, username, path, file listing order, partition count, CPU architecture or allowed dependency resolver state. The [Reproducible Builds testing guidance](https://reproducible-builds.org/docs/plans/) recommends varying environmental aspects to expose uncontrolled variation.

Variation tests do not require all environments to be supported. They test whether the declared perimeter matches reality. If output changes, either eliminate the influence or add it to the supported environment contract.

Keep minimal counterexamples and add them to regression fixtures.

### Diagnose mismatches by layer

First verify manifest and comparator identity. Then verify input bytes/ranges, schemas/parsers, code/build, dependencies, configuration, environment, controlled nondeterminism and outputs in order.

Use intermediate stage digests or row/partition fingerprints to localize divergence, but do not expose sensitive values. Re-run only after preserving the failed artifacts and logs.

Classify a mismatch as contract defect, missing evidence, unavailable material, implementation nondeterminism, accepted numerical variation, corrupted artifact or genuine logic change.

### Govern retention and access

Set a replay horizon based on regulatory, scientific and operational needs. Ensure schemas, code, dependencies, raw/snapshotted inputs, manifests, keys/attestations and comparators survive that horizon.

Apply encryption, access control, audit logging, residency and deletion policies. A right-to-delete or license expiry may intentionally end full reproducibility; record the limitation and preserve non-sensitive proof where permitted.

Test restoration. A catalog entry pointing to an expired object does not satisfy the contract.

## Definitions and Notation

Let the governed transformation be

$$
F:X\times S\times C\times E\times N\rightarrow Y,
$$

where $X$ is input material, $S$ schema/interpretation, $C$ code/configuration, $E$ environment and $N$ controlled nondeterministic choices. The run manifest $M$ holds immutable identifiers for those components plus output identity, comparator $Q$ and provenance $P$.

For digest algorithm $H$ and exact byte string $b$, content identity is $id_H(b)=(H,H(b),|b|)$. Length is not cryptographic evidence but helps catch scope/transfer mistakes. Hashing another serialization $b'$ identifies $b'$, even if $b$ and $b'$ parse to equivalent objects.

Define output equivalence $\sim_Q$. Byte identity uses $y'=y$. Canonical equivalence uses $canon_Q(y')=canon_Q(y)$. Multiset equivalence compares counts of canonical row identities. Approximate numerical equivalence must define, for example,

$$
|a-b|\leq \epsilon_{abs}+\epsilon_{rel}|b|,
$$

plus policies for units, zero, NaN, infinity, shape and aggregate invariants.

For ordered parallel work, a total key $k(r)$ satisfies comparability and uses a stable tie-breaker so distinct records do not remain arbitrarily tied. For stateful replay, transition $Y_t=G(Y_{t-1},X_t,C)$ requires identities for both $Y_{t-1}$ and bounded increment $X_t$.

## Mechanisms, Invariants, or Proof Structure

Use this mechanism to establish a reproducible boundary:

1. Name the boundary, owner, consumers, output and replay horizon.
2. Declare byte, semantic, multiset or tolerance-based output equivalence.
3. Resolve every file, table, stream and external response to a bounded snapshot.
4. Digest exact input bytes and bind schemas, parsers and validation policy.
5. Identify source revision, executed artifact and complete dependency closure.
6. Capture effective configuration, queries, parameters and feature flags.
7. Eliminate, inject or record time, randomness, locale, timezone and external state.
8. Define total ordering, partitioning, concurrency and numerical reduction rules.
9. Identify incremental state, checkpoints, offsets, tombstones and late revisions.
10. Stage outputs and record type, schema, size, digest and rejected/byproduct summaries.
11. Produce schema-versioned canonical manifest and provenance relationships.
12. Protect authenticity where needed without confusing signatures with correctness.
13. Execute a clean-room replay and the declared comparison protocol.
14. Vary environmental dimensions to discover hidden inputs.
15. Preserve mismatches, localize their layer and add regression fixtures.
16. Retain, restore-test, migrate and eventually decommission evidence by policy.

The executable model gives unordered records a total order, embeds schema/configuration into deterministic bytes and digests those bytes. It demonstrates a local invariant; it does not claim that Python dictionary objects or this illustrative format form a general canonicalization standard.

<!-- bijux-verify: {"id":"reproducible-boundary-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stable_order=('a', 'b', 'c')\nsame_bytes=True\nchanged_config_changes_bytes=True\ninput_count=3\ndigest_length=64\n","stderr":""}} -->
```python
import hashlib


def render(records, rounding):
    ordered = sorted(records, key=lambda row: (row["id"], row["event_ms"]))
    lines = ("schema=orders-v1", "rounding=" + rounding)
    for row in ordered:
        line = row["id"] + "|" + str(row["event_ms"]) + "|" + str(row["amount_cents"])
        lines = lines + (line,)
    return (tuple(row["id"] for row in ordered), "\n".join(lines) + "\n")


first = (
    {"id": "c", "event_ms": 3000, "amount_cents": 125},
    {"id": "a", "event_ms": 1000, "amount_cents": 300},
    {"id": "b", "event_ms": 2000, "amount_cents": 250},
)
second = (first[1], first[2], first[0])

stable_order, bytes_a = render(first, "half_even")
_, bytes_b = render(second, "half_even")
_, bytes_c = render(second, "half_up")
digest = hashlib.sha256(bytes_a.encode("utf-8")).hexdigest()

print("stable_order=" + str(stable_order))
print("same_bytes=" + str(bytes_a == bytes_b))
print("changed_config_changes_bytes=" + str(bytes_a != bytes_c))
print("input_count=" + str(len(first)))
print("digest_length=" + str(len(digest)))
```

Critical invariants are:

- **Closure:** all output-affecting material is immutable, declared or explicitly modeled.
- **Interpretation:** schemas, parsers and semantic policies are bound to bytes.
- **Execution:** code, dependencies, configuration and environment are resolvable.
- **Choice:** time, randomness, order, concurrency and external state are controlled.
- **Identity:** each digest names an algorithm, scope and exact representation.
- **Comparison:** equivalence is predefined, executable and versioned.
- **Lineage:** provenance links input entities, execution activity and output entities.
- **Evidence:** rejected data, checkpoints and relevant byproducts are not silently lost.
- **Protection:** evidence is authentic where required and does not disclose secrets.
- **Longevity:** restore tests prove artifacts remain usable for the stated horizon.

**Proof sketch — an output-affecting hidden input prevents manifest sufficiency.** Suppose actual execution is $y=f(x,h)$, but manifest $M$ records only $x$. Assume there exist allowed hidden states $h_1,h_2$ with $f(x,h_1)\neq f(x,h_2)$. A replay procedure receiving only $M$ cannot determine whether to reproduce the first or second output because both executions are consistent with the same recorded evidence. Therefore $M$ is insufficient to uniquely determine byte output. Restoring sufficiency requires eliminating $h$, recording a value/equivalence class that fixes its relevant effect, or weakening the declared comparator with domain justification.

## Alternatives and Trade-Offs

**Byte identity versus semantic equivalence.** Byte identity is simple, strong and cache-friendly, but requires deterministic serialization and metadata. Semantic comparison tolerates irrelevant encoding variation, but its canonicalizer becomes critical code and can conceal meaningful differences. Prefer byte identity for governed primary artifacts when practical.

**Materialized snapshot versus source-native version.** Copying bytes strengthens retention and independence but increases cost and privacy exposure. Native object/database versions reduce duplication but may expire or require the original platform. Use the horizon and sensitivity to decide.

**Full environment image versus declarative environment.** An image is convenient and concrete but can hide kernel/hardware assumptions and become un-runnable. A declarative environment is auditable and portable but relies on resolvers and retained dependencies. Retaining both definition and realized digest is often strongest.

**Strict pinning versus compatible ranges.** Exact pins improve repeatability but delay patches and can freeze vulnerabilities. Compatible ranges support maintenance but do not reproduce an old run unless resolution is captured. Pin each run while separately advancing tested future environments.

**Global sorting versus order-independent comparison.** Sorting gives deterministic bytes but costs memory/shuffle and needs a total key. Set/multiset comparisons avoid presentation order but require canonical row identity and careful multiplicity. Choose according to output semantics.

**Exact arithmetic versus numerical tolerance.** Exact/decimal methods can produce stable governed results at performance or range cost. Floating methods may be necessary for scientific scale. Fix reductions for exact bytes or predeclare a scientifically/domain-valid comparison.

**Capture randomness versus derive it.** Recording every random value is explicit but large. Algorithm/seed/partition specification is compact but version-sensitive. Per-record counter/key derivation can be stable and parallel-friendly. Security randomness must remain unpredictable and outside analytical reproducibility shortcuts.

**Record environment versus remove dependency.** Recording locale or path can reproduce a fragile system. Making output independent of them creates a wider and more durable claim. Variation tests tell which dependencies can be eliminated.

**Embedded provenance versus sidecar manifest.** Embedding improves portability but changes artifact bytes and can create self-reference. Sidecars are independently signable and easier to evolve but can be separated. Bind them through digests and stable identifiers.

**Central provenance service versus artifact-local records.** Central graphs enable queries and governance, but service loss can strand artifacts. Local manifests travel with outputs but duplicate context. Use local minimum evidence with indexed central aggregation.

**Retain raw data versus minimize it.** Raw retention maximizes future repair and replay. It also maximizes privacy, licensing and breach risk. Apply purpose limitation, scoped snapshots, encryption, deletion workflows and honest limitation statements.

**Replay from checkpoint versus raw history.** Checkpoints are fast but bind to state format and may conceal earlier corruption. Raw replay is stronger but expensive and may exceed retention. Periodically cross-check both paths.

## Failure Modes and Misconceptions

- **“It ran twice, so it is reproducible.”** That establishes limited repeat behavior on one context, not independent reconstruction.
- **“The query is the input.”** Mutable database state and isolation determine its result.
- **“The path identifies the file.”** Paths and object keys can be overwritten; content/version identity is required.
- **“A timestamped snapshot is consistent.”** Capture time does not prove transactionally coherent reads.
- **“Offsets reproduce a stream.”** Partition identity, boundaries, transactions, schemas and reference state also matter.
- **“The Git commit is the executable.”** Builds, dependencies, flags and dirty state can change executed bytes.
- **“The container tag pins the environment.”** Tags are mutable; even image digests do not fix all host behavior.
- **“The lockfile closes dependencies.”** Only if the actual resolver honors it and all artifacts remain retrievable and verified.
- **“Defaults do not need recording.”** Effective defaults change across versions and can alter results.
- **“A random seed guarantees reproduction.”** Generator, version, call order and parallel stream assignment matter.
- **“Database rows have a stable natural order.”** Without an explicit total ordering, output order is not contractual.
- **“Sorting by timestamp is deterministic.”** Equal timestamps remain tied without a stable tie-breaker.
- **“Floating addition is associative in the implementation.”** Finite precision and regrouping can change results.
- **“Tolerance can be chosen after comparison.”** That makes the test fit the result rather than the domain.
- **“JSON has one byte representation.”** Whitespace, property order and number/string serialization can vary.
- **“Sorting JSON keys is canonicalization.”** A complete scheme must define primitive serialization and domain restrictions too.
- **“Same digest means same semantic dataset.”** It means same hashed bytes under the assumed algorithm/scope.
- **“A hash authenticates the source.”** An unauthenticated digest can be replaced with the object.
- **“A signature proves correctness.”** It authenticates a statement/key relationship, not transformation validity.
- **“Provenance proves reproducibility.”** Lineage can omit resolvable materials, environment or replay instructions.
- **“Row count is an adequate comparator.”** Different rows can have the same count.
- **“Rejected records do not affect output.”** Changed rejection behavior is a material boundary difference.
- **“Caches are harmless accelerators.”** They can supply stale or undeclared external results.
- **“A retry is idempotent by default.”** Publication and side effects can duplicate even when computations match.
- **“Keep everything forever.”** Reproducibility evidence must respect privacy, security, licensing and deletion duties.

## Worked Examples

### Example 1

A daily job reads `s3://bucket/orders/latest.csv`. The key is overwritten each day, so the path cannot reproduce yesterday's result. The boundary resolves the object generation/version, captures byte size and SHA-256, binds the CSV schema/parser options and records it in the run manifest.

Replay fetches that immutable generation and verifies bytes before parsing. If source version retention is shorter than the seven-year requirement, the boundary copies an encrypted governed snapshot with equivalent access and deletion policy.

### Example 2

A report stores SQL text `SELECT ... FROM sales WHERE updated_at < :cutoff` and cutoff, but it reads three tables in separate autocommit statements. Concurrent changes create a combination that never existed in one database state.

The corrected job runs under an exported consistent snapshot or materializes one governed extract inside a transaction. It records engine/version, snapshot identity, query text, parameters, session settings, output schema and extract digest. Long-term replay uses the retained extract because the database snapshot token expires.

### Example 3

A stream replay says “events from midnight to 01:00.” Late arrivals and partition retention make repeated wall-time queries differ. The reproducible segment instead identifies topic generation, partitions, start-inclusive/end-exclusive offsets, transaction isolation, schemas and the reference-data snapshot.

It also identifies the initial checkpoint and output state. A later run may process the same domain hour, but it is not the same replay unless the bounded log positions and state match.

### Example 4

A JSON manifest is hashed after ordinary serialization. One library emits keys in insertion order and another sorts them; whitespace and number formatting also differ. Both parse to similar objects but yield different digests.

The contract selects RFC 8785 for the allowed JSON domain, validates inputs against its restrictions, canonicalizes, encodes UTF-8 and hashes those bytes. The raw received manifest remains retained. The algorithm and canonicalization version accompany the digest.

### Example 5

A sampling transform records seed `42`, yet results change after moving from one thread to eight. Work completion changes the order in which threads consume a shared generator.

The design derives a counter-based stream from `(run_seed,stable_record_id)` or preassigns named substreams to stable partitions. It pins generator/version and total record ordering. Variation tests run multiple thread counts and verify that the declared output comparator holds.

### Example 6

A revenue aggregation produces last-bit differences across worker counts because floating additions regroup. An engineer proposes accepting any result within one percent after seeing the mismatch, which is far wider than the business error budget.

The currency calculation changes to exact scaled decimals and a deterministic reduction. For a scientific aggregate that must remain floating, the team specifies absolute/relative tolerances, NaN policy and conserved totals before execution, pins relevant libraries and reports variation separately.

### Example 7

A pipeline works in development but changes ordering in production. The developer's filesystem happens to list partition files lexically; the distributed store does not. Sorting rows by `event_time` still leaves identical timestamps tied.

The boundary manifests input parts in canonical content-ID order and sorts output by `(event_time,record_id)`, with null/text rules. A second artifact whose order is semantically irrelevant is compared as a multiset, avoiding unnecessary global sorting.

### Example 8

A geocoding API enriches addresses. Replaying the request a month later returns updated coordinates and provider metadata. Storing only the URL, code revision and API version cannot reproduce the published table.

The run captures policy-approved request identities and exact responses, statuses and provider version under restricted storage, while excluding credentials. If licensing forbids response retention, the manifest says full independent replay ends when provider history is unavailable; it does not overclaim.

### Example 9

A clean-room replay matches all output rows but rejects 12 inputs where the original rejected 10. The team initially calls it equivalent because published row counts match after two duplicate outputs elsewhere.

The comparator also checks accepted/rejected/coerced counts, reason categories, canonical record multiset, schema and key uniqueness. It localizes the difference to a parser dependency. The failed replay artifacts are retained before the dependency is corrected and pinned.

### Example 10

A manifest includes a database password, customer query literals and direct sensitive-object URLs so “everything needed” is in one file. The evidence package becomes a new exfiltration path.

The redesign records authorized secret/version references, opaque governed input IDs and minimal aggregate validation evidence. Sensitive snapshots remain encrypted in a controlled store. Manifest access, signature verification, audit, retention and deletion are tested independently from the replay process.

## Cross-Program Connections

**Software Delivery and Reliability Engineering.** Reproducible software builds, immutable artifacts, dependency locking, promotion and rollback provide patterns for identifying the executable half of a data run.

**Security Engineering.** Digests, signatures, attestations, secret handling and controlled builders address integrity/authenticity threats. Reproducibility evidence itself needs a threat model and access policy.

**Platform Engineering.** Hermetic workers, artifact registries, content-addressed caches, policy enforcement and standardized execution metadata make clean-room replay practical across teams.

**Database Engineering.** Snapshot isolation, transaction positions, schema versions, query plans and session settings determine whether database-derived inputs are stable and interpretable.

**Distributed Systems Engineering.** Partitioning, concurrency, retries, nondeterministic schedules, log offsets and checkpoint state shape reproducibility for stateful and parallel computation.

**API and Service Engineering.** Mutable external responses must become captured inputs. Idempotency keys and staged publication keep replay from duplicating side effects.

**Machine Learning Engineering.** Datasets, feature definitions, code, models, random streams, hardware and numerical libraries all enter an experiment/model reproducibility perimeter.

**Data Architecture Engineering.** Catalog identities, lineage graphs, retention, data contracts and ownership make manifests discoverable and usable beyond one pipeline implementation.

## References

1. Reproducible Builds, [Definitions](https://reproducible-builds.org/docs/definition/) and [Making Plans](https://reproducible-builds.org/docs/plans/), retrieved 2026-09-02.
2. W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/), W3C Recommendation, retrieved 2026-09-02.
3. SLSA, [Specification 1.2: Provenance](https://slsa.dev/spec/v1.2/provenance), retrieved 2026-09-02.
4. IETF, [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html), retrieved 2026-09-02.
5. IETF, [RFC 8949: Concise Binary Object Representation](https://www.rfc-editor.org/rfc/rfc8949.html), retrieved 2026-09-02.
6. IETF, [RFC 6920: Naming Things with Hashes](https://www.rfc-editor.org/rfc/rfc6920.html), retrieved 2026-09-02.
7. NIST, [FIPS 180-4: Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final), retrieved 2026-09-02.
8. Frictionless Data, [Data Resource Specification](https://specs.frictionlessdata.io/data-resource/) and [Table Schema Specification](https://specs.frictionlessdata.io/table-schema/), retrieved 2026-09-02.

## Exercises

### Exercise 1

A batch job reads two overwriteable object keys and three database tables, calls a mutable exchange-rate API, and publishes Parquet plus a dashboard. Define the reproducibility perimeter, immutable input capture, schema/environment identities, primary outputs, byproducts, comparator, access controls and a seven-year replay plan.

### Exercise 2

Two files contain the same logical records in different orders and JSON property layouts, with one duplicate row. Design byte-identity and semantic-multiset comparison protocols. Explain exactly what is canonicalized, hashed and counted, and how the duplicate affects equivalence.

### Exercise 3

A distributed Monte Carlo job records code commit and seed but changes results with worker count and library upgrade. Redesign its random streams, partitioning, dependencies, numerical comparator, variation tests, provenance and claim language. State what can and cannot be byte-reproducible.

### Exercise 4

Design a run-manifest schema for an incremental stream computation. Include log ranges, schemas, initial checkpoint, reference snapshots, code/build, configuration, environment, watermarks, late-data policy, output state, rejected records, digests, provenance, comparator, retention and secrets handling.

### Exercise 5

A clean-room replay has the same row count and totals as the original but different keys, rejection reasons and file digests. Provide a layered diagnostic procedure, evidence preservation steps, completion criteria and rules for deciding whether a comparator change is legitimate.

## Answers to the Exercises

### Answer 1

Begin the perimeter by capturing immutable generations of both objects, a transactionally consistent database extract or durable snapshot, and the exact exchange-rate response used. Bind byte digests, sizes, media types, schemas, parser options, query text/parameters, engine/session settings and API request identity. Record source commit, executed image digest, dependency closure, effective configuration, locale/timezone and injected run time.

Treat governed Parquet and its schema as primary outputs; treat dashboard rendering, logs and validation reports as separate outputs/byproducts according to the claim. Compare Parquet through byte identity if deterministic, otherwise through an explicitly canonical typed multiset plus invariants. Store encrypted snapshots and manifests with role-based access, signed provenance, audited secret references and tested restore. Mirror dependencies for seven years and document deletions/licensing that narrow replay.

### Answer 2

Byte identity hashes each exact file representation and will report inequality for different order/layout. Record algorithm, length and raw-byte scope. A semantic protocol strictly parses under the same schema, canonicalizes each typed record using a specified encoding, hashes canonical row bytes and compares a multiset from row digest to multiplicity.

Property layout and file order then do not matter, but the duplicate increments one row's multiplicity and makes datasets unequal unless both contain it. Do not compare sets, which would erase duplicates. Version parser/canonicalizer, define null/number/Unicode behavior, preserve raw digests and verify schemas plus accepted/rejected counts.

### Answer 3

Derive stable named random streams from run seed plus experiment/record/replicate identity using a pinned generator and implementation. Assign stable logical partitions independent of worker completion, fix aggregation/reduction or capture its numerical model, and pin the full library/runtime/hardware assumptions that affect results.

Run the same logical work with several worker counts, paths and hosts. If exact algorithms and deterministic reductions hold, claim byte identity for the specified environment. If the scientific method permits floating variation, predeclare absolute/relative/statistical tolerances, invariants and sample size; do not claim byte reproduction. Provenance links dataset, executable, dependency environment, stream definition, run and outputs.

### Answer 4

The manifest needs schema/version and run ID; topic/cluster generations; per-partition start-inclusive/end-exclusive offsets; isolation/transaction mode; record schema IDs/digests; initial checkpoint/state digest and schema; reference dataset snapshots; code commit and executable image digest; dependency lock; effective flags; random/time/order/partition policies; runtime/platform; watermark and allowed-lateness state; deduplication keys; tombstone/compaction assumptions; output checkpoint and table/file digests; accepted/rejected/late counts; provenance agent/activity/entity links; comparator; and retention/access policy.

Credentials appear only as authorized secret/version references. Replay first verifies checkpoint and inputs, executes the bounded transition, and compares state/output plus byproduct invariants. A separate raw-history reconstruction can periodically verify checkpoint integrity.

### Answer 5

Preserve both outputs, manifests, logs, rejected data identities and environments before retrying. Verify manifest/comparator versions; exact inputs and schemas; parser behavior; code/build/dependencies; effective configuration; locale/timezone; controlled time/randomness; ordering/partition/reduction; then compare stage/partition/column digests to localize the first divergence.

Equal counts/totals are insufficient because different keys and rejection categories contradict semantic equivalence, while file digests contradict byte identity. Completion requires the predeclared comparator to pass, the cause to be explained, and a regression fixture plus clean replay to pass. Change a comparator only through domain review showing the distinction was previously declared irrelevant—not merely because the new output failed—and version/replay both results under the new contract.
