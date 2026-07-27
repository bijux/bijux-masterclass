# Descriptor Composition and Wrapper Fields


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Descriptor Systems Validation Framework Design"]
  page["Descriptor Composition and Wrapper Fields"]
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

Once descriptor systems start carrying several concerns at once, teams hit a design fork:

- create more subclasses for every combination
- or layer behavior around an inner field

This core focuses on the second option.

This page matters because composition can sound cleaner than subclass explosion while
quietly making field behavior harder to inspect. A learner studying alone needs a way to
prove which layer owns what and when the wrapper stack has become too opaque to justify.

## The sentence to keep

Descriptor composition wraps one field descriptor in another so new behavior can be added
through delegation instead of by multiplying subclasses for every field variant.

That is useful, but only if the layers stay inspectable.

Keep one more sentence beside it:

> every wrapper layer must earn its existence by adding one clear concern without hiding the inner owner.

For self-study, turn that into a written trace:

- name the inner field contract in one sentence
- name the one added concern for each wrapper
- trace one assignment from outermost layer to stored value
- say which layer you would remove first if readability started to slip

## Why composition shows up here

By Module 08, a field might want more than one concern:

- storage
- validation
- coercion
- logging
- caching

If every combination becomes its own subclass, the design quickly turns into a class tree
that is harder to review than the field logic itself.

Composition is the usual escape hatch.

Use this table before trusting a composed field design:

| Pressure | Review question |
| --- | --- |
| inner ownership | what field behavior would still exist if every wrapper disappeared? |
| added concern | what one extra responsibility does this layer add? |
| forwarding | which protocol methods must be delegated to keep the field honest? |
| stack depth | how many layers must a reader traverse to explain one write? |
| escalation | at what point is a wider framework abstraction clearer than more wrappers? |

## A delegation base

```python
class FieldWrapper:
    def __init__(self, inner):
        self.inner = inner

    def __set_name__(self, owner, name):
        self.inner.__set_name__(owner, name)

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return self.inner.__get__(obj, owner)

    def __set__(self, obj, value):
        self.inner.__set__(obj, value)
```

This is the useful center of the pattern:

- the wrapper owns one extra concern
- the inner descriptor still owns the underlying field contract

That keeps layering explicit.

That is the rule to defend through the rest of the page:

remove the wrapper and the inner field should still have a recognizable contract.

## A validated wrapper

```python
def validated(validator, inner):
    class ValidatedField(FieldWrapper):
        def __init__(self):
            super().__init__(inner)

        def __set__(self, obj, value):
            self.inner.__set__(obj, validator(value))

    return ValidatedField()
```

This shape works because the wrapper does one narrow thing:

- it transforms or rejects the incoming value
- then it delegates ordinary field storage to the inner descriptor

That is much easier to reason about than a whole new subclass hierarchy for every rule.

## Evidence route for wrapper reviews

Use this route whenever a composed field sounds elegant but feels hard to trust:

| Evidence step | What it proves |
| --- | --- |
| identify the innermost field | tells you the underlying attribute contract |
| list one responsibility per wrapper | tells you whether each layer has a narrow reason to exist |
| trace `__set_name__`, `__get__`, and `__set__` | tells you whether protocol forwarding is complete and coherent |
| trace one assignment end to end | shows where transformation, validation, and storage actually happen |
| remove one layer mentally | shows whether the wrapper adds value or only ceremony |

## What good composition looks like

Good wrapper-field composition usually has these traits:

- one obvious inner owner
- one obvious added concern per layer
- consistent forwarding of `__set_name__`, `__get__`, and `__set__`
- shallow enough depth that a reviewer can still follow it mentally

That last point matters more than people think.

Keep a layer ledger while you review:

| Layer | Owned concern | Protocol methods it must forward or override | Why it is still worth having |
| --- | --- | --- | --- |
| inner field | base attribute contract | its own full descriptor protocol | it defines the durable field semantics |
| wrapper 1 | one added concern | the methods required for that concern plus correct delegation | it adds one clear behavior without hiding the base field |
| wrapper 2 and beyond | another single concern each | same rule | only justified if the stack still stays readable |

## A write-trace worksheet

Use this worksheet before you accept a wrapper stack as readable:

| Step in one assignment | Which layer owns it? | What value shape leaves this step? |
| --- | --- | --- |
| incoming public value | outermost wrapper or caller contract | raw input |
| validation or transformation | specific wrapper layer | transformed or rejected value |
| storage delegation | inner field | value ready for storage |
| final storage side effect | innermost storage owner | persisted or cached value |

If two adjacent rows have the same answer for ownership, one layer may not be earning its
existence.

## What bad composition looks like

Composition becomes harder to trust when:

- wrappers hide the inner descriptor completely
- different layers each mutate values in surprising ways
- `__set_name__` is forwarded inconsistently
- the stack grows deep enough that field behavior becomes an archaeological dig

At that point, “composable” is no longer the same as “clear.”

## Common overclaims to reject

Reject these descriptions when they appear in review:

| Overclaim | Better replacement |
| --- | --- |
| "wrappers keep everything modular" | "wrappers keep things modular only while each layer stays shallow and inspectable" |
| "the stack is flexible" | "the stack is flexible, but each layer increases review cost" |
| "delegation handles the rest" | "delegation must be traced method by method, especially for `__set_name__`" |
| "we can always add one more layer later" | "another layer is acceptable only if ownership stays legible" |

## Weak answers to reject early

| Weak answer | Why it fails |
| --- | --- |
| "the wrapper is there for flexibility" | flexibility does not name a concrete concern |
| "all layers are lightweight" | lightweight layers can still create heavy review cost |
| "the inner field still works somehow" | somehow means the base contract is not yet clear |
| "delegation is standard" | standard does not prove `__set_name__`, `__get__`, and `__set__` are forwarded coherently |

## Why `__set_name__` deserves special care

One easy bug in wrapped descriptors is forwarding `__set_name__` incorrectly.

Problems include:

- never forwarding it to the inner field
- forwarding it more than once
- partially shadowing the name state in both wrapper and inner descriptor

Because `__set_name__` often initializes storage keys and public names, this is not a
small detail. It is part of whether the wrapped field works at all.

Use this proof route whenever name binding bugs are plausible:

- find where the public and private names are created
- confirm whether wrapper state shadows the inner field or reuses it
- confirm whether forwarding happens once and only once
- test one class definition path, not only instance reads and writes

## Composition is not a license for endless stacks

There is a real limit to how many field layers remain readable.

As a practical rule, very shallow composition is much easier to justify than deep stacks.

If a field design now wants:

- logging
- validation
- coercion
- caching
- encryption
- remote persistence

all as separate wrapper layers, the design may already be asking for a stronger framework
abstraction than “one wrapped descriptor.”

That is the escalation boundary to keep visible:

composition is for additive field concerns, not for hiding architecture behind an
infinite decorator stack.

Use a simple wrapper budget:

- one inner field plus one wrapper is usually easy to justify
- one inner field plus two wrappers needs a written layer ledger
- beyond that, you should prove why a wider abstraction would not be clearer

## Why this is better than subclass explosion

Used well, composition lets a field system say:

- here is the base storage or coercion field
- here is one wrapper adding validation
- here is another wrapper adding one more cross-cutting concern

That makes behavior additive and local instead of forcing a huge family of subclasses such
as:

- `CachedStringField`
- `ValidatedCachedStringField`
- `LoggedValidatedCachedStringField`

and so on.

The goal is not sophistication. The goal is keeping ownership legible.

## Failure modes for wrapper fields

These are the mistakes this page is trying to prevent:

| Failure mode | Why it weakens the design | Repair move |
| --- | --- | --- |
| wrapper adds more than one real concern | the layer stops being easy to justify | split the concerns or move to a wider abstraction |
| inner field ownership becomes hard to state | readers cannot tell what the base contract is anymore | simplify the stack and restate the innermost field contract |
| `__set_name__` forwarding is missing or duplicated | names, storage slots, or validators can drift | trace name initialization explicitly and forward once |
| multiple wrappers mutate values in surprising sequence | write behavior becomes guesswork | document and simplify the transformation order |
| stack depth exceeds quick human inspection | review cost becomes higher than subclass sprawl ever saved | replace the stack with a clearer framework-level owner |

## Review rules for wrapper fields

When reviewing descriptor composition, keep these questions close:

- what does the inner descriptor own?
- what one extra concern does this wrapper add?
- is `__set_name__` delegated correctly and only once?
- how many layers do you need to traverse to understand one attribute write?
- has the stack grown large enough that a different framework abstraction would be clearer?
- can you name the exact layer you would remove first if the stack had to get simpler?

## Exit check for this page

Before moving on, make sure you can do all of these:

- state the base contract of the inner field in one sentence
- name one added concern for one wrapper and nothing more
- explain how `__set_name__` reaches the inner field
- trace one write path through the stack without guessing
- say when you would stop adding wrappers and escalate to a broader design

## What to practice from this page

Try these before moving on:

1. Wrap one validating field around one storage field and explain which concern each layer owns.
2. Show one bug caused by forgetting to forward `__set_name__`.
3. Write one short review note rejecting a four-layer field stack as too opaque.

If those feel ordinary, the next step is hint-driven validation and coercion, where the
descriptor starts reading type metadata as runtime evidence.

## Continue through Module 08

- Previous: [External Storage Descriptors](external-storage-descriptors.md)
- Next: [Hint-Driven Validation and Coercion](hint-driven-validation-and-coercion.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
