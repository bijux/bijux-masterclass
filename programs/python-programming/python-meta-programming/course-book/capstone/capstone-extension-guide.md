# Capstone Extension Guide

<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Metaprogramming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone Extension Guide"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

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
