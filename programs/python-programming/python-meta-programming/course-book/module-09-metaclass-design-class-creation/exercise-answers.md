# Exercise Answers


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Metaclass Design Class Creation"]
  page["Exercise Answers"]
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

Use this page after attempting the exercises yourself. The point is not to match every
example literally. The point is to compare your reasoning against answers that keep
class-creation power, import-time behavior, and lower-power alternatives honest.

Use these answers as reasoning checkpoints, not as short model solutions to imitate. A
strong answer always leaves evidence for why the owner was chosen and what lower-power
alternative was rejected first.

## How to review your own answers against this page

For each exercise, check whether your answer includes:

| Checkpoint | What a strong answer shows |
| --- | --- |
| Named invariant | The exact class-creation, declaration-time, or hierarchy-wide rule |
| Named timing | When the rule acts in the class lifecycle |
| Rejected owner | The strongest lower-power alternative and why it was insufficient |
| Cost visibility | Import-time, reset, or composition cost if power escalates |
| Boundary honesty | What the mechanism does not own |

## Answer 1: Build one class manually with `type(...)`

Example answer:

- `name` becomes the class name
- `bases` determines inheritance
- `namespace` supplies methods and attributes

Useful metadata:

- `__module__` can be set manually so the class has a sensible module identity

Good conclusion:

This is still lower-power than a metaclass because it creates one class explicitly without
automatically changing how future subclasses are created.

Reasoning checkpoint:

- if your answer does not say why repeated future subclass control would change the design,
  your comparison to metaclasses is still weak

## Answer 2: Trigger and explain one metaclass conflict

Example answer:

If `A` uses `MetaA` and `B` uses `MetaB`, then:

```python
class Bad(A, B):
    pass
```

may raise a metaclass conflict because Python cannot find one compatible class-creation
owner for the new class.

Good conclusion:

The error is not just syntax friction. It is a signal that two incompatible class-creation
authorities are being combined without a coherent shared owner.

Reasoning checkpoint:

- a strong answer also says what simplification or joint ownership question must be asked
  before trying a technical repair

## Answer 3: Split one metaclass across `__new__` and `__init__`

Example answer:

- `__new__` should enforce a required method or inject a structural attribute before the class is finalized
- `__init__` should append the finished class to a registry

Good conclusion:

Swapping them makes the design blur structure and bookkeeping. `__new__` owns class-shape
decisions; `__init__` owns post-creation bookkeeping.

Reasoning checkpoint:

- your answer should make clear what namespace or finished-class evidence would be lost by
  moving the rule to the other hook

## Answer 4: Use `__prepare__` for one declaration-time rule

Example answer:

A custom mapping can reject duplicate non-dunder assignments during class body execution.

Why later hooks are worse:

- after the class body finishes, only the final value may remain unless the mapping
  recorded the duplicate event during assignment

Good conclusion:

`__prepare__` is justified only when the class-body-time fact truly matters and cannot be
recovered cleanly later.

Reasoning checkpoint:

- if your answer cannot say exactly what later hooks would fail to recover, the
  `__prepare__` claim is not yet honest

## Answer 5: Reject one unnecessary metaclass

Example answer:

Original idea:

- use a metaclass to register classes in a plugin list

Lower-power replacement:

- use an explicit decorator or helper function for opt-in registration

Good conclusion:

If post-creation registration is enough, the metaclass was not actually needed. The design
does not require class-creation control just because automatic registration sounds neat.

Reasoning checkpoint:

- the best answers name the convenience argument they are rejecting instead of only naming
  the replacement tool

## Answer 6: Review the plugin registry example honestly

Example answer:

Honest metaclass ownership:

- automatically registering every concrete subclass at class-creation time

Remaining risk:

- import order and reload behavior still affect when entries appear and whether tests need reset hooks

Why it is narrower than a full framework:

- it handles registration and ordering only, not discovery, lifecycle management, or configuration

Good conclusion:

The example is justified because the metaclass owns one clear hierarchy-wide class-creation
rule, not because registries are automatically “metaclass territory.”

Reasoning checkpoint:

- your answer should also say what import-time cost is accepted and what broader framework
  responsibilities are still outside the example

## Answer 7: Separate hierarchy-wide policy from post-creation bookkeeping

Example answer:

Suppose a plugin base wants:

- every concrete subclass registered automatically
- registration order preserved
- test resets available

Strong split:

- class-creation policy: deciding that every concrete subclass is registered at creation time
- bookkeeping: appending to the registry and exposing reset helpers

Good conclusion:

Keeping those concerns separate makes review easier because readers can tell which part is
the actual metaclass invariant and which part is ordinary operational support.

Reasoning checkpoint:

- a strong answer names where reset, ordering, or registry maintenance belongs once the
  invariant has been isolated

## Answer 8: Design one reset boundary for import-time class registration

Example answer:

A registry metaclass should often be paired with:

- `registry.clear()`
- a test helper that rebuilds expected entries explicitly
- documented import-order assumptions

Good conclusion:

Import-time behavior without reset discipline turns test isolation into guesswork. A clear
reset boundary makes the registration surface easier to verify and reason about.

Reasoning checkpoint:

- your answer should predict one concrete failure mode that appears when reset boundaries
  are missing

## Answer 9: Compare honest metaclass claims with overstated claims

Example answer:

Honest description:

- "This metaclass registers concrete subclasses at class-creation time and preserves declaration order."

Overstated description:

- "This metaclass manages the whole plugin system automatically."

Good conclusion:

The second version is misleading because words such as "whole" and "automatically" imply
discovery, lifecycle, configuration, and runtime coordination far beyond the actual
class-creation rule.

Reasoning checkpoint:

- the honest version should be specific enough that another learner could review the scope
  without inferring extra framework power

## Answer 10: Produce a metaclass-boundary packet

The packet is strong when another learner can answer:

- what invariant the metaclass owns
- when that invariant is enforced in the class lifecycle
- what declaration-time fact or hierarchy-wide rule justified the metaclass
- which lower-power owner would have been clearer if the invariant were smaller

Repair move if your packet is weak:

- rewrite each line so it begins with the invariant, timing, or rejected owner rather than
  with the mechanism name

## What strong Module 09 answers have in common

Across the whole set, strong answers share the same habits:

- they explain metaclasses in class-creation language
- they keep import-time effects visible
- they separate `__new__`, `__init__`, and `__prepare__` by responsibility
- they treat conflicts as design signals
- they reject metaclass escalation when lower-power tools still own the problem honestly
- they separate hierarchy-wide policy from follow-up bookkeeping
- they leave behind a packet another learner can review without guessing

If an answer still sounds like "metaclasses are powerful so they fit here," revise it
until you can name the exact class-creation invariant they own and why lower-power tools
fail.

## Exit check for the answer key

Before leaving this page, make sure your own answers now do all of the following:

- justify every escalation with an invariant rather than a vibe
- reject at least one lower-power owner explicitly
- keep import-time and reset costs visible
- leave a reviewer enough evidence to disagree with your owner choice for concrete reasons

## Continue through Module 09

- Previous: [Exercises](exercises.md)
- Return: [Overview](index.md)
- Next module: [Module 10](../module-10-runtime-governance-mastery-review/index.md)
- Terms: [Glossary](glossary.md)
