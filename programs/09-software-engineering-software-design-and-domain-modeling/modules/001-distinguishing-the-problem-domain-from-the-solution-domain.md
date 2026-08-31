---
module_id: SDDM-001
program: Software Engineering: Software Design & Domain Modeling
level: 1
module_number: 1
title: Distinguishing the Problem Domain from the Solution Domain
status: complete
last_verified: 2026-08-28
---

# Distinguishing the Problem Domain from the Solution Domain

## One-Page Review

### Governing question

Which facts describe the world in which a need exists, and which decisions describe the software chosen to address that need? A sound design preserves this distinction long enough to test whether the proposed machine can actually produce the required change in its environment.

### Essential definitions

- **Problem domain:** the relevant part of the world: people, organizations, physical processes, rules, concepts, events, constraints, and existing systems.
- **Problem:** a gap between an observed or possible condition and a desired condition for stakeholders.
- **Requirement:** an externally meaningful condition or effect that a satisfactory system must achieve or respect.
- **Domain assumption:** a proposition about the environment on which the requirement-to-solution argument depends.
- **Solution domain:** the designed machine and its implementation choices: components, data structures, protocols, storage, algorithms, interfaces, and deployment mechanisms.
- **Shared phenomenon:** an event, state, or value observable at the boundary between machine and environment.
- **Model:** a purposeful abstraction used to answer stated questions; it is neither the world nor automatically the implementation.

### Central model, mechanism, or theorem

Let (W) denote relevant domain properties and assumptions, (S) a machine specification, and (R) the required effect in the world. The central adequacy obligation is:


$$
W \land S \models R.
$$


The formula is an argument shape, not a promise that every project uses formal logic. It asks reviewers to show why the machine behavior, when composed with credible environmental properties, entails the desired outcome. A solution that satisfies its own tests but relies on a false (W) does not solve the problem.

### Critical invariants

- Requirements state effects or constraints at an observable boundary; implementation tasks state means.
- Domain facts remain true independently of the proposed software; design decisions are replaceable choices.
- Every required effect needs a causal path through phenomena the machine can sense or influence.
- Every relied-upon assumption needs evidence, an owner, and a consequence if false.
- A model's vocabulary must identify its context; the same word may denote different concepts elsewhere.
- Traceability is bidirectional: a design element should serve an accepted need, and each accepted need should have a realization and verification route.

### Common failures

Common failures include writing technology choices as requirements, treating stakeholder requests as verified needs, modeling database tables before domain concepts, assuming the machine can observe hidden facts, confusing a user-interface gesture with the user's goal, and declaring success from internal state while the external outcome remains unknown.

### Compact example

A library wants fewer loans to become overdue. “Send an email 24 hours before the due time” is a proposed solution, not the problem. Relevant domain facts include due-time policy, borrower contactability, renewals, returns, and the meaning of “overdue.” The required effect might be “a borrower with an active loan is given a usable reminder opportunity before the due time.” Email, SMS, an app notification, or a printed notice are alternative mechanisms. The design argument must state assumptions such as address validity and delivery latency; it must not equate “message queued” with “borrower reminded.”

### Connections

This is the entry module; the broader prerequisite expectations are recorded in the [curriculum dependency model](../../../DEPENDENCY_AND_SEQUENCE.md). [SDDM-002](../ROADMAP.md) refines the problem side into stakeholders, goals, and observable outcomes. [SDDM-003](../ROADMAP.md) develops domain language. System-wide allocation belongs later to the [Software Architecture program](../../12-software-engineering-software-architecture/ROADMAP.md), while physical storage belongs to the [Database Engineering program](../../18-database-engineering/ROADMAP.md).

## Governing Question

How can an engineer determine whether a statement belongs to the problem domain or the solution domain, preserve the necessary connection between them, and avoid turning an early implementation guess into an unquestioned definition of success?

The distinction is analytical, not a command to finish all “requirements” before any design. Discovery and design inform each other. A prototype may reveal that an assumed workflow never existed; a proposed data structure may expose an ambiguous identity rule. The discipline is to label what kind of claim is being made and to revise both models deliberately. The current requirements standard treats requirements work as life-cycle activity rather than a one-time document: ISO lists processes and information items spanning systems, software, products, and services ([ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html)).

## Why This Matters

Software is judged in two worlds. Compilers, unit tests, schemas, and service monitors observe properties of the machine. Stakeholders care about effects in an organization or physical environment. A payment service can return HTTP 200 while charging the wrong legal entity. A scheduler can produce a conflict-free timetable that violates a labor agreement. A medical alarm can set an internal flag while failing to attract a clinician's attention. Internal correctness is necessary but does not establish external adequacy.

Michael Jackson's “world and machine” framing makes the boundary explicit: software engineering must describe the world, describe the machine, and argue across their interface rather than deny the world's independent properties ([Jackson 1995](https://doi.org/10.1145/225014.225041)). IEEE's current SWEBOK requirements topics likewise separate requirements sources, analysis, technology constraints, system requirements, software requirements, and derived requirements ([SWEBOK v4.0a topics](https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics)).

The distinction also controls cost and reversibility. A legal retention period is a domain constraint until the law or business context changes. Choosing PostgreSQL table partitioning is a solution decision that should be replaceable without redefining retention. If both are recorded as “the database keeps rows in monthly partitions for seven years,” reviewers cannot tell which part is mandatory, which is merely one mechanism, or what evidence would permit change.

Finally, boundaries protect collaboration. Domain experts can challenge whether a model reflects actual work. Engineers can compare mechanisms. Testers can derive observations at both interfaces. Operators can distinguish “the system performed its action” from “the environmental outcome occurred.” Product owners can change desired outcomes without accidentally prescribing an architecture.

## Prerequisites and Retrieval

This Level-I module assumes ordinary programming experience and familiarity with functions, state, data, tests, and client-server interaction. No prior domain-driven-design terminology is required.

Before continuing, retrieve these ideas:

1. A program maps inputs and prior state to outputs and new state, but the meaning of those values comes from an environment.
2. An abstraction omits detail for a purpose; omission is useful only when the omitted detail cannot change the answer to the model's question.
3. Verification asks whether an artifact satisfies a specification. Validation asks whether the selected specification and artifact address the intended need.
4. A necessary condition must hold for success; a sufficient set of conditions establishes success under stated assumptions.
5. Correlation is not causation. Observing an internal event after a desired outcome does not prove that event caused the outcome.

If any item is unfamiliar, construct a tiny example before proceeding: name a real-world goal, one observable measure of it, and one implementation mechanism. Then ask which facts would remain if that mechanism were replaced.

## Learning Objectives

After completing this module, you should be able to:

- classify statements as domain fact, stakeholder goal, requirement, assumption, specification, design decision, implementation detail, or evidence;
- draw a context boundary showing the machine, relevant external domains, and shared phenomena;
- transform a proposed feature into an outcome-oriented requirement without discarding useful design information;
- write and challenge an adequacy argument of the form $W \land S \models R$;
- detect inaccessible phenomena, circular definitions of success, and solution-shaped vocabulary;
- compare multiple solutions against the same problem model;
- trace requirements to design mechanisms and observed evidence in both directions;
- explain when iterative movement between problem and solution models is productive rather than confused.

## Core Exposition

The **problem domain** is not “everything outside the code.” It is the smallest part of the world that must be understood to justify the system. For a railway-door controller it may include train motion, platform position, door state, passengers, operator commands, and safety rules. Weather may be irrelevant until ice affects sensors. Payroll may be organizationally nearby but outside this problem. Relevance is determined by the required effects and failure risks.

A **problem** combines present or possible conditions, desired conditions, affected stakeholders, and constraints. “We need Kubernetes” is not yet a problem. “Teams wait a median of nine days for a compliant test environment, causing releases to miss regulated review windows” is closer: it identifies an observed condition, an impact, a population, and a constraint. The problem statement may still be wrong; it is now testable.

A **requirement** constrains acceptable outcomes or observable system behavior. It should not hide the actor, object, temporal condition, exceptional cases, or verification route. “Use Redis” is a technology constraint only if an authorized source truly imposes it; otherwise it is a candidate design. “A customer must see a confirmed reservation within two seconds of an accepted booking request, excluding declared maintenance windows” states an observable service property, though terms such as “accepted” and “confirmed” still need definition.

The **solution domain** contains the machine to be built and the choices by which it will behave: state representation, algorithms, interfaces, consistency mechanisms, vendor services, deployment topology, and operational policy. A solution specification should be precise enough to verify independently, yet connected to requirements through an explicit argument.

The boundary is crossed by **shared phenomena**. A sensor reports temperature; a user submits a request; a service emits a response; an actuator changes a valve; a bank confirms settlement. The machine cannot base a guarantee on a domain fact it cannot observe, and it cannot cause an outcome through a phenomenon it cannot control or influence. This yields two review questions:

1. **Observability:** what boundary event or state gives the machine justified knowledge?
2. **Controllability:** what boundary action can the machine take, and what domain property connects that action to the desired effect?

<!-- bijux-verify: {"id":"world-machine-boundary","mode":"schematic","language":"text","toolchain":"none","reason":"the block is a context diagram whose arrows denote shared phenomena, not an executable program"} -->
```text
Borrower --return/renew request--> Reminder Machine
Borrower <--notice presentation---- Reminder Machine
Catalogue --loan and due state----> Reminder Machine
Clock --------current time--------> Reminder Machine
Policy -------due-time rules------> Reminder Machine

Required world effect: borrowers receive a usable opportunity to act before due time.
Machine evidence: notice accepted by a delivery channel.
Remaining assumption: channel acceptance usually leads to timely human presentation.
```

The diagram exposes an epistemic gap. Channel acceptance is observable to the machine; human attention may not be. The requirement must not silently replace “presented to a person” with “queued to a provider.” The team may add read receipts, a second channel, escalation, or a weaker claim. None eliminates uncertainty; each changes the evidence and assumptions.

Models serve questions. A domain model might represent `Loan`, `DueTime`, and `RenewalEligibility` because those concepts explain policy. A solution model might represent `loans` rows, an index on `due_at`, and a queue partition key because those choices explain execution. Similar names do not make the models identical. Conversely, implementation-only objects such as connection pools have no domain counterpart and need none.

The distinction is also temporal. A statement can move categories when authority changes. “Use the existing identity provider” may begin as a provisional design preference. If a regulator-approved security boundary and organizational contract make it mandatory, it becomes a genuine solution constraint sourced in the domain. Engineers should record the source and review date rather than argue from vocabulary alone.

Problem and solution work therefore proceed as disciplined iteration:

1. frame an outcome and boundary;
2. identify relevant domains and phenomena;
3. state assumptions and requirements;
4. propose a machine specification;
5. test the adequacy argument with examples and counterexamples;
6. revise the problem model when design exploration reveals missing facts;
7. revise the design when the argument depends on false or fragile assumptions.

Requirements and architecture therefore co-evolve, but that does not erase their different claim types. Iteration is useful precisely because each side can challenge the other.

## Definitions and Notation

Let:

- (D) be the selected problem-domain boundary;
- (W) be propositions about (D), including stable domain properties and explicit assumptions;
- (R) be required effects or constraints expressed over phenomena in (D);
- (M) be the machine boundary;
- (S) be the specification of (M)'s behavior at shared phenomena;
- (I) be an implementation intended to realize (S);
- (E) be collected evidence.

Three judgments must not be collapsed:

1. **Implementation verification:** $I \models S$. The implementation conforms to its machine specification under the verification model.
2. **Problem adequacy:** $W \land S \models R$. In a world satisfying the stated properties, the specified machine behavior entails the required effect.
3. **Assumption validation:** evidence (E) supports treating (W) as credible for the intended context.

The notation (models) means semantic entailment: every interpretation satisfying the premises also satisfies the conclusion. In ordinary projects, the premises may be structured prose, state models, examples, simulations, and testable contracts rather than a fully formal theory. The obligation still disciplines reasoning.

Important claim types are:

- **Domain fact:** descriptive and independently true or false in the environment.
- **Goal:** a preferred world condition, often broad and negotiable.
- **Requirement:** a necessary condition on an acceptable system or outcome.
- **Assumption:** an unguaranteed environmental proposition relied upon by the argument.
- **Constraint:** a restriction on permissible solutions or outcomes, with an authoritative source.
- **Specification:** prescribed machine behavior at its boundary.
- **Design decision:** a selected internal structure or mechanism with alternatives.
- **Implementation detail:** a concrete realization below the current design abstraction.
- **Evidence:** an observation supporting a claim, always bounded by method and environment.

“Business rule” is not automatically a domain fact. It may be a law, a company policy, an implementation workaround, or a habit. Authority and change mechanism determine its classification.

## Mechanisms, Invariants, or Proof Structure

The core mechanism is an **adequacy case** connecting need to machine behavior. A compact review table is:

| Element | Question | Typical evidence |
|---|---|---|
| Outcome | What condition should differ in the world? | stakeholder decision, baseline measure |
| Boundary | Which domains and interfaces can affect that outcome? | context diagram, observation |
| Requirement | What must be true for an acceptable result? | scenarios, acceptance criteria |
| Assumption | What environmental behavior is relied upon but not controlled? | policy, measurement, experiment |
| Specification | What will the machine sense, decide, and cause? | state model, contract, executable example |
| Verification | Does implementation conform to specification? | tests, analysis, inspection |
| Validation | Does the composed system address the outcome? | field observation, trial, outcome measure |

The decisive invariant is **category traceability**: no arrow in the argument changes a claim's type silently. A queue acknowledgment can verify a messaging specification; it cannot by itself validate human comprehension. A database uniqueness constraint can enforce one machine representation of identity; it cannot decide whether the domain regards two records as the same person.

A second invariant is **causal reachability**. Construct a directed graph whose nodes are relevant domain states and shared phenomena. Every required change must have a path beginning with something the machine can observe or control and ending at the required state. Every edge needs a mechanism or explicit assumption. Missing edges identify wishful requirements; weak edges identify operational risk.

A third invariant is **replaceability of means**. If two candidate solutions (S_1) and (S_2) both satisfy $W \land S_i \models R$, then the problem statement should allow both unless an authorized constraint excludes one. A statement that admits only the first idea may be overspecified.

The adequacy argument is defeasible because (W) may change. Review it with:

- a normal scenario that demonstrates the intended causal chain;
- a boundary case at each threshold or timing edge;
- a counterexample in which the specification holds but the requirement fails;
- an adversarial case that violates a relied-upon assumption;
- an alternative solution to test whether the requirement is solution-neutral;
- production evidence that can confirm or revise the assumptions.

## Alternatives and Trade-Offs

**Solution-first prototyping** is valuable when uncertainty concerns feasibility or human interaction. It produces concrete evidence quickly. Its danger is anchoring: the prototype's fields and screens become the domain vocabulary before the need is understood. Preserve the learning by recording which assumption each prototype tests.

**Document-first requirements** can create a stable review baseline in regulated or multi-supplier contexts. ISO/IEC/IEEE 29148 specifies requirements processes and information-item content without requiring one life-cycle model. The danger is treating document approval as evidence that environmental assumptions are true.

**Domain-driven design** emphasizes a model and language shaped through collaboration with domain experts. Eric Evans's reference definitions make clear that a model is a selectively simplified knowledge structure and that bounded contexts delimit where a model applies ([DDD Reference](https://domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)). The trade-off is effort: rich modeling is justified where conceptual complexity drives risk, not for every CRUD screen.

**Problem frames** emphasize the machine, problem-world domains, requirements, interfaces, and frame concerns. They are strong when physical or organizational causality matters. They can feel formal for small information systems, but their questions about observability and shared phenomena remain useful.

**User stories and jobs-to-be-done** foreground actor value and context. They are good discovery devices but do not alone specify invariants, failure behavior, or machine boundaries. A story can coexist with a context model and precise acceptance obligations.

**Data-model-first design** is efficient when the domain is already well understood and the work is genuinely data-centric. It is hazardous when tables prematurely merge concepts, encode workflow as nullable columns, or let storage identity define domain identity. Physical database design remains a downstream choice owned by Database Engineering.

The correct trade-off is not “analysis versus agility.” It is the cost of explicit reasoning versus the risk of learning through failure. Safety, irreversibility, high coordination cost, and weak observability justify more explicit problem modeling.

## Failure Modes and Misconceptions

1. **“The stakeholder asked for it, so it is a requirement.”** A request is evidence of a perspective. Competing stakeholders, law, feasibility, and actual work may contradict it.
2. **“The problem domain contains no technology.”** Existing systems, protocols, and mandated providers may be real environmental constraints. The question is whether they are given for this decision.
3. **“The solution domain is only code.”** Operational procedures, configuration, deployment, training, and organizational controls can be parts of the designed intervention.
4. **“Domain model equals object model.”** A domain model may use prose, equations, events, decisions, or state machines. Objects are one representation.
5. **“A requirement must never mention implementation.”** Genuine constraints may mandate technologies. The source and reason must be explicit so the constraint can be challenged or retired.
6. **“Problem and solution work happen in separate phases.”** They co-evolve. Their claims must remain distinguishable even when work alternates rapidly.
7. **“Passing acceptance tests proves the problem is solved.”** Tests establish specified observations in tested conditions. Outcome validation may require field evidence.
8. **“The database is the domain.”** Stored data is a representation selected for a purpose. It may omit tacit, temporal, probabilistic, or contested facts.
9. **“All assumptions are bad.”** Engineering always relies on assumptions. Hidden, ownerless, or untested assumptions are bad.
10. **“More realistic models are always better.”** A model should be adequate for its questions. Extra detail increases coupling and review burden.

## Worked Examples

### Example 1

**Situation:** A manager says, “The requirement is to build a mobile app for warehouse picking.”

**Reasoning:** “Mobile app” selects a solution class. Ask what observable condition motivates it. Interviews and timing data show pickers walk to fixed terminals to learn the next location, producing idle travel and stale instructions. A problem statement is: “Pickers need current, location-specific work instructions at the point of work without returning to a fixed terminal.” Relevant domain facts include gloves, connectivity gaps, barcode labels, safety zones, and task reassignment. Candidate solutions include rugged handhelds, wearable displays, cart-mounted terminals, or printed batch routes. “Must operate with gloved hands” may be a genuine interface constraint; “must use iOS” needs an authoritative source.

**Conclusion:** Preserve the mobile-app proposal as a candidate, but validate it against point-of-work access, environmental constraints, and alternatives.

### Example 2

**Situation:** A reservation service marks a booking `confirmed=true` after inserting a row, but the venue can reject the allocation asynchronously.

**Reasoning:** The Boolean is a solution-domain representation. In the problem domain, confirmation means the venue has committed capacity under the applicable policy. The machine can observe its database insert but not venue commitment until a boundary message arrives. If the requirement is “never tell a customer that uncommitted capacity is confirmed,” then a local insert cannot justify the outward status. The design needs states such as `requested`, `venue_accepted`, and `rejected`, or it needs a synchronous commitment protocol. A timeout is not rejection unless the venue contract says so.

**Conclusion:** Name machine states after justified knowledge, not desired world states; otherwise implementation vocabulary conceals an observability gap.

### Example 3

**Situation:** A tax rule states that orders below 100 monetary units pay no regional surcharge and all other orders pay 5%, rounded to two decimal places.

**Reasoning:** The threshold, rate, applicable order amount, currency, and rounding rule are domain claims. A pure function is one possible executable specification. Boundary tests at 99.99 and 100.00 check the discontinuity; 0 checks the lower boundary. Integer minor units avoid binary floating-point ambiguity in this example.

<!-- bijux-verify: {"id":"surcharge-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"0\n500\n0\norder amount cannot be negative\n","stderr":""}} -->
```python
def surcharge_minor_units(order_minor_units: int) -> int:
    if order_minor_units < 0:
        raise ValueError("order amount cannot be negative")
    if order_minor_units < 10_000:
        return 0
    return (order_minor_units * 5 + 50) // 100

print(surcharge_minor_units(9_999))
print(surcharge_minor_units(10_000))
print(surcharge_minor_units(0))
try:
    surcharge_minor_units(-1)
except ValueError as error:
    print(error)
```

The run verifies these observations in the recorded Python environment. It does not prove that the interpreted policy, tax base, or rounding convention is legally correct.

**Conclusion:** Separate policy interpretation from executable mechanism, and test boundary values where the domain rule changes behavior.

### Example 4

**Situation:** A team says, “Users must log in before viewing an invoice,” but invoices are also delivered by a signed one-time link.

**Reasoning:** “Log in” is a mechanism. The likely domain requirement is that only an authorized principal can access an invoice and that access is auditable. Session authentication and a constrained capability link are alternative solutions with different risks. The problem model must define principal, authority, delegation, expiry, revocation, and disclosure. If policy explicitly prohibits bearer capabilities, that prohibition is a sourced constraint; otherwise rejecting the link merely because it is not “login” confuses means with ends.

**Conclusion:** Restate the security objective and authority rules, then compare mechanisms rather than treating one interaction as the goal.

### Example 5

**Situation:** A hospital requests an alert whenever a measured value crosses a threshold.

**Reasoning:** The machine can observe a sensor reading, but the clinical concern may depend on trend, patient condition, sensor quality, and clinician acknowledgment. A threshold alert specification can be verified while still producing alarm fatigue or missing deteriorations. Domain assumptions include calibration, sampling frequency, association of sensor to patient, and staff response. The causal path is reading → detection → delivery → perception → assessment → intervention. The software controls only some edges.

**Conclusion:** Model the full outcome path, make uncontrolled edges explicit, and define evidence separately for detection, delivery, acknowledgment, and clinical response.

### Example 6

**Situation:** An online store has `customer_id` in every order row, so engineers conclude that “customer” is already modeled.

**Reasoning:** The column records a storage reference. Domain questions remain: Can a guest become a registered customer? Can legal identities merge? Does an order belong to an account, a purchaser, a recipient, or all three? Must historic invoices retain the identity at purchase time? The correct domain concepts may require several identities and temporal facts. Conversely, if all the system needs is delivery to a supplied address with no continuity obligations, a rich `Customer` entity may be unnecessary.

**Conclusion:** A stored identifier is evidence of a solution representation, not proof that the relevant domain identity and continuity rules are understood.

### Example 7

**Situation:** A fraud model automatically blocks transactions with score at least 0.9. Product documentation says, “Fraudulent transactions are blocked.”

**Reasoning:** Fraud is a world classification that may be known only after investigation; score is a model output. The implementation controls a policy action based on the score. The accurate specification is “transactions with score ≥ 0.9 at decision time are blocked,” while the goal is to reduce fraud loss subject to false-positive and fairness constraints. Evidence must track calibration, drift, appeal outcomes, and costs. Calling the score “fraud probability” also requires a validated probabilistic interpretation.

**Conclusion:** Do not let a predictive proxy become the definition of the domain fact it estimates.

### Example 8

**Situation:** A team must decide whether a notification rule belongs in code or configuration.

**Reasoning:** The domain rule is “orders awaiting regulated approval must alert the responsible role after four business hours.” Code versus configuration is a solution choice. The choice depends on change frequency, authority, validation, deployment controls, audit needs, and expressive power. A configuration store may improve policy responsiveness but create a second programming language with weaker tests. Hard-coded logic may be safer for rare, reviewed changes but slower to amend. Both can satisfy the same requirement if their governance differs appropriately.

**Conclusion:** Compare implementation mechanisms against rule authority and change economics without relocating the rule's meaning into the storage mechanism.

### Example 9

**Situation:** A team claims success because 99.9% of reminder jobs finish within one minute.

**Reasoning:** This metric verifies machine processing latency. The problem outcome may be timely action by recipients. Relevant measurements form a chain: jobs scheduled, channel accepted, message presented, recipient acted, undesirable outcome avoided. Each later measure is harder to attribute and may need privacy safeguards or experiments. The processing SLO is still valuable—it constrains one mechanism—but should not be relabeled “reminder effectiveness.”

**Conclusion:** Use layered evidence and name each metric after what it directly observes.

### Example 10

**Situation:** Two teams propose solutions for reducing duplicate supplier payments: a database uniqueness constraint and a review workflow.

**Reasoning:** The domain must define duplicate: same invoice number within supplier, same economic obligation under different numbers, corrected invoice, installment, or malicious replay. A uniqueness constraint is strong for exact normalized keys but may reject legitimate reuse or miss semantic duplicates. A review workflow handles ambiguity but adds latency and human error. A combined design can use deterministic constraints for provable duplicates, similarity detection for candidates, and authorized adjudication for contested cases. Its adequacy depends on supplier identity quality and correction policy.

**Conclusion:** A precise problem model enables composition of mechanisms; premature solution choice would encode an incomplete definition of “duplicate.”

## Cross-Program Connections

- **Programming Languages & Semantics:** observable behavior gives a formal vocabulary for what clients can distinguish, but the domain supplies the meaning of observations.
- **Testing & Quality Engineering:** verification evidence concerns artifacts and specified behavior; validation evidence concerns fitness for the intended problem.
- **Software Architecture:** architecture allocates responsibilities after significant domain forces and system qualities are understood. This chapter does not select system-wide structures.
- **Database Engineering:** schemas and constraints realize selected facts; they do not independently establish domain meaning, identity, or authority.
- **Security Engineering:** assets, adversaries, and trust boundaries are problem-domain elements; authentication, cryptography, and policy engines are solution mechanisms.
- **Systems Engineering:** environment, stakeholders, system boundary, and operational context extend beyond software and help reveal non-software interventions.

## References

- Michael Jackson. “The World and the Machine.” *Proceedings of the 17th International Conference on Software Engineering*, 1995, pp. 283–292. DOI [10.1145/225014.225041](https://doi.org/10.1145/225014.225041). Publication identity checked 2026-08-28.
- Eric Evans. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003; concise definitions in [Domain-Driven Design Reference, 2015](https://domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf). Checked 2026-08-28.
- ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018, Systems and software engineering—Life cycle processes—Requirements engineering](https://www.iso.org/standard/72089.html), edition 2, published 2018-11, confirmed 2024 and current published edition on 2026-08-28; ISO reports revision activity.
- Hironori Washizaki, ed. [*Guide to the Software Engineering Body of Knowledge*, v4.0a](https://www.computer.org/education/bodies-of-knowledge/software-engineering/v4). IEEE Computer Society, 2024, minor revision identified 2025-09-25; current page checked 2026-08-28.
- A. Peterson and Jay Stanley Jr. [*Mapping a Domain Model and Architecture to a Generic Design*](https://www.sei.cmu.edu/library/mapping-a-domain-model-and-architecture-to-a-generic-design/). CMU/SEI-94-TR-008, Software Engineering Institute, 1994. Record checked 2026-08-28.

## Exercises

### Exercise 1

Classify each statement and justify the classification: (a) “Invoices are legally retained for seven years”; (b) “Store invoice PDFs in object storage”; (c) “A customer can dispute a charge within 60 days”; (d) “The service returns `202 Accepted`”; (e) “Most customers have a reachable email address.” Use the categories domain fact or constraint, requirement, assumption, specification, and design decision. State any ambiguity that prevents a unique answer.

### Exercise 2

A school wants to “automatically improve attendance” by sending a message when a student is absent. Construct (W), (S), and (R) for this proposal. Trace the causal path from attendance observation to improved attendance and identify at least three edges the machine cannot guarantee.

### Exercise 3

A parcel system declares delivery when a courier taps “Delivered.” Diagnose the modeling defect. Propose machine states and boundary evidence that distinguish courier assertion, geolocation evidence, recipient acknowledgment, and adjudicated delivery. State what your design still cannot prove.

### Exercise 4

Compare two solutions for limiting access to a research dataset: a network allowlist and identity-aware authorization. Hold the problem statement constant. Analyze assumptions, observability, controllability, failure modes, change cost, and evidence. Recommend when each is adequate.

### Exercise 5

Transfer the method to a non-software intervention. A factory wants fewer hand injuries and initially requests a reporting dashboard. Frame the problem, identify relevant domains and shared phenomena, propose at least one software and one non-software solution, and outline an adequacy argument without claiming that correlation proves injury reduction.

## Answers to the Exercises

### Answer 1

(a) is a domain constraint only if a named law or policy actually governs these invoices; otherwise it is an unverified assertion. (b) is a design decision because other storage mechanisms can satisfy retention. (c) is a domain rule or requirement depending on whether it describes existing authority or a desired system obligation; source, jurisdiction, and the meaning of “within” are missing. (d) is a machine specification at an HTTP boundary, not the stakeholder outcome. (e) is an assumption requiring measured evidence, population definition, and expiry. A strong answer explicitly refuses to classify statements solely by grammar and asks who has authority, what remains true without the proposed machine, and what is observable.

### Answer 2

One possible (R) is “for enrolled students in the intervention population, unjustified absence days decrease without increasing unsafe attendance or privacy harm.” (W) includes correct enrollment, timely and accurate absence recording, reachable guardians or students, comprehension, ability to act, and a causal relationship between reminders and attendance. (S) observes a recorded absence, applies eligibility and privacy policy, sends a message through an approved channel, and records channel acceptance. The path is physical absence → staff observation → record entry → machine detection → message submission → channel delivery → human perception → interpretation → feasible action → future attendance. The machine cannot guarantee accurate initial observation, human perception, ability to act, or the behavioral effect. Evaluation therefore needs both mechanism metrics and a defensible outcome study with confounders considered.

### Answer 3

The defect is equating a courier's assertion with the domain fact of delivery. Suitable states might be `in_transit`, `courier_asserted_delivery`, `evidence_collected`, `recipient_acknowledged`, `disputed`, and `adjudicated_delivered`. Evidence can include event time, location with an accuracy bound, package scan, image under privacy policy, signature, recipient acknowledgment, and later dispute resolution. No combination automatically proves the correct person received an undamaged parcel: sensors can be wrong, credentials shared, recipients unavailable, and evidence fraudulent. The outward claim should reflect the strongest justified state, and policy should define who can adjudicate disputes.

### Answer 4

The stable problem is to permit approved principals and deny others under a defined dataset policy. An allowlist assumes network location is a reliable proxy for principal and that address administration is timely; it observes source addresses and controls network admission. It is simple and useful for a tightly controlled enclave but weak for shared networks, roaming users, compromised hosts, and per-record policy. Identity-aware authorization assumes trustworthy identity proofing, credential lifecycle, policy attributes, and enforcement at every path; it offers finer decisions and audits but adds provider dependency and policy complexity. Use an allowlist as one defense for a stable isolated environment, not as proof of user authority. Prefer identity-aware controls where principals, purposes, or entitlements vary, often combined with network restriction. Evidence must include negative tests, revocation, bypass analysis, and audit completeness.

### Answer 5

Frame the outcome as a reduction in defined hand-injury incidence and severity for specified operations without displacing risk or suppressing reports. Relevant domains include workers, machines, guards, materials, procedures, training, shifts, maintenance, incentives, and incident reporting. Shared phenomena include machine state, guard position, task start, near-miss report, and injury record. A software solution might detect guard bypass and stop a machine, relying on sensor integrity and safe-stop mechanics. A non-software solution might redesign a fixture so hands cannot enter the hazard zone, supported by training and inspection. A dashboard observes reports but may not alter exposure and can worsen incentives. An adequacy case links each intervention to reduced hazardous contact under explicit assumptions. Evaluation uses leading measures, near misses, exposure hours, and injury outcomes; a before/after correlation alone is insufficient because workload, reporting, staffing, and product mix may change.
