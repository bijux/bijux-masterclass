# Data and Non-Data Descriptor Precedence


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Descriptors Lookup Attribute Control"]
  page["Data and Non-Data Descriptor Precedence"]
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

This page answers the question that makes descriptors stop feeling mysterious:

why does one descriptor beat instance state while another can be shadowed?

The answer is precedence.

This page matters because descriptor protocol knowledge remains weak until a reader can
predict lookup results without guessing. Precedence is the part that turns "Python did
something weird" into a reviewable explanation.

## The sentence to keep

Data descriptors win over the instance dictionary, while non-data descriptors yield to the
instance dictionary when the same attribute name exists there.

That one rule explains a large share of descriptor behavior.

Keep a second sentence beside it:

> the difference is mechanical, not emotional; the methods present on the descriptor decide the category and therefore the lookup result.

## The two categories

The distinction is mechanical:

- a data descriptor defines `__set__`, `__delete__`, or both
- a non-data descriptor defines only `__get__`

This is why a descriptor's category is not about intention. It is about which methods are
present.

That is worth slowing down for. A descriptor does not become "data-like" because it feels
important. It becomes a data descriptor because `__set__`, `__delete__`, or both are
implemented.

## The default lookup order

For ordinary instance lookup under `object.__getattribute__`, the useful review model
is:

1. look for the attribute on the class and its MRO
2. if that class attribute is a data descriptor, use it
3. otherwise, if the name exists in `obj.__dict__`, return that value
4. otherwise, if the class attribute is a non-data descriptor, call `__get__`
5. otherwise, return the plain class attribute or continue lookup

This is the lookup rule that turns many "Python did something weird" moments into a
reviewable explanation.

## Evidence route for precedence reviews

Use this route whenever a lookup result feels surprising:

| Evidence step | What it proves |
| --- | --- |
| find the class attribute in the MRO | tells you whether a descriptor is even in play |
| inspect which descriptor hooks exist | tells you whether it is data or non-data |
| inspect `obj.__dict__` for the same public name | tells you whether instance state can win |
| replay the order mechanically | turns the result into a reviewable consequence instead of folklore |

## A compact data-descriptor example

```python
class DataField:
    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.private_name, 0)

    def __set__(self, obj, value):
        obj.__dict__[self.private_name] = value


class Sample:
    value = DataField()


s = Sample()
s.value = 10
s.__dict__["value"] = 999
print(s.value)  # 10
```

The descriptor still wins because it is a data descriptor.

That example is worth narrating aloud: Python finds the class attribute, sees that the
descriptor defines `__set__`, classifies it as a data descriptor, and therefore resolves
through the descriptor before the same-named entry in `obj.__dict__` gets a chance.

## A compact non-data example

```python
class NonDataField:
    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return "computed"


class Sample:
    value = NonDataField()


s = Sample()
print(s.value)  # computed
s.value = "shadowed"
print(s.value)  # shadowed
```

This time the instance dictionary wins because the descriptor defines only `__get__`.

The important repair here is to name the exact public name that gets shadowed. A learner
who says only "it was overridden somehow" is still missing the lookup rule.

## Why `property` is important here

Properties are a perfect bridge into the rule.

A `property` object is a data descriptor. Even a read-only property still defines
descriptor machinery that makes it win over `obj.__dict__`.

That is why this does not bypass a property:

```python
obj.__dict__["name"] = "bypass attempt"
```

If `name` is a property, the property still owns the boundary.

That detail connects Module 07 back to Module 06 in a concrete way.

It also corrects a persistent beginner misconception: a read-only property is still a data
descriptor and therefore still owns the attribute boundary during normal lookup.

## Why methods are different

Plain functions defined on classes are non-data descriptors.

That means they can be shadowed by instance attributes. This is not a footnote. It is one
of the reasons method binding stays flexible instead of absolutely dominant over instance
state.

The next core will make that more concrete.

## A comparison table worth keeping open

| Situation | What wins first |
| --- | --- |
| data descriptor plus same-named instance entry | data descriptor |
| non-data descriptor plus same-named instance entry | instance entry |
| plain class attribute plus instance entry | instance entry |
| data descriptor with no instance entry | data descriptor |

## A useful diagram to keep in your head

```text
data descriptor
  -> wins over obj.__dict__

instance dictionary
  -> wins over non-data descriptor

non-data descriptor
  -> runs only if the instance dictionary does not already own the name
```

That is the picture most people actually need in review and debugging.

## Common overclaims to reject

Reject these descriptions when they appear in review:

| Overclaim | Better replacement |
| --- | --- |
| "descriptors always beat instance state" | "data descriptors beat instance state; non-data descriptors do not" |
| "read-only properties are bypassable because they have no setter" | "properties still participate as data descriptors in normal lookup" |
| "shadowing means the descriptor stopped working" | "shadowing means a non-data descriptor yielded to a same-named instance entry" |
| "precedence is too subtle to explain" | "precedence is a mechanical lookup order that can be traced step by step" |

## Failure modes for precedence reasoning

These are the mistakes this page is trying to prevent:

| Failure mode | Why it weakens the design | Repair move |
| --- | --- | --- |
| forgetting to inspect `obj.__dict__` under the public name | shadowing behavior looks magical | inspect the exact name that lookup uses |
| calling a descriptor "data" without checking hooks | category and result get disconnected | point to `__set__` or `__delete__` explicitly |
| treating property lookup as special syntax instead of precedence | lessons stay isolated instead of connected | explain properties in descriptor-precedence language |
| using precedence to justify a subtle API | the code becomes harder to review than it needs to be | simplify the boundary rather than relying on lookup cleverness |

## What this rule is for

Use the precedence rule to answer questions like:

- why does a property still intercept access even when a same-named entry appears in `__dict__`?
- why can an instance attribute replace the behavior of a non-data descriptor?
- why do reusable validators often need to be data descriptors?

If the answer depends on "because descriptors are advanced," the rule is not being used
precisely enough.

## A warning about over-clever APIs

Precedence is a real runtime rule, but it is not a good excuse for cleverness.

If an API is understandable only because its users memorize data-descriptor versus
non-data-descriptor precedence, the API is probably too subtle.

The rule is best used for:

- debugging
- honest explanation
- choosing the smallest owner for a field invariant

It is a poor substitute for clear design.

## Review rules for precedence

When reviewing descriptor lookup, keep these questions close:

- is the class attribute a data descriptor or a non-data descriptor?
- what value, if any, is stored in `obj.__dict__` under the same name?
- is the code relying on shadowing intentionally or accidentally?
- is a property being described incorrectly as bypassable?
- would a plainer attribute boundary be easier to review than a precedence trick?
- can another reviewer narrate the exact winning step without saying "magic"?

## Exit check for this page

Before moving on, make sure you can do all of these:

- explain why a data descriptor beats a same-named instance entry
- explain why a non-data descriptor can be shadowed
- describe one property lookup in data-descriptor language
- inspect one object and name the exact evidence that decides the result

## What to practice from this page

Try these before moving on:

1. Build one data descriptor and show that `obj.__dict__` cannot shadow it.
2. Build one non-data descriptor and show that the instance dictionary can shadow it.
3. Explain one property example in descriptor-precedence language rather than property-specific language.

If those feel ordinary, the next step is method binding: the most common non-data
descriptor behavior in everyday Python.

## Continue through Module 07

- Previous: [Descriptor Protocol and `__set_name__`](descriptor-protocol-and-set-name.md)
- Next: [Functions, Binding, and Method Descriptors](functions-binding-and-method-descriptors.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
