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
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page is one concept inside its parent
module, not a detached essay, and the capstone is the pressure test for whether the
idea holds. Read the second diagram as the working rhythm for the page: name the
problem, study the example, identify the boundary, then carry one review question
forward.

## Why this lesson matters

Shared mutable state is one of the fastest ways to make a clean object model dishonest.

The issue is not that threads exist. The issue is that multiple actors may try to mutate
the same state without one owned policy for:

- who may mutate
- when mutation is serialized
- which invariants must hold across a whole update

If that policy is missing, "thread safe" becomes a hopeful adjective rather than a real
contract.

## Shared mutation is a design choice

Students should not assume that shared mutable access is the normal starting point.

A mutable object under concurrent use needs one clear policy, such as:

- one owner thread mutates it
- callers hand work to a queue instead of touching it directly
- internal locking protects whole invariant-preserving operations
- immutable snapshots are replaced rather than edited in place

The important lesson is that concurrency safety starts with choosing a state ownership
model, not with sprinkling locks afterward.

## Locks protect meaning, not assignments

Weak locking often protects one line at a time:

- assign field A
- release lock
- assign field B later

That can still violate an invariant if the real meaning spans both fields together.

Lock boundaries should usually wrap the full operation that preserves the invariant, not
only isolated assignments.

That is why concurrency belongs in an object-design course: the object's meaning tells
you where the safe mutation boundary is.

## Ownership transfer is often simpler than sharing

The cleanest concurrency design is frequently:

- one owner mutates
- everyone else submits requests or receives snapshots

Queues, worker ownership, and immutable replacement often create simpler reasoning than
letting many threads mutate one object directly.

Students should learn that "use a lock" is not always the best first answer. Sometimes
the better answer is "stop sharing the mutation surface."

## Thread semantics are part of the contract

Callers need to know whether an object is:

- single-threaded only
- safe for concurrent reads only
- internally synchronized for certain operations
- safe only when used through a coordinator

If this is undocumented or implicit, users of the object may accidentally violate the
design and think the bug is random.

## Common mistakes

- assuming the GIL is the same thing as design-level thread safety
- locking individual fields instead of invariant-preserving operations
- letting multiple threads mutate one aggregate because it was convenient
- documenting nothing and expecting callers to guess the thread contract
- using locks when ownership transfer would have produced a clearer model

These mistakes all blur who truly owns state mutation.

## Review checklist

| Question | Good sign |
| --- | --- |
| is there a clear ownership policy for mutable state? | yes |
| do lock boundaries protect whole invariant-preserving updates? | yes |
| could ownership transfer simplify the design more than extra locking? | yes |
| is the thread-safety contract visible to callers? | yes |

## Capstone connection

Use the capstone runtime to ask:

- which mutable state should have one owner?
- where would a queue or worker boundary be clearer than a shared lock?
- which invariants would fail if updates were interleaved halfway through?

Those are the real design questions before adding more concurrency primitives.

## Exit check

Leave this lesson only when you can do all of these:

- explain why owned mutation is often more important than incidental thread safety
- identify one place where a lock must protect a full invariant, not only one assignment
- point to one capstone state surface that should probably be owned by one coordinator rather than many threads
