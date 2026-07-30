# Worked Example: Building a Minimal `@frozen` Class Decorator


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Class Customization Pre Metaclasses"]
  page["Worked Example: Building a Minimal `@frozen` Class Decorator"]
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

The five core lessons in Module 06 become easier to trust when they meet one class tool
that is useful, tempting, and easy to overclaim.

A minimal `@frozen` decorator is exactly that kind of tool.

Treat this page as a review packet, not as a production recipe. Its main value is that it
shows where a post-construction class rule stays honest, where it starts to overstate its
power, and what evidence a reviewer should demand before accepting it.

It combines:

- post-construction class transformation
- attribute-boundary control
- explicit limits around mutability
- a design decision about how much policy should live in one decorator

That makes it the right worked example for this module.

## Review questions for the page

Keep two questions active while reading:

1. what exact mutability surface does this decorator own?
2. what stronger immutability claim must it refuse?

Keep a third question beside them:

3. what first requirement would make this decorator too weak to stay the honest owner?

## The incident

Assume a team wants a small `@frozen` decorator for configuration-style classes.

They want it to:

- allow attributes to be assigned during initialization
- reject later reassignment and deletion
- stay readable to teammates who inspect the class
- avoid reaching for metaclasses

Those are reasonable goals. The mistake would be pretending this now creates deep or
universal immutability.

That sentence is the real incident. The syntax is easy. The hard part is keeping the
class-level claim narrow enough that readers do not confuse "blocks rebinding" with
"makes the object universally immutable."

That is why this page remains useful even if you never ship a decorator like this. It
teaches how to review seductive class claims without letting convenience language outrun
the actual boundary.

## Establish the executable baseline

Run:

```bash
make class-customization-lab-test
make class-customization-lab
```

Keep `labs/class_customization/frozen_surface.py`,
`tests/test_frozen_surface_class_decorator.py`, and the `frozen_surface` evidence packet
together. The source identifies the owner, the tests prove success and failure routes,
and the packet exposes the result to a learner.

## The first design rule: define frozen at the surface

This example uses "frozen" in a deliberately narrow sense:

- instance attributes cannot be reassigned after initialization
- instance attributes cannot be deleted after initialization

This example does not claim:

- deep immutability of nested containers
- protection against every low-level escape hatch
- compile-time enforcement

That boundary keeps the example honest and teachable.

## Non-goals to keep visible

This worked example is intentionally not trying to deliver:

- deep immutability of nested state
- protection against deliberate low-level bypasses
- field-by-field validation semantics
- class-creation-time enforcement
- framework-grade frozen-class infrastructure

If the design needs those guarantees, the decorator has reached the edge of what this
module is trying to teach.

## Step 1: choose a post-construction design

Because the class already exists before the decorator runs, the decorator can install a
small amount of behavior after class creation.

That makes a class decorator a good fit when the rule is:

- opt-in
- uniform across the whole class
- visible in one place

This is exactly the boundary Module 06 is trying to teach.

It also explains why this example belongs before the metaclass material. The policy is
installed after class creation and therefore should be reviewed as post-construction class
customization, not as class-construction control.

## Step 2: allow initialization, then flip the boundary

The decorator needs one moment of flexibility during `__init__`, followed by a stricter
steady state afterward.

One simple design is:

1. wrap `__init__`
2. mark the instance as still initializing before running the original initializer
3. mark initialization as complete afterward
4. reject `__setattr__` and `__delattr__` once initialization succeeds

That keeps the state transition explicit instead of magical.

Use this state-transition table when reviewing the example:

| Moment | What is allowed |
| --- | --- |
| before wrapped `__init__` finishes | initialization assignments may proceed |
| after `_surface_frozen_ready` becomes true | normal rebinding and deletion are rejected |
| inside nested mutable objects already stored on the instance | mutation may still occur unless another owner blocks it |
| if `__init__` raises | no usable instance returns; the decorator makes no post-failure object claim |

## A proof route for the boundary flip

Use this route when you test or explain the implementation:

1. show one assignment during initialization that succeeds
2. show one reassignment after initialization that fails
3. show one deletion after initialization that fails
4. show one nested mutable object that still changes successfully
5. explain why step 4 is part of the intended boundary rather than a bug

## Step 3: keep the interception rules narrow

The `__setattr__` override should reject only the post-initialization mutation boundary.

It should not:

- invent deep copy behavior
- try to freeze class attributes
- claim to secure every internal object graph

If the design needs those guarantees, this decorator is no longer the right owner.

## Read the shipped implementation by owner

`surface_frozen` captures the original `__init__`, `__setattr__`, and `__delattr__`.
It installs three replacement methods and one immutable `FrozenSurfacePolicy`.

| Owner | Responsibility |
| --- | --- |
| wrapped initializer | open initialization, run the original initializer, close only after success |
| installed `__setattr__` | reject ordinary rebinding after the boundary closes |
| installed `__delattr__` | reject ordinary deletion after the boundary closes |
| `FrozenSurfacePolicy` | publish what the decorator blocks and what it deliberately allows |

During initialization, assignments still pass through the original `__setattr__`. A
focused test records that behavior. Policy installation must not erase an existing
initialization rule merely because the decorator adds a later boundary.

The decorator refuses instances without `__dict__` rather than half-supporting slots.
That is a limitation of this teaching implementation, not a limitation of frozen
classes generally.

## What this implementation proves and what it does not

Use the code block as evidence, not as marketing:

| Claim | Supported by this implementation? | Why |
| --- | --- | --- |
| it installs the rule after class creation | yes | the decorator modifies the finished class object |
| it allows initialization before freezing the surface | yes | wrapped `__init__` flips `_surface_frozen_ready` only after successful setup |
| it blocks later rebinding and deletion of top-level instance attributes | yes | `__setattr__` and `__delattr__` reject after the ready flag is set |
| it makes nested lists, dicts, or other contained objects immutable | no | stored objects retain their own mutation behavior |
| it prevents every low-level escape hatch | no | the example is not trying to secure the entire object model |
| it requires a metaclass | no | the rule is installed after class creation and does not depend on namespace control |
| it supports slotted-only instances | no | decoration refuses them clearly |
| subclasses cannot weaken the rule | no | an overriding `__setattr__` can replace the boundary |

Read that table as a review contract, not as decoration. If a future version of the
decorator wants to promise more, both the implementation and the proof burden have to
grow.

## Why this version shows the right boundary

This decorator is useful because it keeps every important choice visible:

- the class is transformed after creation
- initialization still happens through the original constructor
- the mutation boundary is enforced through normal attribute hooks
- the policy is small enough to review in one pass

That is the kind of post-construction customization Module 06 is aiming for.

## A review card for adapting the example

If you change this decorator, answer these before you trust the new version:

| Adaptation question | Why it matters |
| --- | --- |
| does the meaning of "frozen" stay surface-level or expand? | the review claim changes immediately if the meaning widens |
| is the initialization window still explicit? | hidden state transitions weaken reviewability |
| do subclass overrides preserve or bypass the boundary? | inheritance is the first place the policy often drifts |
| does any new helper now own deeper mutability or validation policy? | the decorator may no longer be the only meaningful owner |

## Failure surfaces a reviewer should inspect

Even this bounded design has pressure points:

| Failure surface | Why it matters |
| --- | --- |
| `_surface_frozen_ready` state transitions | the rule is only as clear as the moment the boundary flips |
| nested mutable objects | readers may overclaim deep immutability if this stays implicit |
| inheritance and subclass overrides | later classes may weaken or bypass the surface rule |
| low-level attribute bypasses | the pattern is educational surface control, not a security mechanism |
| inflated naming in docs or comments | truthful code can still become dishonest through language |

## Where the boundary shows up immediately

This decorator is intentionally surface-level.

For example:

```python
@surface_frozen
class Settings:
    def __init__(self, tags):
        self.tags = tags


settings = Settings(["core", "api"])
settings.tags.append("admin")  # still allowed
```

The list object inside `tags` is still mutable. The decorator blocks rebinding
`settings.tags`, but it does not freeze the list itself.

That is not a bug in the example. That is the exact boundary.

This example therefore teaches a precise language habit: say "surface immutability" when
you mean blocked rebinding, and reserve broader language for broader owners.

## Subclass pressure to keep visible

Subclassing is the first place this design often gets weakened or overclaimed:

- a subclass may add helper methods that mutate nested state indirectly
- a subclass may override `__setattr__` or `__delattr__` and erase the boundary
- a subclass may change initialization order and make `_surface_frozen_ready` harder to reason about

That does not make the example bad. It means the example is honest about staying a minimal
class-level tool rather than pretending to be a full immutability framework.

The suite proves this weakness directly: `MutableDeliveryConfig` overrides
`__setattr__` and successfully rebinds `endpoint`. A limitation backed by a test is
harder to erase with optimistic prose.

## Why this does not need a metaclass

Nothing here depends on class-creation-time namespace control.

The decorator works because the needed policy can still be installed after the class
already exists:

- wrap the initializer
- override attribute mutation hooks
- return the modified class

That is strong evidence that a metaclass would be unnecessary escalation for this case.

## Proof ledger

| Claim | Focused test |
| --- | --- |
| initialization succeeds before mutation closes | `test_initialization_succeeds_before_rebinding_and_deletion_are_blocked` |
| nested mutation and low-level bypass remain possible | `test_policy_names_mutability_and_bypass_limits` |
| original attribute policy runs during initialization | `test_original_attribute_policy_still_runs_during_initialization` |
| constructor signature and provenance survive wrapping | `test_wrapped_initializer_preserves_signature_and_provenance` |
| slotted-only classes are refused | `test_slotted_classes_are_refused_instead_of_half_supported` |
| subclass override can replace the boundary | `test_subclass_can_replace_the_boundary_as_the_policy_warns` |

Together these tests define the teaching product. They do not prove security, deep
immutability, hash safety, thread safety, or sealed inheritance.

## Evidence packet to leave behind

If you adapt this example, leave behind a packet another reviewer can inspect quickly:

- the exact meaning of "frozen" in the codebase
- the point in time when mutation becomes blocked
- one example of mutation that is still allowed
- one sentence explaining why a metaclass is unnecessary here
- one sentence naming the first condition that would justify a stronger owner

Add one more packet note:

- one concrete adaptation you would reject because it widens the claim faster than the evidence

## Questions to ask during review

When you see a frozen-class pattern like this, review it with these questions:

- does the decorator define frozen narrowly enough to stay truthful?
- is initialization still allowed explicitly before the object becomes frozen?
- are reassignment and deletion both covered?
- is the design pretending to guarantee deep immutability when it only controls the instance surface?
- would a plain explicit class be clearer if only one class needs this behavior?
- what subclass or nested-state case would be the first place this pattern becomes too weak?

## What this example makes clear about Module 06

This worked example ties the module together:

- class decorators can install post-construction behavior
- dataclass-style convenience is different from immutability policy
- attribute control lives at the `__setattr__` and `__delattr__` boundary
- the smallest honest owner matters more than using the most powerful tool

That is the durable takeaway. The decorator is here as a clean case study in class
customization boundaries, not as a universal immutability recipe.

## Exit check for this page

Before leaving the worked example, make sure you can do all of these:

- explain why the rule belongs to a class decorator rather than a metaclass
- define frozen narrowly enough to stay honest
- name one mutation the decorator blocks and one it still allows
- say what missing requirement would justify a stronger owner than this pattern
- locate the focused test for every frozen-surface claim you make

## Continue through Module 06

- Previous: [Class Customization Boundaries](class-customization-boundaries.md)
- Next: [Exercises](exercises.md)
- Reference: [Exercise Answers](exercise-answers.md)
- Terms: [Glossary](glossary.md)
