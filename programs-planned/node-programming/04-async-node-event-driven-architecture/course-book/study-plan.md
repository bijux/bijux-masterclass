# Ten-Day Study Plan

Each day is a dense module. Use four blocks: model, controlled experiments, independent construction, and capstone transfer. Avoid passive reading for more than two hours at a time.

| Day | Morning model | Midday evidence | Afternoon product | Evening reconstruction |
|---:|---|---|---|---|
| 1 | Draw stack, queues, phases, and partial orders | Predict event-loop investigations | Event Loop Observatory | Explain starvation and a real fairness yield |
| 2 | Draw a promise ownership tree | Compare combinator policies | Owned Promise Nursery | Account for every accepted task |
| 3 | Draw cancellation lineage and deadlines | Classify ambiguous outcomes | Deadline Budget | Defend one remote-commit timeout |
| 4 | Trace synchronous event stacks and reentrancy | Test typed payload and listener failure | Typed Event Hub | Separate authority, command, result, and event |
| 5 | Separate wall, monotonic, logical, and manual time | Drive exact timer boundaries | Deterministic Scheduler | Reconstruct rate-control policy differences |
| 6 | Draw async iterator and queue states | Exercise close, fail, abort, and return | Bounded Async Queue | Explain why pull syntax is not automatic backpressure |
| 7 | Trace async-resource context propagation | Interleave two runs deterministically | Correlation Context | Defend explicit authority versus ambient diagnostics |
| 8 | Draw task tree, capacity, and outcome accounting | Reorder completion and inject failure | Supervised Task Group | Derive continue and fail-fast terminal sets |
| 9 | Draw startup and shutdown state machines | Inject acquisition and cleanup failures | Graceful Lifecycle Harness | Explain one absolute grace deadline |
| 10 | Build authority and feature-impact maps | Audit TaskHarbor invariants | Event-Driven Job Engine | Defend priority and final architecture |

## Daily evidence standard

A day is not complete because the happy path passes. Record:

- one prediction that was wrong and the corrected model;
- one adversarial terminal path;
- one cleanup or ownership proof;
- one explicit bound;
- one result that remains deterministic under schedule variation;
- one guarantee the design intentionally does not provide.

## Week boundary review

After Day 5, rebuild a cancellable polling component without notes. It must use one owner, one deadline, injected time, and exact cleanup. After Day 10, complete the final review and the independent notification-campaign runner before reading its solution criteria.
