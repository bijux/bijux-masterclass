# Refactor 2: Configs and Rules → Dataclasses, Null-Safe APIs, Typestate & Hypothesis

## Goal

Apply Module 3 as an engineering refactor: make the monitoring system’s configuration and rule model *structurally correct*.

Deliverables:
- dataclass-based domain model with semantic value types,
- typestate for rule lifecycle (Draft/Active/Retired),
- boundary DTO validation + translation,
- null-safe APIs (no `Optional` in core collections),
- tests including **property-based tests** for invariants and transitions.

## Where This Fits

Running example: a monitoring service that fetches metrics, evaluates rules, and emits alerts. In earlier modules we refactored toward a layered design (domain/application/infrastructure) with explicit roles. From M03 onward, we tighten *data integrity* and *lifecycle semantics* so the system stays correct under change.

## 1. Starting Point: What We’re Fixing

Typical baseline symptoms (from M01–M02 style code):
- rules are dicts: `{"metric": "...", "threshold": ...}`
- optional fields are everywhere: `activated_at: Optional[float]`
- `None` leaks into lists and lookups return `None`
- lifecycle is encoded as ad-hoc flags (`enabled`, `deleted`, `status="active"`)

These are correctness hazards because the model permits invalid combinations.

## 2. Target Shape (High-Level)

Your end state should look like:

- **Domain value types**: `MetricName`, `Threshold`, `Window`
- **Typestate rules**: `DraftRule`, `ActiveRule`, `RetiredRule`
- **Boundary DTOs**: `RuleConfigDTO` (Pydantic or similar)
- **Translator**: `to_draft_rule(dto) -> DraftRule`
- **Services** accept only valid types:
  - evaluator evaluates `ActiveRule` only
  - orchestrator holds `list[ActiveRule]`, not mixed states

## 3. Step-by-Step Plan (Do It in Small, Safe Commits)

### Step 1 — Introduce semantic value types
- Add `domain/types.py` with `MetricName`, `Threshold`, `Window`.
- Enforce invariants in `__post_init__`.
- Add unit tests per invariant.

### Step 2 — Introduce DTO validation at the boundary
- Add `boundary/dto.py` (Pydantic).
- Validate raw config inputs there.
- Add translator `application/translate.py`.

### Step 3 — Replace dict rules with typestate dataclasses
- Add `domain/rules.py` with `DraftRule`, `ActiveRule`, `RetiredRule`.
- Implement transitions: `DraftRule.activate`, `ActiveRule.retire`.
- Update services to accept the correct state type.

### Step 4 — Remove `Optional` from the core
- Replace `Optional` returns with exceptions or a `Result`.
- Remove `list[Optional[T]]` by ensuring parsing/lookup errors are explicit.

### Step 5 — Add property-based tests with Hypothesis
Target properties:
- constructing values with invalid inputs always fails,
- activating a draft always yields an active with required fields,
- retiring an active always yields a retired,
- illegal state combinations cannot be constructed.

Keep property tests small and focused; they complement unit tests.

## 4. Concrete Test Checklist

Minimum test suite:

- **Unit tests**
  - each semantic type invariant
  - each lifecycle transition
  - boundary DTO rejects invalid shapes
  - translator DTO → domain works

- **Property tests (Hypothesis)**
  - for any valid `MetricName`, equality is stable and hash works (if frozen)
  - for any valid threshold/window, domain construction succeeds
  - for random drafts, `activate()` yields an active that can be evaluated

- **Integration test**
  - orchestrator cycle uses `list[ActiveRule]` only
  - no runtime `if state == ...` inside evaluation loop

## 5. “Done” Definition

You are done when:

- the domain layer has **no dependency** on validation libraries,
- no domain collection contains `None`,
- evaluating rules requires an `ActiveRule` by signature,
- configs are validated at the boundary and translated into domain types,
- the test suite makes it hard to reintroduce invalid states.

## Practical Guidelines

- Refactor in thin slices: introduce new types alongside old code, then migrate callers, then delete old shapes.
- Keep boundary validation separate from domain invariants (DTO vs dataclass).
- Use typestate types to reduce conditional checks in core loops.
- Use Hypothesis for invariants and transitions, not for everything.

## Exercises for Mastery

1. Implement Step 1–3 for at least one rule type end-to-end, including translator and tests.
2. Remove one `Optional` field from the rule model by splitting typestates.
3. Add at least two Hypothesis properties: one for value construction, one for lifecycle transitions.
