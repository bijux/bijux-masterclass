# Frames and Diagnostic-Only Runtime Evidence


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Signatures Provenance Runtime Evidence"]
  page["Frames and Diagnostic-Only Runtime Evidence"]
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

Module 03 ends with the sharpest inspection surface in the module:

- `inspect.currentframe()`
- `inspect.stack()`
- frame objects and their links to locals, globals, and callers

These tools can be useful. They can also be expensive, intrusive, and memory-hungry
enough that the module needs a very clear rule:

> frames belong to diagnostics, debugging, and tooling, not to ordinary application
> control flow.

This is the place where many learners need the strongest pushback. Stack-based tricks can
feel clever, but they almost always weaken legibility, ownership, and reviewability when
they leak into normal program logic.

## The sentence to keep

When frame inspection appears in a design, ask:

> is this genuinely diagnostics, or is the code using stack introspection as normal
> program logic?

If it is normal program logic, skepticism should go up immediately.

Add one sharper question beside it:

> what explicit parameter or owned state should have carried this information instead of the stack?

## What a frame exposes

A frame object represents an execution record.

Useful attributes include:

- `f_code` for the executing code object
- `f_locals` for the local namespace snapshot
- `f_globals` for the global namespace
- `f_back` for the previous frame in the call chain

That is powerful, but it also means frames connect you to large object graphs very
quickly.

This is why the module treats frame access as high-cost evidence even when the helper
looks tiny. The surface area is larger than the few fields you happen to read first.

## `currentframe()` versus `stack()`

For this module, the key difference is:

- `inspect.currentframe()` gives you a starting frame or `None`
- `inspect.stack()` walks and packages much more of the call stack

That second tool is much heavier.

If you only need a small slice of caller context, building it manually from
`currentframe()` is often the more honest and cheaper choice.

Use this choice table:

| Real need | Better move | Why |
| --- | --- | --- |
| One or two caller names for a debug breadcrumb | `currentframe()` plus a bounded `f_back` walk | smaller scope, less packaging overhead |
| Full developer-facing trace context during troubleshooting | `inspect.stack()` may be acceptable | the job is explicitly diagnostic |
| Business rules based on who called the function | reject the design | caller identity should be explicit, not inferred from stack state |

## One picture of frame retention risk

```mermaid
graph TD
  frame["frame"]
  locals["f_locals"]
  objects["local objects"]
  back["f_back"]
  caller["caller frame"]
  callerLocals["caller locals"]
  frame --> locals --> objects
  frame --> back --> caller --> callerLocals
```

Caption: holding onto one frame can keep much more than one local variable alive.

This is why long-lived frame references can create leak-like retention problems.

Independent learners should pause here and state the rule plainly: one stored frame can
accidentally retain far more program state than the helper author intended.

## A small and safer caller helper

```python
import inspect


def top_callers(limit=3):
    frame = inspect.currentframe()
    if frame is None:
        return []
    try:
        out = []
        current = frame.f_back
        while current is not None and len(out) < limit:
            out.append(current.f_code.co_name)
            current = current.f_back
        return out
    finally:
        del frame
```

This helper still belongs to diagnostics, but it avoids the heavier full-stack collection
pattern.

The `del frame` matters because it helps break reference cycles sooner.

That small cleanup line is part of the lesson, not noise. Diagnostic code has memory and
retention consequences that ordinary parameter-passing code does not.

## Snapshot locals instead of retaining frames

If the real need is a bit of diagnostic state, snapshot the information you need instead
of storing frame objects:

```python
import inspect


def snapshot_locals(limit=2):
    frame = inspect.currentframe()
    if frame is None:
        return []
    try:
        out = []
        current = frame.f_back
        while current is not None and len(out) < limit:
            out.append(dict(current.f_locals))
            current = current.f_back
        return out
    finally:
        del frame
```

That is usually a healthier diagnostic pattern than holding onto frames or tracebacks
themselves.

The review gain is that snapshots are easier to reason about:

- they freeze the small evidence you actually wanted
- they do not keep live execution context around longer than necessary

## Why `inspect.stack()` deserves caution

`inspect.stack()` is easy to reach for because it looks convenient. It also does more work
than many callers really need.

Costs and risks include:

- walking the full Python stack
- consulting source line machinery
- building frame info objects for many levels
- retaining references if the result is stored carelessly

That does not make it forbidden. It makes it a tool for debugging and developer-facing
reporting, not a casual utility inside hot paths.

Weak pattern to reject explicitly:

- "it is just a convenience helper, so using `inspect.stack()` everywhere is fine"

That sentence usually hides both unnecessary work and a fuzzy ownership model.

## Diagnostic-only is a real boundary

This module keeps saying "diagnostic-only" on purpose.

That phrase means:

- acceptable in debugging helpers
- acceptable in crash reporting
- acceptable in explicit developer tooling
- risky in ordinary application logic
- especially risky as hidden control flow or authorization logic

The value here is not just performance. It is also legibility and reviewability.

Code that depends on who called it, as seen through stack inspection, is much harder to
reason about than code with explicit parameters and ownership.

Review checkpoint:

- can the same information be passed explicitly?
- is the frame evidence transient and bounded?
- if the helper disappeared, would the application contract become clearer rather than weaker?

## Review rules for frame inspection

When reviewing frame or stack inspection, keep these questions close:

- is this clearly diagnostic code, or has stack inspection leaked into normal logic?
- could the same information be passed explicitly instead of recovered from frames?
- does the code use `currentframe()` for a small bounded need instead of `inspect.stack()` by habit?
- are frame references released promptly instead of stored in long-lived structures?
- would a snapshot of locals or caller names be enough instead of retaining live frame objects?

## Self-study lab

Before leaving this page, write one diagnostic helper note in this format:

- the exact debug question the helper answers
- the smallest frame surface it touches
- the explicit reason it must remain diagnostic-only
- the explicit parameter or owned state you would use instead if the feature became production logic

If the last line feels hard to write, the boundary is probably still too fuzzy.

## What to practice from this page

Try these before moving on:

1. Write a helper that returns the top few caller names using `currentframe()` and `f_back`.
2. Snapshot caller locals without retaining a frame object after the helper returns.
3. Explain one diagnostic use case for frame inspection and one application-level use case that should be rejected.

If those feel ordinary, the worked example can combine the module's evidence tools inside
a safer `__repr__` helper.

## Continue through Module 03

- Previous: [Dynamic Members and Static Structure](dynamic-members-and-static-structure.md)
- Next: [Worked Example: Building a Safe Signature-Guided `__repr__`](worked-example-building-a-safe-signature-guided-repr.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
