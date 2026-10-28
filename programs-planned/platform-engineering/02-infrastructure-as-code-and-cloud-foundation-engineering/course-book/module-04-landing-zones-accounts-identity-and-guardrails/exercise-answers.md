# Worked Answers — Landing Zones and Accounts

## 1. Account separation

It separates IAM and policy administration, quotas, billing/cost attribution, audit ownership, blast radius, and lifecycle. Production can use stricter controls and fewer administrators without constraining sandbox experimentation.

The design is justified only when the team can name which authority, quota, evidence, or failure is independently contained by each boundary.

## 2. Management account

It has organization-wide authority and consolidated billing responsibilities. A workload compromise or ordinary deployment mistake there can affect policy and accounts across the organization. Keep it narrowly used and strongly monitored.

## 3. SCP semantics

An SCP sets the maximum allowed action set for member-account principals. It does not grant permission. Effective authorization still requires identity/resource allows and is constrained by permissions boundaries, sessions, key policies, endpoint policies, and explicit denies.

## 4. Small structure

Management; log archive/security audit; shared services if genuinely shared; non-production workload; production workload; sandbox. Do not add a network account until central network ownership is real.

Each additional account needs a named operator, onboarding path, audit destination, network relationship, budget, and closure procedure; otherwise separation becomes unmanaged complexity.

## 5. Identity classes

Workforce roles represent humans; workload roles are attached to running services; CI roles are federated to a pipeline identity and scoped to release actions; break-glass roles are emergency, monitored, short-lived, and reviewed.

## 6. Plan/apply separation

Untrusted or unapproved source can often run a read-oriented plan. Mutation authority is granted only to an approved plan/digest. This narrows the consequence of pull-request code and makes approval identity explicit.

## 7. Independent logs

The destination account/bucket/key is administered separately; workload roles can deliver but cannot delete/alter retention; trail changes are monitored; evidence spans required regions/events; restore/query access is tested.

A useful negative test is to assume a workload administrator is compromised and prove that the same principal cannot erase or rewrite the evidence used to investigate that compromise.

## 8. Account lifecycle

Examples: OU placement, baseline identity, logging/security enrollment, network onboarding, budget/quota setup, ownership change, quarantine, resource/data cleanup, and account closure.

A mature account record also names the actor and evidence required for each transition, especially quarantine and closure, where abandoned resources and retained data create risk.

## 9. Region deny

Some global services use specific endpoints or require region exceptions. A broad deny can block IAM, DNS, CDN, organization, or support operations. Test documented exceptions in a sandbox OU.

Review the service’s documented control-plane endpoints and test the policy against real operations before promoting the deny to production scope.

## 10. Tags

They provide metadata for inventory, policy conditions, cost, and routing. They do not independently prove owner identity, network isolation, authorization, or correct data classification because they can be absent or mutable.

## 11. Quota and replacement

Safe replacement may require old and new generations simultaneously. If instance, address, target, volume, or load-balancer quotas have no headroom, creation fails before old resources can be retired.

Quota evidence belongs in the release review because a plan can be semantically safe yet operationally impossible to execute without overlap capacity.

## 12. Default provider risk

Any resource or module that omits explicit provider selection may run against the default account/region. In an organization root, an accidental management-account default can create or destroy resources in the highest-authority account.
