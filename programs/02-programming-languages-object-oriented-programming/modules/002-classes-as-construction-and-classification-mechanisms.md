---
module_id: OOP-002
program: Programming Languages: Object-Oriented Programming
level: 1
module_number: 2
title: Classes as Construction and Classification Mechanisms
status: complete
last_verified: 2026-08-29
---

# Classes as Construction and Classification Mechanisms

## One-Page Review

### Governing question

What does a class contribute when it creates objects, groups them for language and tooling rules, and owns behavior shared by a family of instances?

### Essential definitions

- A **class** is a language-defined description or runtime entity that commonly coordinates instance construction, classification, instance-side features, and class-side features. Languages combine these roles differently.
- An **instance** of a class is an object classified by that class according to the language's nominal, runtime, or prototype-based rules.
- **Construction** is the protocol that allocates or obtains an identity, establishes class association and representation, initializes state, and returns or rejects the candidate object.
- **Direct class** means the class most specifically associated with an object at creation or runtime. Inherited membership can additionally classify that object under ancestor classes.
- A **class invariant** is a property intended to hold for every externally usable instance of the class; merely placing fields in a class does not establish it.
- An **instance member** is interpreted relative to an instance, whereas a **class-side** or **static member** belongs to the class-level namespace or runtime class object.
- A **nominal classification** follows declared names and relationships. A **structural classification** follows available operations or shape. They need not agree.
- An **abstract class** can classify instances of concrete descendants and share implementation while prohibiting direct construction.
- A **class object** is a runtime object representing a class in reflective systems. Not every language makes classes ordinary values, and class-object identity is not instance identity.
- A **type** constrains or describes values and operations. A class declaration often introduces a type, but class, type, constructor, and runtime classifier are not universally identical.

### Central model, mechanism, or theorem

Let $C$ be classes, $I$ object identities, and $H$ a heap. Let $direct:I\rightharpoonup C$ record each live object's direct class, and let $\preceq$ be the reflexive-transitive declared classification relation where $c_1\preceq c_2$ means that instances directly classified by $c_1$ are also classified by $c_2$. Then

$$
i\models c
\quad\Longleftrightarrow\quad
direct(i)\preceq c.
$$

A successful construction step has the abstract form

$$
construct(c,a,H)\Downarrow(i,H')
$$

with freshness $i\notin dom(H)$, direct classification $direct(i)=c$, initialized representation in $H'$, and every promised post-construction invariant established before $i$ becomes externally usable. Classification does not prove those obligations were implemented correctly.

### Critical invariants

Each successful ordinary construction returns a distinct live identity unless interning, pooling, or singleton policy explicitly says otherwise. Direct class and inherited membership are distinguished. Class-side mutable state is not copied into each instance. Declared type, runtime class, and implementation representation are never silently conflated. Abstract or otherwise non-constructible classes reject direct construction. Class membership never substitutes for validation of object state, behavior, provenance, authority, certification, or fitness for high-consequence use.

### Common failures

Common failures are calling a class only a record template; assuming every type is a class; assuming every class is directly constructible; confusing a class value with an instance; storing per-instance mutable data in class-side state; treating a subclass name as proof of behavior; testing exact class when inherited membership is intended; using inherited membership when only exact representations are safe; trusting `instanceof` across mutable prototypes, realms, reloads, or class loaders; and publishing a partially initialized object.

### Compact example

Two calls to `Reading(20)` and `Reading(21)` normally produce distinct identities with the same direct class. Both can find shared unit metadata through the class, but each owns its reading value. `type(first) is Reading` asks exact runtime-class identity in Python; `isinstance(first, Reading)` asks membership including recognized subclasses. Neither proposition proves the measurement is calibrated.

### Connections

[OOP-001](001-objects-as-state-behavior-and-identity.md) supplies object identity, state, and behavior. [OOP-003 and later Block 01 modules](../ROADMAP.md) develop messages, dispatch, encapsulation, invariants, and initialization. Class types depend on [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md); domain categories belong to [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md).

## Governing Question

When a declaration says `class Reading`, which guarantees come from the language's class mechanism, which obligations remain with the author, and which classifications are merely convenient descriptions?

The word “class” suggests a set: the class of all readings. In programming languages it also suggests a construction mechanism, a namespace of methods and fields, a nominal type, a runtime descriptor, an inheritance node, and sometimes an ordinary callable object. These roles reinforce one another in familiar languages, so introductory explanations often collapse them. That shortcut fails as soon as an abstract class has instances but cannot be directly constructed, a Python class is replaced by another class object with the same name, a Java class is loaded by two class loaders, or JavaScript's prototype relation changes after construction.

A disciplined account therefore starts with four separate questions. What objects can this mechanism produce? By what rule is an existing object classified? Which features belong to each instance and which belong to the class-level entity? Which claims are checked statically, checked dynamically, or left as programmer obligations? A language's specification—not the spelling `class`—answers them.

## Why This Matters

Classes sit at a boundary between source declarations and runtime populations. One class body may describe storage for millions of objects, code shared by all of them, rules for producing each one, a name accepted by a static checker, metadata used by frameworks, and a runtime token used for reflection. A bug in understanding the boundary can spread widely: one mutable class field becomes shared accidental state; one constructor leak exposes invalid objects; one exact-class check rejects legitimate descendants; one permissive membership check accepts an object whose behavior is incompatible.

The distinction also matters when choosing an abstraction. A class is valuable when a coherent population of identity-bearing objects shares representation rules and behavior. It is less useful when data is a transparent immutable product, when behavior varies independently along several dimensions, when construction needs no persistent classification, or when a capability should expose only one narrow operation. “Make it a class” is not a neutral translation of a noun.

Frameworks amplify classification assumptions. Dependency containers register constructor values. Serializers record class tags. ORMs map rows to classes. Plugin systems discover subclasses. Authorization code may test a class or interface. These mechanisms can be appropriate, but class membership is evidence only of the language relation that established it. It does not establish database freshness, plugin trust, legal authorization, calibration, protocol compatibility, or semantic substitutability.

Current languages make different choices. Java class declarations introduce nominal class types and runtime classes, while interfaces and arrays demonstrate that not every type is an ordinary class. Python executes a class definition to create a class object, and calling that object normally initiates instance creation. ECMAScript class syntax creates a constructor and prototype relationship within a prototype-based object model. ECMA-335 describes classes as types in an inheritance hierarchy and uses an explicit object-creation instruction. The shared vocabulary is useful only when these differences remain visible.

## Prerequisites and Retrieval

Retrieve OOP-001's separation of object identity, state, behavior, reference, and domain identity. Be comfortable with sets, partial functions, relations, graph reachability, namespaces, functions, records, and the difference between a static claim and a runtime check.

Recall that a declaration can introduce several things at once. A function declaration can introduce a name, a callable value, a parameter contract, and executable code without making these one concept. A class declaration likewise can introduce a source-level name, a type-level classifier, construction code, shared members, and a runtime representative. Also retrieve the distinction between necessary and sufficient evidence: passing a runtime membership test can be necessary for an operation while remaining insufficient to establish behavioral or domain safety.

No knowledge of inheritance design, dynamic dispatch internals, metaclasses, or advanced constructors is assumed. This module names those boundaries; OOP-003, OOP-006, OOP-012 through OOP-016, OOP-051 through OOP-060, and OOP-081 through OOP-084 own the deeper mechanisms.

## Learning Objectives

By the end of this module, you should be able to:

1. separate a class's construction, classification, instance-side, and class-side roles;
2. model direct class and inherited class membership without confusing them with object identity;
3. distinguish a class declaration, class name, class value, constructor, class type, and instance;
4. explain why class and type coincide in some contexts but not universally;
5. trace a successful construction from arguments and heap to a fresh classified instance;
6. identify abstract, inaccessible, factory-controlled, pooled, and prototype-based exceptions to a naive “class call creates a new object” rule;
7. diagnose accidental sharing through class-side mutable state;
8. select exact-class, inherited-membership, structural, or behavioral checks according to the consumer's real requirement; and
9. reject claims that class names, subclass declarations, or runtime tags prove high-stakes fitness.

## Core Exposition

A class begins as a **classifier**: it identifies a family of instances according to a language-defined rule. In a simple nominal model, an object records one direct class, and declared inheritance extends membership to ancestor classes. If `SavingsAccount` extends `Account`, a savings object can be a direct instance of `SavingsAccount` and an inherited instance of `Account`. The two statements answer different questions, so APIs should say whether they require exact representation or membership in an admitted family.

Classification does not mean enumerating all objects in advance. Most classes describe an open population whose instances appear and disappear during execution. The class gives a predicate or relation for membership, not a stored set that must literally contain every object. Reflection may enumerate some loaded classes or live objects in a managed environment, but that operational capability is separate from the semantic definition.

A class is also commonly a **construction mechanism**. A creation expression selects a class or constructor, supplies arguments, allocates or obtains storage, associates the result with runtime class information, initializes instance state, and returns a reference. Different languages divide this pipeline differently. Java distinguishes class-instance creation expressions from constructor declarations. Python class calls are mediated by the class's metaclass and ordinary `__new__`/`__init__` conventions. ECMAScript constructor functions create objects whose prototypes derive from a constructor's `prototype` property. This chapter needs only the abstract pipeline; OOP-006 studies constructor and factory design.

Freshness is an important default but not a universal law. Ordinary creation usually returns a new identity. A class may deliberately intern immutable values, return a cached instance, coordinate a pool, or expose only named instances. Python's object-construction hooks can even return an existing or differently classified object. A precise API therefore promises freshness only when clients may rely on it. If identity is unobservable and values are immutable, an implementation may safely share representatives.

Construction and classification can separate. An abstract Java class contributes a class type, implementation, and classifier for concrete descendant instances but rejects direct `new`. A class with inaccessible constructors may require static factories. A deserializer may allocate without the normal public path under narrowly specified runtime rules. A prototype-based object can be classified by delegation even though no class declaration constructed it. Conversely, a factory function can construct records that share no nominal class beyond a built-in representation.

The **instance side** describes features interpreted relative to one receiver: instance fields, properties, and methods. Each instance normally has its own instance storage, though some representations compute or share internal data. The **class side** holds features associated with the class-level entity: Java static fields and methods, Python class attributes and class methods, or ECMAScript static elements. Class-side code lacks an ordinary current instance unless one is supplied explicitly.

This split prevents a common storage error. If every cart needs its own mutable list, that list belongs to instance state and must be created per cart. A single mutable class-side list makes all carts observe one collection. Shared immutable metadata such as a unit symbol may fit the class side; shared mutable registries, counters, caches, or connection pools need an explicit lifecycle, synchronization, test-isolation, and authority policy.

A **class declaration** is source syntax. A **class name** is a binding or type name introduced by that declaration. A **class value** is the runtime representative in languages where classes are values. A **constructor** is a creation operation or callable participating in initialization. A **class type** is a static or semantic set of admitted references and operations. An **instance** is one object classified by the class relation. One spelling may denote different items in different syntactic contexts, but reviewers should preserve the distinction.

Java illustrates nominal coupling without complete identity. Declaring `class Account` introduces a class and a class type; `new Account()` selects a constructor and produces a class instance. Yet an interface type is not a class type, an array is an object without an ordinary user class declaration, and generic source types may erase to one runtime class. A variable's declared type can be `Account` while the referred object's runtime class is `SavingsAccount`. The static type controls which operations are admitted at the expression; the runtime class participates in later dispatch and reflection.

Python makes the runtime class value especially visible. Executing a class definition creates a namespace, asks the metaclass to create a class object, and binds that object to the class name. Rebinding the name does not alter existing instances' class association. Two executions of text spelling the same class name can produce distinct class objects. `type(x) is C` asks exact class-object identity, while `isinstance(x, C)` normally admits recognized subclass relationships and can be customized by abstract base class machinery.

ECMAScript exposes another separation. Its class syntax creates a constructor function and a prototype object connected to created instances. Ordinary `instanceof` examines a constructor-defined membership algorithm, usually whether the constructor's `prototype` occurs on the object's prototype chain. The prototype property and chains are mutable, constructors from different realms are distinct, and custom `Symbol.hasInstance` can redefine the test. Therefore `x instanceof C` is a language operation, not timeless proof of provenance or behavior.

Classification may be **nominal**, **structural**, or **behavioral**. Nominal classification trusts declared identities and relations: this class says it extends that class. Structural classification asks whether a value has a required shape or operations. Behavioral conformance asks whether those operations satisfy semantic obligations across allowed states and histories. A nominal relation can be efficiently checked and tool-friendly while still admitting a badly implemented subclass. Structural agreement can support flexible composition while overlooking state laws. Behavioral evidence is the strongest goal and the hardest to automate.

Class membership and domain category also differ. A `Customer` class is a program construct. “Customer” in the business may include roles, lifecycle, legal standing, effective dates, jurisdiction, and data authority that one runtime tag cannot settle. An object can be an instance of program class `Customer` while representing stale, unauthorized, or fabricated data. Conversely, a domain customer can have several runtime representations in different services and languages.

Classes organize shared behavior, but this chapter does not reduce methods to stored functions. In class-based runtimes, method code is commonly shared while receiver-specific state is supplied during invocation. Lookup, binding, overriding, virtual tables, inline caches, and multiple dispatch belong to later modules. The present invariant is simpler: declaring behavior once does not create one shared instance state, and sharing code does not make all instances identical.

The executable example below demonstrates a deliberately small Python class. It verifies distinct construction, exact and inherited classification, shared immutable class metadata, a class-side population counter, and independent instance values.

<!-- bijux-verify: {"id":"class-construction-classification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"same_runtime_class=True\ndistinct_instances=True\nclassifies_first=True\nshared_unit=C\ncreated=2\nvalues=20,21\n","stderr":""}} -->
```python
class Reading:
    unit = "C"
    created = 0

    def __init__(self, value):
        self.value = value
        Reading.created += 1


first = Reading(20)
second = Reading(21)

print(f"same_runtime_class={type(first) is type(second)}")
print(f"distinct_instances={first is not second}")
print(f"classifies_first={isinstance(first, Reading)}")
print(f"shared_unit={first.unit}")
print(f"created={Reading.created}")
print(f"values={first.value},{second.value}")
```

Execution establishes only those six observations under the recorded Python toolchain. It does not prove universal class semantics, constructor safety, invariant preservation, thread safety of the counter, subclass behavior, calibration, measurement validity, security, persistence identity, or production fitness.

Good class design starts by stating the population and evidence. What does direct membership mean? Can clients extend the population? Is construction public, restricted, abstract, cached, or fallible? Which state belongs to one instance? Which data is truly shared? What behaviors must every admitted instance preserve? Which checks occur statically, dynamically, through tests, or through human assurance? Only after these questions should syntax be selected.

Class evolution requires care. Adding a required construction argument can break clients. Adding mutable class-side state can introduce order dependence. Moving a field from instance to class side changes sharing. Changing class loaders, plugin reload rules, serialization tags, module boundaries, or prototype links can change runtime classification. Renaming a class can break persisted or reflected names even when behavior remains. A class is therefore both a code abstraction and, when exposed, a compatibility surface.

## Definitions and Notation

Let $C$ be classes, $I$ identities, $S$ instance states, and $H:I\rightharpoonup S$ the live heap. The partial function $direct:I\rightharpoonup C$ assigns a direct class to modeled class instances. Let $\preceq\subseteq C\times C$ be a reflexive-transitive classification relation; $c_1\preceq c_2$ means direct instances of $c_1$ are admitted as instances of $c_2$.

Define exact and inherited instance sets:

$$
Exact(c)=\{i\in dom(H)\mid direct(i)=c\},
$$

$$
Instances(c)=\{i\in dom(H)\mid direct(i)\preceq c\}.
$$

Thus $Exact(c)\subseteq Instances(c)$. Equality need not hold when $c$ has descendants. The relation models nominal inherited membership only; structural protocols and customized runtime tests require different predicates.

Let $F_i(c)$ and $M_i(c)$ describe instance-side fields and operations, and $F_c(c)$ and $M_c(c)$ class-side fields and operations. The subscripts indicate ownership, not memory layout. A construction judgment

$$
\langle c,a,H\rangle\Downarrow\langle i,H'\rangle
$$

is successful when the class is constructible for arguments $a$, $i\notin dom(H)$ under a freshness-promising policy, $direct(i)=c$, $H'$ extends the heap with initialized state for $i$, and the promised post-construction predicate $Ready_c(H'(i))$ holds. A failing construction returns an explicit language-defined failure and must not publish an externally usable invalid $i$.

A static typing judgment $\Gamma\vdash e:T$ describes the compile-time type assigned to expression $e$. A runtime classification judgment $eval(e,H)\Downarrow i\land i\models c$ describes an evaluated object's membership. Neither judgment alone proves a behavioral contract $B_c$; that requires implementation reasoning and evidence over admitted interactions.

## Mechanisms, Invariants, or Proof Structure

**Direct versus inherited classification.** From $direct(i)=Savings$, reflexivity gives $i\models Savings$. If $Savings\preceq Account$, transitivity gives $i\models Account$. The reverse does not follow: an `Account` instance need not be a `Savings` instance. Exact-class and inherited-membership checks therefore answer different questions.

**Fresh construction.** Under an ordinary freshness contract, two successful constructions from the same heap occur sequentially:

$$
construct(c,a,H)\Downarrow(i,H_1),\qquad
construct(c,b,H_1)\Downarrow(j,H_2).
$$

Because $i\in dom(H_1)$ and the second result must be fresh relative to $H_1$, $j\ne i$. Equal arguments or equal state do not merge identity. This proof does not apply to an explicitly interning or cached construction policy.

**Instance-state independence.** If $i\ne j$, each has its own instance field location under the abstract heap. Updating $H(i)$ leaves $H(j)$ unchanged by functional update. A shared reference inside both states can still alias another object, so “separate instances” does not prove deep isolation.

**Class-side sharing.** A class-side location belongs to $c$, not to each $i\in Instances(c)$. Mutating it can affect observations through every instance or class access path. Therefore mutable class state requires synchronization and ownership reasoning; construction count in the executable example is evidence of shared access, not a recommended global metric architecture.

**Constructibility is separate from membership.** An abstract class $a$ may have $Instances(a)\ne\varnothing$ because concrete $d\preceq a$, while direct construction of $a$ is prohibited. Consequently, “has instances” does not imply “can create a direct instance.”

**Type/class separation.** If $\Gamma\vdash x:Account$ and runtime evaluation yields $direct(i)=Savings$, both claims can be true. Static admissibility is governed by `Account`; exact runtime classification is `Savings`; inherited membership includes both. Parameterization, erasure, interfaces, structural protocols, and unions create further separations.

**No behavioral proof from a label.** The implication $i\models c\Rightarrow B_c(i)$ holds only if the language or verified program establishes that every admitted direct class preserves $B_c$. Ordinary class declarations do not automatically verify arbitrary semantic predicates. A misleading class name or defective subclass is a counterexample.

**No publication before readiness.** If a reference to $i$ escapes while $Ready_c(H(i))$ is false, another observer can invoke behavior against partial state. The construction proof then cannot assume the class invariant. Avoid callbacks, global registration, thread publication, or overridable external behavior before readiness; OOP-005 and OOP-006 develop the complete discipline.

## Alternatives and Trade-Offs

**Class versus factory function.** A class can unify nominal membership, shared behavior, and construction. A factory function can choose among representations, return cached values, or hide concrete classes. The factory adds indirection but prevents clients from equating one public name with one concrete class.

**Class versus record or value type.** A transparent record makes fields and structural transformation explicit. A class supports identity, behavior ownership, and controlled representation. Wrapping every immutable data product in an identity-oriented class adds ceremony; exposing every invariant-bearing entity as a writable record disperses authority.

**Nominal versus structural classification.** Nominal relations are explicit, efficient, and stable under accidental shape matches. Structural protocols admit independently developed implementations and reduce hierarchy coupling. Nominal membership can accept a semantically wrong descendant; structural conformance can accept coincidental shape. Behavioral tests and contracts remain necessary in either case.

**Exact-class versus inherited-membership checks.** Exact checks are appropriate for representation-specific serializers, native layouts, or security boundaries whose proof covers one exact implementation. They block extension. Inherited checks permit intended polymorphism but rely on every admitted descendant satisfying the required behavior. Prefer asking for the smallest explicit interface when exact representation is irrelevant.

**Public versus restricted construction.** Public construction is direct and discoverable. Restricted constructors plus named factories can express parsing, caching, variants, or failure, but may hide allocation and effects. Abstract classes deliberately separate classification from direct construction. The API should state identity, failure, and side-effect policy.

**Class-side state versus injected owner.** Static metadata is convenient and naturally shared. Mutable static state couples tests, tenants, threads, and application instances. An injected registry or context has explicit identity and lifecycle at the cost of plumbing. Use class-side mutation only when global scope is actually the domain scope.

**Class hierarchy versus prototypes or composition.** Hierarchies combine classification and inherited implementation. Prototype delegation permits per-object evolution. Composition assembles behavior without declaring an “is-a” population. The expected change pattern, not syntactic familiarity, should select the mechanism.

## Failure Modes and Misconceptions

- **“A class is a blueprint that gets copied.”** Method code and class-side state are usually shared, while instance storage and runtime metadata follow language-specific mechanisms.
- **“Every construction returns a fresh object.”** Interning, caching, pooling, named instances, and customized construction can return existing identities.
- **“Every class can be instantiated.”** Abstract classes and classes with inaccessible or failing construction paths intentionally cannot.
- **“Class and type are synonyms.”** Interfaces, arrays, unions, structural protocols, generic instantiations, erased runtime classes, and class objects separate them.
- **“The declared type is the runtime class.”** A variable typed as an ancestor or interface may refer to a descendant instance.
- **“A static field exists once per object.”** It belongs to the class-level entity or loading context and is shared within that scope.
- **“A subclass declaration proves substitutability.”** Nominal inheritance does not mechanically verify preconditions, effects, invariants, or histories.
- **“An exact-class check is safer.”** It may reject supported variants and create brittle central registries; safety depends on the actual representation or behavior requirement.
- **“`instanceof` proves provenance.”** Loader identity, realm boundaries, prototype mutation, customization, deserialization, and hostile objects limit that inference.
- **“A class name proves a domain fact.”** `CertifiedDevice`, `Administrator`, or `ValidatedOrder` are identifiers, not evidence of certification, authority, or validation.
- **“Separate instances have separate graphs.”** Their fields may still alias shared collaborators or mutable class-side objects.
- **“The constructor owns every creation path.”** Reflection, deserialization, cloning, runtime hooks, factories, and frameworks may create or restore objects under separate rules.

## Worked Examples

### Example 1

**Question:** Two calls create `Point(2, 5)`. What is shared and what is distinct?

**Reasoning:** Under an ordinary fresh-construction contract, the calls allocate identities $p$ and $q$ with $p\ne q$. Their direct class is `Point`, their initial coordinate state can be structurally equal, and their methods may resolve to shared class-defined code. Mutating only $p$'s instance field does not change $q$, unless a field references another shared mutable object.

**Conclusion:** One class can classify equal-state but identity-distinct instances while sharing behavior code.

### Example 2

**Question:** If `SavingsAccount` extends `Account`, is a savings object an exact `Account` instance?

**Reasoning:** Its direct class is `SavingsAccount`, so it belongs to $Exact(SavingsAccount)$. The declared relation makes it belong to $Instances(Account)$, but not to $Exact(Account)$. A serializer requiring the exact base layout and a client accepting the account protocol therefore need different checks.

**Conclusion:** Exact class and inherited membership must not share one ambiguous “is an instance” claim.

### Example 3

**Question:** A Java variable is declared `Account account = new SavingsAccount()`. What classifies the expression and object?

**Reasoning:** The variable's declared type is `Account`, which governs compile-time member access and assignments. The allocated object's runtime class is `SavingsAccount`; it is also an inherited instance of `Account`. Later dynamic dispatch may choose descendant behavior, but dispatch is not needed to establish these three simultaneous facts.

**Conclusion:** Declared type, direct runtime class, and inherited classification can differ without contradiction.

### Example 4

**Question:** Can abstract class `Shape` have instances if `new Shape()` is illegal?

**Reasoning:** Concrete `Circle` and `Rectangle` classes can extend `Shape`. Their objects satisfy inherited membership in `Shape`, so $Instances(Shape)$ is nonempty. The language separately rejects direct construction, leaving $Exact(Shape)$ empty if no other mechanism creates direct instances.

**Conclusion:** Classification of descendant objects does not imply direct constructibility.

### Example 5

**Question:** Why do two `Cart` objects unexpectedly contain the same items?

**Reasoning:** The implementation placed one mutable list in a class-side field. Both carts resolve `items` to that same object, so adding through either access path mutates shared state. Moving creation of the list to per-instance construction gives each cart a distinct list, while a deliberately shared catalog should instead be named and owned as such.

**Conclusion:** Per-instance state stored on the class side converts accidental access into global aliasing.

### Example 6

**Question:** A Python function executes the same nested `class Token` statement twice. Are the results one class?

**Reasoning:** Each execution creates a new class object and binds the local name for that invocation. The two class objects can share a name and source location while differing in identity. An instance of the first does not become an instance of the second merely because both render as `Token`.

**Conclusion:** Source spelling does not uniquely determine runtime class identity in a dynamic class system.

### Example 7

**Question:** Why can `value instanceof Constructor` change in ECMAScript without reconstructing `value`?

**Reasoning:** The ordinary test follows the constructor's current membership behavior, usually searching for its current `prototype` object in `value`'s prototype chain. Reassigning `Constructor.prototype`, mutating the object's chain, crossing realms, or defining `Symbol.hasInstance` can change the result.

**Conclusion:** `instanceof` is a specified runtime relation, not immutable historical proof of which code created an object.

### Example 8

**Question:** Two Java plugins contain a class with the same binary name. Must their instances share one runtime class?

**Reasoning:** The Java Language Specification treats runtime class identity as involving both binary name and defining class loader. Isolated plugin loaders can therefore define distinct runtime classes with the same name. A cast or registry keyed only by text can fail even when files came from equivalent source.

**Conclusion:** Runtime classification can include loading context; names alone are insufficient identity.

### Example 9

**Question:** A hospital integration object is an instance of `CertifiedInfusionPump`. Does the class test authorize medication delivery?

**Reasoning:** No. The name and nominal membership do not establish device identity, firmware, calibration, certification scope, maintenance state, authenticated channel, command freshness, unit semantics, patient/order match, dose limits, fail-safe behavior, or clinical workflow. Acceptance requires named biomedical engineers, pharmacists, prescribers, nurses, clinical informaticians, medication-safety and human-factors specialists, accessibility/localization experts, cybersecurity engineers, quality/regulatory and legal staff, device vendors, operators, affected clinical users, and independent clinical/technical reviewers. No external review is claimed.

**Conclusion:** A class predicate cannot carry clinical, regulatory, security, or operational evidence the program never verified.

### Example 10

**Question:** Should an immutable currency code be represented by a class, a record, or interned named instances?

**Reasoning:** A transparent record supports structural values but may admit invalid codes unless construction is controlled. A class can validate and own behavior, though identity-based equality would be misleading. Interned named instances reduce duplication and permit reference comparison only if the closed set, versioning, deserialization, and loader scope are guaranteed. A factory returning an immutable value can preserve validation without promising fresh identity.

**Conclusion:** Choose the mechanism from equality, population, extensibility, and construction requirements—not from the noun “currency.”

## Cross-Program Connections

[Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) separates static judgments, runtime values, environments, and observable behavior. [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) represents class declarations, constructors, layouts, runtime descriptors, and loading identity.

[Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) distinguishes program classes from domain categories and responsibilities. [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) governs exposed class, plugin, module, and compatibility boundaries.

[Database Engineering](../../18-database-engineering/ROADMAP.md) reconstructs runtime instances from records and exposes persistence-identity conflicts. [Security Engineering](../../25-security-engineering/ROADMAP.md) treats type tags and object references as untrusted evidence unless authority and provenance are established.

[Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) makes allocation, layout, lifetime, and representation cost explicit. [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) verifies construction partitions, membership boundaries, shared-state isolation, and behavioral contracts.

## References

- Oracle, [*The Java Language Specification, Java SE 26 Edition*, Chapters 4, 8, 12, and 15](https://docs.oracle.com/en/java/javase/26/docs/specs/jls/index.html), 2026. Official class types, objects, class declarations, constructors, initialization, creation expressions, and runtime class identity; checked 2026-08-29.
- Python Software Foundation, [*Python 3.14.7 Language Reference: Data Model*](https://docs.python.org/3/reference/datamodel.html), 2026. Official identity, type, class-object, instance-creation, attribute, and customization model; checked 2026-08-29.
- Python Software Foundation, [*Python 3.14.7 Language Reference: Class Definitions*](https://docs.python.org/3/reference/compound_stmts.html#class-definitions), 2026. Executable class declarations, namespace preparation, class creation, decorators, and bindings; checked 2026-08-29.
- Ecma International, [*ECMAScript 2026 Language Specification*, Classes and Ordinary Object Behaviours](https://tc39.es/ecma262/2026/multipage/ecmascript-language-functions-and-classes.html), 2026. Constructor/prototype creation, class evaluation, fields, private names, and runtime semantics; checked 2026-08-29.
- Ecma International, [*ECMA-335: Common Language Infrastructure*, 6th edition](https://ecma-international.org/publications-and-standards/standards/ecma-335/), 2012. Common Type System class semantics, inheritance, fields, methods, and object creation.
- Object Management Group, [*Unified Modeling Language 2.5.1*, `9.9 Classifiers](https://www.omg.org/spec/UML/2.5.1/PDF), 2017. Normative modeling definition of classifiers as classifications of instances according to features.
- Martín Abadi and Luca Cardelli, [*A Theory of Objects*](https://link.springer.com/book/10.1007/978-1-4419-8598-9), Springer, 1996, DOI 10.1007/978-1-4419-8598-9. Object calculi, classes, inheritance, typing, and class encodings.
- Kim B. Bruce, [*Foundations of Object-Oriented Languages: Types and Semantics*](https://mitpress.mit.edu/9780262525732/foundations-of-object-oriented-languages/), MIT Press, 2002. Formal separation of objects, class-based languages, subtypes, subclasses, and soundness.
- William R. Cook, [“On Understanding Data Abstraction, Revisited”](https://www.cs.utexas.edu/~wcook/Drafts/2009/essay.pdf), *OOPSLA 2009*, pp. 557–572, DOI 10.1145/1639949.1640133. Distinguishes object interfaces and abstract data types, limiting class-as-record intuitions.
- Alan C. Kay, [“The Early History of Smalltalk”](https://doi.org/10.1145/155360.155364), *ACM SIGPLAN Notices* 28(3), 1993, pp. 69–95. Primary historical account of evolving object, class, and message mechanisms.

## Exercises

### Exercise 1

Define class, instance, direct class, inherited membership, class type, class value, constructor, instance member, and class-side member. Then classify each element of a Java declaration and creation expression without using “the class” ambiguously.

### Exercise 2

Let $Checking\preceq Account$, $Savings\preceq Account$, and heap $H_0$ be empty. Trace successful constructions of `Checking(10)` and `Savings(10)`, giving identities, direct classes, exact/inherited sets, and heap states. Then explain how the proof changes under an interning policy.

### Exercise 3

A Python `Cart` declares `items = []` in the class body and appends through `self.items`. Diagnose observations across two carts, repair per-instance ownership, and design tests that distinguish shared class metadata from forbidden shared mutation, including subclass and concurrent cases.

### Exercise 4

Compare Java, Python, and ECMAScript for class declaration execution, class/constructor values, instance construction, exact class, inherited membership, class-side state, and one boundary where a runtime membership test can surprise a plugin system.

### Exercise 5

A hospital platform loads device adapters as classes and currently authorizes infusion commands when `isinstance(adapter, CertifiedInfusionPump)` succeeds. Design a safe classification and construction boundary, evidence model, rejection behavior, adversarial tests, and named human review needed before any clinical deployment.

## Answers to the Exercises

### Answer 1

A class is the language-defined construction/classification and feature-owning mechanism. An instance is one object admitted by its classification relation. Direct class is the most specific runtime class associated with creation; inherited membership includes ancestor classifiers. A class type is a static set of reference values and admitted operations. A class value is a runtime representative when the language exposes one. A constructor is the special creation/initialization operation selected by a creation expression. Instance members are interpreted relative to one receiver; class-side members belong to the class-level scope/entity.

For `class Point { int x; static int count; Point(int x) {...} }`, `Point` introduces a nominal class declaration and class type; `x` is instance state; `count` is class-side state; and `Point(int)` is a constructor declaration, which Java explicitly does not count as a member. In `Point p = new Point(3)`, the first `Point` is a type name, `p` is a variable, `new Point(3)` is a class-instance creation expression selecting a constructor, and the result is a reference to a newly created `Point` instance if construction completes. The runtime `Class` object representing `Point` is another object and is not `p`.

### Answer 2

Choose fresh identities $i$ and $j$. The first transition gives $H_1=H_0[i\mapsto balance(10)]$ and $direct(i)=Checking$. Thus $Exact(Checking)=\{i\}$, $Instances(Checking)=\{i\}$, and $i\in Instances(Account)$. The second gives $H_2=H_1[j\mapsto balance(10)]$, $j\ne i$, and $direct(j)=Savings$. Now $Exact(Savings)=\{j\}$, $Instances(Savings)=\{j\}$, $Exact(Checking)=\{i\}$, and $Instances(Account)=\{i,j\}$. Equal balances do not imply equal identity or direct class.

Under interning, freshness is not an assumed postcondition. A key would have to include enough information to decide whether `Checking(10)` and `Savings(10)` may share; normally their different direct classes forbid one representative. Even two `Checking(10)` requests could return one identity only if `Checking` is immutable, domain equality matches the key, callers cannot rely on distinct identity, loader/tenant scope is defined, and eviction/concurrency are safe. The membership equations still apply to whatever identity is returned, but the $i\ne j$ proof no longer follows.

### Answer 3

The class body executes once for that class object and binds one list. Neither instance initially has its own `items`; lookup reaches the class list. Appending through `self.items.append(...)` mutates that shared list, so both carts observe every append. Assigning `self.items = [...]` would instead create an instance attribute and shadow the class attribute, producing inconsistent instances.

Repair by creating a fresh list in `__init__` for every cart, preferably exposing behavior such as `add` and an immutable snapshot rather than the list itself. Keep only genuinely immutable metadata such as a schema version on the class side. Tests should create two carts, mutate each independently, assert distinct item containers through public observations, construct in both orders, and ensure a subclass receives its intended initialization. Repeated and concurrent construction should not reuse lists; concurrent operations on one cart need a separate synchronization policy. A test that merely checks both start empty misses shared identity and is insufficient.

### Answer 4

Java class declarations introduce nominal class types and runtime classes; creation uses `new` and constructor selection, exact runtime identity includes defining loader, `instanceof` admits declared subtype relations, and static fields belong to a loaded class. The class name appears in value-like reflective forms such as class literals, but a Java class is not simply called as an ordinary function.

Python executes a class definition, builds a namespace, creates a class object through metaclass machinery, and binds the name. Calling the class object normally invokes its construction protocol. `type(x) is C` is exact class-object identity; `isinstance` includes subclass/ABC rules. Class attributes live on the class object and may be shadowed by instance attributes.

ECMAScript evaluates class syntax to a constructor with a prototype object; `new` invokes construction. Ordinary inherited membership through `instanceof` follows the constructor's membership algorithm/prototype chain rather than a sealed nominal declaration. Static elements belong to the constructor side. A plugin system can be surprised by Java same-name classes from distinct loaders, Python reloads creating new class objects, or ECMAScript cross-realm constructors/prototype mutation. Robust boundaries exchange explicit versioned contracts and capabilities instead of trusting a textual class name alone.

### Answer 5

Replace the authorization predicate with several independent gates. Load an adapter only from an authenticated, signed, allowlisted package whose publisher, digest, API version, dependency set, and revocation state are verified. Bind it to an exact device model/serial, firmware, approved configuration, calibration/maintenance record, and deployment environment. Construct it through a restricted factory that validates configuration, establishes authenticated transport, performs a read-only compatibility handshake, and returns a capability limited to explicitly approved operations. Keep clinical command authorization in a separate policy service using authenticated patient/order/context data, terminology and unit checks, dose/rate bounds, freshness, dual confirmation where required, audit logging, and fail-closed behavior.

Class or interface membership can be one compatibility signal, never the authorization. Reject unknown loaders, duplicate IDs, stale/replayed evidence, unsupported firmware, ambiguous units, confusable text, partial initialization, timeouts, disconnected devices, excessive payloads, invalid state transitions, and adapters whose reported identity disagrees with authenticated device evidence. Test malicious subclasses, monkey-patching/proxying, loader and realm duplication, forged serialization tags, dependency substitution, concurrency, rollback, network partition, clock skew, restart, revocation, and safe shutdown. Preserve a simulator boundary so tests cannot actuate hardware.

Named review and approval must include pharmacists, prescribers, nurses, medication-safety officers, clinical informaticians, biomedical/device and integration engineers, cybersecurity and safety engineers, human-factors, accessibility and localization specialists, quality management, regulators, legal/privacy staff, vendor representatives, site operations/training, affected clinical users, and independent clinical and technical assurance. Require traceable hazards, requirements, verification, validation, usability, cybersecurity, change-control, incident-response, and deployment evidence. No class design or automated test alone establishes clinical safety, regulatory approval, or authority to deliver medication; no external review is claimed here.
