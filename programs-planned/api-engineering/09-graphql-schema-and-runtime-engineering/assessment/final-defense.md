# Final architecture defense

The final defense is a live engineering review, not a slide presentation. The
learner receives a clean checkout, a fixed Course 8 predecessor handoff, and the
released Analysis Graph API 1.0 artifacts. They must demonstrate the system and
explain why each property belongs at the graph layer or remains owned by a
source service.

## Required demonstrations

### 1. Project overview composition

Execute `GetProjectOverview` and show that one page of runs produces one batched
Artifact Service call and one batched Notification Service call. Identify the
owner of every returned fact. Explain why the gateway may compose these facts
but may not write them or join private service tables.

### 2. Stable pagination

Begin a run traversal, insert a newer run, and continue using the existing
cursor. The newer row must not contaminate the old traversal. Decode the cursor
only through the trusted codec and name every bound dimension: tenant,
audience, field scope, normalized filters, continuation key, high-water key,
expiry, and version.

### 3. Mutation safety

Execute `StartAnalysis` twice with the same idempotency key and identical input,
then reuse the key with changed input. Show replay for the identical request and
a conflict for the changed request. Explain why the graph gateway delegates the
command rather than owning an idempotency database.

### 4. Authorization before work

Request `AnalysisRun.artifacts` with run-read permission but without artifact
permission. The field must become `null`, a `FORBIDDEN` error must identify its
exact path, and Artifact Service must receive no call. Repeat with the wrong
tenant and show resource concealment.

### 5. Demand rejection

Present an operation that exceeds a declared budget by depth, aliases, page
size, cost, or service fan-out. The request must be rejected before source
services are invoked. Explain why demand analysis must expand fragments and
include variables rather than inspecting raw text superficially.

### 6. Partial source failure

Fail Artifact Service while Analysis Control and Notification Service remain
available. The response must preserve valid project, run, and delivery data;
set only affected artifact fields to `null`; and report exact field paths and
the failing service. Empty lists are not an acceptable substitute for failure.

### 7. Resumable subscription

Resume after a known sequence, suppress a duplicate event, and reject a gap.
Explain which guarantees belong to the GraphQL subscription field and which
belong to the chosen transport or underlying event system.

### 8. Compatible release

Classify one additive, one review-required, and one breaking schema change.
Demonstrate that schema diff alone is insufficient: all active persisted
operations, ownership coordinates, demand budgets, and an older client must
also pass before release.

## Evidence packet

Submit the machine-readable proof reports, the exact schema and operation
registry, one request/response transcript for each demonstration, source-call
counts, the compatibility decision, and a one-page residual-risk statement.
Every claim must identify its decisive oracle. Assertions such as “the query
looks efficient” or “GraphQL handles this automatically” receive no credit.

The defense fails immediately if any non-compensable property in the rubric is
violated, regardless of the total score.
