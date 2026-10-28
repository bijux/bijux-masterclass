---
module_id: SARCH-040
program: Software Engineering: Software Architecture
level: 1
module_number: 40
title: Choosing a Style from Forces Rather Than Fashion
status: complete
last_verified: 2026-09-06
---

# Choosing a Style from Forces Rather Than Fashion

## One-Page Review

### Governing question

How can architects select, combine, and revisit architectural styles from stakeholder forces, quality scenarios, constraints, risks, and evidence instead of labels, popularity, or vendor defaults?

### Essential definitions

- An **architectural style** is a family of systems characterized by element and relationship types plus constraints on their composition.
- A **force** is a contextual pressure that shapes a decision: desired outcome, constraint, workload, risk, organizational condition, or lifecycle concern.
- A **quality-attribute scenario** states stimulus, source, environment, affected artifact, required response, and response measure.
- A **constraint** removes choices rather than merely preferring one, unless it is negotiable and explicitly treated as such.
- An **alternative** is a coherent candidate architecture with boundaries, data, interactions, deployment, ownership, operations, and migration—not a technology name.
- A **trade-off** occurs when improving one concern changes another concern adversely under the relevant assumptions.
- A **risk** is an uncertain condition with consequence; a **sensitivity point** is a decision whose change strongly affects a quality response; a **trade-off point** affects several qualities in competing ways.
- **Pareto dominance** means one alternative is no worse on every assessed criterion and better on at least one.
- A **fitness function** is an automated or repeatable check that supplies bounded evidence about an architectural property.
- **Option value** is the value of preserving a feasible future choice under uncertainty.

### Central model, mechanism, or theorem

Let alternatives be $A$, scenarios be $Q$, hard constraints be $H$, and evidence be $E$. First eliminate any $a\in A$ that violates a proven hard constraint. For remaining candidates, reason scenario by scenario:

$$
Utility(a)=\sum_{q\in Q}w_q u_q(a),\qquad \sum_{q\in Q}w_q=1,quad w_q\ge0.
$$

This weighted model is a discussion instrument only when scales, weights, interactions, uncertainty, and thresholds are made explicit. Perform sensitivity analysis, examine Pareto dominance, record risks and missing evidence, and prefer the simplest candidate that satisfies required scenarios with acceptable residual risk and migration cost. No aggregate score can rescue a constraint violation or replace judgment.

### Critical invariants

- frame the system, stakeholders, lifecycle, environment, and decision scope before naming styles;
- translate qualities into measurable scenarios and identify hard constraints separately;
- include a credible status quo, modular alternative, distributed alternative, and hybrid where relevant;
- specify each alternative as a whole operating architecture, not a slogan;
- trace claimed benefits through style constraints and mechanisms to scenario responses;
- expose costs in data, failure, security, delivery, operations, organization, and migration;
- use comparable assumptions, workload, boundaries, and evidence across alternatives;
- reject dominated or infeasible choices before optimizing preferences;
- test sensitivity to weights, estimates, thresholds, growth, and correlated failure;
- label measurements, calculations, prototypes, expert judgments, and unresolved uncertainty distinctly;
- choose reversibility and option value deliberately; do not postpone irreversible risks behind “agility”;
- record the decision, rejected alternatives, evidence, triggers, owner, and review date.

### Common failures

Frequent failures include choosing microservices “for scale” without workload; adopting event-driven architecture for every interaction; calling cloud or containers an architecture; comparing a detailed favorite to vague straw alternatives; assigning weighted scores without scale definitions; averaging away a failed constraint; double-counting correlated benefits; assuming quality attributes are independent; ignoring migration and on-call cost; treating a proof of concept as production evidence; composing styles without naming boundaries; maximizing option value forever; mistaking industry frequency for local fit; and retaining a decision after its assumptions have changed.

### Compact example

A 12-person team owns a billing product with one regional deployment, strong transactional invariants, moderate predictable load, and a quarterly integration need. A modular monolith with explicit billing modules, an outbox, and a coarse partner API satisfies release, consistency, and integration scenarios. Twenty microservices would add remote transactions, deployments, identities, and on-call surfaces without a required independent scaling or ownership benefit. The choice can be revisited if teams, workloads, or regulatory isolation change.

### Connections

[SARCH-031](031-layered-architecture.md) through [SARCH-039](039-microservices-architecture.md) supply candidate style families and their constraints. [SARCH-041](../ROADMAP.md) next begins data and integration structure with system-of-record boundaries. Earlier quality-attribute, trade-off, risk, view, and decision-record modules supply the evaluation method.

## Governing Question

Architecture discussions often begin with a fashionable answer: microservices, event streaming, serverless, a mesh, a lakehouse, or “clean architecture.” Labels compress experience, which is useful, but they also hide assumptions. The same style can solve one system's dominant forces and create another system's largest risks.

A responsible choice starts with context and observable needs. It builds coherent alternatives, derives how each responds, checks constraints, gathers evidence, and records uncertainty. The goal is not to identify the universally best style. It is to make a defensible local decision that can be tested and revisited.

## Why This Matters

Style choices shape source dependencies, runtime interactions, deployment units, data authority, trust, latency, failure propagation, team ownership, and operating cost. They are expensive to reverse once public contracts, data, organizational structure, and infrastructure accumulate.

Fashion-driven choices often deliver symbolic compliance: services that release together, events that behave like RPC, layers bypassed through shared data, or plugins with full host privilege. A structured evaluation exposes whether the mechanism that produces the claimed quality actually exists.

The method also prevents false certainty. Estimates are incomplete, scenarios conflict, and organizations change. By recording assumptions, sensitivity, residual risks, and review triggers, architecture becomes a governed learning process rather than a permanent declaration.

## Prerequisites and Retrieval

Retrieve stakeholder, system context, scope, force, constraint, assumption, quality attribute, scenario, workload, style, tactic, mechanism, alternative, trade-off, risk, sensitivity, evidence, prototype, benchmark, model, threshold, dominance, reversibility, migration, total cost of ownership, fitness function, decision record, and review trigger.

From SARCH-003 and SARCH-010 retrieve system context and problem framing; SARCH-004 through SARCH-007 provide qualities and trade-offs; SARCH-011 and SARCH-012 provide evidence and risk; SARCH-019 provides decisions under uncertainty; SARCH-021 through SARCH-028 provide multiple architectural views; and SARCH-031 through SARCH-039 provide the style families evaluated here.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish style, tactic, technology, pattern, deployment model, and product;
2. convert vague quality goals into measurable architectural scenarios;
3. distinguish hard constraints, thresholds, preferences, assumptions, and uncertainties;
4. construct coherent comparable alternatives including status quo and hybrid choices;
5. derive benefits and costs from mechanisms rather than names;
6. apply elimination, Pareto, weighted, sensitivity, and risk reasoning with stated limits;
7. select prototypes, models, tests, and operational evidence appropriate to disputed claims;
8. evaluate style composition across module, runtime, deployment, data, trust, and ownership views;
9. include migration, reversibility, option value, and lifecycle cost in decisions;
10. record a decision with evidence, residual risk, ownership, and review triggers.

## Core Exposition

**Separate the decision vocabulary.** A style constrains element and relationship types: layered systems constrain dependency direction; pipe-and-filter constrains staged transformation; client-server assigns request roles; event-driven systems communicate facts and reactions; microkernels define a core and extensions; services define contract boundaries. A tactic is a narrower response such as retry, cache, redundancy, or authentication. A technology realizes some mechanisms. A vendor product bundles many choices.

Choosing Kubernetes is not choosing microservices. Choosing a broker is not choosing event-driven semantics. A modular monolith can run in containers and publish events. State each decision at the level where its consequences occur.

**Frame the system of interest.** Name the product or subsystem, users, external systems, owners, environments, lifecycle, and decision horizon. A company can use different styles at different boundaries. A batch analytics pipeline, interactive transaction core, plugin ecosystem, and partner API may coexist.

Define what is out of scope. Otherwise every enterprise concern contaminates one decision and no alternative can be evaluated consistently. Record dependencies whose behavior is assumed rather than controlled.

**Elicit forces before solutions.** Forces include functional outcomes, quality scenarios, regulatory duties, existing assets, skills, budgets, deadlines, organization, data gravity, partner constraints, and uncertainty. Ask what changed or is painful. “We need microservices” may conceal release contention, uneven load, acquisition integration, or a desire for team autonomy; each points to different remedies.

Rank forces with stakeholders, but preserve disagreement. A product owner may prioritize feature lead time while operators prioritize recovery and finance prioritizes cost. Architecture resolves a feasible balance; it does not make conflict disappear.

**Turn qualities into scenarios.** “Scalable,” “secure,” and “maintainable” are not testable. A performance scenario might say: during a seasonal peak of 2,000 checkout requests/s, when one recommendation dependency is slow, accepted checkout requests complete at the edge within 700 ms at the 99th percentile while optional recommendations may be omitted.

The scenario identifies source, stimulus, environment, artifact, response, and measure. It reveals candidate tactics: admission, bounded calls, optional dependency, cached projection, scaling, or workload separation. It does not dictate microservices.

ISO/IEC 25010:2023 supplies a current product-quality model and vocabulary [1]. Use such models to prompt omissions, not as a universal list or weighting scheme. The relevant qualities, definitions, and measures remain system-specific.

**Distinguish hard constraints from preferences.** A legal prohibition on moving identified data outside a jurisdiction may eliminate an architecture. A preference for one cloud may be negotiable. Label provenance and authority: law, contract, policy, budget, physical limit, or stakeholder preference.

Challenge purported constraints respectfully. “Must use vendor X” can be a signed contract, sunk-cost argument, or personal habit. A hard constraint has an owner and evidence. If uncertain, evaluate contingent alternatives rather than silently treating it as fact.

**Establish thresholds before scoring.** Some scenarios have minimum acceptable response: no unauthorized actuation, recovery within four hours, or deadline below one second. Alternatives failing a true threshold are infeasible even if excellent elsewhere. Weighted averages must not let low cost compensate for violating safety or law.

Thresholds also prevent endless optimization. Once an alternative meets needed latency, further speed may be worth less than simplicity, recoverability, or cost. Utility functions can represent this, but plain threshold reasoning is often clearer.

**Construct whole alternatives.** “Monolith versus microservices” is too vague. A useful alternative specifies capability boundaries, module dependencies, runtime interactions, data authority, transactions, messages, deployment units, scaling, trust, ownership, delivery, observability, failure, recovery, and migration.

Give each candidate comparable detail. Include the status quo repaired with focused tactics; it often dominates a rewrite. Include a hybrid when forces genuinely differ, such as a modular transaction core plus isolated image workers and durable integration events.

**Avoid straw alternatives.** A detailed preferred design will always beat “keep legacy.” Repair each alternative enough to be credible. Apply the same workload, growth, staffing, security, and budget assumptions. If evidence quality differs, record that uncertainty instead of assigning false precision.

Architecture trade-off methods such as ATAM use stakeholder scenarios to identify risks, sensitivity points, and trade-offs [2]. The durable practice is collaborative causal analysis, not ceremonial scoring.

**Trace benefits through mechanisms.** For every claimed response, write a causal chain:

force or scenario $\rightarrow$ style constraint $\rightarrow$ mechanism or tactic $\rightarrow$ predicted response $\rightarrow$ evidence.

“Microservices scale better” is incomplete. A defensible chain identifies a partitionable image workload, an isolated deployment and queue, independent worker scaling, measured throughput per worker, and a capacity model. A monolith with a separate worker pool may offer the same scaling at lower cost.

**Expose recurring costs.** Distribution creates latency, serialization, ambiguous outcomes, version coexistence, identity, certificates, retries, queues, telemetry, and on-call burden. Event-driven designs create duplicates, lag, ordering, schema evolution, and progress diagnosis. Plugins create compatibility, authority, and lifecycle risk. Layers add indirection and can become bypassed bureaucracy.

Include development, delivery, runtime, support, security, compliance, data migration, training, vendor exit, and retirement. Initial implementation is a small portion of architecture lifecycle cost.

**Use elimination before optimization.** Remove alternatives that violate proven hard constraints or lack a required mechanism. If data cannot leave an isolated site during disconnection, a cloud-only synchronous design is infeasible regardless of its weighted score. If a plugin must execute untrusted native code, in-process loading may fail a memory-isolation threshold.

Do not invent constraints to eliminate an unpopular choice. Document the precise conflict and whether a mitigation changes the alternative enough to restore feasibility.

**Use Pareto reasoning.** Alternative $a$ dominates $b$ when it is at least as good on every assessed criterion and strictly better on one, under the same assumptions. Dominated alternatives can be removed unless they preserve an unmodeled option or have materially different uncertainty.

Often several alternatives remain on a Pareto frontier: one is cheaper, another recovers faster, another preserves release independence. Stakeholders must make a value judgment. Architecture can make the consequences explicit but cannot derive values from technology.

**Use weighted models cautiously.** A weighted sum can structure discussion. Define each criterion's scale and direction, normalize consistently, and avoid double-counting correlated concepts such as deployability, lead time, and team autonomy. Do not multiply ordinal labels as though intervals were measured.

Weights can hide vetoes and uncertainty. Record ranges rather than point estimates where appropriate. Keep raw scenario results beside the score so readers can see why two totals are equal.

**Perform sensitivity analysis.** Vary weights, estimates, workload, and thresholds. If a small change reverses the winner, the decision is sensitive and requires stronger evidence or a reversible path. If one alternative wins across plausible ranges, the decision is robust to that uncertainty.

For two alternatives with utilities $u_1,u_2$ on criterion one and $v_1,v_2$ on criterion two, solve the break-even weight rather than arguing about arbitrary scores. Sensitivity points deserve monitoring after release.

**Represent uncertainty.** Classify inputs as measured, derived, source-backed, expert judgment, assumption, or unknown. Give estimates ranges and confidence. Unknowns with high consequence become risks or experiments. Avoid adding decimal places that source evidence cannot support.

A prototype can reduce technical uncertainty; a stakeholder workshop can reduce semantic uncertainty; a threat model can expose adversarial paths; a migration rehearsal can test operational feasibility. Match the method to the claim.

**Design decisive experiments.** A proof of concept should compare the disputed mechanism under representative conditions. To test whether separate workers isolate image load, measure interactive latency and recovery while workers saturate and crash. A hello-world deployment only proves the tool starts.

State environment, data, versions, workload, expected result, stopping rule, and limitations. Negative evidence matters. A prototype that fails a threshold can eliminate an alternative; one successful run cannot prove universal behavior.

**Model performance end to end.** Allocate latency across admission, queues, calls, processing, storage, and response. Required sequential stages add necessary budgets. Required fan-out is constrained by the slowest branch plus coordination. Percentiles do not generally add as scalars.

Measure the likely bottleneck and saturation. Independent scaling helps only when work and state partition. Moving a shared database bottleneck behind 40 services changes topology, not capacity.

**Model availability and failure structure.** Draw required and optional dependencies, common infrastructure, regions, queues, fallbacks, and manual paths. A product of component availability values assumes independent required-series behavior; correlated identity, DNS, network, or deployment failures invalidate that simplification.

Evaluate failure containment by consequence. Separate processes can isolate crashes but not shared database corruption, retry storms, or invalid domain commands. A fallback that uses the same failing dependency is not independent.

**Model data and consistency.** Identify each datum's authority, writers, readers, transactions, replicas, freshness, retention, privacy, migration, and recovery. Style choices often fail at data: microservices share tables, events lack authoritative meaning, or caches hide stale safety decisions.

Prefer boundaries that keep strongly coupled invariants local. If distribution is justified, specify coordination, compensation, reconciliation, and unknown outcomes. Do not use “eventual consistency” without convergence and user-impact policy.

**Model security and trust.** Draw principals, workloads, administrators, third parties, networks, stores, brokers, gateways, and plugins. State authentication, authorization, delegation, data purpose, keys, audit, revocation, and isolation. More boundaries can reduce privilege scope but also multiply credentials and attack surface.

A centralized gateway can enforce common edge controls but cannot own every domain authorization. A service mesh can secure channels but does not validate business semantics. A sandbox can limit plugin mechanisms but not make dangerous authorized output harmless.

**Model organizational feasibility.** Count ownership surfaces, deployment pipelines, on-call rotations, technologies, contracts, and incident handoffs. A style that requires 20 autonomous teams cannot be realized by one small group using a shared release and support queue.

Organizations can evolve, but the transition is part of the alternative. Training, hiring, platform construction, and new decision rights have cost and lead time. Conway's law makes communication structure relevant evidence [3].

**Compose styles at named boundaries.** Most systems use several styles. A layered modular monolith can expose client-server APIs, publish events through an outbox, run pipe-and-filter analytics, and host bounded plugins. Composition is sound when each view names elements, connectors, data authority, trust, deployment, and ownership.

Styles can conflict. Layering may be bypassed by event consumers writing shared tables. A plugin inside a service can defeat process isolation. An orchestrator can centralize what service boundaries meant to decentralize. Review interactions, not only each style separately.

**Prefer the simplest sufficient architecture.** Simplicity means fewer concepts, authorities, failure modes, deployment surfaces, and coordination mechanisms consistent with required scenarios. It does not mean minimal files or ignoring future change.

Do not optimize only for today's build effort. A simple architecture can preserve clean module boundaries and data ownership, giving future extraction options. Premature distribution spends option value on recurring complexity.

**Consider reversibility and option value.** Reversible choices can be made with less evidence and shorter review. Irreversible public contracts, destructive migrations, proprietary data formats, and organizational commitments need stronger evidence. Preserve seams where uncertainty and consequence justify them.

Option value is not a reason to build every abstraction. An unused generic layer has carrying cost and may constrain future choices incorrectly. Preserve a specific credible option with an owner and trigger.

**Include migration as architecture.** Compare paths, not just target states. A sound target may be infeasible if cutover, data authority, coexistence, rollback, or regulatory evidence cannot be achieved. Identify incremental steps that leave the system coherent.

Use branch-by-abstraction, facades, outboxes, parallel comparison, strangler seams, or data backfill only with explicit ownership and stop conditions. Avoid indefinite dual writes or duplicate authorities. Measure migration progress by retired risk, not new component count.

**Record the decision.** An architecture decision record should capture context, decision, alternatives, rationale, evidence, assumptions, consequences, residual risks, owner, date, and review triggers. Link scenarios and experiment results. Do not rewrite history when the decision changes; supersede it with a new record.

The record is not proof. It makes reasoning reviewable and supports learning. A decision can be correct under old assumptions and wrong after workload, regulation, organization, or technology changes.

**Define fitness functions and operating evidence.** Automate properties that have reliable proxies: forbidden dependency edges, cross-schema writes, contract compatibility, deployment independence, latency budgets, recovery rehearsals, vulnerability policy, or ownership metadata. Each check states what it observes and what it cannot prove.

Operational evidence tests predictions. Compare actual lead time, failure propagation, cost, saturation, recovery, and user outcomes with the decision. Avoid vanity measures such as service count, event volume, or deployment frequency without value and reliability context.

**Set review triggers.** Revisit when a threshold is missed, a key assumption changes, ownership splits, workload grows, regulation changes, dependencies become unavailable, or migration stalls. Also review at a bounded date if uncertainty persists.

Do not continuously churn stable architecture for novelty. A trigger initiates evidence review, not automatic replacement. Retaining the choice can be the correct documented outcome.

**Recognize social and market pressure.** Conference frequency, hiring narratives, analyst categories, and vendor roadmaps are context, not local proof. They may affect skill availability or product support, which are legitimate forces. Translate them into evidence rather than treating popularity as technical merit.

Fashion is especially dangerous when success stories omit scale, team count, failure history, or migration cost. Ask which forces matched, which did not, and what evidence transfers.

## Definitions and Notation

Let alternatives be $A=\{a_1,\ldots,a_m\}$ and quality scenarios be $Q=\{q_1,\ldots,q_n\}$. Hard constraints $H$ are predicates $h(a)$ that must all hold. Feasible set is

$$
F=\{a\in A\mid \forall h\in H,\ h(a)=true\}.
$$

For $a\in F$, normalized scenario utility $u_q(a)$ and nonnegative weight $w_q$ may form $U(a)=\sum_q w_q u_q(a)$ with $\sum_qw_q=1$. This assumes scales are commensurable enough for the stated decision and interactions are addressed separately.

Alternative $a$ Pareto-dominates $b$ over assessed criteria when $u_q(a)\ge u_q(b)$ for every $q$ and the inequality is strict for at least one $q$. Uncertainty intervals can prevent a confident dominance claim.

For risk $r$, record probability or likelihood evidence $p_r$, consequence $c_r$, exposure model if used, mitigation, owner, and residual uncertainty. $p_rc_r$ is only meaningful when scales and assumptions support multiplication.

Let decision record $D$ contain context, alternatives, decision, evidence, assumptions, consequences, risks, owner, and triggers. A trigger is a predicate over observed context that initiates review; it does not automatically reverse $D$.

## Mechanisms, Invariants, or Proof Structure

**Scope invariant.** Every style decision names the system boundary, stakeholders, environments, lifecycle, and time horizon. Evidence outside that scope is not silently generalized.

**Feasibility invariant.** Every selected alternative satisfies each proven hard constraint. Preference aggregation cannot compensate for infeasibility.

**Comparability invariant.** Alternatives use the same scenario definitions, workload, growth, ownership, security, and cost assumptions or state the difference explicitly.

**Causal-trace invariant.** Every claimed quality response identifies a style constraint, mechanism, predicted response, and evidence. A label alone supplies no causal proof.

**Dominance argument.** If $a$ is no worse than $b$ on every assessed criterion and strictly better on one, selecting $b$ cannot improve any assessed criterion under those assumptions. Retaining $b$ requires an unassessed value, different uncertainty, or correction of the model.

**Sensitivity invariant.** A recommendation whose winner changes under small plausible input variation is labeled sensitive. It requires stronger evidence, mitigation, or a reversible path.

**Evidence invariant.** Source authority, model, calculation, prototype, test, and production observation are labeled with environment and limits. Successful observation is not universal proof.

**Composition invariant.** When styles combine, module, runtime, deployment, data, trust, and ownership mappings remain mutually consistent. A constraint in one style is not bypassed accidentally by another.

**Lifecycle invariant.** Selection includes migration, coexistence, rollback, operation, and retirement. A target-state diagram alone is incomplete.

**Review invariant.** Assumptions, residual risks, owner, and triggers are recorded. Changed evidence initiates review without erasing the original rationale.

## Alternatives and Trade-Offs

| Style family | Primary forces it can address | Recurring costs and risks | Warning evidence |
|---|---|---|---|
| Layered | dependency direction, replaceable technical concerns, comprehension | indirection, bypass, horizontal change | every feature crosses every layer and rules are unenforced |
| Modular monolith | strong internal boundaries with local calls and transactions | shared process, deployment, and coarse scaling fate | private data is shared or modules are only folders |
| Hexagonal/onion | domain isolation from volatile adapters and frameworks | ports proliferate; indirect code | abstractions have no credible variation or domain policy leaks outward |
| Pipe-and-filter | staged transformation, reuse, parallel or streaming processing | representation conversion, backpressure, error and state coordination | filters share hidden state or cannot operate independently |
| Event-driven | temporal decoupling, fan-out, audit, asynchronous reaction | duplicates, lag, ordering, schemas, progress and failure diagnosis | commands are mislabeled as facts or delivery implies completion |
| Client-server | centralized capability and authority for many clients | latency, partial failure, version skew, availability dependency | timeout is treated as rollback or session state pins instances |
| Microkernel/plugin | variable features around a stable core | compatibility, trust, lifecycle, resource, and ecosystem governance | plugins access internals or the core contains every optional policy |
| Service-oriented | heterogeneous integration, explicit enterprise capabilities and contracts | mediation gravity, distributed transactions, central governance | bus owns business logic or services mirror legacy tables |
| Microservices | independent team release, scaling, privilege, and selected fault boundaries | distributed data, delivery, security, testing, and on-call multiplication | shared writes, lockstep releases, chatty calls, no accountable owner |
| Hybrid | different styles for different forces and boundaries | interaction complexity and inconsistent assumptions | no view maps how the styles compose |

## Failure Modes and Misconceptions

1. **“Best practice determines the style.”** Practices have contexts; local forces and evidence decide applicability.
2. **“A style name is an alternative.”** A coherent alternative includes data, deployment, ownership, operation, and migration.
3. **“Cloud-native is a style.”** It is a broad ecosystem and operating posture, not one structural constraint set.
4. **“Microservices solve scale.”** Workload, bottleneck, partition, state, and independent scaling mechanism decide.
5. **“Events decouple everything.”** Schema, meaning, delivery, ordering, and lifecycle remain dependencies.
6. **“A weighted score makes the choice objective.”** Weights, scales, interactions, uncertainty, and thresholds contain judgment.
7. **“High totals can offset any weakness.”** Hard constraints and unacceptable risks are not averageable.
8. **“More criteria improve rigor.”** Correlated or irrelevant criteria double-count preferences and obscure decisions.
9. **“A proof of concept proves production fitness.”** It supports only tested mechanisms in its environment.
10. **“The most reversible choice is always best.”** Delaying a safety or regulatory boundary can be the larger irreversible risk.
11. **“Hybrid means compromise without discipline.”** A hybrid is valid when styles own named boundaries and compose coherently.
12. **“The target state is the decision.”** Migration, coexistence, rollback, operation, and retirement are architectural.
13. **“Industry adoption is local evidence.”** It matters only through transferable forces such as skills or support.
14. **“Architecture must maximize future flexibility.”** Options have carrying cost and uncertain relevance.
15. **“Once documented, a decision is permanent.”** Triggers and changed assumptions require review.
16. **“Changing a decision proves it was wrong.”** It may have been correct under earlier context and evidence.

## Worked Examples

### Example 1

**Situation.** A 12-person billing team proposes 20 microservices because it expects growth.

**Reasoning.** Current load is predictable, billing invariants require local transactions, one team releases all capabilities, and only quarterly partner integration crosses ownership. Independent scale and release scenarios are absent. A modular monolith with enforced billing modules, one write authority per module, outbox events, and a coarse partner API meets current requirements and preserves extraction seams. Review triggers include a second product team, a measured isolated bottleneck, or a regulatory privilege split.

**Conclusion.** The simpler architecture satisfies evidence-backed forces while preserving specific future options.

### Example 2

**Situation.** A media ingestion system must decode, normalize, transcribe, enrich, and index independent files at variable rates.

**Reasoning.** The workload is naturally staged; each transformation has a typed artifact, different resource profile, and retry policy. Pipe-and-filter with durable queues provides bounded buffers and independent workers. A single synchronous service would couple latency and scaling; event messages communicate stage completion. Data lineage and idempotent stage identities handle replay.

**Conclusion.** Pipeline and event styles follow transformation and workload forces, not a general preference for asynchronous systems.

### Example 3

**Situation.** An engineering editor needs vendor-specific syntax analyzers but must keep document authorization and storage consistent.

**Reasoning.** A microkernel owns documents, transactions, permissions, and extension lifecycle. Analyzer plugins receive immutable bounded snapshots and return validated diagnostics. Untrusted native analyzers run out of process. Making every analyzer a public enterprise service would add network and operational cost without independent business ownership; embedding them with unrestricted access would violate trust constraints.

**Conclusion.** Plugin architecture fits controlled variability around one product core, with isolation selected from threat consequence.

### Example 4

**Situation.** A trading risk check has a 5 ms end-to-end deadline, shared-memory market state, and one colocated ownership team.

**Reasoning.** A chain of remote microservices cannot meet the threshold with available networking and serialization evidence. A modular in-process design uses explicit modules, preallocated data, bounded work, and local measurement. Asynchronous audit publication occurs after the decision. Security isolation is achieved at process and host boundaries around the trading engine rather than between every calculation.

**Conclusion.** A hard latency threshold eliminates fashionable distribution while retaining internal architectural boundaries.

### Example 5

**Situation.** An insurer must integrate 14 acquired policy systems using different protocols over seven years.

**Reasoning.** The dominant forces are heterogeneous capability access, incremental replacement, durable contracts, and enterprise governance. Coarse service-oriented facades expose claims and policy capabilities; bounded mediation translates protocols and identity. Domain rules stay with service owners rather than an ESB. New implementations replace legacy systems behind stable contracts. Microservices may implement new domains, but “one service per legacy system” is not the governing boundary.

**Conclusion.** SOA and bounded mediation address long-lived heterogeneous integration without making the integration layer the business authority.

### Example 6

**Situation.** A mine must continue ventilation safety during a 30-minute regional link outage while headquarters needs later telemetry.

**Reasoning.** A cloud-only client-server controller violates the local safety constraint. Keep safety sensing and actuation in a local authoritative control system with fail-safe rules. Publish durable telemetry events through a store-and-forward boundary and reconcile after connectivity returns. Headquarters analytics can use a pipeline and services, but no remote component is on the safety-critical path.

**Conclusion.** A hard disconnected-operation force determines authority placement; event integration serves secondary observation.

### Example 7

**Situation.** Two feasible alternatives are scored on delivery speed and recovery. Modular monolith utilities are $(0.8,0.6)$; microservices utilities are $(0.5,0.9)$. Delivery weight is $w$ and recovery weight is $1-w$.

**Reasoning.** Monolith utility is $0.8w+0.6(1-w)=0.6+0.2w$. Microservices utility is $0.5w+0.9(1-w)=0.9-0.4w$. Break-even satisfies $0.6+0.2w=0.9-0.4w$, so $0.6w=0.3$ and $w=0.5$. If plausible stakeholder weights cross 0.5, the recommendation is sensitive. Investigate actual recovery mechanisms and delivery constraints rather than hiding sensitivity in one score.

**Conclusion.** Sensitivity analysis reveals when value judgment or missing evidence controls the result.

### Example 8

**Situation.** A document converter processes hostile native formats, and policy requires that memory corruption not compromise the main records process.

**Reasoning.** An in-process plugin violates the isolation constraint even if it scores well on latency and simplicity. A revised plugin alternative runs converters in restricted supervised processes with bounded input/output and no record-store credentials. A separate conversion service is also feasible. Compare those on latency, deployment, throughput, and operations only after both meet the protection threshold.

**Conclusion.** Constraint elimination precedes preference scoring, and mitigation may create a new feasible alternative.

### Example 9

**Situation.** An online store has transactional catalog administration, bursty image processing, partner updates, and optional recommendations.

**Reasoning.** One style need not own all forces. A layered modular monolith owns catalog administration and transactions. Image jobs use queue-backed workers. Partner changes publish durable events through an outbox. Recommendations use a separately scalable service and a cached optional response. Views map data authority, deployment, trust, and failure so asynchronous consumers never write catalog tables directly.

**Conclusion.** A governed hybrid is more precise than forcing the entire product into one style label.

### Example 10

**Situation.** A regulated claims platform must replace a mainframe, but source-of-truth cutover and rollback are poorly understood.

**Reasoning.** A big-bang service rewrite has an attractive target yet unacceptable migration risk. First expose a coarse claims facade, record outcomes, and build a parallel comparison path for one claim type. Backfill with provenance, choose one write authority at each step, and test rollback after new writes. Review triggers govern expansion. The facade and internal modules preserve options while uncertainty falls; indefinite dual writes are prohibited.

**Conclusion.** Migration feasibility and reversible evidence-gathering can dominate target-state elegance.

## Cross-Program Connections

- **Systems Engineering:** stakeholder needs, constraints, trade studies, risk, interface control, verification, and lifecycle supply broader decision discipline.
- **Software Design and Domain Modeling:** cohesion, bounded contexts, invariants, dependency direction, and change evidence refine candidate boundaries.
- **Software Delivery and Reliability Engineering:** lead time, deployment, SLOs, capacity, incidents, recovery, and operational toil test architectural predictions.
- **Distributed Systems Engineering:** failure, time, ordering, consistency, coordination, and replication determine the cost of distributed alternatives.
- **Security Engineering:** threat modeling, least privilege, trust boundaries, safety, and evidence can eliminate otherwise attractive styles.
- **API and Service Engineering:** contract, compatibility, error, identity, gateway, and resilience mechanics make service alternatives concrete.
- **Data Architecture Engineering:** system-of-record, integration, lineage, canonical models, and data lifecycle expose hidden coupling.
- **Platform Engineering:** paved paths and self-service determine whether many-deployment styles are organizationally feasible.

## References

1. ISO/IEC, *ISO/IEC 25010:2023 Systems and software engineering—Systems and software Quality Requirements and Evaluation (SQuaRE)—Product quality model*, 2nd ed., 2023. <https://www.iso.org/standard/78176.html>
2. Rick Kazman, Mark Klein, and Paul Clements, *ATAM: Method for Architecture Evaluation*, CMU/SEI-2000-TR-004, 2000. <https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=5177>
3. Melvin E. Conway, “How Do Committees Invent?”, *Datamation* 14(4), 1968. <https://www.melconway.com/Home/Committees_Paper.html>
4. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
5. Eoin Woods and Nick Rozanski, *Software Systems Architecture: Working with Stakeholders Using Viewpoints and Perspectives*, 2nd ed., Addison-Wesley, 2012.
6. Neal Ford, Mark Richards, Pramod Sadalage, and Zhamak Dehghani, *Software Architecture: The Hard Parts*, O'Reilly Media, 2021.
7. Michael Nygard, “Documenting Architecture Decisions,” 2011. <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
8. Robert L. Glass, *Facts and Fallacies of Software Engineering*, Addison-Wesley, 2002.

## Exercises

### Exercise 1

Define architectural style, force, quality-attribute scenario, constraint, coherent alternative, Pareto dominance, sensitivity point, and option value. Distinguish a style from a technology.

### Exercise 2

Alternative A has utilities 0.9 for changeability and 0.5 for recovery. Alternative B has 0.6 and 0.8. If changeability weight is $w$ and recovery weight is $1-w$, derive the break-even weight and identify which alternative wins on each side. State two limitations.

### Exercise 3

A team selects event-driven microservices “for scalability” after a successful hello-world broker demo. Diagnose the missing framing, causal evidence, and lifecycle concerns. Propose three decisive investigations.

### Exercise 4

Compare a modular monolith, service-oriented design, and microservices for a regional hospital scheduling platform. Define at least four scenarios, one hard constraint, comparable alternatives, and a plausible hybrid.

### Exercise 5

Design an architecture decision process for autonomous agricultural equipment that must operate safely offline, accept third-party implements, synchronize farm records, and support seasonal analytics. Select and compose styles, state constraints and evidence, plan migration and rollback, and define review triggers.

## Answers to the Exercises

### Answer 1

An **architectural style** defines element and relationship types plus composition constraints. A **force** is a contextual pressure. A **quality-attribute scenario** gives source, stimulus, environment, artifact, response, and measure. A **constraint** eliminates choices when proven and nonnegotiable. A **coherent alternative** specifies boundaries, data, interaction, deployment, ownership, operation, and migration. **Pareto dominance** means no worse on all assessed criteria and better on at least one. A **sensitivity point** strongly changes a quality response or recommendation. **Option value** is value from keeping a feasible future choice. A technology can implement mechanisms used by several styles; selecting a broker, container platform, language, or cloud does not define the architectural constraints or ownership model.

### Answer 2

Alternative A has $U_A=0.9w+0.5(1-w)=0.5+0.4w$. Alternative B has $U_B=0.6w+0.8(1-w)=0.8-0.2w$. Set equal: $0.5+0.4w=0.8-0.2w$, so $0.6w=0.3$ and $w=0.5$. B wins when $w<0.5$; A wins when $w>0.5$; they tie at 0.5. Limitations include subjective or incomparable utility scales, uncertain estimates, interaction between qualities, omitted thresholds or risks, and weights that may not represent stakeholder conflict. The sensitivity means evidence and reversibility matter.

### Answer 3

The statement lacks workload, bottleneck, scale target, latency, consistency, ownership, security, cost, and current-system evidence. It skips the causal chain from partitionable work through independent scaling to measured response. A hello-world demo proves only basic broker operation, not domain semantics, throughput under backpressure, recovery, schema evolution, or production operation. Investigations should include: measure production-like workload and identify the saturating resource; compare a modular single deployment with separate worker pools against distributed services under saturation and failure; model and test data authority, duplicate/out-of-order messages, retries, unknown outcomes, schema coexistence, and recovery. A team/platform readiness and on-call cost assessment is another valid investigation. The alternative remains unselected until evidence connects a mechanism to the scenario.

### Answer 4

Scenarios might require: 99th-percentile interactive search below 800 ms at regional peak; no cross-hospital disclosure without patient authorization; appointment commit remains atomic within one hospital authority; one hospital can upgrade its adapter without consortium downtime; and regional outage recovery within four hours. A hard constraint may prohibit identified patient records outside the legal region. Compare: a modular monolith per regional authority with internal hospital adapters; coarse service-oriented hospital scheduling capabilities with bounded mediation; and independently deployed microservices for search, identity, scheduling, and notifications. Give each the same data, deployment, staffing, identity, failure, and migration detail. A plausible hybrid uses a modular scheduling core per authority, service contracts for hospital and partner integration, asynchronous notifications, and a replicated privacy-minimized availability index. Microservices are extracted only for independently scaled or owned capabilities. Full credit requires scenario measures and truthful data authority, not label preference.

### Answer 5

Keep safety sensing, motion planning, interlocks, and actuation in a local authoritative control core because offline safe operation is a hard constraint. Use a microkernel with versioned implement plugins; untrusted or native drivers run in isolated processes and can propose only bounded commands that the core validates. Store operational records locally and publish durable idempotent events through store-and-forward synchronization; cloud services build farm-wide records under explicit conflict, freshness, and ownership rules. Seasonal analytics uses a pipe-and-filter pipeline and independently scalable batch workers outside the safety path. Evidence includes hardware-in-the-loop safety tests, plugin compatibility and adversarial tests, 24-hour disconnection drills, duplicate/out-of-order synchronization tests, resource saturation, rollback after plugin and schema upgrades, and analytics capacity measures. Migrate one implement type and one record stream at a time, retain one write authority, compare outputs, and provide signed rollback packages. Review triggers include a failed safety threshold, new implement protocol, regulatory change, offline duration beyond assumptions, unresolved synchronization conflicts, analytics saturation, ownership change, or platform support loss. A complete answer must distinguish local safety proof from cloud availability and must not make telemetry completion a prerequisite for safe actuation.
