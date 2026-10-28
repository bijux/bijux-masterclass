# Worked answers — Deployment Independence, Version Skew, and Release Choreography

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. Why is a separate deployment pipeline not proof of independent deployment?

If callers, databases, or private models must change simultaneously, the pipeline only automates a coordinated release train.

**Decisive evidence:** mixed-version release matrix

## 2. What does provider 1.1 need to preserve for consumer 1.0?

Existing request, response, event, and error semantics. Additive features must be optional or ignored safely.

**Decisive evidence:** old-consumer/new-provider contract test

## 3. How can consumer 1.1 work with provider 1.0?

Disable the new feature or use a fallback when the provider capability is absent. Requiring it immediately breaks rolling rollout.

**Decisive evidence:** new-consumer/old-provider test

## 4. Why must event consumers understand retained historical versions?

Replay can deliver events produced long before the current deployment. Silent history rewrite breaks audit and compatibility.

**Decisive evidence:** replay compatibility proof

## 5. What is the service-owned expand-and-contract sequence?

Expand owner schema, deploy compatible code, migrate/backfill, remove old writers, observe, then contract. Other services must not write the schema.

**Decisive evidence:** migration choreography report

## 6. Why can rollback fail after a successful code deployment?

New data, events, or external effects may not be readable or reversible by old code. Rollback boundaries must include data and contracts.

**Decisive evidence:** rollback rehearsal

## 7. What does shadow comparison need beyond response equality?

Authorization, side-effect suppression, error classification, latency/resource bounds, and version identifiers.

**Decisive evidence:** shadow evidence report

## 8. Why is permanent support for every version harmful?

It multiplies code paths, tests, security surface, and ambiguity. Version skew should be bounded and retired deliberately.

**Decisive evidence:** version retirement policy

## 9. How can Notification Service release independently?

Its event input remains compatible, its owned database migrates independently, its delivery behavior stays within contract, and rollback/replay do not require Control deployment.

**Decisive evidence:** notification release proof

## 10. What makes Artifact Service rollback harder than Notification rollback?

Artifact Service owns durable bytes and write authority; rollback may need old readers to understand new objects and must reconcile already stored effects.

**Decisive evidence:** artifact rollback sequence

## 11. Why should a platform catalogue record but not centrally execute all migrations?

Visibility is useful, but central execution recreates a shared release train and weakens owner responsibility.

**Decisive evidence:** migration owner audit

## 12. When is a breaking service release acceptable?

Only under an explicit major transition with consumer inventory, migration path, bounded coexistence, rollback, and approval. It cannot masquerade as an internal change.

**Decisive evidence:** breaking-release governance
