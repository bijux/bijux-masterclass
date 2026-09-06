---
module_id: SDRE-044
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 44
title: Service-Level Agreements
status: complete
last_verified: 2026-09-06
---

# Service-Level Agreements

## One-Page Review

### Governing question

How should engineers read, design, implement, and verify a service-level agreement as a conditional allocation of service responsibility and consequence—without mistaking a credit formula for end-to-end reliability or legal advice?

### Essential definitions

- a **service-level agreement (SLA)** is an agreement between identified parties that defines covered service levels and explicit consequences when its conditions are met or missed;
- a **party** is an entity whose rights, obligations, authority, and notices are governed by the agreement;
- a **covered service** is the exact product, operation, region, tier, and period within scope;
- a **service-level objective (SLO)** inside an SLA is the measured target used for contractual evaluation;
- a **prerequisite** is a customer or provider condition that must hold for coverage;
- an **exclusion** removes declared events or causes from the agreement's calculation or remedy;
- a **demarcation point** separates provider responsibility from customer, network, or third-party responsibility;
- an **evaluation period** is the contractual window, often a billing month;
- a **remedy** is the agreed consequence of a qualifying miss, such as a service credit;
- a **service credit** is an amount calculated under the agreement and is not necessarily cash compensation for business loss;
- a **claim procedure** defines notice channel, deadline, required evidence, and adjudication;
- an **evidence precedence rule** states which measurements govern when sources disagree;
- **sole and exclusive remedy** language limits available contractual remedy as stated by the governing agreement;
- **version provenance** identifies the exact agreement text and effective date applied to an event.

### Central model, mechanism, or theorem

For contractual scope $C$, prerequisites $P$, exclusions $X$, measured service level $S_W$, target $\theta$, and remedy schedule $R$, a simplified eligibility predicate is

$$
E=\mathbf{1}\{C\land P\land\neg X\land S_W<\theta\land\text{valid timely claim}\}.
$$

The calculated remedy is then $E\cdot R(S_W,B)$ for eligible billing base $B$. This model is educational: actual rights depend on the complete governing documents, jurisdiction, facts, and qualified legal interpretation.

### Critical invariants

- identify the parties, incorporated documents, version, effective date, and precedence;
- trace covered service down to operations, regions, tiers, accounts, and configurations;
- reproduce the exact measurement formula, source, timezone, aggregation, and rounding;
- distinguish prerequisites from exclusions and test each against architecture;
- map the demarcation point and every dependency users experience;
- preserve provider and customer evidence with synchronized time and configuration history;
- calculate remedy from the specified billing base and tier, not total business loss;
- automate claim reminders but require authorized review before submission;
- never use a supplier SLA as the workload's SLO or resilience design;
- involve qualified business and legal owners for contractual conclusions.

### Common failures

Failures include reading only the percentage, assuming all features are covered, ignoring required redundancy or retries, confusing provider and workload availability, multiplying SLA percentages as if failures were independent, overlooking billing-period boundaries, treating planned maintenance and quota events casually, losing logs before the claim deadline, assuming credits are automatic, calculating credits from total spend, relying only on a status page, failing to retain the agreement version, and presenting engineering interpretation as legal advice.

### Compact example

A fictional API agreement covers only generally available write operations in two named regions for accounts using the required retry policy. It calculates monthly request success from provider logs, excludes customer credential failures and documented maintenance, and targets 99.9%. Below 99.9% but at least 99.0% earns a 10% credit on the affected regional API charge after a claim within 30 days. A customer measuring 99.7% browser journey success may have severe harm without a qualifying breach if the provider's covered API measure remains 99.95%. The contract informs dependency risk; it does not guarantee the customer's application.

### Connections

[SDRE-043](043-service-level-objectives.md) supplies measurable targets. [SDRE-045](../ROADMAP.md) next treats operational tolerance and policy; agreement credits and engineering error budgets are related but not interchangeable.

## Governing Question

An SLA is often reduced to “99.9% uptime.” The rest of the document determines whether that number applies. Definitions may narrow downtime to failed valid requests, measurement may use provider records, eligibility may require a topology or retry behavior, exclusions may remove important failure causes, and the remedy may be a capped credit available only through a timely claim.

Engineers must translate those terms into architecture, telemetry, operations, and evidence retention. They must also respect role boundaries: engineering can model and test technical meaning, but legal and commercial owners decide interpretation, negotiation, enforceability, and claims. The governing question asks for a rigorous technical reading that supports those owners without impersonating them.

## Why This Matters

Google's SRE text distinguishes an SLA by the explicit or implicit contract and consequences attached to its objectives; the consequence can be financial or take another form [1]. NIST SP 500-307 connects representative, accurate, reproducible service metrics to service selection, agreement, and verification [2]. ISO/IEC 19086-1 supplies common cloud SLA concepts rather than a universal contract or universal objective set, and ISO/IEC 19086-2 supplies a metric model without mandating particular metrics [3, 4].

Current provider agreements demonstrate why the whole document matters. The current Amazon Compute SLA distinguishes region-level and instance-level scopes, defines service credits against affected charges, requires a claim with specified evidence and timing, and lists exclusions [5]. A current Google Cloud Operations SLA defines covered services, monthly uptime, claim evidence, capped financial credits, exclusions, and prior versions [6]. These are source-specific observations checked on 2026-09-06, not summaries of every provider agreement.

Microsoft's current engineering guidance describes SLAs as conditional commitments and warns that credits are generally not automatic, may be small compared with business impact, and do not replace workload resilience [7]. That guidance is not the governing contract for another provider, but it offers a useful reading method: scope, measurement, conditions, exclusions, design implications, and claim preparation.

## Prerequisites and Retrieval

Retrieve SLI, SLO, party, contract, scope, service, operation, availability, durability, evaluation window, billing period, credit, remedy, evidence, exclusion, dependency, redundancy, retry, quota, maintenance, force majeure, notice, claim, version, precedence, and jurisdiction.

From SDRE-041 retrieve property and failure-domain distinctions. From SDRE-042 retrieve measurement populations and unknowns. From SDRE-043 retrieve target, window, attainability, and audience. This chapter supplies technical contract analysis, not legal advice or jurisdiction-specific conclusions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish an SLA from an SLI, SLO, support policy, warranty, and workload target;
2. extract parties, incorporated terms, scope, prerequisites, exclusions, and remedies;
3. reproduce a contractual service-level calculation exactly;
4. map agreement demarcation points to an end-to-end architecture;
5. compare provider and customer measurement populations;
6. calculate tiered service credits from the correct billing base;
7. design evidence capture and retention for a possible claim;
8. identify dependency and aggregation assumptions unsupported by the agreement;
9. govern agreement versions, changes, and operational readiness;
10. communicate technical findings with explicit legal and evidentiary limits.

## Core Exposition

**Assemble the governing document set.** Begin with the signed order, master terms, service-specific SLA, support terms, service descriptions, configuration requirements, price schedule, data-processing terms, acceptable-use policy, and amendments. A web page may be incorporated by reference and changed prospectively. Capture title, canonical URL, version or last-modified date, retrieval date, effective dates, and precedence clause.

Do not assume the page visible during an incident governed the earlier period. Retain the applicable text and a cryptographic digest where policy permits. Link every internal interpretation to a clause and document version. If two documents conflict, record the conflict for authorized legal or commercial resolution.

**Identify parties and authority.** Determine provider, customer legal entity, reseller, affiliate, end user, and authorized claimant. An engineer observing an outage may not have authority to submit or accept a claim. Define internal owners for contract, service, billing, evidence, procurement, legal review, and notification.

Map notices to channels and deadlines. Support tickets, contractual notices, incident escalation, and credit claims may use different systems. Automate reminders and evidence assembly, but do not automatically send a legal assertion without authorized review.

**Resolve covered service precisely.** Record product name, SKU, tier, feature maturity, operation, endpoint, region, zone, account, subscription, and configuration. Generally available core operations may be covered while preview features, optional integrations, control planes, data transfer, or dependent services are not.

Coverage can vary by deployment. One instance may receive different terms from a multi-zone configuration. A regional commitment may require resources in multiple zones. Verify actual configuration continuously; an architecture diagram from procurement time is not proof that prerequisites held during an incident.

**Translate definitions into event logic.** Extract valid request, successful request, downtime, unavailable minute, maintenance, force majeure, excluded service, eligible account, measurement source, evaluation period, and rounding. Represent each as a predicate. Test real incident traces against the predicates and identify facts that require interpretation.

The product's user-visible failure definition will often be broader. A supplier may measure API acceptance while the customer measures completed checkout. The supplier may stop timing at its edge while the customer includes client and downstream work. Keep two models: contractual compliance and end-to-end user reliability.

**Reproduce the formula.** Determine whether measurement is request-, time-, instance-, region-, or account-based. Identify numerator, denominator, exclusions, aggregation, timezone, incomplete operations, retries, maintenance, sampling, missing data, and rounding. Never substitute an internal dashboard query merely because its label resembles the agreement.

For time availability, an agreement might define monthly uptime as $(T-D)/T$, where $T$ is eligible minutes and $D$ is defined downtime. For request availability it may use good valid requests divided by valid requests. Those formulas respond differently to quiet periods, bursts, and never-arrived traffic.

**Distinguish prerequisites from exclusions.** A prerequisite says coverage depends on a condition such as a supported version, multi-zone topology, retry policy, valid account, or quota compliance. An exclusion says certain events or causes do not count, such as customer action, unsupported software, Internet failure beyond a demarcation point, force majeure, or preview features.

These categories have different operational controls. Monitor prerequisites as configuration compliance. For possible exclusions, preserve causal evidence rather than labeling an outage excluded by intuition. The provider and customer may dispute cause or scope.

**Map demarcation and shared responsibility.** Draw the user journey from client through network, identity, provider service, customer code, data, and downstream dependencies. Mark which boundary the SLA covers. An infrastructure credit does not restore lost orders, repair corrupted customer data, or prove an application met its own objective.

Use the SLA as failure-mode evidence. Required retries imply transient failures are expected. Redundancy conditions imply a single resource is insufficient for the stated commitment. Excluded quota breaches require capacity and quota monitoring. But do not treat exclusions as acceptable user outcomes; design mitigations according to user harm.

**Do not compose published percentages naively.** Multiplying two provider percentages assumes compatible populations, windows, definitions, and statistically independent serial failures. Real services share networks, identity, control planes, regions, and operators. Agreements also contain different exclusions and remedies. A product can fail without either supplier breaching its SLA.

Build an architecture reliability model from mechanisms and observed behavior. Use each SLA to identify contractual boundaries and recovery signals, not as a probability distribution. If a supplier commitment is weaker than the workload need, add tested mitigation or change the workload promise.

**Understand the remedy schedule.** Extract threshold tiers, comparison inclusivity, affected billing base, caps, currency, minimum amount, stacking rule, form of credit, expiry, and sole-remedy language. A 10% credit usually applies to specified affected service charges, not total cloud spend, revenue loss, or customer compensation.

The controlled example below evaluates a fictional time-based SLA. It demonstrates tier and billing-base arithmetic only; it does not interpret any real agreement.

<!-- bijux-verify: {"id":"calculate-fictional-sla-credit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"uptime=99.8611% tier=10%\neligible_charge=$5,000.00 credit=$500.00\nbusiness_loss=$80,000.00 uncovered_by_credit=$79,500.00\n","stderr":""}} -->
```python
eligible_minutes = 43_200
downtime_minutes = 60
eligible_charge = 5_000.00
business_loss = 80_000.00
uptime = (eligible_minutes - downtime_minutes) / eligible_minutes

if uptime < 0.99:
    credit_rate = 0.25
elif uptime < 0.999:
    credit_rate = 0.10
else:
    credit_rate = 0.00

credit = eligible_charge * credit_rate
print(f"uptime={uptime:.4%} tier={credit_rate:.0%}")
print(f"eligible_charge=${eligible_charge:,.2f} credit=${credit:,.2f}")
print(f"business_loss=${business_loss:,.2f} uncovered_by_credit=${business_loss-credit:,.2f}")
```

The final line does not assert that business loss is legally recoverable; it shows that this fictional service credit is economically different from harm.

**Prepare evidence before incidents.** Record synchronized timestamps, request outcomes, regions, resources, account and tier, configuration, retry attempts, quotas, deployment history, provider incident identifiers, status communications, invoices, and support correspondence. Preserve raw-enough evidence to recompute the contractual formula and a chain of custody appropriate to the dispute risk.

Test whether logs survive the outage they must prove. Keep retention beyond the claim deadline and likely dispute period. Protect personal data, secrets, and privileged communications. Evidence collection must follow security, privacy, records, and legal-hold policy.

Provider and customer measurements can disagree because of boundary, clock, sampling, classification, aggregation, or loss. Reconcile using matched events and clauses. Do not alter evidence or invent certainty; record known facts, method, discrepancy, and requested resolution.

**Run the claim workflow as an operational procedure.** Detect a possible breach, freeze the governing version, open the required support case, notify contract owners, preserve evidence, reproduce the calculation, review exclusions and prerequisites, calculate the claimed tier, obtain authorization, and submit through the named channel before the deadline.

Track acknowledgment, questions, decision, credit, appeal route, and lessons. A denied claim can reveal an architecture or evidence gap even when commercial owners accept the decision. A granted credit does not establish root cause or prevent recurrence.

**Negotiate from user and architecture needs.** Before purchase, compare covered operations and failure definitions with the workload's journeys. Ask about measurement authority, raw evidence access, exclusions, planned maintenance, support response, recovery objectives, durability, security incidents, data portability, change notice, termination assistance, and remedies.

The engineering team should quantify the cost of meeting prerequisites and the residual risk outside coverage. Commercial and legal teams decide whether terms are acceptable and negotiate changes. Avoid claiming that a standard provider agreement is non-negotiable without verifying the procurement context.

**Govern change.** Monitor SLA URLs and incorporated documents for changes, but validate notifications against authoritative sources. Before a new version takes effect, diff scope, formula, targets, exclusions, claim timing, remedy, and architecture prerequisites. Update controls, evidence, risk registers, and internal runbooks through review.

Retain prior versions and effective intervals. For each incident, apply the version governing that service, account, region, and time. Periodically simulate a claim using synthetic evidence to verify that logs, invoices, roles, and deadlines can be assembled.

## Definitions and Notation

Let $A$ be the applicable agreement version, $C(x,A)$ the covered-scope predicate for observation $x$, $P(x,A)$ satisfied prerequisites, and $X(x,A)$ an applicable exclusion. The contractual eligible set for window $W$ is

$$
V_A(W)=\{x\in W:C(x,A)\land P(x,A)\land\neg X(x,A)\}.
$$

Let $Q_A(x)$ be contractual goodness. For nonempty $V_A(W)$, $S_A(W)=|\{x\in V_A(W):Q_A(x)\}|/|V_A(W)|$. This may differ from the workload SLI because the population, boundary, and predicate differ.

For target $\theta$, claim timeliness $N$, and required evidence $H$, define simplified remedy eligibility

$$
E_A=\mathbf{1}\{S_A(W)<\theta\land N\land H\}.
$$

Let eligible charge be $B\ge0$, credit rate function $r_A(S)\in[0,1]$, and cap $K\ge0$. A simplified service credit is

$$
R_A=E_A\min\{B\,r_A(S_A(W)),K\}.
$$

Actual agreements may add thresholds, minimums, non-stacking rules, currencies, tax treatment, or other conditions. The formula does not determine legal rights outside its stated fictional or extracted terms.

## Mechanisms, Invariants, or Proof Structure

**Scope-subset argument.** Contractual eligibility applies only where all coverage and prerequisite predicates hold and exclusions do not. Therefore a user failure outside $V_A(W)$ can cause real harm without lowering $S_A(W)$. Contract compliance does not imply workload reliability.

**Boundary argument.** If the agreement measures provider acceptance but the workload requires completed user action, $Q_A(x)$ does not imply workload goodness without downstream assumptions. The demarcation point must remain explicit.

**Credit-bound derivation.** With rate $r\in[0,1]$, base $B\ge0$, and cap $K\ge0$, $0\le\min(Br,K)\le B$ when $K\le B$ or otherwise no greater than the smaller term. A percentage credit cannot be assumed to compensate losses beyond its contractual base.

**Non-composition counterexample.** Two services can each meet 99.9% monthly contractual availability yet fail simultaneously during an excluded shared-network event. The workload can be unavailable while neither agreement is breached. Multiplying percentages neither models the exclusion nor the correlation.

**Version argument.** Applying agreement version $A_2$ to an event governed by $A_1$ can change scope, formula, or remedy after the fact. Retaining effective intervals is necessary for reproducible evaluation.

**Evidence argument.** A true breach may yield no remedy if a timely claim or required proof is absent. Therefore operational evidence and notice controls are part of remedy attainability even though they do not improve service availability.

## Alternatives and Trade-Offs

**Provider versus customer measurement.** Provider data may be authoritative under the agreement and omit the client journey. Customer data represents experienced harm and may lack provider internals. Retain both and predefine reconciliation.

**Time versus request measurement.** Time measures duration and can count quiet outages; requests measure demand and can miss periods with no attempts. Use the contractual formula for claims and user-oriented indicators for design.

**Automatic versus claim-based credits.** Automatic credits reduce administrative loss but require trusted detection and entitlement logic. Claims allow review but impose deadlines and evidence burden.

**Broad versus narrow scope.** Broad scope better matches user dependence and increases provider risk and price. Narrow scope is easier to measure but leaves more customer risk. Compare total architecture, not percentage alone.

**Service credits versus other remedies.** Credits are predictable and bounded. Termination rights, fee refunds, support escalation, or negotiated remedies may address other risks but increase complexity. Qualified owners decide appropriateness.

**Provider status versus independent probes.** Status pages provide provider context but may be delayed or coarsely scoped. Independent probes preserve customer evidence but must match contractual definitions and avoid false attribution.

**Standard versus negotiated terms.** Standard terms are scalable and comparable. Negotiated terms may address high-impact workflows, evidence, recovery, or liability but require cost and legal review.

**Single provider versus redundancy.** One provider simplifies semantics and support. Multiple providers may mitigate some failures while adding correlated dependencies, data divergence, security surface, and failover risk. Test mechanisms rather than counting SLAs.

## Failure Modes and Misconceptions

1. **“The SLA is 99.9%.”** The agreement includes far more than its target percentage.
2. **“SLA and SLO are synonyms.”** The agreement adds parties, conditions, consequences, and governing terms.
3. **“The provider SLA is our workload SLO.”** Boundaries, populations, dependencies, and user needs differ.
4. **“A credit is a reliability guarantee.”** It is a remedy under defined conditions after failure.
5. **“Credits cover outage loss.”** The base and cap may be far smaller and losses may be excluded.
6. **“Credits arrive automatically.”** Many agreements require a timely, complete claim.
7. **“The status page proves a breach.”** It may support evidence but need not match contractual scope or formula.
8. **“Every product feature is covered.”** Tiers, previews, operations, control planes, and integrations may differ.
9. **“Customer-caused means obvious.”** Cause and demarcation can be disputed and require evidence.
10. **“Planned maintenance never matters.”** Its notice, duration, window, and exclusion language require exact review.
11. **“Retries only improve availability.”** Required retries can change whether an event qualifies as downtime.
12. **“Two 99.9% SLAs multiply into our availability.”** Definitions, correlation, exclusions, and topology invalidate naive composition.
13. **“A higher percentage is always better.”** Scope, remedy, measurement, configuration, and price can matter more.
14. **“The current webpage governed last year.”** The applicable historical version and incorporation terms decide.
15. **“Engineering logs are automatically legal evidence.”** Integrity, retention, privacy, provenance, and admissibility need governance.
16. **“An engineer can decide enforceability.”** Technical analysis supports but does not replace qualified legal judgment.
17. **“A granted credit proves root cause.”** Commercial resolution and causal investigation answer different questions.
18. **“An exclusion makes user harm acceptable.”** It allocates contractual risk; engineering still mitigates harm.

## Worked Examples

### Example 1

**Situation.** A team buys a service advertised with 99.99% availability, but the agreement covers only multi-zone production instances and the deployment uses one development-tier instance.

**Reasoning.** The percentage does not attach to this configuration. The prerequisite and tier fail before the availability calculation. Engineering must either deploy the covered topology, accept and document the residual risk, or choose another service.

**Conclusion.** Resolve scope and prerequisites before using an SLA as an architecture input.

### Example 2

**Situation.** A 30-day fictional agreement has 43,200 eligible minutes and 60 defined downtime minutes.

**Reasoning.** Monthly uptime is $(43{,}200-60)/43{,}200=99.8611\%$. If the target is 99.9% and the 10% tier covers results below 99.9% but at least 99.0%, this result enters that tier—subject to all other claim conditions.

**Conclusion.** Exact denominator, boundaries, and tier inequalities determine the classification.

### Example 3

**Situation.** The 10% tier applies to a \$5,000 affected regional charge; total provider spend is \$80,000 and estimated business harm is \$200,000.

**Reasoning.** The calculated credit is \$500, not \$8,000 or \$20,000. Whether any other recovery exists depends on governing terms and law, which this engineering calculation cannot decide.

**Conclusion.** Credit base and business harm are separate quantities.

### Example 4

**Situation.** A provider records 99.95% covered API acceptance while the customer's checkout journey records 98.8% completion.

**Reasoning.** Customer code, payment dependency, client network, and post-acceptance processing sit beyond the provider's measured boundary. The supplier may meet its SLA while the workload misses its SLO. Join matched events to locate the gap and improve architecture.

**Conclusion.** Contract compliance at one demarcation point does not imply end-to-end reliability.

### Example 5

**Situation.** An agreement counts a request as failed only after three specified retries, but the customer's client performs none.

**Reasoning.** The customer may experience immediate failure while lacking a contractually qualifying event. Implementing retries could satisfy the prerequisite but must also respect idempotency, deadlines, load, and user harm.

**Conclusion.** SLA prerequisites become operational requirements but still need safe engineering.

### Example 6

**Situation.** A status page reports a 90-minute regional incident; customer logs show 45 minutes of errors, and provider records show 20 contractual downtime minutes.

**Reasoning.** The three sources use different scopes and boundaries. Preserve all of them, match account, operation, timestamp, retry, and exclusion facts, then calculate under the agreement's precedence and dispute process. Selecting 90 minutes because it is largest is not rigorous.

**Conclusion.** Evidence disagreement requires reconciliation, not opportunistic source choice.

### Example 7

**Situation.** Two serial suppliers each publish 99.9% monthly SLA targets, and an architect predicts $0.999^2=99.8001\%$ workload availability.

**Reasoning.** The arithmetic is a component model only under compatible probabilities and independent failures. Published contractual percentages have different definitions and exclusions; both suppliers can meet terms during a shared excluded Internet failure while the workload fails.

**Conclusion.** Do not use contractual targets as independent component probabilities.

### Example 8

**Situation.** A valid credit claim must arrive within 30 days after the billing month, but logs are retained 14 days and invoice allocation completes after 35 days.

**Reasoning.** The evidence and billing controls make remedy unattainable even if a breach occurs. Extend governed retention, preserve incident snapshots, pre-map charges, schedule deadlines, and name authorized reviewers.

**Conclusion.** Claim readiness is a cross-functional operational capability.

### Example 9

**Situation.** A provider updates its online SLA on April 1; an incident occurred March 28 and the claim is prepared April 10.

**Reasoning.** Capture both versions and their effective and incorporation terms. Apply the version governing March 28, not automatically the current page. Escalate ambiguity to contract owners rather than silently choosing the more favorable text.

**Conclusion.** Version provenance is required for reproducible contractual measurement.

### Example 10

**Situation.** A provider excludes quota exhaustion, and a launch fails after customer demand exceeds quota while an approved increase remains pending.

**Reasoning.** Contract coverage depends on exact terms and facts. Engineering should preserve quota, request, approval, and provider communications; meanwhile, the workload failure remains real. Add capacity forecasting, admission control, staged launch, and fallback regardless of claim outcome.

**Conclusion.** Contractual exclusion analysis and user-harm mitigation proceed in parallel.

## Cross-Program Connections

1. [SEME-001](../../10-software-engineering-methods-and-evolution/ROADMAP.md) connects procurement, incentives, ownership, and economic consequences to agreements.
2. [SARCH-001](../../12-software-engineering-software-architecture/ROADMAP.md) connects demarcation points and dependencies to resilience design.
3. [API-001](../../28-api-and-service-engineering/ROADMAP.md) connects valid requests, retries, idempotency, and operation semantics to coverage.
4. [CLOUD-001](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) connects regions, zones, tiers, and shared responsibility to cloud terms.
5. [SEC-001](../../25-security-engineering/ROADMAP.md) connects evidence integrity, privacy, abuse exclusions, and breach obligations.
6. [DARCH-001](../../20-data-architecture-engineering/ROADMAP.md) connects records retention, provenance, and ownership to claim evidence.
7. [STQE-001](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects synthetic probes and configuration tests to readiness.
8. [SYSENG-001](../../26-systems-engineering/ROADMAP.md) connects stakeholder agreements, interfaces, and verification to system lifecycle.
9. [PLAT-001](../../29-platform-engineering/ROADMAP.md) connects standardized evidence capture and configuration controls to internal platforms.
10. [DBE-001](../../18-database-engineering/ROADMAP.md) connects durability, recovery, and data-integrity obligations to service scope.

## References

1. Jones, C., Wilkes, J., Murphy, N. R., and Smith, C. “Service Level Objectives—Agreements.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/service-level-objectives/>. Retrieved 2026-09-06.
2. de Vaulx, F., Simmon, E., and Bohn, R. *Cloud Computing Service Metrics Description*. NIST SP 500-307, 2017. <https://doi.org/10.6028/NIST.SP.500-307>. Retrieved 2026-09-06.
3. ISO/IEC. *ISO/IEC 19086-1:2016 Cloud Computing—Service Level Agreement Framework—Part 1: Overview and Concepts*, with Amendment 1:2025 noted in the official record. <https://www.iso.org/standard/67545.html>. Retrieved 2026-09-06.
4. ISO/IEC. *ISO/IEC 19086-2:2018 Cloud Computing—Service Level Agreement Framework—Part 2: Metric Model*, confirmed 2024, with Amendments 1:2023 and 2:2025. <https://www.iso.org/standard/67546.html>. Retrieved 2026-09-06.
5. Amazon Web Services. “Amazon Compute Service Level Agreement.” Current agreement. <https://aws.amazon.com/compute/sla/>. Retrieved 2026-09-06.
6. Google Cloud. “Cloud Observability (Monitoring, Logging, Trace) Service Level Agreement.” Current page, last modified February 28, 2025. <https://cloud.google.com/operations/sla>. Retrieved 2026-09-06.
7. Microsoft. “How to Read a Service-Level Agreement (SLA).” Azure Reliability documentation, current page. <https://learn.microsoft.com/en-us/azure/reliability/concept-service-level-agreements>. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define SLA, party, covered service, prerequisite, exclusion, demarcation point, evaluation period, remedy, service credit, claim procedure, evidence precedence, and version provenance. Distinguish an SLA from an SLI, SLO, and support policy.

### Exercise 2

A fictional monthly SLA has 44,640 eligible minutes, 120 defined downtime minutes, a 99.9% target, 10% credit below 99.9% to 99.0%, and 25% below 99.0%. The affected charge is \$12,000 and the credit cap is \$2,000. Compute uptime, tier, uncapped credit, and capped remedy.

### Exercise 3

Design an evidence and claim-readiness workflow for a payment API agreement requiring retries, region-specific calculation, provider case IDs, invoice allocation, and a 45-day deadline. Include privacy and authorization controls.

### Exercise 4

Compare two suppliers: one offers 99.99% for a narrowly covered API with 10% credits; the other offers 99.9% end-to-end processing with 50% credits and stronger evidence access. Explain how workload needs, exclusions, failure modes, cost, and remedy affect selection beyond the percentage.

### Exercise 5

Transfer the method to an internal shared identity platform where no legal contract or money changes hands. Design an agreement with consequences, evidence, escalation, and revision while distinguishing it from an external SLA.

## Answers to the Exercises

### Answer 1

An SLA is an agreement between identified parties containing service commitments and consequences. A party has governed rights and obligations. Covered service is the exact in-scope product and configuration. A prerequisite must hold for coverage; an exclusion removes declared events or causes. The demarcation point divides responsibilities. The evaluation period is the contractual measurement window. A remedy is the consequence of a qualifying miss; a service credit is one bounded form. Claim procedure defines channel, deadline, evidence, and adjudication. Evidence precedence governs conflicting sources. Version provenance identifies applicable text and effective date. An SLI measures, an SLO targets, an SLA attaches agreement conditions and consequences, and a support policy governs assistance or response rather than necessarily service performance.

### Answer 2

Uptime is $(44{,}640-120)/44{,}640=44{,}520/44{,}640=99.7312\%$. That is below 99.9% but above 99.0%, so the rate is 10%. The uncapped credit is $12{,}000\times0.10=\$1{,}200$. The \$2,000 cap does not bind, so the simplified remedy remains \$1,200, subject to scope, prerequisites, exclusions, evidence, timely claim, and actual governing terms.

### Answer 3

Continuously inventory covered account, tier, endpoint, region, supported version, quota, and required retry configuration. Log synchronized per-attempt outcomes and retry sequence with privacy-minimized identifiers; retain provider incident and case IDs, configuration history, status communications, and immutable evidence snapshots. At possible breach, freeze the applicable agreement version, open the required provider case, separate regions, reproduce the contract formula, preserve invoice mapping, and notify service, procurement, finance, and legal owners. Schedule checkpoints before 45 days, obtain authorized review, submit through the contractual channel, and track response and credit. Restrict evidence access, redact payment and personal data, apply legal-hold and retention policy, and never auto-submit a legal claim from an alert alone.

### Answer 4

The first percentage may be irrelevant if the workload depends on processing after API acceptance or falls within exclusions. Its smaller credit may have little economic value, though its API could be technically excellent and cheaper. The second has a lower target but broader boundary, stronger evidence, and larger remedy; it may align better with the user journey. Compare operation scope, data correctness, latency, durability, regions, required topology, maintenance, quotas, customer duties, correlated dependencies, recovery, support, evidence authority, claim burden, total cost, and migration risk. Model and test the workload rather than selecting the largest number. Qualified commercial and legal owners assess contractual suitability.

### Answer 5

Name the platform team and consuming teams, covered identity journeys and environments, client prerequisites, measurement sources, availability and latency objectives, security and maintenance exclusions, evidence access, review window, and effective version. Consequences can include escalation, incident review, reliability work priority, release restrictions, consumer migration assistance, or a negotiated capacity change rather than money. Define support and emergency paths, dependency duties, claim-like evidence review, dispute authority, and prospective revisions. This is an internal service agreement with operational consequences; it may be called an SLA organizationally, but it is not automatically a legally enforceable external contract and should not be represented as one.
