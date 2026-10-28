# Module 08 — SLOs, Error Budgets, Dashboards, and Alerts

> **Program stage:** Course 4 of 6 — Operate and recover the promise.

> **Central question:** How do versioned SLOs, exact error budgets, burn rates, dashboards, alerts, and runbooks drive decisions?

## Where this module fits

Define rolling objectives, calculate budget consumption, and alert on sustained burn with runbook context. You arrive from Module 07 with all earlier checkpoints still green. API 1.2 and security profile 1.0 are fixed. This course adds budgets, telemetry, recovery, and operational decisions; observations may explain durable truth but never replace it. The result is the baseline for **Fault Injection, Troubleshooting, and Game Days**.

## Learning outcomes

- Choose objectives from critical journeys.
- Calculate compliance and remaining error budget.
- Use multiwindow burn-rate alerts.
- Design dashboards from outcomes to causes.
- Handle insufficient data and planned exclusions explicitly.

## Capstone result

Publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy.

Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.

## Core reliability model

### Driving question

> How do measurements become explicit reliability decisions, release constraints, and actionable alerts without turning targets into vanity numbers?

An SLO is a versioned decision about an SLI over a window. Its error budget governs risk, dashboards explain current state, and alerts page only when timely human action can protect a critical journey.

### 1. Objective

An SLO sets a target for a defined SLI over a window. It is an engineering policy, not a universal constant or marketing promise.

**Failure if confused.** “99.9% uptime” without event population, window, and exclusions is not an SLO.
### 2. Error budget

The allowed bad-event proportion converts an objective into finite risk. Consuming budget is not automatically an incident, but it changes release and mitigation decisions.

**Failure if confused.** A 99.9% objective permits 0.1% bad eligible events; it does not promise no failures.
### 3. Rolling window

A rolling window continuously reflects recent service behavior; calendar windows align with reporting but create boundary effects. The choice is explicit.

**Failure if confused.** Resetting budget at month start can hide a sustained failure spanning the boundary.
### 4. Burn rate

Burn rate compares actual error consumption with the rate that would exhaust the budget over the objective window.

**Failure if confused.** One percent errors may be catastrophic for a 99.99% target and modest for a 95% target.
### 5. Multiwindow alert

A fast/slow pair requires sustained high burn across two windows, balancing urgency and noise.

**Failure if confused.** A single five-minute spike may page repeatedly even when the long window is healthy.
### 6. Dashboard hierarchy

A dashboard starts with user journeys and SLO state, then exposes dependency and resource evidence for diagnosis.

**Failure if confused.** A wall of CPU charts cannot tell whether artifact retrieval works.
### 7. Runbook linkage

Every actionable alert has an owner, first checks, safe mitigations, stop conditions, and escalation.

**Failure if confused.** An alert named HighErrorRate with no journey or action creates operator guessing.
### 8. Release policy

Error-budget state and observability coverage influence change risk. The policy is explicit and permits documented exceptions.

**Failure if confused.** Automatically blocking every release during budget burn may prevent the repair release itself.

For a new Analysis Runs failure:

Apply **Objective, Error budget, Rolling window** to this module’s capstone increment: Calculate rolling SLOs and error budgets, implement multiwindow burn-rate alerts, build a journey-first dashboard, link alerts to tested runbooks, and reject an unobservable release. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Version every SLO | Indicator, target, window, threshold, and exclusions have a stable version. | Unversioned objective: Historical numbers change meaning | `slo catalog validation` |
| 2 | Use exact event counts | Availability and freshness budgets derive from eligible/good/bad counts, not rounded percentages. | Rounded percentage math: Small populations hide budget use | `SLO vector tests` |
| 3 | Define low-traffic behavior | Insufficient data, longer windows, and synthetic probes are policy choices. | No-data treated green: Instrumentation outage masks failure | `low-traffic vectors` |
| 4 | Alert on budget burn | Page on rates that threaten the objective, not arbitrary raw thresholds alone. | Single-window page: Noise or missed sustained burn | `alert vector tests` |
| 5 | Require multiwindow confirmation | Paging alerts use fast and slow windows unless a documented hard invariant demands immediate action. | Alert without owner: No accountable response | `alert rule review` |
| 6 | Link every page to a runbook | Alert annotations reference an existing tested runbook and owner. | Dashboard by component: Journey failure remains hidden | `alert-runbook proof` |
| 7 | Keep dashboards journey-first | Top panels show SLO state, eligible volume, error budget, and freshness. | Runbook never tested: First use occurs during incident | `dashboard schema review` |
| 8 | Reject unobservable releases | A release removing required SLIs, adding unbounded labels, or coupling health to telemetry cannot pass. | Rigid release freeze: Repair cannot ship | `release proof` |


### Evidence boundary

Synthetic windows prove budget and alert calculations; objective suitability, paging policy, and operator response require service ownership and historical evidence.

## Worked failures


### Case 1 — Raw error-rate page

#### Initial system

The service pages whenever five-minute 5xx exceeds one percent, regardless of SLO target or traffic. Low-volume single failures page; high-volume budget exhaustion may not.


#### Correct design

Compute burn relative to the SLO and require paired short/long windows. Keep separate immediate alerts for hard safety invariants.


#### Lesson

Alert urgency comes from objective risk and actionability.
### Case 2 — Dashboard shows only dependencies

#### Initial system

PostgreSQL, CPU, and memory panels are green while run-start freshness is failing because workers are not claiming jobs.


#### Correct design

Place journey SLO panels first, then queue age, claim rate, lease expiry, and dependency panels for diagnosis.


#### Lesson

Resource health explains; it does not define customer outcome.
### Case 3 — Release removes metric

#### Initial system

A refactor deletes the run-start event and dashboard remains green due to no data.


#### Correct design

Treat missing required SLI input as an observability defect, expose data freshness, and reject the release through the reliability profile.


#### Lesson

No data must not be interpreted as good.
### Case 4 — Budget freeze blocks repair

#### Initial system

The release policy blocks all deployments after budget exhaustion, including a tested fix.


#### Correct design

Permit an explicit repair exception with incident owner, rollback, focused proof, and heightened observation.


#### Lesson

Policy should manage risk, not prevent recovery.

## Python implementation

### Mechanism under review

Compute exact objective states and multiwindow alerts with explicit insufficient-data results; validate runbook linkage and release policy.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/slo.py`
- `capstone/tracks/python-fastapi/src/api_reliability/alerts.py`
- `capstone/tracks/python-fastapi/src/api_reliability/runbooks.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_slo_alerts.py`

### Executable invariant

```python
from api_reliability.alerts import BurnRateAlert, evaluate_burn_rate_alert
from api_reliability.slo import SLODefinition, SLOWindow

result = evaluate_burn_rate_alert(
    SLODefinition("api", 0.999, 28 * 86400),
    BurnRateAlert("fast", "page", 3600, 300, 14.4, minimum_events=100),
    long_window=SLOWindow(good=9_980, total=10_000),
    short_window=SLOWindow(good=980, total=1_000),
)
assert result.firing is True
```

The cited files own the complete implementation and regression evidence.

### Guided failure investigation — Raw error-rate page

**Initial condition.** The service pages whenever five-minute 5xx exceeds one percent, regardless of SLO target or traffic. Low-volume single failures page; high-volume budget exhaustion may not.

**Expected repair.** Compute burn relative to the SLO and require paired short/long windows. Keep separate immediate alerts for hard safety invariants.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=08 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **Unversioned objective.** Historical numbers change meaning The decisive check is catalog history.
- **Rounded percentage math.** Small populations hide budget use The decisive check is exact count calculation.
- **No-data treated green.** Instrumentation outage masks failure The decisive check is freshness panel and state.
- **Single-window page.** Noise or missed sustained burn The decisive check is multiwindow vector.
- **Alert without owner.** No accountable response The decisive check is catalog linkage.
- **Dashboard by component.** Journey failure remains hidden The decisive check is journey panel review.

## TypeScript implementation

### Mechanism under review

Use discriminated result types and exact integer event counts; avoid floating truthiness and preserve the same alert decisions across shared vectors.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/slo.ts`
- `capstone/tracks/typescript-fastify/src/reliability/alerts.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

### Executable invariant

```typescript
const decision = evaluateBurnRateAlert(
  { id: "api", objective: 0.999, windowSeconds: 28 * 86_400, version: "1.0" },
  { id: "fast", severity: "page", longWindowSeconds: 3_600,
    shortWindowSeconds: 300, threshold: 14.4, minimumEvents: 100 },
  { good: 9_980, total: 10_000 }, { good: 980, total: 1_000 },
);
if (!decision.firing) throw new Error("expected fast burn");
```

The cited files own the complete implementation and regression evidence.

### Guided failure investigation — Raw error-rate page

**Initial condition.** The service pages whenever five-minute 5xx exceeds one percent, regardless of SLO target or traffic. Low-volume single failures page; high-volume budget exhaustion may not.

**Expected repair.** Compute burn relative to the SLO and require paired short/long windows. Keep separate immediate alerts for hard safety invariants.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=08 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **Unversioned objective.** Historical numbers change meaning The decisive check is catalog history.
- **Rounded percentage math.** Small populations hide budget use The decisive check is exact count calculation.
- **No-data treated green.** Instrumentation outage masks failure The decisive check is freshness panel and state.
- **Single-window page.** Noise or missed sustained burn The decisive check is multiwindow vector.
- **Alert without owner.** No accountable response The decisive check is catalog linkage.
- **Dashboard by component.** Journey failure remains hidden The decisive check is journey panel review.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **Unversioned objective** | Editing one YAML value is simple. | Historical decisions cannot be interpreted against the objective in force. | The current calculation still passes. | catalog history. |
| **Rounded percentage math** | Displayed percentages are reused in automation. | Rounding changes burn and release decisions near the threshold. | Values are far from the boundary in examples. | exact count calculation. |
| **No-data treated green** | No failures are observed. | An absent measurement population appears healthy. | Tests always provide events. | freshness panel and state. |
| **Single-window page** | One fast burn alert is easy to understand. | Brief noise pages or slow exhaustion is missed. | The fixture models only one timescale. | multiwindow vector. |
| **Alert without owner** | The expression is considered the main work. | No one is accountable for triage or repair. | Rule syntax tests do not exercise response. | catalog linkage. |
| **Dashboard by component** | Infrastructure metrics are readily available. | The user journey and its budget are fragmented. | Each component looks healthy in isolation. | journey panel review. |
| **Runbook never tested** | A document exists and appears complete. | Commands, permissions, and assumptions fail during an incident. | Static review cannot prove operational usability. | game-day evidence. |
| **Rigid release freeze** | A single budget threshold seems objective. | Low-risk repairs and high-risk changes are treated identically. | The simple fixture does not encode decision context. | exception policy test. |

## What you add to the capstone

### Increment

Calculate rolling SLOs and error budgets, implement multiwindow burn-rate alerts, build a journey-first dashboard, link alerts to tested runbooks, and reject an unobservable release.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/slo.py`
- `capstone/tracks/python-fastapi/src/api_reliability/alerts.py`
- `capstone/tracks/python-fastapi/src/api_reliability/runbooks.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_slo_alerts.py`
- `capstone/tracks/typescript-fastify/src/reliability/slo.ts`
- `capstone/tracks/typescript-fastify/src/reliability/alerts.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Version every SLO.** Indicator, target, window, threshold, and exclusions have a stable version.
- **Use exact event counts.** Availability and freshness budgets derive from eligible/good/bad counts, not rounded percentages.
- **Define low-traffic behavior.** Insufficient data, longer windows, and synthetic probes are policy choices.
- **Alert on budget burn.** Page on rates that threaten the objective, not arbitrary raw thresholds alone.
- The planted failure **Raw error-rate page** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Raw error-rate page**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Compute burn relative to the SLO and require paired short/long windows. Keep separate immediate alerts for hard safety invariants.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How do measurements become explicit reliability decisions, release constraints, and actionable alerts without turning targets into vanity numbers?” is decided by durable state rather than telemetry?
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

These are the smallest useful entry points for **SLOs, Error Budgets, Dashboards, and Alerts**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/slo.py`

```python


@dataclass(frozen=True, slots=True)
class SLODefinition:
    identifier: str
    objective: float
    window_seconds: int
    description: str = ""
    version: str = "1.0"

    def __post_init__(self) -> None:
        if not 0 < self.objective < 1:
            raise ValueError("objective must be between zero and one")
        if self.window_seconds <= 0:
            raise ValueError("window must be positive")
        if not self.version or len(self.version) > 40:
            raise ValueError("SLO definition version must contain 1..40 characters")

    @property
    def allowed_bad_fraction(self) -> float:
        return 1.0 - self.objective


@dataclass(frozen=True, slots=True)
class SLOWindow:
    good: int
    total: int

    def __post_init__(self) -> None:
        if self.good < 0 or self.total < 0 or self.good > self.total:
            raise ValueError("invalid SLO event counts")

    @property
    def bad(self) -> int:
        return self.total - self.good

    @property
    def compliance(self) -> float | None:
        return None if self.total == 0 else self.good / self.total


def error_budget_events(definition: SLODefinition, total: int) -> float:
    if total < 0:
        raise ValueError("total must be non-negative")
    return definition.allowed_bad_fraction * total


def burn_rate(definition: SLODefinition, window: SLOWindow) -> float | None:
    if window.total == 0:
        return None
    observed_bad_fraction = window.bad / window.total
    return observed_bad_fraction / definition.allowed_bad_fraction


def budget_remaining_fraction(
    definition: SLODefinition,
    window: SLOWindow,
) -> float | None:
    allowed = error_budget_events(definition, window.total)
    if window.total == 0 or allowed == 0:
        return None
    return (allowed - window.bad) / allowed
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/slo.ts`

```typescript
export interface SLODefinition { readonly id: string; readonly objective: number; readonly windowSeconds: number; readonly description?: string; readonly version?: string }
export interface SLOWindow { readonly good: number; readonly total: number }

export function validateSLO(definition: SLODefinition): void {
  if (!(definition.objective > 0 && definition.objective < 1)) throw new Error("objective must be between zero and one");
  if (definition.windowSeconds <= 0) throw new Error("window must be positive");
  const version = definition.version ?? "1.0";
  if (version.length < 1 || version.length > 40) throw new Error("SLO definition version must contain 1..40 characters");
}
export function bad(window: SLOWindow): number { if (window.good < 0 || window.total < window.good) throw new Error("invalid counts"); return window.total - window.good; }
export function compliance(window: SLOWindow): number | undefined { return window.total === 0 ? undefined : window.good / window.total; }
export function burnRate(definition: SLODefinition, window: SLOWindow): number | undefined {
  validateSLO(definition); if (window.total === 0) return undefined; return (bad(window) / window.total) / (1 - definition.objective);
}
export function budgetRemainingFraction(definition: SLODefinition, window: SLOWindow): number | undefined {
  validateSLO(definition); if (window.total === 0) return undefined;
  const allowed = (1 - definition.objective) * window.total; return (allowed - bad(window)) / allowed;
}
```

Compare the two tracks by this invariant: **objectives operate on exact eligible populations and multiwindow burn alerts require both fast and slow evidence with no-data handling**. The intended implementation difference is: query syntax differs from pure model code; computed compliance, budget, and alert state must match.

## Module synthesis

The module answer to “How do operational signals become explicit objectives and actionable decisions rather than decorative dashboards?” is now executable in the capstone: Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.

## Next in the story

Module 09, [Fault Injection, Troubleshooting, and Game Days](../module-09-fault-injection-troubleshooting-and-game-days/index.md), asks: *Can the system and its operators detect a controlled failure, find the durable cause, mitigate it, and return to a verified steady state?* The current checkpoint must remain green while that new responsibility is added.
