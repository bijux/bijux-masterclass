---
module_id: CA-001
program: Computer Architecture
level: 1
module_number: 1
title: Boolean Logic and Combinational Circuits
status: complete
last_verified: 2026-08-29
---

# Boolean Logic and Combinational Circuits

## One-Page Review

### Governing question

How can an engineer translate a finite input-output requirement into a combinational circuit and establish that the implementation computes the intended Boolean function without confusing functional equivalence with physical correctness?

### Essential definitions

- A **Boolean value** belongs to the set \(\mathbb{B}=\{0,1\}\). In positive logic, 0 and 1 conventionally denote low and high logical levels, not exact voltages.
- A **Boolean function** \(f:\mathbb{B}^n\rightarrow\mathbb{B}^m\) maps every input vector to exactly one output vector.
- A **combinational circuit** is an acyclic network whose modeled outputs depend only on the current modeled inputs. It contains no intentional stored state.
- A **literal** is a variable or its complement. A **minterm** fixes every input variable and denotes one truth-table row.
- **Sum of products** is an OR of AND terms; **product of sums** is an AND of OR terms.
- Two expressions or networks are **functionally equivalent** when they produce equal outputs for every input in the declared Boolean domain.
- A gate set is **functionally complete** if every Boolean function can be expressed using gates from that set. NAND alone and NOR alone are functionally complete.
- A **don't-care condition** is an input pattern whose output may be chosen for optimization only because the specification explicitly makes that pattern irrelevant or unreachable.

### Central model, mechanism, or theorem

For a fully specified finite function, enumerate its truth table, form a canonical expression, simplify under Boolean identities or an exact method, map the expression to available gates, and compare the implementation with the specification on all \(2^n\) input vectors when feasible. The canonical sum-of-products construction proves representability: OR together the minterms for rows where the output is 1. NAND completeness follows constructively because NOT, AND, and OR can each be built from NAND.

### Critical invariants

Every legal input vector has one specified output vector. Simplification preserves the complete truth table, including output width and bit order. A declared don't-care is never silently treated as impossible. Combinational dependency graphs remain acyclic. Interface polarity, active-low notation, bus indexing, and logical-level conventions stay explicit. Verification distinguishes two-valued functional behavior from timing, unknown states, electrical loading, metastability, power, and manufacturing defects.

### Common failures

Engineers often translate prose directly into gates, omit a truth-table row, mistake XOR for OR, apply De Morgan's law without complementing every term and operator, optimize against an assumed impossible input, create an accidental feedback loop, or accept a few simulation vectors as proof of equivalence. Another failure is to call a Boolean function “the circuit”: the same function has many networks whose delay, area, power, hazards, fan-out, technology mapping, and fault behavior differ.

### Compact example

A 2-to-1 selector with data inputs \(d_0,d_1\) and select \(s\) has specification \(y=(\lnot s\land d_0)\lor(s\land d_1)\). If \(s=0\), the second product is 0 and the first reduces to \(d_0\); if \(s=1\), the first is 0 and the second reduces to \(d_1\). Those cases cover all select values, so the expression implements the selector in the two-valued model. They do not establish propagation delay or glitch-free switching while \(s\) changes.

### Connections

The next module adds sequential logic and state; later modules add registers, arithmetic circuits, timing, power, datapaths, and processor architecture. Discrete mathematics supplies propositional equivalence. Testing contributes exhaustive and property-based checks. Hardware-description languages encode concurrent hardware structure, while synthesis maps Boolean networks into a target library. Safety and security engineering determine whether the specification, fault model, and assurance case are adequate for consequential uses.

## Governing Question

How can a finite behavioral requirement be transformed into a stateless Boolean network with auditable evidence of functional equivalence, while keeping the limits of that abstraction visible?

The question has two parts. **Synthesis** asks how to obtain an implementation from a function. **Verification** asks whether the implementation realizes that function. Neither part, by itself, establishes that the original function captures stakeholder intent or that a fabricated circuit behaves safely in its electrical and temporal environment.

## Why This Matters

Every processor eventually reduces architectural decisions to physical mechanisms that steer signals, compare tags, select operands, detect conditions, and generate controls. A decoder decides which instruction class is present. A multiplexer selects one source. A comparator determines equality or order. An adder, cache tag path, permission check, and interrupt controller combine many such functions. When the foundational reasoning is weak, errors propagate upward into state machines and complete processors.

Boolean logic also teaches a durable engineering discipline: separate specification from representation, preserve invariants across transformations, and attach evidence to the claim actually made. Shannon's switching-circuit work made the correspondence between symbolic Boolean reasoning and switch networks systematic. Modern tools automate far larger transformations, but they still require exact interfaces, sound assumptions, suitable equivalence notions, and physical sign-off beyond a truth table.

## Prerequisites and Retrieval

Retrieve sets, functions, binary notation, propositional operators, algebraic substitution, and basic graph vocabulary. You should be able to enumerate \(n\)-bit patterns and read a small Python program. No transistor physics or hardware-description-language experience is required. When uncertain, reconstruct the truth table before manipulating symbols.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish Boolean values, logical levels, expressions, functions, gates, and physical circuits;
2. translate bounded prose into interfaces, truth tables, Boolean expressions, and gate networks;
3. derive canonical sum-of-products and product-of-sums forms;
4. apply identity, complement, absorption, distributive, and De Morgan laws without changing the function;
5. explain and construct functional completeness from NAND or NOR;
6. design and reason about decoders, encoders, multiplexers, comparators, and simple voting logic;
7. prove small two-valued combinational equivalence by exhaustive enumeration;
8. identify unspecified inputs, unsafe don't-care assumptions, cycles, width errors, and polarity errors; and
9. state what Boolean verification cannot establish about timing, electrical behavior, faults, or high-stakes fitness.

## Core Exposition

A Boolean variable ranges over two mathematical values. An electrical implementation represents those values using voltage or current ranges interpreted by a technology. The map is deliberately abstract: a logical 1 is not “one volt,” and real signals can transition, float, violate thresholds, or become unknown to a simulator. Start with the Boolean model because it makes finite behavior precise, then add other models when the claim requires them.

A single-output function of \(n\) inputs has \(2^n\) possible input rows and \(2^{2^n}\) possible truth tables. Multiple outputs can be treated as a vector of single-output functions that share inputs and possibly internal terms. A truth table is complete only when it defines every legal input vector, preserves input order, states output polarity, and marks any intentionally unspecified row explicitly.

The basic operators are NOT, AND, and OR. We write complement as \(\lnot a\), conjunction as \(a\land b\), and disjunction as \(a\lor b\). XOR, \(a\oplus b\), is 1 exactly when its operands differ; XNOR is 1 when they agree. Operator precedence conventions vary, so parentheses and an explicit notation table are cheaper than an ambiguous review.

For any truth-table row, a minterm is an AND of all input literals: use the variable when the row bit is 1 and its complement when the row bit is 0. The minterm is 1 only on that row. OR every on-set minterm to obtain canonical sum of products. Dually, form a maxterm that is 0 on one row and AND maxterms for the zero rows to obtain canonical product of sums. These constructions may be inefficient, but they give a mechanical path from a complete table to a correct expression.

Boolean algebra permits semantics-preserving rewrites. Identity gives \(a\land1=a\) and \(a\lor0=a\). Domination gives \(a\lor1=1\) and \(a\land0=0\). Idempotence gives \(a\lor a=a\). Complement gives \(a\lor\lnot a=1\). Absorption gives \(a\lor(a\land b)=a\). Distributivity works in both directions. De Morgan gives \(\lnot(a\land b)=\lnot a\lor\lnot b\) and \(\lnot(a\lor b)=\lnot a\land\lnot b\). A rewrite is justified by an identity or by equivalence over every valuation, not by visual plausibility.

NAND is \(\lnot(a\land b)\). Tie its inputs together to obtain NOT: \(\operatorname{NAND}(a,a)=\lnot a\). NAND that result with itself to recover AND. Apply NAND to individually inverted inputs to obtain OR by De Morgan. Thus NAND can build NOT, AND, and OR; canonical forms then establish that NAND can realize every finite Boolean function. NOR has a dual construction. Functional completeness says “expressible,” not “optimal,” “fast,” or “safe.”

Common reusable structures follow directly. A decoder maps an \(n\)-bit input to up to \(2^n\) one-hot outputs. An encoder maps an asserted input to a code but needs a policy for zero or multiple assertions; a priority encoder supplies one. A multiplexer selects one data input according to control bits. A demultiplexer steers one input. Equality comparison can AND bitwise XNOR terms. Magnitude comparison requires an ordering rule from the most significant differing bit. Majority logic emits 1 when more than half of the votes are 1, but the word “vote” does not make its inputs independent or trustworthy.

Optimization has several objectives. Fewer literals or gates may reduce area, but factoring can change depth and reconvergent paths. A two-level sum of products can be regular yet expensive. A multilevel network can reuse terms yet create fan-out or timing concerns. Quine and McCluskey developed systematic exact minimization for two-level forms; practical synthesis tools use richer algorithms and technology libraries. “Minimal” must name the cost model: literals, gates, library cells, depth, delay, area, power, or another target.

Don't-care conditions allow the implementation to choose 0 or 1 on designated rows, sometimes enabling major simplification. They are specification facts, not designer convenience. An input called “unreachable” can arise during reset, transition, fault, test, malicious manipulation, or a later interface revision. Preserve the assumption, its owner, and the behavior if it is violated. In safety or security logic, fail-safe behavior may be required instead of optimization freedom.

Verification begins with independent representations. Derive the reference table from requirements; derive or simulate the network separately; compare each legal vector and report counterexamples with full inputs and outputs. Exhaustive enumeration is decisive for a small two-valued function. For larger designs, binary decision diagrams, SAT-based equivalence checking, theorem proving, assertions, simulation, coverage, and formal property checking extend the evidence. Yet a proof relative to the wrong specification remains a precisely proved mistake.

The following executable evidence defines a selector and a three-input majority function, constructs majority using NAND-derived NOT, AND, and OR, and exhaustively compares all eight inputs. It also checks both De Morgan identities. Python booleans model only stable two-valued logic.

<!-- bijux-verify: {"id":"combinational-equivalence-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"majority_vectors=8\nmajority_ones=4\nnand_mismatches=0\ndemorgan_checks=16\nmux_vectors=8\n","stderr":""}} -->
```python
from itertools import product


def nand(a, b):
    return not (a and b)


def nand_not(a):
    return nand(a, a)


def nand_and(a, b):
    return nand_not(nand(a, b))


def nand_or(a, b):
    return nand(nand_not(a), nand_not(b))


def majority_spec(a, b, c):
    return (a and b) or (a and c) or (b and c)


def majority_nand(a, b, c):
    ab = nand_and(a, b)
    ac = nand_and(a, c)
    bc = nand_and(b, c)
    return nand_or(nand_or(ab, ac), bc)


vectors = list(product((False, True), repeat=3))
mismatches = sum(majority_spec(*v) != majority_nand(*v) for v in vectors)
ones = sum(majority_spec(*v) for v in vectors)
demorgan = 0
for a, b in product((False, True), repeat=2):
    assert (not (a and b)) == ((not a) or (not b))
    assert (not (a or b)) == ((not a) and (not b))
    demorgan += 4

mux_vectors = 0
for select, d0, d1 in vectors:
    y = ((not select) and d0) or (select and d1)
    assert y == (d1 if select else d0)
    mux_vectors += 1

print(f"majority_vectors={len(vectors)}")
print(f"majority_ones={ones}")
print(f"nand_mismatches={mismatches}")
print(f"demorgan_checks={demorgan}")
print(f"mux_vectors={mux_vectors}")
```

The run proves equality only for the encoded two-valued functions and enumerated domains. It does not simulate propagation delay, simultaneous transitions, four-state HDL semantics, transistor behavior, fan-out, hazards, power, fabrication variation, radiation faults, or the adequacy of any real voting requirement.

## Definitions and Notation

Let \(\mathbb{B}=\{0,1\}\). Input vectors are \(x=(x_{n-1},\ldots,x_0)\in\mathbb{B}^n\); output vectors are \(y=f(x)\in\mathbb{B}^m\). The **on-set** \(f^{-1}(1)\) contains rows where a single-output function is 1; the **off-set** contains rows where it is 0. A **care set** contains rows whose result is constrained, and a **don't-care set** contains explicitly unconstrained rows.

An **implicant** is a product term whose 1-valuations lie inside the on-set. A **prime implicant** cannot drop another literal while remaining an implicant. An **essential prime implicant** covers at least one on-set minterm covered by no other prime implicant. These definitions support exact two-level minimization; they do not make a two-level implementation physically optimal.

A gate network is a directed graph \(G=(V,E)\) whose input vertices have no predecessors and whose internal vertices compute gate functions. Under the combinational model, \(G\) is acyclic. **Logic depth** is the maximum number of gate stages on a path under a stated decomposition. **Fan-in** counts a gate's inputs; **fan-out** counts loads driven by a signal. Physical delay is not equal to abstract depth without a technology and load model.

We use overbar-free text notation to avoid rendering ambiguity: `not`, `and`, `or`, `xor`, and explicit parentheses. In a schematic, a bubble usually denotes inversion and names such as `reset_n` commonly denote active-low polarity; both require a declared convention. Bit-vector indexing must say whether the leftmost shown bit is most significant.

## Mechanisms, Invariants, or Proof Structure

Use a reviewable synthesis chain:

1. **Bound the interface.** Name every input and output, width, encoding, polarity, legal pattern, and environmental assumption.
2. **State behavior independently.** Convert prose into cases, a truth table, equations, or properties. Resolve conflicts and missing rows before implementation.
3. **Construct a correct baseline.** Use canonical minterms or maxterms when necessary. Correctness precedes optimization.
4. **Simplify with evidence.** Record identities, Karnaugh-map groupings, exact minimization output, or synthesis reports. Preserve the care set and output semantics.
5. **Map to a gate basis.** Respect target fan-in, cell availability, polarity, width, and structural constraints.
6. **Check structure.** Reject combinational cycles, undriven or multiply driven nets, truncation, unintended latches, and accidental constant outputs.
7. **Check function.** Compare reference and implementation for all vectors when tractable; otherwise use formal equivalence or properties plus clearly bounded simulation.
8. **Add physical evidence.** Timing, hazards, electrical rules, power, placement, reset, clock-domain, and fault analysis belong to subsequent sign-off layers.

The central functional invariant is

\[
\forall x\in C:\quad f_{\text{implementation}}(x)=f_{\text{specification}}(x),
\]

where \(C\) is the declared care set. This formulation prevents a common mistake: claiming complete equivalence after checking only convenient inputs. If don't-cares exist, behavior outside \(C\) is unconstrained by this particular claim, not necessarily harmless.

Canonical sum-of-products gives a constructive existence proof. For each on-set row \(r\), form minterm \(m_r\). Exactly one full minterm is true for any input vector. Therefore \(\bigvee_{r\in f^{-1}(1)}m_r\) is 1 exactly on the on-set. NAND completeness then substitutes a NAND construction for NOT, AND, and OR. The proof says a representation exists; exponential canonical size motivates simplification and structured components.

For an \(n\)-input exhaustive check, the evidence size grows as \(2^n\). At 12 inputs, 4,096 vectors are routine; at 64, enumeration is infeasible. Formal equivalence tools reason symbolically, often by reducing inequivalence to whether a **miter** output can ever become 1. Tool success is conditional on parsed semantics, constraints, black boxes, unknown-state treatment, and solver correctness, so preserve versions, commands, assumptions, and reports.

## Alternatives and Trade-Offs

**Truth tables versus equations.** Tables make finite coverage visible and are excellent for small interfaces. Equations expose structure and scale better but can hide missing cases. Maintain both for review-critical blocks and mechanically compare them.

**Canonical versus simplified forms.** Canonical forms are mechanically traceable but often large. Simplified forms reduce a chosen symbolic cost but can obscure correspondence to requirements. Preserve an executable or formal equivalence route between them.

**Two-level versus multilevel networks.** Two-level logic has predictable structure and supports classic minimization. Factored multilevel logic can share subexpressions and reduce area or depth, but reconvergent paths and shared terms complicate physical behavior and fault analysis.

**NAND-only versus target-library mapping.** A universal gate basis is pedagogically and theoretically useful. Real libraries include inverters, complex gates, multiplexers, and characterized cells. Forcing NAND everywhere can worsen delay, area, power, and clarity.

**Manual algebra versus automated synthesis.** Manual work builds understanding and can reveal specification errors. Automated synthesis explores large designs and technology-specific costs. Neither excuses an unreviewed interface or an absent equivalence check.

**Exhaustive simulation versus formal methods.** Exhaustive enumeration is simple and decisive over small finite two-valued domains. Formal equivalence scales symbolically but introduces tool semantics and constraints. Random simulation samples behavior and is valuable for integration, yet passing samples cannot prove a combinational function equal over an untested domain.

**Binary versus four-state reasoning.** Binary algebra supports clean proofs. HDLs commonly add unknown and high-impedance values that expose initialization and contention. A design equivalent under two states may differ under four-state simulation, and neither directly models analog voltage trajectories.

## Failure Modes and Misconceptions

- **“A gate output changes instantly.”** Boolean functions omit time; real gates have delay and finite transitions.
- **“Combinational means no glitches.”** Unequal path delays can produce hazards even when stable endpoints are correct.
- **“XOR is inclusive OR.”** XOR excludes the `11` case; the names sound similar but the tables differ.
- **“A truth table with examples is complete.”** For \(n\) binary inputs, completeness needs all legal rows or an explicit symbolic specification.
- **“Don't-care means cannot occur.”** It means the specified output is unconstrained for a documented reason; occurrence and safety remain separate questions.
- **“Fewer gates is always better.”** Gate count ignores cell type, fan-in, fan-out, depth, wiring, power, load, hazards, testability, and technology.
- **“NAND completeness proves this NAND network is good.”** Completeness establishes expressiveness only.
- **“Simulation passed, so the logic is proved.”** That is true only if the simulation exhausts the exact finite domain with trustworthy reference semantics; ordinary vector sampling is weaker.
- **“The HDL is software executed top to bottom.”** Synthesizable combinational HDL describes concurrent hardware; incomplete assignment can infer state.
- **“Feedback settles to a Boolean answer.”** A cycle violates the acyclic combinational model and may oscillate, retain history, or behave analogically.
- **“Majority voting creates reliability.”** Correlated faults, shared power, common specification defects, voter failure, and invalid sensors can defeat it.
- **“Functional equivalence proves safety or security.”** It proves equality to a function under assumptions, not adequacy of the function, fault containment, tamper resistance, timing, or lifecycle assurance.

## Worked Examples

### Example 1

**Question:** Derive a canonical expression for \(f(a,b)=1\) on rows `01` and `10`.

**Reasoning:** Row `01` gives minterm \(\lnot a\land b\); row `10` gives \(a\land\lnot b\). OR them: \(f=(\lnot a\land b)\lor(a\land\lnot b)\). This is XOR.

**Conclusion:** Canonical minterms translate an on-set mechanically and expose all covered rows.

### Example 2

**Question:** Simplify \(a\lor(a\land b)\).

**Reasoning:** By absorption, the expression equals \(a\). If \(a=1\), both expressions are 1; if \(a=0\), the product is 0. The result does not depend on \(b\).

**Conclusion:** A named identity plus complete case reasoning justifies removing the redundant term.

### Example 3

**Question:** Build OR using NAND only.

**Reasoning:** `NAND(a,a)` is \(\lnot a\), and likewise for \(b\). NAND those complements: \(\lnot(\lnot a\land\lnot b)=a\lor b\) by De Morgan.

**Conclusion:** `NAND(NAND(a,a), NAND(b,b))` implements OR in the stable two-valued model.

### Example 4

**Question:** Specify a 2-to-4 decoder with enable \(e\) and input bits \(a_1a_0\).

**Reasoning:** Each output is an enabled minterm: \(y_0=e\land\lnot a_1\land\lnot a_0\), \(y_1=e\land\lnot a_1\land a_0\), \(y_2=e\land a_1\land\lnot a_0\), and \(y_3=e\land a_1\land a_0\). When \(e=0\), all are 0; when \(e=1\), exactly one is 1 for every binary input.

**Conclusion:** The one-hot invariant follows from mutually exclusive, collectively exhaustive minterms.

### Example 5

**Question:** Design equality for two 3-bit words \(a\) and \(b\).

**Reasoning:** Corresponding bits agree under XNOR. Therefore \(eq=\bigwedge_{i=0}^{2}\lnot(a_i\oplus b_i)\). One differing bit makes the conjunction 0; all equal bits make it 1.

**Conclusion:** Word equality decomposes into bit equality followed by reduction AND.

### Example 6

**Question:** May invalid BCD inputs `1010` through `1111` be don't-cares in a seven-segment decoder?

**Reasoning:** Only if the interface contract makes their output irrelevant and the environment plus fault analysis supports that assumption. During reset, corruption, test, or a producer defect, those patterns may occur. Choosing blank, diagnostic, or fail-safe behavior can be preferable to maximum simplification.

**Conclusion:** Don't-cares require owned environmental evidence, not merely unused nominal encodings.

### Example 7

**Question:** Does verifying a 32-input function with one million random vectors prove equivalence?

**Reasoning:** The domain contains \(2^{32}=4,294,967,296\) vectors. Even distinct random tests cover less than 0.024% of it. A single rare counterexample may remain. Symbolic equivalence, structural reduction, or a proof over partitions is needed for a universal claim.

**Conclusion:** Large test counts are empirical evidence, not proof of untested finite behavior.

### Example 8

**Question:** Why can \((a\land b)\lor(\lnot a\land c)\) glitch when \(b=c=1\) and \(a\) changes?

**Reasoning:** The stable function is 1 before and after the transition, but one product path can turn off before the other turns on because inversions and gates have unequal delays. Adding the consensus term \(b\land c\) can remove the static-1 hazard for a suitable implementation, but actual timing still needs physical analysis.

**Conclusion:** Stable Boolean equivalence does not imply hazard-free temporal behavior.

### Example 9

**Question:** A ventilator controller uses `open = pressure_ok AND command_open AND NOT emergency_stop`. Is exhaustive truth-table agreement enough to deploy it?

**Reasoning:** No. The Boolean check omits sensor validity, stuck-at and transient faults, active-low wiring errors, response deadlines, analog thresholds, power loss, independent shutdown paths, software interaction, alarms, misuse, maintenance, and regulatory requirements. Named clinical, respiratory-therapy, biomedical, hardware, firmware, safety, human-factors, cybersecurity, quality, regulatory, manufacturing, service, and independent assurance reviewers must own acceptance evidence. No such external review is claimed.

**Conclusion:** High-stakes logic requires system safety and lifecycle assurance beyond functional equivalence.

### Example 10

**Question:** Two networks pass all 16 vectors of a four-input truth table. Are they interchangeable?

**Reasoning:** They are functionally equivalent for the declared two-valued interface. They may differ in propagation delay, load drive, area, energy, hazards, test coverage, placement, resilience, and four-state behavior. Interchangeability depends on which additional constraints the surrounding system imposes.

**Conclusion:** State the equivalence relation and all nonfunctional acceptance criteria explicitly.

## Cross-Program Connections

Discrete mathematics and theoretical computer science supply propositional functions, normal forms, satisfiability, and proof. Algorithms explain why exhaustive enumeration grows exponentially and why minimization can be computationally difficult. Programming-languages work clarifies syntax versus semantics, while compiler construction parallels logic synthesis: both transform representations while preserving specified behavior.

Computer architecture owns the path from digital building blocks to arithmetic units, control, pipelines, caches, and processors. [Operating Systems](../../22-operating-systems/ROADMAP.md) consumes architectural mechanisms but owns resource policy and kernel behavior. [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) observes the hardware-software boundary from executable programs. [Concurrency, Parallelism, and Asynchrony](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) later depends on atomic and memory-order mechanisms that cannot be derived from combinational logic alone.

[Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) contributes oracle design, coverage limits, and evidence discipline. [Security Engineering](../../25-security-engineering/ROADMAP.md) treats logic that enforces access or trust as part of a larger threat model. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns stakeholder need, interface, hazard, verification, validation, and lifecycle integration. These connections prevent a small correct function from being mistaken for a correct system.

## References

- Claude E. Shannon, [*A Symbolic Analysis of Relay and Switching Circuits*](https://doi.org/10.1109/EE.1938.6431064), *Transactions of the American Institute of Electrical Engineers* 57(12), 1938. Primary correspondence between Boolean algebra and switching-network analysis and synthesis.
- W. V. Quine, [*The Problem of Simplifying Truth Functions*](https://doi.org/10.1080/00029890.1952.11988183), *American Mathematical Monthly* 59(8), 1952. Primary systematic Boolean minimization work.
- E. J. McCluskey Jr., [*Minimization of Boolean Functions*](https://doi.org/10.1002/j.1538-7305.1956.tb03835.x), *Bell System Technical Journal* 35(6), 1956. Primary tabular minimum-sum-of-products method, including don't-care terms.
- IEEE, [*IEEE/ANSI 91a-1991 — Standard Graphic Symbols for Logic Functions*](https://standards.ieee.org/standard/91a-1991.html), official standard record checked 2026-08-29. Logic-function descriptions, symbols, and representation conventions; the record identifies its historical status.
- IEEE, [*IEEE 1800-2023 — SystemVerilog Unified Hardware Design, Specification, and Verification Language*](https://standards.ieee.org/ieee/1800/7743/), active standard published 2024. Current official language semantics for behavioral, RTL, gate-level, testbench, assertion, and coverage models.
- Sarah L. Harris and David Money Harris, [*Digital Design and Computer Architecture: RISC-V Edition*](https://www.sciencedirect.com/book/9780128200643/digital-design-and-computer-architecture), Morgan Kaufmann, 2021. Digital logic, combinational/sequential circuits, HDL, and processor construction.
- Neil H. E. Weste and David Money Harris, [*CMOS VLSI Design: A Circuits and Systems Perspective*, fourth edition](https://www.pearson.com/en-us/subject-catalog/p/cmos-vlsi-design-a-circuits-and-systems-perspective/P200000003427/9780321547743), Pearson, current publisher record checked 2026-08-29. Physical implementation, delay, power, and circuit-level limits beyond ideal Boolean gates.
- Noam Nisan and Shimon Schocken, [*From Nand to Tetris*](https://www.nand2tetris.org/), official course and project site checked 2026-08-29. Constructive progression from NAND-based logic through a computer system.

## Exercises

### Exercise 1

For \(f(a,b,c)=1\) on minterms `001`, `010`, `100`, and `111`, write canonical sum of products, identify the familiar function, and give its complete output table in row order `000` through `111`.

### Exercise 2

Prove algebraically and by a four-row truth table that \(\lnot(a\lor b)=\lnot a\land\lnot b\). Then describe a NAND-only construction for the right-hand side.

### Exercise 3

Specify a 4-to-1 multiplexer with data inputs \(d_0\ldots d_3\) and select bits \(s_1s_0\). Give its Boolean expression, state a decisive exhaustive test size, and name three physical properties that test does not establish.

### Exercise 4

A designer simplifies a 4-bit BCD validity detector by treating inputs 10–15 as don't-cares because “software never sends them.” Review the assumption and propose a verification plan that covers normal, reset, fault, and future-interface behavior.

### Exercise 5

A railway crossing controller proposes combinational logic that lowers a barrier when either of two track sensors reports an approaching train and raises it when both report clear. Define the Boolean evidence, fault evidence, timing evidence, system evidence, and named human-review roles required before any field use. Do not assume the two sensors fail independently.

## Answers to the Exercises

### Answer 1

The canonical expression is \((\lnot a\land\lnot b\land c)\lor(\lnot a\land b\land\lnot c)\lor(a\land\lnot b\land\lnot c)\lor(a\land b\land c)\). It is three-input odd parity, \(a\oplus b\oplus c\). In row order `000,001,010,011,100,101,110,111`, outputs are `0,1,1,0,1,0,0,1`. The familiar name is justified by all rows, not just the four on-set examples.

### Answer 2

Starting from the right, if either input is 1 then its complement is 0, so the conjunction is 0; if both inputs are 0, both complements are 1, so the conjunction is 1. The rows `(a,b): left,right` are `00:1,1`, `01:0,0`, `10:0,0`, `11:0,0`. For NAND only, make \(\lnot a\) as `NAND(a,a)` and \(\lnot b\) similarly; NAND those terms, then NAND that intermediate with itself to recover their AND. Four NAND gates suffice in this direct construction.

### Answer 3

The expression is \(y=(\lnot s_1\land\lnot s_0\land d_0)\lor(\lnot s_1\land s_0\land d_1)\lor(s_1\land\lnot s_0\land d_2)\lor(s_1\land s_0\land d_3)\). There are six binary inputs, so an exhaustive two-valued test has \(2^6=64\) vectors and asserts that `y` equals the selected data bit for each. It does not establish propagation delay, glitches while selects change, electrical loading, energy, four-state behavior, or implementation faults; any three suffice.

### Answer 4

The claim “software never sends them” is neither an interface guarantee nor a fault model. Invalid patterns may occur during reset, partial update, corruption, test, hardware defect, malicious input, or later reuse. First define whether the detector output for 10–15 must be false, diagnostic, fail-safe, or truly irrelevant, and name the authority for that choice. Exhaustively compare the reference and implementation over all 16 stable patterns; test reset and transition behavior with appropriate temporal/electrical models; inject stuck-at, transient, and interface faults; check the producer contract and versioning; and preserve an assertion for invalid input. Only then may synthesis use don't-cares within the approved care set.

### Answer 5

The stable Boolean table must define every combination of both sensors, manual override, maintenance state, barrier-position feedback, and any explicit fault indicators; a simplistic two-input OR is inadequate unless the bounded system specification proves those are the only relevant inputs. Independently derive and exhaustively compare the implementation, preserving active-low polarity and fail-safe output behavior. Fault evidence must address stuck-clear, stuck-occupied, intermittent, common power/cable/environment failures, disagreement, voter/controller failure, diagnostic coverage, degraded modes, and repair. Timing evidence must cover detection distance, train speed, worst-case processing and actuation, barrier motion, signal transitions, hazards, power loss, and deadline margins. System evidence must include track layout, road users, human behavior, emergency access, communications, alarms, operations, maintenance, cybersecurity, environmental qualification, installation, inspection, incident response, and regulated acceptance testing. Named reviewers must include railway signaling and rolling-stock domain engineers, functional-safety and hazard-analysis authorities, electrical/electronic and embedded engineers, civil/road interface experts, human-factors and accessibility specialists, operations and dispatch, maintainers, cybersecurity, quality/configuration management, regulator or authorized assessor, emergency services, affected operator representatives, and independent safety assurance. This chapter supplies none of the required field authorization or external review.
