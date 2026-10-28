# Worked Answers — Drift, Import, Refactoring, and Migrations

## 1. Drift classification

A console edit is **remote drift**. Changed but unapplied code is an **unapplied desired-state change**. A provider reading the same object differently is a **representation/normalization change**. Wrong lineage is **state corruption or selection error**. An emergency firewall rule is an **intentional out-of-band change** that needs reconciliation and expiry, not blind reversal.

## 2. Adopt reality

Adopt when the remote change is the approved current intent—for example an incident mitigation, provider-required property, or operational correction—and restoring the old configuration would be unsafe. The change still needs ownership, review, and a repository update so the declared model catches up.

## 3. Refresh-only scope

It updates state’s recorded remote values. It does not mutate the cloud object, make configuration match, prove authorization, or establish that the remote value is desirable. It can memorialize an unauthorized change if used without classification.

## 4. Import limitations

Import binds an address to a remote ID. The configuration may omit security, lifecycle, routing, encryption, or tags. The subsequent plan reveals how OpenTofu would reconcile the object. Adoption is complete only after the managed surface and data plane match intended policy.

## 5. Moved mapping

```hcl
moved {
  from = aws_vpc.atlas
  to   = module.network.aws_vpc.this
}
```

The exact destination must match the child module’s resource address.

Run a plan before and after the mapping: the accepted refactor shows address movement with no remote create or destroy action.

## 6. Retaining move history

An environment that has not yet applied the migration still has the old address in state. Removing the moved block too early makes its later plan see a destroy/create. Retention length follows the supported upgrade window.

## 7. State split

Benefits include narrower authority, smaller blast radius, independent lifecycle, and reduced lock contention. Risks include cross-state coupling, sequencing, duplicate ownership, output/data exposure, and harder recovery. The split must follow ownership, not file size alone.

## 8. NAT migration

Expand by creating per-zone NAT paths and routes without deleting the old egress. Transition subnets one at a time and verify source addresses, availability, and cost. Contract by deleting the central path only after every route and recovery procedure uses the new design.

## 9. Provider upgrade separation

A combined change obscures causality. If the plan changes, reviewers cannot tell whether provider normalization or redesign caused it. A dedicated upgrade makes tests, rollback, and incident diagnosis clearer.

Record the old and new provider locks, run the same fixtures under both, and isolate any state upgrade or replacement proposal before functional changes enter the review.

## 10. Ownership outcomes

Transfer means another managed state/controller adopts the same remote object. Forgetting means current state stops managing it while the object remains unmanaged or manually owned. Destruction removes the remote object. Each needs a distinct approval and consumer check.

## 11. State move evidence

Backend version/backup, lock/freeze, source and destination addresses, remote IDs, exact commands, peer approval, expected plan afterward, data-plane validation, and recovery commands. A successful exit code is not enough.

The post-move plan must be empty for the moved objects and remote identifiers must remain unchanged; otherwise the procedure has not demonstrated identity preservation.

## 12. Safe drift job

Use a read-only role, refresh/plan only, store a signed/hashed report, classify sensitive changes, notify owners, and require review for mutation. Never give the detection job unrestricted apply authority. Temporary incident changes should carry an ID and expiry recognized by the classifier.
