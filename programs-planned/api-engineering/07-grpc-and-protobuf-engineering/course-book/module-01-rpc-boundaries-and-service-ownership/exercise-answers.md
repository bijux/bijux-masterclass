# Worked Answers — Module 01: RPC Boundaries, Service Ownership, and Interaction Choice

Use these solutions to audit your reasoning for **RPC Boundaries, Service Ownership, and Interaction Choice**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. A public browser client needs to list analysis runs. Should this become a gRPC method? Explain the governing factors.

Keep the public list operation on HTTP. Browser interoperability, cache and pagination semantics, and the existing public contract matter more than generated internal stubs. A private gRPC query may exist behind the gateway only if a separately owned control authority and the extra synchronous edge are justified.

**Decisive evidence:** interaction decision record

The chapter’s decisive distinction is this: Public clients use the OpenAPI HTTP surface because resource-oriented semantics, browser and command-line compatibility, cache validators, pagination, and broad tooling matter. Independent consumers use the AsyncAPI event surface because they react to durable facts at their own pace and may replay history. Code inside one process uses ordinary language calls because a network boundary would add partial failure without adding ownership.

## 2. An internal worker must receive assignments and report progress for several hours. Compare unary polling, durable events, and a bidirectional RPC stream.

Unary polling creates repeated requests and weak session semantics. Durable events support independent consumers and replay but are not a direct assignment channel. A bidirectional stream fits a controlled worker session because both sides need timely messages, flow control, cancellation, and connection state; durable leases must still preserve authority after disconnect.

**Decisive evidence:** worker-session failure matrix

In the cumulative capstone, the rule becomes concrete: The main candidate is the analysis control plane. An API process may ask an internal authority to create, inspect, or cancel a run. Workers may hold a bidirectional stream to receive assignments and report progress. Dataset and artifact transfer may use streaming RPCs when binary framing and controlled peers are useful. None of this replaces the public HTTP API or event log.

## 3. Why is a generated stub not equivalent to a local function call even when the signature looks identical?

The call can fail before reaching the server, after commit, or while the response is lost. It crosses deployment, authorization, compatibility, and latency boundaries. A local-looking signature hides those remote uncertainties unless the design makes them explicit.

**Decisive evidence:** remote-call ambiguity trace

A useful way to reason about the boundary is: Examine rollback. If the gateway can switch between a local port and a gRPC adapter with the same application command and idempotency identity, the protocol can be introduced reversibly. If the first gRPC release requires a new database owner, mandatory dual writes, and a coordinated gateway deployment, the boundary is already too ambitious.

## 4. A proposed ProjectService exposes CRUD for the projects table. Identify the smell and propose a capability-oriented alternative.

The service mirrors persistence rather than owning a capability. Use AnalysisControlService for run decisions, and add project administration only if policy and ownership are independently meaningful. CRUD can remain behind the HTTP resource API or local application.

**Decisive evidence:** service ownership map

The implementation consequence is: A weak decomposition mirrors persistence: ProjectService, DatasetService, RunService, and ArtifactService, each exposing CRUD. That arrangement distributes joins, transactions, and authorization while preserving the original database coupling. A stronger RPC surface names cohesive capabilities. AnalysisControlService owns run-control decisions. DatasetTransferService owns bounded upload and artifact download. WorkerPlaneService owns worker sessions, assignments, progress, and completion attempts. These services may use several tables internally because service boundaries follow responsibility rather than rows.

## 5. For CreateRun, name the contract, state, deadline, retry, and operational owners.

The RPC contract is owned by the RPC/API platform owner; authoritative run state by Analysis Control; the edge request owns the deadline; the caller owns retry policy; and the control-plane operational owner carries availability. Ambiguity in any role blocks release.

**Decisive evidence:** ownership worksheet

The important nuance is: For every candidate method, record contract owner, implementation owner, state owner, deadline owner, retry owner, and operational owner. These roles may belong to one team, but they are not interchangeable. The state owner determines whether retry is safe. The edge owns when the result loses value. The operational owner carries the incident burden. The contract owner governs field numbers and compatibility after implementations change.

## 6. When is a durable event preferable to a synchronous RPC even if gRPC would be faster?

Use an event when the sender does not need an immediate decision, several independent consumers need the fact, temporal decoupling matters, or replay is required. Lower transport latency is not enough reason for synchronous coupling.

**Decisive evidence:** synchronous/asynchronous decision matrix

Under concurrency or failure, the distinction becomes: The interaction matrix records whether the caller can proceed without an immediate result, whether stale data is acceptable, whether the operation changes authoritative state, and whether compensation is possible. A durable event is preferable when the sender does not need a decision now. An RPC is appropriate when the caller must know the outcome and the callee is the only authority able to decide it.

## 7. Why should a worker progress frame not automatically become the public AnalysisRunProgressed event?

A progress frame is attempt-scoped and may be duplicated, stale, or rejected because its lease generation is obsolete. Analysis Control must validate it, commit authoritative state, and publish the public event transactionally.

**Decisive evidence:** event ownership and lease vectors

The design remains honest only if: Also record what authority the response represents. GetRun returns an authoritative snapshot from Analysis Control. WatchRun returns an ordered observation stream but not a replayable public event log. DownloadArtifact returns bytes from the artifact authority. A worker progress frame is an attempt report, not the final public fact that progress occurred. Naming these distinctions prevents internal transport messages from leaking into public contracts.

## 8. Describe the failure path when an HTTP request calls two RPCs and the second times out after committing.

The first call consumes part of the edge budget. The second may commit but miss the deadline while returning. The caller sees failure although state changed. A new request identifier can duplicate the effect; the design needs one deadline, persistent idempotency, and reconciliation.

**Decisive evidence:** deadline and idempotency sequence diagram

The consumer-facing consequence is: Every synchronous edge consumes availability and latency budget. If an HTTP request invokes three sequential RPCs, the user-visible path succeeds only when all components and the network cooperate within one deadline. The path inherits the slowest tail. A design review must draw the complete critical path and assign one absolute deadline at the edge. Each child call receives the remaining budget rather than a fresh timeout.

## 9. What evidence would justify deploying DatasetTransferService separately?

Evidence includes independent transfer scaling, clear artifact ownership, isolation benefit, distinct security or retention policy, and the ability to operate without another service’s private database. A preference for another framework is insufficient.

**Decisive evidence:** boundary dossier

The operational consequence is: The proposed remote boundary is useful only if it preserves that ownership. A gateway can call CreateRun; Analysis Control can still perform the whole transaction. That is a coherent protocol boundary. A weaker design creates the run in one service, the job in another, and asks a third service to publish an event. It has distributed one atomic decision before any independent ownership or scaling evidence exists.

## 10. Give one interaction that should remain a local call throughout this course.

Domain validation and state transitions owned by one application transaction should remain local. RPC would add latency and partial failure while weakening atomicity without adding independent ownership.

**Decisive evidence:** transaction boundary map

The strongest engineering interpretation is: The capstone result is intentionally small. Approve only the minimal RPC surface and reject several attractive but unjustified candidates. Course 8 will later decide whether any approved protocol boundary deserves independent deployment. Course 7 must not smuggle microservice decomposition into a protocol lesson.

## 11. Why does mirroring tables into services tend to create a distributed monolith?

Services still need one another’s data and decisions, so joins and transactions become network calls while deployments are separate. Change and failure remain coupled—the defining shape of a distributed monolith.

**Decisive evidence:** distributed-monolith rejection case

The defect-oriented view is: Methods express application outcomes. CreateRun accepts enough information to make an idempotent run-creation decision; it does not expose “insert row.” CancelRun enforces version and state preconditions. WatchRun observes ordered state without pretending that reads advance work. Work coordinates a worker session instead of exposing lease tables. This naming discipline makes the contract reviewable before framework and code-generation details obscure the architecture.

## 12. Write a decision rule for HTTP, events, gRPC, and local calls.

Use local calls within one ownership and transaction boundary; HTTP for public interoperable resource semantics; durable events for independent reaction to facts; and gRPC for controlled typed synchronous or streaming capabilities across a justified boundary.

**Decisive evidence:** final interaction policy

Across the Python and TypeScript tracks, the invariant is: Now examine latency and availability. The public HTTP request already has an edge deadline. Adding one internal RPC consumes part of that budget and adds a new unavailable state. That may be justified if the control authority will be reused by worker and operator clients or if its security boundary is distinct. It is not justified merely because gRPC is faster than JSON in a microbenchmark.
