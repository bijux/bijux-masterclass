# Orientation — OpenAPI Contract Engineering

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Orientation question:** Is the incoming boundary exact, and can you explain why Course 1 owns the next engineering responsibility?

## Why this orientation exists

Course 1 starts from accumulated guarantees rather than an empty repository. Orientation prevents a stale handoff, an unavailable tool, or an accidental version change from contaminating the ten teaching days. The goal is not setup for its own sake; it is to make the first claim of **OpenAPI Contract Engineering** honest.

## Incoming boundary

Basic programming ability, command-line familiarity, and no assumed OpenAPI experience.

Verify that boundary before editing. Compare the predecessor bytes or entry evidence, inspect the version ledger, and identify which artifacts are historical inputs. A hard implementation problem in Course 1 must be solved at the current layer, not by rewriting an earlier contract or proof.

## Course responsibility

Define a precise, reviewable, executable HTTP API contract without confusing a description, a framework, and a running provider.

The governing question is:

> What exactly does the API promise, and how can providers and consumers verify that promise?

The current version state is:

> Public API 1.1; OpenAPI 3.1.2 executable baseline; OpenAPI 3.2.0 standards frontier; no durable database yet.

## Reader route

Use the course book in this order:

1. [Course introduction](../index.md) for the complete module arc;
2. [Capstone](../capstone.md) for the cumulative Analysis Runs Platform state;
3. [Standards](../standards.md) for normative and course-profile boundaries;
4. [Evidence model](../evidence-model.md) for authoritative versus diagnostic proof;
5. [Language strategy](../language-strategy.md) before opening implementation code.
6. Re-read the list through this course’s lens: **Specify the public promise**.

The chapter teaches the model. Exercises force transfer. Worked answers expose reasoning. The lab attacks one mechanism. The checkpoint decides whether the result is strong enough to carry into the next module.

## Implementation route

The course strategy is **symmetric Python/TypeScript providers**. Record the selected route and the reason it supports your learning goal. Do not switch runtimes in the middle of a failed mechanism; first determine whether the model, the implementation, or the environment is wrong.

## Evidence boundary

List the proof routes available on your machine and classify them as deterministic, local process, live persistence/network, documentation, or independent-tool evidence. The first stronger environment-backed claim is **provider conformance over real HTTP**. Until that route actually runs, use narrower wording and record it as `not-executed`.

## Readiness test

You are ready for [HTTP and OpenAPI Foundations](../module-01-http-openapi-foundations/index.md) when you can explain, without repository jargon:

1. what the predecessor already settled;
2. what Course 1 is allowed to change;
3. which versions and profiles are independent axes;
4. which implementation route you selected;
5. which evidence classes are available;
6. what the outgoing handoff must prove: A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflow description, compatibility policy, and provider-neutral behavioral scenarios.
