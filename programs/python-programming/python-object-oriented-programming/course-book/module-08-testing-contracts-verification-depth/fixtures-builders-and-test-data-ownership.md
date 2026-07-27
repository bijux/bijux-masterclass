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

This lesson is about keeping the important values visible enough that the test still
teaches the claim it is supposed to prove.

Bad test data design makes good assertions unreadable.
The setup becomes the real problem when it:

- hides which values matter
- smuggles in accidental defaults
- spreads semantic meaning across distant helpers
- makes legal and illegal states equally magical

If the setup hides the pressure of the test, the proof weakens even when the assertions
are correct.

## Keep one proof visible

Use one capstone-style claim:

- seat confirmation depends on visible seat count and prior attendee state
- retry safety depends on visible durable progress and prior visible outcome state

Now ask:

Could another maintainer see the values that matter for this claim without reading three
helper modules first?

If the answer is no, the data design is already weakening the proof.

## Test data needs an owner

The core question is:

- who is responsible for making this input understandable?

Usually the answer is:

- the test itself, when only a few values matter
- a small local builder, when construction is verbose but the critical overrides should
  stay visible
- a narrowly shared fixture, when many tests truly depend on the same stable baseline

Ownership matters because it tells the reader where the meaningful shape came from.

## Shared fixtures solve one problem and create another

Large shared fixtures make tests shorter.
They also create hidden cost:

- the reader no longer knows which fields are essential
- one fixture can smuggle in accidental invariants
- changing one default can break unrelated proofs

That does not make shared fixtures always wrong.
It means they should be treated as owned abstractions, not free convenience.

## Builders are useful when construction is repetitive but meaningful

Builders help when an object needs several values before it becomes valid.

A good builder usually:

- provides honest defaults
- exposes the variations tests commonly need
- keeps invalid combinations explicit when a test wants them
- stays thin enough that the resulting object is still imaginable

A bad builder becomes a second object model with:

- hidden mutation
- surprising defaults
- helper-specific jargon
- special cases nobody can explain quickly

The builder should reduce incidental setup cost, not create another system to debug.

## Keep pressure values near the assertion

One strong review rule is simple:

- if a value matters to the claim, let the reader see it nearby

If a test proves expiry behavior, the relevant timestamps should not be buried behind
three fixture layers.
If a test proves retry safety, the visible progress markers should not be hidden behind a
generic "valid issuance" helper.

This is not an argument against helpers.
It is an argument for semantic visibility.

## Builders should speak domain language

If the model speaks in terms such as:

- confirmed attendee
- waitlisted attendee
- issued certificate
- stale repository version

then builders and fixtures should reflect that same vocabulary.

Helpers named after raw storage fields or old constructor noise force readers to
translate setup back into domain meaning before they can understand the proof.

That is wasted effort in a learning-oriented course.

## Worked capstone example

Suppose an enrollment object needs:

- workshop id
- seat limit
- attendee state
- version

A weak helper might:

- build one giant default enrollment
- let every test mutate it afterward

A stronger approach could be:

- a small builder with honest defaults for a normal open enrollment
- explicit overrides such as `with_seat_limit(1)` or `with_confirmed_attendee(...)`
- local variables in the test for the few values that actually explain the proof

That way the reader can see:

- what state the object started from
- what was intentionally varied
- why the assertion should hold

## Prefer local setup when the rule is subtle

Not every repeated shape deserves a shared helper.

Prefer local setup when:

- the object is simple enough to read directly
- the test is teaching a subtle timing or lifecycle rule
- the values are unlikely to recur meaningfully elsewhere

Over-reuse can make the suite smaller while making each individual proof harder to
audit.

## Build a setup packet

Before creating a shared helper or builder, write a short packet:

- what recurring setup pain it removes
- what important values must remain visible
- which tests truly share the same baseline
- what semantic jargon the helper should use

If that packet is weak, the abstraction is probably premature.

## Common failure modes

- giant reusable fixtures that hide which inputs matter
- builders with more complexity than the domain objects they build
- mutating shared fixture state across tests
- keeping important semantic values far from the assertion they explain
- using helpers that speak storage language instead of domain language

## Setup review card

Use this short card when reviewing a fixture or builder:

| Question | What you want to see |
| --- | --- |
| can the reader tell which inputs matter without chasing many helpers? | yes |
| do builders expose meaningful overrides instead of hidden magic? | yes |
| are shared fixtures small and honestly scoped? | yes |
| does the setup reinforce domain language? | yes |

## Capstone connection

Use this page to ask:

- which capstone fixtures currently hide lifecycle or timing details that matter to the
  proof
- where a small builder would improve readability more than another shared fixture
- which helpers should be narrowed because they now carry too many unrelated defaults

That is how test data setup becomes part of proof quality rather than invisible noise.

## Exit check

Leave this lesson only when you can do all of these:

- explain what test data ownership means in practice
- identify one case where a builder is better than a giant shared fixture
- rewrite one capstone setup so the important values are visible near the assertion
