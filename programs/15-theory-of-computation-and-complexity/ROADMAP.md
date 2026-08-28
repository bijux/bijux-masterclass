# 15. Theory of Computation & Complexity

**Program code:** `TOCC`

**Purpose:** Develop rigorous understanding of formal languages, computability, reductions, resource-bounded computation, and the structural limits of efficient algorithms.

**Level-II professional outcome:** Ready for graduate algorithms, cryptography, formal languages, complexity research, and principled reasoning about what software can and cannot compute efficiently.

**Prerequisites:** discrete mathematics; proof techniques; algorithms and asymptotic analysis.

**Primary ownership:** automata and formal languages; computability and undecidability; reductions; time and space complexity; NP-completeness; randomized complexity; approximation hardness; parameterized and fine-grained complexity; circuit and communication complexity; interactive and quantum complexity foundations.

**Explicit exclusions:** algorithm implementation and empirical performance (Program 16); program semantics and proof systems (Program 07); compiler construction (Program 08).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Formal Languages and Computational Models

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Alphabets, Strings, Languages, and Decision Problems** | `001-alphabets-strings-languages-and-decision-problems.md` |
| 002 | **Machines, Recognizers, Deciders, and Transducers** | `002-machines-recognizers-deciders-and-transducers.md` |
| 003 | **Encodings and Effective Representations** | `003-encodings-and-effective-representations.md` |
| 004 | **Closure Properties as a Reasoning Tool** | `004-closure-properties-as-a-reasoning-tool.md` |
| 005 | **Proof Techniques for Language Classes** | `005-proof-techniques-for-language-classes.md` |
| 006 | **Countability and Diagonal Arguments** | `006-countability-and-diagonal-arguments.md` |
| 007 | **Universal Machines and Simulation** | `007-universal-machines-and-simulation.md` |
| 008 | **Reductions as Transformations Between Problems** | `008-reductions-as-transformations-between-problems.md` |
| 009 | **Robustness Across Reasonable Machine Models** | `009-robustness-across-reasonable-machine-models.md` |
| 010 | **Classifying a New Computational Problem Precisely** | `010-classifying-a-new-computational-problem-precisely.md` |

### Block 02 — Finite Automata and Regular Languages

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Deterministic Finite Automata** | `011-deterministic-finite-automata.md` |
| 012 | **Nondeterministic Finite Automata** | `012-nondeterministic-finite-automata.md` |
| 013 | **Equivalence of Determinism and Nondeterminism** | `013-equivalence-of-determinism-and-nondeterminism.md` |
| 014 | **Regular Expressions** | `014-regular-expressions.md` |
| 015 | **Automata-Expression Conversions** | `015-automata-expression-conversions.md` |
| 016 | **Closure Properties of Regular Languages** | `016-closure-properties-of-regular-languages.md` |
| 017 | **The Pumping Lemma for Regular Languages** | `017-the-pumping-lemma-for-regular-languages.md` |
| 018 | **Myhill-Nerode Equivalence** | `018-myhill-nerode-equivalence.md` |
| 019 | **State Minimization** | `019-state-minimization.md` |
| 020 | **Limits and Practical Uses of Finite-State Models** | `020-limits-and-practical-uses-of-finite-state-models.md` |

### Block 03 — Context-Free Languages and Pushdown Automata

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Context-Free Grammar Language Class** | `021-context-free-grammar-language-class.md` |
| 022 | **Derivations and Parse Trees** | `022-derivations-and-parse-trees.md` |
| 023 | **Ambiguity** | `023-ambiguity.md` |
| 024 | **Normal Forms** | `024-normal-forms.md` |
| 025 | **Pushdown Automata** | `025-pushdown-automata.md` |
| 026 | **Equivalence of Grammars and Pushdown Automata** | `026-equivalence-of-grammars-and-pushdown-automata.md` |
| 027 | **Closure Properties of Context-Free Languages** | `027-closure-properties-of-context-free-languages.md` |
| 028 | **The Pumping Lemma for Context-Free Languages** | `028-the-pumping-lemma-for-context-free-languages.md` |
| 029 | **Deterministic Context-Free Languages** | `029-deterministic-context-free-languages.md` |
| 030 | **Decidability Questions for Grammars** | `030-decidability-questions-for-grammars.md` |

### Block 04 — Computability and Undecidability

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Turing Machines** | `031-turing-machines.md` |
| 032 | **Multitape, Nondeterministic, and Enumerator Models** | `032-multitape-nondeterministic-and-enumerator-models.md` |
| 033 | **Church-Turing Thesis** | `033-church-turing-thesis.md` |
| 034 | **Decidable and Recognizable Languages** | `034-decidable-and-recognizable-languages.md` |
| 035 | **Mapping Reductions** | `035-mapping-reductions.md` |
| 036 | **The Halting Problem** | `036-the-halting-problem.md` |
| 037 | **Rice's Theorem** | `037-rice-s-theorem.md` |
| 038 | **Post Correspondence Problem** | `038-post-correspondence-problem.md` |
| 039 | **Undecidable Properties of Grammars and Programs** | `039-undecidable-properties-of-grammars-and-programs.md` |
| 040 | **Proving Undecidability Without Hand-Waving** | `040-proving-undecidability-without-hand-waving.md` |

### Block 05 — Time Complexity and NP-Completeness

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Time Complexity and Polynomial Robustness** | `041-time-complexity-and-polynomial-robustness.md` |
| 042 | **Class P** | `042-class-p.md` |
| 043 | **Verification and Class NP** | `043-verification-and-class-np.md` |
| 044 | **Polynomial-Time Many-One Reductions** | `044-polynomial-time-many-one-reductions.md` |
| 045 | **Cook-Levin Theorem Structure** | `045-cook-levin-theorem-structure.md` |
| 046 | **SAT and 3SAT** | `046-sat-and-3sat.md` |
| 047 | **Clique, Independent Set, and Vertex Cover** | `047-clique-independent-set-and-vertex-cover.md` |
| 048 | **Hamiltonian Path and Traveling Salesperson** | `048-hamiltonian-path-and-traveling-salesperson.md` |
| 049 | **Subset Sum and Partition** | `049-subset-sum-and-partition.md` |
| 050 | **Designing a Correct NP-Completeness Proof** | `050-designing-a-correct-np-completeness-proof.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Space, Hierarchies, and Completeness

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Space Complexity** | `051-space-complexity.md` |
| 052 | **PSPACE and Polynomial-Space Computation** | `052-pspace-and-polynomial-space-computation.md` |
| 053 | **Savitch's Theorem** | `053-savitch-s-theorem.md` |
| 054 | **PSPACE-Complete Problems** | `054-pspace-complete-problems.md` |
| 055 | **Logarithmic Space and Class L** | `055-logarithmic-space-and-class-l.md` |
| 056 | **NL and Reachability** | `056-nl-and-reachability.md` |
| 057 | **Time Hierarchy Theorem** | `057-time-hierarchy-theorem.md` |
| 058 | **Space Hierarchy Theorem** | `058-space-hierarchy-theorem.md` |
| 059 | **Complete Problems and Structural Insight** | `059-complete-problems-and-structural-insight.md` |
| 060 | **Relativization and Barriers to Separation Proofs** | `060-relativization-and-barriers-to-separation-proofs.md` |

### Block 07 — Randomized and Counting Complexity

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Randomized Turing Machines** | `061-randomized-turing-machines.md` |
| 062 | **RP, coRP, and ZPP** | `062-rp-corp-and-zpp.md` |
| 063 | **BPP and Error Amplification** | `063-bpp-and-error-amplification.md` |
| 064 | **Randomized Reductions** | `064-randomized-reductions.md` |
| 065 | **Pairwise Independence and Limited Randomness** | `065-pairwise-independence-and-limited-randomness.md` |
| 066 | **Derandomization and Pseudorandom Generators** | `066-derandomization-and-pseudorandom-generators.md` |
| 067 | **Counting Class #P** | `067-counting-class-p.md` |
| 068 | **#P-Completeness** | `068-p-completeness.md` |
| 069 | **Approximate Counting** | `069-approximate-counting.md` |
| 070 | **Connections Between Counting, Sampling, and Decision** | `070-connections-between-counting-sampling-and-decision.md` |

### Block 08 — Approximation and Hardness

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Optimization Problems and Approximation Ratios** | `071-optimization-problems-and-approximation-ratios.md` |
| 072 | **Approximation-Preserving Reductions** | `072-approximation-preserving-reductions.md` |
| 073 | **Polynomial-Time Approximation Schemes** | `073-polynomial-time-approximation-schemes.md` |
| 074 | **Hardness of Approximation** | `074-hardness-of-approximation.md` |
| 075 | **Probabilistically Checkable Proofs** | `075-probabilistically-checkable-proofs.md` |
| 076 | **Gap Reductions** | `076-gap-reductions.md` |
| 077 | **MAX-SAT and Constraint Satisfaction** | `077-max-sat-and-constraint-satisfaction.md` |
| 078 | **Set Cover Hardness** | `078-set-cover-hardness.md` |
| 079 | **Unique Games Perspective** | `079-unique-games-perspective.md` |
| 080 | **Recognizing When Approximation Is the Right Complexity Response** | `080-recognizing-when-approximation-is-the-right-complexity-response.md` |

### Block 09 — Parameterized and Fine-Grained Complexity

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Parameterized Problems and Fixed-Parameter Tractability** | `081-parameterized-problems-and-fixed-parameter-tractability.md` |
| 082 | **Kernelization** | `082-kernelization.md` |
| 083 | **Bounded Search Trees** | `083-bounded-search-trees.md` |
| 084 | **Class W[1] and Parameterized Hardness** | `084-class-w-1-and-parameterized-hardness.md` |
| 085 | **Parameterized Reductions** | `085-parameterized-reductions.md` |
| 086 | **Exponential Time Hypothesis** | `086-exponential-time-hypothesis.md` |
| 087 | **Strong Exponential Time Hypothesis** | `087-strong-exponential-time-hypothesis.md` |
| 088 | **Fine-Grained Reductions** | `088-fine-grained-reductions.md` |
| 089 | **Conditional Lower Bounds for Classic Problems** | `089-conditional-lower-bounds-for-classic-problems.md` |
| 090 | **Choosing Parameters That Reveal Hidden Tractability** | `090-choosing-parameters-that-reveal-hidden-tractability.md` |

### Block 10 — Alternative Complexity Models

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Circuit Families and Circuit Size** | `091-circuit-families-and-circuit-size.md` |
| 092 | **Class P/poly and Advice** | `092-class-p-poly-and-advice.md` |
| 093 | **Circuit Lower-Bound Questions** | `093-circuit-lower-bound-questions.md` |
| 094 | **Communication Complexity** | `094-communication-complexity.md` |
| 095 | **Deterministic and Randomized Communication** | `095-deterministic-and-randomized-communication.md` |
| 096 | **Interactive Proof Systems** | `096-interactive-proof-systems.md` |
| 097 | **IP, AM, and the Power of Interaction** | `097-ip-am-and-the-power-of-interaction.md` |
| 098 | **Zero-Knowledge Proofs as a Complexity Concept** | `098-zero-knowledge-proofs-as-a-complexity-concept.md` |
| 099 | **Quantum Computation and Class BQP** | `099-quantum-computation-and-class-bqp.md` |
| 100 | **Mapping the Major Complexity Classes and Open Boundaries** | `100-mapping-the-major-complexity-classes-and-open-boundaries.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
