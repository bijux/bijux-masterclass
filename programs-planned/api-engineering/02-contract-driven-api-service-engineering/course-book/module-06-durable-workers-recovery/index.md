# Module 06 — Durable Workers and Recovery

> **Program stage:** Course 2 of 6 — Make the promise durable.

> **Central question:** What makes a 202 Accepted operation honest after the API process or worker dies?

## Where this module fits

Build a PostgreSQL-backed job protocol with claims, leases, generations, heartbeats, cancellation, and recovery. You arrive from Module 05 with all earlier checkpoints still green. The Course 1 handoff is fixed. This course may change internal architecture and add a compatible API release, but it may not solve an implementation problem by quietly weakening the public contract. The result is the baseline for **Streaming and Artifact Integrity**.

## Learning outcomes

- Separate durable acceptance from execution.
- Claim work without holding a long transaction.
- Fence stale workers with lease generation.
- Recover abandoned jobs safely.
- Make duplicate execution converge on one durable outcome.

## Capstone result

Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery.

Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.

## Core model

### Driving question

> What internal machinery makes `202 Accepted` honest?

Accepted work must exist durably before the response, be claimable by one active lease generation, survive process death, and produce idempotent effects under at-least-once execution.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- the public behavior inherited from Course 1;
- the application or domain decision owner;
- the durable database, worker, storage, or delivery mechanism;
- the proof that exposes failure after retry, concurrency, or restart.


### 1. Durable acceptance

The API returns `202` only after run, initial event, durable job, and idempotency outcome are committed. Worker availability is irrelevant to acceptance; the status resource reveals queued progress until a worker claims it.

**Counterexample.** Create a task with `asyncio.create_task()` or `setImmediate()` and return before durable recording.

**Evidence direction.** Stop all workers, submit, restart API, and later start a worker; the run still completes.

### 2. Claim with skip-locked

Workers select eligible queued or expired jobs in stable order, lock a candidate, update lease metadata, and return the claim in one transaction. `SKIP LOCKED` allows other workers to claim other rows without waiting.

**Counterexample.** Select one queued ID, commit, then update it in a second statement so two workers select the same row.

**Evidence direction.** Multiple worker processes claim distinct jobs under a synchronized load.

### 3. Lease

A lease is time-bounded authority to execute a job. Heartbeats extend it while work is alive. Expiry makes abandoned work recoverable. Lease duration must exceed normal heartbeat jitter but remain bounded enough for recovery.

**Counterexample.** A permanent `claimed=true` flag requires manual repair after process death.

**Evidence direction.** Kill after claim, advance/wait beyond expiry, and observe another worker reclaim.

### 4. Lease generation fencing

Every claim increments a generation. All progress and terminal writes include the active owner and generation in their predicate. A stale process holding old authority cannot commit after recovery.

**Counterexample.** A late worker commits by run ID only after a newer worker has completed.

**Evidence direction.** Pause worker A, expire and recover with B, then release A; A’s write affects zero rows.

### 5. At-least-once effects

The system assumes job logic may execute repeatedly because of crash ambiguity. Effects use deterministic artifact content/identity and transactional guards. The goal is one logical result, not proof that CPU instructions ran once.

**Counterexample.** Generate a random artifact ID before each attempt and insert unconditionally.

**Evidence direction.** Execute the same claimed work twice and assert one visible artifact/result.

### 6. Heartbeat and progress

Progress updates both the run event stream and lease liveness under the active generation. Heartbeats are not terminal commits and should be cheap. A stuck worker that cannot heartbeat eventually loses authority.

**Counterexample.** Heartbeat in a separate thread continues while the actual job deadlocks forever and progress never advances.

**Evidence direction.** Tests distinguish lease renewal, progress monotonicity, and eventual expiry after heartbeat stop.

### 7. Retry classification

Transient infrastructure failures may requeue with bounded exponential delay. Permanent input or analysis failures terminate the run. Poison jobs stop after a maximum attempt count and record a stable failure rather than spinning forever.

**Counterexample.** Retry every exception forever, including invalid dataset content.

**Evidence direction.** Fixture errors are classified into retryable and terminal paths with exact attempt counts.

### 8. Graceful worker shutdown

On termination, the worker stops claiming new work and either completes the current guarded boundary or releases/lets the lease expire. It never marks uncompleted work successful merely to exit quickly.

**Counterexample.** Signal handler sets all leased jobs to completed.

**Evidence direction.** Process test sends termination during work and later proves recovery or committed completion.

### Design pressure

Choose the principle above most likely to fail in **Durable Workers and Recovery**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Job row

Run identity, status, availability, attempt count, lease owner, lease generation, expiry, and timestamps.

**Invariant:** Only one current generation has authority.

Select eligible row, lock it, increment generation/attempt, set lease, and return payload.

**Invariant:** No two workers receive the same active generation.

Progress or terminal update constrained by job ID, owner, generation, and expected lifecycle.

**Invariant:** Stale workers update zero rows.

Expired leased work becomes eligible for another claim.

**Invariant:** Process death cannot permanently strand accepted work.

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

### Decision 1: Define queued, leased, succeeded, failed, and retry states for job rows separately from public run states.

### Decision 2: Choose claim order and `SKIP LOCKED` transaction.

### Decision 3: Choose lease duration and heartbeat interval with an explicit ratio.

### Decision 4: Increment generation at every claim and include it in every worker write.

### Decision 5: Define attempt limit and retry delay function.

### Decision 6: Make artifact/result effects idempotent under duplicate execution.

### Decision 7: Place cancellation observation immediately before terminal transaction.

### Decision 8: Define signal handling: stop claiming, finish/abandon safely, close resources.

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

1. `Worker` owns the loop, but `PostgresRepository` owns claim and guarded transaction SQL.
2. Use monotonic process timing only for local sleeps; persisted lease expiry uses injected/database wall-clock semantics.
3. Catch cancellation signals outside the domain transition and set a stop flag.
4. Perform bounded analysis on staged/local input without holding a database transaction open.
5. Heartbeat through short independent transactions carrying lease generation.
6. Terminal repository methods return whether the generation still had authority.

### Representative pattern

```python
async def claim_job(self, worker_id: str, lease_seconds: int) -> ClaimedJob | None:
    async with self.pool.connection() as connection:
        async with connection.transaction():
            row = await connection.execute(CLAIM_SQL, (worker_id, lease_seconds))
            return map_claim(row.fetchone()) if row.rowcount else None

async def complete_job(self, claim: ClaimedJob, result: Result) -> bool:
    # Every terminal write includes lease owner and generation.
    return await self._complete_if_current(
        run_id=claim.run_id,
        lease_owner=claim.lease_owner,
        lease_generation=claim.lease_generation,
        result=result,
    )
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

1. Use an `AbortController` or explicit stop flag for process shutdown; do not abandon promises without closing the pool.
2. Keep event-loop-blocking analysis bounded or offload CPU-heavy work in a later specialized course.
3. Claim with one checked-out client and release before processing.
4. Use lease generation as `bigint`/safe mapped value consistently.
5. Heartbeat and terminal methods carry immutable claim data rather than re-reading ambient worker identity.
6. Await pool closure and artifact stream cleanup before process exit.

### Representative pattern

```typescript
const claim = await repository.claimJob(workerId, leaseSeconds);
if (claim !== null) {
  const result = await analyze(claim, signal);
  const committed = await repository.completeIfCurrent({
    runId: claim.runId,
    leaseOwner: claim.leaseOwner,
    leaseGeneration: claim.leaseGeneration,
    result,
  });
  if (!committed) await discardStaleLocalEffects(result);
}
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

1. Claim candidate with `FOR UPDATE SKIP LOCKED`, then update lease metadata in the same transaction.
2. Partial claim indexes cover queued availability and expired leases.
3. Guard progress/terminal updates with `lease_owner` and `lease_generation`.
4. Unique artifact/result constraints make duplicate execution converge.

### Representative SQL

```sql
WITH candidate AS (
  SELECT run_id
    FROM run_jobs
   WHERE (status = 'queued' AND available_at <= clock_timestamp())
      OR (status = 'leased' AND lease_expires_at <= clock_timestamp())
   ORDER BY available_at, created_at
   FOR UPDATE SKIP LOCKED
   LIMIT 1
)
UPDATE run_jobs AS job
   SET status='leased', lease_owner=$1,
       lease_generation=lease_generation+1,
       lease_expires_at=clock_timestamp()+$2::interval,
       attempt=attempt+1
  FROM candidate
 WHERE job.run_id=candidate.run_id
RETURNING job.*;
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

Accepted work must exist durably before the response, be claimable by one active lease generation, survive process death, and produce idempotent effects under at-least-once execution.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | accepted without worker durable | Write the narrow command and machine-readable oracle. |
| 2 | workers claim distinct jobs | Write the narrow command and machine-readable oracle. |
| 3 | killed lease recovered | Write the narrow command and machine-readable oracle. |
| 4 | generation increments | Write the narrow command and machine-readable oracle. |
| 5 | stale worker fenced | Write the narrow command and machine-readable oracle. |
| 6 | duplicate execution one logical result | Write the narrow command and machine-readable oracle. |
| 7 | cancellation race deterministic | Write the narrow command and machine-readable oracle. |
| 8 | shutdown stops new claims | Write the narrow command and machine-readable oracle. |

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

> Remove lease generation from terminal UPDATE and release a paused old worker after a recovered worker completes.

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

### 1. In-memory background task

**Observable symptom:** Accepted run remains queued forever after API restart.

**Root cause:** Work existed only in process memory.

**Repair:** Commit a durable job before returning 202.

**Permanent regression:** Submit with workers down, restart, then complete.

### 2. Two-step claim

**Observable symptom:** Multiple workers process the same active generation.

**Root cause:** Selection and lease update are not atomic.

**Repair:** Lock/select/update within one transaction using skip-locked.

**Permanent regression:** Multi-worker synchronized claim test.

### 3. Permanent claimed flag

**Observable symptom:** Killed worker strands work indefinitely.

**Root cause:** No lease expiry or recovery.

**Repair:** Use time-bounded leases and reclaim expired rows.

**Permanent regression:** Kill-and-recover proof.

### 4. Lease without fencing

**Observable symptom:** Old worker overwrites newer completion.

**Root cause:** Writes check only job or run ID.

**Repair:** Increment generation and include it in all guarded writes.

**Permanent regression:** Paused stale worker after recovery.

### 5. Non-idempotent artifact creation

**Observable symptom:** Recovery creates duplicate visible artifacts.

**Root cause:** Random identity and unconditional publication.

**Repair:** Content/deterministic identity plus uniqueness and guarded metadata transaction.

**Permanent regression:** Execute one job twice.

### 6. Unbounded retry

**Observable symptom:** Invalid input consumes workers forever.

**Root cause:** All exceptions classified transient.

**Repair:** Separate permanent/retryable conditions and cap attempts.

**Permanent regression:** Poison fixture reaches terminal failure once.

### 7. Long transaction during analysis

**Observable symptom:** Locks and pool connections remain held for job duration.

**Root cause:** Claim transaction wraps processing.

**Repair:** Commit claim, process outside transaction, use short guarded writes.

**Permanent regression:** Inspect active transactions during controlled long analysis.

### 8. Unsafe shutdown success

**Observable symptom:** Terminated process reports work complete without artifact.

**Root cause:** Shutdown path forces terminal state.

**Repair:** Commit only genuine completion; otherwise lease recovery handles it.

**Permanent regression:** Signal during analysis and inspect state/artifact.

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

The Analysis Runs API now has an honest durable execution path: accepted work survives API and worker failure and stale processes cannot rewrite newer truth.

### Increment plan

1. Implement job claim SQL and document lock, order, and lease predicates.
2. Run API with workers stopped; submit and verify durable queued state after restart.
3. Run multiple workers and verify distinct claims.
4. Implement heartbeats, retry classification, attempt cap, and exponential delay.
5. Implement generation-guarded progress and terminal transactions.
6. Kill a worker after claim and after partial progress, then recover after expiry.

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

These are the smallest useful entry points for **Durable Workers and Recovery**.

### Python — `capstone/tracks/python-fastapi/src/analysis_service/worker.py`

```python
READ_CHUNK_SIZE = 64 * 1024


class PermanentJobFailure(RuntimeError):
    """A failure that retrying the same durable input cannot repair."""


class Worker:
    def __init__(
        self,
        repository: Repository,
        store: FileSystemArtifactStore,
        transport: OutboundTransport,
        settings: Settings,
    ) -> None:
        self.repository = repository
        self.store = store
        self.transport = transport
        self.settings = settings
        self.stop = threading.Event()

    def _source_path(self, job: ClaimedJob) -> Path:
        if job.source_kind == "local-file":
            if not job.content_path:
                raise PermanentJobFailure(
                    "ready local dataset has no content path"
                )
            return self.store.path_for(
                job.content_path,
                job.expected_checksum,
            )

        return resolve_remote_fixture(
            self.settings.remote_fixture_root,
            str(job.source.get("uri", "")),
        )

    def _analyze(self, job: ClaimedJob) -> dict[str, object]:
        digest = sha256()
        size = 0
        lines = 0
        last_byte = b""
        chunks = 0

        with self._source_path(job).open("rb") as stream:
            while block := stream.read(READ_CHUNK_SIZE):
                digest.update(block)
                size += len(block)
                lines += block.count(b"\n")
                last_byte = block[-1:]
                chunks += 1
                if chunks % 8 == 0:
                    self.repository.renew_job_lease(
                        job,
                        self.settings.worker_lease_seconds,
                    )

        if size and last_byte != b"\n":
            lines += 1

        actual_checksum = digest.hexdigest()
        expected_checksum = job.expected_checksum or job.source.get(
            "checksumSha256"
        )
        if expected_checksum and actual_checksum != expected_checksum:
```

### TypeScript — `capstone/tracks/typescript-fastify/src/worker.ts`

```typescript
  webhookSignature,
} from "./webhooks.js";

const READ_CHUNK_SIZE = 64 * 1024;

class PermanentJobFailure extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "PermanentJobFailure";
  }
}

export class Worker {
  private stopping = false;

  public constructor(
    private readonly repository: PostgresRepository,
    private readonly store: FileSystemArtifactStore,
    private readonly transport: OutboundWebhookTransport,
    private readonly settings: Settings,
  ) {}

  public stop(): void {
    this.stopping = true;
  }

  public async processOneJob(): Promise<boolean> {
    const job = await this.repository.claimJob(
      this.settings.workerId,
      this.settings.workerLeaseSeconds,
    );
    if (!job) return false;

    try {
      await this.repository.markJobRunning(job);
      const result = await this.analyze(job);
      await this.repository.renewJobLease(
        job,
        this.settings.workerLeaseSeconds,
      );

      // Python and TypeScript publish the exact same canonical bytes.
      const staged = await this.store.stageBytes(
        Buffer.from(canonicalJson(result), "utf8"),
        "application/json",
      );
      const storageKey =
        `artifacts/${staged.checksumSha256.slice(0, 2)}/` +
        staged.checksumSha256;
      await this.store.publish(staged, storageKey);
      await this.repository.completeJob(
        job,
        staged,
        storageKey,
        `${job.algorithm}.json`,
        { algorithm: job.algorithm, artifactCount: 1 },
      );
    } catch (error) {
      if (isLeaseLost(error)) {
        console.warn(
          JSON.stringify({
            event: "stale-worker-result-rejected",
            runId: job.runId,
            generation: job.leaseGeneration,
          }),
```

Compare the two tracks by this invariant: **a lease generation prevents an expired worker from committing effects after another worker takes ownership**. The intended implementation difference is: worker loops and cancellation primitives differ, but claim, renew, recover, and complete transitions must match.

## Module synthesis

The module answer to “What internal machinery makes `202 Accepted` honest after API or worker processes die?” is now executable in the capstone: Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.

## Next in the story

Module 07, [Streaming and Artifact Integrity](../module-07-streaming-artifact-integrity/index.md), asks: *How do large request and response bodies move through the service without unbounded memory or corrupt publication?* The current checkpoint must remain green while that new responsibility is added.
