# First Session Guide

Use this page when this is your first honest pass through the capstone and you want a
coherent route without trying to understand every guide at once. The goal is not to cover
everything. The goal is to leave the first session able to name the domain, the authority
boundary, and the next proof route.

## Best first-session route

1. Read `GUIDE_INDEX.md` to understand what the local doc set is trying to do.
2. Read `README.md` until the scenario and review routes make sense.
3. Read `DOMAIN_GUIDE.md` to settle the vocabulary.
4. Read `SCENARIO_GUIDE.md` to understand the default flow.
5. Read `OWNERSHIP_BOUNDARIES.md` to settle authority versus derivation versus orchestration.
6. Run `make demo`.
7. Read `RULE_LIFECYCLE_GUIDE.md` or `EVENT_FLOW_GUIDE.md` depending on whether the pressure is lifecycle or collaboration.
8. Stop there unless you already have a specific proof question.

## If you only have thirty minutes

1. Read `README.md`.
2. Read `DOMAIN_GUIDE.md`.
3. Run `make demo`.
4. Read `OWNERSHIP_BOUNDARIES.md`.

## If you already know the question

- If the question is about authority, read `OWNERSHIP_BOUNDARIES.md`.
- If the question is about scenarios, read `SCENARIO_BOUNDARY_MAP.md`.
- If the question is about commands, read `COMMAND_GUIDE.md`.
- If the question is about file ownership, read `ARCHITECTURE.md` and `SOURCE_GUIDE.md`.

## Stop the first session when you can answer these

- What object is authoritative for rule lifecycle and alert creation?
- Which artifacts are derived views rather than the source of truth?
- Which local command should you use next, and why is it the smallest honest route?

## Best companion files

- `GUIDE_INDEX.md`
- `README.md`
- `DOMAIN_GUIDE.md`
- `OWNERSHIP_BOUNDARIES.md`
- `COMMAND_GUIDE.md`
