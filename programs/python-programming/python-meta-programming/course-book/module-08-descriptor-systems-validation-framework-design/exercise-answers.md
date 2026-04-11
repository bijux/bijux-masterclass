# Exercise Answers

Use this page after attempting the exercises yourself. The point is not to match every
example literally. The point is to compare your reasoning against answers that keep
descriptor-system power, cache policy, backend ownership, and framework boundaries honest.

## Answer 1: Design one cached field honestly

Example answer:

A cached `word_count` field might:

- compute on first read
- store its cached value in `obj.__dict__["_word_count_cached"]`
- expose an `invalidate(obj)` method whenever `text` changes

Good conclusion:

The cache design is not complete until the invalidation story is explicit. “It caches the
value” is not enough by itself.

## Answer 2: Review one external-storage field

Example answer:

A field backed by a memory store or database might use a key such as:

- `field:Post:12:title`

and:

- read through the backend on cache miss
- write through on assignment and refresh the local cache

Good conclusion:

Attribute access now hides storage I/O and serialization work, so the design needs clear
documentation or observability rather than pretending the field is purely local.

## Answer 3: Compose one wrapper field

Example answer:

- the inner field owns storage and ordinary set/get behavior
- the wrapper field adds validation before delegating to the inner descriptor

Good conclusion:

Composition works well when each layer owns one extra concern and forwarding of
`__set_name__`, `__get__`, and `__set__` stays consistent.

## Answer 4: Validate one narrow hint subset

Example answer:

Support:

- plain runtime classes such as `int` and `str`
- `Union` or `Optional`
- selected `Annotated[...]` validators

Refuse:

- parameterized generics such as `list[int]`

Good conclusion:

This is an honest hint-driven field because it names its supported surface clearly and
does not claim to understand every typing construct.

## Answer 5: Reject one descriptor that became architecture

Example answer:

Suppose one “smart field” tries to own:

- lazy loading
- cache invalidation across related records
- object identity management
- transaction coordination

Better owners:

- explicit session or unit-of-work objects
- model-layer coordination services
- broader framework infrastructure

Good conclusion:

Once multiple records or lifecycle phases must be coordinated, the descriptor is no longer
the whole owner. The design has crossed into framework architecture.

## Answer 6: Review the educational mini relational model

Example answer:

Field layer ownership:

- validating and storing one field value
- reading one field through a backend-backed descriptor

Framework or model layer ownership:

- model registration
- record reconstruction
- relationship orchestration

Good conclusion:

The mini relational model is educational because it exposes the mechanism clearly but
omits the infrastructure a real ORM would need, such as transactions, identity maps, and
query planning.

## What strong Module 08 answers have in common

Across the whole set, strong answers share the same habits:

- they treat invalidation as part of descriptor behavior
- they make the backend or source of truth explicit
- they keep composed fields shallow and readable
- they name the exact hint subset a field understands
- they say when a field system has become broader architecture

If an answer still sounds like "framework behavior can live in the descriptor somehow,"
revise it until you can say exactly what the descriptor owns and what should move out of
it.
