# External Storage Descriptors

The second pressure that turns simple descriptors into framework-shaped machinery is this:

the instance is no longer the source of truth.

Instead, the descriptor mediates access to something outside the object:

- a database row
- a key-value store
- a configuration backend
- a serialized record cache

That changes the design completely.

## The sentence to keep

An external-storage descriptor is a field descriptor whose source of truth lives outside
the instance, while the descriptor provides attribute access, key derivation, and often a
local read-through cache.

That is much bigger than “store a value in `obj.__dict__`.”

## What changes when storage becomes external

Once storage moves out of the instance, the descriptor usually has to own more than one
thing:

- how to derive or find the backend key
- how to serialize and deserialize values
- when to read through a local cache
- when to write through to the backend

This is why external descriptors feel much closer to framework design.

## A small educational backend

```python
import json


class MemoryStore:
    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data.get(key)

    def set(self, key, value):
        self._data[key] = value


store = MemoryStore()
```

This is obviously too small for production, but it is the right scale for showing the
descriptor mechanics honestly.

## A read-through external field

```python
class ExternalField:
    def __init__(self, store, prefix="field", pk_field="id"):
        self.store = store
        self.prefix = prefix
        self.pk_field = pk_field

    def __set_name__(self, owner, name):
        self.name = name
        self.cache_name = f"_{name}_cached"
        self.key_template = f"{self.prefix}:{owner.__name__}:%s:{name}"

    def _pk(self, obj):
        return getattr(obj, self.pk_field, None)

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        if self.cache_name in obj.__dict__:
            return obj.__dict__[self.cache_name]

        pk = self._pk(obj)
        if pk is None:
            return None

        raw = self.store.get(self.key_template % pk)
        if raw is None:
            return None

        value = json.loads(raw)
        obj.__dict__[self.cache_name] = value
        return value

    def __set__(self, obj, value):
        pk = self._pk(obj)
        if pk is None:
            raise ValueError("primary key must exist before writing external state")

        self.store.set(self.key_template % pk, json.dumps(value))
        obj.__dict__[self.cache_name] = value

    def invalidate(self, obj):
        obj.__dict__.pop(self.cache_name, None)
```

This is a small example, but it already surfaces the real concerns:

- backend key design
- read-through caching
- write-through persistence
- invalidation after local staleness

## Why primary keys matter here

When external state is shared or persisted, object identity in memory is not enough.

That is why examples like this usually derive keys from stable identifiers such as:

- primary keys
- model names
- field names

Those keys let the backend treat stored values as record state rather than as process-local
instance state.

## Hidden I/O is the risk you should name

External descriptors are powerful, but they can hide expensive behavior behind ordinary
attribute access.

That means `obj.field` may now imply:

- deserialization
- cache lookup
- storage reads
- latency or failure from a remote system

If that cost is not visible in docs, review, or instrumentation, the design is easy to
misread.

## Caching here is different from Core 1

In the previous core, the descriptor usually computed the value from local instance state.

Here, the descriptor does not own the source of truth at all.

So the cache is not only about saving computation. It is about avoiding repeated backend
access while still recognizing that the backend is authoritative.

That makes staleness and invalidation more serious.

## Serialization is part of the contract

External fields do not only store values. They cross a serialization boundary.

That boundary raises questions like:

- how are values encoded?
- what happens to `None`?
- what type information is lost?
- what happens when the stored schema drifts over time?

Even in a toy example, those questions are part of the field design.

## When external descriptors are a good fit

Use them when:

- one attribute genuinely maps to backend-managed state
- a field-level API improves readability
- the keying strategy is stable and reviewable
- read-through caching and invalidation are explicit

That is the honest zone for this pattern.

## When they are a poor fit

External descriptors are a weaker fit when:

- remote access cost is too surprising for normal attribute syntax
- the storage model needs transactions, units of work, or stronger consistency guarantees
- the object graph needs identity maps or relationship orchestration
- the system needs broader observability than a field can provide alone

Those are clues that the design has moved into framework architecture.

## Review rules for external fields

When reviewing an external-storage descriptor, keep these questions close:

- where is the real source of truth?
- how is the backend key derived?
- what does read-through caching hide or reveal?
- what invalidates stale local state?
- is attribute syntax still a reasonable surface for the cost of this access?

## What to practice from this page

Try these before moving on:

1. Build one external descriptor with a stable key format and explain why instance identity alone is not enough.
2. Add a local read cache and one explicit invalidation hook.
3. Write one short review note warning that attribute access now hides backend I/O.

If those feel ordinary, the next step is composition: layering field behavior without
turning every variation into a new subclass.

## Continue through Module 08

- Previous: [Cached Descriptors and Invalidation](cached-descriptors-and-invalidation.md)
- Next: [Descriptor Composition and Wrapper Fields](descriptor-composition-and-wrapper-fields.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
