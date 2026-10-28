---
module_id: SYSENG-006
program: Systems Engineering
level: 1
module_number: 6
title: Open and Closed Systems
status: complete
last_verified: 2026-08-30
---

# Open and Closed Systems

## One-Page Review

### Governing question

Which matter, energy, information, control, authority, resources, people, risk, and responsibility cross a chosen boundary—and when is treating a system as closed a valid analytical approximation rather than a hidden assumption?

### Essential definitions

- An **open system** exchanges one or more relevant quantities or influences with its environment across the selected boundary.
- A **closed system** excludes a specified class of exchange across a selected boundary for a stated interval and concern; closure is relative, not an unqualified label.
- In thermodynamics, a **closed system** can exchange energy but not matter, while an **isolated system** exchanges neither matter nor energy under the model.
- In control, **open-loop control** acts without using measured consequences to adjust the action; **closed-loop control** uses feedback. These terms describe control topology, not thermodynamic exchange.
- An **exchange** is a boundary-crossing transfer or influence, such as mass, energy, information, command, money, labor, authority, liability, or hazard.
- An **external input** is supplied by the environment; an **output** crosses outward; a **disturbance** affects behavior but is not selected as the control action.
- An **endogenous variable** is explained within the model; an **exogenous variable** is supplied from outside it.
- **analytical closure** means the model contains enough internal relations and specified external inputs to answer its question without an unexplained variable.
- A **selectively open** system permits some exchanges and constrains others through interfaces, membranes, policies, or controls.
- **dynamic boundary** means membership or permitted exchanges change by mode, lifecycle stage, configuration, or authority.
- A **balance residual** is the discrepancy between observed stock change and declared net boundary/internal flows; it is evidence of error, missing flow, or violated assumptions.

### Central model, mechanism, or theorem

For quantity $q$ inside boundary $B$:

$$
q(t_1)-q(t_0)=\int_{t_0}^{t_1}[in_q(t)-out_q(t)+create_q(t)-destroy_q(t)]dt.
$$

Define closure as a predicate:

$$
Closed(B,q,[t_0,t_1],m,c),
$$

where $m$ is operating mode and $c$ the concern. A system may be closed to matter during sealed operation, open to energy through heat transfer, open to information through telemetry, and closed to unauthenticated control. Honest analysis names every index and checks the balance or influence paths appropriate to the claim.

### Critical invariants

- Never call a system open or closed without naming boundary, exchange class, interval, mode, and concern.
- A black-box view hides internals; it does not imply environmental closure.
- Thermodynamic closure, feedback-loop closure, organizational openness, network isolation, and analytical closure are distinct concepts.
- Every declared stock balances against boundary flows and internal creation/destruction with compatible units.
- External does not mean negligible, random, or uncontrollable; internal does not mean fully controlled.
- Closure assumptions have owners, evidence, tolerances, and invalidation triggers.
- Interfaces can filter, authenticate, transform, buffer, meter, or reject exchange; selective permeability has failure modes.
- Normal, degraded, emergency, maintenance, update, and retirement modes can have different openness.
- Boundary choices must not erase exported harm, lifecycle obligations, or dependency.
- Model agreement establishes closure only to measurement resolution and stated alternatives.

### Common failures

Failures include calling an air-gapped computer closed while power, people, media, heat, and electromagnetic effects cross; calling feedback control thermodynamically closed; assuming a sealed enclosure is isolated; omitting supplier and operator exchanges; treating API access control as absence of information flow; hiding waste outside a product boundary; declaring a model closed because it runs without exceptions; using unexplained forcing data while claiming endogenous explanation; balancing average flows while stocks drift; ignoring leaks below sensor resolution; and keeping a normal-mode boundary during emergency or maintenance.

### Compact example

A rechargeable battery enclosure is closed to matter under a no-leak operating assumption, but open to electrical work and heat. Its management controller is closed-loop if voltage, current, and temperature feedback alter charging; it remains thermodynamically open. During venting, maintenance, or fire, the matter-closure assumption fails. “The battery is closed” is therefore incomplete and can support a dangerous analysis.

### Connections

Retrieve system boundary/context, elements/relationships, emergence, and feedback dynamics from Modules 001–005. Continue to complexity and uncertainty, assumptions and external dependencies, operational scenarios, and problem framing. Later interface, integration, safety, security, resilience, lifecycle, and systems-of-systems modules govern specific boundary exchanges.

## Governing Question

Every useful system model excludes most of the universe. Yet every operational system depends on some environment and affects it. Engineers need closure assumptions to calculate, test, and assign responsibility, but closure can become a convenient fiction that hides a dependency or exported consequence. How can a team state exactly what is allowed to cross a boundary and prove that the approximation is adequate for the decision?

The answer is indexed closure. Replace “the system is closed” with a testable statement such as: “During nominal sealed operation from initialization to service access, boundary B admits no intentional material flow above detection limit L, while electrical energy, heat, authenticated commands, telemetry, and mechanical load cross named interfaces.” The statement can be challenged by mode, quantity, evidence, and consequence.

## Why This Matters

Open-system reasoning prevents local optimization. A factory imports energy, material, information, labor, and capital and exports products, heat, waste, data, risk, and obligations. A cloud service imports identity, requests, configuration, supplier capability, and operator decisions and exports responses, telemetry, bills, and failure effects. Ignoring exchanges makes performance, safety, security, sustainability, or accountability appear better than the whole context supports.

Closed-system approximations are nevertheless essential. Conservation analysis encloses a control mass or volume. A test isolates a subsystem from uncontrolled inputs. A formal model treats some variables as constant. A security boundary denies classes of communication. The approximation is useful when omitted exchange is impossible, bounded below decision relevance, or separately modeled and monitored.

The word “closed” is overloaded. Thermodynamics distinguishes closed and isolated systems by matter and energy exchange. Control engineering distinguishes whether an action is adjusted using feedback. General systems theory describes organisms and organizations as open systems maintained through environmental exchange. Software engineers call a network isolated, a component encapsulated, a model self-contained, or a source ecosystem closed. These may coexist but are not interchangeable.

ISO/IEC/IEEE 15288:2023 frames a system of interest within a lifecycle and environment rather than prescribing absolute closure. SEBoK's open- and closed-system glossary entries reflect general-systems usage. ISO 15288 and the NASA handbook emphasize context, interfaces, external systems, lifecycle support, and validation in intended environments. The practical lesson is to model boundary interactions even when design authority ends at the line.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a boundary is selected for a concern and can differ across viewpoints;
2. an interface is a governed boundary-crossing relationship, not merely a line;
3. stocks change through flows, and balance equations require compatible units;
4. feedback is a causal path from consequences to later action;
5. a system property can depend on environmental and inter-element interaction;
6. external authority can constrain an internal design;
7. verification within a test enclosure differs from validation in operational context.

Take a laptop labeled “self-contained.” Enumerate power, heat, air, light, radio, peripherals, users, credentials, software supply, time, and legal/organizational control. Decide which exchanges matter for battery-life, confidentiality, usability, and repair questions. The boundary can remain the laptop while relevance changes by concern.

## Learning Objectives

After completing this module, you should be able to:

1. define open, closed, isolated, selectively open, endogenous, exogenous, and analytical closure;
2. distinguish thermodynamic closure from open-/closed-loop control;
3. state closure as a boundary-, quantity-, interval-, mode-, and concern-indexed claim;
4. construct matter, energy, information, and responsibility exchange inventories;
5. derive and audit a stock/flow balance residual;
6. identify hidden exchanges, exported consequences, and invalid closure assumptions;
7. model interfaces as selective filters with failure behavior;
8. reason about changing openness across lifecycle and operating modes;
9. design verification evidence for isolation and validation evidence for environmental adequacy;
10. use closure without erasing stakeholder, safety, security, sustainability, or support obligations.

## Core Exposition

**Begin with boundary and quantity.** Openness is meaningless without both. A greenhouse exchanges sunlight, heat, gases, water, organisms, information, labor, and money. It may be approximately closed to bulk plant matter during an experiment while open to energy and gas. A secure enclave can be closed to ordinary software reads while open to timing, power, faults, and privileged management.

Record an exchange tuple:

$$
e=(source,destination,q,interface,trigger,rate,quality,authority,mode,evidence).
$$

The exchange quantity $q$ includes more than physical substance. Systems engineering must track information, commands, responsibility, people, resources, risk, and lifecycle obligations where those alter outcomes. Conservation laws apply only to suitable quantities; responsibility and information need semantic rather than mass-balance models.

**Use thermodynamic terms precisely.** An open thermodynamic system exchanges matter and energy. A closed thermodynamic system exchanges energy but not matter. An isolated ideal exchanges neither. No real engineered isolation is absolute at arbitrary precision and duration. State tolerances and heat, radiation, leakage, or coupling assumptions.

A control volume can remain fixed in space while matter flows through. A closed control mass follows a fixed collection of matter while its shape changes. Choose the representation matching the calculation. Do not transfer thermodynamic definitions blindly to organizations or software.

**Separate control topology.** An open-loop washing timer runs a programmed duration without measuring cleanliness. A closed-loop temperature controller measures temperature and adjusts heat. Both appliances exchange energy, matter, information, and human action with the environment. Closing the control loop changes information/action relationships, not material closure.

Feedback can cross the system-of-interest boundary. A human observes an output and adjusts an input; the combined human-machine system has a closed loop even if the machine alone does not. State whose boundary defines the loop.

**Separate black-box abstraction.** Treating a supplier service as a black box means internal structure is hidden for the current model. Its requests, responses, failures, costs, policy, updates, and authority remain boundary exchanges. A black box can be highly open. Conversely, a white-box model can describe a materially closed vessel.

**Model analytical closure.** A quantitative model is analytically closed for question Q when it supplies equations/rules and initial/boundary conditions sufficient to determine or characterize its variables under declared external inputs. It can model an open physical system. Weather data may be exogenous; internal temperature is endogenous. The claim is not that weather is unimportant, but that its trajectory is supplied rather than explained.

Unexplained residuals indicate missing flow, measurement error, unmodeled creation/destruction, wrong timing, or boundary mismatch. They do not identify which explanation is true. Use residual magnitude, uncertainty, and pattern to investigate.

**Audit balances.** For a tank with initial mass $M_0$, deliveries $D$, withdrawals $W$, internal generation $G$, destruction $L$, and measured final mass $M_1$:

$$
residual=M_1-[M_0+D-W+G-L].
$$

Zero within uncertainty is consistent with the declared balance; it does not prove no hidden equal-and-opposite flows. Nonzero residual disproves at least one assumption if measurements and arithmetic are trusted.

The executable example audits a fuel inventory and classifies exchange claims. Declared flows predict 45 units, while measurement reports 42, leaving -3 units. The model cannot decide whether the cause is leakage, metering, timing, theft, evaporation, or recording error.

<!-- bijux-verify: {"id":"indexed-closure-and-balance","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"predicted_final=45.0\nmeasured_final=42.0\nresidual=-3.0\nbalance_closed=false\nbattery matter=closed energy=open information=open\nairgap matter=closed energy=open information=selective\nfeedback_controller thermodynamic=open control_loop=closed\nresidual_cause=undetermined\nevidence=declared_boundary_model_only\n","stderr":""}} -->
```python
initial = 100.0
deliveries = [20.0, 0.0, 15.0]
withdrawals = [30.0, 25.0, 35.0]
measured_final = 42.0
predicted_final = initial + sum(deliveries) - sum(withdrawals)
residual = measured_final - predicted_final

systems = {
    "battery": {"matter": "closed", "energy": "open", "information": "open"},
    "airgap": {"matter": "closed", "energy": "open", "information": "selective"},
}

print(f"predicted_final={predicted_final:.1f}")
print(f"measured_final={measured_final:.1f}")
print(f"residual={residual:.1f}")
print(f"balance_closed={str(abs(residual) < 0.01).lower()}")
for name, exchanges in systems.items():
    print(f"{name} matter={exchanges['matter']} energy={exchanges['energy']} information={exchanges['information']}")
print("feedback_controller thermodynamic=open control_loop=closed")
print("residual_cause=undetermined")
print("evidence=declared_boundary_model_only")
```

**Treat interfaces as selective permeability.** A firewall permits some packets, a membrane permits selected molecules, an airlock transfers people/material under conditions, and a review gate transfers authority/configuration. For each, specify allowed class, direction, state, authentication, rate, transformation, buffering, rejection, audit, failure, bypass, and emergency behavior.

Selective controls are themselves elements. A filter can clog, leak, misclassify, saturate, or be bypassed. An authentication gateway can fail open or closed, depend on time and identity providers, and export telemetry. “The boundary blocks X” requires evidence in normal and degraded configurations.

**Model semi-open systems.** Most engineered systems are intentionally open to value-producing exchanges and closed to harmful or unauthorized ones. A payment service accepts authorized instructions and returns outcomes; it should reject forged control while remaining observable and maintainable. Security is not maximum closure: updates, recovery, audit, and support need governed channels.

**Track dynamic boundaries.** During normal battery operation, the enclosure is sealed. During maintenance it opens to technician, tools, atmosphere, parts, and diagnostic information. During thermal runaway it vents matter and energy. During disposal, custody and hazardous-material flows dominate. One timeless label hides the most consequential modes.

Software boundaries also move. A service in normal mode accepts public requests through a gateway; incident mode grants emergency operator commands; migration mode dual-writes another store; retirement mode exports records and revokes credentials. Each mode needs authority and evidence.

**Include enabling systems.** Development tools, manufacturing, provisioning, training, calibration, maintenance, supply, incident response, and disposal cross the lifecycle boundary even if excluded from the delivered operational product. A device closed to field update may depend on depot reprogramming. Analyze the full support path before claiming autonomy or isolation.

**Include organizations and environments.** Open organizations obtain people, knowledge, funding, legitimacy, material, and demand and return products, services, waste, decisions, and effects. Policies and incentives alter exchanges. Organizational closure can preserve focus but block learning; excessive openness can overload decision and dilute accountability. These are qualitative system claims requiring contextual evidence, not thermodynamic equations.

**Avoid exported consequences.** Moving waste, risk, workload, privacy harm, emissions, or maintenance outside the procurement boundary does not remove it from stakeholder value. Maintain separate operational, legal, ecological, safety, and responsibility boundaries and trace crossings among them.

**Design isolation evidence.** Verify barriers, seals, access controls, protocol allowlists, energy coupling, emissions, side channels, bypass, maintenance ports, configuration, and monitoring to the required tolerance. Test faults and mode transitions. A negative observation establishes only that the test did not detect exchange above its capability.

**Design openness evidence.** Verify capacity, semantics, timing, quality, compatibility, authentication, consent, accessibility, and failure handling for desired exchanges. An interface that is “open” but unusable under load or inaccessible to stakeholders does not support the intended system outcome.

**Validate environmental adequacy.** A system verified under a closed test environment may fail when real users, weather, networks, suppliers, policies, and adversaries interact. Preserve controlled tests for causal evidence, then validate progressively representative environments with guardrails and rollback.

## Definitions and Notation

Let universe $U$ and system boundary $B\subset U$ be selected for concern $c$. Let $Q$ be exchange classes. For $q\in Q$, define boundary flows $F_q^{in}(t)$ and $F_q^{out}(t)$. A closure claim is:

$$
Closed(B,q,T,m,c;\epsilon)\iff
|F_q^{in}|+|F_q^{out}|\le\epsilon
$$

over interval $T$ in mode $m$, under a declared norm/aggregation and tolerance $\epsilon$. For forbidden discrete events, the rule may be zero accepted events rather than a magnitude.

An **isolated** thermodynamic ideal is closed to matter and energy. A **sealed** object is a physical design claim with leak rate/tolerance, not automatically isolation. An **air gap** excludes an intended network connection but does not exclude removable media, people, supply chain, power, electromagnetic coupling, acoustics, or every information path.

Let model variables be partitioned into endogenous $X$, exogenous $Z$, parameters $\theta$, and outputs $Y$:

$$
X_{t+1}=f(X_t,Z_t;\theta),\quad Y_t=g(X_t,Z_t).
$$

Analytical closure for a question requires rules, initial state, parameter values/ranges, and exogenous inputs sufficient for the requested inference. It does not make the represented physical system closed.

## Mechanisms, Invariants, or Proof Structure

Use this closure-analysis procedure:

1. **Name question and boundaries.** Include physical, functional, control, security, organizational, legal, ecological, and lifecycle views where relevant.
2. **Enumerate exchange classes.** Matter, energy, information, control, people, money, authority, responsibility, risk, waste, and support.
3. **Index by interval and mode.** Normal, degraded, emergency, maintenance, update, migration, and retirement.
4. **Specify interfaces and filters.** Direction, quantity, unit, semantics, capacity, condition, authority, failure, bypass, and evidence.
5. **Write balances or influence paths.** Use conservation where valid and semantic/causal models elsewhere.
6. **Classify endogenous/exogenous variables.** State why external forcing is adequate for the question.
7. **Measure residual and uncertainty.** Investigate discrepancies and alternative explanations.
8. **Challenge closure.** Test leak, side channel, common cause, operator action, supplier change, environment, and mode transition.
9. **Trace exported consequences.** Expand or relate boundaries until every material stakeholder/lifecycle effect is owned.
10. **Verify and validate.** Demonstrate isolation/selective exchange, then validate outcome in a representative environment.

Five invariants guide review.

**Indexing invariant.** Every openness/closure statement names boundary, exchange, interval, mode, concern, and tolerance.

**Balance invariant.** Conserved stocks reconcile with declared flows and uncertainty; residuals remain visible.

**Semantic invariant.** Terms from thermodynamics, control, organization, security, and modeling are not substituted across domains without definition.

**Lifecycle invariant.** Maintenance, emergency, evolution, and retirement exchanges are not excluded by nominal product scope.

**Evidence invariant.** Absence of detected exchange is bounded by test sensitivity, coverage, configuration, and duration.

## Alternatives and Trade-Offs

**Broad versus narrow boundary.** Broad boundaries expose consequences and dependencies but increase modeling/governance load. Narrow boundaries support tractable ownership but require explicit interfaces and external-effect analysis.

**Isolation versus connectivity.** Isolation reduces attack and dependency paths but impedes updates, monitoring, collaboration, and recovery. Governed connectivity adds value and exposure. Compare lifecycle behavior, not one diagram.

**Endogenous explanation versus exogenous forcing.** Endogenizing a variable can reveal feedback and policy effects. Treating it exogenously simplifies analysis. Promote variables when their response to the system can change the conclusion.

**Controlled test closure versus field realism.** Isolation improves repeatability and causal attribution. Representative environments reveal interaction. Use a ladder of evidence and keep claims tied to each setting.

**Fail closed versus fail open.** Denying action on uncertainty protects some security/safety objectives but can block emergency service. Permitting action preserves availability but increases unauthorized/hazard risk. Define per function, mode, and authority.

**Tight filtering versus graceful degradation.** Strict interface validation prevents invalid exchange but may make version skew unavailable. Tolerant readers preserve service but can hide semantic loss. Version contracts and observe rejected/degraded cases.

**Self-sufficiency versus external specialization.** Internal capability reduces supplier dependence but costs expertise and scale. External services add leverage and independent change. Model exit, substitution, outage, data, authority, and support.

## Failure Modes and Misconceptions

1. **Closed means no interaction.** Thermodynamic closed systems may exchange energy; other domains require explicit definitions.
2. **Closed-loop control means a closed system.** It describes feedback topology only.
3. **Black box means closed.** Hidden internals can still exchange extensively.
4. **Air-gapped means information-isolated.** People, media, emissions, power, and supply chains remain paths.
5. **Sealed means isolated.** Heat, radiation, load, and bounded leakage can cross.
6. **External means irrelevant.** External entities can dominate outcome and authority.
7. **No observed flow proves none exists.** Detection limits and duration bound the claim.
8. **A zero residual proves model completeness.** Equal missing flows or errors can cancel.
9. **A self-contained model explains its inputs.** Exogenous data may drive its result.
10. **Interfaces are passive holes.** Filters and gateways have state, policy, capacity, and failure.
11. **The operational boundary covers lifecycle.** Support and disposal use different systems and exchanges.
12. **Moving harm outside scope removes it.** Stakeholder and legal consequences cross procurement boundaries.

## Worked Examples

### Example 1

**Question:** Is a sealed rechargeable battery open or closed?

**Assumptions:** The boundary follows the production enclosure; the concern is normal charging over one hour; “closed to matter” means no measured mass transfer above the qualified leak-test threshold. The charger, cooling air, and supervisory controller are outside.

**Reasoning:** Charge and heat cross the enclosure even if no electrolyte or gas does. Voltage, current, and temperature observations cross to the controller, whose later command closes a control loop. Suppose mass is unchanged within a 0.1 g instrument uncertainty; that supports the qualified matter claim only for the tested state and interval. It does not establish absence of microleakage or cover pressure relief. When a service plug is removed or a relief vent opens, a permitted matter path changes the predicate's mode index. Energy conservation must therefore include electrical work and heat even while the matter balance has zero declared boundary flow.

**Evidence limit:** A seal qualification, mass measurement, pressure test, and mode/configuration record can support the claim. The label on the enclosure cannot.

**Conclusion:** The battery has different closure classifications by exchange and mode; an unqualified label is false precision.

### Example 2

**Question:** Does an air-gapped workstation have a closed information boundary?

**Assumptions:** The workstation has no installed network interface, sits in a controlled room, and signs artifacts that later leave on removable media. The concern is unauthorized disclosure or command during operation and maintenance.

**Reasoning:** Removing an intended live network edge closes one interface class. The state trace still includes an operator entering data, software arriving through provisioning, a clock and power source influencing execution, signed output leaving on media, and status appearing on a display. Electromagnetic, acoustic, optical, thermal, timing, or power effects may form side channels under the threat model. Each path needs a source, destination, direction, authority, rate or capacity, and mode. A media port that policy says “never use” is not absent; it is a selectively controlled path whose enforcement must be tested. Maintenance may temporarily introduce diagnostic equipment and a different authority set.

**Evidence limit:** Hardware inventory, radio survey, port configuration, custody records, procedure observation, emissions testing where required, and adversarial trials bound the claim. None proves information isolation against unstated channels or adversaries.

**Conclusion:** Air-gapping removes a class of connection; it does not prove information isolation or eliminate lifecycle exchange.

### Example 3

**Question:** Audit the fuel record with initial 100, deliveries 35, withdrawals 90, and measured final 42.

**Assumptions:** All quantities use the same corrected volume unit, the opening and closing readings refer to the same tank boundary, and deliveries and withdrawals use the same cutoff interval. No internal creation term is physically applicable; temperature correction and line inventory are initially assumed accounted for.

**Reasoning:** The declared transition is $100+35-90=45$. The observed transition ends at 42, so $r=42-45=-3$. The negative sign says observed stock is below the declared prediction. It is compatible with an omitted outward flow, overstated input, understated output, biased stock measurement, temperature conversion error, or timing mismatch. It is not uniquely diagnostic of theft or leakage. If the combined expanded uncertainty were 5 units, the discrepancy might be statistically unremarkable; if it were 0.5, investigation would be urgent. Plotting residuals by interval can distinguish persistent bias from event-correlated losses.

**Evidence limit:** Calibration, raw timestamps, temperature records, transfer tickets, line-fill state, uncertainty propagation, and independent reconciliation determine how strongly the residual challenges closure.

**Conclusion:** The nonzero residual falsifies the complete declared balance, not a specific explanation.

### Example 4

**Question:** A thermostat uses room temperature feedback. Is the room a closed system?

**Assumptions:** The control boundary contains sensor, thermostat logic, and heater; the thermal boundary contains room air and furnishings. Outdoor weather, occupants, ventilation, and power supply are external. The question concerns temperature regulation over a day.

**Reasoning:** At time $t$, measured temperature changes the heater command at $t+1$, so the control topology is closed-loop. Meanwhile, the room receives heater power, solar radiation, occupant/equipment heat, and supply air; it loses heat through envelope and exhaust. A defensible state equation contains these terms, for example $C\dot T=P_h+Q_{solar}+Q_{people}-UA(T-T_o)-Q_{vent}$. Omitting the environmental terms would predict that heater input accumulates indefinitely or that temperature never changes when the heater is off. Door opening is both a thermal disturbance and a human-system interaction.

**Evidence limit:** Loop logs can establish feedback behavior; heat-flow estimates, weather, occupancy, ventilation measurements, and model residuals establish the thermal claim. Evidence for one does not establish the other.

**Conclusion:** Control-loop closure coexists with strong thermodynamic and socio-technical openness.

### Example 5

**Question:** When is a supplier service a valid exogenous input rather than part of the model?

**Assumptions:** A local service calls a supplier scoring API. The first question is whether local transformation logic handles a fixed response trace correctly; the second is whether the product can meet a monthly service objective as demand varies.

**Reasoning:** For the first question, replayed supplier responses can be exogenous: the experiment deliberately holds them fixed and explains only local state transitions. For the service objective, call volume may trigger quotas, latency, price tiers, or supplier protection; degraded answers may change user retries and therefore future demand. That reciprocal path makes supplier behavior endogenous to the relevant model or demands bounded scenarios. Write the dependency as contract state—version, quota, latency distribution, failure semantics, data policy, change authority, and substitution lead time—not merely a constant “API available.” A sensitivity run can show whether plausible supplier variation crosses the decision threshold.

**Evidence limit:** Contract text, production observations, fault injection, quota tests, change history, and exit rehearsal bound the model. A successful replay validates only the local transformation under that trace.

**Conclusion:** Exogeneity is a question-specific modeling choice, invalid when reciprocal behavior can change the decision.

### Example 6

**Question:** Can a security gateway be both open and closed?

**Assumptions:** The gateway fronts a clinical status service. Normal reads require authenticated staff roles; writes require a smaller operator role; emergency responders may obtain a narrowly defined read capability. Identity, clock, policy distribution, and logging services sit outside its process boundary.

**Reasoning:** The gateway is open to messages satisfying transport, syntax, identity, authorization, rate, and state predicates. It is closed to disallowed operations only to the degree those predicates and every bypass enforce the policy. On identity-provider loss, denying all writes may be appropriate while an independently authenticated emergency read remains available; “fail closed” is therefore function-indexed. Responses, rejection details, timing, and logs are outbound information flows and can themselves leak or overload dependencies. Parser differences between gateway and backend can turn an apparently rejected representation into an accepted one.

**Evidence limit:** Policy-model review, configuration attestation, positive/negative contract tests, parser differential tests, dependency-loss exercises, rate saturation, bypass enumeration, and log/privacy review support the classification for a named version and threat model.

**Conclusion:** Security boundaries implement selective openness; useful service and protection are both boundary policies.

### Example 7

**Question:** A factory reports zero waste inside its production boundary. Is the production system waste-free?

**Assumptions:** The metric counts material remaining on the factory site at month end; contractors remove scrap and wastewater, while packaging and product leave through normal dispatch. The claim is presented as lifecycle environmental performance.

**Reasoning:** The site ledger can truthfully reach zero retained waste while recording large outward material flows. Transfer changes location and custody, not physical existence or stakeholder consequence. Build parallel boundaries: site operations, supply chain, product lifecycle, watershed/airshed, and legal responsibility. Reconcile purchased material into product, reusable inventory, emissions, effluent, scrap, and measurement residual. Then trace contractor treatment, recovery yield, secondary residues, transport, and final disposal. If hazardous material is embedded in product, end-of-life responsibility may be delayed rather than eliminated. A narrow operational metric cannot answer the broader claim.

**Evidence limit:** Weighbridge data, material composition, discharge monitoring, manifests, contractor assurance, chain of custody, recovery mass balance, and lifecycle assumptions are needed. A signed handoff proves custody transfer, not benign final outcome.

**Conclusion:** Boundary transfer is an exchange, not elimination; claims about sustainability require the relevant lifecycle boundary.

### Example 8

**Question:** A chamber test detects no moisture ingress for 24 hours. What closure claim is justified?

**Assumptions:** Ten production-representative enclosures are tested at a specified pressure, temperature, humidity, orientation, seal age, and assembly state. The method detects at least 0.2 g ingress over 24 hours with a declared false-negative rate.

**Reasoning:** A nondetection constrains exchange only above the method's capability in those samples and conditions. It does not establish a literal zero flow. If the service requirement is less than 1 g over five years with vibration, freeze-thaw cycling, repair, and pressure changes, the chamber evidence must be connected to those stressors by a qualified acceleration or degradation model. Sample variation matters: ten passing units weakly characterize a rare manufacturing defect. Inspection after testing can reveal whether the interface aged even without measured stock change.

**Evidence limit:** Calibration, blanks/controls, detection-limit study, sample provenance, environmental logs, seal configuration, statistical confidence, aging rationale, and post-test inspection define the supportable claim. Other fluids and maintenance modes remain outside it.

**Conclusion:** Negative evidence creates a bounded leak-rate claim, not absolute material closure.

### Example 9

**Question:** Why can closing an organization to external change reduce system fitness?

**Assumptions:** A platform organization freezes feature intake for a quarter to stabilize service. Operational telemetry continues, but customer research, support escalations, supplier notices, and regulatory review are also paused by an overbroad interpretation of the freeze.

**Reasoning:** Restricting work admission can protect capacity and reduce disruptive switching. Closing evidence channels is different: incidents, unmet user needs, dependency changes, and legal duties keep evolving. The organization emits product behavior that changes customer workflows, then stops observing the consequences; its internal model grows stale. Separate exchanges into work commitments, evidence, mandatory authority, operational control, and emergency escalation. Each can have distinct filters and response times. A triage record preserves learning without promising immediate delivery, while named decision rights prevent every external request from becoming work.

**Evidence limit:** Intake categories, queue age, rejected evidence, incident trends, customer outcomes, dependency changes, decisions, and model revisions show whether selective closure improved focus or merely suppressed feedback.

**Conclusion:** Organizational openness is a governed learning relationship, not unrestricted permeability or thermodynamic analogy.

### Example 10

**Question:** A medical infusion device works in a closed laboratory test. What remains before operational validation?

**Assumptions:** Bench verification used a reference fluid path, simulated patient load, trained engineer, stable mains power, approved consumables, and isolated network. The intended use includes clinical staff, varied patients, interoperating systems, transport, cleaning, alarms, maintenance, and emergencies.

**Reasoning:** The laboratory boundary removes variability so failures can be attributed and requirements checked. Validation asks whether the integrated socio-technical system achieves safe intended use. Progressively introduce representative drug libraries, accessories, users, lighting/noise, gloves, network latency/loss, electromagnetic conditions, battery depletion, occlusion/air faults, alarm competition, cleaning, shift handoff, cybersecurity events, and emergency override. Trace every new exchange to an authority, acceptance criterion, observation method, and rollback. A successful nominal bench run supplies no evidence about a clinician interpreting an alarm under workload or a malformed library update crossing the configuration boundary.

**Evidence limit:** Simulation, human-factors, interoperability, environmental, fault, security, maintenance, and appropriately governed field evidence support different claims. No external clinical, regulatory, academic, or practitioner review is claimed here.

**Conclusion:** Controlled closure supports verification and causal evidence; representative openness is essential to validate intended use and risk.

## Cross-Program Connections

- [Network Engineering](../../24-network-engineering/ROADMAP.md) defines communication paths, segmentation, filtering, and external network behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) engineers trust boundaries, attack surfaces, information flow, isolation, and controlled administration.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) models open interactions among independently failing and evolving nodes.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) governs selectively open service contracts and compatibility.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) designs organizational and technical interfaces between platform and consuming teams.
- [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) realizes network, identity, resource, tenancy, and supplier boundaries.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, May 2023. Consulted 2026-08-30.
2. SEBoK Editorial Board. [Open System](https://sebokwiki.org/wiki/Open_System_%28glossary%29), *Guide to the Systems Engineering Body of Knowledge*, version 2.13 glossary. Consulted 2026-08-30.
3. SEBoK Editorial Board. [Closed System](https://sebokwiki.org/wiki/Closed_System_%28glossary%29), *Guide to the Systems Engineering Body of Knowledge*, version 2.13 glossary. Consulted 2026-08-30.
4. Ludwig von Bertalanffy. *General System Theory: Foundations, Development, Applications*. George Braziller, revised edition, 1968.
5. Donella H. Meadows. *Thinking in Systems: A Primer*. Chelsea Green, 2008.
6. Karl J. Åström and Richard M. Murray. [*Feedback Systems: An Introduction for Scientists and Engineers*](https://press.princeton.edu/books/hardcover/9780691193984/feedback-systems), second edition, Princeton University Press, 2021. Consulted 2026-08-30.
7. NASA. [*NASA Systems Engineering Handbook*, Rev. 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Consulted 2026-08-30.
8. International Union of Pure and Applied Chemistry. [*Quantities, Units and Symbols in Physical Chemistry (Green Book)*](https://iupac.org/what-we-do/books/greenbook/), abridged fourth edition, RSC Publishing, 2023. Consulted 2026-08-30.

## Exercises

### Exercise 1

Classify a greenhouse as open, closed, or selectively open for matter, energy, information, control, people, and finance across normal operation, storm emergency, maintenance, and retirement.

### Exercise 2

A reservoir begins at 500 ML, receives 80 ML rainfall/runoff and 25 ML transfer, supplies 70 ML, loses an estimated 12 ML to evaporation, and measures 518 ML at the end. Compute the residual and list competing explanations.

### Exercise 3

Diagnose the claim “our offline signing system is closed because it has no network card.” Produce an exchange inventory and verification plan.

### Exercise 4

Compare a tightly isolated industrial controller with a remotely managed controller across safety, security, update, observability, recovery, supplier, and lifecycle concerns.

### Exercise 5

Design boundaries and closure evidence for a biocontainment laboratory information-and-control system. Separate physical, biological, information, control, organizational, emergency, and lifecycle claims and named human authority.

## Answers to the Exercises

### Answer 1

In normal operation the greenhouse is open to solar/electrical energy, heat, water, gases, nutrients, information, control, labor, organisms under policy, products, waste, and finance. It may be selectively closed to pests, unauthorized people/control, contaminated material, and rain through the enclosure. A storm changes water, wind, debris, power, and emergency-control flows. Maintenance opens panels/enclosure to technicians, tools, parts, software, atmosphere, and waste. Retirement exports plants, substrate, structure, hazardous/electronic material, records, credentials, and responsibility.

A strong answer states boundary, direction, units/semantics, filters, authorities, failure modes, tolerances, and evidence for each exchange. “Closed greenhouse” can only be a quantity- and mode-specific approximation.

### Answer 2

Predicted final stock is $500+80+25-70-12=523$ ML. Measured final is 518 ML, so residual is $-5$ ML. Explanations include underestimated evaporation/seepage, unrecorded release or abstraction, rainfall/runoff error, transfer/supply metering bias, boundary storage omitted, timing mismatch, or final-level conversion error. Quantify each measurement's uncertainty and covariance before deciding whether 5 ML is significant. A zero corrected residual would be consistent with the balance but would not prove no offsetting missing flows.

### Answer 3

The missing network card removes one intended communication interface. Inputs include removable media, keyboard/console, power, time, firmware and manufacturing supply chain, operator procedure, keys, and maintenance tools. Outputs include signed artifacts, displays, media writes, logs, timing, power/electromagnetic/acoustic emissions, heat, and disposed hardware. People and custody transfer information and authority.

Verification covers hardware/configuration inventory, disabled radios/ports, boot chain, media workflow, malware controls, key generation/storage/use/destruction, role separation, physical access, tamper evidence, side-channel requirements, power/time dependencies, logging, backup/recovery, maintenance, and adversarial procedure tests. The claim must name threat model, modes, tolerance, duration, and external assurance; “no NIC” is not analytical closure.

### Answer 4

Isolation reduces remote attack and dependency paths and can make control behavior independent of WAN failure. It complicates vulnerability intelligence, patching, telemetry, fleet visibility, remote expertise, evidence collection, and recovery; removable-media and physical-maintenance paths remain. Remote management improves observability, coordinated updates, support, and recovery but adds identity, network, management-plane, supplier, credential, and compromise dependencies.

Compare hazard response, fail-open/closed policy, authenticated update, rollback, local safe control, monitoring, incident authority, bandwidth loss, credential expiry, supplier outage, fleet configuration, maintenance burden, and decommissioning. A hybrid can keep safety control local while using a constrained, mediated, auditable maintenance channel. Validate both normal benefit and adversarial/degraded behavior.

### Answer 5

Physical/biological boundaries cover rooms, pressure zones, air, samples, organisms, personnel, waste, decontamination, equipment, power, and environmental release. Information boundaries cover sample identity, results, access, audit, research/clinical/privacy rules, networks, media, backups, suppliers, and retention. Control boundaries cover ventilation, interlocks, alarms, access, equipment, safe shutdown, manual override, and emergency authority. Organizational boundaries cover operators, biosafety, facilities, security, IT, researchers, health services, regulators, responders, suppliers, and waste handlers.

Evidence includes pressure/airflow and filter tests, containment challenge, interlocks, sensor calibration, alarm and response exercises, identity/access and information-flow tests, configuration and signed updates, backup/recovery, power/network loss, maintenance transfer, spill/fire/evacuation modes, decontamination, custody, waste, incident reporting, and retirement. Automation cannot establish biological risk acceptability, legal sufficiency, emergency authority, worker/community legitimacy, or model completeness. No external biosafety, regulatory, academic, or practitioner review is claimed. Named biosafety, laboratory, occupational health, facilities, controls, software, cybersecurity/privacy, waste, emergency, human-factors, and regulatory authorities must review the safety case, evidence independence, residual risk, procedures, training, operation, and change.
