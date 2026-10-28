# Module 01 — Application Use Cases and Boundaries

> **Program stage:** Course 2 of 10 — Implement the promise durably.

> **Central question:** How does a public operation become an application use case without letting the framework own the system?

## Where this module fits

Course 2 begins from this incoming boundary: **The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.**

This module establishes the course’s first new responsibility by asking: **How does a public operation become an application use case without letting the framework own the system?** Its capstone increment is **Create transport, application, and adapter boundaries for the fixed operation ledger**. That result is required before **Domain State and Invariants** can be studied honestly.

## Learning outcomes

- Separate transport, application, domain, and infrastructure responsibilities.
- Translate public models into internal commands and results.
- Inject clocks, identifiers, and external dependencies.
- Keep business decisions out of FastAPI and Fastify handlers.
- Map every operation ID to one application owner.

## Capstone increment

Create transport, application, and adapter boundaries for the fixed operation ledger.

## Core model

### Driving question

> How does a published HTTP operation become maintainable application behavior without allowing the web framework to own the system?

The contract names observable behavior; an application use case owns the decision and orchestration needed to produce that behavior. FastAPI and Fastify are adapters, not the architecture.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- which Course 1 operation or representation **Application Use Cases and Boundaries** must preserve;
- which application or domain component owns the decision;
- where durable state or external effects cross a boundary;
- which counterexample and proof would falsify the result: Create transport, application, and adapter boundaries for the fixed operation ledger


### 1. Frozen public boundary

The bundled OpenAPI description, operation ledger, behavioral scenarios, security matrix, and generated clients form the predecessor handoff. They are not suggestions. During Modules 1–9 the service must conform to those bytes; internal difficulty is solved internally. This constraint separates implementation engineering from redesign.

**Counterexample.** Changing `202` to `201` because the new worker is not ready, or removing `If-Match` because the ORM update method is awkward.

**Evidence direction.** `make predecessor-proof` verifies handoff hashes and `make operation-proof` checks one owner per operation.

### 2. Operation ownership

Every `operationId` must have one transport adapter and one application owner. Ownership is not necessarily one function per endpoint: a coherent use case may delegate to domain policies and ports, but there must be a traceable place where authorization, transaction intent, and result semantics are decided.

**Counterexample.** The same `createAnalysisRun` rule appears independently in a route, a background task, and a repository helper.

**Evidence direction.** The operation map is machine-readable and source scans reject missing or duplicated operation identifiers.

### 3. Translation boundary

Pydantic or TypeBox models describe accepted transport values. They should be converted into commands before application work. Likewise, database rows and filesystem metadata are not response models. Translation keeps framework defaults, SQL column names, and storage details from becoming accidental API commitments.

**Counterexample.** Returning a raw database row whose `owner_id`, `position`, and `version` columns leak into JSON.

**Evidence direction.** Unit tests invoke use cases with plain values; black-box tests assert that persistence-only fields never cross the wire.

### 4. Composition root

Concrete dependencies are assembled once at process startup: settings, connection pool, repository, artifact store, clock, identifier source, outbound transport, and service. Business modules should not read environment variables or instantiate pools. This makes lifecycle and replacement visible.

**Counterexample.** Calling `os.getenv()` or `new Pool()` inside a use-case method.

**Evidence direction.** A source audit and tests using deterministic substitutes prove that application code has no hidden construction.

### 5. Ports with behavioral meaning

A port exists when the application needs a capability whose implementation may vary and whose behavior can be specified. `ProjectRepository` and `ArtifactStore` are meaningful; a one-method wrapper around `json.dumps` is usually not. Ports express required guarantees, not generic CRUD.

**Counterexample.** A universal repository interface with `save(anything)` that cannot state atomic update or ownership semantics.

**Evidence direction.** Port tests name preconditions, atomicity, and returned outcomes rather than mocking call counts alone.

### 6. Application failure vocabulary

The application reports stable conditions such as not found, forbidden, precondition required, precondition failed, conflict, and invalid state. It does not raise FastAPI exceptions or Fastify reply objects. The transport maps these conditions to the predecessor Problem Details contract.

**Counterexample.** A repository throws `HTTPException(404)` or returns a Fastify reply from SQL code.

**Evidence direction.** The same failure catalog is exercised by direct use-case tests and HTTP conformance tests.

### 7. Principal boundary

Authentication occurs at the transport edge, but the resulting principal is an explicit input to every protected use case. Ownership is therefore not ambient global state. Later authorization-aware SQL can bind the principal directly into predicates.

**Counterexample.** A service method relies on a thread-local “current user” set by middleware.

**Evidence direction.** Direct tests pass two principals and prove resource identity alone cannot bypass ownership.

### 8. Deterministic collaborators

Clocks and identifier sources are dependencies because time and identity participate in ETags, cursors, leases, event timestamps, and replay evidence. Deterministic substitutes make boundary conditions reproducible without sleeping or patching globals.

**Counterexample.** Calling wall-clock time repeatedly inside a transaction and asserting only approximate timestamps.

**Evidence direction.** Tests fix the clock and generated identifiers, then compare exact state transitions and payloads.

### Design pressure

Choose the principle above most likely to fail in **Application Use Cases and Boundaries**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Transport adapter

Parse and authenticate the request, translate it into a command, call one application use case, and serialize the documented result. It may know HTTP; it must not own domain transitions or SQL.

**Invariant:** Changing FastAPI to another transport should not rewrite the use case.

Coordinates policy, repository capabilities, transactions, and external ports for one outcome. It names intent such as create project or submit analysis rather than exposing tables.

**Invariant:** A use case is executable without a running web server.

Pure rules such as allowed run transitions, canonical fingerprints, ETag parsing, and retry schedules. These functions depend on values, not process resources.

**Invariant:** Given the same inputs, the result is deterministic.

Implements a port using PostgreSQL, the filesystem, HTTP, or a framework. It absorbs technology-specific exceptions and lifecycle.

**Invariant:** Technology details do not appear in the public contract or pure domain tests.

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

For **Application Use Cases and Boundaries**, record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

### Decision 1: Draw the complete `createProject` request path from raw HTTP to returned representation.

### Decision 2: For each step, mark whether it may know HTTP, SQL, environment variables, or wall-clock time.

### Decision 3: Create an operation ownership table for all frozen operations before adding code.

### Decision 4: Define the smallest application command for project creation; exclude headers already converted into principal or request metadata.

### Decision 5: Define stable application failures and map each to the predecessor problem type and status.

### Decision 6: Choose where a transaction begins, even though the first repository is in memory; later modules must not move that decision accidentally.

### Decision 7: Name only ports with a behavioral contract. Delete wrappers whose only purpose is folder symmetry.

### Decision 8: Construct the service in one composition root and make shutdown ownership explicit.

### Worked reasoning pattern

Suppose a learner proposes: “The route can check first, then the repository can write.” Ask:

- Which concurrent request, restart, or dependency failure challenges **Application Use Cases and Boundaries**?
- What must be decided or committed at one owning boundary?
- Which state survives a lost response or interrupted process?
- Which focused proof answers the module question: How does a public operation become an application use case without letting the framework own the system?


### Design review

The design review must challenge the module-specific failure named in the lab and identify the durable oracle that distinguishes a real repair from a cosmetic pass.

## Python implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/python-fastapi/src/analysis_service/
```

### Focus points

1. `build_app()` is the composition root. It creates settings, repository, artifact store, service, and FastAPI routes.
2. Pydantic request models are converted to plain dictionaries before crossing into `AnalysisService`.
3. `failures.py` defines application conditions; `problems.py` is the only HTTP translation point.
4. `domain.py` contains canonical JSON, fingerprints, ETag rules, state transitions, and webhook signatures as pure functions.
5. Use dependency injection for the authenticated principal, but pass the resulting `Principal` explicitly to service methods.
6. Test service methods directly before using `TestClient` or HTTPX.

### Representative pattern

```python
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True, slots=True)
class CreateProject:
    principal_id: str
    name: str
    description: str | None

class Projects(Protocol):
    async def create(self, command: CreateProject) -> "Project": ...

class CreateProjectUseCase:
    def __init__(self, projects: Projects) -> None:
        self._projects = projects

    async def execute(self, command: CreateProject) -> "Project":
        # HTTP status, request objects, and SQL rows do not belong here.
        return await self._projects.create(command)
```

The excerpt for **Application Use Cases and Boundaries** isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## TypeScript implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/typescript-fastify/src/
```

Runtime schemas, TypeScript types, Fastify lifecycle, Node streams, and node-postgres sessions solve different problems. Keep them separate while reading.

### Focus points

1. `buildApp()` assembles the Fastify instance, PostgreSQL repository, artifact store, and service.
2. TypeBox schemas validate transport values; TypeScript types do not replace runtime validation.
3. `problems.ts` owns HTTP serialization of known application failures.
4. Use explicit constructor dependencies in `AnalysisService`; avoid importing a global pool into handlers.
5. Fastify decorators and hooks remain transport concerns; the service accepts ordinary values and principal data.
6. Compile and execute the local core tests without installing the full framework stack.

### Representative pattern

```typescript
export type CreateProject = Readonly<{
  principalId: string;
  name: string;
  description: string | null;
}>;

export interface Projects {
  create(command: CreateProject): Promise<Project>;
}

export class CreateProjectUseCase {
  public constructor(private readonly projects: Projects) {}

  public execute(command: CreateProject): Promise<Project> {
    return this.projects.create(command);
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

1. This module reads the schema but does not yet let SQL dictate application boundaries.
2. Identify which future operations need atomic behavior: create plus idempotency record, terminal run plus event plus outbox, and ETag-guarded update.
3. Write transaction-intent comments at the use-case level before implementing database adapters.

### Representative SQL

```sql
-- Transaction intent written before adapter implementation:
-- create analysis run = idempotency reservation + run + initial event + job.
-- No network or filesystem effect belongs inside this transaction.
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

The contract names observable behavior; an application use case owns the decision and orchestration needed to produce that behavior. FastAPI and Fastify are adapters, not the architecture.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | predecessor manifest verifies byte-for-byte | Write the narrow command and machine-readable oracle. |
| 2 | operation map has exactly one owner per language | Write the narrow command and machine-readable oracle. |
| 3 | use-case tests run without HTTP | Write the narrow command and machine-readable oracle. |
| 4 | route handlers contain no domain transition table | Write the narrow command and machine-readable oracle. |
| 5 | public models exclude owner and position columns | Write the narrow command and machine-readable oracle. |
| 6 | principal is explicit in protected service calls | Write the narrow command and machine-readable oracle. |
| 7 | configuration is read only in composition code | Write the narrow command and machine-readable oracle. |
| 8 | known failures map to stable problem types | Write the narrow command and machine-readable oracle. |

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

> Put the project-name rule only in the HTTP route. The direct use-case test should reveal that the architecture cannot defend the invariant outside HTTP.

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

### 1. Framework-owned business rule

**Observable symptom:** A direct service test cannot reproduce route behavior.

**Root cause:** The route validates lifecycle state or chooses domain outcomes.

**Repair:** Move the decision into a pure policy or use case; leave only translation in the route.

**Permanent regression:** Call the use case directly for both legal and illegal states.

### 2. Public model reused as row model

**Observable symptom:** Internal columns appear in responses or database changes force API changes.

**Root cause:** One class was made responsible for wire, application, and persistence representations.

**Repair:** Create explicit mapping functions and separate types.

**Permanent regression:** Assert serialized responses reject or omit persistence-only fields.

### 3. Hidden dependency construction

**Observable symptom:** Tests open real connections or read the developer environment unexpectedly.

**Root cause:** A module instantiates concrete resources during import or inside a use case.

**Repair:** Move construction to the composition root and inject ports.

**Permanent regression:** Import and execute the application layer with fake dependencies and an empty environment.

### 4. HTTP exception below transport

**Observable symptom:** The domain package imports FastAPI or Fastify.

**Root cause:** Status codes were used as the internal failure vocabulary.

**Repair:** Raise or return application conditions, then translate once.

**Permanent regression:** Dependency boundary source check plus direct failure tests.

### 5. Ambient principal

**Observable symptom:** Concurrent tests occasionally authorize the wrong owner.

**Root cause:** Principal information is stored globally or inferred late.

**Repair:** Pass an immutable principal into every protected use case and repository predicate.

**Permanent regression:** Run interleaved requests for two principals.

### 6. Ceremonial port explosion

**Observable symptom:** A simple change crosses many one-line interfaces without adding substitutability or guarantees.

**Root cause:** Folders were copied from an architecture diagram rather than derived from behavior.

**Repair:** Collapse boundaries that cannot state an independent contract.

**Permanent regression:** Architecture review requires a falsifiable reason for each port.

### 7. Mutable frozen contract

**Observable symptom:** Implementation tests pass only after changing predecessor files.

**Root cause:** The API was modified to accommodate internal convenience.

**Repair:** Restore the handoff from its manifest and solve the implementation problem internally.

**Permanent regression:** Run predecessor hash proof before every module checkpoint.

### 8. Nondeterministic time and identity

**Observable symptom:** Tests sleep, use loose timestamp windows, or intermittently compare identifiers.

**Root cause:** Clocks and identifier generation are hidden globals.

**Repair:** Inject deterministic sources at the application boundary.

**Permanent regression:** Exact-value tests with a fixed clock and seeded identifiers.

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

The first vertical slice creates and reads projects through explicit application boundaries while preserving every Course 1 response, header, security, and error commitment.

### Increment plan

1. Verify the predecessor manifest and copy no contract file into an editable location.
2. Build the complete operation ownership map, including anonymous and protected operations.
3. Trace `createProject` and `getProject` through transport, command, service, port, mapping, and response.
4. Implement the slice first with deterministic in-memory ports in the chosen primary track.
5. Run the same use-case tests without starting the framework.
6. Wire the route adapters and run the frozen behavioral scenarios for the slice.

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

The **Application Use Cases and Boundaries** increment must preserve the frozen API and every earlier durability invariant while delivering this result: Create transport, application, and adapter boundaries for the fixed operation ledger The comparison track must expose the same public outcomes even when internal libraries and control flow differ.


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

These are the smallest useful entry points for **Application Use Cases and Boundaries**.

### Python — `capstone/tracks/python-fastapi/src/analysis_service/service.py`

```text
# Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
)


class AnalysisService:
    def __init__(
        self,
        repository: Repository,
        artifacts: ArtifactStore,
        upload_limit: int,
    ) -> None:
        self.repository = repository
        self.artifacts = artifacts
        self.upload_limit = upload_limit

    def list_projects(
        self,
        principal: Principal,
        limit: int,
        cursor: str | None,
        name: str | None,
    ):
        return self.repository.list_projects(
            principal,
            limit,
            parse_cursor(cursor),
            name,
        )

    def create_project(self, principal: Principal, body: ProjectCreate):
        return self.repository.create_project(principal, body)

    def get_project(self, principal: Principal, project_id: str):
        return self.repository.get_project(principal, project_id)

    def update_project(
        self,
        principal: Principal,
        project_id: str,
        if_match: str | None,
        body: ProjectPatch,
    ):
        return self.repository.update_project(
            principal,
            project_id,
            if_match,
            body,
        )

    def list_datasets(
        self,
        principal: Principal,
        project_id: str,
        limit: int,
        cursor: str | None,
        status: str | None,
```

### TypeScript — `capstone/tracks/typescript-fastify/src/service.ts`

```text
// Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
  WebhookSubscriptionCreate,
} from "./types.js";

const ALLOWED_UPLOAD_MEDIA_TYPES = new Set([
  "text/csv",
  "application/json",
  "application/octet-stream",
]);

/** Framework-independent application use cases. */
export class AnalysisService {
  public constructor(
    public readonly repository: PostgresRepository,
    private readonly artifacts: FileSystemArtifactStore,
    private readonly uploadLimit: number,
  ) {}

  public listProjects(
    principal: Principal,
    limit: number,
    cursor: string | undefined,
    name: string | undefined,
  ) {
    return this.repository.listProjects(
      principal,
      limit,
      parseCursor(cursor),
      name,
    );
  }

  public createProject(principal: Principal, body: ProjectCreate) {
    return this.repository.createProject(principal, body);
  }

  public getProject(principal: Principal, projectId: string) {
    return this.repository.getProject(principal, projectId);
  }

  public updateProject(
    principal: Principal,
    projectId: string,
    ifMatch: string | undefined,
    body: ProjectPatch,
  ) {
    return this.repository.updateProject(
      principal,
      projectId,
      ifMatch,
      body,
    );
  }

  public listDatasets(
    principal: Principal,
```

Compare the two tracks by this invariant: **route adapters translate HTTP input into application commands; use cases own decisions**. The intended implementation difference is: Python uses explicit service methods and protocols; TypeScript uses structural interfaces and async methods.

## Module synthesis

You are ready to leave this module when you can **Separate transport, application, domain, and infrastructure responsibilities, Translate public models into internal commands and results, and Inject clocks, identifiers, and external dependencies** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a framework-owned validation rule, observe which direct test fails to detect it, then move the rule and keep the regression** and requiring the following oracle: **A direct application test must reject the same invalid command as the HTTP route while importing no framework package.**

The cumulative platform now includes **Create transport, application, and adapter boundaries for the fixed operation ledger**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Domain State and Invariants](../module-02-domain-state-invariants/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
