# Lab — Reject an Unsafe Landing Zone

## Goal

Determine whether an account and authority design can contain a compromised Atlas workload without relying on naming conventions, tags, or operator goodwill.

## Safety boundary

The required path evaluates local organization, identity, and guardrail fixtures only. It does not create or modify an AWS Organization. The optional cloud comparison must use an explicitly authorized sandbox organization; it may not attach policies to production organizational units.

## Baseline

Load:

```text
capstone/fixtures/organization/organization-small.json
capstone/fixtures/organization/scp-deny-audit-disable.json
```

Draw the account graph and identify the management, security, log archive, shared services, non-production workload, and production workload responsibilities represented by the fixture.

## Hypothesis

A landing zone is an authority architecture, not a folder tree. Workloads must not run in the management account. The log archive must not be deletable by the workloads it records. Human administration, CI planning, CI applying, runtime access, audit delivery, security investigation, and break-glass access require distinct trust paths. A broad regional deny can break global services unless the exception model is explicit and tested.

## Controlled action

1. Evaluate `organization-small.json` against the architecture policy.
2. Introduce `bad-management-workload.json` and identify the exact authority boundary it violates.
3. Evaluate the audit-disable deny policy and state what it can and cannot prevent.
4. Evaluate `bad-region-deny.json`; identify which global or control-plane operations require explicit treatment.
5. Trace these identities end to end: planner, applier, workload, log delivery, security auditor, and break-glass operator.
6. For each identity, record trust source, target account, permitted actions, session duration, and revocation owner.
7. Simulate a compromised Atlas runtime identity and list the maximum reachable resources by account and service.
8. Propose one guardrail that belongs at organization level and one that must remain account- or workload-local.
9. Optional Level D: compare the model with an authorized AWS Organizations sandbox and retain effective-policy evidence without modifying production OUs.

## Oracle

- the baseline assigns accountable owners and distinct authorities;
- workload execution in the management account is rejected;
- the authoritative audit archive is outside workload authority;
- long-lived shared credentials are rejected;
- broad regional deny without tested exceptions is rejected;
- compromise scope is expressible as a bounded set of accounts, roles, and resources;
- organization guardrails are not misrepresented as complete workload authorization.

## Evidence

Retain the account graph, identity-flow table, guardrail ownership table, effective-policy reasoning, compromise blast-radius analysis, and a limitation statement for organization behavior not executed against a real control plane.

## Interpretation

Explain why moving resources into more accounts does not automatically create isolation. Isolation depends on trust policies, delegated administration, cross-account roles, logging authority, billing/management authority, and the recovery path. Also explain why an organization deny is a ceiling, not a grant of useful runtime permission.

## Cleanup

The dependency-light lab creates nothing. If the optional cloud comparison was performed, revert all sandbox policy and OU changes, confirm no production account was targeted, and retain only redacted CloudTrail event identifiers.

## Completion gate

You pass only when you can name the exact accounts and resources a compromised Atlas instance can affect, explain why it cannot alter organization policy or delete the authoritative audit archive, and identify one remaining risk the landing-zone structure alone does not solve.
