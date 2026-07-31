# Wrapper Policy Boundaries


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Decorator Design Policies Typing"]
  page["Wrapper Policy Boundaries"]
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

Module 05 needs one explicit decision page, not just more decorator patterns.

All the earlier cores in this module raise the same design pressure:

- factories capture policy
- retries and timeouts govern control flow
- annotation-aware wrappers start enforcing contracts
- caches own state, history, and operational hooks

At some point the right question stops being "how do we write this decorator?" and becomes:

> should this still be a decorator at all?

That is not an anti-decorator slogan. It is a stewardship question. The course needs you
to see when the call boundary is still the right owner and when it has become a hiding
place for broader runtime policy.

## The sentence to keep

When a wrapper keeps growing, ask:

> what part of this behavior still belongs at the callable boundary, and what part would be
> clearer as an explicit object, field, or service?

That is the core judgment Module 05 is trying to teach.

Add one more question beside it:

> if this wrapper disappeared tomorrow, what explicit owner would need to exist so the policy would still make sense?

## Decorators are strongest at the callable boundary

A decorator is the most natural tool when the concern is truly about a call boundary:

- tracing one call
- timing one call
- adding a narrow warning
- preserving or slightly adapting one callable contract

Those all stay close to the original idea of function transformation.

They also share an important limit: the wrapper is still mainly speaking about one call,
not coordinating a larger subsystem.

## Compare the two shipped policies

The Module 05 lab intentionally keeps two policies in decorators:

| Wrapper | Why the boundary remains defensible | Pressure that would move it out |
| --- | --- | --- |
| `retry` | one callable, immutable finite policy, named exception types, no shared cross-call state | shared budgets, circuit state, metrics, dynamic reconfiguration, or coordination across deliveries |
| `validated` | one callable, small supported hint subset, explicit refusal, no coercion or schema registry | nested structures, cross-field rules, rich errors, coercion, or reusable schemas |

This is a provisional design judgment, not proof that decorators are always the right
owner for retry or validation. The important feature is that the exit conditions are
named before the wrappers grow.

## Decorators get weaker as policy widens

The more a wrapper starts owning:

- cross-call state
- multiple retry and timeout knobs
- validation rules with broad schema meaning
- cache lifetimes and reset policy
- rate-limit coordination

the more it starts competing with explicit runtime components.

That does not make the decorator automatically wrong. It does mean the burden of proof is
higher.

Use this escalation ladder when the answer feels uncertain:

1. is the concern still about one call boundary?
2. does the wrapper now own state or policy across calls?
3. do reviewers need independent inspection, reset, or configuration surfaces?
4. would a named object or service explain ownership more honestly?

If you are answering "yes" by step 3 or 4, the decorator is already under structural
pressure.

## One picture of the escalation boundary

```text
Thin callable concern
  -> decorator is often a good fit

Growing policy with state, coordination, or configuration
  -> decorator may still work, but explicit objects or services become stronger candidates
```

This is a power-boundary judgment, not a syntax preference.

## A decision table for likely owners

Use this table when a wrapper starts carrying more than one policy concern:

| If the behavior mainly... | Likely better owner |
| --- | --- |
| labels or observes one call narrowly | decorator |
| coordinates retries, backoff, or limits across many call sites | explicit policy object or client wrapper |
| owns shared mutable state that operators must inspect | explicit service or component |
| interprets rich validation metadata | validator object or framework boundary |
| depends heavily on call ordering with other wrappers | clearer composition owner than another hidden layer |

## Write a boundary record

When the answer is not obvious, write five lines:

```text
Policy:
Current owner:
Evidence surface:
Why this owner still fits:
Exit condition:
```

For the lab retry wrapper:

```text
Policy: retry TransientDeliveryError at most three total attempts with 0.1s then 0.2s waits
Current owner: the callable wrapper produced by retry
Evidence surface: __retry_policy__, deterministic event packet, focused tests
Why this owner still fits: the rule is local, finite, immutable, and has no shared lifecycle
Exit condition: retries must coordinate state or budgets across more than one callable
```

This record is deliberately short, but it cannot hide behind "simple." It names the
owner, the proof, and the point at which the decision expires.

## Warning signs that a decorator may be the wrong owner

Strong warning signs include:

- too many configuration arguments
- complicated ordering interactions with other decorators
- state that tests need to reset in non-obvious ways
- behavior that spans more than one callable cleanly
- policies that would be easier to inspect if they were explicit objects

At that point, the wrapper may be hiding design complexity rather than containing it.

That sentence is the page's central warning: a compact wrapper can reduce visual clutter
while increasing ownership confusion.

## Explicit objects often improve visibility

Sometimes the better design is:

- a retry policy object
- a validator object
- a cache service
- a limiter or scheduler component

Why these can be better:

- state becomes first-class instead of hidden in closures
- control surfaces become explicit
- composition is easier to inspect
- test reset and configuration become less magical

This is exactly the kind of downward-pressure decision to practice here.

It also improves teaching quality. A learner can point at a retry object, validator
component, or cache service and say what it owns. A layered decorator stack makes that
sentence harder.

## Decorators and explicit objects can still cooperate

The design does not need to be decorator or object in a pure sense.

A healthier pattern is often:

- decorator at the callable boundary
- explicit object owning the heavier policy

That way the wrapper stays thin and the wider system still gets an obvious owner for state
and coordination.

This is often the most honest compromise once policy grows.

In review language, that often sounds like:

- keep the boundary wrapper
- move the real policy to something with a visible name, state surface, and lifecycle

For example, a boundary decorator could delegate to:

```python
class DeliveryPolicy:
    def run(self, operation, /, *args, **kwargs):
        ...


def governed_by(policy: DeliveryPolicy):
    def decorate(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            return policy.run(function, *args, **kwargs)
        return wrapped
    return decorate
```

The decorator still marks the call boundary. `DeliveryPolicy` becomes the explicit
owner of shared state, lifecycle, inspection, and coordination. This is pseudocode:
Module 05 does not need a second policy framework; the ownership split is the point.

## Typing pressure is another warning sign

If a decorator starts trying to:

- interpret complex annotations deeply
- enforce schema-like rules
- carry rich validation metadata

then the design may already be drifting toward a dedicated validation layer.

That is one reason the worked example stays partial on purpose.

It is also why "we can keep adding one more decorator feature" is weak design language
here. Once the wrapper starts interpreting rich metadata deeply, the owner story usually
wants a new shape.

The capstone already models a lower-power alternative for configuration validation:
descriptor-backed fields own per-attribute rules. Module 05's action validation stays
at the call boundary because it reasons about bound action arguments. Later descriptor
modules will explain why assignment-time field invariants belong to a different owner.

## Common overclaims to reject

Reject these sentences when you hear them:

| Overclaim | Better replacement |
| --- | --- |
| "the decorator keeps the design simple" | "the decorator keeps the call surface small, but we still need to judge ownership" |
| "the policy is local enough" | "the policy still needs a named owner and visible control surfaces" |
| "we can always split it out later" | "the cost of a hidden owner is already showing up now" |
| "the object version would be too verbose" | "verbosity is a weaker problem than ambiguous ownership" |

## Failure modes for wrapper ownership

These are the boundary failures to catch before they harden:

| Failure mode | Why it weakens the design | Repair move |
| --- | --- | --- |
| stacking more decorators to avoid naming a real owner | policy gets harder to inspect and reason about | introduce the explicit owner now |
| keeping shared state in closures because it feels compact | stewardship and reset routes stay hidden | move state to a first-class object or component |
| calling the design simple because the surface is short | short syntax hides broad semantics | judge by owned policy, not line count |
| letting order interactions carry design meaning silently | the policy becomes distributed across layers | reduce the stack or move coordination into one clearer owner |

## Review one proposed stack

Suppose an incident action is decorated as:

```python
@cached(maxsize=256)
@retry(exceptions=(DeliveryError,), max_attempts=3)
@validated(on_mismatch="warn")
@action("Deliver an incident.")
def deliver(...):
    ...
```

A code review must resolve at least these questions:

- does a cache hit bypass validation, retry, and action-history recording?
- does warning mode let an incompatible value reach delivery?
- are failed deliveries cached?
- does retry produce one action-history record or one per attempt?
- what cache key distinguishes operationally different calls?

Reordering the decorators changes those answers. That is evidence that composition
itself has become a policy owner. Prefer an explicit orchestration component before
letting stack order become an undocumented workflow language.

## Smallest honest review route

Run `make decorator-policy-lab`, then write one boundary record for each packet. Your
record passes when another learner can find the owner and its proof without reading the
implementation twice. There is no automated test for the final ownership judgment;
the executable evidence constrains the facts on which the judgment is based.

## Review rules for policy boundaries

When reviewing a policy-heavy wrapper, keep these questions close:

- is the concern still truly about one callable boundary?
- would the state and configuration be clearer as a first-class object or service?
- is decorator order now carrying too much hidden semantic weight?
- does the wrapper expose enough control and inspection surfaces for the policy it owns?
- which lower-power or more explicit design almost worked, and why was it rejected?
- can another reviewer point to the real policy owner in one sentence?

## Exit check for this page

Before moving on, make sure you can do all of these:

- name one case where the decorator should stay the owner
- name one case where an explicit object should take over
- explain why a short call surface can still hide a broad ownership problem
- describe one sentence that would reveal the real owner more honestly than another decorator layer

## What to practice from this page

Try these before moving on:

1. Write boundary records for `retry`, `validated`, and the teaching cache.
2. Take one retry or cache decorator and sketch the equivalent explicit object design.
3. Predict the behavior of the four-decorator stack above, then explain why the stack
   should not become the course's application architecture.
4. Write one review note that rejects a wrapper because its policy surface has become
   too broad and names the replacement owner.

If those feel ordinary, the worked example can combine the module's policy and typing
pressures inside one deliberately partial validator.

## Continue through Module 05

- Previous: [Cache Policy and lru_cache Behavior](cache-policy-and-lru-cache-behavior.md)
- Next: [Worked Example: Building a Partial `@validated` Decorator](worked-example-building-a-partial-validated-decorator.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
