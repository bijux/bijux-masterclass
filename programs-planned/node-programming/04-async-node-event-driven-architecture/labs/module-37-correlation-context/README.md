# Correlation Context

## Product

Build a small AsyncLocalStorage-based correlation layer and an optional diagnostics surface. The layer carries run and task identifiers across asynchronous suspension without becoming domain or authorization authority.

Read [Module 37](../../course-book/module-37-async-context-correlation-and-diagnostic-boundaries/index.md).

## Public contract

Expose immutable `CorrelationContext`, `current()`, `run(context, operation)`, and `child(taskId, operation)`. Publish start, end, and error diagnostics on one stable channel. The package must work correctly with zero subscribers.

## Invariants

Concurrent contexts never overwrite each other. Nested child scope restores the parent. The store contains small immutable identifiers only. Operation failure is rethrown with identity preserved. Diagnostic publication cannot change the operation’s terminal result. Subscriber ownership and unsubscription are explicit.

## Required evidence

Use deferred promises to resume two runs in the opposite order from creation. Test nested restoration, missing-parent child failure, error publication, zero-subscriber behavior, subscription removal, and no context after run completion. Add a design analysis of how a leaked timer would retain its context.

## Prohibited design

Do not read authentication or tenant authority from ambient context. Do not create a channel per request. Do not install process-global subscribers inside this reusable package. Do not store request bodies, mutable domain objects, or secrets.

## Isolation and optional-observer evidence

Start at least fifty interleaved logical operations, each with a distinct correlation ID, and verify that nested promise, timer, and event callbacks retain the correct immutable store. Add a deliberately mutable-store counterexample to the design record but not the final implementation.

Publish bounded messages through `diagnostics_channel`. Prove that zero subscribers, one subscriber, subscriber removal, and concurrent contexts do not change domain outcomes. Document why authorization values remain explicit arguments.

## Bounded context schema

Define the maximum size and allowed fields of the context store. Tests should reject or normalize unbounded labels. Explain which diagnostics use ambient lookup and which domain operations require explicit arguments.

## Retention measurement

Use `WeakRef` only as an exploratory diagnostic, not a deterministic test oracle. The required evidence is architectural: the final context schema excludes large domain values, and all owned callbacks are disposed at lifecycle completion.

## Independent transfer

Integrate the context layer into a command library that can be called from a CLI or server. Define behavior when no host context exists and show that explicit command authorization remains independent of diagnostics.

## Implementation stages

Implement immutable run scope first, then nested child derivation, then optional diagnostics. Add interleaving tests before adding convenience methods. Keep the diagnostics wrapper compatible with the selected Node ambient types without exposing untyped messages publicly.

## Review questions

Can any caller mutate the store? Which resources create propagation boundaries? What fields are safe to retain? Which fields become dangerous metric labels? What happens when a diagnostics subscriber throws?

## Completion evidence

Submit concurrent-isolation traces, nested restoration tests, subscriber disposal, and a field-classification table. Include one explicit statement that context is not authorization or domain state.
