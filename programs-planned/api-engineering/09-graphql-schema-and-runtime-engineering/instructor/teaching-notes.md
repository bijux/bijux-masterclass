# Instructor teaching notes

The course should remain centered on three questions:

1. What client capability does the graph expose?
2. Which service owns each fact or command?
3. Which evidence proves the runtime preserves that ownership under selection,
   failure, and evolution?

Do not allow the teaching to collapse into SDL memorization or framework tours.
A resolver is not good because it is short; it is good when its authority,
demand, failure behavior, and source-call pattern are explicit. Require learners
to draw the execution path for every substantial field.

Use the two language tracks comparatively. A learner should implement one track
fully and review the other for semantic parity. Do not demand artificial folder,
class, or exception symmetry. Compare observable invariants: operation identity,
authorization timing, batch counts, cursor population, mutation replay, error
paths, and release decisions.

The most important misconceptions to surface are:

- GraphQL does not eliminate source-service boundaries.
- A flexible query language does not grant unlimited computation.
- DataLoader does not fix every N+1 problem and must be request-scoped.
- `null` is part of the contract, not a generic failure value.
- HTTP success does not mean every selected field succeeded.
- A schema that validates can still break active clients or operational budgets.
- Subscriptions do not define a complete delivery protocol by themselves.
- Federation is an architecture option, not the inevitable endpoint of GraphQL.

Each lab should begin with a prediction. The learner states what source calls,
response data, errors, and durable effects should occur before executing the
experiment. Afterward they compare the result with the prediction and identify
which model was wrong. This makes the laboratory diagnostic rather than
procedural.

During the final defense, interrupt vague explanations with concrete questions:
Which field coordinate? Which tenant? Which operation hash? Which source owner?
Which call count? Which exact error path? Which release gate? The course is
complete only when the learner can connect schema language to runtime behavior
and operational evidence without hiding behind a framework.
