# Fixtures, Builders, and Test Data Ownership

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
