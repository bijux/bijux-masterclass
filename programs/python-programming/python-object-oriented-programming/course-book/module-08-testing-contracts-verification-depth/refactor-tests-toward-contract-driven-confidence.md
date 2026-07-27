# Refactor: Tests toward Contract-Driven Confidence

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Testing Contracts Verification Depth"]
  page["Refactor: Tests toward Contract-Driven Confidence"]
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

## Why this refactor matters

Many weak test suites are not missing effort. They are missing structure.

Typical symptoms:

- behavior tests pin helpers instead of domain promises
- lifecycle objects are tested one method at a time instead of through histories
- repositories have custom tests per backend but no shared contract
- integration tests are either absent or bloated
- snapshots freeze noise

The result is familiar: many green checks, thin confidence.

This refactor page shows how to reshape a suite so each layer proves a real design claim
and the whole system gains explainable coverage instead of accumulated testing weight.

## Start by naming the promises worth defending

Before moving tests around, identify the design truths that matter most.

For the monitoring capstone, examples might include:

- an incident lifecycle cannot move through invalid transitions
- repository substitutes preserve the same semantic behavior
- runtime workflows save, publish, and expose public results consistently
- operator-facing output stays reviewably stable

If the suite cannot be explained in terms of these promises, it is probably organized by
convenience instead of proof value.

## Step 1: strip local tests back to behavior claims

Look for tests that mostly defend:

- helper calls
- private method choreography
- temporary collaborator structure
- mocks used as implementation surveillance

Refactor those toward behavior-first tests that answer:

- what command happened?
- what visible outcome matters?
- what invariant or error is being defended?

This reduces noise and makes the local layer readable again.

## Step 2: add lifecycle proof where history matters

Once local behavior tests are cleaner, find the places where one-call coverage still
misses the real risk.

Typical candidates:

- aggregates with typestate
- repeated commands
- event-emitting transitions
- derived values that drift across several changes

Add sequence-focused tests or state-machine style tests so the suite proves histories,
not just isolated calls.

## Step 3: extract shared contract suites for substitutes

If multiple repositories, adapters, or integration boundaries claim compatibility, stop
testing them with separate hand-written suites only.

Instead:

1. define the semantic contract once
2. run the same suite against every claimed substitute
3. split the interface if honest capability differences appear

This step often reveals that a fake or in-memory substitute has been over-trusted for a
long time.

## Step 4: improve test data ownership before adding more tests

Weak setup design will undermine every higher layer.

Before expanding the suite, tighten:

- oversized fixtures
- hidden defaults
- builders that conceal important values
- helpers that speak implementation language instead of domain language

The point is simple: a reviewer should be able to see what matters in each proof route
without tracing setup through half the repository.

## Step 5: choose generated proof where breadth matters

Not every invariant deserves property-based testing, but some claims become clearer once
you stop pretending a few examples are enough.

Look for:

- round-trip guarantees
- ordering laws
- semantic equality rules
- wide transition spaces

Add properties there, especially when shrunk counterexamples would teach something the
team is currently missing.

## Step 6: place workflow proof at the right integration layer

After local, stateful, and contract proof is clearer, look at what still spans layers.

Integration tests should prove things like:

- load, mutate, save, and publish flows
- repository plus aggregate round-trips
- adapter translation under realistic boundary use
- runtime coordination that lower layers cannot honestly see

Do not use integration tests as a substitute for missing lower-layer clarity. Use them
for composition risk only.

## Step 7: review public-output approvals as contracts

If the suite contains snapshots or golden files, inspect them with one question:

- is this artifact truly a public or reviewer-facing contract?

Keep and improve the ones that protect real representations.
Delete or narrow the ones that only freeze internal noise.

That turns approval testing into a review tool instead of a maintenance tax.

## A worked refactor route

Imagine the capstone currently has:

- many unit tests with heavy mocks
- a few broad end-to-end checks
- no shared repository contracts
- hidden fixture defaults

An ordered refactor route could be:

1. rewrite the most brittle mock-driven tests into behavior-first domain tests
2. add sequence tests for incident lifecycle paths
3. extract one repository contract suite and run it against in-memory and durable implementations
4. replace hidden fixture sprawl with a small set of readable builders
5. add one property for a meaningful round-trip or equality guarantee
6. narrow integration tests so each one proves a specific composed workflow
7. review snapshot artifacts and keep only the ones guarding stable public output

This route produces a suite with distinct evidence layers instead of a pile of
historical habits.

## Common mistakes

- adding more tests before fixing what the current tests are actually proving
- keeping brittle mocks because changing them feels expensive
- piling more integration tests on top of weak local proof
- adding properties or snapshots as fashion rather than because the claim demands them
- reorganizing tests by directory only, without changing the proof structure

## Review checklist

| Question | Good sign |
| --- | --- |
| can each major design claim be paired with a first-failing suite? | yes |
| has brittle implementation surveillance been replaced with behavior proof where possible? | yes |
| are shared substitutes governed by shared contracts? | yes |
| do higher layers prove composition and public-boundary risk rather than local detail? | yes |

## Capstone connection

Use this refactor route to review the capstone today.

Ask:

- which tests still mostly defend choreography?
- which lifecycle rules need sequence proof?
- which repositories or adapters need a shared contract suite next?
- which public outputs deserve approval-style review and which do not?

Those questions turn Module 08 into a concrete suite redesign plan.

## Exit check

Leave this refactor page only when you can do all of these:

- describe an ordered path for turning a brittle suite into a contract-driven one
- name one capstone layer that is over-tested and one that is under-proved
- explain why adding more tests without restructuring proof routes can still leave confidence weak
