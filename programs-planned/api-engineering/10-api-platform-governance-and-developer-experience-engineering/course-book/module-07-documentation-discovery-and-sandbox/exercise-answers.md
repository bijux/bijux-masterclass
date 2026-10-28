# Worked answers — Documentation, Discovery, Sandboxes, and Consumer Onboarding

## 1. Why is generated reference documentation insufficient for onboarding?

Reference lists fields and operations; it rarely explains which interface to choose, how to obtain credentials, how to complete a useful task, or what failure means. Onboarding needs task and concept material around the reference.

## 2. What is time to first success?

The elapsed time from a consumer obtaining or beginning onboarding to completing a defined useful workflow in a safe environment. It is a product outcome, not merely time to open the portal.

## 3. Why must examples declare a contract version?

Otherwise copied code can silently target a different release than the reader expects. Version binding makes examples reproducible and deprecation impact visible.

## 4. What makes a sandbox isolated?

Synthetic data, separate tenant identity, short-lived credentials, bounded resources, controlled egress, reset semantics, and no route to production state.

## 5. Why is production data in a sandbox unacceptable?

It violates the trust boundary, creates privacy and retention risk, and turns a learning environment into an uncontrolled production replica.

## 6. What should documentation search optimize?

Successful task discovery and reduced time to useful evidence. Search impressions or query counts are not outcomes; zero-result and reformulation rates reveal gaps.

## 7. How should four interface types be documented?

Start from consumer tasks and decision criteria, then link protocol-specific reference. Do not force consumers to understand every interface before choosing one.

## 8. Who owns documentation semantics?

The API owner owns behavior and domain meaning. The platform owns publishing, structure, discoverability, quality checks, and common guidance. Shared editing does not erase authority.

## 9. What belongs in a quickstart?

Prerequisites, safe credentials, smallest useful workflow, expected result, cleanup, version, and a path to troubleshooting. It should not hide side effects.

## 10. Why publish failure examples?

Consumers need to recognize authorization, validation, conflict, rate, and dependency outcomes. Happy paths alone create fragile integrations.

## 11. What is an onboarding support handoff?

A documented transition from platform help—catalog, credentials, sandbox, SDK—to domain-owner help for contract semantics and business behavior.

## 12. How can docs become stale even when they build?

Links and syntax can remain valid while examples target old versions, owners change, runtime behavior drifts, or task outcomes no longer match. Freshness needs semantic and executable evidence.
