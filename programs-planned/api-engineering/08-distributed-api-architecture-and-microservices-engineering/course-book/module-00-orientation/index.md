# Orientation — Distributed API Architecture and Microservices Engineering

> **Program stage:** Course 8 of 10 — Distribute ownership deliberately.

> **Orientation question:** Is the incoming boundary exact, and can you explain why Course 8 owns the next engineering responsibility?

## Why this orientation exists

Course 8 starts from accumulated guarantees rather than an empty repository. Orientation prevents a stale handoff, an unavailable tool, or an accidental version change from contaminating the ten teaching days. The goal is not setup for its own sake; it is to make the first claim of **Distributed API Architecture and Microservices Engineering** honest.

## Incoming boundary

The Course 7 platform with governed HTTP, event, and RPC interfaces and migration history through 015.

Verify that boundary before editing. Compare the predecessor bytes or entry evidence, inspect the version ledger, and identify which artifacts are historical inputs. A hard implementation problem in Course 8 must be solved at the current layer, not by rewriting an earlier contract or proof.

## Course responsibility

Use ownership and failure evidence to approve, reject, extract, operate, and reverse service boundaries without creating a distributed monolith.

The governing question is:

> When does a remote service boundary create more value than the coordination, latency, consistency, security, release, and operational costs it introduces?

The current version state is:

> HTTP API 1.2, Events API 1.0, and RPC API 1.0 preserved; distributed architecture profile 1.0 introduced; owner-local migration histories begin.

## Reader route

Use the course book in this order:

1. [Course introduction](../index.md) for the complete module arc;
2. [Capstone](../capstone.md) for the cumulative Analysis Runs Platform state;
3. [Standards](../standards.md) for normative and course-profile boundaries;
4. [Evidence model](../evidence-model.md) for authoritative versus diagnostic proof;
5. [Language strategy](../language-strategy.md) before opening implementation code.
6. Re-read the list through this course’s lens: **Distribute ownership deliberately**.

The chapter teaches the model. Exercises force transfer. Worked answers expose reasoning. The lab attacks one mechanism. The checkpoint decides whether the result is strong enough to carry into the next module.

## Implementation route

The course strategy is **one primary implementation track plus one comparative reference track**. Record the selected route and the reason it supports your learning goal. Do not switch runtimes in the middle of a failed mechanism; first determine whether the model, the implementation, or the environment is wrong.

## Evidence boundary

List the proof routes available on your machine and classify them as deterministic, local process, live persistence/network, documentation, or independent-tool evidence. The first stronger environment-backed claim is **multi-process service topology with version skew**. Until that route actually runs, use narrower wording and record it as `not-executed`.

## Readiness test

You are ready for [Distribution Economics, Boundary Evidence, and Architecture Fitness Functions](../module-01-distribution-economics-and-boundary-evidence/index.md) when you can explain, without repository jargon:

1. what the predecessor already settled;
2. what Course 8 is allowed to change;
3. which versions and profiles are independent axes;
4. which implementation route you selected;
5. which evidence classes are available;
6. what the outgoing handoff must prove: Distributed Architecture Profile 1.0, explicit service and data ownership, versioned projections, saga and trust policies, independent release choreography, extraction evidence, and a GraphQL boundary brief.
