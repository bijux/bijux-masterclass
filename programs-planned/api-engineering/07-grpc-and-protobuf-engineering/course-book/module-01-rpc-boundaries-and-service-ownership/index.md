# RPC Boundaries, Service Ownership, and Interaction Choice

**Module 01 of 10**

> **Governing question:** Which interactions deserve a typed RPC boundary, and which should remain HTTP requests, durable events, or local function calls?

## Place in the program

Course 6 established durable asynchronous facts and independent consumers. This module does not begin by generating stubs. It begins by deciding whether a remote synchronous boundary is justified at all. The Analysis Runs Platform already has three valid interaction forms—public HTTP, durable events, and local calls. gRPC becomes a fourth form only where ownership, latency, typing, and deployment independence justify the additional failure boundary.

## Learning outcomes

- distinguish local calls, public HTTP operations, durable events, and internal RPCs by ownership, coupling, latency, and failure semantics
- recognize when gRPC improves a boundary and when it merely makes a distributed monolith more efficient
- design RPC services around stable capabilities rather than database tables or existing classes
- separate control-plane commands from event facts and bulk data movement
- identify caller, callee, deadline owner, retry owner, and authoritative state for every proposed RPC
- reject unjustified service extraction with explicit evidence rather than architectural fashion

## Capstone result

Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely.

## RPC is a boundary decision, not a transport upgrade

gRPC is often introduced as “HTTP/2 plus generated code.” That description is technically incomplete and pedagogically dangerous. The consequential decision is not whether bytes travel efficiently; it is whether two separately deployed components are allowed to depend on a synchronous remote capability. A local function call shares memory, failure fate, deployment, and transaction boundaries. An RPC crosses at least some of those boundaries. It can time out after the server has committed, be retried after the caller has forgotten the first attempt, and fail because the channel is unhealthy even when both applications are individually correct.

Treat every proposed RPC as an architectural claim: the caller needs a result now; the callee owns the capability; synchronous coupling is acceptable; the latency budget includes network and queue delay; and the operation can be given safe deadline, cancellation, retry, authorization, and compatibility semantics. If those claims are not true, generated stubs do not repair the design. The first professional skill in this course is therefore refusal: being able to state that a local call, HTTP resource, or durable event is the better interface.

## Four interaction forms in one platform

Public clients use the OpenAPI HTTP surface because resource-oriented semantics, browser and command-line compatibility, cache validators, pagination, and broad tooling matter. Independent consumers use the AsyncAPI event surface because they react to durable facts at their own pace and may replay history. Code inside one process uses ordinary language calls because a network boundary would add partial failure without adding ownership. Course 7 introduces gRPC only for internal capabilities that are strongly typed, latency-sensitive, controlled at both ends, and plausibly separately deployable.

The main candidate is the analysis control plane. An API process may ask an internal authority to create, inspect, or cancel a run. Workers may hold a bidirectional stream to receive assignments and report progress. Dataset and artifact transfer may use streaming RPCs when binary framing and controlled peers are useful. None of this replaces the public HTTP API or event log. The same business capability can have several views, but each view needs a distinct audience, semantics, and owner.

## Capability services instead of table services

A weak decomposition mirrors persistence: ProjectService, DatasetService, RunService, and ArtifactService, each exposing CRUD. That arrangement distributes joins, transactions, and authorization while preserving the original database coupling. A stronger RPC surface names cohesive capabilities. `AnalysisControlService` owns run-control decisions. `DatasetTransferService` owns bounded upload and artifact download. `WorkerPlaneService` owns worker sessions, assignments, progress, and completion attempts. These services may use several tables internally because service boundaries follow responsibility rather than rows.

Methods express application outcomes. `CreateRun` accepts enough information to make an idempotent run-creation decision; it does not expose “insert row.” `CancelRun` enforces version and state preconditions. `WatchRun` observes ordered state without pretending that reads advance work. `Work` coordinates a worker session instead of exposing lease tables. This naming discipline makes the contract reviewable before framework and code-generation details obscure the architecture.

## Synchronous coupling consumes a budget

Every synchronous edge consumes availability and latency budget. If an HTTP request invokes three sequential RPCs, the user-visible path succeeds only when all components and the network cooperate within one deadline. The path inherits the slowest tail. A design review must draw the complete critical path and assign one absolute deadline at the edge. Each child call receives the remaining budget rather than a fresh timeout. Parallel calls may reduce elapsed latency but increase demand and failure combinations.

The interaction matrix records whether the caller can proceed without an immediate result, whether stale data is acceptable, whether the operation changes authoritative state, and whether compensation is possible. A durable event is preferable when the sender does not need a decision now. An RPC is appropriate when the caller must know the outcome and the callee is the only authority able to decide it. This distinction becomes the foundation for deadline and retry design later in the course.

## The ownership worksheet

For every candidate method, record contract owner, implementation owner, state owner, deadline owner, retry owner, and operational owner. These roles may belong to one team, but they are not interchangeable. The state owner determines whether retry is safe. The edge owns when the result loses value. The operational owner carries the incident burden. The contract owner governs field numbers and compatibility after implementations change.

Also record what authority the response represents. `GetRun` returns an authoritative snapshot from Analysis Control. `WatchRun` returns an ordered observation stream but not a replayable public event log. `DownloadArtifact` returns bytes from the artifact authority. A worker progress frame is an attempt report, not the final public fact that progress occurred. Naming these distinctions prevents internal transport messages from leaking into public contracts.

## Python and TypeScript implications

Python and TypeScript make remote calls look deceptively ordinary. A Python stub resembles a function; a TypeScript client method resembles an async call. The course keeps transport-aware application ports. Callers pass deadlines and cancellation, and they handle typed RPC outcomes rather than catching arbitrary framework exceptions everywhere. Server adapters translate generated messages into application commands. Generated messages never become domain entities or database rows.

The two tracks need not share class layouts. They must agree on method paths, serialized messages, metadata policy, status behavior, deadlines, and externally visible stream semantics. Python may use synchronous handlers for the live reference while TypeScript uses Promise-based adapters. Shared proof is the contract and behavioral vectors, not matching syntax.

## Failure review before code

Before approving an RPC, rehearse failures: the caller times out after commit; a client retries a non-idempotent command; a channel reconnects and replays buffered work; a server drains while a stream remains open; a worker loses its lease but sends a late success; an authorization decision trusts forged metadata; a schema change reuses a field number. If the boundary has no answer for these cases, it is not ready for generation.

The capstone result is intentionally small. Approve only the minimal RPC surface and reject several attractive but unjustified candidates. Course 8 will later decide whether any approved protocol boundary deserves independent deployment. Course 7 must not smuggle microservice decomposition into a protocol lesson.

## Worked design review: should Analysis Control be remote?

Consider a proposal to move run creation into a separately deployed `AnalysisControlService` immediately. The proposal cites generated clients, lower payload overhead, and the possibility of scaling control decisions independently. A serious review starts by drawing the current transaction: validate the principal and project, bind the request identifier, create the run, create the initial job, and append the outbox event. All five effects currently share one application and database owner.

The proposed remote boundary is useful only if it preserves that ownership. A gateway can call `CreateRun`; Analysis Control can still perform the whole transaction. That is a coherent protocol boundary. A weaker design creates the run in one service, the job in another, and asks a third service to publish an event. It has distributed one atomic decision before any independent ownership or scaling evidence exists.

Now examine latency and availability. The public HTTP request already has an edge deadline. Adding one internal RPC consumes part of that budget and adds a new unavailable state. That may be justified if the control authority will be reused by worker and operator clients or if its security boundary is distinct. It is not justified merely because gRPC is faster than JSON in a microbenchmark. Serialization cost is unlikely to dominate a database-backed mutation, and a new hop can worsen tail latency.

Examine rollback. If the gateway can switch between a local port and a gRPC adapter with the same application command and idempotency identity, the protocol can be introduced reversibly. If the first gRPC release requires a new database owner, mandatory dual writes, and a coordinated gateway deployment, the boundary is already too ambitious.

The decision record therefore approves an Analysis Control RPC *contract* but defers independent deployment. It also approves a worker stream because workers are independently deployed peers with a real duplex protocol. It rejects a `ProjectService` whose methods mirror table CRUD. It keeps public listing on HTTP and committed facts on the Event API.

This review illustrates the course’s central discipline: protocol selection follows ownership and failure analysis. A method catalogue is not an architecture. Every approved method must name the authoritative state, synchronous need, deadline owner, retry owner, operational owner, and rollback path. Any proposal that cannot fill those columns remains local or asynchronous.

## Implementation reading

Read `capstone/rpc-case/interaction-decisions.yaml`, `service-ownership.yaml`, and `rpc-catalog.yaml` before opening either language track. Then compare the Python `ports.py` and TypeScript `catalog.ts` representations. They model the same ownership evidence without forcing identical class structure.

## Failure checklist

- Could this remain a local call inside one ownership and transaction boundary?
- Does the caller truly need a synchronous result?
- Who owns the absolute deadline and retry decision?
- Which state is authoritative when caller and server disagree?
- Does the boundary require independent operation, scaling, or security?
- Would the proposed service merely wrap a table or existing class?

## Transition

After preserving the checkpoint evidence, continue to **Protobuf Modeling, Presence, and Semantic Types**. Do not progress while the non-compensable gate remains unresolved.
