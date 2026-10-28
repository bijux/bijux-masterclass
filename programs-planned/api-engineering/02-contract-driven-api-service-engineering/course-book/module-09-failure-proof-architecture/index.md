# Module 09 — Failure-Oriented Verification

> **Program stage:** Course 2 of 10 — Implement the promise durably.

> **Central question:** How do tests prove transactions, concurrency, restart, storage, and delivery guarantees rather than only happy paths?

## Where this module fits

Module 08 produced **Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints**. This module extends that result by asking: **How do tests prove transactions, concurrency, restart, storage, and delivery guarantees rather than only happy paths?**

The new capstone increment is **Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs**. It becomes the prerequisite for **Lifecycle and Compatible Release**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Choose the narrowest oracle for each claim.
- Use real PostgreSQL for database concurrency claims.
- Inject failures at transaction and process boundaries.
- Retain planted defects as regression tests.
- Separate deterministic local checks from environment-backed checks.

## Capstone increment

Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs.

## Core model

### Driving question

> How do we prove implementation guarantees rather than infer them from a passing unit suite?

Each claim requires evidence at the narrowest layer that can falsify it, then selected cross-layer proofs. A good proof architecture separates contract, pure policy, database, concurrency, process, storage, network, and release failures instead of hiding them behind one green command.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- which Course 1 operation or representation **Failure-Oriented Verification** must preserve;
- which application or domain component owns the decision;
- where durable state or external effects cross a boundary;
- which counterexample and proof would falsify the result: Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs


### 1. Claim–evidence mapping

Every important claim has an evidence owner. “Run transition table is exhaustive” belongs to pure vector tests; “submission rolls back atomically” belongs to real PostgreSQL; “accepted job survives process death” belongs to a process proof. One test may support several claims, but no claim survives only as prose.

**Counterexample.** A unit test with mocked repository is cited as proof that PostgreSQL unique constraints arbitrate concurrency.

**Evidence direction.** The course proof matrix links each non-compensable completion gate to exact commands and artifacts.

### 2. Narrowest falsifier

Start at the cheapest layer capable of disproving the claim. A pure function should not require Compose; a migration checksum should not require a live API. Cross-layer tests are added where integration itself is the risk.

**Counterexample.** Boot the entire topology to test one ETag parser edge case.

**Evidence direction.** Proof runtime and failure messages identify the responsible layer.

### 3. Real dependency test

Mocks can verify orchestration but cannot reproduce SQL isolation, constraint metadata, file rename behavior, stream cancellation, or HTTP timeout ambiguity. Those claims use real disposable dependencies under controlled conditions.

**Counterexample.** Mock `repository.commit()` to throw and claim rollback is proven.

**Evidence direction.** PostgreSQL and filesystem tests inspect durable state after injected failures.

### 4. Concurrency oracle

A concurrency test needs a logical oracle: expected row counts, unique identities, accepted/rejected outcomes, final version, or lease generation. Merely completing without exception is weak. Barriers and controlled hooks position actors near the critical section.

**Counterexample.** Launch 100 requests and assert all returned some 2xx response.

**Evidence direction.** Idempotency proof asserts one run/job/record plus identical logical response; ETag proof asserts one success.

### 5. Process-failure proof

The process is killed at a named durable boundary, not at arbitrary sleep. Test hooks or database observation identify claim, publication, or commit state. Restart behavior is then checked from external evidence.

**Counterexample.** Sleep 0.5 seconds and kill, producing flaky unknown placement.

**Evidence direction.** Proof reports record boundary reached, PID/container killed, restart, and final database/event state.

### 6. Planted defect discipline

A defect exercise predicts the first failing gate, captures the smallest counterexample, repairs the root cause, and retains a regression. The learner may not merely broaden expected behavior or delete the test.

**Counterexample.** Change the contract to permit duplicate artifacts after the test fails.

**Evidence direction.** Defect records include before/after command output and permanent test location.

### 7. Capability honesty

Proof commands distinguish passed, failed, skipped by explicit user choice, and not executed because a dependency is unavailable. Tool absence must be visible in a capability report and cannot yield a green final proof.

**Counterexample.** Catch `FileNotFoundError: docker` and print “unsupported—pass.”

**Evidence direction.** Final report includes status per capability and fails required completion when any is not executed.

### 8. Evidence immutability

Reports, seed values, fixtures, migration hashes, and minimized counterexamples are versioned. Volatile logs are supplementary. A reviewer can rerun the exact command from a clean checkout and compare the machine-readable result.

**Counterexample.** A screenshot of a terminal with no command, versions, or retained fixture.

**Evidence direction.** Manifest and proof reports include input hashes, tool versions, assertions, and timestamps.

### Design pressure

Choose the principle above most likely to fail in **Failure-Oriented Verification**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Proof matrix

Claim, layer, command, required topology, oracle, report, and limitations.

**Invariant:** Every completion gate has at least one executable owner.

Prediction, injected change, first failure, minimal reproducer, repair, regression location.

**Invariant:** The regression remains after the defect is removed.

Executed status and evidence for each dependency-backed proof.

**Invariant:** Unavailable is never represented as passed.

Composition of deterministic and environment-backed gates from a clean checkout.

**Invariant:** Failure stops completion and names the narrowest failing proof.

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

For **Failure-Oriented Verification**, record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

### Decision 1: Inventory all course claims and assign a proof layer.

### Decision 2: Separate local core proof from PostgreSQL/process proof without weakening completion.

### Decision 3: Design disposable topology reset and safety guards.

### Decision 4: Add deterministic hooks for transaction boundaries, worker claim, publication, and outbox commit.

### Decision 5: Define logical oracles for every concurrency workload.

### Decision 6: Retain seeds and minimized fixtures for generated or race tests.

### Decision 7: Produce JSON reports with commands, versions, assertions, and limitations.

### Decision 8: Run an independent reviewer protocol using only public contract and evidence.

### Worked reasoning pattern

Suppose a learner proposes: “The route can check first, then the repository can write.” Ask:

- Which concurrent request, restart, or dependency failure challenges **Failure-Oriented Verification**?
- What must be decided or committed at one owning boundary?
- Which state survives a lost response or interrupted process?
- Which focused proof answers the module question: How do tests prove transactions, concurrency, restart, storage, and delivery guarantees rather than only happy paths?


### Design review

The design review must challenge the module-specific failure named in the lab and identify the durable oracle that distinguishes a real repair from a cosmetic pass.

## Python implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/python-fastapi/src/analysis_service/
```

### Focus points

1. Use pytest markers to separate core, PostgreSQL, process, and release suites; marker selection is visible in commands.
2. Fixtures create unique disposable database names and artifact roots, then guarantee cleanup.
3. Use `asyncio.Event`/thread barriers or database hooks instead of arbitrary sleeps for race placement.
4. Process tests invoke real CLI/server/worker entry points, not internal methods.
5. Report exact failing assertions and minimized inputs to `capstone/reports`.
6. Compile/import checks remain separate from behavior proof.

### Representative pattern

```python
@pytest.mark.postgres
async def test_same_etag_has_one_winner(project, client_factory, barrier):
    first = client_factory()
    second = client_factory()

    async def patch(client, name):
        await barrier.wait()
        return await client.patch_project(project.id, etag=project.etag, name=name)

    results = await asyncio.gather(patch(first, "A"), patch(second, "B"))
    assert sorted(result.status for result in results) == [200, 412]
    assert await database.project_version(project.id) == project.version + 1
```

The excerpt for **Failure-Oriented Verification** isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## TypeScript implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/typescript-fastify/src/
```

Runtime schemas, TypeScript types, Fastify lifecycle, Node streams, and node-postgres sessions solve different problems. Keep them separate while reading.

### Focus points

1. Vitest integration suites create/close pools per controlled lifecycle and use explicit timeouts only as outer safety limits.
2. Node test hooks or promises coordinate critical sections; `setTimeout` is not the race oracle.
3. Spawn compiled server/worker processes and capture stdout/stderr as supplementary evidence.
4. Use shared JSON scenario and vector files rather than duplicating expected behavior in two languages.
5. Run typecheck separately from tests; a successful compile does not prove runtime validation.
6. Write JSON capability results even when a required external executable is missing, then fail final completion.

### Representative pattern

```typescript
test("concurrent idempotent submissions create one logical run", async () => {
  const gate = new DeferredGate(participants);
  const results = await Promise.all(
    clients.map((client) => gate.run(() => client.submit(request, key))),
  );
  expect(new Set(results.map((r) => r.body.id)).size).toBe(1);
  expect(await database.countRunsForKey(owner, key)).toBe(1);
});
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

1. Database assertions count and inspect logical rows after concurrent/process tests.
2. Test setup refuses database names without the course disposable prefix.
3. Failure hooks may use advisory locks or controlled settings only inside test topology.
4. Migration and release proof begins from clean database and from prior-version state.

### Representative SQL

```sql
-- A concurrency oracle inspects durable cardinality, not only HTTP:
SELECT count(*) FROM analysis_runs WHERE owner_id=$1 AND public_id=$2;
SELECT count(*) FROM run_jobs WHERE run_id=$2;
SELECT count(*) FROM idempotency_records
 WHERE owner_id=$1 AND operation_id='createAnalysisRun' AND idempotency_key=$3;
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

Each claim requires evidence at the narrowest layer that can falsify it, then selected cross-layer proofs. A good proof architecture separates contract, pure policy, database, concurrency, process, storage, network, and release failures instead of hiding them behind one green command.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | claim matrix complete | Write the narrow command and machine-readable oracle. |
| 2 | core proof deterministic | Write the narrow command and machine-readable oracle. |
| 3 | real PostgreSQL proof | Write the narrow command and machine-readable oracle. |
| 4 | barrier concurrency oracles | Write the narrow command and machine-readable oracle. |
| 5 | named process kill boundaries | Write the narrow command and machine-readable oracle. |
| 6 | all planted defects detected | Write the narrow command and machine-readable oracle. |
| 7 | unavailable capability fails completion | Write the narrow command and machine-readable oracle. |
| 8 | reports rerunnable from clean checkout | Write the narrow command and machine-readable oracle. |

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

> Configure final proof to treat missing Docker/PostgreSQL as “unsupported/pass.” The capability audit must reject this false green result.

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

### 1. Mock-proven database guarantee

**Observable symptom:** Unit suite passes while concurrent live writes violate uniqueness/rollback.

**Root cause:** Mock behavior was treated as PostgreSQL behavior.

**Repair:** Add disposable real-database integration and concurrency proof.

**Permanent regression:** Direct row-count and constraint assertions.

### 2. Sleep-driven race

**Observable symptom:** Test passes/fails depending on machine speed.

**Root cause:** Timing guesses place actors near a race.

**Repair:** Use barriers, hooks, or observed durable state.

**Permanent regression:** Repeat stress with deterministic coordination.

### 3. No logical oracle

**Observable symptom:** All requests return but duplicates remain hidden.

**Root cause:** Test asserts process survival, not business outcome.

**Repair:** Assert identities, versions, table counts, events, and artifacts.

**Permanent regression:** Machine-readable final state snapshot.

### 4. Giant end-to-end suite

**Observable symptom:** Failure gives no indication whether parser, SQL, worker, or receiver is wrong.

**Root cause:** All claims delegated to one topology test.

**Repair:** Use layered proofs and a small number of cross-layer paths.

**Permanent regression:** Proof matrix ownership review.

### 5. Skipped means green

**Observable symptom:** Final proof passes on a machine without PostgreSQL or Node dependencies.

**Root cause:** Unavailable capabilities are swallowed.

**Repair:** Report not-executed and fail required completion.

**Permanent regression:** Run doctor in deliberately missing-tool environment.

### 6. Deleted defect evidence

**Observable symptom:** The fix cannot be reviewed and future regressions reappear.

**Root cause:** Only final passing code retained.

**Repair:** Keep minimized regression and defect record without preserving unsafe production branch.

**Permanent regression:** Repository audit checks defect-to-test map.

### 7. Unsafe test database

**Observable symptom:** Proof modifies developer or shared data.

**Root cause:** No disposable-name and ownership guard.

**Repair:** Require unique course prefix, explicit opt-in URL, and teardown.

**Permanent regression:** Safety test rejects ordinary database URL.

### 8. Screenshot evidence

**Observable symptom:** Reviewer cannot rerun or inspect inputs.

**Root cause:** Visual terminal output substitutes for machine-readable proof.

**Repair:** Store command, versions, fixture hashes, assertions, and JSON result.

**Permanent regression:** Manifest verifies report inputs and scripts.

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

All prior module claims become an explicit, rerunnable evidence architecture rather than a collection of informal green tests.

### Increment plan

1. Create the complete claim-to-proof matrix for all non-compensable gates.
2. Implement local `core-proof` and environment-backed proof groups.
3. Build safe disposable PostgreSQL and artifact-root fixtures.
4. Add barrier-based idempotency/ETag tests and named worker/outbox process hooks.
5. Run every planted defect one at a time and predict the first failing gate before execution.
6. Minimize each counterexample and map it to a permanent regression.

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

The **Failure-Oriented Verification** increment must preserve the frozen API and every earlier durability invariant while delivering this result: Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs The comparison track must expose the same public outcomes even when internal libraries and control flow differ.


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

These are the smallest useful entry points for **Failure-Oriented Verification**.

### Python — `capstone/tests/runtime/proof_runner.py`

```text
# Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
COMPOSE = CAPSTONE / "compose.yaml"


class ProofFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class Track:
    name: str
    api_base: str
    database_url: str
    worker_service: str
    api_service: str


def track_config(name: str) -> Track:
    if name == "python":
        return Track(
            name="python",
            api_base=os.getenv("PYTHON_API_BASE", "http://127.0.0.1:58000"),
            database_url=os.getenv(
                "PYTHON_TEST_DATABASE_URL",
                "postgresql://analysis:analysis@127.0.0.1:55432/analysis_python",
            ),
            worker_service="python-worker",
            api_service="python-api",
        )
    if name == "typescript":
        return Track(
            name="typescript",
            api_base=os.getenv("TYPESCRIPT_API_BASE", "http://127.0.0.1:58001"),
            database_url=os.getenv(
                "TYPESCRIPT_TEST_DATABASE_URL",
                "postgresql://analysis:analysis@127.0.0.1:55432/analysis_typescript",
            ),
            worker_service="typescript-worker",
            api_service="typescript-api",
        )
    raise ProofFailure("track must be python or typescript")


@dataclass
class Response:
    status: int
    headers: dict[str, str]
    body: bytes

    def json(self) -> Any:
        if not self.body:
            return None
        try:
            return json.loads(self.body)
        except json.JSONDecodeError as exc:
            raise ProofFailure(
```

### TypeScript — `capstone/tracks/typescript-fastify/test-core/domain.test.mjs`

```yaml
});

test("cancellation is requested before it is observed", () => {
  const requested = evolve(
    { state: "running", progress: 40, cancellationRequested: false },
    "request-cancel",
  );
  assert.equal(requested.state, "running");
  assert.equal(evolve(requested, "observe-cancel").state, "canceled");
});

test("retry delay is bounded", () => {
  assert.equal(retryDelaySeconds(99), 300);
});

test("canonical JSON rejects cross-language number ambiguity", () => {
  assert.throws(() => canonicalJson({ value: 1.5 }));
  assert.throws(() => canonicalJson({ value: 9_007_199_254_740_992 }));
});

test("canonical JSON sorts Unicode names by code point", () => {
  assert.equal(canonicalJson({ "😀": 1, "￿": 2 }), '{"￿":2,"😀":1}');
});
```

Compare the two tracks by this invariant: **a planted defect must cause the smallest relevant oracle to fail before the repair can count as evidence**. The intended implementation difference is: test runners differ; shared scenarios and durable observations remain provider-neutral.

## Module synthesis

You are ready to leave this module when you can **Choose the narrowest oracle for each claim, Use real PostgreSQL for database concurrency claims, and Inject failures at transaction and process boundaries** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Assemble a proof runner that detects every planted defect: broken transaction, unstable cursor, lost replay, stale update, worker overwrite, unbounded upload, unsigned webhook, and cross-owner leak** and requiring the following oracle: **Each planted defect fails the gate that claims to detect it; disabling PostgreSQL or Node changes status to not-executed rather than green.**

The cumulative platform now includes **Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Lifecycle and Compatible Release](../module-10-lifecycle-compatible-release/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
