# Static Lookup and Disciplined Observation


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Runtime Observation Inspection"]
  page["Static Lookup and Disciplined Observation"]
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

The earlier pages in Module 02 teach separate boundaries:

- names are not stored state
- dynamic attribute access is not passive
- classification tools answer different questions
- callability is only a limited claim

This page turns those ideas into one repeatable observation workflow and introduces the
most important preview tool for that workflow:

`inspect.getattr_static`

## The sentence to keep

When you inspect runtime objects for tooling or review, ask:

> do I need the value normal lookup would produce, or do I need the raw thing attached to
> the object without executing lookup behavior?

That is the static-versus-dynamic boundary in one sentence.

## Dynamic lookup answers the runtime-behavior question

Normal attribute access and `getattr(obj, name)` answer:

> what happens if I let Python run the attribute protocol?

That can involve:

- descriptors
- `__getattribute__`
- `__getattr__`
- proxy logic
- metaclass behavior for class attributes

Sometimes that is exactly what you want. Often, tooling wants a narrower and safer
question.

## Static lookup answers a tooling question

`inspect.getattr_static(obj, name)` aims to retrieve the raw attribute or descriptor
without triggering normal attribute resolution behavior.

That makes it useful when you need to inspect what is attached rather than what executing
lookup would return.

Typical cases:

- debugging tools
- schema or manifest builders
- documentation helpers
- review utilities that should avoid business behavior

This is not a claim that static lookup is perfect or universal. It is a claim that the
question is different, and the tool matches that different question.

## One picture of the boundary

```text
Dynamic read
  getattr(obj, "x")
  -> run normal attribute protocol

Static read
  inspect.getattr_static(obj, "x")
  -> inspect the attached object without normal protocol execution
```

Caption: debugging and tooling often want attachment truth, not execution truth.

## A property shows the difference clearly

```python
import inspect


class Demo:
    @property
    def value(self):
        print("property executed")
        return 10


obj = Demo()

raw = inspect.getattr_static(obj, "value")
assert isinstance(raw, property)

resolved = getattr(obj, "value")
assert resolved == 10
```

The printed line only appears during the dynamic read. That is the runtime boundary:

- static lookup reveals the property object
- dynamic lookup executes the property

## Static lookup is not the first tool for every question

This module is not arguing that static lookup should replace everything else.

A disciplined workflow usually looks like this:

1. discover candidate names with `dir(obj)` when needed
2. inspect stored state with `vars(obj)` or `obj.__dict__` when available
3. use `type`, `isinstance`, or `issubclass` for the classification question you really mean
4. resolve values dynamically only when you actually need the runtime behavior
5. use static lookup when tooling must avoid triggering descriptors or fallback hooks

That workflow keeps the risk of observation proportional to the question being asked.

## Static lookup improves honesty in tooling

Suppose you are building a debug printer, plugin manifest, or field inspector.

If you use dynamic reads by default, your tool may:

- execute properties
- trigger lazy-loading behavior
- trigger network or file access hidden behind `__getattr__`
- accidentally mutate caches or other state while "observing"

If you use static lookup where appropriate, the tool can say something narrower and more
honest:

> here is the raw attribute object attached to this instance or class, without running its
> normal access behavior.

That is often the right default for observability tools.

## Static lookup still needs interpretation

Static lookup does not remove the need for judgment.

It may return:

- a property object
- a slot descriptor
- a function stored on the class
- a plain value

The tooling still has to decide what to show and what to execute, if anything.

That is why Module 02 treats static lookup as part of a workflow, not as a silver bullet.

## Module 03 will deepen this story

This page is only a preview, not the final `inspect` module lesson.

Module 03 will expand the tooling story around:

- signatures
- provenance
- stronger runtime evidence
- more explicit static-versus-dynamic distinctions

Module 02 only needs enough of the idea to make observation discipline real.

## Review rules for disciplined observation

When reviewing tooling or runtime-inspection code, keep these questions close:

- does the code need raw attachment truth or normal runtime behavior?
- is a dynamic read being used where static lookup would better match the tool's purpose?
- has the workflow separated discovery, stored-state inspection, classification, and execution?
- is the code explicit about when it chooses to evaluate descriptors or properties?
- does the tool fail honestly when a surface is unavailable instead of quietly executing more protocol?

## What to practice from this page

Try these before moving on:

1. Compare `inspect.getattr_static(obj, "x")` with `getattr(obj, "x")` on a property.
2. Write down one tooling situation where dynamic lookup is the right choice and one where static lookup is the right choice.
3. Turn the five-step workflow above into a checklist you could use during code review.

If those feel ordinary, the worked example can pressure-test the workflow in a realistic
debug-printing tool.

## Continue through Module 02

- Previous: [Callable Objects and the Call Protocol](callable-objects-and-the-call-protocol.md)
- Next: [Worked Example: Building a Safer Debug Printer](worked-example-building-a-safer-debug-printer.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
