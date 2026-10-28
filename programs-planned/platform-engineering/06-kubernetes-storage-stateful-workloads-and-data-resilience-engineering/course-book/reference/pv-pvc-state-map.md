# PersistentVolume and PersistentVolumeClaim state map

## Claim states

- **Pending** — no compatible bound volume exists yet, or provisioning/binding awaits another transition.
- **Bound** — the claim and volume identify one another; attach, mount, and application readiness remain separate.
- **Lost** — the bound volume is no longer available to the claim.

## Volume states

- **Available** — not yet bound to a claim.
- **Bound** — reserved for one claim identity.
- **Released** — the claim was removed, but the resource is not yet available for safe reuse.
- **Failed** — automatic reclaim or lifecycle work failed.

## Binding evidence

A safe binding checks class, capacity, volume mode, access mode, selector, claim UID, and topology. Static prebinding does not waive compatibility. Dynamic provisioning records the request identity and backend handle. `WaitForFirstConsumer` adds consumer placement to the decision.

## Reuse and adoption

A Released volume can contain sensitive or authoritative data. Before reuse, verify reclaim policy, sanitation, data lineage, encryption context, claim identity, and whether a newer authoritative copy exists. Editing `claimRef` to make a volume Available is an operational migration, not routine cleanup.

## Protection

PVC/PV protection finalizers reduce deletion races while resources are in use. They do not replace authorization, backups, or deliberate deletion policy. Removing finalizers is a destructive intervention that requires data-owner approval and backend evidence.
