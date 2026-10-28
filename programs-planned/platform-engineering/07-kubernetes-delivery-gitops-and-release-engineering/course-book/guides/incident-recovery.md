# Guide — Delivery incident recovery

Start with the earliest failed transition: source, artifact, render, comparison, apply, health, exposure, journey, or data gate.

Bound scope before changing state. Suspend only the affected reconciliation units. Preserve controller Events, source revisions, rendered output, inventories, managed fields, progressive analysis, and credential logs.

Choose among traffic abort, desired-state rollback, forward fix, compensation, or data recovery using the documented rollback frontier. Manual cluster changes are temporary unless reviewed and committed as durable desired state.

Before resuming reconciliation, classify every live-to-Git difference and restore ordinary scoped credentials. Closure requires user and data verification plus a no-op reconciliation.

## Extended reader notes

Use the release ledger to locate the earliest broken transition. Preserve source revision, artifact set, rendered digest, inventory, diff, controller conditions, live fields, health, actual traffic, journey results, and data phase before making broad changes.

Contain the smallest authority: suspend one Application or Kustomization, stop one automation writer, or freeze one promotion wave. Choose reconcile, revert, forward fix, or retire based on compatibility and ownership. Document break-glass fields and merge them back into reviewed desired state.

After recovery, verify that protected resources remain, controller inventory is coherent, source lineage is restored, and emergency credentials are revoked. A recovered workload with unreconciled authority remains an incident.
