# Capstone Extension Guide

<!-- page-maps:start -->
## Page Maps

```mermaid
graph TD
  guide["Capstone Extension Guide"]
  plugin["Add a plugin"]
  field["Add a field type"]
  action["Add an action"]
  policy["Preserve policy boundaries"]

  guide --> plugin
  guide --> field
  guide --> action
  guide --> policy
```

```mermaid
flowchart LR
  idea["Extension idea"] --> choose["Choose the owning layer"]
  choose --> source["Edit one source file first"]
  source --> tests["Add or update proof tests"]
  tests --> review["Run review checklist and proof route"]
```
<!-- page-maps:end -->

This guide explains how to extend the capstone without making it pedagogically muddy.
The rule is to keep one extension attached to one clear ownership boundary.

## Safe extension categories

### Add a new plugin

Edit `plugins.py`, add one concrete subclass, and prove that registration, manifest
export, and invocation all work without changing metaclass internals.

### Add a new field type

Edit `fields.py`, add a new descriptor specialization, and prove coercion and manifest
shape before using it in a plugin.

### Add a new action

Edit one plugin method, use `@action`, and prove the wrapper preserves signature and
history recording.

## Unsafe extension patterns

- adding metaclass behavior before trying a class decorator or plain function
- making manifest generation execute plugin methods
- hiding registry resets or test isolation inside unrelated helper code

## Review rule

Every extension should answer:

- why this layer owns the change
- why a lower-power layer was insufficient
- what new proof was added to keep the runtime observable
- which local capstone guide or review bundle changed as a result
