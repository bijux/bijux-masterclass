# Orientation — Contract-Driven API Service Engineering

> **Program stage:** Course 2 of 10 — Implement the promise durably.

> **Orientation question:** Is the incoming boundary exact, and can you explain why Course 2 owns the next engineering responsibility?

## Why this orientation exists

Course 2 starts from accumulated guarantees rather than an empty repository. Orientation prevents a stale handoff, an unavailable tool, or an accidental version change from contaminating the ten teaching days. The goal is not setup for its own sake; it is to make the first claim of **Contract-Driven API Service Engineering** honest.

## Incoming boundary

The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.

Verify that boundary before editing. Compare the predecessor bytes or entry evidence, inspect the version ledger, and identify which artifacts are historical inputs. A hard implementation problem in Course 2 must be solved at the current layer, not by rewriting an earlier contract or proof.

## Course responsibility

Turn the fixed Course 1 contract into a durable modular service whose important guarantees survive concurrent requests and process failure.

The governing question is:

> Which application, database, worker, storage, and release mechanisms keep the public contract true under concurrency, restart, and partial failure?

The current version state is:

> API 1.1 preserved; additive API 1.2 introduced; OpenAPI 3.1.2 preserved; migrations 001–005.

## Reader route

Use the course book in this order:

1. [Course introduction](../index.md) for the complete module arc;
2. [Capstone](../capstone.md) for the cumulative Analysis Runs Platform state;
3. [Standards](../standards.md) for normative and course-profile boundaries;
4. [Evidence model](../evidence-model.md) for authoritative versus diagnostic proof;
5. [Language strategy](../language-strategy.md) before opening implementation code.
6. Re-read the list through this course’s lens: **Implement the promise durably**.

The chapter teaches the model. Exercises force transfer. Worked answers expose reasoning. The lab attacks one mechanism. The checkpoint decides whether the result is strong enough to carry into the next module.

## Implementation route

The course strategy is **one primary implementation track plus one comparative reference track**. Record the selected route and the reason it supports your learning goal. Do not switch runtimes in the middle of a failed mechanism; first determine whether the model, the implementation, or the environment is wrong.

## Evidence boundary

List the proof routes available on your machine and classify them as deterministic, local process, live persistence/network, documentation, or independent-tool evidence. The first stronger environment-backed claim is **concurrent PostgreSQL behavior**. Until that route actually runs, use narrower wording and record it as `not-executed`.

## Readiness test

You are ready for [Application Use Cases and Boundaries](../module-01-application-use-cases/index.md) when you can explain, without repository jargon:

1. what the predecessor already settled;
2. what Course 2 is allowed to change;
3. which versions and profiles are independent axes;
4. which implementation route you selected;
5. which evidence classes are available;
6. what the outgoing handoff must prove: A durable API 1.2 service with migrations 001–005, persistent idempotency, atomic conditional updates, stable pagination, worker recovery, artifact integrity, transactional webhook delivery, and compatible-release evidence.
