# Mechanism Selection, Review Gates, and Escalation Boundaries

The earlier pages in this module each protect one danger zone. This page turns those
lessons into a repeatable approval standard.

That matters because good governance is not just knowing that a mechanism is risky. It is
knowing what should be chosen instead, and what evidence earns an escalation.

## The sentence to keep

Choose the lowest-power mechanism that solves the problem, and only escalate when the
higher-power tool owns something the lower-power tools cannot own honestly.

That sentence is the review gate for the whole course.

## The runtime power ladder is about blast radius

The ladder in this course is not about prestige. It is about how widely a mechanism can
change runtime behavior.

From lower power to higher power:

1. explicit code and ordinary objects
2. wrappers and decorators
3. descriptors and attribute-level control
4. metaclasses and class-creation hooks
5. import hooks, AST transforms, and dynamic execution with global consequences

Each step upward raises the review cost because the mechanism becomes harder to see,
harder to reverse, or harder to scope.

## What escalation should sound like

Weak escalation language:

- "this is more elegant"
- "this avoids boilerplate"
- "the runtime can enforce it automatically"

Stronger escalation language:

- "this must happen during class creation before subclasses exist"
- "this behavior belongs to one attribute access point rather than a method"
- "this instrumentation must see imports as they happen"
- "this trusted expression language cannot be modeled as simple data without losing the needed semantics"

The difference is ownership, not enthusiasm.

## Plugin systems make the ladder concrete

Plugin architectures are a good governance test because several mechanisms can plausibly
solve them.

Default choice:

- decorator-based registration

Escalation case:

- metaclass-based registration when a class hierarchy must enforce registration for every
  concrete subclass with no opt-out

Usually reject:

- import-hook-based plugin discovery for ordinary application behavior

The point is not that decorators are always morally pure. The point is that they usually
keep registration more explicit, local, and testable.

## A small selection table

| Need | First honest choice | Why it stays governable |
| --- | --- | --- |
| explicit opt-in registration | decorator | definition-time change stays visible at one symbol |
| per-field validation or conversion | descriptor or property | ownership sits on one attribute path |
| hierarchy-wide class-creation rule | metaclass | the hook matches the timing of the invariant |
| process-wide import instrumentation | import hook | the problem is already process-wide |
| user-controlled expressions | data or out-of-process execution | trust boundary remains honest |

Selection is clearer when the table names the owner, not just the mechanism.

## Review gates for escalation

Before approving a higher-power design, reviewers should be able to point to all of these:

- the lower-power alternative that was considered first
- the specific ownership reason that made it insufficient
- the observability plan
- the reset, disable, or rollback path
- the test surface for failure cases
- the performance story if the mechanism sits on a hot path

If any one of those is missing, the escalation case is not finished.

## Lower-power rejection is a sign of strength

One of the best outcomes in Module 10 is a clean rejection.

Examples:

- reject `exec` because configuration data plus explicit dispatch is clearer
- reject a metaclass because a decorator or helper registers classes honestly enough
- reject a protocol runtime check because unit tests and a small adapter do the job more clearly
- reject an import hook because explicit imports keep startup behavior visible

The course is doing its job when the review answer is often "do less."

## Approval language should stay operational

When a design is approved, the explanation should mention operational facts:

- when the mechanism runs
- what it can mutate
- how it is observed
- how it is reset or disabled
- what evidence proves it stays deterministic

If the approval note only says the abstraction is clever or elegant, governance has not
really happened.

## A drop-in review checklist

Use this when one of the course mechanisms appears in design review:

```text
Runtime governance checklist

□ Lowest-power mechanism considered first
□ Escalation reason tied to ownership, not taste
□ Import-time, class-time, call-time, or attribute-time effects named explicitly
□ Introspection and traceback surfaces preserved
□ Reset, cleanup, or disable path documented
□ Determinism and test isolation addressed
□ Performance evidence supplied for hot paths
□ Security claims stop at the real boundary
```

This is the practical heart of Module 10.

## What this page is really teaching

The lesson is not "always stay at the bottom of the ladder."

The lesson is:

- higher-power tools need stronger ownership arguments
- rejecting escalation is often the most professional decision
- review gates should talk about timing, scope, evidence, and reversibility

That is how the earlier modules become long-term engineering judgment.

## What to practice from this page

Try these before moving on:

1. Take one design that uses a metaclass or import hook and argue for a lower-power replacement.
2. Write one escalation justification that names timing and ownership precisely.
3. Review one plugin design and explain why the chosen mechanism is or is not the lowest-power honest fit.

If those feel ordinary, the module is ready for a worked example that applies all five core
lessons to one reviewable runtime design.

## Continue through Module 10

- Previous: [Import Hooks, AST Transforms, and Tooling Boundaries](import-hooks-ast-transforms-and-tooling-boundaries.md)
- Next: [Worked Example: Reviewing a Plugin Runtime for Observability and Control](worked-example-reviewing-a-plugin-runtime-for-observability-and-control.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
