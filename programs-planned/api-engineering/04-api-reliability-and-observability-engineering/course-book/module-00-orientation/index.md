# Orientation — API Reliability and Observability Engineering

> **Program stage:** Course 4 of 10 — Observe, diagnose, contain, and recover the promise.

> **Orientation question:** Is the incoming boundary exact, and can you explain why Course 4 owns the next engineering responsibility?

## Why this orientation exists

Course 4 starts from accumulated guarantees rather than an empty repository. Orientation prevents a stale handoff, an unavailable tool, or an accidental version change from contaminating the ten teaching days. The goal is not setup for its own sake; it is to make the first claim of **API Reliability and Observability Engineering** honest.

## Incoming boundary

The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

Verify that boundary before editing. Compare the predecessor bytes or entry evidence, inspect the version ledger, and identify which artifacts are historical inputs. A hard implementation problem in Course 4 must be solved at the current layer, not by rewriting an earlier contract or proof.

## Course responsibility

Make failures observable and recoverable through explicit budgets, lifecycle states, telemetry meaning, service-level objectives, fault experiments, and reconciliation.

The governing question is:

> How do operators know whether the user promise is still true, and how do they recover it without making the incident worse?

The current version state is:

> API 1.2 and Security Profile 1.0 preserved; Reliability Profile 1.0 introduced; migrations 001–008.

## Reader route

Use the course book in this order:

1. [Course introduction](../index.md) for the complete module arc;
2. [Capstone](../capstone.md) for the cumulative Analysis Runs Platform state;
3. [Standards](../standards.md) for normative and course-profile boundaries;
4. [Evidence model](../evidence-model.md) for authoritative versus diagnostic proof;
5. [Language strategy](../language-strategy.md) before opening implementation code.
6. Re-read the list through this course’s lens: **Observe, diagnose, contain, and recover the promise**.

The chapter teaches the model. Exercises force transfer. Worked answers expose reasoning. The lab attacks one mechanism. The checkpoint decides whether the result is strong enough to carry into the next module.

## Implementation route

The course strategy is **one primary implementation track plus one comparative reference track**. Record the selected route and the reason it supports your learning goal. Do not switch runtimes in the middle of a failed mechanism; first determine whether the model, the implementation, or the environment is wrong.

## Evidence boundary

List the proof routes available on your machine and classify them as deterministic, local process, live persistence/network, documentation, or independent-tool evidence. The first stronger environment-backed claim is **a multiprocess failure-and-telemetry experiment**. Until that route actually runs, use narrower wording and record it as `not-executed`.

## Readiness test

You are ready for [Reliability Model and Critical Journeys](../module-01-reliability-model-and-critical-journeys/index.md) when you can explain, without repository jargon:

1. what the predecessor already settled;
2. what Course 4 is allowed to change;
3. which versions and profiles are independent axes;
4. which implementation route you selected;
5. which evidence classes are available;
6. what the outgoing handoff must prove: Reliability Profile 1.0, migration 008, critical journeys, deadline and resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans.
