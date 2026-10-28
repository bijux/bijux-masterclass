---
module_id: SEC-001
program: Security Engineering
level: 1
module_number: 1
title: Assets, Adversaries, Trust, and Security Goals
status: complete
last_verified: 2026-08-28
---

# Assets, Adversaries, Trust, and Security Goals

## One-Page Review

### Governing question

What must be valued, relied upon, defended, and observed before “make the system secure” becomes an engineering claim?

### Essential definitions

- An **asset** is anything stakeholders value and whose loss, disclosure, alteration, unavailability, misuse, or unsafe behavior can cause harm.
- An **adversary** is an actor pursuing an outcome contrary to a protection need; model capabilities, access, knowledge, incentives, and constraints.
- **Trust** is reliance on an entity or assumption to behave as required. Trust is accepted dependency, not evidence of trustworthiness.
- A **security goal** states the protected asset, stakeholder, property, conditions, and observable success or violation.
- A **threat** is a circumstance or event with potential to cause an adverse impact by exploiting exposure or weakness.
- An **assumption** is a condition the design relies on but does not enforce.
- **Residual risk** is risk remaining after decisions and controls; it still needs an owner and review trigger.

### Central model, mechanism, or theorem

Build the initial security claim as:

`stakeholder → asset → harmful outcome → adversary capabilities → trusted dependencies → security goal → falsifying observation`.

This is not yet a full threat model. It establishes the typed inputs required to construct and review one.

### Critical invariants

- Every security goal protects a named asset for a named stakeholder.
- Adversaries are described by capabilities and position, not stereotypes.
- Every trusted dependency is explicit, minimized where possible, and assigned an owner.
- Assumptions are distinguishable from enforced controls and verified properties.
- Goals state scope and observable violation rather than naming a product or technique.
- Safety, privacy, reliability, and organizational harm are considered alongside data secrecy.

### Common failures

Frequent errors are protecting “the system” without assets, treating every attacker as omnipotent, calling internal components trusted by location, listing controls as goals, hiding assumptions, confusing compliance with security, ignoring administrators and suppliers, and deleting residual-risk statements after a test passes.

### Compact example

For a medical portal, “use encryption” is not a goal. A goal is: an authenticated patient must not receive another patient's clinical record through any patient-facing read operation; violation is any foreign record content or metadata disclosed under the stated identity and deployment assumptions. Encryption may support parts of that goal but does not define or prove it.

### Connections

[SEC-002](../ROADMAP.md) refines confidentiality, integrity, availability, and authenticity. Formal problem statements connect to [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md); protection mechanisms connect to [Operating Systems](../../22-operating-systems/ROADMAP.md); network position connects to [Network Engineering](../../24-network-engineering/ROADMAP.md).

## Governing Question

Security engineering starts with stakeholder harm, not a catalog of products or vulnerabilities. A payroll database contains sensitive records, but the assets also include correct salary changes, timely payment, accountable approvals, administrator credentials, recovery capability, employee privacy, and organizational trust. Each asset can require different evidence and owners.

An adversarial perspective changes ordinary engineering assumptions. Inputs may be chosen to trigger worst cases, identities may be valid but misused, insiders may already hold privileges, and dependencies may be compromised. Security cannot promise absence of all harm. It can state protection goals, constrain adversary models, reduce exposed trust, and build evidence that specific claims survive named attacks and failures.

## Why This Matters

Controls selected before assets and adversaries often solve the wrong problem. Encrypting a database at rest may reduce harm from stolen media while doing nothing against an authorized service account exporting records. Adding multi-factor authentication may reduce credential replay but not an administrator abusing legitimate authority. The control is meaningful only in a chain from stakeholder need to adversary capability and observable outcome.

NIST SP 800-160 Volume 1 Revision 1 frames trustworthy-system engineering around stakeholder protection needs, life-cycle reasoning, and evidence ([official final publication](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final)). This chapter adopts that engineering stance without claiming that one framework certifies a system.

## Prerequisites and Retrieval

You should understand system boundaries, actors, data flows, requirements, and basic probability. Recall that a set of capabilities can be compared by inclusion, a universal requirement needs adversarial counterexamples, and evidence supports only the assumptions and environment under which it was gathered.

## Learning Objectives

After completing this module, you should be able to:

- inventory data, service, control, identity, safety, and organizational assets;
- connect assets to stakeholders and concrete harm;
- describe adversaries by capability, access, knowledge, incentives, and limits;
- distinguish trusted from trustworthy and assumptions from controls;
- formulate scoped, falsifiable security goals;
- identify third-party, administrative, physical, and lifecycle dependencies;
- reason about residual risk and ownership;
- critique vague or control-shaped security statements.

## Core Exposition

An asset is defined by value and harm, not storage format. **Primary assets** are outcomes or information stakeholders directly care about: accurate balances, confidential diagnoses, safe machine control, or election integrity. **Supporting assets** enable them: credentials, signing keys, logs, source code, build systems, backups, personnel knowledge, and availability of dependencies. Compromise of a supporting asset can defeat several goals at once.

Asset analysis records owner, lifecycle, location, copies, derivations, authorized operations, and harmful outcomes. Data can require protection during collection, use, sharing, archival, and deletion. A model that names only the production database misses caches, telemetry, exports, test fixtures, devices, backups, and human memory.

Adversary labels such as “hacker,” “nation state,” or “insider” are too coarse for design. Record capabilities:

- network reach and physical proximity;
- valid or stolen credentials;
- tenant, employee, administrator, or supplier position;
- ability to choose inputs, timing, and concurrency;
- access to source, binaries, logs, or hardware;
- budget, patience, repeatability, and risk tolerance;
- ability to compromise dependencies or coerce trusted actors.

Let adversary capabilities be set `C_A`. A scenario requiring capabilities `P` is feasible in this abstraction when `P ⊆ C_A`; feasibility does not imply success, likelihood, or impact. Capability sets support comparison: an authenticated tenant and a database administrator expose different scenarios even if both are called insiders.

Trust means the system relies on something. A component can be trusted yet poorly designed; a cryptographic library can be trustworthy for a supported operation yet called with an unsafe protocol. Record the proposition relied upon: “the identity provider binds this subject to this tenant under policy X,” not “the identity provider is trusted.” The **trusted computing base** is the set of components whose correct behavior is necessary for a security property. Smaller is usually easier to assess, but only if required enforcement remains inside it.

A trust boundary appears where authority, interpretation, ownership, or assurance changes. Network hops often coincide with boundaries but do not define them. Parsing untrusted bytes inside one process crosses an interpretation boundary. A service accepting a signed assertion crosses from another administrative authority. Later modules provide systematic boundary and threat-modeling methods; here the requirement is to expose reliance.

A security goal should contain:

1. stakeholder and protected asset;
2. desired property and prohibited harm;
3. actors, operations, and lifecycle scope;
4. adversary capability or environmental assumptions;
5. observable acceptance or violation criterion;
6. owner and evidence type.

“Use TLS,” “deploy a firewall,” and “comply with policy” are design or governance statements. A goal such as “an unauthenticated network client cannot obtain invoice contents through the public service interface” can be falsified. It still needs scope: traffic metadata, administrators, endpoints, logs, backups, and compromised servers may be outside or inside the claim.

## Definitions and Notation

- `A`: set of assets under review.
- `S(a)`: stakeholders who value asset `a`.
- `H(a)`: harmful outcomes involving `a`.
- `C_x`: capabilities available to actor `x`.
- `T_g`: dependencies whose correct behavior is necessary for goal `g`.
- `E_g`: evidence collected for goal `g` under explicit assumptions.
- **Attack surface:** reachable points where adversary-controlled action can affect a protected system.
- **Control:** a safeguard or countermeasure selected to change risk.
- **Assurance:** justified confidence, based on evidence, that a claim is satisfied.
- **Risk:** uncertainty about adverse impact; quantitative or qualitative estimates must state assumptions.

Evidence is monotone only with care: a stronger adversary model can invalidate prior evidence, and a larger trusted base creates more necessary correctness assumptions. Passing one test adds bounded evidence; it does not subtract an unmodeled actor.

## Mechanisms, Invariants, or Proof Structure

Review an initial security claim through this chain:

1. identify stakeholder and valued asset;
2. state concrete adverse outcome;
3. define adversary position and capabilities;
4. enumerate relied-upon people, components, and assumptions;
5. write the security goal independently of a chosen control;
6. identify a decisive counterexample or observation;
7. assign evidence and residual-risk ownership.

The following authoring check demonstrates completeness and capability inclusion. It is not a security enforcement mechanism.

<!-- bijux-verify: {"id":"security-claim-shape","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"complete: True\nvague: False\ntenant-scenario: True\nnetwork-only-scenario: False\n","stderr":""}} -->
```python
required_fields = {
    "stakeholder", "asset", "harm", "adversary", "trust", "goal", "criterion"
}

def complete(claim):
    return required_fields <= claim.keys() and all(claim[field] for field in required_fields)

claim = {
    "stakeholder": "patient",
    "asset": "clinical record",
    "harm": "foreign disclosure",
    "adversary": "authenticated patient choosing record identifiers",
    "trust": "identity-to-patient binding and record ownership data",
    "goal": "patient reads return only records authorized for that patient",
    "criterion": "no foreign content or metadata in any patient read response",
}
print("complete:", complete(claim))
print("vague:", complete({"goal": "use encryption"}))

tenant = {"network", "valid-account", "choose-record-id"}
scenario = {"network", "valid-account", "choose-record-id"}
print("tenant-scenario:", scenario <= tenant)
print("network-only-scenario:", scenario <= {"network"})
```

Completeness of fields does not prove the goal is correct, exhaustive, implemented, or satisfied. Human review and adversarial system evidence remain necessary.

## Alternatives and Trade-Offs

**Asset-centric versus system-centric framing.** Asset-centric analysis follows value across components and lifecycle. System-centric analysis is easier to bound but can miss downstream copies and business harm. Use both views and reconcile them.

**Broad versus narrow adversary models.** Broad models reduce hidden assumptions but can make useful guarantees impossible or prohibitively costly. Narrow models enable precise claims but must disclose excluded capabilities and review triggers.

**Trust versus verification.** Some reliance is unavoidable: hardware, operators, compilers, authorities, and suppliers participate. Verification can reduce or relocate trust, not eliminate every dependency.

**Prevention versus resilience.** Preventing compromise is valuable; detection, containment, recovery, and safe degradation address attacks and errors that bypass preventive controls.

**Security versus other system goals.** Stronger controls can affect usability, availability, privacy, cost, and safety. Trade-offs need stakeholder authority rather than being hidden as implementation defaults.

## Failure Modes and Misconceptions

1. Data is the only asset. False: identities, control, safety, service, evidence, and reputation can be assets.
2. An adversary must be external. False: tenants, insiders, suppliers, and administrators may act adversely.
3. Trusted means verified secure. False: trust records reliance; trustworthiness requires evidence.
4. A network diagram contains every trust boundary. False: interpretation and administrative authority can change within one host.
5. A control is a security goal. False: “encrypt” does not name the protected outcome and scope.
6. Compliance proves security. False: compliance evidence covers specified criteria, not every adversary or harm.
7. More trust improves security. False: each necessary trusted dependency adds a correctness assumption.
8. An omnipotent attacker is conservative and useful. Often false: it prevents discriminating feasible controls and evidence.
9. Passing tests eliminates residual risk. False: tests are bounded by paths, inputs, environment, and oracle.
10. Security is complete at release. False: assets, dependencies, adversaries, and environments evolve.

## Worked Examples

### Example 1

**Question:** What are the assets in payroll?

**Reasoning:** Salary confidentiality is one. Correct payment amounts, authorized changes, timely payment, approval evidence, credentials, recovery copies, and employee trust are also valued.

**Conclusion:** Inventory value and harm, not tables alone.

### Example 2

**Question:** Why is “a sophisticated hacker” unusable?

**Reasoning:** It gives no network position, credential, privilege, knowledge, budget, or control of inputs, so it cannot determine feasible scenarios.

**Conclusion:** Model capabilities and constraints.

### Example 3

**Question:** Is an authenticated customer still an adversary?

**Reasoning:** The customer may honestly use permitted operations or deliberately substitute another customer's identifier while retaining a valid session.

**Conclusion:** Authentication establishes facts, not benign intent or object authorization.

### Example 4

**Question:** What is trusted in a signed software update?

**Reasoning:** Key custody, signer authorization, build inputs, signing implementation, client verification, rollback policy, and update distribution may all be necessary to the goal.

**Conclusion:** A valid signature is one link in a larger trusted base.

### Example 5

**Question:** Is an internal network automatically trusted?

**Reasoning:** Devices, workloads, operators, and routes have different authority; compromise or misconfiguration can originate inside.

**Conclusion:** Location is evidence only when tied to enforced identity and assumptions.

### Example 6

**Question:** Rewrite “protect customer data.”

**Reasoning:** Name customer, record class, operations, actors, lifecycle, disclosure or alteration harm, adversary capabilities, trusted dependencies, and observable violation.

**Conclusion:** A security goal must be falsifiable and scoped.

### Example 7

**Question:** Is availability only uptime?

**Reasoning:** A service can answer health checks while authorized users cannot complete a critical operation, or it can serve corrupted results quickly.

**Conclusion:** Availability goals name useful operation, load, duration, and correctness.

### Example 8

**Question:** How is a backup a supporting asset?

**Reasoning:** It enables recovery but may contain the same sensitive data, depend on keys, and become a destructive attack target.

**Conclusion:** Supporting assets inherit protection needs and add trust.

### Example 9

**Question:** What remains after least-privilege database access?

**Reasoning:** The authorized service identity can still be compromised, application queries can be flawed, administrators may bypass the control, and exports may escape its boundary.

**Conclusion:** A control changes residual risk; it does not erase the security case.

### Example 10

**Question:** When should the model be revisited?

**Reasoning:** New assets, actors, endpoints, dependencies, privileges, regions, regulations, incidents, and deployment routes can invalidate capability or trust assumptions.

**Conclusion:** Review triggers are part of residual-risk ownership.

## Cross-Program Connections

- **Software Design:** domain stakeholders determine value, harm, and authority.
- **Operating Systems:** privilege and isolation enforce parts of trusted boundaries.
- **Networking:** reachability and intermediary control shape adversary capabilities.
- **Cloud Infrastructure:** providers, control planes, identities, and regions expand the trusted base.
- **Reliability Engineering:** accidents and failures can produce the same asset harm as malice, but causal models and treatments may differ.

## References

- Ron Ross, Mark Winstead, and Michael McEvilley. [NIST SP 800-160 Vol. 1 Rev. 1, *Engineering Trustworthy Secure Systems*](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final). NIST, November 2022, DOI 10.6028/NIST.SP.800-160v1r1. Current final status checked 2026-08-28.
- National Institute of Standards and Technology. [*The NIST Cybersecurity Framework (CSF) 2.0*](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final). CSWP 29, February 2024. Current final status checked 2026-08-28.
- Joint Task Force Transformation Initiative. [NIST SP 800-30 Rev. 1, *Guide for Conducting Risk Assessments*](https://csrc.nist.gov/pubs/sp/800/30/r1/final). NIST, September 2012. Final-publication status checked 2026-08-28.
- Ross Anderson. [*Security Engineering: A Guide to Building Dependable Distributed Systems*, 3rd ed.](https://www.cl.cam.ac.uk/archive/rja14/book.html) Wiley, 2020, ISBN 9781119642787. Author and Cambridge archive checked 2026-08-28.
- Jerome H. Saltzer and Michael D. Schroeder. [“The Protection of Information in Computer Systems.”](https://doi.org/10.1109/PROC.1975.9939) *Proceedings of the IEEE* 63(9), 1975, pp. 1278–1308.

## Exercises

### Exercise 1

Create an asset inventory for a university examination system. Include primary and supporting assets, stakeholders, lifecycle stages, and concrete harms.

### Exercise 2

Compare capability sets for an unauthenticated Internet client, an authenticated student, a teaching assistant, a system administrator, and a compromised software supplier. Give one scenario feasible for each but not the previous actor.

### Exercise 3

For a password-reset service, enumerate trusted propositions and distinguish each from evidence that could justify trustworthiness. Identify assumptions outside the service.

### Exercise 4

Rewrite “use encryption and MFA to secure payroll” into at least three control-independent security goals with actors, scope, criteria, and residual-risk notes.

### Exercise 5

A hospital introduces an AI service that receives clinical notes from its record system and returns treatment suggestions. Produce the initial stakeholder–asset–harm–adversary–trust–goal chain, including safety, privacy, availability, supplier, operator, and model-update concerns. State review triggers.

## Answers to the Exercises

### Answer 1

Primary assets include confidential question content before release, authentic candidate identity, correct submissions and grades, fair timing, availability during the examination, and defensible appeals evidence. Stakeholders include students, examiners, the university, accreditation bodies, and accessibility staff. Supporting assets include author accounts, question repositories, release schedules, signing or audit keys, clocks, proctor records, backups, grading code, accommodations, and recovery procedures. Lifecycle stages are authoring, review, distribution, sitting, collection, grading, appeal, retention, and deletion. Harms include premature disclosure, impersonation, answer alteration, denial during a timed sitting, discriminatory accommodation failure, false audit evidence, and unrecoverable submissions.

### Answer 2

Let the Internet client have public reach and chosen inputs: it can flood a public endpoint. Add a valid student session: it can request another student's submission identifier. Add limited course-management rights for a teaching assistant: it can alter grades within an assigned course. Add host and database administration: it can bypass application checks or replace audit data. Add control of a trusted build/update source: a supplier compromise can insert code that executes later under service authority. The sets are illustrative, not necessarily strictly nested in a real organization; document which privileges and constraints each actor actually has.

### Answer 3

Trusted propositions include that the identity store maps the account correctly, recovery channels reach the intended person, tokens are unpredictable and single-use, expiry is enforced, redirects are fixed, rate limiting covers the deployment, logs omit secrets, operators protect signing material, and the email or messaging provider delivers without unauthorized disclosure. Evidence can include identity-process review, entropy analysis, state-machine tests, adversarial replay and redirect tests, multi-replica rate-limit tests, log scanning, key-access audit, and provider contract plus incident history. Assumptions may include control of the user's mailbox, device integrity, provider availability, DNS and network behavior, and administrator honesty; these are not made true by application tests.

### Answer 4

Goal 1: only authorized payroll approvers may cause a salary change, and every accepted change must identify subject, old value, new value, authority, and immutable approval evidence; compromised approvers and database administrators remain residual risks unless separately constrained. Goal 2: an employee using the employee portal must receive only that employee's payroll records, with any foreign content or metadata constituting violation; service administrators and exports require separate scope. Goal 3: stolen password knowledge alone must not establish an approver session under the declared identity policy; recovery channels, session theft, coercion, and identity-provider compromise remain. Encryption and MFA can be candidate controls after these goals exist.

### Answer 5

Stakeholders include patients, clinicians, the hospital, regulators, and emergency staff. Assets include note confidentiality and integrity, correct patient/model association, safe clinical decisions, service availability, consent and purpose limits, provenance, override capability, and incident evidence. Harms include disclosure to the supplier or wrong tenant, prompt or input manipulation, unsafe suggestion accepted as fact, unavailable advice delaying care, model updates changing behavior silently, and operators exporting notes. Adversaries include authenticated users selecting foreign records, compromised hospital or supplier identities, malicious insiders, network attackers within their actual reach, and supply-chain actors controlling model or code updates. Trusted propositions include record identity, transport endpoints, supplier isolation and retention, model/version provenance, clinician review, monitoring, and fail-safe workflow. Goals should prohibit cross-patient disclosure, require suggestions to remain linked to source patient and version, preserve human authorization for treatment, and provide safe fallback when unavailable. Evidence includes adversarial tenancy tests, provenance verification, clinical safety evaluation by authorized humans, failure drills, privacy audit, and update rollback. Review on new data use, model/version, supplier, region, endpoint, privilege, incident, regulation, or clinical workflow; no external medical validation is claimed by this chapter.
