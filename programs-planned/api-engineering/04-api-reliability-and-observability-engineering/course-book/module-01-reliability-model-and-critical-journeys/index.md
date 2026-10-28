# Module 01 — Reliability Model and Critical Journeys

> **Program stage:** Course 4 of 10 — Observe, diagnose, contain, and recover the promise.

> **Central question:** Which user journeys matter, what makes them good or bad, and which durable facts establish the outcome?

## Where this module fits

Course 4 begins from this incoming boundary: **The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.**

This module establishes the course’s first new responsibility by asking: **Which user journeys matter, what makes them good or bad, and which durable facts establish the outcome?** Its capstone increment is **Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims**. That result is required before **Deadlines, Cancellation, and Retry Budgets** can be studied honestly.

## Learning outcomes

- Define critical journeys and eligible event populations.
- Separate prevention, mitigation, repair, and verification.
- Choose public or durable correctness oracles before telemetry.
- Catalog failure modes and residual risks.
- Trace reliability requirements to tests, runbooks, and owners.

## Capstone increment

Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims.

## Core reliability model

### Driving question

> What exactly must continue to work, for whom, under which failures, and how will we know?

Reliability is a property of user journeys and durable outcomes, not a synonym for process uptime.

### 1. Critical journey

A critical journey is an externally meaningful sequence such as submitting one analysis exactly once or retrieving a verified artifact. It crosses components and therefore cannot be represented by a single endpoint uptime percentage.

**Failure if confused.** A healthy API process can still fail the journey when an accepted run never starts.
### 2. Good, bad, eligible, excluded

An indicator needs an explicit population. Good and bad events are counted only inside an eligible set; exclusions represent client-owned or policy-owned outcomes rather than convenient removal of server failures.

**Failure if confused.** Excluding every 4xx is wrong because a server regression can reject valid credentials with 403.
### 3. Reliability invariant

An invariant states what must remain true across retries, restart, concurrency, and partial failure. It is stronger than an implementation detail and narrower than a slogan.

**Failure if confused.** A completed run has one consistent job, event, artifact, and outbox record.
### 4. Failure ownership

Failures are classified by the component that can prevent, detect, mitigate, or repair them, not whichever component first emits an error.

**Failure if confused.** A slow webhook receiver is external, but unbounded retries and duplicate delivery effects remain provider responsibilities.
### 5. Steady state

A steady-state statement defines normal behavior using user-visible and durable evidence and becomes the baseline for fault experiments.

**Failure if confused.** Ninety-nine percent of eligible accepted runs begin within thirty seconds.
### 6. Evidence hierarchy

Public observations, durable state, telemetry, and operator narrative answer different questions. Telemetry supports diagnosis but does not decide business correctness.

**Failure if confused.** A missing span cannot mean a run never completed; database and checksum decide completion.
### 7. Residual risk

Every design leaves bounded uncertainty. Recording it prevents local demonstrations from being presented as production proof.

**Failure if confused.** Dependency-light proof cannot demonstrate PostgreSQL lock behavior without PostgreSQL.

For a new Analysis Runs failure:

Apply **Critical journey, Good, bad, eligible, excluded, Reliability invariant** to this module’s capstone increment: Derive the reliability case for six Analysis Runs journeys and connect every reliability requirement to one failure mode and one verification. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Model journeys before components | Start with user outcomes, then map API, database, worker, storage, and webhook stages. | Component-only dashboard: All processes green while accepted runs stall | `journeys.yaml and architecture review` |
| 2 | Define event populations | Every SLI names eligible, good, bad, and excluded events with unambiguous ownership. | Undefined denominator: Objective changes when query changes | `slo-catalog.yaml validation` |
| 3 | Keep correctness durable | Database and artifact state remain authoritative; telemetry may be delayed, sampled, or dropped. | Telemetry as authority: Sampling changes correctness conclusion | `reconciliation and telemetry-loss tests` |
| 4 | Trace every requirement | Each REL requirement references a journey or failure mode and at least one verification. | No residual-risk record: Local proof presented as production evidence | `proof-map completeness check` |
| 5 | Separate mitigation from repair | A traffic shift or circuit opening is not root-cause correction. | Ambiguous ownership: Incident bounces between teams | `incident timeline review` |
| 6 | State environment boundaries | Local deterministic, live integration, and operated evidence are reported separately. | Mitigation called repair: Incident closes while defect remains | `FINAL-VERIFICATION.md` |
| 7 | Reject vanity availability | Process uptime alone cannot satisfy a journey objective. | Too many critical journeys: No priority exists | `counterexample exercise` |
| 8 | Prefer falsifiable claims | A reliability claim identifies what would disprove it. | No negative claim: Requirement cannot fail mechanically | `checkpoint defense` |


### Evidence boundary

The local corpus proves internal consistency of the reliability case; it cannot choose business criticality or objective targets for an actual organization.

## Worked failures

### Case 1 — Healthy API, stalled work

#### Initial system

POST /analysis-runs returns 202 and every health probe stays green, but no worker acquires the durable job. Endpoint availability is high while run-start freshness is zero.


#### Correct design

Define the journey from accepted response to first running event. Accepted committed runs are eligible; starts within thirty seconds are good. Durable job and event rows are the oracle.


#### Lesson

A process-level availability dashboard misses the failure.
### Case 2 — Telemetry success, durable failure

#### Initial system

A span reports artifact publication success, but the transaction recording the artifact rolls back.


#### Correct design

Terminal-state reconciliation checks run, job, event, artifact, and outbox. The service reports failure or retries; it does not trust the span.


#### Lesson

Telemetry can be emitted before durable commit.
### Case 3 — Misleading exclusion

#### Initial system

All 503 responses are excluded as overload, so the service can fail every request and still show perfect availability.


#### Correct design

Only outcomes outside provider responsibility—such as malformed credentials or explicit client cancellation—are excluded. Provider overload remains bad.


#### Lesson

An exclusion is a governance decision, not a query convenience.
### Case 4 — Unowned webhook delay

#### Initial system

The receiver is slow, so the provider declares webhook freshness outside its responsibility despite controlling deadlines, retry schedule, backlog, and duplicate handling.


#### Correct design

Separate receiver availability from provider delivery behavior. Measure acknowledgement within five minutes and classify external cause without erasing provider responsibility.


#### Lesson

External dependency does not mean no service responsibility.

## Python implementation

### Mechanism under review

Replay SLO and reconciliation vectors; inspect immutable findings and explicit insufficient-data states.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/slo.py`
- `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_slo_alerts.py`

### Executable invariant

```python
from api_reliability.slo import SLODefinition, SLOWindow, burn_rate

slo = SLODefinition("run-start", objective=0.995, window_seconds=28 * 86400)
window = SLOWindow(good=995, total=1_000)
assert burn_rate(slo, window) == 1.0
```

The cited files must expose the complete **Reliability Model and Critical Journeys** implementation path and its negative regression evidence.

### Guided failure investigation — Healthy API, stalled work

**Initial condition.** POST /analysis-runs returns 202 and every health probe stays green, but no worker acquires the durable job. Endpoint availability is high while run-start freshness is zero.

**Expected repair.** Define the journey from accepted response to first running event. Accepted committed runs are eligible; starts within thirty seconds are good. Durable job and event rows are the oracle.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=01 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **Component-only dashboard.** All processes green while accepted runs stall The decisive check is journey SLI and durable-state check.
- **Undefined denominator.** Objective changes when query changes The decisive check is versioned SLI definition.
- **Telemetry as authority.** Sampling changes correctness conclusion The decisive check is database/artifact oracle.
- **No residual-risk record.** Local proof presented as production evidence The decisive check is evidence-boundary review.
- **Ambiguous ownership.** Incident bounces between teams The decisive check is failure-owner matrix.
- **Mitigation called repair.** Incident closes while defect remains The decisive check is action taxonomy.

## TypeScript implementation

### Mechanism under review

Replay the same vectors; preserve exact count math and bigint-safe identifiers while keeping runtime-specific syntax idiomatic.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/slo.ts`
- `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

### Executable invariant

```typescript
const slo = { id: "run-start", objective: 0.995, windowSeconds: 28 * 86_400, version: "1.0" };
const rate = burnRate(slo, { good: 995, total: 1_000 });
if (rate !== 1) throw new Error("unexpected burn rate");
```

The cited files must expose the complete **Reliability Model and Critical Journeys** implementation path and its negative regression evidence.

### Guided failure investigation — Healthy API, stalled work

**Initial condition.** POST /analysis-runs returns 202 and every health probe stays green, but no worker acquires the durable job. Endpoint availability is high while run-start freshness is zero.

**Expected repair.** Define the journey from accepted response to first running event. Accepted committed runs are eligible; starts within thirty seconds are good. Durable job and event rows are the oracle.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=01 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **Component-only dashboard.** All processes green while accepted runs stall The decisive check is journey SLI and durable-state check.
- **Undefined denominator.** Objective changes when query changes The decisive check is versioned SLI definition.
- **Telemetry as authority.** Sampling changes correctness conclusion The decisive check is database/artifact oracle.
- **No residual-risk record.** Local proof presented as production evidence The decisive check is evidence-boundary review.
- **Ambiguous ownership.** Incident bounces between teams The decisive check is failure-owner matrix.
- **Mitigation called repair.** Incident closes while defect remains The decisive check is action taxonomy.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **Component-only dashboard** | It is easy to organize charts by deployable component because infrastructure exports metrics that way. | A user journey can fail across several healthy-looking components. | A component smoke test never evaluates the end-to-end outcome population. | journey SLI and durable-state check. |
| **Undefined denominator** | A percentage can be produced quickly when the eligible population is left implicit. | Different readers include retries, cancellations, or no-traffic windows differently. | A happy-path test observes one event, not the population definition. | versioned SLI definition. |
| **Telemetry as authority** | Logs and traces are immediately visible while database evidence is slower to inspect. | Dropped or duplicated telemetry can contradict committed state. | The success test usually emits both the state change and the span, so the distinction stays hidden. | database/artifact oracle. |
| **No residual-risk record** | Teams prefer a green checklist to an explicit statement of remaining uncertainty. | Uncovered failure modes silently become operational assumptions. | Ordinary tests exercise implemented controls, not the risks outside their scope. | evidence-boundary review. |
| **Ambiguous ownership** | A shared reliability document can appear collaborative. | No one is accountable for the requirement, alert, repair, or release decision. | The mechanism can pass while response ownership remains undefined. | failure-owner matrix. |
| **Mitigation called repair** | Reducing symptoms often looks like recovery. | The authoritative inconsistency remains and may reappear after traffic returns. | A short test ends before the unrepaired state causes another failure. | action taxonomy. |
| **Too many critical journeys** | Declaring every endpoint critical avoids prioritization conflict. | Attention, alerts, and error budgets become too diffuse to guide action. | Endpoint tests do not reveal whether the chosen set supports real user outcomes. | business impact ranking. |
| **No negative claim** | Positive requirements are easier to automate. | Readers infer that the proof established live behavior, durability, or production readiness it never executed. | A passing route reports what it checked, not the tempting conclusions it must reject. | planted counterexample. |

## What you add to the capstone

### Increment

Derive the reliability case for six Analysis Runs journeys and connect every reliability requirement to one failure mode and one verification.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/slo.py`
- `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_slo_alerts.py`
- `capstone/tracks/typescript-fastify/src/reliability/slo.ts`
- `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Model journeys before components.** Start with user outcomes, then map API, database, worker, storage, and webhook stages.
- **Define event populations.** Every SLI names eligible, good, bad, and excluded events with unambiguous ownership.
- **Keep correctness durable.** Database and artifact state remain authoritative; telemetry may be delayed, sampled, or dropped.
- **Trace every requirement.** Each REL requirement references a journey or failure mode and at least one verification.
- The planted failure **Healthy API, stalled work** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Healthy API, stalled work**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Define the journey from accepted response to first running event. Accepted committed runs are eligible; starts within thirty seconds are good. Durable job and event rows are the oracle.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “What exactly must continue to work, for whom, under which failures, and how will we know?” is decided by durable state rather than telemetry?
2. What is the smallest fault that disproves the design?
3. Which label, context value, or event field could become unbounded?
4. What happens after restart halfway through the operation?
5. Which Course 3 security constraint could observability violate?
6. Which proof is local and which needs a live environment?
7. How do the two tracks preserve the same invariant idiomatically?
8. What behavior would block release despite OpenAPI compatibility?

### Required artifacts

Record `accept`, `accept-with-residual-risk`, or `reject`. A rejection names the failed requirement and exact evidence needed for reconsideration.

## Representative implementation

These are the smallest useful entry points for **Reliability Model and Critical Journeys**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/http.py`

```python


@dataclass(frozen=True, slots=True)
class HttpOutcome:
    eligibility: str
    outcome: str


def classify_http_outcome(operation: str, status: int) -> HttpOutcome:
    """Classify one completed request for the course availability SLI.

    Client-policy and validation failures are excluded because the service
    fulfilled the protocol correctly. Timeout, overload, and server failures
    remain eligible bad events because they represent unavailable service for a
    valid journey. The policy is explicit and shared by both implementations.
    """

    if not 100 <= status <= 599:
        raise ValueError("status must be an HTTP status code")
    if operation.startswith("internal") or operation.startswith("/internal/"):
        return HttpOutcome("excluded", "neutral")
    if 200 <= status < 400:
        return HttpOutcome("eligible", "good")
    if status in {408, 425, 429} or status >= 500:
        return HttpOutcome("eligible", "bad")
    return HttpOutcome("excluded", "neutral")
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/http.ts`

```typescript
export interface HttpOutcome {
  readonly eligibility: "eligible" | "excluded";
  readonly outcome: "good" | "bad" | "neutral";
}

export function classifyHttpOutcome(operation: string, status: number): HttpOutcome {
  if (!Number.isSafeInteger(status) || status < 100 || status > 599) {
    throw new Error("status must be an HTTP status code");
  }
  if (operation.startsWith("internal") || operation.startsWith("/internal/")) {
    return { eligibility: "excluded", outcome: "neutral" };
  }
  if (status >= 200 && status < 400) {
    return { eligibility: "eligible", outcome: "good" };
  }
  if ([408, 425, 429].includes(status) || status >= 500) {
    return { eligibility: "eligible", outcome: "bad" };
  }
  return { eligibility: "excluded", outcome: "neutral" };
}
```

Compare the two tracks by this invariant: **eligible, good, bad, and excluded populations are defined before telemetry and tied to durable user outcomes**. The intended implementation difference is: data types differ; the same operation/status pair must receive the same classification.

## Module synthesis

You are ready to leave this module when you can **Define critical journeys and eligible event populations, Separate prevention, mitigation, repair, and verification, and Choose public or durable correctness oracles before telemetry** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a component-only availability claim that ignores stalled jobs** and requiring the following oracle: **Every active REL requirement has a source and proof; Stalled jobs fail run-start freshness while API health remains green; Provider-owned 5xx and timeout outcomes cannot be excluded; Durable state decides terminal correctness.**

The cumulative platform now includes **Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Deadlines, Cancellation, and Retry Budgets](../module-02-deadlines-timeouts-cancellation-and-retry-budgets/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
