# Worked Answers — Declarative Infrastructure and the Execution Model

## 1. Existing remote bucket, absent state

OpenTofu normally proposes creating the bucket because configuration has a desired address and state has no associated remote object. Providers do not automatically adopt arbitrary objects by matching names; automatic adoption would be ambiguous and unsafe. Add complete resource configuration and a configuration-driven `import` block, review the import plan, and only then apply the association.

## 2. Renaming a resource

State correlates remote objects with resource addresses. The old address disappears and the new address appears, so the default interpretation is destroy old/create new. A `moved` block records the historical identity transition and lets OpenTofu reinterpret the existing state at the new address.

## 3. `count` identity shift

Inserting or reordering list elements changes index-to-object association. First choose semantic keys, then add one `moved` mapping for every existing index, verify the plan contains moves rather than replacements, and only then change the collection implementation.

## 4. `depends_on`

Use it for a real hidden behavioral dependency that cannot be expressed by passing a value, such as waiting for policy propagation required by a later API call. Broad dependencies serialize unrelated nodes and can make otherwise known values unknown until apply, reducing plan quality and parallelism.

## 5. Same commit, different plan

Examples include a newer provider selected by an unlocked constraint, a data source returning a newer AMI, remote drift discovered during refresh, different variable values, a different account/region, or changed organization policy. Source alone does not identify the planning context.

## 6. Unknown security values

Unknown means the plan cannot prove the final value. If the value controls public exposure, encryption, principal authority, or destructive behavior, approving it delegates the decision to apply time without review. Redesign so the value is known or require a bounded exception with post-apply enforcement.

## 7. Provider meaning

The provider defines schemas, defaults, normalization, replacement rules, state upgrades, and API behavior. A provider upgrade can turn an in-place update into replacement, expose new drift, or interpret a value differently. The provider lock digest is part of plan identity.

## 8. Saved plan

It reduces the risk that approval and apply calculate different actions from changed source, variables, or state. Remote infrastructure, quotas, policies, credentials, and provider API availability can still change between plan and apply. Saved plans are also sensitive artifacts.

## 9. Limits of `prevent_destroy`

The guard exists inside the resource configuration. Removing the whole block removes the guard. It also does not protect against console deletion, backend loss, or another configuration managing the object. Durable protection needs object retention, backups, policy, and review.

## 10. `ignore_changes`

Legitimate: an autoscaling controller owns desired capacity while OpenTofu owns the group’s structure. Illegitimate: ignoring security-group rules because another team edits them manually and the drift is inconvenient. The legitimate case has an explicit external owner and reconciliation model.

## 11. Successful apply, unhealthy target

The control plane accepted the resource operations, but the platform release is not correct. Inspect target health reason codes and prove DNS, TLS, listener routing, security-group path, Atlas readiness, and one end-to-end job. Do not convert an unhealthy target into a successful release metric.

## 12. Plan identity record

At minimum: source commit/digest, root stack, variables digest, backend key, workspace if used, state lineage and serial, OpenTofu version, provider lock digest, account ID, region, caller role class, plan SHA-256, creation time, and expiry/approval. This lets another operator detect a stale or mis-targeted plan.
