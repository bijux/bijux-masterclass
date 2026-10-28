# Lab — Turn Resource Blocks into an Architectural Module

## Goal

Design a network module that owns a coherent decision, exposes a small typed interface, preserves resource identity during evolution, and improves the root composition rather than merely relocating HCL.

## Safety boundary

The required work uses checked JSON interface fixtures, the local HCL module under `capstone/modules/network`, and dependency-light validation. It creates no cloud resources. Native `tofu test` is optional and must use `-backend=false` or a local-only backend.

## Baseline

Review:

```text
capstone/fixtures/modules/network-v1.json
capstone/fixtures/modules/network-v2.json
capstone/fixtures/modules/network-bad.json
capstone/fixtures/migrations/flat-network-config.json
capstone/fixtures/migrations/flat-network-state.json
capstone/fixtures/migrations/module-network-config.json
capstone/fixtures/migrations/network-moves.json
capstone/modules/network/
```

Write a one-paragraph responsibility statement before changing an interface. It must say which network decisions the module owns and which decisions remain in the root.

## Hypothesis

A useful module reduces the number of invalid compositions. Semantic map keys preserve identity better than positional lists. Provider configuration belongs in the root. Outputs should expose capabilities the caller needs, not mirror every provider attribute. A module upgrade is safe only when interface compatibility and state-address migration are considered together.

## Controlled action

1. Compare the flat and module-shaped configuration fixtures. Identify the intended owner for VPC addressing, subnet roles, route tables, and egress policy.
2. Validate `network-v1.json`; then evaluate `network-bad.json` and explain each rejected input.
3. Upgrade the interface to `network-v2.json`. Classify every input/output change as compatible, review-required, or breaking.
4. Inspect the HCL module and confirm that provider configuration remains in the root.
5. Map the flat resource addresses to module addresses using `network-moves.json`.
6. Simulate the upgraded plan and verify that the move map prevents avoidable replacement.
7. Reduce the output surface to VPC identity, subnet identities by role and zone, and route-table identities. Defend every retained output.
8. Identify one repeated block that should *not* become a module because it does not own a stable decision.
9. Optional Level B: run `tofu init -backend=false` and `tofu test` in the network module when OpenTofu is available.

## Oracle

- the responsibility statement describes one coherent architectural decision;
- typed input validation rejects malformed or ambiguous subnet definitions;
- semantic keys remain stable across ordering changes;
- child configuration contains no provider ownership;
- the output inventory is bounded and caller-oriented;
- interface changes are classified before release;
- moved declarations preserve existing resource identity;
- at least one proposed abstraction is rejected as unnecessary.

## Evidence

Retain the responsibility statement, interface table, compatibility classification, rejected-input report, before/after resource-address table, move map, simulated upgrade plan, and the written rejection of one unjustified module.

## Interpretation

Explain why module count is a poor maturity metric. A deep wrapper can hide operationally important decisions; a thin wrapper can add ceremony without reducing risk. The relevant question is whether the abstraction creates a stable contract around an owned decision and makes unsafe states harder to express.

## Cleanup

Remove `.terraform`, temporary state, generated plans, and local test artifacts. Run `make clean` and verify the checked module source remains unchanged unless your evidence includes a deliberate reviewed patch.

## Completion gate

You pass only when the module interface is narrower than the provider surface, the upgrade preserves state identity, and you can defend both one abstraction you created and one abstraction you deliberately refused to create.
