# Fixtures, Builders, and Test Data Ownership

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Testing Contracts Verification Depth"]
  page["Fixtures, Builders, and Test Data Ownership"]
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

Read the first diagram as a placement map: this page is one concept inside its parent
module, not a detached essay, and the capstone is the pressure test for whether the
idea holds. Read the second diagram as the working rhythm for the page: name the
problem, study the example, identify the boundary, then carry one review question
forward.

## Why this lesson matters

Bad test data design makes good tests unreadable.

Students often blame a test for being hard to follow when the real problem is that the
data setup:

- hides which values matter
- reuses giant fixtures with accidental defaults
- spreads meaning across distant helper files
- makes invalid combinations too easy or valid combinations too magical

If the setup hides the point of the test, the proof becomes weaker even when the
assertions are correct.

## Test data should have a visible owner

The core question is:

- who is responsible for making this test input understandable?

Usually the answer should be:

- the test itself, when only a few values matter
- a small local builder, when construction is verbose but the relevant overrides should stay visible
- a narrowly shared fixture, when many tests truly depend on the same stable setup

Ownership means the reader can tell where the important shape of the data came from.

## Shared fixtures solve one problem and create another

Large shared fixtures make tests shorter.

They also create a hidden cost:

- the reader no longer knows which fields are essential
- the fixture may smuggle in accidental invariants
- changing one default can break dozens of unrelated tests

That does not mean shared fixtures are always wrong. It means they should be treated as
owned abstractions, not free convenience.

## Builders are useful when construction is meaningful but repetitive

Builders help when domain objects need many values before they become valid.

A good builder usually:

- provides honest defaults
- exposes only the variations tests commonly need
- makes invalid combinations explicit when a test wants them
- stays thin enough that readers can still imagine the resulting object

A bad builder becomes a second object model with:

- inheritance layers
- hidden mutation
- surprising defaults
- special cases nobody can explain quickly

The builder should reduce incidental setup cost, not add a new system to debug.

## Keep relevant values close to the assertion

One strong review rule is:

- if a value matters to the claim, let the reader see it nearby

For example, if a test is proving expiry behavior, the relevant timestamps should not be
buried behind three fixture calls and two helper modules. The test should show the times
or the named builder overrides clearly.

This is not about avoiding helpers entirely. It is about keeping semantic pressure near
the surface being proved.

## Builders should preserve domain language

If the model speaks in terms such as:

- active incident
- acknowledged rule
- expired lease
- repository conflict

then builders and fixtures should reflect that vocabulary.

Helpers named after raw storage fields or legacy constructor noise make tests harder to
review because they force the reader to translate setup back into domain meaning.

## A worked example

Suppose an incident aggregate requires:

- identifier
- severity
- opened timestamp
- current state
- version

A weak test helper might construct a giant default incident and let every test mutate it
after creation.

A stronger approach could be:

- a small builder with honest defaults for a normal open incident
- explicit methods or overrides such as `with_severity("critical")` or `closed_at(...)`
- local values in the test for the fields that explain the proof

Then a reader can see:

- what kind of incident the test started from
- what was intentionally varied
- why the assertion should hold

## When local setup is better than reuse

Not every repeated shape deserves a shared helper.

Prefer local setup when:

- the object is simple enough to read directly
- the test is teaching a subtle rule and needs setup to stay explicit
- the values are unlikely to recur meaningfully elsewhere

Excessive reuse can make the suite smaller while making each proof harder to audit.

## Common mistakes

- building giant reusable fixtures that hide which inputs matter
- creating builders with more complexity than the domain objects they build
- mutating shared fixture state across tests
- keeping important semantic values far from the assertion they explain
- using setup helpers that speak storage language instead of domain language

## Review checklist

| Question | Good sign |
| --- | --- |
| can the reader tell which test inputs matter without chasing many helpers? | yes |
| do builders expose meaningful overrides instead of hidden magic? | yes |
| are shared fixtures small and honestly scoped? | yes |
| does test setup reinforce domain language? | yes |

## Capstone connection

Use the capstone suite to ask:

- which fixtures currently hide lifecycle or timing details that matter to the proof?
- where would a small builder improve readability more than another shared fixture?
- which helpers should be narrowed because they are now carrying too many unrelated defaults?

This is how test data setup becomes part of proof quality rather than invisible noise.

## Exit check

Leave this lesson only when you can do all of these:

- explain what test data ownership means in practice
- identify one case where a builder is better than a giant shared fixture
- rewrite one capstone setup so the important values are visible near the assertion
