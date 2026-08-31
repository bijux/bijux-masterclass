---
module_id: SEPAT-007
program: Software Engineering: Patterns
level: 1
module_number: 7
title: Pattern Sequences and Pattern Languages
status: complete
last_verified: 2026-08-28
---

# Pattern Sequences and Pattern Languages

## One-Page Review

### Governing question

How can related patterns guide a designer through successive context changes without becoming a fixed recipe or an unstructured catalog?

### Essential definitions

- A **pattern collection** groups patterns around a topic without necessarily relating their use.
- A **pattern catalog** provides a consistent index and description form for lookup and comparison.
- A **pattern system** organizes patterns and their relationships within a domain.
- A **pattern sequence** is a context-sensitive path in which applying one pattern creates or reveals the context for considering another.
- A **pattern language** is a coherent network of patterns that helps generate whole designs in a domain through typed relationships, entry points, sequences, alternatives, and resulting contexts.
- A **root pattern** or **entry pattern** gives a high-level starting point from which more specific problems become visible.
- A **resulting context** is the situation after applying a pattern, including resolved forces and new problems.
- A **branch** represents alternative next patterns under different force configurations; a **feedback edge** returns to an earlier concern after new evidence.
- **Generativity** is the capacity to guide construction and adaptation, rather than merely classify finished designs.

### Central model, mechanism, or theorem

Model a language as a directed, typed graph

$$
L=(P,R,E),
$$

where (P) is patterns, (R) is relationship types, and $E\subseteq P\times R\times P$ is edges. Design state (x_i) determines which outgoing edge is admissible:

$$
x_{i+1}=apply(p_i,x_i),\qquad
p_{i+1}\in applicable(successors(p_i),x_{i+1}).
$$

A sequence is therefore a path discovered through resulting contexts, not the printed order of a book. Different projects can take different paths, revisit earlier patterns, or stop when no remaining force justifies another move.

### Critical invariants

- Every edge states a semantic relationship: prerequisite, refinement, alternative, complement, conflict, or resulting-context successor.
- Entry points match recognizable domain contexts and reader goals.
- A sequence re-evaluates forces after every application; later patterns are not automatic.
- Branches and stopping conditions remain explicit.
- Higher-level patterns constrain but do not mechanically determine lower-level implementations.
- The language covers a coherent domain without claiming universal completeness.
- Navigation, construction, and verification evidence are distinct.

### Common failures

Common failures include calling a tagged list a language, treating chapter order as a sequence, using arrows without relationship meanings, forcing one path for all contexts, omitting alternatives and stopping conditions, hiding context introduced by earlier patterns, claiming completeness from catalog size, and creating cycles that provide no design guidance.

### Compact example

An integration language may begin with Messaging when asynchronous integration fits. Resulting questions lead to Message Channel, Message, and Message Endpoint. A format mismatch leads toward Message Translator; multiple source formats may refine that choice to Normalizer. Poison messages create a different successor such as Dead-Letter Channel. A project follows only the branches activated by its context.

### Connections

[SEPAT-006](006-pattern-composition.md) integrates patterns in one design; this module explains navigation across evolving contexts. [SEPAT-008](../ROADMAP.md) uses sequences to evolve existing designs. Pattern-language navigation connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md), and the messaging modules later in this program.

## Governing Question

What turns a set of individually useful patterns into a language that helps people unfold a coherent design?

A catalog answers “what patterns exist?” A language also answers “where can I enter, what problem follows from this choice, what alternatives fit the new forces, and when should I stop?” It preserves relationships among scales and topics so designers can move from a broad domain structure to concrete collaborations without assuming one universal architecture.

The word *language* is deliberately demanding. A pattern language is not a vocabulary list, directory taxonomy, or dependency graph. Its edges carry contextual design knowledge. The result should help a practitioner produce a design that fits local conditions, not merely annotate an existing design with names.

## Why This Matters

Isolated patterns can solve local problems while producing an incoherent whole. A Queue chosen without endpoint, message identity, failure, and management patterns leaves essential operations unspecified. Repository chosen without transaction and identity scope can conflict with Unit of Work. A language makes these resulting-context problems visible.

Sequences also control overengineering. A catalog invites browsing and pattern accumulation. A generative path asks the current problem at each step and stops when the resulting context is acceptable. Optional branches remain optional.

For teaching, a language separates conceptual order from page order. Learners can start at root patterns, follow domain paths, compare alternatives, and return to deeper details. For production, the network gives reviewers traceability from broad forces to local mechanisms and exposes gaps where the language lacks evidence.

## Prerequisites and Retrieval

You should understand pattern form, applicability, resulting context, composition, and graph basics. Retrieve these facts:

1. Applying a pattern changes context and introduces new consequences.
2. Related patterns can be alternatives, complements, refinements, prerequisites, or successors.
3. A design process contains feedback and uncertainty; it is not necessarily linear.
4. A more detailed pattern should preserve constraints established at a broader level.
5. Stopping is a design decision: no pattern is justified when no material force remains.
6. Coverage of known patterns does not establish completeness of a domain language.

## Learning Objectives

After completing this module, you should be able to:

- distinguish collection, catalog, system, sequence, and language;
- type relationships among patterns;
- identify root patterns and context-sensitive entry points;
- derive next candidates from resulting context;
- represent branches, alternatives, feedback, and stopping conditions;
- distinguish book order, implementation order, and generative sequence;
- audit a claimed language for coherence, coverage, and navigability;
- use a language without surrendering local design judgment.

## Core Exposition

### From vocabulary to generative structure

A collection can be valuable even when relationships are weak. A catalog improves retrieval through a common form. A pattern system adds classification and cross-references. A language must go further: it organizes a domain so application of one pattern helps reveal and resolve the next problem.

Generativity does not mean automatic code generation. It means the language supports a constructive conversation with context. The designer observes forces, applies an appropriate pattern, examines the resulting context, and follows a justified relation to another candidate.

### Resulting context drives sequence

Pattern order comes from state transitions. A Message Channel creates questions about delivery semantics and endpoints. A bounded queue creates saturation, admission, and poison-item questions. A Facade creates compatibility and evolution responsibilities. These problems are not arbitrary cross-links; they arise because of the preceding choice.

Consequently, a sequence is conditional. A lossless workload may choose backpressure after Bounded Buffer; a best-effort telemetry path may choose Load Shedding. Both start from the same capacity problem and branch on different consequences.

### Relationship types

Useful language edges include:

- **requires:** the target establishes a precondition;
- **refines:** the target specializes a broader pattern;
- **alternative:** both address a similar problem under different forces;
- **complements:** the target resolves another aspect of the same resulting context;
- **uses:** the source solution incorporates the target mechanism;
- **conflicts:** simultaneous application creates incompatible obligations;
- **precedes:** the source normally establishes context for the target;
- **follows:** the target addresses a resulting problem;
- **generalizes:** the target captures a broader relationship.

“Related to” is too weak when a precise relation is known. One pair can have different relations under different contexts, so document rationale rather than force one global edge type.

### Entry points and scale

Readers enter with different problems. An application developer may enter an integration language at Message Endpoint; an architect at Integration Style; an operator at System Management. Root patterns provide a high-level map, but a usable language also offers symptom, role, and goal indexes.

Patterns at larger scale establish boundaries and forces for smaller patterns. Ports and Adapters can create adapter roles later implemented using Adapter, Facade, or Anti-Corruption Layer decisions. Lower-level patterns must not silently violate higher-level ownership or trust boundaries.

### Sequences are not recipes

A recipe prescribes ordered steps under narrow preconditions. A pattern sequence offers conditional choices. Applying pattern (p) does not mandate every successor. The designer reassesses context and can choose a branch, revisit an earlier decision, or stop.

Some transitions have practical precedence: establish message identity before deduplication, or define a deadline before allocating retries. Even then, implementation can be iterative and partial. Describe the dependency rather than claiming one project schedule.

### Branching, feedback, and repair

A language is usually a network, not a tree. Alternatives branch; later evidence can require revisiting capacity, boundaries, or error semantics. Feedback edges should explain what new evidence invalidates an assumption.

Cycles are useful only when they guide refinement. “A relates to B and B relates to A” adds no direction. “Load testing after Competing Consumers reveals database contention, prompting reconsideration of concurrency partitioning” is actionable feedback.

### Coherence and coverage

Coherence means patterns address a shared domain and their relationships preserve compatible concepts and force vocabulary. A language mixing object construction, incident management, and UI layout needs an explicit larger domain or should be separated.

Coverage is bounded. State scope, audience, exclusions, maturity, and evidence gaps. A language can be useful without solving every domain problem. False completeness is more dangerous than an explicit missing pattern.

### Language evidence

Each node needs pattern evidence. Each edge also needs evidence: known sequences, causal resulting contexts, or reviewed design reasoning. Whole-language evidence includes whether practitioners can find entry points, construct designs, distinguish alternatives, and avoid known failure modes.

Evaluate independent projects, not only examples derived from the language. Otherwise the language can appear coherent because users copied its assumptions.

### Evolution and versioning

Pattern languages are living knowledge. New contexts introduce nodes; repeated confusion reveals missing edges; obsolete technology assumptions change idioms while durable patterns remain. Version relationship meaning and preserve aliases so design records remain interpretable.

Removal is also evolution. Merge duplicate patterns, split overloaded ones, and retire unsupported claims with migration notes. Avoid a graph where every new pattern links to everything else.

## Definitions and Notation

Let a pattern language be

$$
L=(P,R,E,A,S),
$$

where (P) is patterns, (R) typed relationships, $E\subseteq P\times R\times P$ edges, (A) entry conditions, and (S) stopping predicates. A design state (x) contains current context, unresolved forces, decisions, and evidence.

An application transition is partial:

$$
apply:P\times X\rightharpoonup X.
$$

It is defined only when the pattern is applicable and its preconditions hold. Candidate successors are

$$
Next_L(p,x')=\{q\mid (p,r,q)\in E\land guard(r,q,x')\}.
$$

A sequence is a path

$$
\sigma=(p_1,x_1),(p_2,x_2),\ldots,(p_n,x_n)
$$

where each transition is defined and each next node passes its edge guard. Completion for this path is contextual:

$$
Stop_L(x_n)=true,
$$

not “every node in (P) was applied.”

Graph reachability supports navigation but does not prove semantic validity. A typed edge with a prose rationale and evidence is stronger than an untyped hyperlink.

## Mechanisms, Invariants, or Proof Structure

### Define domain and boundaries

State the problems covered, intended users, scales, excluded concerns, and evidence threshold. Split incoherent domains before drawing edges.

### Establish root patterns and entry conditions

Find broad recurring decisions that reveal smaller problems. Add symptom- and role-based entry points so readers need not know the root name.

### Derive edges from resulting context

For every pattern, list new problems and plausible alternatives. Type each edge and state the guard that activates it. Remove ornamental links.

### Traverse a small language

This executable model follows one integration path. It selects only successors whose guards match the evolving facts.

<!-- bijux-verify: {"id":"resulting-context-traversal","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entry: Message Channel\nnext: Message Translator\nnext: Normalizer\nnext: Dead-Letter Channel\nstop: declared integration problems covered\n","stderr":""}} -->
```python
facts = {
    "format_mismatch": True,
    "many_source_formats": True,
    "poison_messages": True,
}

edges = {
    "Message Channel": (("format_mismatch", "Message Translator"),),
    "Message Translator": (("many_source_formats", "Normalizer"),),
    "Normalizer": (("poison_messages", "Dead-Letter Channel"),),
    "Dead-Letter Channel": (),
}

current = "Message Channel"
print("entry:", current)
while edges[current]:
    selected = [target for guard, target in edges[current] if facts.get(guard, False)]
    if not selected:
        break
    current = selected[0]
    print("next:", current)
print("stop: declared integration problems covered")
```

This model demonstrates guarded navigation, not design correctness. Real branches can have several admissible alternatives and need consequence comparison.

### Audit paths and gaps

Test representative beginner, specialist, and adverse paths. Find dead ends, unjustified cycles, unreachable patterns, missing alternatives, and nodes with too many vague links.

### Validate with independent use

Observe whether practitioners can enter from real problems, explain choices, construct coherent designs, and stop. Record deviations as evidence for evolution rather than noncompliance.

## Alternatives and Trade-Offs

**Flat catalog.** Easy to publish and search. It leaves composition and ordering to readers.

**Taxonomic hierarchy.** Groups by scope or intent and supports browsing. Parent-child classification does not necessarily guide application.

**Decision tree.** Makes exclusive branches explicit. It struggles with feedback, composition, multiple active forces, and evolving evidence.

**Directed pattern graph.** Represents rich relationships and multiple paths. Without typed edges and guards it becomes a link cloud.

**Reference architecture.** Provides a concrete whole and implementation constraints. It embodies one path rather than preserving a family of contextual paths.

**Playbook.** Gives operational steps and checkpoints for a narrower environment. It can link to a pattern language for rationale.

**Automated recommender.** Can filter by declared facts and expose candidate paths. It cannot validate evidence or assume stakeholder priorities safely.

## Failure Modes and Misconceptions

1. **A large catalog is a language.** Size does not provide generativity or relationships.
2. **The table of contents is the sequence.** Publication order supports reading, not necessarily design transitions.
3. **Every edge means “use next.”** Relationship type and contextual guard determine meaning.
4. **A sequence is a recipe.** It branches, revisits, and stops based on resulting context.
5. **Root patterns must be applied first in code.** They orient reasoning; implementation can proceed incrementally.
6. **Cycles show richness.** Unexplained cycles create navigation noise.
7. **Every project should use the whole language.** Completion is contextual, not node coverage.
8. **A framework is the language.** It embodies selected paths and policies but does not exhaust the reusable reasoning.
9. **Cross-references prove coherence.** Shared concepts, compatible forces, and evidenced transitions do.
10. **A language is finished when published.** Independent use, new contexts, and failures drive evolution.

## Worked Examples

### Example 1

**Question:** Is the Gang of Four book automatically a pattern language?

**Reasoning:** It is a systematic catalog with rich related-pattern entries and compositions. A language claim additionally asks for contextual entry points and generative sequences across resulting contexts. Readers can use the catalog language-like, but the classification depends on the stronger navigation evidence.

**Conclusion:** A strong catalog can support a language without publication format alone proving one.

### Example 2

**Question:** How does Factory Method lead to another pattern?

**Reasoning:** Factory Method resolves subclass-controlled creation. If entire product families must vary together, its resulting limits indicate Abstract Factory as an alternative or refinement. If construction itself is staged, Builder addresses a different branch.

**Conclusion:** Successors arise from newly visible forces, not catalog numbering.

### Example 3

**Question:** What is a stopping condition after Adapter?

**Reasoning:** If one provider is translated faithfully behind a stable local contract, conformance tests pass, and no broader subsystem simplification or provider selection force exists, stop. Facade and Strategy are not mandatory decorations.

**Conclusion:** A language prevents pattern accumulation by making “problem resolved” a valid endpoint.

### Example 4

**Question:** Why can Bounded Buffer branch?

**Reasoning:** Saturation with lossless work may lead to producer backpressure. Best-effort work may lead to Load Shedding. Poison items may lead to quarantine. Fairness or priority can lead to scheduling patterns.

**Conclusion:** One resulting context exposes multiple guarded branches.

### Example 5

**Question:** Is Ports and Adapters followed mechanically by Repository?

**Reasoning:** A persistence port may be implemented by Repository when domain-oriented collection semantics fit. Reporting queries may use explicit query services; a key-value domain may need a simpler port. The higher-level boundary constrains dependency direction but not one data pattern.

**Conclusion:** Broader patterns constrain choices without determining them.

### Example 6

**Question:** What does the traversal program establish?

**Reasoning:** Given three true facts and one outgoing edge at each node, it reproducibly follows Channel, Translator, Normalizer, and Dead-Letter Channel. It does not establish that Messaging was initially applicable or that these implementations satisfy delivery and failure contracts.

**Conclusion:** Graph traversal verifies navigation logic, not pattern fitness or system behavior.

### Example 7

**Question:** How can a feedback edge improve a resilience language?

**Reasoning:** After Retry and Circuit Breaker, load testing may reveal queue growth and missed deadlines. A feedback edge returns to Timeout/Deadline and admission-budget decisions with new evidence instead of adding another resilience wrapper.

**Conclusion:** Useful feedback links specify the observation that reopens an earlier decision.

### Example 8

**Question:** When are two patterns alternatives rather than successors?

**Reasoning:** Active Record and Data Mapper both organize persistence but fit different domain complexity and coupling forces. Applying one does not normally create the other as a next step; a context change can motivate migration.

**Conclusion:** Type the relation as alternative, with migration as a separate transition.

### Example 9

**Question:** What makes a security pattern graph incoherent?

**Reasoning:** If authentication, input validation, encryption, and audit nodes link only because all concern security, the graph lacks causal contexts and scale. Separate trust-boundary, identity, data-protection, and operations paths, then state their interactions.

**Conclusion:** A common topic is insufficient; relations must guide force resolution.

### Example 10

**Question:** How should a language record an evidence gap?

**Reasoning:** Suppose several projects use Transactional Outbox followed by Idempotent Consumer, but retention interactions are undocumented. Mark the edge supported for duplicate-delivery handling while labeling retention and replay-window policy unresolved; add a review target rather than a universal claim.

**Conclusion:** Explicit incompleteness makes a language safer and directs future mining.

## Cross-Program Connections

- **Programming Languages:** grammar is only an analogy; pattern languages are contextual design networks, not formal languages by default.
- **Software Design:** pattern sequences unfold solution structure while preserving domain/problem separation.
- **Software Architecture:** root patterns and quality boundaries connect larger decisions to local patterns.
- **Testing & Quality Engineering:** path, edge, branch, and stopping claims need independent scenarios and evidence.
- **Database Engineering:** persistence languages relate transaction, identity, mapping, query, and cache patterns.
- **Distributed Systems:** resulting contexts expose timing, delivery, duplication, coordination, and recovery branches.
- **Security Engineering:** security languages need explicit trust contexts and cannot be a checklist of controls.
- **Platform Engineering:** reference implementations embody approved paths while the language preserves rationale and alternatives.
- **Technical Leadership:** shared language improves design conversation only when names retrieve full conditional arguments.
- **Knowledge Management:** versioned edges, aliases, evidence, and gaps make experiential knowledge maintainable.

## References

1. Christopher Alexander, Sara Ishikawa, Murray Silverstein, et al., *A Pattern Language: Towns, Buildings, Construction*, Oxford University Press, 1977. The foundational connected language of patterns across scales and resulting contexts.
2. Kent Beck and Ward Cunningham, [“Using Pattern Languages for Object-Oriented Programs”](https://c2.com/doc/oopsla87.html), Technical Report CR-87-43, 1987. Early primary adaptation of pattern-language thinking to object-oriented program construction.
3. Frank Buschmann, Kevlin Henney, and Douglas C. Schmidt, [*Pattern-Oriented Software Architecture, Volume 5: On Patterns and Pattern Languages*](https://www.oreilly.com/library/view/pattern-oriented-software/9780471486480/30_pattern-concept.html), Wiley, 2007. Distinguishes collections, sequences, compounds, and languages and examines their generative character.
4. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*, Wiley, 1996. Provides a pattern system spanning architectural, design, and idiomatic scales.
5. Gregor Hohpe and Bobby Woolf, [*Enterprise Integration Patterns* introduction and language organization](https://www.enterpriseintegrationpatterns.com/patterns/messaging/Introduction.html), Addison-Wesley, 2003. Demonstrates root patterns, topical branches, typed refinements, and non-linear navigation in a production integration domain.
6. James O. Coplien, *Software Patterns*, SIGS Books, 1996, ISBN 978-1-884842-50-4. Develops organizational and process pattern languages, sequences, and generative application.
7. Munawar Hafiz, Paul Adamczyk, and Ralph Johnson, [“Growing a Pattern Language (for Security)”](https://www.hillside.net/plop/2011/papers/A-39-Hafiz.pdf), PLoP 2011. Examines resulting-context links, branches, sequences, and evolution across a large security-pattern body.

## Exercises

### Exercise 1

Classify each artifact as collection, catalog, system, sequence, or language: an alphabetical list of concurrency patterns; consistently formatted GoF entries; a graph classifying messaging patterns by intent; one context-sensitive path through four resilience patterns; and a network with entry points, typed guarded edges, alternatives, and stopping conditions.

### Exercise 2

Set `many_source_formats` to false in the executable traversal. State the resulting output and explain whether Dead-Letter Channel becomes unreachable because it is irrelevant or because the toy graph is incomplete.

### Exercise 3

Create typed relationships among Adapter, Facade, Strategy, and Anti-Corruption Layer for integrating two providers. Include at least one alternative and one stopping condition.

### Exercise 4

Audit a “microservices pattern language” whose nodes are API Gateway, Database per Service, Saga, Circuit Breaker, Kubernetes, and Observability, with every node linked to every other by “related.” Identify structural and evidentiary repairs.

### Exercise 5

Design a small pattern-language fragment for an unfamiliar research-data ingestion system. Include domain scope, two entry points, at least six patterns, typed guarded edges, one branch, one feedback edge, stopping conditions, and an evidence plan.

## Answers to the Exercises

### Answer 1

The alphabetical list is a collection. Consistently formatted GoF entries form a catalog. The intent-classified messaging graph is a pattern system unless its edges guide construction. The four-pattern path is a sequence. The network with contextual entry, typed guarded transitions, alternatives, and stopping conditions is a pattern language candidate; it still needs node, edge, coherence, and independent-use evidence.

### Answer 2

The output is only `entry: Message Channel` then `next: Message Translator`, followed by the stop line, because Translator's sole outgoing guard is false. Dead-Letter Channel becomes unreachable because the toy graph routes poison handling only through Normalizer. Poison messages could exist with one source format, so this is a language-model gap rather than proof the pattern is irrelevant. A stronger graph would permit a guarded poison-message edge from Translator or a common processing context.

### Answer 3

Begin with an owned integration boundary. Adapter is a refinement when each provider interface is incompatible but semantically translatable. Strategy complements it when provider selection varies under a stable local capability: each adapter can fulfill a strategy role. Facade is an alternative or complement when clients need a simpler subsystem-level entry rather than interchangeable providers alone. Anti-Corruption Layer generalizes or contains multiple adapters/translators when foreign concepts threaten the local domain model.

Stop after one Adapter when one provider, one stable local contract, and conformance evidence resolve the problem. Stop after Adapter-plus-Strategy when selection is contained and clients need no subsystem simplification. Do not add Facade or Anti-Corruption Layer merely because the names are related.

### Answer 4

The nodes mix architecture style consequences, data ownership, transaction workflow, resilience, one product/platform, and a broad operational concern. “Related” provides no direction, guard, or context. First state scope and exclusions, replace Kubernetes with technology-neutral deployment or orchestration patterns (keeping Kubernetes as an implementation), and decompose Observability into specific operational problems.

Add entry contexts such as independent deployment need, cross-service transaction, and remote dependency failure. Type edges: Database per Service creates distributed consistency context that may lead to Saga; remote calls may require Deadline before bounded Retry/Circuit Breaker; API Gateway is conditional on external-client routing forces. Add alternatives such as modular monolith, shared database under explicit ownership, direct edge routing, and choreography versus orchestration. Add conflicts, hard constraints, stopping conditions, and feedback from load/failure tests. Evidence must cover each node, each transition, independent project paths, and known negative outcomes—not merely technology adoption.

### Answer 5

Scope the fragment to receiving externally produced research datasets, validating them, preserving provenance, and making accepted data available; exclude analytical modeling. Entry points are “new external source” and “ingestion overload or failure.” Patterns can include Adapter, Canonical Data Model, Message Channel, Message Translator, Bounded Buffer, Quarantine/Dead-Letter Channel, Idempotent Consumer, and Provenance Record.

From a new source, `Adapter --requires format mismatch--> Message Translator`; Translator `--refines many formats--> Canonical Data Model`. Accepted records `--complement asynchronous transfer--> Message Channel`; at-least-once delivery `--requires duplicates possible--> Idempotent Consumer`. From overload, Channel `--follows bounded resources--> Bounded Buffer`, branching to backpressure for lossless submissions or load shedding for explicitly disposable previews. Validation failure leads to Quarantine. Recovery tests revealing duplicate replay feed back to identity and idempotency decisions.

Stop when required sources translate without semantic loss, provenance remains traceable, capacity is bounded, failure disposition is owned, and acceptance/replay contracts pass. Gather evidence through independent source integrations, schema-difference reviews, conformance fixtures, saturation and fault tests, operator exercises, and change-history analysis. Mark untested source classes and retention interactions as language gaps rather than assumed coverage.
