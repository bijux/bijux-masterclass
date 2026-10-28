# Module 10 — Lifecycle and Compatible Release

> **Program stage:** Course 2 of 6 — Make the promise durable.

> **Central question:** How can old and new service versions coexist through a database change and still preserve the public contract?

## Where this module fits

Implement configuration validation, health states, graceful shutdown, and expand–backfill–enforce release sequencing. You arrive from Module 09 with all earlier checkpoints still green. The Course 1 handoff is fixed. This course may change internal architecture and add a compatible API release, but it may not solve an implementation problem by quietly weakening the public contract. The result closes the course and produces the handoff to **API Security Engineering**.

## Learning outcomes

- Distinguish startup, liveness, readiness, and draining.
- Order application and schema releases safely.
- Keep old and new service versions compatible during expansion.
- Define the rollback boundary explicitly.
- Release API 1.2 without breaking API 1.1 consumers.

## Capstone result

Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof.

Course 2 ends with a release-ready service, migrations 001–005, and an additive API 1.2 contract.

## Core model

### Driving question

> Can the service be built, started, upgraded, stopped, rolled back, and recovered without violating its contract or data?

Release readiness is controlled lifecycle and compatibility, not an infrastructure collection. Configuration validation, health semantics, graceful drain, immutable images, ordered migrations, and expand–backfill–enforce are the bounded operational endpoint of this course.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- the public behavior inherited from Course 1;
- the application or domain decision owner;
- the durable database, worker, storage, or delivery mechanism;
- the proof that exposes failure after retry, concurrency, or restart.


### 1. Configuration contract

Required settings, types, ranges, secret sources, paths, and environment-specific restrictions are validated at startup. Defaults are safe for local course use but not silently reused for production-designated environments. Configuration appears in evidence without exposing secret values.

**Counterexample.** Discover a malformed database URL on the first request or log webhook secrets during startup.

**Evidence direction.** Startup matrix covers missing, malformed, unsafe, and valid configurations.

### 2. Liveness versus readiness

Liveness reports that the process is functioning and should not be restarted merely because a dependency is temporarily unavailable. Readiness reports whether the instance should receive its role’s work. The API may be unready when migrations are missing; a worker may be unready when it cannot reach PostgreSQL.

**Counterexample.** One `/health` query performs a full workflow and causes restart loops during database maintenance.

**Evidence direction.** Dependency interruption changes readiness predictably while process remains live.

### 3. Graceful drain

Shutdown first stops admission, then waits a bounded period for active requests or work, closes resources, and exits. Timeout behavior is explicit. Streams and uploads receive cancellation and cleanup; workers stop claiming before handling current authority.

**Counterexample.** Signal handler immediately calls `process.exit()` or `os._exit()`.

**Evidence direction.** Long request/upload and active job shutdown proofs inspect final state and residue.

### 4. Immutable build artifact

The container/image is built from pinned dependencies and source, runs as non-root, writes only declared volumes, and does not install packages at startup. The same artifact is promoted between release steps; configuration changes outside it.

**Counterexample.** Container entrypoint runs `pip install -U` or `npm install` on every boot.

**Evidence direction.** Image metadata, lock/pin files, non-root identity, and clean build proof.

### 5. Migration ordering

Schema migrations are an explicit release step with one owner. Application startup verifies required schema but does not let every replica race to mutate production. Expansion precedes new code when old code tolerates it; enforcement follows old-code removal.

**Counterexample.** Every API replica automatically applies all migrations during startup.

**Evidence direction.** Release script records migration target and prevents code requiring a later schema from becoming ready.

### 6. Version coexistence

During rolling release, old and new application versions may access the same expanded schema. New code must write data old code tolerates; old code must not erase new fields. The course runs service 1.0 and service 1.1 sequentially/concurrently against migration phases.

**Counterexample.** New code assumes `result_summary NOT NULL` before backfill and old instances are gone.

**Evidence direction.** Compatibility matrix executes both versions at each permitted phase.

### 7. Rollback boundary

Application rollback is possible while schema remains in its backward-compatible expanded form. Destructive enforcement is delayed because database rollback may be impossible or expensive. Release notes state the last safe rollback point.

**Counterexample.** Drop/rename old column in the same deployment that first uses the replacement.

**Evidence direction.** Deploy service 1.1, create data, return to service 1.0 code, and complete predecessor workflows.

### 8. Operational evidence package

The final artifact includes build commands, topology, configuration schema, health semantics, migration plan, rollback plan, runbook, proof reports, tool versions, and manifest. It does not claim unexecuted cloud or scale properties.

**Counterexample.** “Production ready” stated because Compose starts once.

**Evidence direction.** Final defense traces every operational claim to an executed command or explicit limitation.

### Design pressure

Choose the principle above most likely to fail in **Lifecycle and Compatible Release**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Release phase

Known combination of contract version, application version, and migration target.

**Invariant:** Every permitted phase has a tested compatibility statement.

Role-specific checks required before accepting requests or jobs.

**Invariant:** It is cheap, bounded, and non-destructive.

Stop admission, await bounded active work, clean resources, exit.

**Invariant:** No success is fabricated to accelerate shutdown.

Concrete detection, diagnostic, mitigation, and recovery commands for known failures.

**Invariant:** A fresh operator can execute it without undocumented knowledge.

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

### Decision 1: Enumerate configuration with type, secret status, default, and failure behavior.

### Decision 2: Define separate liveness/readiness for API, worker, receiver, and database.

### Decision 3: Define signal sequence and maximum drain time per process role.

### Decision 4: Pin runtime/dependencies and run containers as non-root with declared writable paths.

### Decision 5: Define one migration owner and schema-version readiness check.

### Decision 6: Write service 1.0/service 1.1 compatibility matrix for migrations 002–005.

### Decision 7: Define the last safe application rollback point and delayed enforcement.

### Decision 8: Create runbook and final evidence manifest without overstating scope.

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

1. Parse `Settings` once before app construction and validate filesystem/database/network restrictions.
2. Use FastAPI lifespan for pool/transport startup and shutdown; route handlers do not own shared resource closure.
3. Run Uvicorn with signal-aware graceful timeout and explicit worker process model for the course topology.
4. API readiness verifies migration target and minimal database query with a short timeout.
5. Worker signal handler stops claim loop before pool closure and relies on lease recovery when necessary.
6. Build wheel/install in image stage; runtime container does not mutate dependencies.

### Representative pattern

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings.from_environment()   # fail before readiness
    await resources.open(settings)
    await resources.require_schema(settings.required_schema)
    app.state.ready = True
    try:
        yield
    finally:
        app.state.ready = False              # stop admission first
        await resources.drain(settings.shutdown_timeout)
        await resources.close()
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

1. Validate environment into an immutable `Settings` object before `buildApp()`.
2. Use Fastify `onClose`/`close()` to stop admission and close pool/transport resources.
3. Handle `SIGTERM`/`SIGINT` once, await drain, and set nonzero exit on timeout/failure.
4. Readiness checks required migration target through a short pooled query.
5. Compile TypeScript during image build; production image runs emitted JavaScript without dev tooling where practical.
6. Run as non-root and restrict writes to artifact/runtime volumes.

### Representative pattern

```typescript
const shutdown = async (signal: NodeJS.Signals): Promise<void> => {
  admission.close();
  const timer = AbortSignal.timeout(settings.shutdownTimeoutMs);
  await Promise.race([app.close(), aborted(timer)]);
  await pool.end();
  process.exitCode = 0;
};
process.once("SIGTERM", () => void shutdown("SIGTERM"));
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

1. Migrations 003 expand optional result summary, 004 backfills, and 005 contracts/enforces final shape.
2. Schema migration ledger lets readiness compare required application target.
3. Old/new compatibility is tested at each allowed migration target.
4. Rejected breaking API 1.2.0 candidate contract fixture demonstrates that schema compatibility does not excuse public breaking change.

### Representative SQL

```sql
-- 003 expand: nullable field accepted by old and new code
ALTER TABLE analysis_runs ADD COLUMN result_summary jsonb;
-- 004 backfill existing terminal rows
UPDATE analysis_runs SET result_summary = '{}'::jsonb
 WHERE status='completed' AND result_summary IS NULL;
-- 005 contract, only after old code is retired
ALTER TABLE analysis_runs
  ADD CONSTRAINT completed_summary_required
  CHECK (status <> 'completed' OR result_summary IS NOT NULL) NOT VALID;
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

Release readiness is controlled lifecycle and compatibility, not an infrastructure collection. Configuration validation, health semantics, graceful drain, immutable images, ordered migrations, and expand–backfill–enforce are the bounded operational endpoint of this course.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | startup config matrix | Write the narrow command and machine-readable oracle. |
| 2 | role-specific health semantics | Write the narrow command and machine-readable oracle. |
| 3 | graceful API drain | Write the narrow command and machine-readable oracle. |
| 4 | worker recovery on shutdown | Write the narrow command and machine-readable oracle. |
| 5 | non-root reproducible build | Write the narrow command and machine-readable oracle. |
| 6 | migration owner/target verified | Write the narrow command and machine-readable oracle. |
| 7 | service 1.0/service 1.1 coexistence | Write the narrow command and machine-readable oracle. |
| 8 | application rollback before contract | Write the narrow command and machine-readable oracle. |

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

> Make migration 003 immediately require a non-null field that service 1.0 does not write. The coexistence proof must fail before the migration can be accepted.

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

### 1. Late configuration failure

**Observable symptom:** Process becomes ready then fails on first use of malformed setting.

**Root cause:** Environment reads are scattered and lazy.

**Repair:** Parse/validate complete configuration before readiness.

**Permanent regression:** Startup invalid-setting matrix.

### 2. Health endpoint overload

**Observable symptom:** Dependency outage triggers restart storms or health checks cause load.

**Root cause:** Liveness conflated with full dependency readiness.

**Repair:** Separate cheap liveness from bounded role readiness.

**Permanent regression:** Database interruption behavior test.

### 3. Immediate exit

**Observable symptom:** Uploads leave staging files and workers abandon claims without orderly recovery.

**Root cause:** Signals call hard exit.

**Repair:** Stop admission, cancel/await cleanup, close resources with deadline.

**Permanent regression:** Signal during long request and job.

### 4. Migration race at startup

**Observable symptom:** Multiple replicas contend or apply incompatible history.

**Root cause:** Every application instance owns schema mutation.

**Repair:** Run explicit single migration job; application only verifies target.

**Permanent regression:** Concurrent startup with migration owner disabled/enabled.

### 5. Expand and contract together

**Observable symptom:** Old version crashes during rollout or rollback impossible.

**Root cause:** Destructive constraint/drop occurs before coexistence ends.

**Repair:** Separate expand, code, backfill, and delayed enforcement phases.

**Permanent regression:** Old/new compatibility matrix.

### 6. Mutable startup install

**Observable symptom:** Same release starts with different dependency versions or fails without registry.

**Root cause:** Dependencies installed/upgraded at runtime.

**Repair:** Build immutable pinned artifact and run offline.

**Permanent regression:** Network-disabled container startup.

### 7. Root and broad writes

**Observable symptom:** Compromise can modify application/runtime filesystem widely.

**Root cause:** Container defaults to root and no write boundary.

**Repair:** Non-root user, read-only source, declared writable volumes.

**Permanent regression:** Identity and write-permission checks.

### 8. Production-ready overclaim

**Observable symptom:** Course claims autoscaling, HA, backup recovery, or SLO evidence not tested.

**Root cause:** Compose success is generalized beyond evidence.

**Repair:** State bounded operational baseline and explicit exclusions.

**Permanent regression:** Final defense claim-to-evidence audit.

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

The selected reference track becomes a release-ready modular service with verified lifecycle and one compatible evolution, while all Course 1 behavior remains conformant.

### Increment plan

1. Finalize configuration schema, startup validation, and role-specific health routes.
2. Implement graceful API and worker shutdown with bounded drain and cleanup.
3. Build selected-track image from pinned dependencies and verify non-root/write boundaries.
4. Deploy PostgreSQL, receiver, API, and worker from clean state; run predecessor workflow.
5. Apply migration 003, run old and new versions in the allowed coexistence window, and create data.
6. Apply backfill 004, roll application code back to service 1.0, and rerun frozen clients.

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

These are the smallest useful entry points for **Lifecycle and Compatible Release**.

### Python — `capstone/tracks/python-fastapi/src/analysis_service/config.py`

```python


@dataclass(frozen=True, slots=True)
class Settings:
    database_url: str
    artifact_root: Path
    webhook_transport_base: str
    webhook_encryption_key: str
    callback_signing_secret: str
    remote_fixture_root: Path
    worker_id: str
    worker_lease_seconds: int = 15
    upload_limit_bytes: int = 1_048_576
    service_release: str = "1.0"
    environment: str = "development"

    @property
    def public_api_version(self) -> str:
        """Public contract implemented by this executable service release."""

        return SERVICE_TO_API_VERSION[self.service_release]

    @property
    def exposes_api_1_2(self) -> bool:
        return self.service_release == "1.1"

    @classmethod
    def from_env(cls) -> "Settings":
        service_release = os.getenv("SERVICE_RELEASE", "1.0")
        value = cls(
            database_url=os.getenv(
                "DATABASE_URL",
                "postgresql://analysis:analysis@127.0.0.1:55432/analysis_python",
            ),
            artifact_root=Path(
                os.getenv("ARTIFACT_ROOT", ".runtime/artifacts")
            ).resolve(),
            webhook_transport_base=os.getenv(
                "WEBHOOK_TRANSPORT_BASE",
                "http://127.0.0.1:58080",
            ).rstrip("/"),
            webhook_encryption_key=os.getenv(
                "WEBHOOK_ENCRYPTION_KEY",
                COURSE_ENCRYPTION_KEY,
            ),
            callback_signing_secret=os.getenv(
                "CALLBACK_SIGNING_SECRET",
                COURSE_CALLBACK_SECRET,
            ),
            remote_fixture_root=Path(
                os.getenv("REMOTE_FIXTURE_ROOT", "fixtures/remote")
            ).resolve(),
            worker_id=os.getenv("WORKER_ID", f"python-worker-{os.getpid()}"),
            worker_lease_seconds=_positive_int("WORKER_LEASE_SECONDS", 15),
            upload_limit_bytes=_positive_int("UPLOAD_LIMIT_BYTES", 1_048_576),
```

### TypeScript — `capstone/tracks/typescript-fastify/src/config.ts`

```typescript
import { mkdirSync } from "node:fs";
import { resolve } from "node:path";

export type ServiceRelease = "1.0" | "1.1";

export type Settings = Readonly<{
  databaseUrl: string;
  artifactRoot: string;
  remoteFixtureRoot: string;
  webhookTransportBase: string;
  webhookEncryptionKey: string;
  callbackSigningSecret: string;
  workerId: string;
  workerLeaseSeconds: number;
  uploadLimitBytes: number;
  serviceRelease: ServiceRelease;
  publicApiVersion: "1.1.0" | "1.2.0";
  environment: string;
}>;

const COURSE_ENCRYPTION_KEY = "course-training-encryption-key";
const COURSE_CALLBACK_SECRET = "course-callback-signing-secret";

export function settingsFromEnvironment(): Settings {
  const rawRelease = process.env["SERVICE_RELEASE"] ?? "1.0";
  if (rawRelease !== "1.0" && rawRelease !== "1.1") {
    throw new Error("SERVICE_RELEASE must be 1.0 or 1.1");
  }

  const settings: Settings = {
    databaseUrl:
      process.env["DATABASE_URL"] ??
      "postgresql://analysis:analysis@127.0.0.1:55432/analysis_typescript",
    artifactRoot: resolve(
      process.env["ARTIFACT_ROOT"] ?? ".runtime/artifacts",
    ),
    remoteFixtureRoot: resolve(
      process.env["REMOTE_FIXTURE_ROOT"] ?? "fixtures/remote",
    ),
    webhookTransportBase: (
      process.env["WEBHOOK_TRANSPORT_BASE"] ?? "http://127.0.0.1:58080"
    ).replace(/\/$/, ""),
    webhookEncryptionKey:
      process.env["WEBHOOK_ENCRYPTION_KEY"] ?? COURSE_ENCRYPTION_KEY,
    callbackSigningSecret:
      process.env["CALLBACK_SIGNING_SECRET"] ?? COURSE_CALLBACK_SECRET,
    workerId:
      process.env["WORKER_ID"] ?? `typescript-worker-${process.pid}`,
    workerLeaseSeconds: positiveInteger("WORKER_LEASE_SECONDS", 15),
    uploadLimitBytes: positiveInteger("UPLOAD_LIMIT_BYTES", 1_048_576),
    serviceRelease: rawRelease,
    publicApiVersion: rawRelease === "1.1" ? "1.2.0" : "1.1.0",
    environment: process.env["APP_ENV"] ?? "development",
  };
```

Compare the two tracks by this invariant: **old and new service versions coexist during expand/backfill/enforce without weakening API 1.1 or API 1.2 behavior**. The intended implementation difference is: configuration loaders differ; release identity, migration order, health, and rollback limits are shared.

## Module synthesis

The module answer to “Can the service start, migrate, coexist, drain, roll back, and recover without violating its public contract or data?” is now executable in the capstone: Course 2 ends with a release-ready service, migrations 001–005, and an additive API 1.2 contract.

## Course exit

The ten module results now satisfy this course promise: A PostgreSQL-backed service with transactions, durable jobs, bounded artifacts, reliable webhooks, and a compatible API 1.2 release. The next course is **API Security Engineering**; it consumes the outgoing handoff rather than reinterpreting completed work.

## Next in the story

This course now has the mechanism needed for its final defense. The outgoing handoff becomes the immutable starting point for **Course 3 — API Security Engineering**, where the responsibility becomes: Preserve the API and durable-service guarantees when callers, credentials, inputs, destinations, and dependencies are not trusted by default.
