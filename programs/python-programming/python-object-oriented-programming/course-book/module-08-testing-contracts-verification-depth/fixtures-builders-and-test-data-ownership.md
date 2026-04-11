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

Read the first diagram as a placement map: this page is one concept inside its parent module, not a detached essay, and the capstone is the pressure test for whether the idea holds. Read the second diagram as the working rhythm for the page: name the problem, study the example, identify the boundary, then carry one review question forward.

## Purpose

Keep test setup readable and intentional by giving test data a clear owner instead of
hiding everything behind sprawling shared fixtures.

## 1. Shared Fixtures Can Hide Too Much

Large reusable fixtures often make tests shorter while making intent harder to see.
Readers cannot tell which inputs matter because everything arrives preassembled.

## 2. Builders Help When Construction Is Verbose

A builder or factory can make setup explicit:

- provide good defaults
- override the fields that matter for the test
- keep invalid combinations difficult unless the test needs them

## 3. Ownership Means Local Clarity

The test that cares about a value should usually declare or customize it nearby. This
reduces invisible coupling between distant fixture files and local expectations.

## 4. Do Not Recreate Production Complexity in Test Helpers

Test helpers should reduce accidental verbosity, not become a second object model with
its own bugs and inheritance tree.

## Practical Guidelines

- Prefer local clarity over maximal fixture reuse.
- Use builders when object construction is verbose but meaningful.
- Keep shared fixtures small and honest about what they provide.
- Review test helpers for hidden invariants or accidental complexity.

## Exercises for Mastery

1. Replace one oversized fixture with a builder or local setup.
2. Audit one builder and remove any fields that tests never need to vary.
3. Identify one test where local data ownership would improve readability.
