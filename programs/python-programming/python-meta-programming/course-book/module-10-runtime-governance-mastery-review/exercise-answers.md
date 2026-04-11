# Exercise Answers

Use this page after attempting the exercises yourself. The point is not to match one
phrase perfectly. The point is to compare your reasoning against answers that keep trust
boundaries, interface claims, operational control, and escalation policy honest.

## Answer 1: Reject one unsafe dynamic execution idea

Example answer:

- input comes from end users through a configurable formula field
- that input is untrusted, so in-process `eval` is rejected immediately
- the replacement is either a tiny explicit expression language or a separate-process execution model

Good conclusion:

Restricted globals do not solve the real problem. The trust boundary requires a stronger
design boundary than a namespace dictionary.

## Answer 2: Compare one ABC and one protocol honestly

Example answer:

- use an ABC when incomplete implementations should fail at instantiation time
- use a protocol when structural compatibility matters most to static analysis
- only use `@runtime_checkable` when a shallow runtime filter is actually helpful

Good conclusion:

Neither surface proves full behavior. The review story should say exactly whether the
contract is nominal, structural, static, or shallow runtime-only.

## Answer 3: Add a reversal path to one dynamic mechanism

Example answer:

- a registry gains `clear()` or `clear(group)` support
- a patch becomes a context-managed patch that restores the original symbol on exit
- the cleanup prevents test bleed and incident-time confusion about current global state

Good conclusion:

Reversibility is part of the mechanism's design, not an optional improvement for later.

## Answer 4: Review one import hook or AST transform proposal

Example answer:

- the proposal is rejected for application plugin discovery because explicit imports or entry points are clearer
- if the proposal is kept at all, it must be framed as tooling-grade instrumentation
- cleanup, ordering, reload, and location preservation become first-class review questions

Good conclusion:

The strongest import-hook approvals solve global instrumentation problems, not local
application architecture convenience.

## Answer 5: Defend or reject one escalation

Example answer:

- a metaclass is approved only because the invariant belongs to class creation for every concrete subclass
- a decorator or helper is preferred if opt-in registration is enough
- the approval note must mention observability, reset hooks, and performance evidence where relevant

Good conclusion:

Escalation is justified by ownership and timing, not by the desire to reduce visible
boilerplate.

## Answer 6: Review the capstone runtime as Module 10 evidence

Example answer:

- observational surfaces such as `manifest`, `registry`, and `signatures` earn trust before invocation
- the metaclass is justified because deterministic registration belongs to class definition time
- an import-hook-based discovery layer would be rejected as making the runtime less explicit and harder to review

Good conclusion:

The capstone is defensible because it keeps runtime facts inspectable and rejects extra
power it does not need.

## What strong Module 10 answers have in common

Across the whole set, strong answers share the same habits:

- they stop security claims at the real enforceable boundary
- they keep interface promises smaller than the mechanism's aura
- they demand reset, disable, and cleanup paths for dynamic behavior
- they distinguish application design from tooling-grade runtime control
- they justify power with ownership, timing, and proof surfaces

If an answer still sounds impressed by the mechanism itself, revise it until the judgment
sounds operational instead.

## Continue through Module 10

- Previous: [Exercises](exercises.md)
- Next: [Glossary](glossary.md)
- Return: [Overview](index.md)
