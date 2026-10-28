# Module 08 — Transactional Outbox and Webhook Delivery

> **Program stage:** Course 2 of 6 — Make the promise durable.

> **Central question:** How can a committed business change reliably produce an external webhook without a dual write?

## Where this module fits

Commit an outbox record with the domain state, then deliver at least once with stable event identity. You arrive from Module 07 with all earlier checkpoints still green. The Course 1 handoff is fixed. This course may change internal architecture and add a compatible API release, but it may not solve an implementation problem by quietly weakening the public contract. The result is the baseline for **Failure-Oriented Verification**.

## Learning outcomes

- Explain the dual-write failure.
- Insert outbox intent in the domain transaction.
- Separate dispatcher attempts from logical events.
- Retry only classified failures with bounded delay.
- Require receiver deduplication for at-least-once delivery.

## Capstone result

Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints.

Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.

## Core model

### Driving question

> How can the service communicate externally without reporting domain success while losing the corresponding event?

Commit domain state and an outbox event together; perform network delivery afterward with signed, identifiable, retryable, deduplicable attempts. HTTP delivery is at-least-once and receivers must treat event identity as the unit of idempotency.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- the public behavior inherited from Course 1;
- the application or domain decision owner;
- the durable database, worker, storage, or delivery mechanism;
- the proof that exposes failure after retry, concurrency, or restart.


### 1. Dual-write problem

Domain state and outbound delivery live in different systems. There is no ordinary transaction spanning PostgreSQL and an arbitrary receiver. Direct sequential calls always leave a crash window in one direction.

**Counterexample.** Update run, commit, then send webhook and assume a `try` statement makes both one unit.

**Evidence direction.** Inject process death between each ordered step and identify the inconsistent outcome.

### 2. Transactional outbox

The same transaction that commits the terminal run and domain event inserts an immutable outbox row. After commit, a dispatcher can retry network delivery independently. Absence of delivery does not erase domain success.

**Counterexample.** Enqueue an in-memory callback after commit.

**Evidence direction.** Kill the API/worker immediately after commit; a later dispatcher still discovers and delivers the event.

### 3. Event versus delivery identity

One logical event may produce several deliveries: a request callback and multiple matching subscriptions. Event ID remains stable across all recipients and retries; delivery ID identifies one target-specific attempt stream.

**Counterexample.** Generate a new event ID for every retry, preventing receiver deduplication.

**Evidence direction.** Attempt history shows one event ID, stable payload digest, one delivery ID per target, and increasing attempts.

### 4. Canonical signed bytes

The exact transmitted bytes, timestamp, and secret feed HMAC. Sender and receiver must agree on canonical JSON or sign the already-serialized body. Re-serializing parsed JSON can change bytes and invalidate signatures.

**Counterexample.** Sign a dictionary, then let the HTTP client serialize it differently.

**Evidence direction.** Shared vectors verify Python, TypeScript, and receiver signatures byte-for-byte.

### 5. Freshness and constant-time verification

The receiver checks timestamp skew to limit replay windows and compares signatures using constant-time primitives. Freshness does not replace event-ID deduplication; both address different replay threats.

**Counterexample.** Accept a valid signature from months ago or compare secrets with ordinary string equality.

**Evidence direction.** Valid, modified-body, modified-timestamp, stale, malformed, and duplicate vectors.

### 6. Delivery leasing and retry

Dispatchers claim pending/expired deliveries with generation fencing like jobs. Retryable network/5xx responses use bounded backoff; most 4xx responses become terminal because repeating the same request will not help.

**Counterexample.** Hold a database transaction open while waiting for receiver response.

**Evidence direction.** Receiver `fail_first` scenario records increasing attempts, no duplicate logical delivery, and eventual success.

### 7. Receiver idempotency

A receiver stores event ID and body digest. Exact repeats return success without repeating domain effect; same ID with different body is conflict. This is required because sender timeout cannot distinguish rejected from accepted delivery.

**Counterexample.** Treat every POST as a new command.

**Evidence direction.** Send identical request twice and a modified request with the same ID.

### 8. Destination control

Webhook configuration is an SSRF boundary. Validate HTTPS, reject credentials/fragments, constrain hostnames or resolve-and-check addresses, limit redirects, set deadlines/body limits, and avoid forwarding internal credentials.

**Counterexample.** Allow `http://169.254.169.254/` or follow redirects to loopback.

**Evidence direction.** Destination corpus covers loopback, private, link-local, userinfo, non-HTTPS, redirect, and approved host.

### Design pressure

Choose the principle above most likely to fail in **Transactional Outbox and Webhook Delivery**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Outbox event

Immutable logical event ID, type, subject, payload, occurrence time, and expansion state.

**Invariant:** Created atomically with the domain transition it describes.

Target-specific state with attempts, availability, lease owner/generation, and terminal result.

**Invariant:** Retries retain event identity and payload bytes.

Timestamp plus canonical body authenticated with recipient secret.

**Invariant:** Any byte or timestamp change invalidates signature.

Stored event ID and digest used to deduplicate exact retries.

**Invariant:** One event ID cannot denote two bodies.

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

### Decision 1: Define terminal run event payload and stable event ID before delivery code.

### Decision 2: Insert run completion, event, artifact metadata, and outbox in one transaction.

### Decision 3: Define expansion from event to callback and subscription deliveries.

### Decision 4: Define canonical bytes and signature header format.

### Decision 5: Define receiver freshness window and deduplication behavior.

### Decision 6: Classify HTTP/network results into retry, success, or terminal failure.

### Decision 7: Lease deliveries with generation fencing and bounded attempts.

### Decision 8: Constrain destinations and redirect policy before storing subscriptions.

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

1. `HttpxOutboundTransport` sends already-serialized bytes with explicit timeouts and redirects disabled.
2. Use `hmac.compare_digest()` for receiver verification and a shared signature vector file.
3. Expand outbox rows and claim deliveries in short PostgreSQL transactions.
4. Never decrypt/expose webhook secrets outside the delivery boundary longer than necessary.
5. Record attempt status and bounded response/error summary without storing secret headers.
6. Use the controlled receiver’s SQLite evidence for black-box retry/dedup proofs.

### Representative pattern

```python
def signed_request(secret: str, event: dict[str, object], now: int) -> SignedRequest:
    body = canonical_json(event)             # serialize once
    timestamp = str(now)
    signature = webhook_signature(secret, timestamp, body)
    return SignedRequest(
        body=body,
        headers={
            "Content-Type": "application/json",
            "X-Event-Id": str(event["eventId"]),
            "X-Webhook-Timestamp": timestamp,
            "X-Webhook-Signature": signature,
        },
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

1. Use `createHmac()` and `timingSafeEqual()` with equal-length buffers.
2. Pass a prebuilt `Buffer` to `fetch`; sign that exact buffer rather than a mutable object.
3. Use `AbortSignal.timeout()` or explicit `AbortController` for hard deadlines.
4. Disable or constrain redirects; validate destination before every delivery to handle changed DNS/policy.
5. Lease and complete deliveries with owner/generation predicates.
6. Persist concise error classification, not entire potentially sensitive response bodies.

### Representative pattern

```typescript
const body = Buffer.from(stableStringify(event), "utf8");
const timestamp = String(clock.unixSeconds());
const signature = createHmac("sha256", secret)
  .update(timestamp, "ascii")
  .update(".")
  .update(body)
  .digest("hex");
await fetch(target, { method: "POST", body, redirect: "manual", signal });
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

1. Outbox row is inserted in the terminal run transaction.
2. Unique event ID and delivery target identity prevent duplicate expansion.
3. Delivery rows have availability, attempts, lease owner/generation, and terminal status.
4. Partial indexes support unexpanded outbox and pending/expired delivery claims.

### Representative SQL

```sql
BEGIN;
UPDATE analysis_runs SET status='completed', progress=100, completed_at=clock_timestamp()
 WHERE public_id=$1 AND status='running';
INSERT INTO run_events(event_id, run_id, event_type, payload) VALUES ($2,$1,$3,$4);
INSERT INTO outbox_events(event_id, event_type, subject, payload) VALUES ($2,$3,$1,$4);
COMMIT;
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

Commit domain state and an outbox event together; perform network delivery afterward with signed, identifiable, retryable, deduplicable attempts. HTTP delivery is at-least-once and receivers must treat event identity as the unit of idempotency.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | domain completion always outbox | Write the narrow command and machine-readable oracle. |
| 2 | kill after commit still delivers | Write the narrow command and machine-readable oracle. |
| 3 | event ID stable across retries | Write the narrow command and machine-readable oracle. |
| 4 | exact bytes signature vectors | Write the narrow command and machine-readable oracle. |
| 5 | stale signature rejected | Write the narrow command and machine-readable oracle. |
| 6 | receiver exact duplicate idempotent | Write the narrow command and machine-readable oracle. |
| 7 | same ID changed body conflict | Write the narrow command and machine-readable oracle. |
| 8 | forbidden destination rejected | Write the narrow command and machine-readable oracle. |

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

> Remove the outbox insert and send only after commit; kill the process in the gap and prove the receiver never learns about the completed run.

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

### 1. Network inside domain transaction

**Observable symptom:** Slow receiver holds locks; rollback may follow accepted webhook.

**Root cause:** External HTTP treated as transactional database work.

**Repair:** Insert outbox in transaction; deliver after commit.

**Permanent regression:** Receiver delay plus lock/rollback inspection.

### 2. Send after commit without outbox

**Observable symptom:** Process death loses notification forever.

**Root cause:** Delivery intent exists only in memory.

**Repair:** Persist immutable event intent atomically.

**Permanent regression:** Kill immediately after completion commit.

### 3. New event ID per retry

**Observable symptom:** Receiver repeats business effect.

**Root cause:** Attempt identity confused with event identity.

**Repair:** Stable event ID and target-specific delivery ID.

**Permanent regression:** `fail_first` attempts share event/delivery identity.

### 4. Sign object, send other bytes

**Observable symptom:** Valid local signature fails at receiver.

**Root cause:** Serialization differs between signing and transport.

**Repair:** Serialize once, sign and send exact bytes.

**Permanent regression:** Nested/unicode/key-order vectors.

### 5. No freshness check

**Observable symptom:** Captured signed request replays indefinitely.

**Root cause:** HMAC authenticates bytes but not timeliness policy.

**Repair:** Include timestamp in signature and enforce bounded skew.

**Permanent regression:** Stale timestamp vector.

### 6. Receiver not idempotent

**Observable symptom:** Timeout retry repeats downstream effect.

**Root cause:** Every POST treated as unique.

**Repair:** Store event ID/digest before effect and replay success.

**Permanent regression:** Exact duplicate plus changed-body conflict.

### 7. Unbounded redirect SSRF

**Observable symptom:** Approved URL redirects to internal address.

**Root cause:** Only initial URL validated.

**Repair:** Disable redirects or validate every hop/resolved address.

**Permanent regression:** Controlled redirect-to-loopback case.

### 8. Retry every status

**Observable symptom:** Permanent 400/401 loops consume dispatcher capacity.

**Root cause:** No response classification or attempt cap.

**Repair:** Define retryable network/408/429/5xx policy and terminal client failures.

**Permanent regression:** Matrix of receiver forced statuses.

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

Completed analyses now produce durable, signed, retryable webhook deliveries without coupling domain transactions to receiver availability.

### Increment plan

1. Implement terminal run/event/artifact/outbox atomic transaction.
2. Implement outbox expansion into callback and subscription deliveries.
3. Implement delivery claim, lease generation, bounded retry, and attempt recording.
4. Implement serialize-once HMAC signing in the primary track.
5. Run shared signature vectors against both tracks and receiver.
6. Use receiver `fail_first`, forced 4xx/5xx, duplicate, stale, and changed-body cases.

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

These are the smallest useful entry points for **Transactional Outbox and Webhook Delivery**.

### Python — `capstone/tracks/python-fastapi/src/analysis_service/webhooks.py`

```python
APPROVED_WEBHOOK_HOST = "hooks.example.test"


def parse_destination(url: str) -> SplitResult:
    parsed = urlsplit(url)
    try:
        approved_port = parsed.port in {None, 443}
    except ValueError:
        approved_port = False
    approved = (
        parsed.scheme == "https"
        and parsed.hostname == APPROVED_WEBHOOK_HOST
        and parsed.username is None
        and parsed.password is None
        and parsed.fragment == ""
        and approved_port
    )
    if not approved:
        raise ServiceError(
            422,
            "Request validation failed",
            "Webhook destinations must use the approved HTTPS host.",
            "validation",
        )
    return parsed


def validate_destination(url: str) -> None:
    parse_destination(url)


class HttpxOutboundTransport:
    """Route approved training webhook URLs to the local receiver.

    Production code would resolve and connect to the approved destination while
    applying DNS/IP controls. This adapter intentionally keeps the course
    network-independent and does not pretend to be a general SSRF defence.
    """

    def __init__(self, training_base: str):
        self.training_base = training_base.rstrip("/")

    def _route(self, url: str) -> str:
        parsed = parse_destination(url)
        query = f"?{parsed.query}" if parsed.query else ""
        return f"{self.training_base}{parsed.path or '/'}{query}"

    def post(
        self,
        url: str,
        body: bytes,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> int:
        timeout = httpx.Timeout(timeout_seconds)
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                self._route(url),
                content=body,
                headers=headers,
```

### TypeScript — `capstone/tracks/typescript-fastify/src/webhooks.ts`

```typescript
import { canonicalJson, webhookSignature } from "./domain.js";
import { ApiProblem } from "./problems.js";

const APPROVED_HOST = "hooks.example.test";

/** Validate the logical public destination before it reaches the adapter. */
export function validateDestination(value: string): URL {
  let url: URL;
  try {
    url = new URL(value);
  } catch {
    throw invalidDestination("Webhook destination must be an absolute URL.");
  }

  if (
    url.protocol !== "https:" ||
    url.hostname !== APPROVED_HOST ||
    url.username !== "" ||
    url.password !== "" ||
    url.hash !== "" ||
    (url.port !== "" && url.port !== "443")
  ) {
    throw invalidDestination(
      "Webhook destinations must use the approved HTTPS host and port.",
    );
  }
  return url;
}

export function canonicalWebhookBody(value: unknown): Buffer {
  return Buffer.from(canonicalJson(value), "utf8");
}

export { webhookSignature };

/**
 * Course transport adapter.
 *
 * The application validates a public `https://hooks.example.test/...` URL.
 * Local exercises route only its path/query to the controlled receiver. This
 * indirection keeps the domain policy realistic without permitting arbitrary
 * network access during a self-contained lab.
 */
export class OutboundWebhookTransport {
  public constructor(private readonly trainingBase: string) {}

  private route(target: string): URL {
    const logical = validateDestination(target);
    const base = new URL(
      this.trainingBase.endsWith("/")
        ? this.trainingBase
        : `${this.trainingBase}/`,
    );
    const routed = new URL(logical.pathname.replace(/^\//, ""), base);
    routed.search = logical.search;
    return routed;
  }

  public async post(
    target: string,
```

Compare the two tracks by this invariant: **terminal run state and its outbound event commit together, while delivery attempts remain retryable and deduplicated**. The intended implementation difference is: HTTP client libraries differ; exact event bytes, identifier, signature, and retry state must match.

## Module synthesis

The module answer to “How can a committed domain outcome produce an external notification without losing intent or duplicating effects unpredictably?” is now executable in the capstone: Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.

## Next in the story

Module 09, [Failure-Oriented Verification](../module-09-failure-proof-architecture/index.md), asks: *How do we prove the service’s guarantees rather than infer them from happy-path unit tests?* The current checkpoint must remain green while that new responsibility is added.
