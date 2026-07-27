# Cached Descriptors and Invalidation


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Descriptor Systems Validation Framework Design"]
  page["Cached Descriptors and Invalidation"]
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

Module 08 begins with the first way descriptor systems usually grow beyond simple field
validation:

they stop returning raw stored values and start managing time.

Lazy computation, cached results, and invalidation all live there.

This page matters because caching can make a field look simpler while making its truth
conditions harder to see. A reader studying alone needs a way to ask not only "is it
cached?" but also "when does this cached value stop being trustworthy?"

## The sentence to keep

A cached descriptor is not only a descriptor that remembers a value. It is a descriptor
that must define when the value is computed, where it is stored, and how it becomes
invalid.

That is the real design surface.

Keep one more sentence beside it:

> freshness is part of the field contract, not an afterthought the caller is supposed to guess.

If you are studying alone, turn that sentence into a written check every time you see
cached access:

- what dependency can make the value stale?
- what exact code path clears the old value?
- what wrong answer would a caller get if invalidation never happened?

## Three related patterns

Keep these three patterns separate:

- pure computed access recalculates on every read
- lazy access computes on first read and may or may not retain the result
- cached access stores a result and reuses it until something invalidates it

People often blur these together, but they create different review questions.

Use this table when the language around caching starts to blur:

| Pattern | Review question |
| --- | --- |
| pure computed access | what cost do we pay every read? |
| lazy access | when does computation happen, and is the result retained? |
| cached access | what makes the retained result stale, and how is that state cleared? |

## A pure computed descriptor

```python
class ComputedField:
    def __init__(self, compute):
        self.compute = compute

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return self.compute(obj)
```

This is simple because it does not promise reuse or freshness beyond the current read.

## A cached descriptor with explicit storage

```python
class CachedField:
    def __init__(self, compute):
        self.compute = compute

    def __set_name__(self, owner, name):
        self.cache_name = f"_{name}_cached"

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        if self.cache_name not in obj.__dict__:
            obj.__dict__[self.cache_name] = self.compute(obj)
        return obj.__dict__[self.cache_name]

    def invalidate(self, obj):
        obj.__dict__.pop(self.cache_name, None)
```

This is already a stronger design because the cache policy is visible:

- one per-instance cache slot
- first-read computation
- explicit invalidation hook

It is also a stronger teaching shape because the invalidation surface is not hidden in a
wider object method or some undocumented side effect.

## Why invalidation is part of the field contract

Suppose a cached descriptor computes `word_count` from `text`.

If `text` changes but `word_count` stays cached, the descriptor has become stale.

That means the real contract is not just:

- how do we cache?

It is also:

- what changes make the cached value outdated?
- who is responsible for clearing it?

If those answers are missing, the cache design is incomplete.

## Evidence route for cache reviews

Use this route whenever a cached field sounds more reliable than its code warrants:

| Evidence step | What it proves |
| --- | --- |
| find the compute function | tells you what the cached value depends on |
| find the cache storage slot | tells you where stale state can persist |
| inspect the invalidation API or trigger | tells you whether freshness has an owner |
| mutate a dependency and re-read | shows whether the design goes stale quietly or refreshes honestly |

## A dependency example

```python
class Post:
    def __init__(self, text):
        self.text = text

    word_count = CachedField(lambda obj: len(obj.text.split()))


post = Post("hello world")
print(post.word_count)  # 2
post.text = "hello careful world"
Post.word_count.invalidate(post)
print(post.word_count)  # 3
```

This is a small example, but it keeps the right instinct visible:

dependencies matter just as much as the cache itself.

That is the review sentence to keep. A cached field without named dependencies is already
trying to hide a design risk.

## Where cached values should live

For most course-level cached descriptors, the safest owner is still the instance:

```python
obj.__dict__[cache_name]
```

That keeps cached state:

- per instance
- easy to inspect during debugging
- separate from the shared descriptor object

The same storage rule from Module 07 still applies.

Use this storage table when the owner story is unclear:

| Storage choice | Why it helps or hurts |
| --- | --- |
| `obj.__dict__[cache_name]` | keeps cached state per instance and easy to inspect |
| hidden storage on the descriptor object | risks shared or misleading state |
| backend-wide shared cache hidden behind the field | may already be wider infrastructure, not one field concern |

## A dependency ledger you should keep

Many weak cache designs fail because the dependency set stays implied instead of written
down. Keep a ledger like this while you review:

| Cached field | Depends on | Where cached state lives | Invalidation owner | Stale-read symptom |
| --- | --- | --- | --- | --- |
| `word_count` | `text` | `obj.__dict__["_word_count_cached"]` | explicit `invalidate(obj)` or `text` setter | reports old count after text change |
| your own field | fill this in | fill this in | fill this in | fill this in |

If you cannot fill every column, the cache story is still incomplete.

## Why hidden freshness assumptions are dangerous

Caching often makes code look faster and cleaner while quietly making it less truthful.

Common failure modes are:

- input changes that do not invalidate cached outputs
- external dependencies changing behind the cache
- no clear distinction between cached data and current data

This is why cache review is really state review.

## Common overclaims to reject

Reject these descriptions when they appear in review:

| Overclaim | Better replacement |
| --- | --- |
| "the descriptor keeps it fast" | "the descriptor reuses a cached value until its invalidation rule says otherwise" |
| "lazy and cached mean basically the same thing" | "lazy controls compute timing; cached adds reuse and therefore freshness risk" |
| "the cache will refresh when needed" | "the refresh trigger must be named explicitly" |
| "stale data is unlikely" | "staleness is a field-design concern that needs an owner" |

## Weak answers to reject early

These answers sound practical but weaken review discipline:

| Weak answer | Why it fails |
| --- | --- |
| "the value is recomputed eventually" | eventually is not an invalidation owner |
| "the setter probably clears the cache somewhere" | probably means the dependency path is still unproven |
| "this field is safe because it is only local state" | local state can still go stale when derived inputs change |
| "callers know they should refresh it" | the field contract has been pushed onto memory and habit |

## Failure modes for cached descriptors

These are the mistakes this page is trying to prevent:

| Failure mode | Why it weakens the design | Repair move |
| --- | --- | --- |
| caching without a named invalidation rule | stale values become hidden behavior | add explicit invalidation ownership |
| computing from mutable dependencies without refresh logic | correctness drifts after updates | tie invalidation to dependency changes |
| storing cached state in a confusing shared place | inspection and isolation get worse | keep cache state per instance unless wider infrastructure is explicit |
| treating field-level caching as distributed or cross-instance coherence | the field claims too much infrastructure power | move wider coherence to explicit architecture |

## A note on concurrency

You may see educational examples that use simple locks around first-load caching.

That can be useful as a bounded example, but the key point is:

serious concurrent caching is larger than one clever descriptor.

For this course, the important boundary is:

- per-instance cache mechanics can be shown in a descriptor
- real concurrent cache coordination usually belongs to stronger infrastructure

## When cached descriptors are a good fit

Use them when:

- the value is expensive to compute
- the value is meaningfully instance-scoped
- freshness can be described clearly
- invalidation can be made explicit

That is the sweet spot.

## When they are a poor fit

Cached descriptors are a weaker fit when:

- the value depends on volatile external state
- the invalidation story is unclear
- the system needs cross-instance or distributed coherence
- the cost of being stale is high

Those cases usually need more architecture than a field object alone.

## Review packet for one cached field

Before you leave this page, make sure you can produce one packet containing:

- the compute function or dependency rule
- the cache slot name
- the invalidation owner
- one stale-read example
- one refused stronger claim such as cross-instance coherence or automatic global freshness

## Review rules for cached descriptors

When reviewing a cached descriptor, keep these questions close:

- when is the value first computed?
- where is the cached value stored?
- what dependencies can make the cache stale?
- who invalidates it and how explicitly?
- is this still an attribute-level cache, or is it drifting toward wider caching infrastructure?
- can another reviewer point to the exact freshness owner in one sentence?

## Exit check for this page

Before moving on, make sure you can do all of these:

- explain the difference between computed, lazy, and cached access
- name one dependency that can make a cached field stale
- identify where the cached value lives
- say who or what clears it when it is no longer trustworthy

## What to practice from this page

Try these before moving on:

1. Implement one descriptor that computes on every read and one that caches after the first read.
2. Add an explicit `invalidate(obj)` method and show one stale-cache bug it prevents.
3. Write one short review note rejecting a cached descriptor because the freshness story is too vague.

If those feel ordinary, the next step is external storage, where the descriptor stops
owning the source of truth entirely.

## Continue through Module 08

- Previous: [Overview](index.md)
- Next: [External Storage Descriptors](external-storage-descriptors.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
