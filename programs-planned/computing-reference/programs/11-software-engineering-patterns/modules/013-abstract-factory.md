---
module_id: SEPAT-013
program: Software Engineering: Patterns
level: 1
module_number: 13
title: Abstract Factory
status: complete
last_verified: 2026-08-28
---

# Abstract Factory

## One-Page Review

### Governing question

When must several product roles vary as one coherent family, and how can a client create them without naming concrete family members?

### Essential definitions

- An **Abstract Factory** declares creation operations for a set of related Product roles without exposing their concrete classes to clients.
- A **Concrete Factory** implements every required creation operation for one product family.
- A **product family** is a set of products intended and verified to collaborate under one platform, protocol, theme, provider, or policy.
- A **product role** is one position in every complete family, such as Button, Checkbox, or Dialog.
- **family coherence** means products returned by one factory share every compatibility dimension required by their collaboration.
- A **family invariant** is a property across multiple products, not merely within each product independently.
- **family selection** chooses one Concrete Factory, normally once at a composition boundary.
- A **partial family** omits a required role; it is invalid unless the Abstract Factory contract marks that role optional explicitly.
- A **cross-family mix** combines products from incompatible Concrete Factories and can violate behavior even when each product satisfies its individual role contract.

### Central model, mechanism, or theorem

Let roles be (R=\{r_1,\ldots,r_n\}) and families (G=\{g_1,\ldots,g_m\}). Abstract Factory operations create

\[
F_{g_j}(r_i,c)\rightarrow p_{ij}:P_i.
\]

Individual validity requires (p_{ij}\models P_i). Family validity additionally requires

\[
Compatible_{g_j}(p_{1j},\ldots,p_{nj},c).
\]

Selecting one factory establishes a configuration witness for all products it creates. Type conformance alone does not prove cross-product compatibility; contract tests must exercise collaboration invariants.

### Critical invariants

- Every Concrete Factory implements the complete required role set.
- Every returned product satisfies its individual Product contract.
- Products from one factory share the declared family identity and configuration.
- Clients select and receive one family factory explicitly; they do not instantiate Concrete Products.
- Family selection is stable over the collaboration lifetime unless migration is atomic and supported.
- Ownership, error, security, and resource semantics are compatible across roles.
- Adding a family includes a full shared contract suite; adding a role updates all Concrete Factories.
- Optional roles use an explicit capability model, not `null` or silent fallback to another family.

### Common failures

Common failures include creating unrelated products in one factory, using Abstract Factory for one product role, returning mixed provider or protocol versions, treating matching interface names as proof of compatibility, selecting a family repeatedly inside clients, adding `null` methods for incomplete families, hiding an unbounded service locator behind the factory, leaking Concrete Product types, forgetting the cost of adding a product role, and allowing runtime family swaps while old products remain active.

### Compact example

A UI supports light and high-contrast themes. Each family creates both Button and Checkbox products carrying the same theme token. The screen receives one factory and never chooses concrete widgets. Contract tests verify each widget and render mixed interaction. If a new Slider role becomes required, both factories must implement it; if a dark family is added, one new complete factory is added.

### Connections

[SEPAT-011](011-simple-factory-and-creation-functions.md) centralizes one closed selection; [SEPAT-012](012-factory-method.md) varies one product through creator override; [SEPAT-014](../ROADMAP.md) assembles one complex product stepwise. Abstract Factory connects to platform abstraction in [Software Engineering: Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), family types in [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), and provider compatibility in [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

What evidence shows that product choices must move together as a family, and what boundary can enforce that coherence throughout creation, use, and migration?

Abstract Factory solves correlated variability. A renderer, font service, and color profile may all vary by platform. A storage client, credential provider, and retry classifier may vary by cloud provider. Choosing each independently creates combinations that compile but fail semantically.

The pattern makes one family decision produce all related roles. It is justified only when family consistency matters. A grab bag of unrelated constructors is a container, not a product-family abstraction.

## Why This Matters

Compatibility defects cross component boundaries. An encoder emits protocol version 3 while a decoder expects version 2; a transaction uses one provider's identity but another provider's retry semantics; a themed widget bypasses the accessibility palette. Unit tests of individual products can all pass.

One selected factory makes valid combinations easier to construct and invalid combinations harder. It localizes concrete dependencies and supports whole-family substitution in tests or deployment.

The structure has a known evolution asymmetry. Adding a Concrete Factory is often localized. Adding a required Product role changes the Abstract Factory interface, every Concrete Factory, clients, tests, and compatibility policy. Apply it when the role set is more stable than the family set.

## Prerequisites and Retrieval

You should understand interfaces, subtype contracts, creation functions, Factory Method, dependency injection, and configuration. Retrieve these facts:

1. Multiple individually valid objects can be incompatible together.
2. A family is defined by shared forces and collaboration, not directory placement or vendor name alone.
3. Factory selection and product use are separate responsibilities.
4. Interface changes propagate to every implementation.
5. Optional capability and missing implementation are different states.
6. Long-lived resources make mid-session family replacement a migration problem.

## Learning Objectives

After completing this module, you should be able to:

- identify Abstract Factory, Concrete Factory, Product roles, Concrete Products, and client roles;
- derive a family from correlated variation and compatibility forces;
- specify individual and cross-product contracts;
- distinguish Abstract Factory from simple factory, Factory Method, Builder, and Service Locator;
- implement and test complete families;
- model optional roles and capability discovery explicitly;
- analyze role-addition versus family-addition cost;
- migrate family implementations without mixing incompatible live products.

## Core Exposition

### Correlated variability is the force

List creation decisions and inspect whether they change together. If choosing platform `A` forces matching Button, Checkbox, and Dialog behavior, the variation is a family. If a logger varies independently from all three, it does not belong in that Abstract Factory merely because the UI uses it.

Use change history, compatibility matrices, protocols, and incidents. “These classes come from one vendor” is weaker evidence than “their identity, transaction, and failure contracts require one provider context.”

### Define stable product roles

The Abstract Factory interface names roles expected across every complete family. Roles should be meaningful to clients: `create_button`, `create_transaction`, or `create_encoder`. Avoid generic `resolve(type)` because it erases completeness and becomes Service Locator.

Each role has its own behavioral contract. The factory adds family-level contracts: shared version, theme, endpoint authority, identity domain, transaction scope, security policy, or lifecycle.

### Select one family explicitly

External configuration maps to one Concrete Factory at a composition root. Consumers receive the Abstract Factory or ready products. They do not repeatedly inspect environment variables or provider names.

Pass ready products when their lifetime is application-wide. Pass the factory when a consumer legitimately creates multiple products during behavior and family coherence must be retained.

### Complete families

A Concrete Factory must implement every required role. Construction should fail early if configuration cannot support the family. Returning `null`, an unsupported exception late in use, or a product borrowed from another family defeats valid construction.

If capability differences are inherent, split the interface, represent capabilities explicitly, or make roles optional with a typed result and client policy. Do not pretend the family is complete.

### Individual and collaboration contracts

Test each Concrete Product against its Product contract. Then test combinations produced by each Concrete Factory. A button and checkbox might share focus order, theme token, event loop, accessibility settings, and disposal authority.

For protocols, encode with one product and decode with its partner. For data systems, create a transaction and repository from the same factory, then verify identity and commit visibility. Cross-product tests are the evidence distinctive to this pattern.

### Implementation strategies

A Concrete Factory can use direct constructors, Factory Methods, a Prototype table, functions, or dependency injection. Abstract Factory describes the client-facing family creation contract, not one mandated implementation technique.

Factory operations may return interfaces, values, or resource handles. Keep configuration immutable where possible so every product receives the same family witness.

### Adding families

To add family (g_{m+1}), implement every role, run the shared family suite, add explicit selection, and document migration. Existing clients and the Abstract Factory interface need not change if the role set is stable.

This is the pattern's open axis. It is not cost-free: a new family must satisfy all role and collaboration contracts, operations, security, and version support.

### Adding product roles

Adding `create_slider` changes the Abstract Factory interface and every Concrete Factory. Defaults can ease source migration but can silently create incoherent products. Treat role addition as coordinated schema evolution.

Version the family contract across independent deployments. Provide compatibility windows and prove no client requests the new role from an old factory.

### Runtime switching and migration

Switching a theme before creating a new short-lived screen may be safe. Switching a database family while transactions, repositories, or sessions remain active is not. Define a family scope and quiescence boundary.

Use expand–migrate–contract: introduce the new factory, create isolated new scopes, compare behavior, drain old scopes, then retire the old family. Never combine old and new products unless an explicit bridge proves compatibility.

### Type-level family coherence

Some languages can encode families with associated types, generics, modules, or dependent relationships. This can reject cross-family mixes statically within one compilation boundary. Runtime configuration, plugins, serialization, and version skew still need validation.

If the type system cannot express the relationship, use immutable family identifiers and runtime assertions at boundaries. Do not scatter tag checks through ordinary clients.

### Avoid container growth

An Abstract Factory should own one coherent family. Adding unrelated `create_logger`, `create_clock`, `create_user_repository`, and `create_email_service` creates an application container interface. Clients gain broad construction authority and dependencies become obscure.

Split by stable family boundary or assemble ready dependencies at the composition root. The number of methods is not the issue; causal coherence is.

## Definitions and Notation

Let roles (R), families (G), configuration (c), and Concrete Factory (F_g) be defined as above. Role completeness is

\[
\forall g\in G,\forall r_i\in R_{required}:F_g(r_i,c)=Ok(p_{ig})\text{ or a documented creation failure}.
\]

For successful products, individual validity is

\[
I_i(p_{ig},c)=true.
\]

Family coherence uses witness (w_g(c)):

\[
family(p_{ig})=w_g(c)\quad\forall r_i\in R,
\]

plus collaboration properties

\[
J_g(p_{1g},\ldots,p_{ng},c)=true.
\]

A product (p_{ia}) from family (a) and (p_{jb}) from family (b) is not assumed compatible when (a\ne b), even if each satisfies its individual interface. Safe family migration from (a) to (b) requires a boundary at which no live invariant spans both, or an explicit compatibility relation proved for that span.

## Mechanisms, Invariants, or Proof Structure

### Find coupled decisions

Identify product roles whose provider, platform, version, theme, or policy must change together. Exclude independent services.

### Define complete role contracts

Specify every required operation, product behavior, family witness, collaboration invariant, ownership, and error contract.

### Select and freeze family scope

Choose one Concrete Factory at an explicit boundary and keep it stable for the collaboration lifetime.

### Verify family coherence

The executable example creates two complete UI families and checks that paired products share the expected family token.

<!-- bijux-verify: {"id":"coherent-widget-families","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"light: button=light-button checkbox=light-checkbox compatible=True\ncontrast: button=contrast-button checkbox=contrast-checkbox compatible=True\n","stderr":""}} -->
```python
class Widget:
    def __init__(self, family, role):
        self.family = family
        self.role = role

    def render(self):
        return f"{self.family}-{self.role}"


class LightFactory:
    family = "light"

    def create_button(self):
        return Widget(self.family, "button")

    def create_checkbox(self):
        return Widget(self.family, "checkbox")


class ContrastFactory:
    family = "contrast"

    def create_button(self):
        return Widget(self.family, "button")

    def create_checkbox(self):
        return Widget(self.family, "checkbox")


for factory in (LightFactory(), ContrastFactory()):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    compatible = button.family == checkbox.family == factory.family
    print(
        f"{factory.family}: button={button.render()} "
        f"checkbox={checkbox.render()} compatible={compatible}"
    )
```

The run verifies two roles, two families, and one equality invariant. It does not prove UI accessibility, behavior, resource compatibility, arbitrary family completeness, or safety of runtime switching.

### Exercise both evolution axes

Test adding a family without client changes and simulate adding a role across all factories. This exposes the pattern's real maintenance trade.

### Plan migration and removal

Define scope, draining, compatibility, rollback, and contraction. Remove the abstraction if only one family remains and the boundary owns no useful compatibility or testing role.

## Alternatives and Trade-Offs

**Direct construction.** Clear for one stable family. It permits scattered or mixed selection when families vary.

**Simple factory.** Selects among products for one role. Multiple independent selectors may create incoherent combinations.

**Factory Method.** Lets creator subtypes choose one Product. Multiple roles can require parallel hooks and do not automatically share a family witness.

**Abstract Factory.** Makes complete family selection explicit and supports whole-family substitution. Adding roles is invasive and the abstraction can become a container.

**Builder.** Assembles one complex product across ordered steps. It does not inherently coordinate separate Product roles.

**Prototype table.** Clones family exemplars and can implement a Concrete Factory. Copy semantics and resource identity require care.

**Dependency injection composition.** Supplies ready coherent products without exposing creation. It fits when clients need products once rather than repeated family creation.

**Service Locator.** Provides broad runtime lookup. It hides dependency sets and does not guarantee family completeness.

## Failure Modes and Misconceptions

1. **Several constructors imply Abstract Factory.** The products must vary coherently as a family.
2. **One product role needs Abstract Factory.** A simple factory or Factory Method is usually smaller.
3. **Common interfaces prove family compatibility.** Collaboration invariants require separate evidence.
4. **Every family can return null for missing roles.** This creates invalid late failure.
5. **Adding roles is easy.** It changes every Concrete Factory and often every deployed implementation.
6. **Family selection can happen anywhere.** Scattered selection permits cross-family mixes.
7. **Runtime swapping is just configuration.** Live products can span state, resources, and transactions.
8. **Generic resolve is more flexible.** It erases role completeness and approaches Service Locator.
9. **A vendor defines one family automatically.** Versions, regions, identity domains, and policies can split compatibility.
10. **The factory must remain after one family survives.** Retain it only for a meaningful boundary, tests, or future supported variability.

## Worked Examples

### Example 1

**Question:** What family property does the executable example test?

**Reasoning:** Each Concrete Factory returns Button and Checkbox products whose family tokens equal one another and the factory token. It does not test actual widget behavior.

**Conclusion:** Cross-product equality is one bounded family invariant, not complete compatibility.

### Example 2

**Question:** When do database repositories and transactions form a family?

**Reasoning:** They must share connection/session, identity map, isolation, commit authority, and provider error semantics. Independently selecting them can make writes invisible or commits ineffective.

**Conclusion:** Transactional collaboration supplies stronger evidence than a shared vendor label.

### Example 3

**Question:** Should logger creation join a UI widget factory?

**Reasoning:** A logger used by the UI varies independently from theme widgets. Adding it broadens client authority without enforcing a family invariant.

**Conclusion:** Exclude unrelated conveniences from the family contract.

### Example 4

**Question:** How is Abstract Factory different from Factory Method?

**Reasoning:** Factory Method binds one product creation to creator subtype and stable workflow. Abstract Factory exposes several role operations on a selected family object. Concrete Factory methods may themselves use Factory Method.

**Conclusion:** The patterns address different variation structures and can compose.

### Example 5

**Question:** What happens when a Slider role is added?

**Reasoning:** Change the Abstract Factory contract, implement Slider for every family, extend shared family tests, migrate independently deployed factories, and guard clients during the compatibility window.

**Conclusion:** Role-set stability is a major applicability force.

### Example 6

**Question:** How should a platform with no native checkbox behave?

**Reasoning:** Supply a verified emulated checkbox satisfying the contract, split the factory capability, or reject family construction. Returning null or borrowing another platform's product creates late incoherence.

**Conclusion:** Model incomplete capability explicitly.

### Example 7

**Question:** Are two versions of one protocol provider the same family?

**Reasoning:** Not necessarily. Encoder, decoder, validator, error mapping, and negotiation must share a compatible version. Treat incompatible versions as distinct families with bridges where proven.

**Conclusion:** Family identity includes every collaboration-relevant dimension.

### Example 8

**Question:** When should clients receive ready products instead of a factory?

**Reasoning:** If a consumer needs one long-lived repository and transaction coordinator, construct and inject them at the composition root. Passing the factory grants unnecessary creation authority.

**Conclusion:** Expose the narrowest capability required by client behavior.

### Example 9

**Question:** How can associated types improve the design?

**Reasoning:** They can bind each factory implementation to exact Product types and reject some cross-family combinations statically. Runtime configuration and versioned plugins still require evidence.

**Conclusion:** Type relationships strengthen but do not replace family contracts.

### Example 10

**Question:** When can Abstract Factory be removed?

**Reasoning:** If only one family remains permanently, clients never create products repeatedly, and no test or compatibility boundary benefits, inject ready concrete or role-interface products and contract the factory.

**Conclusion:** Preserve coherence with the smallest current mechanism.

## Cross-Program Connections

- **Object-Oriented Programming:** interface families, associated types, and subtype contracts express role relationships.
- **Functional Programming:** records of creation functions encode an Abstract Factory without classes.
- **Programming Languages:** modules, generics, and type families can prevent some invalid combinations.
- **Software Design:** common closure and protected variation identify stable role sets and variable families.
- **Software Architecture:** platform and provider abstractions often operate at family scale.
- **Testing & Quality Engineering:** collaboration contract suites detect defects missed by product unit tests.
- **Database Engineering:** transaction, repository, identity, and dialect components require coherent provider scope.
- **Distributed Systems:** protocol versions and serialization families require negotiated compatibility.
- **Cloud Engineering:** client, credential, endpoint, retry, and telemetry semantics may form provider families.
- **Security Engineering:** family selection can enforce approved algorithms, trust roots, and policy versions.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Abstract Factory intent, structure, participants, consequences, and implementation discussion.
2. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, [*Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*](https://www.wiley.com/en-us/Wiley%2BSoftware%2BPatterns%2BSeries-c-7544), Wiley, 1996. Connects pattern systems and platform-oriented families across architectural and design scales.
3. Craig Larman, [*Applying UML and Patterns*, 3rd ed.](https://www.pearson.com/en-us/subject-catalog/p/applying-uml-and-patterns-an-introduction-to-object-oriented-analysis-and-design-and-iterative-development/P200000000422), Prentice Hall, 2004. Applies GoF patterns within responsibility-driven object design.
4. Bernd Bruegge and Allen H. Dutoit, [*Object-Oriented Software Engineering Using UML, Patterns, and Java*, 3rd ed.](https://www.pearson.com/en-us/subject-catalog/p/object-oriented-software-engineering-using-uml-patterns-and-java/P200000003319/9780136061250), Prentice Hall, 2009. Covers platform encapsulation and Abstract Factory in object design.
5. Eric Evans, [*Domain-Driven Design: Tackling Complexity in the Heart of Software*](https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217), Addison-Wesley, 2003. Supplies aggregate, lifecycle, and valid-construction reasoning relevant to coherent domain product creation.
6. Martin Fowler, [“Inversion of Control Containers and the Dependency Injection Pattern”](https://martinfowler.com/articles/injection.html), 2004, accessed 2026-08-28. Supports explicit configuration/use separation and comparison with service location.

## Exercises

### Exercise 1

Specify individual Product and family contracts for the executable widgets. Add at least ten collaboration tests beyond the printed family-token equality.

### Exercise 2

Add a required Slider role. Describe source, binary, deployment, test, and compatibility changes for independently versioned Concrete Factories.

### Exercise 3

Design an Abstract Factory for repository, transaction, and identifier products across in-memory and SQL families. State family invariants and when ready-product injection is preferable.

### Exercise 4

Plan a live migration from protocol family version 2 to version 3 without mixing incompatible encoders, decoders, and validators.

### Exercise 5

An unfamiliar radiation-therapy platform supports independently supplied device families. Produce a graduate-level Abstract Factory design covering complete roles, calibration identity, safety invariants, trust, real-time behavior, versioning, evidence, migration, rollback, and human authorization.

## Answers to the Exercises

### Answer 1

Button and Checkbox contracts define rendering, focus, activation/toggle behavior, accessibility name/state, event-loop affinity, error behavior, disposal, thread safety, and nonmutation of shared theme configuration. Family contracts require the same immutable theme version, palette, scale, font metrics, focus manager, event loop, accessibility policy, and disposal authority.

Test Button and Checkbox individually, then paired rendering scale, palette contrast, focus traversal in both directions, keyboard activation, disabled-state consistency, accessibility tree order, high-contrast state visibility, shared event-loop enforcement, concurrent misuse rejection, theme-version mismatch rejection, disposal order, double disposal, and no use after family scope closes. Test both families through one suite and add a deliberate mixed pair that must be rejected at the boundary.

### Answer 2

Add `create_slider` to the source contract and implement a Product contract for value range, steps, events, accessibility, theme, ownership, and thread affinity. Every Concrete Factory must add a compatible Slider and the shared family suite must exercise three-product collaboration. Source clients compiled against the old interface may remain unchanged, but every implementation must compile against the new contract.

Across independent binaries, an old factory lacks the entry point. Introduce a versioned capability contract or a new factory interface; do not assume binary compatibility. Deploy factories supporting both versions before clients request Slider, verify inventory and negotiation, then enable clients. Keep old clients during the window. Reject a family that advertises the new version without Slider; never return null or cross-family fallback. Contract old interfaces only after every provider and client leaves the window.

### Answer 3

Roles are Repository, Transaction, and IdentifierCodec. InMemoryFactory creates products sharing one in-memory store, lock/version policy, and identifier namespace. SqlFactory creates products sharing one data source/session policy, dialect, transaction authority, and identifier mapping. Individual contracts cover query/save, begin/commit/rollback, and parse/render; family contracts require repository operations participate in the created transaction, read-your-writes behavior, consistent identity, one commit authority, compatible errors, and uniform ownership.

Run shared families against commit, rollback, conflicts, duplicate identity, failure cleanup, concurrency, and nested-scope policy. Inject ready Repository and transaction coordinator when a consumer holds one application-scoped pair and never creates scopes. Pass a narrow factory when each operation legitimately opens a new coherent transaction/repository scope. Do not give ordinary entities the family factory.

### Answer 4

Treat v2 and v3 as distinct immutable factories, each producing encoder, decoder, validator, and negotiator with one version witness. Expand by deploying components capable of receiving both versions while emitting v2. Establish explicit protocol negotiation and correlation; record peer capability. Add v3 shadow encode/decode comparison on nonauthoritative traffic and test unknown fields, ordering, errors, size, security, and replay.

Migrate one complete session or connection scope at a time to v3; never use a v3 encoder with a v2-only validator. Metrics identify version and factory instance. Roll back new scopes to v2 while existing scopes drain according to their original family. Once all peers, persisted payloads, replayers, and recovery tools support v3, stop v2 emission, drain v2 sessions, preserve required readers for the retention window, then contract. A bridge is a separately specified product with its own loss and security contract, not evidence that arbitrary mixing is safe.

### Answer 5

Define roles such as DeviceCommandEncoder, FeedbackDecoder, CalibrationValidator, SafetyInterlockAdapter, and SessionMonitor. One Concrete Factory corresponds to an approved device model, firmware range, calibration set, treatment-machine identity, and safety-policy version. It must create the complete role set or fail closed before treatment. Every product carries the same immutable family witness; the treatment session verifies it before activation and prohibits mid-session family replacement.

Individual contracts bound input, output, timing, allocation, failure, ownership, and shutdown. Family invariants include calibration identity, units, coordinate system, dose limits, command/feedback correlation, monotonic sequence, fail-safe interlock behavior, deadline, and one audit clock/domain. Signed allowlisted artifacts, verified boot/trust chain, revocation, least capability, secret hygiene, and deterministic selection protect loading. Faults, timeouts, stale calibration, version mismatch, duplicate/reordered feedback, saturation, restart, partition, and corrupted sensor data must lead to specified safe states.

Evidence includes requirements traceability, independent hazard analysis, contract and family tests, static analysis, bounded model checking where tractable, worst-case timing on representative hardware, simulation, hardware-in-the-loop, fault injection, calibration verification, cybersecurity analysis, and controlled clinical validation. Migrate only at a quiescent treatment boundary using signed configuration, complete preflight checks, and rehearsed rollback to a still-approved family; never roll back to revoked firmware or calibration. Named clinical physics, medical, safety, security, regulatory, real-time, device, verification, and operations authorities must approve each family and deployment scope. Repository validation provides no treatment authorization.
