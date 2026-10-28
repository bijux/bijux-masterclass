# Module 07 — Streaming and Artifact Integrity

> **Program stage:** Course 2 of 6 — Make the promise durable.

> **Central question:** How can large uploads, progress streams, and artifacts remain bounded, durable, and integrity-checked?

## Where this module fits

Stream uploads and downloads, verify checksums, and publish content-addressed artifacts atomically. You arrive from Module 06 with all earlier checkpoints still green. The Course 1 handoff is fixed. This course may change internal architecture and add a compatible API release, but it may not solve an implementation problem by quietly weakening the public contract. The result is the baseline for **Transactional Outbox and Webhook Delivery**.

## Learning outcomes

- Enforce limits while streaming rather than after buffering.
- Stage bytes safely and clean up failures.
- Use content addressing and no-clobber publication.
- Persist event streams for SSE and NDJSON consumers.
- Keep artifact authorization and storage paths separate.

## Capstone result

Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download.

Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.

## Core model

### Driving question

> How do large representations move through the service without exhausting memory, publishing partial content, or violating ownership?

A file is not durable merely because bytes reached the process. Safe data movement requires bounded reads, staged writes, cryptographic checksums, atomic publication, transactional metadata, cleanup, and streamed retrieval.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- the public behavior inherited from Course 1;
- the application or domain decision owner;
- the durable database, worker, storage, or delivery mechanism;
- the proof that exposes failure after retry, concurrency, or restart.


### 1. Bounded ingestion

Read multipart content in fixed chunks, track cumulative size, and abort when the configured maximum is exceeded. Declared `Content-Length` may permit early rejection but cannot replace measured enforcement because it can be absent or false.

**Counterexample.** Call `await file.read()` or concatenate every chunk into one buffer before validation.

**Evidence direction.** Upload a file well above the chunk size while tracking peak memory, then exceed the maximum by one byte.

### 2. Private staging

Incomplete bytes live under a staging directory that no download route serves. A unique temporary name prevents collisions. Failure or disconnect removes the staged file. Publication occurs only after validation and checksum finalization.

**Counterexample.** Write directly to the final artifact path and rely on a “complete” flag.

**Evidence direction.** Kill the upload mid-stream and prove no public path or metadata exists; staging cleanup is bounded.

### 3. Content-addressed publication

The final path derives from the SHA-256 digest, typically with prefix directories. Identical content converges to one immutable object. Publication uses an atomic filesystem rename within one filesystem; cross-filesystem moves do not provide the same guarantee.

**Counterexample.** Use original client filename as the storage path.

**Evidence direction.** Upload identical bytes twice and observe one content object with separate or reused logical metadata as designed.

### 4. Integrity metadata

Artifact metadata stores checksum, byte size, media type, owner, run, and path identity. Retrieval verifies enough metadata/path consistency to detect tampering. Full checksum-on-every-download is a policy trade-off; the course includes an explicit audit command and verification path.

**Counterexample.** Trust file path and return whatever bytes currently exist.

**Evidence direction.** Modify stored bytes and run integrity proof; the artifact is rejected or audit fails.

### 5. Cross-resource ownership

Upload and download authorization joins dataset/run/artifact identity with owner in one query path. A guessed artifact ID cannot bypass the project/run ownership chain.

**Counterexample.** Check artifact owner after opening the file and logging metadata.

**Evidence direction.** Foreign artifact requests never open the storage path and return concealed not found.

### 6. Streaming response lifecycle

A streaming response owns a producer, backpressure, cancellation, and cleanup. The producer yields bounded chunks or events. It does not hold a database transaction or pool connection for the stream lifetime.

**Counterexample.** Keep a transaction open while a slow client downloads a large artifact.

**Evidence direction.** Inspect active transactions during a throttled download; disconnect and assert file handle cleanup.

### 7. SSE and NDJSON framing

SSE uses text event framing and blank-line termination; NDJSON uses one complete JSON value per line. Both carry stable event IDs/positions so consumers can detect order and reconnect. Neither changes the durable event source.

**Counterexample.** Split one JSON object across NDJSON lines or omit SSE terminators.

**Evidence direction.** Incremental parsers consume arbitrarily split network chunks and reconstruct every event.

### 8. Two-system commit gap

Filesystem and PostgreSQL cannot commit atomically in this design. Publishing first avoids metadata pointing to missing content, but a crash before metadata commit can leave an orphan. The course records, audits, and safely removes orphans after a retention window.

**Counterexample.** Claim that a Python `try` block makes file rename and SQL commit atomic.

**Evidence direction.** Inject process death between publication and metadata commit, then run orphan detection.

### Design pressure

Choose the principle above most likely to fail in **Streaming and Artifact Integrity**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Staged file

Private temporary path plus measured size, checksum, and media type.

**Invariant:** Never addressable by a public operation.

Immutable content-addressed file atomically present at final path.

**Invariant:** Path digest agrees with bytes.

Authorized durable pointer from run to published content.

**Invariant:** Visible metadata never points to an incomplete object.

Bounded iterator over file chunks or persisted events.

**Invariant:** No long-lived database transaction and cleanup on cancellation.

### Boundary diagram

```text
frozen OpenAPI + generated client
                |
                v
       transport/auth adapter
                |
                v
      application use case
        /       |       \
       v        v        v
  PostgreSQL  artifact  outbound HTTP
       ^        store       adapter
       |          \          /
       +----------- worker ---+
```

### Decision record template

```text
Decision:
Context and competing designs:
Chosen guarantee:
Mechanism:
Failure window that remains:
Evidence:
Rollback or migration path:
What this does not prove:
```

Use this template for at least two decisions from today. A course answer that hides remaining failure windows is incomplete.

## Worked service design

### Objective

Turn the module thesis into explicit choices before framework or SQL convenience dictates the design.

### Working method

For each decision, produce three artifacts:

1. a short decision record;
2. a sequence/state/transaction sketch;
3. a falsifying example with expected evidence.

For each decision, record the inherited API behavior, the new durable requirement, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof file that owns the choice.

### Decision 1: Choose upload chunk size and hard maximum independently.

### Decision 2: Define allowed media types and filename treatment; never trust paths from clients.

### Decision 3: Place staging and final storage on the same filesystem for atomic rename.

### Decision 4: Define content-addressed path format and immutable overwrite behavior.

### Decision 5: Choose publication-before-metadata and document orphan recovery.

### Decision 6: Define download chunking, conditional headers, and disconnect cleanup.

### Decision 7: Define SSE and NDJSON event framing from the same persisted event rows.

### Decision 8: Build integrity audit and orphan audit commands.

### Worked reasoning pattern

Suppose a learner proposes: “The route can check first, then the repository can write.” Ask:

- Can another request change the fact between check and write?
- Which rows or effects must commit atomically?
- What survives a lost response or process restart?
- Which focused test makes the race or partial effect observable?


### Design review

The design review must challenge the module-specific failure named in the lab and identify the durable oracle that distinguishes a real repair from a cosmetic pass.
## Python implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/python-fastapi/src/analysis_service/
```

### Focus points

1. `FileSystemArtifactStore.stage()` consumes an async byte iterator, updates `hashlib.sha256`, and enforces maximum bytes.
2. Use `os.replace()` only after final validation and ensure staging/final directories share a filesystem.
3. Open downloads lazily and yield fixed chunks; close handles in `finally` when the client disconnects.
4. FastAPI upload wrappers are transport adapters; pass an async iterator and media metadata to the store.
5. Never trust `UploadFile.filename` as a path component.
6. Use persisted run-event positions for SSE/NDJSON rather than in-memory pub/sub.

### Representative pattern

```python
async def stage(self, chunks: AsyncIterator[bytes], media_type: str) -> StagedFile:
    digest = hashlib.sha256()
    size = 0
    temporary = self._new_staging_path()
    try:
        with temporary.open("xb") as target:
            async for chunk in chunks:
                size += len(chunk)
                if size > self.maximum_bytes:
                    raise PayloadTooLarge(self.maximum_bytes)
                digest.update(chunk)
                target.write(chunk)
        return StagedFile(temporary, size, digest.hexdigest(), media_type)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
```

This excerpt is deliberately smaller than the complete implementation. Identify the transaction or decision boundary, one hidden assumption, the cleanup/error path, and the regression that would fail if the guard moved outside that boundary.


## TypeScript implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/typescript-fastify/src/
```

Runtime schemas, TypeScript types, Fastify lifecycle, Node streams, and node-postgres sessions solve different problems. Keep them separate while reading.

### Focus points

1. Pipe the multipart file stream through byte-count and hash logic; do not convert it to a single `Buffer`.
2. Use `pipeline()`/stream events or explicit async iteration with abort handling and cleanup.
3. Atomic rename requires same-filesystem staging; handle `EXDEV` as a configuration failure, not silent copy.
4. Build `Readable` download streams and destroy them on request abort.
5. Fastify reply streaming bypasses normal JSON serialization, so headers and error timing must be set before bytes are sent.
6. Parse persisted event rows into correct SSE or NDJSON frames without holding a database client indefinitely.

### Representative pattern

```typescript
for await (const chunk of part.file) {
  size += chunk.byteLength;
  if (size > settings.maximumUploadBytes) throw new PayloadTooLarge();
  hash.update(chunk);
  if (!target.write(chunk)) await once(target, "drain");
}
await finished(target);
await rename(stagedPath, contentAddressedPath(hash.digest("hex")));
```

Interrogate the excerpt for cancellation, connection ownership, rollback, retry scope, and any framework convenience that could change the durable guarantee.


### Cross-language comparison

Write no more than one page:

```text
shared public guarantee:
Python mechanism:
TypeScript mechanism:
idiomatic difference:
proof shared by both:
proof that must remain track-specific:
```

## SQL and durable state

### Module data focus

1. Artifact metadata references completed run and owner; uniqueness prevents duplicate logical artifact names.
2. Run events use monotonic per-run positions to support ordered streams and reconnection.
3. No database transaction remains open while reading or writing the full content body.
4. Orphan audit compares storage digest paths with committed metadata.

### Representative SQL

```sql
-- The database stores only committed publication metadata.
INSERT INTO artifacts(public_id, run_id, owner_id, storage_digest, byte_size, media_type)
VALUES ($1, $2, $3, $4, $5, $6)
ON CONFLICT (run_id, logical_name) DO NOTHING;
```

### Reading the statement as a proof obligation

For every SQL fragment, annotate:

```text
input parameters:
rows it may observe:
locks or transaction context:
condition that makes it atomic:
rows it may change:
constraint/index supporting it:
zero-row meaning:
retry behavior:
application failure mapping:
```

### Constraint exercise

Choose one invariant from the mental model and classify it:

Explain the classification rather than adding a trigger reflexively.

## How to verify the guarantee

### Principle

A file is not durable merely because bytes reached the process. Safe data movement requires bounded reads, staged writes, cryptographic checksums, atomic publication, transactional metadata, cleanup, and streamed retrieval.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | upload memory bounded | Write the narrow command and machine-readable oracle. |
| 2 | size limit enforced by measured bytes | Write the narrow command and machine-readable oracle. |
| 3 | interrupted upload unpublished | Write the narrow command and machine-readable oracle. |
| 4 | atomic final rename | Write the narrow command and machine-readable oracle. |
| 5 | checksum matches bytes | Write the narrow command and machine-readable oracle. |
| 6 | tamper detected | Write the narrow command and machine-readable oracle. |
| 7 | foreign artifact never opened | Write the narrow command and machine-readable oracle. |
| 8 | streams parse under arbitrary chunking | Write the narrow command and machine-readable oracle. |

### Layer selection

Use the narrowest layer capable of falsification:

```text
pure function/vector
    ↓
application use case with substitutes
    ↓
real PostgreSQL/filesystem/receiver integration
    ↓
HTTP provider conformance
    ↓
concurrent actors
    ↓
process death and restart
    ↓
old/new release coexistence
```

Skipping directly to the bottom produces slow, opaque evidence and still may miss combinatorial policy errors.

### Defect protocol

The planted defect for this module is:

> Write uploads directly to the final served path and use a slow producer so another request can observe partial bytes.

Before injecting it, write:

```text
predicted first failing proof:
smallest input/interleaving:
expected durable state:
expected public observation:
what a weaker test would miss:
```

After repair, preserve:

```text
actual first failure:
root cause:
repair boundary:
permanent regression path:
remaining limitation:
```

### Evidence report schema

```json
{
  "claim": "...",
  "status": "passed | failed | not-executed",
  "command": "...",
  "topology": {"postgresql": "18.4", "track": "python | typescript"},
  "inputs": ["fixture/hash"],
  "assertions": ["observable or durable oracle"],
  "report": "capstone/reports/...",
  "limitations": ["what this does not establish"]
}
```

A missing dependency is `not-executed`, never `passed`.

## Failure patterns

### 1. Whole-body buffering

**Observable symptom:** Memory grows linearly with upload/download size.

**Root cause:** Framework convenience method materializes content.

**Repair:** Use async iteration/streams with fixed chunks.

**Permanent regression:** Large payload plus peak-memory threshold.

### 2. Trusting Content-Length

**Observable symptom:** Oversized chunked or dishonest request bypasses limit.

**Root cause:** Only declared length was checked.

**Repair:** Count actual bytes while reading.

**Permanent regression:** Missing/false length and limit+1 cases.

### 3. Public partial file

**Observable symptom:** Concurrent download sees truncated content.

**Root cause:** Upload writes to final served path.

**Repair:** Private staging then atomic publication.

**Permanent regression:** Slow upload with concurrent download attempts.

### 4. Client filename traversal

**Observable symptom:** Upload escapes storage root or overwrites another file.

**Root cause:** Untrusted filename used as path.

**Repair:** Ignore for storage identity; sanitize only optional display metadata.

**Permanent regression:** Traversal and separator filename corpus.

### 5. Metadata before bytes

**Observable symptom:** API exposes artifact whose file is missing after crash.

**Root cause:** Database commits before publication.

**Repair:** Publish first, then metadata, and audit possible orphans.

**Permanent regression:** Failure injection at both sides of boundary.

### 6. Claimed cross-system atomicity

**Observable symptom:** Rare unexplained orphan or dangling metadata remains.

**Root cause:** Code assumes try/rollback spans filesystem.

**Repair:** Document ordering and reconciliation.

**Permanent regression:** Kill process between operations and run audit.

### 7. Long transaction stream

**Observable symptom:** Slow clients exhaust pool and retain snapshots/locks.

**Root cause:** Database cursor/transaction held for response duration.

**Repair:** Read bounded event pages or immutable metadata, close transaction, then stream.

**Permanent regression:** Throttled client with active-transaction check.

### 8. Malformed framing

**Observable symptom:** Consumers hang or merge events.

**Root cause:** SSE blank line or NDJSON line boundary omitted.

**Repair:** Centralize frame encoder and test arbitrary network chunk splits.

**Permanent regression:** Incremental parser vector suite.

### Failure triage template

```text
public symptom:
first incorrect durable fact:
first component that could have prevented it:
why existing proof missed it:
minimal reproducer:
repair:
regression:
claim still not proved:
```

## What you add to the capstone

### Target state

Dataset bytes and analysis artifacts now have a bounded, integrity-checked physical path, while progress streams expose only committed events.

### Increment plan

1. Implement chunked multipart staging with actual-byte limit and SHA-256.
2. Implement atomic content-addressed publication and metadata transaction.
3. Implement orphan and staging cleanup audits.
4. Implement owner-qualified artifact retrieval with bounded download stream.
5. Implement SSE and NDJSON from persisted event positions.
6. Run large, limit, limit+1, interrupted, duplicate-content, and foreign-owner cases.

### Files to inspect before editing

```text
predecessor/spec/dist/openapi.bundle.yaml
predecessor/behavioral-scenarios.yaml
predecessor/scope-matrix.yaml
capstone/shared/operation-map.yaml
capstone/shared/state-machine.json
capstone/tracks/python-fastapi/
capstone/tracks/typescript-fastify/
capstone/scripts/course_tool.py
```

### Integration invariant

The increment must preserve the frozen contract, all earlier durable invariants, owner-aware access, bounded resources, restart safety, and equivalent public outcomes in the comparison track.


### Review trace

For one operation affected today, produce:

```text
operationId:
request/credential input:
application use case:
domain rule:
transaction/query:
external/file/process boundary:
response/problem mapping:
proof command:
remaining failure window:
```

## Representative implementation

These are the smallest useful entry points for **Streaming and Artifact Integrity**.

### Python — `capstone/tracks/python-fastapi/src/analysis_service/artifacts.py`

```python
CHUNK_SIZE = 64 * 1024


class FileSystemArtifactStore:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.staging = self.root / ".staging"
        self.staging.mkdir(parents=True, exist_ok=True)

    def _safe(self, key: str) -> Path:
        relative = PurePosixPath(key)
        if relative.is_absolute() or not relative.parts or ".." in relative.parts:
            raise ValueError("unsafe storage key")
        path = (self.root / Path(*relative.parts)).resolve()
        if path != self.root and self.root not in path.parents:
            raise ValueError("storage key escaped root")
        return path

    async def stage_upload(
        self,
        source: BinaryIO,
        media_type: str,
        limit: int,
    ) -> StagedFile:
        descriptor, raw_path = tempfile.mkstemp(
            prefix="upload-",
            dir=self.staging,
        )
        path = Path(raw_path)
        digest = sha256()
        size = 0
        try:
            with os.fdopen(descriptor, "wb") as target:
                while True:
                    block = await asyncio.to_thread(source.read, CHUNK_SIZE)
                    if not block:
                        break
                    size += len(block)
                    if size > limit:
                        raise ServiceError(
                            413,
                            "Payload too large",
                            "The training upload limit is 1 MiB.",
                            "payload-too-large",
                        )
                    digest.update(block)
                    target.write(block)
                target.flush()
                os.fsync(target.fileno())
            if size == 0:
                raise ServiceError(
                    422,
                    "Request validation failed",
                    "The uploaded file is empty.",
                    "validation",
                )
            return StagedFile(path, size, digest.hexdigest(), media_type)
        except BaseException:
            path.unlink(missing_ok=True)
            raise

    def stage_bytes(self, content: bytes, media_type: str) -> StagedFile:
        if not content:
            raise ValueError("artifact cannot be empty")
```

### TypeScript — `capstone/tracks/typescript-fastify/src/artifacts.ts`

```typescript

import type { StagedFile } from "./types.js";

const CHUNK_SIZE = 64 * 1024;

export class FileSystemArtifactStore {
  private readonly root: string;
  private readonly staging: string;

  public constructor(root: string) {
    this.root = resolve(root);
    this.staging = resolve(this.root, ".staging");
  }

  public async initialize(): Promise<void> {
    await mkdir(this.staging, { recursive: true });
  }

  private safe(key: string): string {
    if (
      isAbsolute(key) ||
      key.length === 0 ||
      key.split("/").includes("..") ||
      key.includes("\\")
    ) {
      throw new Error("unsafe storage key");
    }
    const path = resolve(this.root, key);
    const rel = relative(this.root, path);
    if (rel === ".." || rel.startsWith(`..${sep}`) || isAbsolute(rel)) {
      throw new Error("storage key escaped root");
    }
    return path;
  }

  public async stageStream(
    source: Readable,
    mediaType: string,
    limit: number,
  ): Promise<StagedFile> {
    await this.initialize();
    const temporaryPath = resolve(this.staging, `upload-${randomUUID()}`);
    const hash = createHash("sha256");
    let size = 0;

    const meter = new Transform({
      transform(chunk: Buffer, _encoding, callback) {
        size += chunk.length;
        if (size > limit) {
          callback(new Error("payload-too-large"));
          return;
        }
        hash.update(chunk);
        callback(null, chunk);
      },
    });

    try {
      await pipeline(
        source,
        meter,
        createWriteStream(temporaryPath, {
          flags: "wx",
          highWaterMark: CHUNK_SIZE,
        }),
```

Compare the two tracks by this invariant: **staging is bounded, publication is atomic and no-clobber, and the digest names exactly the published bytes**. The intended implementation difference is: stream APIs differ; the checksum, size, confinement, and idempotent-publish outcome do not.

## Module synthesis

The module answer to “How do large request and response bodies move through the service without unbounded memory or corrupt publication?” is now executable in the capstone: Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.

## Next in the story

Module 08, [Transactional Outbox and Webhook Delivery](../module-08-webhooks-transactional-outbox/index.md), asks: *How can a committed domain outcome produce an external notification without losing intent or duplicating effects unpredictably?* The current checkpoint must remain green while that new responsibility is added.
