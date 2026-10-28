# Reference — Infrastructure Migration Playbook

Infrastructure evolves while remote objects, state addresses, callers, and workloads remain live. The safest migrations make ownership and identity transitions explicit instead of treating a clean final configuration as sufficient.

## 1. Define old and new models

Document:

```text
old owner and state root
old resource address
remote immutable identifier
new owner and state root
new resource address
data-plane dependency
rollback boundary
```

If the old and new ownership models are unclear, do not begin state movement.

## 2. Classify every object

Each object must be one of:

- unchanged in place;
- moved to another address in the same state;
- transferred to another state owner;
- imported/adopted;
- replaced deliberately;
- split into several objects;
- merged;
- forgotten but retained unmanaged;
- destroyed and retired.

“Not in the new code” is not a lifecycle decision.

## 3. Separate configuration migration from behavior migration

A module refactor can preserve the same remote object using `moved` blocks. A network topology change may require new resources and traffic transition. Do not combine provider upgrade, module rewrite, account transfer, and data-plane redesign in one opaque plan unless the coupling is unavoidable and explicitly defended.

## 4. Prefer configuration-driven transitions

Use:

- `moved` blocks for address identity changes;
- `import` blocks for adoption;
- `removed` or equivalent ownership records for deliberate forgetting where supported;
- explicit old/new resources for phased replacement;
- versioned module interfaces;
- owner-local data copy or projection mechanisms for state transfer.

Configuration-driven history is reviewable and repeatable. Direct state commands are incident-grade tools when configuration cannot express the transition.

## 5. Expand–transition–contract

For a topology change:

### Expand

Create new capacity or an additive interface while old behavior remains valid.

### Transition

Move traffic, data, or callers gradually. Measure both generations. Preserve idempotency and avoid two uncontrolled writers for the same fact.

### Contract

Remove the old path only when evidence shows no remaining dependency and rollback no longer requires it.

Example: changing from one NAT gateway to per-zone NAT:

```text
create additional NAT and routes
→ verify private-b egress through nat-b
→ observe flow/cost/health
→ remove private-b dependency on nat-a
→ retire transitional route
```

## 6. Protect state identity

Before any state transfer:

- stop writers;
- back up and digest both source and destination state;
- confirm lineages and serials;
- enumerate remote IDs;
- define exact address mapping;
- prove destination has no conflicting owner;
- retain command transcript;
- recalculate full plans in both roots afterward.

Never allow source and destination states to manage the same remote object simultaneously.

## 7. Account and region moves

Many cloud resources cannot be moved across accounts or regions in place. A migration may be a replication and cutover rather than a state move. Consider:

- identity and key ownership;
- DNS and certificate authority;
- data copy and consistency;
- IP and endpoint changes;
- quota in both locations;
- audit continuity;
- rollback while both environments exist;
- eventual destruction and data-retention law.

A copied resource with the same name is not the same resource identity.

## 8. Provider and module upgrades

Upgrade provider dependencies separately when possible. Provider changes can alter defaults, normalization, replacement rules, and state schema. First obtain a plan with only the dependency upgrade, then perform the architectural change on the accepted baseline.

For module upgrades, test old state and old caller inputs against the new version. Retain move declarations and compatibility notes until all supported upgrade paths cross them.

## 9. Emergency drift

An incident mitigation—such as a temporary deny rule—must not be erased automatically by the next “clean” apply. Record:

```text
incident ID
owner
creation time
purpose
expected expiry
decision: adopt, replace, or remove
```

Drift detection should report the condition. It should not silently revert an active mitigation without incident ownership.

## 10. Verification and rollback

Before the irreversible step, define:

- control-plane checks;
- data-plane checks;
- negative tests;
- data integrity;
- allowed staleness or downtime;
- rollback trigger;
- last reversible point;
- owner of the decision.

Rollback may not be inverse apply. A data schema, key, DNS cache, or provider object may not be backward compatible. Sometimes forward repair is safer.

## 11. Migration dossier

A completed migration retains:

```text
old/new architecture
object classification
address and ID mappings
plans and approvals
state digests
apply transcript
traffic/data transition evidence
rollback decision
final data-plane proof
retired-resource inventory
remaining risks
```

The final clean plan is useful, but it does not explain how the system arrived there. The dossier preserves that history for the next operator and the next migration.
