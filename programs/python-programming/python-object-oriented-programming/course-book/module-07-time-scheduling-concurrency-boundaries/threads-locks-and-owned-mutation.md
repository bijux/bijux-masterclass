# Threads, Locks, and Owned Mutation

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Time Scheduling Concurrency Boundaries"]
  page["Threads, Locks, and Owned Mutation"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  state["name the mutable state"] --> owner["choose who owns mutation"]
  owner --> scope["decide whether a lock protects a whole invariant"]
  scope --> handoff["compare locking with ownership transfer"]
  handoff --> contract["state the caller-visible concurrency contract"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page is the central concurrency-design
lesson in Module 07. Read the second diagram as the reasoning route: start by naming the
state surface, decide who owns mutation, then choose locks or handoff based on invariant
protection instead of habit.

## Why this lesson matters

Shared mutable state is one of the fastest ways to make a clean object model dishonest.

The problem is not that threads exist. The problem is that several actors may try to
change the same state without one explicit policy for:

- who is allowed to mutate
- how whole invariant-preserving updates are serialized
- what callers may assume about concurrent use

If that policy is missing, "thread-safe" becomes an optimistic adjective instead of a
reviewable contract.

## Shared mutation is a design choice, not the default

Students often meet concurrency after they already have mutable objects and start from
the assumption that the state will stay shared while locks are added later.

That is backwards.

A mutable object under concurrent use needs one explicit policy such as:

- one owner thread mutates it
- callers hand work to a queue instead of touching it directly
- immutable snapshots are replaced instead of edited in place
- internal locking protects whole invariant-preserving operations

The important lesson is that concurrency safety starts by choosing an ownership model,
not by sprinkling synchronization on top of accidental sharing.

## Worked question: what is the actual state surface?

Before discussing locks, name the mutable surface precisely.

For reminder delivery, it might be:

- reminder sent-state
- attempt count
- dedupe marker
- last scheduled deadline

That level of detail matters because a "thread-safe reminder object" is too vague to
review. Different fields may participate in one invariant together, and the design has
to acknowledge that explicitly.

## Locks should protect meaning, not isolated assignments

Weak locking often protects one field at a time:

1. assign field A
2. release lock
3. assign field B later

That may still violate the real invariant if meaning spans both fields together.

Stronger locking protects the whole update that preserves the invariant, such as:

- check reminder has not been sent
- mark dedupe token
- record send completion state

The lesson is not "always use bigger locks." The lesson is "draw lock scope around the
meaningful operation, not around convenient lines of code."

## Ownership transfer is often simpler than shared mutation

The cleanest concurrency design is frequently:

- one owner mutates
- everyone else submits requests or receives snapshots

Queues, worker ownership, and immutable replacement often produce simpler reasoning than
letting many threads mutate one object directly.

Students should hear this plainly:

> "Use a lock" is not always the first good answer. Often the first good answer is
> "stop sharing the mutation surface."

That sentence prevents a great deal of accidental complexity.

## Compare two designs before choosing

For one mutable state surface, compare:

| Design | What it buys | What it risks |
| --- | --- | --- |
| shared object plus lock | local coordination around one object | blurry ownership, wider critical sections, harder retry reasoning |
| queue or owner handoff | explicit mutation ownership and clearer retry path | more coordination infrastructure and work routing |

This comparison is what many concurrency lessons skip. Without it, learners may think
locking is the normal path and ownership transfer is an exotic optimization, when the
opposite is often true.

## The concurrency contract must be visible to callers

Callers need to know whether an object is:

- single-threaded only
- safe for concurrent reads only
- internally synchronized for certain whole operations
- safe only when used through a coordinator or queue boundary

If none of that is documented or tested, users of the object will guess. Concurrency
bugs then look random even when the real issue is that the contract was never stated.

## Review drill: ask these four questions

For any concurrent mutable surface, ask:

1. who owns mutation?
2. what invariant spans more than one field or step?
3. would owned handoff be simpler than shared locking?
4. what may callers assume under concurrent use?

If any answer is fuzzy, the design is not ready for the label "thread-safe."

## Common mistakes

- assuming the GIL provides design-level thread safety
- locking assignments instead of invariant-preserving operations
- letting several threads mutate one aggregate because it was convenient
- documenting nothing and expecting callers to infer the concurrency contract
- reaching for locks before asking whether mutation should be shared at all

All of these mistakes blur the same thing: who truly owns the state transition.

## Capstone connection

Use the capstone runtime to ask:

- which mutable state surface should have one owner?
- where would a queue or coordinator boundary be clearer than a shared lock?
- which invariant would fail if two updates interleaved halfway through?
- what does the caller currently think "safe to call concurrently" means?

Those questions turn concurrency into an object-design review instead of a primitive
catalog.

## Exit check

Leave this lesson only when you can do all of these:

- explain why owned mutation is often more important than incidental thread safety
- identify one place where a lock must protect a whole invariant rather than one
  assignment
- point to one state surface that should probably be owned by one coordinator or worker
  instead of many threads
