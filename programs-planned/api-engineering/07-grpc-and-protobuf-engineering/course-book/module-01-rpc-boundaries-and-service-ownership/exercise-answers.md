# Worked answers — RPC Boundaries, Service Ownership, and Interaction Choice

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. A public browser client needs to list analysis runs. Should this become a gRPC method? Explain the governing factors.

Keep the public list operation on HTTP. Browser interoperability, cache and pagination semantics, and the existing public contract matter more than generated internal stubs. A private gRPC query may exist behind the gateway only if a separately owned control authority and the extra synchronous edge are justified.

**Decisive evidence:** interaction decision record

## 2. An internal worker must receive assignments and report progress for several hours. Compare unary polling, durable events, and a bidirectional RPC stream.

Unary polling creates repeated requests and weak session semantics. Durable events support independent consumers and replay but are not a direct assignment channel. A bidirectional stream fits a controlled worker session because both sides need timely messages, flow control, cancellation, and connection state; durable leases must still preserve authority after disconnect.

**Decisive evidence:** worker-session failure matrix

## 3. Why is a generated stub not equivalent to a local function call even when the signature looks identical?

The call can fail before reaching the server, after commit, or while the response is lost. It crosses deployment, authorization, compatibility, and latency boundaries. A local-looking signature hides those remote uncertainties unless the design makes them explicit.

**Decisive evidence:** remote-call ambiguity trace

## 4. A proposed ProjectService exposes CRUD for the projects table. Identify the smell and propose a capability-oriented alternative.

The service mirrors persistence rather than owning a capability. Use AnalysisControlService for run decisions, and add project administration only if policy and ownership are independently meaningful. CRUD can remain behind the HTTP resource API or local application.

**Decisive evidence:** service ownership map

## 5. For CreateRun, name the contract, state, deadline, retry, and operational owners.

The RPC contract is owned by the RPC/API platform owner; authoritative run state by Analysis Control; the edge request owns the deadline; the caller owns retry policy; and the control-plane operational owner carries availability. Ambiguity in any role blocks release.

**Decisive evidence:** ownership worksheet

## 6. When is a durable event preferable to a synchronous RPC even if gRPC would be faster?

Use an event when the sender does not need an immediate decision, several independent consumers need the fact, temporal decoupling matters, or replay is required. Lower transport latency is not enough reason for synchronous coupling.

**Decisive evidence:** synchronous/asynchronous decision matrix

## 7. Why should a worker progress frame not automatically become the public AnalysisRunProgressed event?

A progress frame is attempt-scoped and may be duplicated, stale, or rejected because its lease generation is obsolete. Analysis Control must validate it, commit authoritative state, and publish the public event transactionally.

**Decisive evidence:** event ownership and lease vectors

## 8. Describe the failure path when an HTTP request calls two RPCs and the second times out after committing.

The first call consumes part of the edge budget. The second may commit but miss the deadline while returning. The caller sees failure although state changed. A new request identifier can duplicate the effect; the design needs one deadline, persistent idempotency, and reconciliation.

**Decisive evidence:** deadline and idempotency sequence diagram

## 9. What evidence would justify deploying DatasetTransferService separately?

Evidence includes independent transfer scaling, clear artifact ownership, isolation benefit, distinct security or retention policy, and the ability to operate without another service’s private database. A preference for another framework is insufficient.

**Decisive evidence:** boundary dossier

## 10. Give one interaction that should remain a local call throughout this course.

Domain validation and state transitions owned by one application transaction should remain local. RPC would add latency and partial failure while weakening atomicity without adding independent ownership.

**Decisive evidence:** transaction boundary map

## 11. Why does mirroring tables into services tend to create a distributed monolith?

Services still need one another’s data and decisions, so joins and transactions become network calls while deployments are separate. Change and failure remain coupled—the defining shape of a distributed monolith.

**Decisive evidence:** distributed-monolith rejection case

## 12. Write a decision rule for HTTP, events, gRPC, and local calls.

Use local calls within one ownership and transaction boundary; HTTP for public interoperable resource semantics; durable events for independent reaction to facts; and gRPC for controlled typed synchronous or streaming capabilities across a justified boundary.

**Decisive evidence:** final interaction policy
