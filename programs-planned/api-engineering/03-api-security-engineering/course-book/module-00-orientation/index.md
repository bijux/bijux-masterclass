# Orientation — API Security Engineering

> **Program stage:** Course 3 of 10 — Defend the promise.

> **Orientation question:** Is the incoming boundary exact, and can you explain why Course 3 owns the next engineering responsibility?

## Why this orientation exists

Course 3 starts from accumulated guarantees rather than an empty repository. Orientation prevents a stale handoff, an unavailable tool, or an accidental version change from contaminating the ten teaching days. The goal is not setup for its own sake; it is to make the first claim of **API Security Engineering** honest.

## Incoming boundary

The Course 2 API 1.2 durable-service handoff and migrations 001–005.

Verify that boundary before editing. Compare the predecessor bytes or entry evidence, inspect the version ledger, and identify which artifacts are historical inputs. A hard implementation problem in Course 3 must be solved at the current layer, not by rewriting an earlier contract or proof.

## Course responsibility

Derive, implement, and adversarially verify security properties around the durable service without replacing engineering judgment with middleware or scanner output.

The governing question is:

> How does the API remain trustworthy when callers, credentials, inputs, destinations, dependencies, and networks cannot be trusted by default?

The current version state is:

> API 1.2 preserved; Security Profile 1.0 introduced; migrations 001–007.

## Reader route

Use the course book in this order:

1. [Course introduction](../index.md) for the complete module arc;
2. [Capstone](../capstone.md) for the cumulative Analysis Runs Platform state;
3. [Standards](../standards.md) for normative and course-profile boundaries;
4. [Evidence model](../evidence-model.md) for authoritative versus diagnostic proof;
5. [Language strategy](../language-strategy.md) before opening implementation code.
6. Re-read the list through this course’s lens: **Defend the promise**.

The chapter teaches the model. Exercises force transfer. Worked answers expose reasoning. The lab attacks one mechanism. The checkpoint decides whether the result is strong enough to carry into the next module.

## Implementation route

The course strategy is **one primary implementation track plus one comparative reference track**. Record the selected route and the reason it supports your learning goal. Do not switch runtimes in the middle of a failed mechanism; first determine whether the model, the implementation, or the environment is wrong.

## Evidence boundary

List the proof routes available on your machine and classify them as deterministic, local process, live persistence/network, documentation, or independent-tool evidence. The first stronger environment-backed claim is **an operated identity and network boundary**. Until that route actually runs, use narrower wording and record it as `not-executed`.

## Readiness test

You are ready for [Threat Modeling and Security Requirements](../module-01-threat-modeling/index.md) when you can explain, without repository jargon:

1. what the predecessor already settled;
2. what Course 3 is allowed to change;
3. which versions and profiles are independent axes;
4. which implementation route you selected;
5. which evidence classes are available;
6. what the outgoing handoff must prove: Security Profile 1.0, migrations 006–007, a threat-to-requirement security case, identity and authorization policy, hostile-input vectors, SSRF and webhook protections, abuse controls, and incident evidence.
