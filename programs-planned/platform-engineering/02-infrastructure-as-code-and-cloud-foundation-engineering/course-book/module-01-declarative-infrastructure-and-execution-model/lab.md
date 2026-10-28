# Lab — Diagnose a Plan Before It Becomes an Apply

## Goal

Determine whether a proposed infrastructure change is a faithful consequence of declared intent, an artifact of unstable resource identity, or an invalid action produced from stale planning context.

## Safety boundary

The required experiment uses the dependency-light Atlas plan model and checked fixtures. It creates no cloud resources and does not require credentials. The optional OpenTofu extension is limited to local validation and planning; it must not use an AWS backend or provider credentials.

## Baseline

From the course root, produce the baseline semantic plan:

```bash
PYTHONPATH=capstone python3 -m cloud_model.cli plan \
  capstone/fixtures/plan/config-v1.json \
  capstone/fixtures/plan/state-v1.json
```

Record the configuration digest, state lineage, state serial, resource addresses, and planned actions. The baseline should contain no unexplained replacement or deletion.

## Hypothesis

A legitimate change to one declared attribute should produce a narrow update. Replacing semantic collection keys should create address churn even when the underlying objects are conceptually unchanged. A saved plan must be rejected when the state serial or lineage changes after planning. A syntactically valid graph may still be rejected by policy when it exposes an unsafe public path.

## Controlled action

1. Compare `config-v2-intended.json` with `state-v1.json`. Explain every action from the changed intent.
2. Compare `config-v2-unstable-keys.json` with the same state. Identify which create/delete pairs are caused by address identity rather than desired infrastructure change.
3. Bind the baseline plan to `state-v1.json`, then attempt to evaluate it against `state-v2.json` and `state-other-lineage.json`. Retain both rejection records.
4. Inspect `plan-public-ingress.json`. Separate graph validity from policy acceptability.
5. Write the semantic keys and state-move declarations that would preserve the existing objects during the collection-key repair.
6. Optional Level B: when OpenTofu is available, run `tofu fmt -check -recursive capstone` and inspect a saved local plan. Do not configure an AWS backend.

## Oracle

- the intended fixture changes only the declared attribute;
- the unstable-key fixture produces address churn that can be explained without invoking provider behavior;
- serial and lineage mismatches reject the saved-plan context;
- unrestricted ingress is rejected even though it is representable;
- the proposed identity repair preserves logical objects rather than accepting avoidable replacement;
- no cloud API is called.

## Evidence

Retain a table with one row per planned action and these columns:

```text
resource address
before identity
requested intent
planned action
mechanism causing the action
acceptable or rejected
proof needed after a real apply
```

Also retain the plan digest, state lineage and serial, stale-plan rejection, policy rejection, and the proposed move map.

## Interpretation

Explain why a plan is evidence about a planning model, not evidence that the provider can complete the change or that the resulting data plane will work. Distinguish three review questions: *Is this the intended graph? Is this an acceptable action? What observation after apply would prove the resulting system?*

## Cleanup

Run:

```bash
make clean
```

Confirm that no state, saved plan, `.terraform`, credential, or generated report remains outside the designated evidence directory.

## Completion gate

You pass only when you can explain every create, update, replacement, and deletion; demonstrate stale-context rejection; and present a semantic-key migration that avoids unnecessary replacement. “The plan looks reasonable” is not evidence.
