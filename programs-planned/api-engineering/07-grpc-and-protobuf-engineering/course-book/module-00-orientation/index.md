# Orientation — gRPC and Protobuf Engineering

> **Program stage:** Course 7 of 10 — Engineer typed internal invocation and streaming.

> **Orientation question:** Is the incoming boundary exact, and can you explain why Course 7 owns the next engineering responsibility?

## Why this orientation exists

Course 7 starts from accumulated guarantees rather than an empty repository. Orientation prevents a stale handoff, an unavailable tool, or an accidental version change from contaminating the ten teaching days. The goal is not setup for its own sake; it is to make the first claim of **gRPC and Protobuf Engineering** honest.

## Incoming boundary

The Course 6 HTTP API 1.2 and Analysis Events API 1.0 handoff with profiles and migrations through 012.

Verify that boundary before editing. Compare the predecessor bytes or entry evidence, inspect the version ledger, and identify which artifacts are historical inputs. A hard implementation problem in Course 7 must be solved at the current layer, not by rewriting an earlier contract or proof.

## Course responsibility

Design and verify Protobuf schemas and gRPC interactions without pretending that generated stubs turn remote calls into local functions.

The governing question is:

> How should typed internal capabilities be modeled and operated when remote calls can fail ambiguously, stream for long periods, and evolve across language boundaries?

The current version state is:

> HTTP API 1.2 and Events API 1.0 preserved; RPC API 1.0 introduced; proto3 baseline; Edition 2024 frontier; migrations 001–015.

## Reader route

Use the course book in this order:

1. [Course introduction](../index.md) for the complete module arc;
2. [Capstone](../capstone.md) for the cumulative Analysis Runs Platform state;
3. [Standards](../standards.md) for normative and course-profile boundaries;
4. [Evidence model](../evidence-model.md) for authoritative versus diagnostic proof;
5. [Language strategy](../language-strategy.md) before opening implementation code.
6. Re-read the list through this course’s lens: **Engineer typed internal invocation and streaming**.

The chapter teaches the model. Exercises force transfer. Worked answers expose reasoning. The lab attacks one mechanism. The checkpoint decides whether the result is strong enough to carry into the next module.

## Implementation route

The course strategy is **one primary implementation track plus one comparative reference track**. Record the selected route and the reason it supports your learning goal. Do not switch runtimes in the middle of a failed mechanism; first determine whether the model, the implementation, or the environment is wrong.

## Evidence boundary

List the proof routes available on your machine and classify them as deterministic, local process, live persistence/network, documentation, or independent-tool evidence. The first stronger environment-backed claim is **networked gRPC with generated descriptors**. Until that route actually runs, use narrower wording and record it as `not-executed`.

## Readiness test

You are ready for [RPC Boundaries, Service Ownership, and Interaction Choice](../module-01-rpc-boundaries-and-service-ownership/index.md) when you can explain, without repository jargon:

1. what the predecessor already settled;
2. what Course 7 is allowed to change;
3. which versions and profiles are independent axes;
4. which implementation route you selected;
5. which evidence classes are available;
6. what the outgoing handoff must prove: Analysis RPC API 1.0, gRPC Profile 1.0, proto3 executable baseline, Edition 2024 frontier, migrations 013–015, streaming protocols, method policy, and compatibility evidence.
