# Wrapper Policy Boundaries

Module 05 needs one explicit decision page, not just more decorator patterns.

All the earlier cores in this module raise the same design pressure:

- factories capture policy
- retries and timeouts govern control flow
- annotation-aware wrappers start enforcing contracts
- caches own state, history, and operational hooks

At some point the right question stops being "how do we write this decorator?" and becomes:

> should this still be a decorator at all?

## The sentence to keep

When a wrapper keeps growing, ask:

> what part of this behavior still belongs at the callable boundary, and what part would be
> clearer as an explicit object, field, or service?

That is the core judgment Module 05 is trying to teach.

## Decorators are strongest at the callable boundary

A decorator is the most natural tool when the concern is truly about a call boundary:

- tracing one call
- timing one call
- adding a narrow warning
- preserving or slightly adapting one callable contract

Those all stay close to the original idea of function transformation.

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

## One picture of the escalation boundary

```text
Thin callable concern
  -> decorator is often a good fit

Growing policy with state, coordination, or configuration
  -> decorator may still work, but explicit objects or services become stronger candidates
```

This is a power-boundary judgment, not a syntax preference.

## Warning signs that a decorator may be the wrong owner

Strong warning signs include:

- too many configuration arguments
- complicated ordering interactions with other decorators
- state that tests need to reset in non-obvious ways
- behavior that spans more than one callable cleanly
- policies that would be easier to inspect if they were explicit objects

At that point, the wrapper may be hiding design complexity rather than containing it.

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

## Decorators and explicit objects can still cooperate

The design does not need to be decorator or object in a pure sense.

A healthier pattern is often:

- decorator at the callable boundary
- explicit object owning the heavier policy

That way the wrapper stays thin and the wider system still gets an obvious owner for state
and coordination.

This is often the most honest compromise once policy grows.

## Typing pressure is another warning sign

If a decorator starts trying to:

- interpret complex annotations deeply
- enforce schema-like rules
- carry rich validation metadata

then the design may already be drifting toward a dedicated validation layer.

That is one reason the worked example stays partial on purpose.

## Review rules for policy boundaries

When reviewing a policy-heavy wrapper, keep these questions close:

- is the concern still truly about one callable boundary?
- would the state and configuration be clearer as a first-class object or service?
- is decorator order now carrying too much hidden semantic weight?
- does the wrapper expose enough control and inspection surfaces for the policy it owns?
- which lower-power or more explicit design almost worked, and why was it rejected?

## What to practice from this page

Try these before moving on:

1. Take one retry or cache decorator and sketch the equivalent explicit object design.
2. Name one case where a decorator should stay and one where policy should move out.
3. Write one review note that rejects a wrapper because its policy surface has become too broad.

If those feel ordinary, the worked example can combine the module's policy and typing
pressures inside one deliberately partial validator.

## Continue through Module 05

- Previous: [Cache Policy and lru_cache Behavior](cache-policy-and-lru-cache-behavior.md)
- Next: [Worked Example: Building a Partial `@validated` Decorator](worked-example-building-a-partial-validated-decorator.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
