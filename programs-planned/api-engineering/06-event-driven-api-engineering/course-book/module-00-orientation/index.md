# Orientation — Event-Driven API Engineering

> **Program stage:** Course 6 of 10 — Extend the promise across asynchronous time.

> **Orientation question:** Is the incoming boundary exact, and can you explain why Course 6 owns the next engineering responsibility?

## Why this orientation exists

Course 6 starts from accumulated guarantees rather than an empty repository. Orientation prevents a stale handoff, an unavailable tool, or an accidental version change from contaminating the ten teaching days. The goal is not setup for its own sake; it is to make the first claim of **Event-Driven API Engineering** honest.

## Incoming boundary

The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.

Verify that boundary before editing. Compare the predecessor bytes or entry evidence, inspect the version ledger, and identify which artifacts are historical inputs. A hard implementation problem in Course 6 must be solved at the current layer, not by rewriting an earlier contract or proof.

## Course responsibility

Design, evolve, secure, operate, and verify asynchronous message contracts under delay, duplication, reordering, replay, and consumer failure.

The governing question is:

> How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth?

The current version state is:

> HTTP API 1.2 preserved; Analysis Events API 1.0 introduced; AsyncAPI 3.1.0; CloudEvents 1.0-compatible profile; migrations 001–012.

## Reader route

Use the course book in this order:

1. [Course introduction](../index.md) for the complete module arc;
2. [Capstone](../capstone.md) for the cumulative Analysis Runs Platform state;
3. [Standards](../standards.md) for normative and course-profile boundaries;
4. [Evidence model](../evidence-model.md) for authoritative versus diagnostic proof;
5. [Language strategy](../language-strategy.md) before opening implementation code.
6. Re-read the list through this course’s lens: **Extend the promise across asynchronous time**.

The chapter teaches the model. Exercises force transfer. Worked answers expose reasoning. The lab attacks one mechanism. The checkpoint decides whether the result is strong enough to carry into the next module.

## Implementation route

The course strategy is **one primary implementation track plus one comparative reference track**. Record the selected route and the reason it supports your learning goal. Do not switch runtimes in the middle of a failed mechanism; first determine whether the model, the implementation, or the environment is wrong.

## Evidence boundary

List the proof routes available on your machine and classify them as deterministic, local process, live persistence/network, documentation, or independent-tool evidence. The first stronger environment-backed claim is **durable broker redelivery and replay**. Until that route actually runs, use narrower wording and record it as `not-executed`.

## Readiness test

You are ready for [Event Thinking, Ownership, and Message Taxonomy](../module-01-event-thinking-and-ownership/index.md) when you can explain, without repository jargon:

1. what the predecessor already settled;
2. what Course 6 is allowed to change;
3. which versions and profiles are independent axes;
4. which implementation route you selected;
5. which evidence classes are available;
6. what the outgoing handoff must prove: Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.
