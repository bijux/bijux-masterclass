---
module_id: SEPAT-003
program: Software Engineering: Patterns
level: 1
module_number: 3
title: Reading and Writing a Pattern Form
status: complete
last_verified: 2026-08-28
---

# Reading and Writing a Pattern Form

## One-Page Review

### Governing question

How should a pattern be structured so a reader can recover its argument, test its evidence, adapt its solution, and anticipate its liabilities?

### Essential definitions

- A **pattern form** is the organized set of fields used to present pattern knowledge consistently.
- **Intent** is a concise statement of the pattern's purpose and design effect.
- **Motivation** is a concrete story that makes the problem and solution dynamics intelligible.
- **Context** gives relevant preconditions; the **problem** states the unresolved tension; **forces** explain why obvious solutions are inadequate.
- The **solution** states the essential configuration, while **structure**, **participants**, and **collaborations** make it constructable.
- **Consequences** describe the resulting context, including benefits, liabilities, and new problems.
- **Known uses** are independently identifiable occurrences that support recurrence and feasibility.
- **Variants** preserve the central intent while changing some structure or policy; **related patterns** explain alternatives, prerequisites, complements, and successors.
- **Shepherding** is iterative author–reviewer collaboration; a **writers' workshop** is a reader-centered peer-review practice used by pattern communities.

### Central model, mechanism, or theorem

A readable form exposes a causal chain:

$$
C\rightarrow P\xrightarrow{F}S\rightarrow K\rightarrow C'.
$$

In context (C), problem (P) arises; forces (F) justify solution configuration (S); consequences (K) produce resulting context (C'). Evidence and known uses support recurrence and feasibility. Relations connect (C') to alternatives or successor patterns. The form is complete only when a reader can trace important forces through solution decisions to consequences.

### Critical invariants

- The name is memorable but must not substitute for the problem.
- Context, problem, and forces remain solution-independent.
- The solution is constructable and distinguishes essential structure from variation.
- Dynamics explain behavior over time, not only a static diagram.
- Consequences include liabilities and resulting responsibilities.
- Known uses identify actual occurrences and do not count the author's example as independent evidence.
- Related patterns state the relationship, not merely a list of names.
- A structural checklist can detect omissions but cannot prove recurrence, clarity, or solution quality.

### Common failures

Common failures include beginning with a class diagram, hiding the problem in motivation prose, listing generic quality attributes as forces, describing an implementation instead of an adaptable configuration, omitting failure dynamics, using hypothetical examples as known uses, advertising only benefits, citing related patterns without comparison, and revising wording while ignoring a broken argument.

### Compact example

A draft called “Bounded Work Queue” states a context of bursty producers and slower consumers, a problem of containing memory and overload, forces of throughput, bounded capacity, latency, fairness, and admission behavior, and a solution with a finite queue plus explicit full-queue policy. Its consequences include backpressure or loss, queueing latency, capacity tuning, and saturation telemetry. A static queue diagram is insufficient unless enqueue/dequeue, blocking, cancellation, shutdown, and failure dynamics are explained.

### Connections

[SEPAT-001](001-recurring-problems-context-forces-and-consequences.md) establishes the causal pattern argument; [SEPAT-002](002-pattern-versus-idiom-principle-recipe-and-framework.md) locates the form among other guidance. [SEPAT-004](../ROADMAP.md) deepens intent and applicability, while [SEPAT-007](../ROADMAP.md) connects forms into pattern languages. Iterative authoring and review connect to [Software Engineering: Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md).

## Governing Question

What information architecture lets different readers quickly answer: do I have this problem, why is this solution plausible, how do I build it, what will it cost, and where do I go next?

Pattern forms vary. Alexander's architectural patterns, the Gang of Four catalog, Pattern-Oriented Software Architecture, enterprise patterns, and conference papers use different headings and narrative styles. The headings are not the essence. Their purpose is to preserve a conditional design argument and make important information retrievable.

A terse reader may scan name, context, problem, and solution. An implementer needs participants, collaborations, variants, and pitfalls. A reviewer needs forces, consequences, evidence, and known uses. A maintainer needs resulting context and related patterns. A strong form serves all four without duplicating claims or pretending that completion of fields proves quality.

## Why This Matters

Unstructured design advice is hard to evaluate. A persuasive anecdote can conceal missing recurrence. A polished diagram can hide a solution-shaped problem. A code sample can make one implementation look inevitable. Pattern form forces the author to expose the links that readers must challenge.

Consistent forms also support catalogs. Readers can compare two patterns with similar problems, find contraindications, and navigate sequences. Reviewers can locate evidence gaps. Teams can turn known consequences into decision and test criteria.

Form alone is not enough. Mechanical templates often produce filler: “performance” appears under forces, “more flexibility” under consequences, and familiar products under known uses without explaining the occurrence. The authoring discipline is causal: every field must contribute to recognizing, selecting, constructing, or evaluating the pattern.

## Prerequisites and Retrieval

You should be able to distinguish problem and solution domains, read a component or class diagram, and reason about quality trade-offs. Retrieve these facts:

1. Context and forces bound a pattern's applicability.
2. A solution has both structure and behavior over time.
3. Evidence from one instance establishes possibility, not recurrence.
4. A negative consequence is part of the result, not a defect in documentation.
5. Different readers need recognition, construction, and evaluation paths.
6. Peer review of technical content and peer review of reader comprehension ask different questions.

## Learning Objectives

After completing this module, you should be able to:

- identify the semantic purpose of common pattern-form fields;
- read a pattern in recognition, construction, and critical-review passes;
- write a solution-independent problem and discriminating forces;
- describe essential structure, participants, collaborations, and dynamics;
- distinguish examples, known uses, variants, implementation notes, and related patterns;
- trace forces to decisions and consequences;
- use structural validation without overstating it as quality evidence;
- organize shepherding and workshop feedback into substantive revision.

## Core Exposition

### A form is an interface for design knowledge

The pattern form is an interface between an author's experience and a reader's future decision. Like a software interface, it should expose stable meaning and hide incidental detail without hiding necessary behavior. Section names may vary, but a reader needs access to recognition, rationale, construction, evidence, and navigation.

No universal template fits every scope. An object pattern may emphasize participants and collaborations. A distributed pattern needs failure, timing, delivery, and operational dynamics. An organizational pattern may describe roles and sequences rather than code. Choose fields that preserve the actual forces while retaining the causal core.

### Name and intent

The **name** creates vocabulary. It should be distinctive, pronounceable, and suggest the central image or mechanism without claiming an unearned benefit. “Reliable Queue” asserts a quality that depends on delivery and storage semantics; “Dead-Letter Channel” names a structural role more honestly.

**Intent** compresses the pattern into one or two sentences: the recurring problem addressed and the essential design effect. It is a retrieval aid, not a replacement for context or forces. If intent cannot be stated without several unrelated goals, the draft may contain multiple patterns.

Aliases help readers map established names, but indiscriminate renaming fragments vocabulary. Cite the canonical source when adopting an established pattern and explain material differences before assigning a new name.

### Context and indications

Context describes the system before application. Include facts that change fitness: lifecycle, scale, trust, variability, consistency, ownership, or existing patterns. Exclude background that does not discriminate.

**Indications** or symptoms help readers recognize the problem: repeated type tests, unbounded queue growth, synchronized client retries, or mapping logic spread across services. Symptoms are evidence prompts, not the problem itself. The same symptom can have different causes.

Preconditions belong here. If the solution requires idempotent operations, a stable identity, or an authoritative schema, say so before recommending it. Hidden preconditions turn pattern application into trial and error.

### Problem and forces

The problem should be a concise question or tension, stated without the solution name or participants. It must match the solution's abstraction level. A broad organizational problem cannot be solved fully by one helper class.

Forces explain why the problem resists a trivial solution. Name each force and show its direction. “Performance matters” is weak. “Consumers require low median latency, but unbounded concurrency exhausts the dependency during bursts” exposes a conflict. Include human and operational forces when they affect design.

Do not reverse-engineer forces solely to praise a chosen solution. Gather them from incidents, change history, constraints, measurements, interviews, and competing designs. Rank or group them locally without pretending unlike concerns share objective units.

### Motivation

Motivation is a concrete narrative that carries the reader from context through problem to a plausible solution. It can introduce a running example, show a failed direct design, and reveal how forces interact. It should illuminate rather than smuggle new preconditions or replace explicit sections.

Use one example whose details are easy to remember but not so product-specific that readers confuse them with the pattern. Later known uses demonstrate breadth.

### Solution and rationale

The solution states an instruction or configuration: introduce these responsibilities, connect them this way, and coordinate them under these rules. It must be constructable. “Add flexibility” is an objective; “encapsulate each algorithm behind a common strategy role and let the context delegate to a selected strategy” is a solution core.

Separate essentials from variation. Essential elements are those required for the force resolution claimed. Optional hooks, storage technologies, names, and optimizations belong in variants or implementation notes. Rationale maps decisions back to forces and should compare plausible alternatives.

### Structure, participants, and collaborations

Structure describes stable relationships. A diagram can help, but prose must define every role and dependency. Participants say who owns state and responsibilities. Collaborations describe messages, data, control, and lifecycle.

Dynamics answer what happens over time: registration, steady operation, failure, cancellation, recovery, and teardown. For concurrent or distributed patterns, describe ordering, concurrency, duplication, time, and partial failure explicitly. A static topology cannot express them.

### Consequences and resulting context

Consequences close the argument. Organize them by resolved forces, introduced liabilities, properties that remain unchanged, and new responsibilities. Quantify only where evidence supports it. “Adds one network hop and one durable queue” is more reviewable than “may reduce performance.”

The **resulting context** makes composition visible. Applying a queue pattern introduces capacity and poison-message problems; these can lead to backpressure and dead-letter patterns. It can also invalidate earlier assumptions. A pattern language grows from such transitions.

### Implementation, variants, and sample code

Implementation notes explain pitfalls and technology choices without redefining the pattern. Sample code demonstrates one instance and must state which parts are illustrative. Keep language-specific concerns here unless the pattern itself is an idiom.

Variants change some structure or policy while retaining the central problem and force resolution. Explain the changed context and consequences. If a variant solves a different problem or removes an essential participant, it may be a related pattern rather than a variant.

### Known uses and evidence

Known uses support claims that the solution has worked in actual settings. Identify the system, source, relevant context, and recognizable pattern role. Avoid unverifiable prestige lists. An implementation copied from another known use is not independent evidence of rediscovery, though it remains operational experience.

Pattern mining usually begins with multiple occurrences. Ask what is invariant, what varies, and which consequences repeat. Counterexamples and failed uses are valuable because they sharpen contraindications.

### Related patterns

Relations should be typed in prose: alternative solution to the same problem, prerequisite, component, specialization, generalization, frequent collaborator, successor in resulting context, or superficially similar but different. “See also Observer, Mediator, and Event Bus” provides navigation without knowledge.

Related-pattern analysis also guards scope. If half the solution is already another pattern, reference and compose it rather than silently duplicating it.

### Review and revision

Authors are too close to their own context to see every hidden assumption. A shepherd can ask repeated recognition and force questions across drafts. A writers' workshop emphasizes how informed readers experience the text: what they understood, where the argument broke, and which alternatives or consequences are missing.

Review form and content separately. Structural validation can ensure required sections exist. Technical review checks mechanism, evidence, and consequences. Reader review checks whether the pattern transfers without the author's oral explanation. Revision should repair the earliest broken link in the causal chain, not merely add more prose.

## Definitions and Notation

Define a pattern document as a mapping from fields to claims:

$$
D=\{name\mapsto N,context\mapsto C,problem\mapsto P,forces\mapsto F,
solution\mapsto S,consequences\mapsto K,uses\mapsto U,relations\mapsto R\}.
$$

Let solution decisions be $Q=\{q_1,\ldots,q_m\}$. A **rationale trace** is

$$
T\subseteq F\times Q\times K.
$$

Coverage requires every dominant force to connect to at least one decision and every material decision to at least one anticipated consequence. Coverage detects unexplained claims; it does not prove the decision resolves the force.

Let $U=\{u_1,\ldots,u_n\}$ be known uses and (origin(u_i)) identify lineage. Independent recurrence requires diversity beyond repeated deployment of one inherited implementation. There is no universal numeric threshold; the document should state the evidence actually available.

A form validator checks predicates such as (present(field)), (nonempty(field)), and declared trace coverage. Let (StructuralPass(D)) denote those checks. In general,

$$
StructuralPass(D)\not\Rightarrow PatternQuality(D).
$$

Quality additionally depends on truth, recurrence, coherence, readability, appropriate scope, and evidence.

## Mechanisms, Invariants, or Proof Structure

### Read in three passes

First, perform a **recognition pass** over name, context, problem, and intent: do you face this situation? Second, perform a **mechanism pass** over solution, structure, participants, and dynamics: how does it work? Third, perform a **judgment pass** over forces, consequences, known uses, variants, and relations: is it justified here?

### Write problem-first

Draft context, problem, and forces before naming the solution. Remove participant names from the problem. Compare at least one simpler alternative. Only then state the solution core. This sequence reduces solution bias.

### Build the rationale trace

Create a table from each force to the decisions that answer it and the resulting benefits or liabilities. Unmapped forces indicate a weak solution; unmapped decisions indicate accidental complexity; benefit-only traces indicate missing costs.

### Exercise the dynamics

Walk at least normal operation, boundary capacity, participant failure, cancellation or abandonment, recovery, and teardown where applicable. Ask who owns state and who observes each failure. Convert missing decisions into explicit variants or contraindications.

### Audit known uses

For each occurrence, record evidence source, independence, context match, visible roles, and observed consequences. Remove examples that are only hypothetical or share no essential mechanism.

### Validate structure without confusing it with quality

This executable checker verifies a small required-field and trace-coverage contract. It cannot judge whether prose is true, coherent, recurrent, or useful.

<!-- bijux-verify: {"id":"pattern-form-structure","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fields: complete\nforces covered: 3/3\ndecisions traced: 2/2\nstructural result: pass\nquality result: requires human and empirical review\n","stderr":""}} -->
```python
draft = {
    "name": "Bounded Work Queue",
    "context": "bursty producers and slower consumers",
    "problem": "contain overload without losing control of admission",
    "forces": ("bounded memory", "throughput", "visible saturation"),
    "solution": "finite queue with an explicit full-queue policy",
    "consequences": ("backpressure or rejection", "queueing latency", "capacity tuning"),
    "known_uses": ("system-a", "system-b"),
    "related_patterns": ("Producer-Consumer", "Load Shedding"),
}

trace = {
    "bounded memory": ("finite capacity",),
    "throughput": ("decoupled producer and consumer",),
    "visible saturation": ("finite capacity",),
}

required = (
    "name", "context", "problem", "forces", "solution",
    "consequences", "known_uses", "related_patterns",
)
decisions = {decision for mapped in trace.values() for decision in mapped}
expected_decisions = {"finite capacity", "decoupled producer and consumer"}

print("fields:", "complete" if all(draft.get(field) for field in required) else "incomplete")
print(f"forces covered: {sum(force in trace for force in draft['forces'])}/{len(draft['forces'])}")
print(f"decisions traced: {len(decisions & expected_decisions)}/{len(expected_decisions)}")
structural_pass = all(draft.get(field) for field in required) and set(draft["forces"]) <= set(trace)
print("structural result:", "pass" if structural_pass else "fail")
print("quality result: requires human and empirical review")
```

### Revise from causal breaks

When feedback reports confusion, locate the earliest link: missing context, ambiguous problem, unranked forces, nonconstructable solution, or incomplete consequences. Repairing the cause is better than adding an FAQ around it.

## Alternatives and Trade-Offs

**Alexandrian narrative form.** A compact context–problem–forces–solution–resulting-context narrative preserves flow and adaptation. Readers may need supplemental implementation detail for software mechanisms.

**Catalog template.** Separate intent, motivation, applicability, structure, participants, collaborations, consequences, implementation, sample code, known uses, and related patterns support reference use. Rigid completion can invite filler.

**Problem–solution card.** A one-page card improves discovery and review speed. It should link to evidence and dynamics rather than pretending to be sufficient for complex patterns.

**Literate case study.** A narrative can expose real decisions and consequences vividly. The reusable core may be hard to extract unless explicit pattern fields summarize it.

**Machine-readable pattern schema.** Structured metadata supports search, linting, and relationship graphs. It cannot encode the full nuance of forces or validate truth automatically.

**Code-first reference implementation.** Code proves one construction path and enables tests. It overfits a language and can cause readers to copy incidental structure.

**Individual expert review.** A technical expert can challenge correctness deeply. A workshop adds diverse reader interpretation and transfer feedback; neither replaces source and operational evidence.

## Failure Modes and Misconceptions

1. **Completing every heading proves a pattern exists.** Structure is necessary evidence organization, not recurrence or quality proof.
2. **The name should advertise the benefit.** Benefit claims can conceal conditionality and failure modes.
3. **Motivation can replace context and forces.** Stories aid comprehension but make assumptions hard to retrieve if not stated explicitly.
4. **A static diagram explains the solution.** It omits lifecycle, ordering, failure, recovery, and teardown.
5. **Implementation notes belong in the solution core.** Technology choices can freeze incidental variants and reduce transfer.
6. **Two deployments of copied code are two independent known uses.** They show operation, not independent rediscovery or generality.
7. **Known use means endorsement.** An occurrence may exhibit negative consequences or be retained only because migration is costly.
8. **Related patterns are bibliography.** The relation must explain choice, composition, or resulting-context navigation.
9. **Longer prose resolves review feedback.** Additional words can bury an unresolved causal gap.
10. **Friendly peer review replaces verification.** Readability feedback does not establish semantic, performance, security, or production claims.

## Worked Examples

### Example 1

**Question:** Is “FlexibleFactory” a good pattern name?

**Reasoning:** It combines a vague benefit with a familiar solution word and does not distinguish the recurring problem. “Abstract Factory” names the abstraction role and is established vocabulary; a new variant should explain why a new name is needed.

**Conclusion:** Prefer distinctive mechanism or image over an unbounded quality claim, and preserve established names when meaning matches.

### Example 2

**Question:** Rewrite “How do we implement an Observer?” as a pattern problem.

**Reasoning:** Remove the solution participant and state the tension: “How can one subject notify a varying set of dependents about state changes without depending directly on their concrete types?” This admits direct calls, callbacks, polling, or event channels for comparison.

**Conclusion:** A solution-independent problem keeps alternatives visible.

### Example 3

**Question:** Why is “performance” a weak force?

**Reasoning:** It gives no direction, measure, or conflict. “Dispatch must add less than 2 ms at the 99th percentile, while subscribers may be added independently” exposes latency and extensibility in tension. Evidence can now test both.

**Conclusion:** A force becomes useful when its pressure and conflict discriminate among designs.

### Example 4

**Question:** What is missing from a queue structure diagram?

**Reasoning:** Producer, queue, and consumer boxes show topology. The pattern still needs enqueue behavior when full, consumer failure, item ownership, ordering, cancellation, shutdown, restart, and monitoring. These dynamics determine whether memory is bounded and work is lost or delayed.

**Conclusion:** Constructable pattern solutions require temporal and failure semantics.

### Example 5

**Question:** Is a tutorial's fictional shop a known use of Repository?

**Reasoning:** It illustrates the roles but supplies no independent occurrence or operational evidence. It belongs under motivation or example. A known use identifies a real system or documented source and explains how the recognizable pattern operated in context.

**Conclusion:** Illustration supports understanding; known use supports recurrence and feasibility.

### Example 6

**Question:** What does the executable checker establish for Bounded Work Queue?

**Reasoning:** It confirms eight fields are nonempty, all three named forces have trace entries, and two expected decisions appear. It cannot tell whether `system-a` exists, whether forces are important, or whether finite capacity resolves overload safely.

**Conclusion:** Structural validation detects omissions but deliberately defers truth and quality review.

### Example 7

**Question:** Is a lossy queue a variant of Bounded Work Queue?

**Reasoning:** Both preserve finite capacity, but one blocks producers and another drops items under a declared policy. They address the same overload context with different latency, loss, and producer-coupling consequences. If loss changes the problem domain fundamentally, the variant may be better documented as Load Shedding composed with a bounded queue.

**Conclusion:** Variant boundaries depend on preserved intent and force resolution, not superficial structure.

### Example 8

**Question:** How should Circuit Breaker relate to Retry?

**Reasoning:** Retry may precede a breaker for bounded transient attempts, while the breaker suppresses calls when failure evidence crosses policy. They can complement or conflict: retries inflate failure counts and probes. The relation should state ordering, shared budgets, and amplification risks.

**Conclusion:** A related-pattern entry explains interaction and selection, not merely proximity.

### Example 9

**Question:** Workshop readers understand the solution but cannot tell when to use it. What should the author revise?

**Reasoning:** Adding code would not repair recognition. The author should sharpen context, indications, problem, force priorities, and contraindications, then verify that motivation illustrates them. Only after that should solution detail be reconsidered.

**Conclusion:** Revise the earliest broken reader task rather than the most visible section.

### Example 10

**Question:** A pattern's known uses all derive from one open-source framework. What can be claimed?

**Reasoning:** The deployments support feasibility and may reveal operating consequences. Because they inherit one design lineage, they provide limited evidence of independent recurrence. The author should report lineage, seek distinct occurrences, and narrow generality claims meanwhile.

**Conclusion:** Evidence quality depends on independence and context diversity, not just occurrence count.

## Cross-Program Connections

- **Programming Languages & Semantics:** solution dynamics need explicit execution, error, and ordering models.
- **Metaprogramming:** machine-readable forms and validators can check structure but not semantic quality.
- **Software Design & Domain Modeling:** solution-independent problem statements prevent technical patterns from redefining domain needs.
- **Software Architecture:** pattern forms document local reusable decisions; architectural records document one system's chosen instance.
- **Testing & Quality Engineering:** consequences become hypotheses and conformance properties.
- **Distributed Systems:** timing, duplication, partial failure, and recovery make dynamics central to the form.
- **Security Engineering:** trust boundaries and authority must appear in context, forces, solution, and consequences.
- **Technical Writing:** headings support retrieval; motivation supports comprehension; examples support transfer; review tests reader experience.
- **Research Methods:** known uses, independence, counterexamples, and bounded claims resemble empirical case evidence.
- **Engineering Management:** shepherding, workshops, and revision practices create shared ownership of design knowledge.

## References

1. Gerard Meszaros and Jim Doble, [“A Pattern Language for Pattern Writing”](https://hillside.net/index.php/a-pattern-language-for-pattern-writing), in *Pattern Languages of Program Design 3*, Addison-Wesley, 1998. A self-demonstrating language for context, problem, forces, solution, resulting context, readability, examples, and relations.
2. The Hillside Group, [“Gang of Four Template”](https://hillside.net/index.php/gang-of-four-template), accessed 2026-08-28. The catalog form for intent, motivation, applicability, structure, participants, collaborations, consequences, implementation, code, known uses, and relations.
3. The Hillside Group, [“Pattern Writing Checklist”](https://hillside.net/index.php/pattern-writing-checklist), accessed 2026-08-28. Doug Lea's checklist emphasizing constructability, force evidence, variation, actual uses, generality, variants, and relationships.
4. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, [*Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*](https://www.oreilly.com/library/view/pattern-oriented-software-architecture/9781118725269/), Wiley, 1996. Provides a detailed pattern description form and reader paths through context, problem, solution, implementation, and pattern systems.
5. Frank Buschmann, Kevlin Henney, and Douglas C. Schmidt, [*Pattern-Oriented Software Architecture, Volume 5: On Patterns and Pattern Languages*](https://www.oreilly.com/library/view/pattern-oriented-software/9780471486480/30_pattern-concept.html), Wiley, 2007. Examines forces, context, consequences, pattern quality, and pattern-language concepts critically.
6. James O. Coplien and Bobby Woolf, [“A Pattern Language for Writers' Workshops”](https://hillside.net/documents/PatternLanguageForWritersWorkshops.pdf), 1999 revision. Documents reader-centered workshop practices as a complement to conventional technical review.
7. Christopher Alexander, Sara Ishikawa, Murray Silverstein, et al., *A Pattern Language: Towns, Buildings, Construction*, Oxford University Press, 1977, ISBN 978-0-19-501919-3. The foundational example of connected, generative pattern forms and resulting-context navigation.

## Exercises

### Exercise 1

For a proposed “Versioned Cache” pattern, list the minimum information you would seek in each of these fields: context, problem, forces, solution, dynamics, consequences, known uses, and related patterns.

### Exercise 2

Modify the structural-checker model mentally so `visible saturation` has no trace entry. State the printed force coverage and structural result. Explain what human review must ask next.

### Exercise 3

Diagnose this draft: context says only “modern services”; problem says “how to add a circuit breaker”; forces list “quality” and “best practice”; solution gives a library annotation; consequences say “more resilient”; known uses list three unnamed clients. Rewrite its context, problem, and two forces.

### Exercise 4

Design a three-pass reading protocol for comparing Observer, Mediator, and an Event Bus for one system. State which fields you inspect in each pass and what decision evidence you record.

### Exercise 5

You have three independently built incident-response tools that all quarantine malformed messages differently. Outline a pattern-mining and review process that could produce one defensible pattern document without erasing meaningful variants.

## Answers to the Exercises

### Answer 1

The context should identify repeated expensive reads, a source of truth, version identity, allowed staleness, and deployment/failure boundaries. The problem should state how to reuse a value while preventing clients from accepting a value for the wrong version. Forces should include latency, source load, freshness, version lookup cost, memory, invalidation, and observability. The solution should define cache key/version relationship, authority, validation, and miss behavior.

Dynamics should cover lookup, hit, version change, stale entry, concurrent fill, eviction, source failure, and restart. Consequences should include faster reads and lower source load plus memory, invalidation/version coupling, stampede risk, and diagnostic state. Known uses must identify real systems and recognizable version-key behavior. Related patterns should explain Cache-Aside, Memoization, Single Flight, and invalidation or event-driven update relationships rather than list names.

### Answer 2

Only two of three forces occur in `trace`, so the checker would print `forces covered: 2/3` and `structural result: fail`. Human review must ask whether visible saturation is actually a dominant force, which decision exposes it—capacity metrics, rejection signals, or queue-depth telemetry—and which benefits and liabilities follow. Adding a dummy mapping passes structure but does not show that operators can detect saturation in time.

### Answer 3

The context is nondiscriminating, the problem assumes a solution, the forces are slogans, the solution is a product idiom, the consequence is untestable, and known uses are unverifiable. A stronger version is:

- **Context:** A synchronous client calls a remote dependency that experiences correlated failures. Calls have 300 ms deadlines, traffic is high enough that failed attempts consume material capacity, and callers can return a degraded response.
- **Problem:** How can the client stop spending request and dependency capacity on calls unlikely to succeed while detecting recovery soon enough to resume service?
- **Force 1:** Fast failure contains latency and load during an outage, but suppressing calls can reject work after the dependency recovers.
- **Force 2:** Recovery probes provide evidence, but too many probes recreate overload and too few delay restoration.

The annotation becomes one implementation note. Consequences must include state, false-open/false-closed policy, observability, and interaction with retries.

### Answer 4

In the recognition pass, read context, problem, intent, indications, and contraindications for all three. Record whether the system needs one-to-many notification, coordination among peers, or cross-boundary asynchronous distribution; also record lifecycle and failure-domain facts.

In the mechanism pass, read participants, collaborations, and dynamics. Trace registration, routing, ordering, errors, reentrancy, backpressure, delivery, and teardown. In the judgment pass, compare forces, consequences, known uses, variants, and relations. Record mandatory constraints, evidence for subscriber variability, latency and failure measurements, ownership introduced by each candidate, and the simplest alternative. The result may compose patterns or choose explicit calls; the protocol does not force one catalog name.

### Answer 5

First document each occurrence independently: incoming message context, malformed criteria, quarantine storage, identity, operator workflow, retry or disposal, security, and measured consequences. Establish lineage so copied designs are not counted as independent rediscovery. Interview maintainers and inspect incidents to extract common forces and divergent constraints.

Draft a solution-independent problem and common force set before naming the solution. Identify an essential core—separate malformed messages from normal flow while preserving evidence and an explicit disposition path—and mark storage, notification, retention, and replay policies as candidate variants. Trace every force to decisions and consequences. Include failures such as quarantine overload, sensitive payload exposure, and endless replay.

Use a shepherd to challenge scope and evidence, then a workshop with maintainers and readers unfamiliar with the tools. Validate whether each team recognizes its problem and can construct an instance without copying one product. Retain variants when they respond to real context differences; split a distinct pattern if one variant solves a different problem. Publish named known uses with consent, limitations, contraindications, typed related-pattern links, and unresolved evidence gaps. No review process should claim generality beyond the three independent cases without further evidence.
