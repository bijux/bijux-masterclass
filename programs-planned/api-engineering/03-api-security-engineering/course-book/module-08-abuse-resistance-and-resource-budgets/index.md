# Module 08 — Abuse Resistance and Resource Budgets

> **Program stage:** Course 3 of 6 — Defend the promise.

> **Central question:** How can the service resist brute force and resource exhaustion without turning traffic control into false authorization?

## Where this module fits

Apply principal-, tenant-, operation-, cost-, storage-, and concurrency-aware budgets. You arrive from Module 07 with all earlier checkpoints still green. API 1.2 and its durable service behavior are fixed. This course adds controls derived from explicit threats; it does not redefine successful business outcomes or treat middleware configuration as proof of security. The result is the baseline for **Adversarial Verification and Supply-Chain Assurance**.

## Learning outcomes

- Choose rate-limit dimensions from abuse paths.
- Implement deterministic token-bucket behavior.
- Limit simultaneous expensive work with leak-free permits.
- Bound uploads, streams, queue depth, and storage.
- Return coherent `429` or `503` outcomes without amplifying retries.

## Capstone result

Introduce principal/tenant/operation/cost budgets, concurrency permits, quotas, and bounded degradation.

Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.

## Core security model

> How does the API remain available and fair when callers use valid operations at malicious or excessive rates?

Availability security requires explicit budgets for rate, concurrency, bytes, queue depth, storage, and stream lifetime. Controls must be keyed to the protected resource, cost-aware, deterministic under test, and honest about single-process versus distributed scope.

Separate public behavior, control decision, authoritative state, evidence, and operating assumption for every concept.

### 1. Budget dimension

Requests, concurrent work, bytes, CPU-weight, queue slots, storage, and connection time are distinct resources.

Keys combine tenant, principal, operation, credential, network source, or global pool according to the threat; no one key fits all abuse.

Capacity permits a bounded burst; refill rate controls sustained use. Fixed-point arithmetic avoids floating drift in deterministic tests.

An operation acquires a permit before expensive work and releases it on success, failure, cancellation, and timeout.

Reject before durable/expensive effects when required capacity is unavailable; estimate cost from server-controlled rules.

Longer-window consumption such as uploaded bytes, artifact storage, or analysis units is durable and auditable.

Producers slow or reject when consumers and queues saturate rather than buffering without bound.

Use coherent `429` for caller/tenant budgets and `503` for service capacity, with bounded retry guidance and no amplification.

## Abuse control is resource accounting

Valid credentials and schema-valid requests can still exhaust CPU, memory, database connections, worker slots, storage, or outbound delivery capacity. A requests-per-minute counter is therefore one instrument, not a complete availability-security design.

Inventory expensive resources per operation. Dataset upload consumes ingress bandwidth, staging space, checksum CPU, and storage. Analysis submission consumes a durable row, queue capacity, worker time, artifact space, and possible webhook retries. Event streaming consumes a connection and periodic work over time. Assign admission checks before the first expensive or irreversible effect.

Use several budget dimensions:

- principal and tenant request rate;
- operation-specific cost units;
- concurrent uploads, analyses, streams, and webhook attempts;
- queued work and oldest age;
- bytes per object and per tenant;
- daily or monthly quota where business policy requires it;
- invalid-credential and identifier-enumeration behavior at the edge.

A token bucket permits bounded bursts and refills over time. Use integer or fixed-point arithmetic so Python and JavaScript do not diverge at floating boundaries. Charge attempts that consume parsing or cryptographic work even when they fail. Define whether a rejected request consumes a token and test the boundary exactly.

Concurrency permits protect scarce simultaneous resources. Acquire before opening the expensive dependency or reading the full upload. Release in a `finally` path on success, exception, cancellation, and client disconnect. A leaked permit is a slow availability incident; a permit acquired after work starts is not admission control.

### Scope claims honestly

An in-process limiter protects one process. It does not enforce a tenant-wide budget across replicas. A database- or Redis-backed design introduces consistency, latency, partition, and fail-open/fail-closed choices. The course can prove local arithmetic and lifecycle while explicitly reserving distributed enforcement for a later performance/traffic course.

Retry responses must not synchronize clients into another burst. `Retry-After` should be truthful for the enforced budget; clients should still use jitter where policy permits. Use 429 for a caller budget and 503 for service-wide inability to admit valid work, with documented bodies and no false promise that retry is always safe.

Enumeration resistance combines authorization-aware queries, concealment, bounded invalid attempts, and uniform response shape. It does not require making every response take exactly the same time, which is usually impractical; it requires removing deterministic high-signal differences and monitoring repeated probes.

The completion proof measures bounded behavior under bursts, low-and-slow streams, canceled uploads, repeated invalid credentials, noisy tenants, and failing webhook destinations. The service must degrade by rejecting new work before it corrupts accepted work.

## Security requirements and standards

1. The service MUST satisfy **Budget dimension**: Requests, concurrent work, bytes, CPU-weight, queue slots, storage, and connection time are distinct resources.
2. The service MUST satisfy **Budget identity**: Keys combine tenant, principal, operation, credential, network source, or global pool according to the threat; no one key fits all abuse.
3. The service MUST satisfy **Token bucket**: Capacity permits a bounded burst; refill rate controls sustained use. Fixed-point arithmetic avoids floating drift in deterministic tests.
4. The service MUST satisfy **Concurrency permit**: An operation acquires a permit before expensive work and releases it on success, failure, cancellation, and timeout.
5. The service MUST satisfy **Admission control**: Reject before durable/expensive effects when required capacity is unavailable; estimate cost from server-controlled rules.
6. The service MUST satisfy **Quota**: Longer-window consumption such as uploaded bytes, artifact storage, or analysis units is durable and auditable.
7. The service MUST satisfy **Backpressure**: Producers slow or reject when consumers and queues saturate rather than buffering without bound.
8. The service MUST satisfy **Failure contract**: Use coherent `429` for caller/tenant budgets and `503` for service capacity, with bounded retry guidance and no amplification.

## Worked attacks and defenses

Run only against course fixtures. The goal is to understand control boundaries, not to maximize payload novelty.

### Attack 1 — Valid-operation flood

A legitimate token submits many expensive analyses within schema and authorization rules.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 2 — Low-and-slow streams

Many event streams remain open and consume connection/memory state without high request rate.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 3 — Upload concurrency

Several individually legal uploads exceed memory, staging disk, or file-descriptor capacity together.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 4 — Identifier enumeration

A caller sends many cheap object lookups to discover valid IDs or timing differences.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 5 — Retry amplification

Clients retry `429`/`503` immediately or multiple internal layers retry the same failing dependency.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 6 — Noisy tenant

One tenant fills the global worker queue and starves others.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.

### Prioritization

Rank these attacks using explicit asset impact, caller capability, exposure, and confidence in controls. Record which require environment-backed evidence.

## Python implementation

### Reference design

Implement a deterministic fixed-point token bucket with injected monotonic clock, a context-managed concurrency permit, and a composite budget key. Keep the in-memory reference labeled single-process. Add an interface for a durable/distributed store without pretending the local map coordinates replicas.

### Work method

Use explicit immutable inputs, narrow exception taxonomies, and standard-library/PyJWT cryptography through named profiles.

## TypeScript implementation

### Reference design

Use integer microtokens or bigint nanounits and an injected monotonic time source. Make permit release idempotent and safe in `finally`. Avoid timers as the authority; compute refill from stored timestamp. Test abort/cancellation and queue admission explicitly.

## Failure patterns

### 1. One global requests-per-minute limit for all operations and tenants.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 2. Charging only successful requests, making invalid expensive parsing free.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 3. Acquiring a permit after starting the expensive effect.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 4. Forgetting to release on exception or disconnect.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 5. Using process memory while claiming multi-replica enforcement.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 6. Returning retry hints that synchronize all clients into another burst.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

## What you add to the capstone

### Objective

Apply operation-specific budgets to run submission, uploads, event streams, artifact reads, and webhook registration. Simulate time deterministically, test cancellation, and plant a permit leak plus global-only limiter; prove starvation/leak before repair.

### Required artifacts

Do not modify predecessor bytes or convert missing environment capabilities into passes.

## Representative implementation

These are the smallest useful entry points for **Abuse Resistance and Resource Budgets**.

### Python — `capstone/tracks/python-fastapi/src/api_security/abuse.py`

```python


@dataclass(slots=True)
class TokenBucket:
    capacity_units: int
    refill_units_per_second: int
    tokens_units: int | None = None
    last_ms: int = 0
    scale: int = 1_000_000
    _capacity: int = field(init=False, repr=False)
    _refill_per_second: int = field(init=False, repr=False)
    _tokens: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.capacity_units <= 0 or self.refill_units_per_second < 0:
            raise ValueError("invalid bucket configuration")
        self._capacity = self.capacity_units * self.scale
        self._refill_per_second = self.refill_units_per_second * self.scale
        self._tokens = self._capacity if self.tokens_units is None else self.tokens_units * self.scale

    def allow(self, *, now_ms: int, cost_units: int = 1) -> bool:
        if now_ms < self.last_ms or cost_units <= 0:
            raise ValueError("invalid token-bucket input")
        elapsed = now_ms - self.last_ms
        refill = (elapsed * self._refill_per_second) // 1000
        self._tokens = min(self._capacity, self._tokens + refill)
        self.last_ms = now_ms
        cost = cost_units * self.scale
        if self._tokens < cost:
            return False
        self._tokens -= cost
        return True


class ConcurrencyLimiter:
    def __init__(self, limit: int) -> None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        self.limit = limit
        self.in_use = 0
        self._lock = Lock()

    def try_acquire(self) -> "Permit | None":
        with self._lock:
            if self.in_use >= self.limit:
                return None
            self.in_use += 1
            return Permit(self)

    def _release(self) -> None:
        with self._lock:
            if self.in_use <= 0:
                raise RuntimeError("permit accounting underflow")
            self.in_use -= 1


class Permit:
    def __init__(self, limiter: ConcurrencyLimiter) -> None:
        self._limiter = limiter
        self._released = False

    def release(self) -> None:
        if not self._released:
            self._limiter._release()
            self._released = True
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/abuse.ts`

```typescript
export class TokenBucket {
  readonly #capacity:number; readonly #refillPerSecond:number; #tokens:number; #lastMs=0; readonly #scale=1_000_000;
  constructor(capacityUnits:number,refillUnitsPerSecond:number){if(capacityUnits<=0||refillUnitsPerSecond<0)throw new Error("invalid bucket configuration");this.#capacity=capacityUnits*this.#scale;this.#refillPerSecond=refillUnitsPerSecond*this.#scale;this.#tokens=this.#capacity;}
  allow(nowMs:number,costUnits=1):boolean{if(!Number.isSafeInteger(nowMs)||nowMs<this.#lastMs||costUnits<=0)throw new Error("invalid token-bucket input");const elapsed=nowMs-this.#lastMs;this.#tokens=Math.min(this.#capacity,this.#tokens+Math.floor(elapsed*this.#refillPerSecond/1000));this.#lastMs=nowMs;const cost=costUnits*this.#scale;if(this.#tokens<cost)return false;this.#tokens-=cost;return true;}
}
export class ConcurrencyLimiter { #inUse=0; constructor(readonly limit:number){if(limit<=0)throw new Error("limit must be positive");} get inUse():number{return this.#inUse;} tryAcquire():Permit|undefined{if(this.#inUse>=this.limit)return undefined;this.#inUse+=1;return new Permit(()=>{if(this.#inUse<=0)throw new Error("permit accounting underflow");this.#inUse-=1;});}}
export class Permit { #released=false; constructor(private readonly releaseFn:()=>void){} release():void{if(!this.#released){this.releaseFn();this.#released=true;}} }
```

Compare the two tracks by this invariant: **cost is charged before expensive work and bounded by principal, tenant, operation, concurrency, storage, and time dimensions**. The intended implementation difference is: permit and clock implementations differ; no exception or disconnect may leak capacity.

## Module synthesis

The module answer to “How does the API keep expensive operations bounded when valid-looking clients consume resources aggressively?” is now executable in the capstone: Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.

## Next in the story

Module 09, [Adversarial Verification and Supply-Chain Assurance](../module-09-adversarial-verification-and-supply-chain/index.md), asks: *How do we know a security check detects a missing control rather than merely confirming the control is present?* The current checkpoint must remain green while that new responsibility is added.
