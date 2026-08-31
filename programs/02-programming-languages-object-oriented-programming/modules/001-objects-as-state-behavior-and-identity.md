---
module_id: OOP-001
program: Programming Languages: Object-Oriented Programming
level: 1
module_number: 1
title: Objects as State, Behavior, and Identity
status: complete
last_verified: 2026-08-28
---

# Objects as State, Behavior, and Identity

## One-Page Review

### Governing question

What makes a software object one continuing thing rather than merely a collection of equal-looking data?

### Essential definitions

- An **object** is a computational entity modeled by its identity, state, and behavior.
- **State** is the information associated with the object that can affect future observations.
- **Behavior** is the set of operations or messages the object can accept and the observable results, state transitions, and effects those interactions can produce.
- **Identity** is the criterion by which the object remains the same object across time and state changes, and differs from other objects with equal state.
- A **reference** designates an object. Two references to one object are **aliases**.
- An **object graph** consists of objects as nodes and references as directed edges.
- **Runtime identity** distinguishes live instances in one execution; **domain identity** identifies an entity in a problem domain, often across processes or persistence cycles. They are not automatically the same.

### Central model, mechanism, or theorem

Model a heap as $H:I\rightharpoonup S$, mapping object identities to states, and an environment as $\rho:Name\rightharpoonup I$, mapping names to identities. An operation transition has the form

$$
\langle i,H,m,a\rangle\longrightarrow\langle H',r,t\rangle,
$$

where object (i) receives operation (m) with arguments (a), produces result (r) and observable trace (t), and may replace (H(i)) with a new state while preserving identity (i). If $\rho(x)=\rho(y)=i$, then (x) and (y) alias the same object; an update through either is visible through both.

### Critical invariants

- Equal state does not imply equal identity.
- State change does not by itself change identity.
- Assignment normally copies a reference, not the designated object.
- Rebinding one name does not redirect its other aliases.
- Mutating a shared object can be observed through every alias that can reach it.
- An object's behavior includes failures and effects, not only returned values.
- Domain identity must have an explicit scope and authority; an identifier field alone does not create uniqueness.

### Common failures

Typical failures are treating objects as bags of fields, confusing reference identity with structural equality, saying “passed by reference” when a reference value is copied, assuming a shallow copy duplicates a graph, using mutable objects as keys under unstable equality, leaking invalid intermediate state, and mistaking two in-memory representatives of one database row for one runtime object.

### Compact example

Let `primary` and `alias` refer to one counter whose state is 3, while `peer` refers to another counter also at 3. Then `primary` and `alias` have the same identity; `peer` has equal state but different identity. Incrementing through `alias` makes `primary` observe 4, while `peer` remains 3.

### Connections

The conceptual prerequisite is [PLS-001's separation of programs and observable behavior](../../01-programming-languages-and-semantics/modules/001-programs-languages-and-observable-behavior.md). [OOP-002](../ROADMAP.md) explains how classes construct and classify objects. Object storage connects to [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md), while domain identity connects to [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md).

## Governing Question

When a program changes an object, what persists, what changes, and who can observe the difference?

An object is useful because it provides continuity. A bank account remains the same account as its balance changes. A network connection remains the same connection as it moves from opening to established to closed. A parser can accumulate position while offering operations that interpret the next token. In each case, clients interact with something that has a history and a set of permitted behaviors, not merely a snapshot of fields.

The compact phrase “state, behavior, and identity” prevents three reductions. State without behavior is merely exposed data. Behavior without state can still be object-like, but it does not explain stateful collaboration. State and behavior without identity cannot explain aliasing, lifecycle, or two independent objects that happen to look equal. A rigorous object model states all three and says which observations are public.

## Why This Matters

Object-oriented programs are graphs of collaborating, evolving entities. A local-looking update can affect distant code because both paths reach the same node. A “copy” can duplicate only the outer node and preserve shared inner nodes. A persistence layer can create two runtime objects for one domain entity. A cache can return one long-lived representative or many detached snapshots. These are identity and aliasing decisions before they are framework decisions.

The model also guides design review. Asking only “which fields does this class have?” encourages an anemic record with unrelated procedures elsewhere. Asking “what behavior does this object own, what states can it enter, and how is it identified?” exposes responsibility, lifecycle, and invariant questions. Later chapters treat classes, encapsulation, invariants, equality, and responsibility in depth; this chapter establishes the common ontology.

## Prerequisites and Retrieval

You should understand variables, functions, assignment, records, sequences, simple set notation, and the distinction between a value and a name bound to that value. Retrieve these points:

1. A name is not the object it designates.
2. A mapping can associate several names with one target.
3. A sequence of operations may matter even when initial and final snapshots match.
4. Equality is a relation whose definition depends on the compared domain.
5. A precondition limits admitted calls; a postcondition describes results after an admitted call.

No particular class syntax is assumed. Classes are one object-construction and classification mechanism, not the definition of objecthood.

## Learning Objectives

After completing this module, you should be able to:

- explain an object through state, behavior, and identity without relying on one language's syntax;
- distinguish bindings, references, runtime objects, snapshots, and domain entities;
- draw and update an object graph;
- predict how mutation is observed through aliases;
- distinguish mutation from rebinding and shallow copying from graph duplication;
- write a transition model for an object's operation;
- state an object's valid state space and behavioral obligations;
- diagnose runtime-identity and domain-identity conflicts in production systems.

## Core Exposition

An object's **state** is not necessarily every byte in its representation. It is the information that the chosen model associates with the object and that can affect future observations. For a counter, state might be one integer. For a file handle, it may include open/closed status, current position, access mode, and a connection to operating-system state. Derived caches may be representation state without belonging to the abstract state promised to clients.

An object's **behavior** is more than a list of method names. It includes the conditions under which operations are admitted, their results, permitted state transitions, failures, and externally visible effects. Two objects with methods named `withdraw` need not share behavior if one permits overdrafts and the other rejects them. Signatures describe call shape; behavioral contracts describe meaning.

An object's **identity** answers whether two designations refer to the same continuing entity. Runtime systems commonly supply reference identity: two references are identical if they designate the same allocated object. Domain models may instead use an account number, shipment identifier, or composite key across time and process boundaries. A domain identifier is data inside a runtime representation; the runtime does not automatically enforce its uniqueness or authority.

State, behavior, and identity interact. An operation selects an object by reference, consults its current state, and may produce a successor state for that same identity. Clients usually reason that the object persists through the transition. Creation introduces an identity; retirement makes further operations invalid or redirects them through a lifecycle policy.

An **alias** exists when two access paths reach the same object. In a heap graph, variables and object fields are roots or edges. Mutation changes a node; every path to that node can observe the changed state. Rebinding changes one edge and does not mutate either its old or new target. This is why the phrase “objects are passed by reference” is often too loose: in many languages a function receives a copied reference value. It can mutate the shared target, but assigning a new target to its local parameter does not rebind the caller's name.

A copy operation must state its depth and semantics. A **shallow copy** creates a new outer identity and copies field values, including references to existing nested objects. A **deep copy** attempts to recreate a reachable graph, but must decide how to preserve sharing, cycles, external resources, subclasses, and identities. Serialization often constructs a new graph under a format-specific policy and is not a universal clone.

Objects need not be mutable. An immutable object can have identity, behavior, and stable state; operations return new objects instead of changing it. Conversely, a mutable record is not automatically well-designed object orientation if arbitrary clients modify fields without a coherent behavioral boundary. Object-oriented design is about interaction and ownership of behavior, not maximizing class or mutation counts.

Classes are also not required for every object model. Prototype-based languages derive behavior by delegation among objects. Closures can package private state with functions. Actors combine identity with message handling and isolated state. These mechanisms differ, but each can realize a boundary with state, behavior, and identity.

## Definitions and Notation

Let:

- (I) be a set of runtime object identities;
- (S) be a set of object states;
- $H:I\rightharpoonup S$ be a partial heap mapping live identities to states;
- $\rho:Name\rightharpoonup I$ be an environment mapping names to identities;
- (M) be operation or message names;
- (A) be argument tuples;
- (R) be results;
- (T) be observable traces.

The notation $H[i\mapsto s']$ means a heap equal to (H) except that identity (i) now maps to state (s'). An operation transition is

$$
\langle i,H,m,a\rangle\longrightarrow\langle H[i\mapsto s'],r,t\rangle.
$$

An alias relation for names is

$$
x\sim_\rho y\quad\Longleftrightarrow\quad\rho(x)=\rho(y).
$$

Reference equality compares identities. Structural equality compares selected state recursively or fieldwise. Domain equality compares according to a business relation. These relations can disagree and must not share one unexplained word “same.”

For an invariant predicate $Inv:S\to\{true,false\}$, an operation's basic preservation obligation is

$$
Inv(s)\land Pre_m(s,a)\land Step_m(s,a,s',r,t)\Longrightarrow Inv(s').
$$

Module 005 develops invariants fully. Here the formula clarifies that behavior constrains state transitions rather than merely exposing setters.

## Mechanisms, Invariants, or Proof Structure

**Identity preservation.** If an admitted operation changes (H(i)=s) to (H'(i)=s'), the identity remains (i). Allocating a replacement (j) with equal state is not the same transition when reference identity is observable.

**Alias visibility.** Suppose $\rho(x)=\rho(y)=i$ and an operation through (x) changes (H(i)=s) to (H'(i)=s'). Looking up either name after the transition reaches (i), so both observe $H'(\rho(x))=H'(\rho(y))=s'$. This is a direct substitution proof. It assumes both observations occur after the same heap update and no intervening transition.

**Distinct-equal independence.** Suppose $i\ne j$ but (H(i)=H(j)=s). Updating (i) yields $H'=H[i\mapsto s']$. Because $j\ne i$, functional update gives (H'(j)=H(j)=s). Equal initial state therefore does not couple distinct identities.

**Rebinding isolation.** If only $\rho$ changes to $\rho[x\mapsto j]$, the heap is unchanged and any other name $y\ne x$ retains its old mapping. Rebinding a parameter is therefore different from mutating its target.

**Invariant locality with shared references.** An object can control transitions issued through its behavior, but it cannot preserve an invariant if mutable representation escapes and can be changed around that behavior. Encapsulation and ownership mechanisms determine whether the preservation proof's assumptions hold.

**Domain-identity coherence.** If two live objects claim one domain identifier, the application must define whether they are independent snapshots, synchronized representatives, or an error. A map from domain ID to one canonical live object is an identity-map policy, not a universal property of object orientation.

## Alternatives and Trade-Offs

**Reference objects versus values.** Reference objects make continuity and shared mutation explicit. Values make substitution and independent reasoning easier. Many systems use identity-bearing entities at boundaries and immutable values for measurements, money, dates, and configuration. Module 007 develops this distinction.

**Mutable versus immutable state.** In-place mutation can express one owner evolving efficiently. Immutable transitions retain prior versions and reduce alias interference, but introduce new identities and possible allocation costs. The right question is which histories and authorities must be observable.

**Behavior-rich objects versus data records.** Behavior-rich objects keep state transitions near the state they govern. Plain records are effective for serialization, interchange, and transparent transformations. Converting every record into a class adds ceremony; exposing every domain entity as a record disperses rules.

**Runtime identity versus domain identity.** Runtime identity is precise within one process lifetime. Domain identity survives reconstruction and distribution but needs uniqueness, lifecycle, and reconciliation policies. Treating a database key as if it were a memory reference creates stale-object and duplicate-representative bugs.

**Shallow sharing versus deep copying.** Structural sharing can be efficient and intentional when shared nodes are immutable or jointly owned. Deep copying reduces some interference but can destroy meaningful identity, duplicate resources, and mishandle cycles. Copy policy belongs to the object graph's contract.

**Class-based versus prototype, closure, or actor objects.** Classes centralize construction and classification. Prototypes emphasize delegation, closures emphasize lexical privacy, and actors emphasize isolated message processing. Each makes different operations and costs visible; none changes the need to state identity, state, and behavior.

## Failure Modes and Misconceptions

1. **An object is a row of fields.** Fields are one representation; behavior and identity determine how the entity participates in a program.
2. **Equal fields mean the same object.** Two independent counters may both contain 3.
3. **Identity means an `id` property.** Runtime identity can differ despite equal identifier fields, and duplicate fields can violate a domain policy.
4. **Assignment clones an object.** It commonly copies a reference and creates an alias.
5. **Reassigning a parameter changes the caller's binding.** It usually redirects only the local name when references are passed as values.
6. **A shallow copy isolates nested mutation.** Copied reference fields still lead to shared nested objects.
7. **Immutable means identity-free.** An immutable object can be reference-distinct from an equal immutable object.
8. **Classes are required for objects.** Prototype, closure, actor, and other object models exist.
9. **Private state guarantees valid behavior.** Private representation helps control access, but methods can still implement invalid transitions.
10. **One domain entity always has one runtime object.** Persistence, caching, messaging, and process boundaries routinely create multiple representatives.

## Worked Examples

### Example 1

**Question:** Can two objects have equal state and different identity?

**Reasoning:** Create two counters independently with state 3. A structural comparison of their snapshots can return equal, while reference comparison returns false. Updating the first must not update the second because they occupy distinct heap identities.

**Conclusion:** State equality is compatible with identity inequality.

### Example 2

**Question:** What changes when an alias invokes behavior?

**Reasoning:** This executable example creates one alias and one distinct equal-state object. The class syntax is only a host-language vehicle; construction mechanisms are studied in OOP-002.

<!-- bijux-verify: {"id":"state-behavior-identity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"primary is alias: True\nprimary is peer: False\ninitial states: 3 3\nafter alias increment: 4 3\n","stderr":""}} -->
```python
class Counter:
    def __init__(self, value):
        self._value = value

    def increment(self):
        self._value += 1

    def read(self):
        return self._value


primary = Counter(3)
alias = primary
peer = Counter(3)

print("primary is alias:", primary is alias)
print("primary is peer:", primary is peer)
print("initial states:", primary.read(), peer.read())
alias.increment()
print("after alias increment:", primary.read(), peer.read())
```

**Conclusion:** Behavior invoked through an alias changes the shared object; an equal-state peer remains independent.

### Example 3

**Question:** Does assigning a new object to a parameter replace the caller's object?

**Reasoning:** Let caller name (c) and parameter (p) initially contain the same identity (i). Reassigning (p) to new identity (j) changes only $\rho(p)$. The mapping $\rho(c)=i$ and heap object (H(i)) remain. Mutating (H(i)) through (p) before rebinding would instead be visible through (c).

**Conclusion:** Copying a reference into a parameter permits shared-target mutation but not remote rebinding of the caller's name.

### Example 4

**Question:** A document changes from `draft` to `approved`. Is it now a different document?

**Reasoning:** Under a domain model with stable document ID `D7`, approval is a state transition of entity `D7`. A new runtime snapshot may represent the successor state, so runtime identity can change while domain identity persists. If approval creates a legally new revision, the domain may instead assign revision identity `D7-R2` while retaining a lineage relation.

**Conclusion:** Identity across change is a model decision; runtime allocation and domain continuity answer different questions.

### Example 5

**Question:** What does a shallow copy of an order isolate?

**Reasoning:** Suppose order (o_1) refers to address object (a). A shallow copy creates order (o_2) and copies the reference to (a). Changing an outer scalar field of (o_2) leaves (o_1) unchanged, but mutating (a) is visible from both. Copying the address too creates a new node but may still share deeper country or contact objects.

**Conclusion:** “Copy” is incomplete without a graph-depth, sharing, and identity policy.

### Example 6

**Question:** Can an object exist without a class declaration?

**Reasoning:** A closure can retain private counter state and return operations `increment` and `read`; callers interact with one continuing captured cell. A prototype object can delegate behavior to another object. An actor can retain isolated state behind a mailbox identity. These have state, behavior, and identity under their respective language models.

**Conclusion:** Classes are an important mechanism for objects, not a necessary definition of them.

### Example 7

**Question:** Does immutability eliminate identity?

**Reasoning:** Two separately allocated immutable coordinate objects can both represent ((2,5)) while reference comparison distinguishes them. If the program treats coordinates purely as values, structural equality is the useful relation and allocation identity should remain unobserved. If one coordinate is a canonical interned object, reference identity may be an optimization but should not silently become the domain contract.

**Conclusion:** Immutability removes state transitions from an instance; it does not logically force reference identity to disappear.

### Example 8

**Question:** Why can changing one collaborator affect several owners?

**Reasoning:** An invoice and a shipment both reference customer object (c). If code changes (c.address) in place, both access paths observe the new address. That may be intended shared truth or an error if each needed a historical snapshot. Drawing the graph exposes the decision: one shared node versus two copied address values.

**Conclusion:** Shared collaborators create semantic coupling; graph shape must match ownership and history requirements.

### Example 9

**Question:** A persistence query loads the same customer twice. Is there one object or two?

**Reasoning:** Without an identity map, each query can construct a distinct runtime object with domain ID `C42`. Mutating one leaves the other stale. With an identity map scoped to a unit of work, both queries return aliases to one representative. Across processes there will still be distinct runtime identities, so versioning or concurrency control must reconcile changes.

**Conclusion:** One domain identity can have several runtime representatives; canonicalization is a scoped repository policy.

### Example 10

**Question:** How should a reservation object handle `confirm` after `cancel`?

**Reasoning:** State alone lists `pending`, `confirmed`, and `cancelled`; behavior defines admitted transitions. A reasonable protocol permits `confirm` and `cancel` from `pending`, perhaps `cancel` from `confirmed`, and rejects `confirm` from `cancelled`. Returning a fresh record with an arbitrary status field would not enforce this history. The same reservation identity persists through admitted transitions until lifecycle policy retires it.

**Conclusion:** Object behavior gives state temporal meaning by owning which transitions are permitted.

## Cross-Program Connections

- **Programming Languages & Semantics:** heap, environment, transition, and observation models give object behavior precise meaning.
- **Functional Programming:** immutable values and persistent data structures offer alternatives to shared mutable identity.
- **Concurrent & Parallel Programming:** aliases across threads turn local object invariants into synchronization obligations.
- **Domain Modeling & Domain-Driven Design:** entity identity and value equality express domain continuity rather than allocation details.
- **Database Engineering:** identity maps, object-relational mapping, snapshots, and optimistic versions reconcile stored and live identity.
- **Distributed Systems:** one logical entity has replicas and messages rather than one globally shared runtime reference.
- **Security Engineering:** possessing an object reference can convey authority; leaked aliases can therefore leak capabilities.
- **Testing & Quality Engineering:** tests must choose between state snapshots, behavior observations, and reference-identity assertions.

## References

- Martín Abadi and Luca Cardelli. [*A Theory of Objects*](https://link.springer.com/book/10.1007/978-1-4419-8598-9). Springer, 1996, DOI 10.1007/978-1-4419-8598-9. Publisher record checked 2026-08-28.
- Alan C. Kay. [“The Early History of Smalltalk.”](https://doi.org/10.1145/155360.155364) *ACM SIGPLAN Notices* 28(3), 1993, pp. 69–95, DOI 10.1145/155360.155364. ACM record checked 2026-08-28.
- William R. Cook. [“On Understanding Data Abstraction, Revisited.”](https://www.cs.utexas.edu/~wcook/Drafts/2009/DataAbstractionRevisited.pdf) *OOPSLA 2009*, pp. 557–572, DOI 10.1145/1640089.1640133. Author-hosted paper checked 2026-08-28.
- Grady Booch, Robert Maksimchuk, Michael Engle, Jim Conallen, Kelli Houston, and Bobbi Young. [*Object-Oriented Analysis and Design with Applications*, 3rd ed.](https://www.pearson.com/en-us/subject-catalog/p/object-oriented-analysis-and-design-with-applications/P200000000143/9780201895513). Addison-Wesley Professional, 2007, ISBN 9780201895513. Publisher record checked 2026-08-28.
- Peter Wegner. [“Dimensions of Object-Based Language Design.”](https://doi.org/10.1145/38765.38823) *OOPSLA 1987*, pp. 168–182, DOI 10.1145/38765.38823. ACM DOI metadata checked 2026-08-28.

## Exercises

### Exercise 1

Define state, behavior, and identity for each of these objects: a counter, an open file handle, and an immutable postal address. State one detail that belongs to representation rather than abstract state in each case.

### Exercise 2

Let $\rho(a)=i$, $\rho(b)=i$, and $\rho(c)=j$, where $i\ne j$, and initially (H(i)=H(j)=5). Trace these steps: increment through (b); rebind (b) to (j); increment through (b). Give the final mappings and heap values after each step.

### Exercise 3

Draw an object graph for two project objects that share one mutable owner object, where the owner refers to one address. Describe a shallow copy of the first project. Then design an update that changes only the copied project's owner address without affecting either original project, naming every node that must receive a new identity.

### Exercise 4

Compare a mutable `TemperatureSensor` object with an immutable `TemperatureReading` value. Define useful identity and equality relations, allowed state changes, and behavior for each. Explain why forcing both into the same object policy would be misleading.

### Exercise 5

A service processes account `A17` in two worker processes. Each worker has a different runtime object loaded at version 8. Both attempt an update, producing versions 9 with different balances. Diagnose why reference identity cannot solve the conflict. Specify the domain identity, state/version rule, behavior required of persistence, and the observable result for the losing update.

## Answers to the Exercises

### Answer 1

For a counter, abstract state is its integer count, behavior includes read and admitted increment/decrement operations, and identity distinguishes independent counters with equal counts; a cached formatted string is representation state. For an open file handle, state includes open/closed status, access mode, and logical position, behavior includes read, write, seek, and close under their preconditions, and identity ties operations to one live resource; an operating-system table index is representation. For an immutable postal address, state is the normalized address components, behavior can format or validate without changing the instance, and identity may be treated as unobservable in favor of structural value equality; object header or allocation address is representation.

### Answer 2

Initially both (a) and (b) designate (i), while (c) designates (j); both heap states are 5. Incrementing through (b) updates (H(i)) to 6, so (a) and (b) both observe 6 while (c) observes 5. Rebinding (b) to (j) changes the environment to $\rho(a)=i$ and $\rho(b)=\rho(c)=j$; the heap remains (H(i)=6,H(j)=5). Incrementing through the rebound (b) updates (H(j)) to 6. Finally all three names observe the numeric state 6, but (a) still designates (i), whereas (b) and (c) designate (j). Equal final state does not merge identities.

### Answer 3

The initial graph has project nodes (p_1) and (p_2), both pointing to owner (o), which points to address (d). A shallow copy creates project (p_3) but copies its owner edge to (o), so no owner or address isolation exists. To change only the copied project's address, create a new address (d'), a new owner (o') equal to (o) except for its edge to (d'), and redirect only (p_3)'s owner edge to (o'). Nodes (p_1), (p_2), (o), and (d) remain unchanged. Copying only (d) would still require a way to redirect an owner edge without mutating shared (o), which is why the entire changed path needs new identities.

### Answer 4

`TemperatureSensor` has runtime and perhaps hardware domain identity, mutable calibration/connection state, and behavior such as sample, calibrate, and disconnect. Two sensors returning 20°C are not thereby equal. `TemperatureReading` contains value, unit, timestamp, and perhaps sensor domain ID; it is immutable and usefully compared structurally under a declared normalization policy. Sampling creates a new reading rather than mutating an old one. Giving readings identity-based equality would hinder comparison and caching; giving sensors structural equality would collapse independent devices and lifecycles.

### Answer 5

The workers cannot compare or share reference identity across processes; their objects are distinct representatives. Domain identity is account ID `A17`. State includes balance and persisted version. Persistence behavior should condition an update on expected version 8 and atomically advance the stored version to 9. The first accepted update wins; the second finds that the current version is 9 and returns a version-conflict outcome without overwriting it. The losing worker must reload and deliberately retry or surface the conflict. This optimistic-concurrency rule reconciles domain identity and state history without pretending there is one global runtime object.
