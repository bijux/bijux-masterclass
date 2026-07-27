# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Class Customization Pre Metaclasses"]
  page["Exercises"]
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

Use these after reading the five core lessons and the worked example. The goal is not to
collect more class tricks. The goal is to make class-level ownership, attribute
boundaries, and escalation decisions explicit.

Each exercise asks for three things:

- the class rule or invariant you are trying to enforce
- the class-level tool you chose
- the reason that choice is the smallest honest owner

Treat the ten exercises as one full lab day on class customization before metaclasses.

This is not a "use ten advanced class features" worksheet. It is a boundary-review lab. A
weak answer can compile, look tidy, and still miss the learning goal if it hides the real
owner or overstates what the chosen tool actually guarantees.

Do them in order:

- Exercises 1-3 establish class decorators, dataclass limits, and single-attribute boundaries
- Exercises 4-6 move into reusable attribute control, lower-power placement, and frozen-surface limits
- Exercises 7-8 extend that discipline into escalation decisions and explicit invariant ownership
- Exercises 9-10 package the whole module into a reviewable class-boundary packet

Keep one class-boundary table while you work:

| Invariant or class rule | Smallest honest owner | What it controls directly | What it does not control | Review judgment |
| --- | --- | --- | --- | --- |

Keep one second table beside it:

| Exercise | Evidence the reviewer can inspect | Stronger tool rejected | Missing condition that would justify escalation |
| --- | --- | --- | --- |

## Evidence discipline for the whole exercise set

Do not hand in answers that stop at "this seems cleaner" or "this is more advanced."

Across the set, your packet should name:

- the exact owner carrying the rule
- one observable proof that the rule really works at that boundary
- one stronger mechanism you rejected first
- one gap, allowed mutation, or missing condition that stays visible

## Exercise 1: Use one class decorator for an opt-in class rule

Write or inspect a class decorator that adds one visible post-construction behavior.

What to hand in:

- the behavior it adds
- one sentence explaining why the class decorator can install it after class creation
- one sentence explaining why this does not need a metaclass
- one sentence naming the first requirement that would make the decorator too weak

Verification hint:

- expand the decorator into an explicit helper call and confirm the timing story still matches

## Exercise 2: Separate dataclass generation from validation

Create or review a small `@dataclass` example with defaults and generated methods.

What to hand in:

- the generated behavior you are relying on
- one invariant that the dataclass still does not enforce for you
- one sentence describing where that missing rule should live instead
- one sentence naming the overclaim you are deliberately refusing

Verification hint:

- imagine one clearly invalid runtime value and identify the exact line that would reject it, or admit that no line does yet

## Exercise 3: Control one attribute boundary with a property

Implement one property that protects a single attribute.

What to hand in:

- the attribute rule it enforces
- one setter or getter behavior that makes the boundary visible
- one explanation of why a property is clearer here than a class-wide hook
- one sentence explaining what would change if the same rule appeared on many fields

Verification hint:

- show that the property still wins over same-named instance-dictionary state during normal lookup

## Exercise 4: Promote one repeated property rule into a descriptor

Take a repeated field rule and sketch or build a reusable descriptor for it.

What to hand in:

- the repeated rule
- one reason the rule is now better owned by a descriptor than by copied properties
- one sentence explaining why this is still different from metaclass control
- one sentence naming the exact reuse pressure that caused the escalation

Verification hint:

- name at least two attributes or classes that would otherwise carry copied property logic

## Exercise 5: Place one design on the lower-power ladder

Choose one class customization requirement and place it on this ladder:

- plain class code
- class decorator
- property
- descriptor
- metaclass

What to hand in:

- the requirement
- the level you chose
- one sentence rejecting at least one stronger option as unnecessary
- one sentence naming the missing condition that stronger option would actually need

Verification hint:

- rewrite the requirement one level lower and explain exactly where clarity would break, if it would

## Exercise 6: Review the limits of a frozen surface

Use the worked example pattern on a minimal `@frozen` decorator or a similar design.

What to hand in:

- the exact mutation boundary the decorator controls
- one kind of mutation it still allows
- one explanation of why that remaining mutability does not make the example dishonest
- one sentence naming the first change that would force a stronger owner than the minimal decorator

Verification hint:

- include one successful nested mutation or other allowed change so the remaining boundary stays visible

## Midday self-check

Before moving into the final four exercises, make sure you can already answer these
questions clearly:

- when a class decorator is enough and when class-creation-time control is not actually needed
- which invariants `@dataclass` generates for convenience and which ones still need a real owner
- why a property, descriptor, or `__post_init__` hook may be clearer than a broader class-wide mechanism
- what kind of "frozen" claim remains honest for a shallow attribute boundary

If you cannot answer those four questions in plain language, return to Exercises 1-6 and
make the owner, boundary, and rejected stronger option more explicit before continuing.

If your answers still rely on phrases like "the magic handles it" or "the class feature
makes it safe," revise them before moving on. Those phrases hide exactly the owner story
this module is trying to teach.

## Exercise 7: Separate repeated field policy from class-wide policy

Choose one rule that repeats across attributes or classes and decide whether it belongs in
`__post_init__`, a property, or a descriptor.

What to hand in:

- the repeated rule
- the owner you chose
- one explanation of why at least one alternative owner would be less clear
- one sentence naming who would debug the rule if it started failing in production

Verification hint:

- identify whether the first debugging stop would be a constructor hook, one attribute boundary, or a reusable descriptor

## Exercise 8: Reject one unnecessary escalation to metaclass power

Choose one class customization idea that may tempt someone to reach for a metaclass too
early.

What to hand in:

- the original requirement
- the lower-power owner you would choose instead
- one sentence explaining what true class-creation-time need is still missing
- one sentence describing what evidence would finally justify metaclass escalation

Verification hint:

- say whether the rule needs class-body timing, descriptor naming time, or only finished-class mutation time

## Exercise 9: Compare honest class claims with overstated class claims

Choose one class customization tool and write both an honest description and an overstated
description of what it guarantees.

What to hand in:

- the honest description
- the overstated description
- one explanation of which words make the overstated version misleading
- one replacement sentence that stays useful without inflating the guarantee

Verification hint:

- circle or quote the exact inflated words such as "automatic," "immutable," or "enforces" before rewriting them

## Exercise 10: Produce a class-boundary packet

Assemble:

- one class-boundary table
- one dataclass example with a named missing invariant owner
- one attribute-boundary example using a property or descriptor
- one rule for rejecting unnecessary escalation to metaclasses

The packet is strong when another learner can use it to answer:

- which owner is carrying the invariant
- what that owner controls directly
- why a stronger mechanism was rejected as unnecessary

Make the packet easy to scan. Another learner should be able to review it without knowing
your original code in detail.

## Packet quality checks

Before you accept your packet, make sure it does all of these:

- uses at least three different owner surfaces honestly instead of forcing every answer into one favorite tool
- records at least three rejected stronger mechanisms explicitly
- leaves at least three visible gaps or allowed mutations instead of pretending the surfaces are universal
- gives another learner enough evidence to disagree with you for concrete reasons

## Repair prompts for weak exercise drafts

Use these prompts when an answer feels vague, overpowered, or suspiciously confident:

| If your answer says... | Ask yourself instead... |
| --- | --- |
| "the dataclass enforces it" | where is the explicit rule owner actually located? |
| "the property keeps it simple" | simple because it is one attribute boundary, or just because the syntax looks friendly? |
| "a descriptor is more advanced" | what repeated field pressure makes reuse necessary here? |
| "a metaclass could handle it" | what class-creation-time requirement is missing right now? |
| "the object is frozen" | which mutations are still allowed? |

## Mastery standard for this exercise set

Across all six answers, the module wants the same habits:

- you distinguish generated convenience from real policy ownership
- you keep attribute control at the narrowest honest boundary
- you treat descriptors as reusable attribute tools, not as prestige mechanisms
- you reject metaclass escalation when post-construction or attribute-boundary tools are still enough

Across all ten answers, add two more habits:

- you distinguish repeated field policy from truly class-wide creation policy
- you leave behind a class-boundary packet another learner could review without guessing

If an answer still sounds like "the class magic handles it," keep going.

## Exit check for the exercise set

Before you leave Module 06 practice, make sure your packet lets another learner answer
all of these:

- which class rules stayed post-construction and which ones crossed to attribute-boundary ownership
- which stronger tools you rejected and why
- which remaining gaps or allowed mutations stayed explicit
- which requirement would finally justify metaclass escalation

## Continue through Module 06

- Previous: [Worked Example: Building a Minimal `@frozen` Class Decorator](worked-example-building-a-minimal-frozen-class-decorator.md)
- Next: [Exercise Answers](exercise-answers.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
