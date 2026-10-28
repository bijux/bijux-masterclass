# Evidence Model

Infrastructure claims need evidence from the layer that owns the claim.

## Four evidence classes

### A — semantic and static

Proves course invariants, CIDR arithmetic, state-transition logic, module contracts, plan classification, and policy behavior. It does not prove OpenTofu or AWS behavior.

### B — OpenTofu executable

Uses the pinned CLI for formatting, initialization, tests, plan serialization, state operations, and local-provider experiments. It proves tool behavior for the tested version but not AWS data-plane behavior.

### C — AWS sandbox

Uses a disposable account to create, inspect, replace, restore, and destroy real resources. It can prove provider API behavior, route selection, IAM effects, health checks, metadata options, storage restore, and cost-producing topology.

### D — organizational foundation

Uses multiple accounts and organization controls. It is required for claims about delegated administration, centralized audit, account vending, organization policies, and production identity federation.

## Plans are proposals, not outcomes

A saved plan proves what OpenTofu intended to request based on one configuration, state snapshot, provider version, credentials, and refresh result. It does not prove that apply succeeded or that the resulting data plane works.

## Applies are control-plane evidence, not business evidence

A successful apply proves that provider operations completed according to the provider. Atlas still needs HTTPS, health, metadata, attachment, restore, and negative-reachability tests.

## Evidence identity

Retain:

- source commit;
- OpenTofu and provider versions;
- module versions;
- account and region;
- caller identity;
- backend and state lineage;
- plan digest;
- apply result;
- data-plane checks;
- cleanup result.

Without identity, two correct-looking artifacts may describe different infrastructure generations.
