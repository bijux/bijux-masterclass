# Module 02 — Domain State and Invariants

> **Program stage:** Course 2 of 10 — Implement the promise durably.

> **Central question:** Which state transitions and invariants must remain true regardless of framework or database?

## Where this module fits

Module 01 produced **Create transport, application, and adapter boundaries for the fixed operation ledger**. This module extends that result by asking: **Which state transitions and invariants must remain true regardless of framework or database?**

The new capstone increment is **Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior**. It becomes the prerequisite for **Relational Modeling and Migrations**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Model legal and illegal state transitions.
- Distinguish entities, values, commands, and outcomes pragmatically.
- Keep domain failures stable and transport-neutral.
- Control time and identifiers in tests.
- Prove invariants with pure state-transition tests.

## Capstone increment

Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior.

## Core model

### Driving question

> Which rules must remain true regardless of framework, database, worker, or deployment?

A state machine is not a status string plus scattered conditionals. Legal transitions, terminal-state immutability, progress monotonicity, cancellation semantics, and artifact availability belong to explicit deterministic policy.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- which Course 1 operation or representation **Domain State and Invariants** must preserve;
- which application or domain component owns the decision;
- where durable state or external effects cross a boundary;
- which counterexample and proof would falsify the result: Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior


### 1. Invariant ownership

An invariant has one authoritative implementation. Database constraints may reinforce it and transport validation may reject malformed input earlier, but neither should invent a different rule. The state transition policy is the reference for legal run changes.

**Counterexample.** The route permits `running → cancelled`, the worker permits `running → completed`, and a SQL trigger applies a third rule without tests connecting them.

**Evidence direction.** A generated transition matrix tests every source/target pair and compares both tracks.

### 2. State versus event

State summarizes the current truth; an event records that a transition occurred. `status=completed` is not the same object as `analysis.run.completed`. Events need stable identifiers and timestamps because streams and webhooks may replay them.

**Counterexample.** Reconstructing event identifiers from current status, making duplicate delivery impossible to distinguish.

**Evidence direction.** Tests assert one state transition creates one persisted event and repeated reads do not create events.

### 3. Terminal immutability

Completed, failed, and cancelled runs are terminal in this course. Progress, result, failure, and cancellation fields have state-specific constraints. Terminal immutability prevents late workers or retries from rewriting accepted history.

**Counterexample.** A stale worker changes a cancelled run to completed because it still holds an old in-memory object.

**Evidence direction.** Transition tests reject every edge leaving a terminal state; later lease fencing proves stale processes cannot bypass it.

### 4. Monotonic progress

Progress may remain the same or increase within a running execution, but it may not decrease. It reaches 100 only with completion. This rule is visible in SSE/NDJSON events and therefore cannot be a UI convention.

**Counterexample.** A retry restarts at progress 0 and overwrites the persisted progress of the original attempt.

**Evidence direction.** Property-style tests generate progress sequences and find the first decreasing or premature-100 value.

### 5. Cancellation request versus observation

The API records a cancellation request. A worker later observes it before a commit boundary and transitions to cancelled. If completion commits first, cancellation returns a conflict. This gives a deterministic rule for a real race.

**Counterexample.** The HTTP handler sets status to cancelled while the worker continues writing artifacts.

**Evidence direction.** Pure race tables enumerate request-before-commit and commit-before-request outcomes.

### 6. Artifact availability rule

Artifacts exist only for completed runs. An empty list before completion would ambiguously mean no result versus not ready. The public contract therefore reports lifecycle conflict until completion and returns persisted artifacts afterward.

**Counterexample.** Creating a placeholder artifact row at submission time and exposing it as downloadable.

**Evidence direction.** Direct policy tests plus HTTP scenarios for queued, running, failed, cancelled, and completed runs.

### 7. Error classification

The same English sentence can map to different protocol meaning. A malformed ID is validation, an absent owned resource is not found, a forbidden transition is conflict, a missing `If-Match` is precondition required, and a stale validator is precondition failed.

**Counterexample.** Returning 400 for every application failure because it is “the client’s fault.”

**Evidence direction.** An error catalog maps each application condition to one stable type, status, and machine code.

### 8. Pure policy as executable specification

A deterministic transition function accepts current state and command and returns a new snapshot or stable failure. It is small enough for exhaustive testing and language parity. Persistence and HTTP then execute and expose the decision.

**Counterexample.** The only documentation is a flowchart that no test imports and no worker follows.

**Evidence direction.** Both language tracks load shared state-machine vectors and produce identical outcomes.

### Design pressure

Choose the principle above most likely to fail in **Domain State and Invariants**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Run snapshot

Immutable view containing state, progress, cancellation request, result/failure information, and version.

**Invariant:** Fields are internally coherent for the state.

Intent such as start, report progress, complete, fail, request cancellation, or observe cancellation.

**Invariant:** A command does not mutate the snapshot in place.

Validates source state and command, computes the next snapshot, and names the event to emit.

**Invariant:** No I/O and no wall-clock reads occur inside the decision.

Application conditions map to stable HTTP Problem Details only at the transport edge.

**Invariant:** Changing detail text does not change the machine discriminator.

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

For **Domain State and Invariants**, record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

### Decision 1: Write the full run transition table including self-transitions that are explicitly rejected.

### Decision 2: Define state-specific field constraints for progress, result, failure, and cancellation.

### Decision 3: Decide which commands are idempotent and what repeated application returns.

### Decision 4: Define the cancellation race without referring to thread timing.

### Decision 5: Separate current state from emitted event records.

### Decision 6: Classify every failure through the shared error catalog.

### Decision 7: Create deterministic vectors consumed by both language tracks.

### Decision 8: Prove database-independent policy before adding persistence.

### Worked reasoning pattern

Suppose a learner proposes: “The route can check first, then the repository can write.” Ask:

- Which concurrent request, restart, or dependency failure challenges **Domain State and Invariants**?
- What must be decided or committed at one owning boundary?
- Which state survives a lost response or interrupted process?
- Which focused proof answers the module question: Which state transitions and invariants must remain true regardless of framework or database?


### Design review

The design review must challenge the module-specific failure named in the lab and identify the durable oracle that distinguishes a real repair from a cosmetic pass.

## Python implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/python-fastapi/src/analysis_service/
```

### Focus points

1. Use `RunState`, `RunSnapshot`, `require_transition()`, and `evolve()` as the pure policy center.
2. Prefer frozen dataclasses or immutable Pydantic-independent values for snapshots.
3. Raise named application failures rather than `ValueError` for expected illegal commands.
4. Generate a Cartesian transition test across all states and commands.
5. Keep timestamps and event IDs outside `evolve()`; pass them when persistence records the accepted transition.
6. Use Python `StrEnum` only as an internal representation; serialize the exact contract strings.

### Representative pattern

```python
def evolve(snapshot: RunSnapshot, command: RunCommand) -> Transition:
    match (snapshot.state, command.kind):
        case (RunState.QUEUED, "start"):
            return Transition(snapshot.running(progress=0), "analysis.run.started")
        case (RunState.RUNNING, "progress") if command.progress >= snapshot.progress:
            return Transition(snapshot.running(progress=command.progress), "analysis.run.progressed")
        case (RunState.RUNNING, "complete"):
            return Transition(snapshot.completed(progress=100), "analysis.run.completed")
        case (RunState.QUEUED | RunState.RUNNING, "cancel-observed"):
            return Transition(snapshot.cancelled(), "analysis.run.cancelled")
        case _:
            raise InvalidTransition(snapshot.state, command.kind)
```

The excerpt for **Domain State and Invariants** isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## TypeScript implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/typescript-fastify/src/
```

Runtime schemas, TypeScript types, Fastify lifecycle, Node streams, and node-postgres sessions solve different problems. Keep them separate while reading.

### Focus points

1. Use discriminated unions for commands and snapshots where they improve exhaustiveness.
2. Enable strict checking and use a `never` exhaustiveness guard for command handling.
3. Return a new object from `evolveRun()` rather than mutating shared state.
4. Test the same JSON vectors used by Python.
5. Do not rely on compile-time unions for untrusted request values; runtime schemas still validate them.
6. Keep error classes independent of Fastify replies.

### Representative pattern

```typescript
export function evolveRun(snapshot: RunSnapshot, command: RunCommand): Transition {
  switch (command.kind) {
    case "start": return requireState(snapshot, "queued").start();
    case "progress": return requireMonotonicProgress(snapshot, command.progress);
    case "complete": return requireState(snapshot, "running").complete();
    case "cancel-observed": return requireCancellable(snapshot).cancel();
    default: return assertNever(command);
  }
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

1. Preview check constraints that can reinforce state-specific invariants without duplicating the entire transition graph.
2. Plan a version column so accepted transitions can later be conditional and stale workers can be fenced.
3. Plan an append-only event table keyed by run and monotonic position.

### Representative SQL

```sql
CHECK (status IN ('queued','running','completed','failed','cancelled')),
CHECK (progress BETWEEN 0 AND 100),
CHECK ((status = 'completed') = (completed_at IS NOT NULL)),
CHECK (status <> 'completed' OR progress = 100)
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

A state machine is not a status string plus scattered conditionals. Legal transitions, terminal-state immutability, progress monotonicity, cancellation semantics, and artifact availability belong to explicit deterministic policy.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | all source/target transitions classified | Write the narrow command and machine-readable oracle. |
| 2 | terminal states have no outgoing edges | Write the narrow command and machine-readable oracle. |
| 3 | progress never decreases | Write the narrow command and machine-readable oracle. |
| 4 | 100 progress requires completion | Write the narrow command and machine-readable oracle. |
| 5 | cancellation race table deterministic | Write the narrow command and machine-readable oracle. |
| 6 | artifact access follows run state | Write the narrow command and machine-readable oracle. |
| 7 | error catalog complete | Write the narrow command and machine-readable oracle. |
| 8 | both languages consume shared vectors | Write the narrow command and machine-readable oracle. |

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

> Assign `status = completed` directly in one worker path. The repair must make bypass impossible or mechanically detectable, not merely remove this one line.

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

### 1. Status as free string

**Observable symptom:** Unexpected states appear after typo or unchecked assignment.

**Root cause:** State was stored without a closed vocabulary or transition owner.

**Repair:** Use a closed enum plus explicit transition function and database check constraint.

**Permanent regression:** Reject unknown states at transport, domain, and persistence boundaries.

### 2. Scattered transition checks

**Observable symptom:** HTTP and worker disagree about legal transitions.

**Root cause:** Each caller implemented its own conditionals.

**Repair:** Route all state changes through one pure policy.

**Permanent regression:** Shared transition matrix used by every caller.

### 3. Terminal rewrite

**Observable symptom:** A completed run later becomes failed or cancelled.

**Root cause:** Late process updates are unconditional.

**Repair:** Make terminal immutability part of policy and later add version/lease guards.

**Permanent regression:** Attempt every outgoing terminal edge.

### 4. Progress rollback

**Observable symptom:** A client sees 70, then 20.

**Root cause:** Worker retries overwrite progress without monotonic validation.

**Repair:** Reject decreasing progress and bind updates to the active lease generation.

**Permanent regression:** Generated increasing/decreasing sequences.

### 5. Cancellation fiction

**Observable symptom:** API reports cancelled while computation and artifact publication continue.

**Root cause:** Request and observation were modeled as one instantaneous action.

**Repair:** Persist cancellation request; worker observes it before commit.

**Permanent regression:** Race-table and process test for both orderings.

### 6. Placeholder artifact

**Observable symptom:** A queued run exposes a URL that later 404s or serves incomplete data.

**Root cause:** Availability was modeled independently from terminal state and publication.

**Repair:** Create artifact metadata only after atomic publication and completion transaction.

**Permanent regression:** Assert conflict before completion and integrity after.

### 7. Generic 400 mapping

**Observable symptom:** Clients cannot distinguish conflict, precondition, and validation recovery.

**Root cause:** Application failures were collapsed into one status.

**Repair:** Use stable failure classes and error catalog mappings.

**Permanent regression:** Table-driven problem response tests.

### 8. Impure transition

**Observable symptom:** State tests sleep or depend on current time and random IDs.

**Root cause:** Decision code creates timestamps/events itself.

**Repair:** Return transition intent; supply time and identity at orchestration.

**Permanent regression:** Exact deterministic vector comparisons.

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

The Analysis Run lifecycle becomes an executable policy shared by HTTP, worker, streams, artifacts, and webhooks. No later module is allowed to mutate status outside this path.

### Increment plan

1. Complete the run state and command matrix before editing provider code.
2. Implement pure transition policy and state-specific field validation in the primary track.
3. Load shared vectors and execute them in both local cores.
4. Add project and dataset invariants needed by later persistence.
5. Build the application failure catalog and one transport translator.
6. Run direct tests for legal, illegal, repeated, and boundary commands.

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

The **Domain State and Invariants** increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior The comparison track must expose the same public outcomes even when internal libraries and control flow differ.


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

These are the smallest useful entry points for **Domain State and Invariants**.

### Python — `capstone/tracks/python-fastapi/src/analysis_service/domain.py`

```python
MAX_POSTGRES_BIGINT = 9_223_372_036_854_775_807


class RunState(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


TERMINAL_STATES = frozenset(
    {RunState.COMPLETED, RunState.FAILED, RunState.CANCELED}
)

TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.QUEUED: frozenset({RunState.RUNNING, RunState.CANCELED}),
    RunState.RUNNING: frozenset(
        {RunState.COMPLETED, RunState.FAILED, RunState.CANCELED}
    ),
    RunState.COMPLETED: frozenset(),
    RunState.FAILED: frozenset(),
    RunState.CANCELED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class StoredResponse:
    status: int
    headers: dict[str, str]
    body: dict[str, Any]
    replay: bool


@dataclass(frozen=True, slots=True)
class RunSnapshot:
    state: RunState
    progress: int
    cancellation_requested: bool = False


MAX_SAFE_JSON_INTEGER = 9_007_199_254_740_991


def _validate_canonical_value(value: Any) -> None:
    """Validate the deliberately small cross-language JSON profile."""

    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_JSON_INTEGER:
            raise TypeError("canonical JSON integers must be JavaScript-safe")
        return
    if isinstance(value, float):
        raise TypeError("canonical JSON profile rejects floating-point values")
    if isinstance(value, list):
        for item in value:
            _validate_canonical_value(item)
        return
    if isinstance(value, dict):
        for key, member in value.items():
            if not isinstance(key, str):
                raise TypeError("canonical JSON object keys must be strings")
            _validate_canonical_value(member)
        return
```

### TypeScript — `capstone/tracks/typescript-fastify/src/domain.ts`

```text
// Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
} from "./core/domain.js";
import { canonicalJson } from "./core/domain.js";

export function requestFingerprint(
  operationId: string,
  ownerId: string,
  body: unknown,
): string {
  return createHash("sha256")
    .update(canonicalJson({ operationId, ownerId, body }), "utf8")
    .digest("hex");
}

export function filterFingerprint(
  operationId: string,
  ownerId: string,
  filters: unknown,
): string {
  return createHash("sha256")
    .update(canonicalJson({ operationId, ownerId, filters }), "utf8")
    .digest("hex");
}

export function webhookSignature(
  secret: string,
  timestamp: string,
  body: Uint8Array,
): string {
  const digest = createHmac("sha256", secret)
    .update(timestamp, "ascii")
    .update(".")
    .update(body)
    .digest("hex");
  return `sha256=${digest}`;
}

export function verifyWebhookSignature(
  secret: string,
  timestamp: string,
  body: Uint8Array,
  candidate: string,
): boolean {
  const expected = Buffer.from(webhookSignature(secret, timestamp, body));
  const received = Buffer.from(candidate);
  return (
    expected.length === received.length &&
    timingSafeEqual(expected, received)
  );
}
```

Compare the two tracks by this invariant: **both tracks reject illegal run transitions and produce identical canonical bytes for fingerprints**. The intended implementation difference is: Python uses dataclasses and enums; TypeScript uses readonly types and discriminated unions.

## Module synthesis

You are ready to leave this module when you can **Model legal and illegal state transitions, Distinguish entities, values, commands, and outcomes pragmatically, and Keep domain failures stable and transport-neutral** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a direct status assignment in the worker path, prove the matrix does not protect callers that bypass policy, then repair and add a source/behavior regression** and requiring the following oracle: **Every state/command pair has one explicit expected outcome; adding a new state or command must make the exhaustive proof fail until classified.**

The cumulative platform now includes **Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Relational Modeling and Migrations](../module-03-relational-modeling-migrations/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
