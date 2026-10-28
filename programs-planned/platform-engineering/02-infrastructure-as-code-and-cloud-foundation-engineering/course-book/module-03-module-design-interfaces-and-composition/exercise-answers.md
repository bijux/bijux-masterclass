# Worked Answers — Module Design

## 1. Root-only responsibilities

Backend selection, provider configurations and aliases, account/region credentials, environment inputs, exact module versions, and cross-capability composition belong in the root. Child modules declare compatible provider requirements and own one capability.

## 2. Thin wrappers

They add another interface, version, documentation surface, and migration burden without raising architectural meaning. They often expose nearly every provider argument, so callers must still understand the provider resource while also understanding the wrapper.

## 3. Network responsibility

It owns the account-local VPC, subnets keyed by stable zone slots, route tables, declared egress path, and flow-log plumbing. It rejects overlap and public routes in private tables. It receives address/zone/egress/log inputs and outputs stable subnet/route interfaces.

## 4. Structured maps

A semantic map key preserves object identity across insertion/reordering. An object keeps related attributes together and supports type validation. Parallel lists can become misaligned and `count` indices shift when edited.

## 5. Unsafe delegated input

`additional_admin_policy_json` or `allow_public_ssh` lets callers bypass the module’s security model. If extension is necessary, expose a constrained, inspectable vocabulary with policy checks.

The safer test is to enumerate the intended extension cases and design a typed input that makes every allowed case visible in plans and policy evaluation.

## 6. Output leak

Returning entire provider objects or internal route/security-group inventories causes callers to depend on provider schema and implementation details. Output the stable architectural values callers actually need.

A caller should be unable to infer or couple itself to resources the module is free to replace during a compatible upgrade.

## 7. Provider blocks

Provider configurations are global operational authority selected by root modules. Embedding them hides account/region choice and prevents normal module `for_each`, `count`, and `depends_on` patterns. Child modules declare requirements, not credentials/configuration.

## 8. Dependency inversion

The workload receives subnet IDs and an instance profile rather than creating its own network and role. The root can satisfy those dependencies with created modules or discovered existing resources without changing the workload module.

## 9. Confused ownership switches

One module is trying to both own a dependency and accept an external owner. The branches often differ in lifecycle and outputs. Split creation from consumption and let the root choose the dependency source.

## 10. Change classification

An optional output is usually additive. Changing default NAT profile is behaviorally and financially breaking. Renaming an address requires a move and is breaking without it. Narrowing validation is breaking for callers using values now rejected.

## 11. Move retention

Keep moves for all supported upgrade paths. Test upgrade from prior released states. Removing a move too early causes older callers to see destroy/create even when newer callers do not.

## 12. Proof levels

Static formatting/interface/policy checks; semantic CIDR/profile/key tests; `tofu test` plan assertions with mocks; live sandbox route, flow-log, egress, and negative reachability checks; plus upgrade proof from prior state for a published module.
