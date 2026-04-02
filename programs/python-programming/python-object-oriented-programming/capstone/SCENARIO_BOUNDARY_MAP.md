# Scenario Boundary Map

Use this page when you know a scenario would teach the idea faster than a file tree, but
you are not sure which scenario demonstrates which ownership boundary. The goal is to
turn the scenarios into deliberate teaching routes instead of isolated walkthroughs.

## Route by scenario

| Scenario | Best for learning | Start with | Then inspect | Best proof route |
| --- | --- | --- | --- | --- |
| default monitoring flow | aggregate authority, policy evaluation, and incident creation | `SCENARIO_GUIDE.md` | `RULE_LIFECYCLE_GUIDE.md`, `EVENT_FLOW_GUIDE.md`, `model.py` | `make inspect` |
| retirement flow | lifecycle cleanup, derived view updates, and authority after state change | `RETIREMENT_SCENARIO_GUIDE.md` | `PROJECTION_GUIDE.md`, `EVENT_FLOW_GUIDE.md`, retirement outputs | `make inspect-retirement` |
| rate-of-change flow | replaceable policy seams and extension without aggregate drift | `RATE_OF_CHANGE_SCENARIO_GUIDE.md` | `policies.py`, `PUBLIC_API_GUIDE.md`, extension surfaces | `make inspect-rate-of-change` |
| walkthrough bundle | the human reading route across multiple boundaries | `TOUR.md` | `WALKTHROUGH_GUIDE.md`, `TARGET_GUIDE.md`, `BUNDLE_GUIDE.md` | `make tour` |
| inspection bundle | current state, lifecycle evidence, and scenario variants in one place | `INSPECTION_GUIDE.md` | saved inspection bundle plus scenario guides | `make inspect` |
| verification bundle | executable confirmation plus saved review output | `PROOF_GUIDE.md` | verification report, `TEST_GUIDE.md`, event and walkthrough guides | `make verify-report` |

## Route by question

- If the question is "who is authoritative when the rule changes?" start with the default monitoring flow.
- If the question is "what else changes when a rule retires?" start with the retirement flow.
- If the question is "where should variation live?" start with the rate-of-change flow.
- If the question is "what is the most legible route for a human reviewer?" start with the walkthrough bundle.
- If the question is "what does the current state and scenario surface look like together?" start with the inspection bundle.

## Best companion files

- `SCENARIO_GUIDE.md`
- `RETIREMENT_SCENARIO_GUIDE.md`
- `RATE_OF_CHANGE_SCENARIO_GUIDE.md`
- `RULE_LIFECYCLE_GUIDE.md`
- `EVENT_FLOW_GUIDE.md`
