# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Decorator Design Policies Typing"]
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
collect more decorator patterns. The goal is to make policy ownership, typing limits, and
wrapper honesty explicit.

Each exercise asks for three things:

- the policy or contract you are trying to enforce
- the wrapper or explicit boundary you chose
- the reason that choice is honest enough for the problem

Treat the ten exercises as one full lab day on decorator policy and typing boundaries.

Do them in order:

- Exercises 1-3 establish factory capture, resilience policy, and narrow runtime validation
- Exercises 4-6 separate cache policy, overloaded decorators, and partial validator limits
- Exercises 7-8 extend that discipline into escalation boundaries and explicit policy owners
- Exercises 9-10 package the whole module into a reviewable decorator-governance packet

Keep one policy-boundary table while you work:

| Policy or contract | Wrapper or owner | What it really controls | What it refuses to claim | Review judgment |
| --- | --- | --- | --- | --- |

## Exercise 1: Build one decorator factory with real configuration

Write a parameterized decorator and apply it twice with different configuration.

What to hand in:

- the factory implementation
- two differently configured uses
- one explanation of what was captured at definition time and what runs on each call

## Exercise 2: Review one resilience wrapper

Implement or inspect a retry, timeout, or rate-limit decorator.

What to hand in:

- the rule it enforces at the call boundary
- one concrete control-flow or failure behavior it changes
- one sentence explaining why this is policy rather than a thin transformation

## Exercise 3: Validate one narrow hint subset

Build a tiny annotation-aware validator for a supported subset of hints.

What to hand in:

- the supported hint subset
- one call that passes and one that fails
- one example of a hint surface you explicitly refuse to support

## Exercise 4: Inspect cache policy instead of only cache speed

Use `functools.lru_cache` or a bounded cache wrapper.

What to hand in:

- the key or typed-mode behavior you are relying on
- one inspection or reset hook such as `cache_info()` or `cache_clear()`
- one explanation of why cache policy is more than "just performance"

## Exercise 5: Reject one decorator that grew too large

Take a wrapper idea that is carrying too much policy and redesign it mentally.

What to hand in:

- the overloaded decorator idea
- the explicit object, service, or later-course mechanism you would move it to
- one explanation of why that new owner is easier to review

## Exercise 6: Review a partial validator honestly

Use the worked example pattern on `@validated` or a similar runtime checker.

What to hand in:

- the exact claim the validator is allowed to make
- one unsupported typing feature it must reject or ignore
- one explanation of why warning mode is not the same as safety

## Midday self-check

Before moving into the final four exercises, make sure you can already answer these
questions clearly:

- when decorator capture stays narrow and when it turns into hidden policy
- why resilience wrappers and caches need operational review instead of only syntax review
- what a partial runtime validator is allowed to claim without overstating typing support
- when a decorator should give up ownership to an explicit object or service

If you cannot answer those four questions in plain language, return to Exercises 1-6 and
make the policy owner, runtime boundary, and unsupported claim more explicit before
continuing.

## Exercise 7: Separate local convenience from durable policy

Choose one decorator idea that feels convenient in a single file but risky as a long-term
course pattern.

What to hand in:

- the convenient decorator idea
- the exact policy it would silently own over time
- one explanation of why an explicit owner would teach the boundary more honestly

## Exercise 8: Design one explicit policy owner

Take one broad decorator idea and redesign it as an explicit object, helper, or service.

What to hand in:

- the original decorator shape
- the new owner you would introduce
- one review advantage and one learning advantage the explicit owner creates

## Exercise 9: Compare safe claims with overstated claims

Choose one typing-aware or policy-heavy decorator and write both an honest description and
an overstated description.

What to hand in:

- the honest description
- the overstated description
- one explanation of which words make the second version misleading

## Exercise 10: Produce a decorator-governance packet

Assemble:

- one policy-boundary table
- one resilience or cache example with an explicit control surface
- one partial typing example with a named unsupported feature
- one redesign rule for moving overloaded decorator policy into an explicit owner

The packet is strong when another learner can use it to answer:

- what policy the decorator actually owns
- what typing or runtime claim it can support honestly
- when the wrapper boundary should be replaced by a clearer owner

## Mastery standard for this exercise set

Across all six answers, the module wants the same habits:

- you separate thin callable transformation from policy ownership
- you keep runtime typing claims partial and explicit
- you prefer explicit objects or services when decorator policy grows too broad
- you preserve transparency even when wrappers become more powerful

Across all ten answers, add two more habits:

- you distinguish convenient local wrappers from durable course-worthy policy boundaries
- you leave behind a decorator-governance packet another learner could review without guessing

If an answer still sounds like "the decorator just handles it," keep going.

## Continue through Module 05

- Previous: [Worked Example: Building a Partial `@validated` Decorator](worked-example-building-a-partial-validated-decorator.md)
- Next: [Exercise Answers](exercise-answers.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
