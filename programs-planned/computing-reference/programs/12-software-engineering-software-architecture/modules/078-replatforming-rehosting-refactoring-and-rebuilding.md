---
module_id: SARCH-078
program: Software Engineering: Software Architecture
level: 2
module_number: 78
title: Replatforming, Rehosting, Refactoring, and Rebuilding
status: complete
last_verified: 2026-09-06
---

# Replatforming, Rehosting, Refactoring, and Rebuilding

## One-Page Review

### Governing question

Given a legacy capability, how should architects choose and combine rehosting, replatforming, refactoring, and rebuilding so the modernization addresses evidenced constraints, preserves required behavior and data, exposes uncertainty, and leaves an operable path rather than a fashionable destination diagram?

### Essential definitions

- **rehosting** moves substantially the same application and operational model to another environment with intentionally limited application change;
- **replatforming** changes important runtime, infrastructure, or managed-platform mechanisms while retaining most application responsibilities and behavior;
- **refactoring** changes internal structure and dependency boundaries while intentionally preserving externally required behavior;
- **rearchitecting** changes major responsibility, interaction, data-authority, or deployment decisions and may be performed incrementally through refactoring;
- **rebuilding** creates a new implementation of a capability from understood outcomes and obligations rather than translating the old implementation line by line;
- **replacement** adopts another product or service instead of implementing the capability and therefore includes supplier, data, contract, exit, and operating-model change;
- a **modernization unit** is a bounded capability or component for which one strategy and transition can be decided coherently;
- a **hard constraint** makes an option inadmissible rather than merely lowering its score;
- **residual risk** is risk intentionally carried after the chosen change;
- **option value** is the value of preserving an informed future choice under uncertainty;
- an **exit condition** states when transitional work or a deliberately limited strategy has delivered its promised outcome.

### Central model, mechanism, or theorem

Let $O$ be feasible strategies after hard constraints are applied. For option $o$, estimate scenario-dependent benefits $B_t(o)$, cost $C_t(o)$, risk losses $p_j(o)L_j(o)$, and residual value $V_H(o)$ over horizon $H$:

$$
NPV_H(o)=\sum_{t=0}^{H}\frac{B_t(o)-C_t(o)-\sum_j p_j(o)L_j(o)}{(1+r)^t}+\frac{V_H(o)}{(1+r)^H}.
$$

The expression structures assumptions; it does not manufacture reliable probabilities. Compare ranges and sensitivity, keep noncompensable constraints outside the score, and choose a portfolio by modernization unit. Revisit the decision when evidence changes.

### Critical invariants

- the strategy is tied to a named stakeholder outcome and baseline;
- safety, legal, data, security, accessibility, and continuity constraints are gates;
- required behavior is characterized independently of accidental legacy structure;
- data meaning, authority, history, and migration are explicit;
- operational responsibilities and failure modes match the proposed platform;
- transition states have compatible contracts, one authority, evidence gates, and recovery;
- estimates expose range, source, confidence, dependencies, and excluded effects;
- no option assumes unsupported staff, platform, supplier, or toolchain capability;
- mixed strategies retain end-to-end coherence;
- retirement removes old cost and risk rather than merely adding a new stack.

### Common failures

Common failures include treating strategy labels as standardized; applying one strategy to an entire estate; using target technology as the objective; rehosting and calling inherited risk solved; replatforming into proprietary mechanisms without exit analysis; refactoring without characterization tests or stopping criteria; rebuilding from incomplete requirements; reproducing every legacy feature and defect; scoring hard constraints as small penalties; hiding uncertainty in one-point estimates; double-counting benefits; ignoring transition and dual-running cost; assuming a managed platform transfers accountability; and declaring modernization complete before old data, licenses, credentials, skills, and recovery paths retire.

### Compact example

A claims platform must leave expiring hardware in nine months, but policy logic changes weekly and contains poorly understood exceptions. A full rebuild cannot establish behavior and regulatory evidence by the deadline. The organization rehosts the characterized core first to remove the hardware constraint, replatforms stateless jobs only where rollback is tested, and creates seams around claim adjudication. It then refactors high-change policy modules and incrementally rebuilds one bounded decision after parallel evidence. The rehost is a deliberate risk-reduction state with dated exit conditions, not a claim that modernization is complete.

### Connections

[SARCH-070](070-running-an-evidence-based-architecture-review.md) supplies decision evidence, [SARCH-074](074-incremental-decomposition.md) supplies modernization units, and [SARCH-075](075-strangler-and-parallel-run-architectures.md) plus [SARCH-076](076-data-migration-architecture.md) supply transition mechanisms. [SARCH-079](../ROADMAP.md) next develops component decommissioning.

## Governing Question

Modernization strategy is a choice about which uncertainty and cost to accept, not a ladder on which “rebuild” is automatically most advanced. Rehosting can be the rational response to an urgent facility exit. Replatforming can remove undifferentiated operations. Refactoring can recover changeability while preserving proven behavior. Rebuilding can escape constraints embedded too deeply to change economically. Each can also fail when applied to the wrong unit or justified by a technology slogan.

Taxonomies vary across vendors and literature. This chapter uses operational definitions and requires every decision record to state them. The important questions are what remains invariant, what changes, what evidence supports the change, and how authority moves. A portfolio can use all four strategies across different capabilities and times.

## Why This Matters

Legacy systems often deliver real value while accumulating obsolete platforms, fragile dependencies, knowledge concentration, security exposure, licensing cost, and slow change. They also encode unrecorded business rules, reconciliations, accessibility behavior, and operator judgment. An indiscriminate rewrite discards that evidence; an indiscriminate move preserves every constraint.

Strategy mistakes concentrate risk. A rehost program may move an outage-prone system faster into a new environment without improving recovery. A replatform may silently change network, identity, consistency, or backup behavior. An endless refactor consumes investment without a measurable outcome. A rebuild develops feature breadth while the old system continues changing, then discovers at cutover that data and operations were the real product.

Modernization must be evaluated as a sequence of production states. ISO/IEC/IEEE 14764:2022, checked in the official ISO record on 2026-09-06, remains the published third edition and treats maintenance as lifecycle work rather than a synonym for defect repair [12]. The durable lesson is that software change, migration, operation, and disposal require explicit processes and evidence.

## Prerequisites and Retrieval

Retrieve stakeholder, outcome, constraint, quality-attribute scenario, baseline, architecture decision, dependency, coupling, cohesion, technical debt, change cost, total cost of ownership, net present value, discount rate, uncertainty, sensitivity analysis, option value, residual risk, characterization test, seam, strangler, compatibility window, canary, data authority, backfill, CDC, cutover, rollback, roll forward, service objective, recovery objective, supplier lock-in, portability, licensing, skills, accessibility, compliance, retention, and decommissioning.

SARCH-061 through SARCH-070 supply trade-off, risk, quality, performance, reliability, threat, cost, and review methods. SARCH-071 through SARCH-077 supply drift analysis and incremental modernization mechanisms. This module owns strategy selection and composition, not implementation recipes for a particular cloud or product.

## Learning Objectives

After completing this module, you should be able to:

1. define and distinguish rehosting, replatforming, refactoring, rearchitecting, rebuilding, replacement, retention, and retirement;
2. select a bounded modernization unit rather than force one estate-wide strategy;
3. establish outcomes, baselines, hard constraints, and decision horizon;
4. characterize required legacy behavior without making the legacy system an oracle;
5. compare lifecycle cost, risk, option value, transition cost, and residual debt;
6. use scenarios and sensitivity analysis without laundering judgment into a score;
7. identify platform, supplier, data, skills, and operating-model consequences;
8. compose mixed strategies into coherent intermediate states;
9. define evidence gates, recovery, stopping, and retirement conditions;
10. revise a decision when assumptions or evidence materially change.

## Core Exposition

**Begin with the outcome, not the verb.** State the stakeholder problem in measurable terms: hardware support ends by a date; a policy change takes twelve weeks; recovery exceeds the tolerated duration; a jurisdiction forbids current data placement; a component cannot meet peak demand; or scarce expertise creates unacceptable continuity risk. Record the current baseline and counterfactual of doing nothing.

“Move to cloud,” “adopt microservices,” and “eliminate legacy” are proposed means. Turn them into scenarios with stimulus, environment, response, and measure. If an option cannot affect the measure through a credible mechanism, it should not receive modernization credit.

**Choose the modernization unit.** Divide the estate by capability, authority, dependency, and lifecycle rather than organization chart or server. One application may contain a stable ledger, replaceable reporting engine, obsolete UI, and high-change policy module. Applying one strategy to all four discards useful differences.

The unit must still be coherent. Moving a UI without its release and contract constraints may not change lead time. Rebuilding a calculation while leaving its data and approvals in the old system may produce a permanent facade. Use SARCH-074's seams and stopping rules to keep the unit chapter-sized and outcome-bearing.

**Inventory obligations and current evidence.** Map behavior, data, interfaces, jobs, users, operators, suppliers, licenses, identities, environments, recovery, security, accessibility, records, and manual work. Sample incidents and changes. Find direct database consumers, file transfers, seasonal paths, and disaster procedures.

Distinguish requirement, observed behavior, defect, workaround, obsolete feature, and unresolved ambiguity. Characterization tests record what the system does; they do not declare every behavior correct. Domain and accountable policy owners decide what a replacement must preserve or deliberately change.

**Apply hard constraints before optimization.** Some options are unavailable: a deadline may be shorter than a safe rebuild; source code may be missing; a platform may lack required certification evidence; data may not leave a jurisdiction; safety analysis may require determinism; or a supplier contract may prohibit necessary access. Treating these as low weighted scores permits unrelated benefits to compensate for a prohibition.

Record the evidence, authority, and expiry of each constraint. A perceived constraint may be negotiable, while a statutory or physical one may not be. Do not let “compliance says no” replace a precise rule and qualified interpretation.

**Understand rehosting.** Rehosting moves substantially the same application, often with compatible operating-system, runtime, network, and storage assumptions. Its strengths are speed, limited application change, preserved behavior, and a smaller verification surface. It can remove a facility, hardware, or unsupported-host constraint and buy time for later change.

It normally preserves application coupling, scaling limits, deployment model, operational toil, and defects. Environmental equivalence is not automatic: latency, clock, filesystem, identity, multicast, IP, backup, and failure behavior may change. Rehost plans need representative performance, recovery, integration, licensing, security, and rollback evidence plus an honest list of residual risks.

**Understand replatforming.** Replatforming changes meaningful platform mechanisms—perhaps managed database, runtime, container platform, identity, messaging, build, or observability—while retaining most capability structure. It can remove unsupported middleware, standardize operation, improve recovery primitives, or reduce toil.

The application still absorbs semantic change. Connection lifetime, transaction isolation, storage durability, case sensitivity, queue delivery, autoscaling, secrets, maintenance, network egress, and backup restoration can differ. A managed service transfers tasks, not outcome accountability. Validate the contract actually offered and preserve an exit or recovery strategy proportionate to dependency.

**Understand refactoring and rearchitecting.** Refactoring changes internal structure while intentionally preserving required external behavior. It is appropriate when value and rules remain useful but change is slowed by entanglement. Characterization, modular boundaries, dependency inversion, testability, data ownership, and incremental release provide the safety system.

Architecture-scale refactoring may alter deployment and interaction while preserving capability outcomes. Call it rearchitecting when responsibilities, authority, or quality mechanisms change materially. Set stopping criteria tied to outcomes; “clean code” has no natural end. Refactor the hotspot or seam that reduces measured change and risk rather than formatting the whole estate.

**Understand rebuilding.** Rebuilding implements a capability anew from validated outcomes, constraints, and required behavior. It can adopt a new domain model, remove obsolete functions, support a different operating model, and escape fundamental technology or structure limitations. It also has the widest discovery and transition surface.

Requirements are rarely complete. The old system continues changing, so feature parity recedes. Rare workflows, data history, integrations, performance, accessibility, recovery, and operator judgment arrive late. Use bounded vertical slices, parallel evidence, explicit authority, and retirement. A line-by-line translation is usually an expensive reimplementation of old structure rather than a purposeful rebuild.

**Include retain, retire, and replace.** Not every capability needs transformation. Retain a stable component when its value, risk, and lifecycle are acceptable. Retire behavior whose outcome is no longer required. Replacement with a product or service can reduce implementation ownership but introduces fit, configuration, integration, supplier, data, security, cost, continuity, and exit obligations.

These options prevent a false four-way choice. A portfolio that rebuilds obsolete behavior has failed before implementation. A product replacement that requires recreating every legacy customization may provide less leverage than focused refactoring.

**Model lifecycle economics.** Estimate discovery, delivery, migration, dual operation, verification, training, support, licenses, infrastructure, opportunity cost, retirement, and expected incident or delay loss. Include the do-nothing baseline and horizon. Separate cash, staff capacity, elapsed time, and risk exposure; they are not interchangeable even if a model expresses them monetarily.

Use ranges or distributions rather than false precision. Name estimate source and confidence. Avoid double counting: faster change and resulting revenue may be the same causal benefit. Include residual debt and terminal value. Discounting expresses time preference, not ethical permission to defer safety or legal obligations.

**Use scores as conversation, not proof.** Weighted matrices can expose how priorities affect ranking. Normalize criteria, define direction, keep hard gates outside, and show sensitivity. If small reasonable weight changes reverse the winner, the decision is fragile and should preserve option value or gather discriminating evidence.

Do not average away stakeholder conflict. Operations, security, users, finance, and product may value different outcomes legitimately. Preserve dissent and decision authority. A high total score cannot compensate for an unhandled catastrophic scenario.

**Value learning and reversibility.** A short rehost can buy time, but only if it does not consume the budget and political will needed for the next constraint. An internal seam can produce information before an extraction. A prototype can test platform behavior without moving authority. Option value comes from reducing uncertainty or preserving choices.

Prefer small experiments that distinguish options: measure database compatibility, characterize a rule cluster, restore a representative backup, migrate one cohort, or benchmark a critical path. A demonstration built on toy data and no failure is weak evidence. Define in advance what result changes the decision.

**Evaluate operational fit.** Each strategy changes skills, on-call load, diagnosis, deployment, capacity, recovery, incident coordination, and supplier interaction. A platform promising elasticity still needs workload partitioning, limits, observability, and cost controls. A service decomposition needs contract and distributed-systems maturity.

Compare the proposed operating model with available people and learning time. Training is real work. Outsourcing operation does not outsource accountability. Ensure emergency access, audit, patching, vulnerability response, support hours, and restore are explicit.

**Evaluate security and dependency change.** Modernization can remove unsupported components and also expand identity, network, supply-chain, management-plane, and supplier attack surfaces. Threat-model each transition state, including copied data, compatibility modes, temporary credentials, remote administration, and rollback artifacts.

Inventory dependency end-of-life and provenance. Rebuilding on a current framework does not guarantee a maintainable supply chain. Rehosting an unsupported runtime preserves exposure. Replatforming may create deep proprietary dependencies; assess portability, data export, contractual exit, and recovery without assuming lock-in is always unacceptable or harmless.

**Treat data as a separate workstream and gate.** Strategy names do not explain identity, history, semantic mapping, backfill, concurrent changes, deletion, reconciliation, or authority. A modest application rehost can still require a difficult data move. A rebuild can reuse data physically while radically changing meaning.

Use SARCH-076's snapshot, CDC, idempotency, version, reconciliation, fencing, and retirement discipline. Test volume, skew, retention, precision, time, access, privacy, restore, and rollback. Data uncertainty often determines feasible sequence more strongly than code complexity.

**Compose strategies coherently.** A program may rehost a stable core, replatform batch execution, refactor policy boundaries, rebuild customer interaction, replace document rendering, and retire unused reports. Record contracts and authority between units. Avoid creating a target where every unit uses a different platform without operational reason.

Composition also happens through time. Rehost-to-refactor is valid if the first state removes an urgent constraint and has funded exit conditions. Replatform-to-rebuild can establish delivery and observability. Each state must deliver value, remain supportable, and not make the next state harder without an acknowledged trade-off.

**Design the transition before choosing the destination.** Identify compatibility windows, routing, parallel comparison, data movement, cutover, rollback horizon, roll-forward repair, support, and retirement. A theoretically attractive target can be infeasible because the transition crosses an unbounded dual-write or outage state.

Use one authority for each mutable fact. Expand before contract, canary by coherent cohort, isolate shadow effects, and fence old writers. Account for external effects and clients that cannot update promptly. The transition architecture is part of option cost and risk.

**Define evidence and exit conditions.** Rehost evidence may require identical business outcomes, bounded performance change, restored backups, and removal of old hosting. Replatform evidence adds service semantics, failover, limits, portability, and operational readiness. Refactoring evidence shows preserved behavior plus improved change locality or testability. Rebuild evidence covers requirements, comparison, data, scale, security, accessibility, operations, and retirement.

Exit conditions include obsolete routes, stores, licenses, credentials, pipelines, recovery plans, support procedures, and teams. If old and new must remain indefinitely, model that as a permanent architecture and fund it rather than hiding it as migration.

**Reassess at decision checkpoints.** Track actual cost, risk, outcome, and new evidence. Stop, narrow, or change strategy when premises fail. Sunk cost does not make completion rational. Equally, novelty fatigue is not evidence that a sound change should stop.

Record what was learned and update the architecture decision. The best portfolio is adaptive but not directionless: durable outcomes and invariants remain stable while means change under evidence.

## Definitions and Notation

Let:

- $U$ be bounded modernization units;
- $O_u$ be candidate options for unit $u$;
- $F_u\subseteq O_u$ be options satisfying every hard constraint;
- $B_t(o)$ and $C_t(o)$ be benefit and cost in period $t$;
- $p_j(o)$ and $L_j(o)$ be estimated probability and loss for risk scenario $j$;
- $r$ be the declared discount rate;
- $H$ be the decision horizon;
- $V_H(o)$ be residual or terminal value at $H$;
- $s_i(o)$ be an explicitly scaled option score on criterion $i$;
- $w_i$ be its declared weight;
- $E(o)$ be transition states and their evidence gates;
- $R(o)$ be residual risks accepted with owner and review date.

An option outside $F_u$ is inadmissible regardless of weighted score. Expected-value terms do not adequately express every catastrophic, rights-sensitive, or poorly estimated risk. Use scenarios, ranges, dominance checks, and sensitivity alongside the model.

## Mechanisms, Invariants, or Proof Structure

**Feasibility invariant.** Selection is over $F_u$, not all named strategies. If a hard condition fails, unrelated benefit cannot compensate. This prevents a large speed or cost score from offsetting an option that cannot preserve a required safety, legal, data, or continuity property.

**Lifecycle-value model.** The NPV expression makes timing, cost, expected risk loss, horizon, and residual value visible. It is conditionally correct arithmetic for its inputs; it cannot validate their estimates or convert nonmonetary obligations automatically. Report ranges and scenarios.

**Executable sensitivity example.** These illustrative ordinal scores show two reasonable priority profiles selecting different strategies. The result demonstrates sensitivity, not a recommended modernization decision.

<!-- bijux-verify: {"id":"compare-strategy-sensitivity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"exit-deadline: rehost 5.80\nlong-horizon: rebuild 4.90\n","stderr":""}} -->
```python
options = {
    "rehost": {"speed": 9, "fit": 3, "change": 2, "risk": 4},
    "replatform": {"speed": 7, "fit": 6, "change": 5, "risk": 5},
    "refactor": {"speed": 4, "fit": 8, "change": 8, "risk": 7},
    "rebuild": {"speed": 2, "fit": 9, "change": 10, "risk": 10},
}
profiles = {
    "exit-deadline": {"speed": .6, "fit": .2, "change": .1, "risk": -.1},
    "long-horizon": {"speed": .1, "fit": .3, "change": .4, "risk": -.2},
}
for profile, weights in profiles.items():
    scores = {
        option: sum(values[key] * weight for key, weight in weights.items())
        for option, values in options.items()
    }
    winner = max(scores, key=scores.get)
    print(f"{profile}: {winner} {scores[winner]:.2f}")
```

Execution verifies only the displayed arithmetic over invented scores. It does not establish interval scales, probability, cost, feasibility, stakeholder priority, or a real winner.

**Sensitivity proposition.** If two plausible weight profiles select different feasible options, ranking is not robust to the contested priorities. The decision should preserve the conflict, gather evidence that separates options, choose a reversible state, or use accountable judgment. Averaging the profiles hides rather than resolves the disagreement.

**Rebuild incompleteness argument.** Let required behavior be $Q$ and discovered specification be $D\subset Q$. An implementation satisfying all of $D$ does not imply it satisfies $Q$ unless $D=Q$ or another argument covers $Q\setminus D$. Therefore passing tests derived only from documented requirements cannot establish parity when undocumented obligations exist.

**Portfolio coherence invariant.** For adjacent modernization units, contracts, data authority, identity, security, operations, and recovery must compose in every intermediate state. Local option optimality does not imply an operable system portfolio.

## Alternatives and Trade-Offs

**Rehost versus replatform.** Rehost narrows change and can meet urgent exit dates; replatform may remove more operational burden but changes runtime semantics and dependency.

**Refactor versus rebuild.** Refactor preserves accumulated behavior and enables increments but may be constrained by fundamentals. Rebuild offers deliberate models but carries rediscovery, parity, transition, and dual-running risk.

**Rebuild versus replace.** Rebuild retains product control and implementation burden. Replacement accelerates commodity capability but transfers roadmap and creates integration, supplier, configuration, data, and exit concerns.

**One large program versus capability portfolio.** Central coordination can manage shared constraints but encourages one strategy and distant value. Capability slices produce learning and retirement sooner but require coherent architecture governance.

**Optimize now versus preserve options.** A specialized target may maximize near-term fit. A reversible intermediate state can be worth more under uncertainty. Option value must still have a plausible future decision, not justify indefinite delay.

**Parallel operation versus decisive cutover.** Parallel evidence reduces semantic uncertainty but adds cost, exposure, and dual-system risk. Shorter cutover reduces transition duration but concentrates discovery and recovery risk.

## Failure Modes and Misconceptions

1. **“Rebuild is the highest modernization level.”** strategies answer different forces.
2. **“The taxonomy is universal.”** define what changes and remains for this decision.
3. **“One application needs one strategy.”** bounded capabilities often differ.
4. **“Rehost removes technical debt.”** it usually relocates much of it.
5. **“Replatform changes no application semantics.”** platform contracts affect behavior.
6. **“Managed means no operations.”** accountability, configuration, recovery, and incidents remain.
7. **“Refactoring is cosmetic.”** architecture-scale refactoring changes dependency and ownership while preserving required outcomes.
8. **“Refactoring should continue until clean.”** use measured outcome and stopping conditions.
9. **“The old system is the specification.”** it also contains defects and obsolete behavior.
10. **“Documented requirements are complete.”** rare and manual paths often contradict that assumption.
11. **“A weighted score makes the answer objective.”** inputs and weights encode judgment.
12. **“Every concern belongs in the score.”** hard constraints and rights may be noncompensable.
13. **“Estimated benefits add independently.”** causal overlap can double count value.
14. **“Target cost is total cost.”** discovery, migration, parallel run, retirement, and residual risk matter.
15. **“A prototype proves feasibility.”** scale, history, security, failure, and operations may be absent.
16. **“Mixed strategies are inconsistent.”** they are sound when boundaries and transition compose.
17. **“Rollback is always available.”** new state and external effects can cross a point of no return.
18. **“Deployment completes modernization.”** old obligations must retire and outcomes must improve.

## Worked Examples

### Example 1

**Situation.** Data-center lease expiry is nine months away, while a safe core rewrite is estimated at two to four years.

**Reasoning.** The deadline makes full rebuild infeasible as the first state. A characterized rehost removes facility risk with bounded application change. The decision records inherited coupling and operational debt, reserves funding, creates seams around high-change policy, and gives the rehost dated exit conditions.

**Conclusion.** Rehosting can be a rational destination for one constraint and an explicit intermediate state for others.

### Example 2

**Situation.** A team proposes moving an application database to a managed relational service without code changes.

**Reasoning.** Investigation finds unsupported extensions, filesystem imports, isolation assumptions, superuser tasks, and a six-hour restore requirement. This is a replatform with semantic and operational change, not a transparent host move. Compatibility, performance, failover, privileges, backup restore, export, and rollback become gates.

**Conclusion.** Platform abstraction does not erase the mechanisms on which the application depends.

### Example 3

**Situation.** Policy changes touch forty files but production behavior is valuable and well characterized.

**Reasoning.** Refactoring introduces a policy module, captures decisions behind a contract, moves data authority, enforces dependencies, and measures touched files and test time. Rebuilding the whole product would add rediscovery and data risk without evidence that the remaining capability model is wrong.

**Conclusion.** Refactor when structure blocks change but required behavior remains an asset.

### Example 4

**Situation.** A 25-year-old scheduling engine cannot express multi-resource constraints required by the product.

**Reasoning.** Wrappers and local refactors cannot add the model without preserving a fundamentally incompatible representation. The team rebuilds the bounded scheduling decision, retains legacy as evidence rather than oracle, defines new invariants, migrates data, compares qualified cohorts, and transfers one authority incrementally.

**Conclusion.** Rebuild is justified by a proven model constraint, not age alone.

### Example 5

**Situation.** The sensitivity snippet selects rehost for an exit profile and rebuild for a long-horizon profile.

**Reasoning.** The rankings differ because weights differ, not because the code discovered truth. Stakeholders inspect the urgent deadline, long-term change cost, hard constraints, uncertainty, and sequencing. A rehost that preserves a later rebuild may dominate a forced immediate choice if its transition cost and delay are acceptable.

**Conclusion.** Sensitivity exposes fragile judgment and can motivate a staged option.

### Example 6

**Situation.** A vendor product supplies 90% of document management, but the old system has hundreds of custom workflows.

**Reasoning.** The team classifies workflows as required control, differentiating capability, workaround, or obsolete. It replaces commodity storage and retention where contract, data export, access, recovery, and exit are acceptable; it rebuilds or refactors only distinctive decisions. It does not recreate every customization automatically.

**Conclusion.** Replacement value depends on reducing customization while preserving real obligations.

### Example 7

**Situation.** A replatform business case counts reduced operator work and lower operating cost separately, although the cost reduction is entirely the removed operator work.

**Reasoning.** The benefits share one causal mechanism and are double counted. The analysis separates staff capacity, cash expense, service improvement, and opportunity value; it records whether released capacity can actually be redeployed. Ranges and source confidence replace one optimistic total.

**Conclusion.** Economic structure must expose causal overlap and realizability.

### Example 8

**Situation.** A rebuilt service passes all documented requirements but disagrees on an annual reconciliation path.

**Reasoning.** The rare path belongs to $Q\setminus D$: required behavior absent from discovered specification. Operators and domain owners determine whether it is a control, workaround, or defect. The candidate remains nonauthoritative until the obligation is implemented or explicitly retired.

**Conclusion.** Satisfaction of incomplete documentation cannot prove capability completeness.

### Example 9

**Situation.** A bank mixes rehost, replatform, refactor, and rebuild across one transaction journey.

**Reasoning.** Each local choice appears sound, but identity changes twice, two units claim account authority, and recovery cannot reconstruct the combined state. The portfolio review establishes one authority, compatible identifiers, transaction and compensation rules, end-to-end recovery, and coherent release states before approving slices.

**Conclusion.** Local strategy quality does not guarantee portfolio coherence.

### Example 10

**Situation.** A new stack serves all traffic, yet old middleware licenses, replicas, exports, credentials, and recovery images remain.

**Reasoning.** Operating cost and attack-surface exposure persist, rollback assumptions are ambiguous, and data copies retain obligations. Owners migrate or retire consumers, preserve only governed records, revoke access, prove new recovery, remove old infrastructure, and measure the promised outcome.

**Conclusion.** Retirement and realized outcomes—not new deployment—complete modernization.

## Cross-Program Connections

- [SEME](../../10-software-engineering-methods-and-evolution/ROADMAP.md) owns maintenance process, legacy evolution, reverse engineering, and modernization methods.
- [SEPAT](../../11-software-engineering-patterns/ROADMAP.md) supplies seams, adapters, strangler, branch-by-abstraction, outbox, and migration patterns.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns delivery, operational readiness, deployment, recovery, and incident practice.
- [DBE](../../18-database-engineering/ROADMAP.md) owns engine migration, transaction, schema, replication, and database verification mechanisms.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) supplies semantic authority, lineage, retention, governance, and enterprise data constraints.
- [SEC](../../25-security-engineering/ROADMAP.md) supplies threat, identity, vulnerability, supplier, privacy, and retirement controls.
- [SYSENG](../../26-systems-engineering/ROADMAP.md) develops lifecycle, stakeholder, trade study, assurance, transition, and disposal judgment.
- [PLAT](../../29-platform-engineering/ROADMAP.md) owns platform product, self-service, portability, operations, and adoption capability.

## References

1. Neil Ernst, Mary Popeck, Felix Bachmann, and Patrick Donohoe. “Creating Software Modernization Roadmaps: The Architecture Options Workshop.” WICSA, 2016. https://www.sei.cmu.edu/library/creating-software-modernization-roadmaps-the-architecture-options-workshop/
2. Barry W. Boehm. *Software Engineering Economics*. Prentice Hall, 1981.
3. Meir M. Lehman and Les Belady, editors. *Program Evolution: Processes of Software Change*. Academic Press, 1985.
4. Michael Feathers. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
5. Pramod J. Sadalage and Martin Fowler. *Refactoring Databases*. Addison-Wesley, 2006.
6. Sam Newman. *Monolith to Microservices*. O'Reilly Media, 2019.
7. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage. *Building Evolutionary Architectures*. 2nd ed. O'Reilly Media, 2022.
8. Ipek Ozkaya. *Managing Technical Debt*. Addison-Wesley, 2019.
9. Rick Kazman, Jai Asundi, and Mark Klein. “Quantifying the Costs and Benefits of Architectural Decisions.” ICSE, 2001. https://doi.org/10.1109/ICSE.2001.919103
10. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.
11. Martin Fowler. “Strangler Fig.” 22 August 2024. Checked 2026-09-06. https://martinfowler.com/bliki/StranglerFigApplication.html
12. ISO/IEC/IEEE. “ISO/IEC/IEEE 14764:2022 Software engineering — Software life cycle processes — Maintenance.” Official record checked 2026-09-06. https://www.iso.org/standard/80710.html

## Exercises

### Exercise 1

Define rehosting, replatforming, refactoring, rearchitecting, rebuilding, replacement, modernization unit, hard constraint, residual risk, option value, and exit condition.

### Exercise 2

An option has expected annual benefits of 300 units and costs of 180 units at the end of years 1–3, expected risk loss of 20 units each year, terminal value 100 at year 3, and discount rate 10%. Using the chapter's model with no time-zero flow, compute its NPV to two decimals.

### Exercise 3

A team calls a managed-database move “rehosting,” has no restore test, and assumes unchanged isolation and extensions. Diagnose the decision and specify the minimum evidence before authority moves.

### Exercise 4

Create a modernization portfolio for a retail estate containing a stable ledger, obsolete reports, a high-change promotion engine, a commodity document store, and an unsupported hosting platform. Justify strategies, sequencing, data authority, evidence, transition, stopping, and retirement.

### Exercise 5

A national court system includes active cases, sealed records, public access, accessibility obligations, local integrations, historical formats, judicial workflows, and statutory retention. Propose a governed modernization strategy without claiming the architecture determines legal meaning, judicial policy, lawful access, or adequate accessibility.

## Answers to the Exercises

### Answer 1

Rehosting moves substantially the same application and operating assumptions to another environment. Replatforming changes important runtime or infrastructure mechanisms while retaining most application responsibility. Refactoring changes internal structure while preserving required behavior. Rearchitecting materially changes responsibility, interaction, authority, or deployment decisions. Rebuilding creates a new implementation from validated outcomes and obligations. Replacement adopts another product or service. A modernization unit is a bounded capability for coherent strategy and transition. A hard constraint makes an option inadmissible. Residual risk remains after change with explicit acceptance. Option value is the value of preserving an informed future choice. An exit condition states when a transitional or limited strategy has delivered and its temporary mechanisms can end.

### Answer 2

Each year's net expected flow is $300-180-20=100$. Present value of the three flows is

$$
100/1.1+100/1.1^2+100/1.1^3
=90.9091+82.6446+75.1315=248.6852.
$$

Terminal value contributes $100/1.1^3=75.1315$. Total NPV is approximately $323.82$ units. The arithmetic is conditional on point estimates and does not show ranges, dependencies, catastrophic gates, benefit overlap, or whether capacity and cash are interchangeable.

### Answer 3

The move is a replatform under this chapter's definition because database service semantics and operations change materially. The label hid extension, isolation, privilege, recovery, and platform dependencies. Authority must not move on the assumption that SQL compatibility establishes behavioral compatibility.

Inventory types, extensions, procedures, collations, precision, isolation, locks, connection behavior, identities, network, maintenance, replication, backups, integrations, and direct users. Test representative correctness and concurrency, failure and failover, load and skew, access controls, observability, backup restore to the required point and duration, migration boundary and reconciliation, data export, rollback horizon, and operator response. Record service version and guarantees, residual differences, hard gates, qualified approvals, and a fenced authority-transfer procedure.

### Answer 4

First define outcomes and the unsupported-host deadline. Rehost components whose behavior is stable when necessary to remove the urgent host constraint, with compatibility and recovery evidence plus dated exits. Retain and characterize the ledger initially; refactor only seams needed for support, security, data authority, or change, because correctness history is valuable. Retire obsolete reports after consumer, record, and policy evidence.

Refactor the high-change Promotion capability around one policy and data authority, then rebuild bounded decisions only where its model cannot meet current needs. Compare old and new behavior without treating legacy defects as truth. Replace the commodity document store if product fit, metadata, retention, access, export, recovery, supplier, and exit evidence are acceptable. Replatform shared delivery and observation mechanisms where it reduces unsupported operation without forcing one risky cutover.

Sequence vertical slices with compatible contracts, one write authority, snapshot and CDC data movement, isolated shadowing, stable cohorts, fencing, and state-aware rollback or roll forward. Track lead time, risk, restore, incidents, cost, and residual debt. Stop refactoring when the target outcome is met; stop or change a strategy when premises fail. Retire old routes, data copies, jobs, licenses, credentials, pipelines, support, and recovery per slice. Full credit requires portfolio coherence rather than five unrelated local choices.

### Answer 5

Establish accountable judicial, clerk, records, legal, security, privacy, accessibility, archival, operations, local-court, and public-service authorities. Inventory active and historical case behavior, seals, access decisions, filings, calendars, identity, evidence references, local integrations, manual work, formats, retention, disaster procedure, and public interfaces. Separate technical observation from determinations of legal meaning and lawful access.

Use bounded modernization units. Urgently rehost only where infrastructure expiry requires it and behavior can be characterized. Replatform supported commodity runtime and storage only after access, encryption, isolation, audit, restore, jurisdiction, and export evidence. Refactor ownership and contracts around case, filing, scheduling, access, and publication decisions. Rebuild a capability only where current models cannot satisfy validated needs, using governed parallel evidence and retaining original records and provenance. Replace commodity functions only with supplier continuity and exit plans; retire truly obsolete paths through authorized records decisions.

Preserve sealed and sensitive-data authority, stable identities, uncertain historical representation, chain of custody, accessibility metadata, and statutory retention. Migrate with consistent boundaries, versioned changes, reconciliation, fencing, and tested recovery. Roll out by authorized coherent court or case cohorts where lawful, with offline and local integration behavior. Retire credentials, exports, replicas, licenses, support, and old recovery only after evidence. Architecture can structure options, controls, provenance, and checks; qualified institutions and affected users must determine judicial policy, legal interpretation, lawful disclosure, records disposition, and accessibility adequacy.
