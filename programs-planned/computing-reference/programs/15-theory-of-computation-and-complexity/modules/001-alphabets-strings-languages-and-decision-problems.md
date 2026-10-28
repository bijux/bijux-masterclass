---
module_id: TOCC-001
program: Theory of Computation & Complexity
level: 1
module_number: 1
title: Alphabets, Strings, Languages, and Decision Problems
status: complete
last_verified: 2026-08-28
---

# Alphabets, Strings, Languages, and Decision Problems

## One-Page Review

### Governing question

How do finite symbolic encodings turn open-ended computational questions into precise membership problems that a mathematical machine can accept or reject?

### Essential definitions

- An **alphabet** (Σ) is a finite, nonempty set of symbols.
- A **string** over (Σ) is a finite sequence of symbols from (Σ).
- The **empty string** (ε) is the unique string of length zero.
- (Σ^n) is the set of strings of length exactly (n); (Σ^* = ⋃_{n≥ 0}Σ^n); (Σ^+ = ⋃_{n≥ 1}Σ^n).
- A **language** over (Σ) is any set (L ⊆ Σ^*).
- A **decision problem** asks a yes/no question for each valid instance. After an encoding, its yes-instances form a language.
- An **encoding** maps mathematical or real objects to finite strings. It must make instance boundaries and validity decidable before complexity claims are meaningful.

### Central model, mechanism, or theorem

Choose an alphabet and an encoding (e : X → Σ^*) for instances (X). For a predicate (P : X → \{0,1\}), define

$$
L_{P,e}=\{e(x)∣ x∈ X ∧ P(x)=1\}.
$$

A decider for the problem is a machine that halts on every input string and answers yes exactly for strings in (L_{P,e}), while also applying a declared policy to malformed encodings.

### Critical invariants

- Strings are finite even when a language is infinite.
- (ε ∈ Σ^*) for every alphabet; (ε), ({ε\}), and (∅) are different objects.
- Concatenation has identity (ε) and is associative, but is generally not commutative.
- Complement is relative to a stated universe, normally (Σ^*).
- A decision problem is not its English name: the instance set, encoding, predicate, and malformed-input policy determine the language.
- Complexity is measured against encoding length (|e(x)|), not an informal notion of object size.

### Common failures

Typical errors are confusing a symbol with a one-symbol string, confusing the empty string with the empty language, allowing infinite strings into (Σ^*), taking a complement without fixing (Σ), using an ambiguous encoding, hiding a promise on inputs, and comparing running times under exponentially different encodings.

### Compact example

Let (Σ=\{0,1\}) and (L=\{w∈Σ^*∣ w contains exactly two 1s\}). Then `101`, `110`, and `00100` are in (L); `10`, `111`, and (ε) are not. (L) is infinite because zeros can be inserted without bound, but every member is finite. Membership for a string (w) is decided by scanning it once and testing whether the count of `1` is two.

### Connections

The prerequisite is the [curriculum's mathematical and programming foundation](../../../DEPENDENCY_AND_SEQUENCE.md). [TOCC-002](../ROADMAP.md) develops operations and closure properties of languages. Formal syntax connects to the [Programming Languages & Semantics roadmap](../../01-programming-languages-and-semantics/ROADMAP.md); concrete algorithm specifications connect to [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md).

## Governing Question

What must be fixed before “an algorithm solves a problem” becomes a mathematical proposition rather than an informal claim?

We need a set of instances, a finite representation for each instance, a yes/no predicate, and a convention for invalid representations. This reduction to language membership is foundational because machine models consume finite descriptions. The same abstraction later lets us compare automata, define decidability, construct reductions, and measure resources independently of a particular programming language.

The current ACM/IEEE-CS/AAAI CS2023 report treats algorithms, complexity, and computability as common algorithmic foundations and emphasizes capabilities and limitations independent of programming language or hardware ([CS2023 final report](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm)). This chapter supplies the notation on which that study rests; it does not yet classify languages by machine power.

## Why This Matters

An informal problem can change when its representation changes. “Is this integer prime?” seems unambiguous, yet a unary encoding `11111` and binary encoding `101` represent the same integer 5 with lengths 5 and 3. An algorithm polynomial in the numeric value may be exponential in binary input length. Complexity statements therefore require encodings.

Language notation also separates data from judgment. A graph, formula, program, or protocol trace becomes a finite string. The language contains precisely the encodings judged positive. Stanford's overview of complexity uses this standard view: a decision problem corresponds to a set, and mathematical instances are mapped to finite binary strings before a reference machine is applied ([Computational Complexity Theory](https://plato.stanford.edu/archives/sum2024/entries/computational-complexity/)).

Finally, elementary distinctions prevent later proof failures. If (ε) is mistaken for (∅), base cases in induction and automata constructions fail. If complement lacks a universe, closure statements are ill-typed. If encodings are ambiguous, one string may denote multiple instances, so membership no longer answers a unique question.

## Prerequisites and Retrieval

You should be comfortable with finite sets, subsets, unions, functions, sequences, predicates, induction on natural numbers, and basic asymptotic reasoning. Retrieve these facts:

1. A set is determined by membership, not order or repetition.
2. A sequence has order and may repeat elements.
3. (A⊆ B) means every member of (A) is a member of (B).
4. A function assigns exactly one output to each input in its domain; an injective function never maps two domain elements to one codomain element.
5. A proof by induction requires a base case and a step from (n) to (n+1).

No previous automata theory is assumed. The module deliberately distinguishes mathematical strings from programming-language string objects, whose finite memory, encoding format, and APIs add implementation concerns.

## Learning Objectives

After completing this module, you should be able to:

- define alphabets, strings, length, concatenation, powers, star, plus, and languages without type confusion;
- derive elementary identities involving (Σ^n), (Σ^*), and concatenation;
- distinguish empty-string, empty-language, and singleton-language boundary cases;
- represent a yes/no predicate as a language under an explicit encoding;
- evaluate whether an encoding is total, injective, unambiguous, and efficiently decodable;
- explain how encoding length affects a complexity claim;
- distinguish decision, search, optimization, counting, and promise formulations;
- specify how malformed strings are handled.

## Core Exposition

An **alphabet** is a finite nonempty set of atomic symbols for the model. Symbols need not be characters. A token such as `IDENTIFIER` can be one symbol in a parser alphabet; a DNA model may use ({A,C,G,T}); binary theory normally uses ({0,1}). “Atomic” is relative to the abstraction: a Unicode character may occupy multiple bytes, while a byte may be treated as one of 256 symbols.

A **string** is a finite sequence. If (w=a_1a_2⋯a_n), then its length is (|w|=n). The empty sequence is (ε), with (|ε|=0). A symbol (a∈Σ) and the length-one string (a∈Σ^1) are conventionally written alike, but their mathematical types differ.

For strings (x=a_1⋯a_m) and (y=b_1⋯b_n), concatenation is (xy=a_1⋯a_mb_1⋯b_n). Thus (|xy|=|x|+|y|), (εx=xε=x), and ((xy)z=x(yz)). In general (xy≠yx): with (x=01) and (y=1), (xy=011) while (yx=101).

Define powers of an alphabet by length:

$$
Σ^0=\{ε\},\qquad
Σ^n=\{w∣ w\text{ is a string over }Σ\text{ and }|w|=n\}.
$$

Then (Σ^*=⋃_{n=0}^{∞}Σ^n) and (Σ^+=⋃_{n=1}^{∞}Σ^n=Σ^*∖\{ε\}). The star contains strings of every finite length, not infinite sequences. If (|Σ|=k), then (|Σ^n|=k^n): each of (n) positions has (k) independent choices.

A **language** is simply a subset of (Σ^*). It need not be grammatical, computable, finite, or useful. Examples over ({0,1}) include the empty language, the language containing only (ε), all strings, palindromes, valid encodings of prime numbers, and languages no algorithm can decide. Later machine models induce important language classes; “language” itself imposes no such restriction.

Set operations apply after the common universe is fixed. For (L,K⊆Σ^*), union and intersection have their usual meanings. Complement is (L̅=Σ^*∖ L). Language concatenation is (LK=\{xy∣ x∈ L,y∈ K\}). Language powers use (L^0=\{ε\}) and (L^{n+1}=L^nL); Kleene star is (L^*=⋃_{n≥0}L^n). Alphabet star and language star share notation but apply to different types.

A decision problem begins with instances (X) and predicate (P). Machines require finite inputs, so select an encoding. Desirable properties include:

- **totality on intended instances:** every (x∈ X) has a representation;
- **unambiguity:** each accepted encoding denotes at most one intended instance;
- **effective validity:** malformed strings can be recognized;
- **effective decoding:** represented structure can be recovered;
- **reasonable size:** encoding does not hide exponential expansion;
- **canonicality or an equivalence policy:** multiple encodings of one instance are either prevented or treated consistently.

An encoding need not be unique to be usable. Graphs can have many vertex orderings. The language must then include every valid encoding of a positive instance, or define canonicalization. What matters is that representation choices are explicit and computationally controlled.

## Definitions and Notation

For an alphabet (Σ):

- (Σ^0=\{ε\}).
- (Σ^{n+1}=Σ^nΣ), where set concatenation is intended.
- (Σ^*=⋃_{n∈ℕ}Σ^n).
- (Σ^+=Σ^*∖\{ε\}).
- (w^0=ε) and (w^{n+1}=w^nw) for a string (w).
- (w^R) is the reversal of (w).
- (x≼ w) means (x) is a prefix of (w): there exists (y) with (w=xy).
- A language is (L⊆Σ^*); its characteristic predicate is (χ_L(w)=1) exactly when (w∈ L).

The three empty-looking objects have different types and membership:

| Object | Type | Cardinality | Does it contain (ε)? |
|---|---|---:|---|
| (ε) | string | length 0 | not a set-membership question |
| ({ε\}) | language | 1 | yes |
| (∅) | language | 0 | no |

For a decision problem, write (e:X→Σ^*) for encoding and (L_{P,e}=\{e(x):P(x)\}). If malformed strings are rejected, a total decider (D:Σ^*→\{0,1\}) satisfies (D(w)=1⇔ w∈ L_{P,e}).

## Mechanisms, Invariants, or Proof Structure

Several elementary results will recur throughout the program.

**Length homomorphism.** For all strings (x,y), (|xy|=|x|+|y|). This follows directly from sequence concatenation: the result contains all (|x|) positions followed by all (|y|) positions.

**Associativity.** For all (x,y,z), ((xy)z=x(yz)). Both sides yield the same ordered sequence of symbols: first those of (x), then (y), then (z). Parentheses describe construction, not a symbol in the result.

**Counting fixed-length strings.** If (|Σ|=k), then (|Σ^n|=k^n). Proof by induction: for (n=0), (Σ^0=\{ε\}) has (1=k^0) member, including when (k>0). If (Σ^n) has (k^n) strings, appending one of (k) symbols uniquely produces every string of length (n+1), so the count is (k^n k=k^{n+1}).

**Unique length partition.** The sets (Σ^m) and (Σ^n) are disjoint when (m≠ n), because a string has one length. Therefore (Σ^*) is a disjoint countable union of finite sets. It is countably infinite whenever (Σ) is nonempty.

**Decision-language correspondence.** Once a valid encoding policy is fixed, every predicate determines a language of yes-encodings, and membership in that language recovers the decision answer. This is definitional, not a computability theorem: the resulting language may be undecidable.

Proof review must preserve types. A step such as “(ε⊆ L)” is ill-typed because a string is not a set. A step using (L̅) must name (Σ^*). A complexity proof must express bounds in (|e(x)|).

## Alternatives and Trade-Offs

**Binary versus larger alphabets.** Any fixed finite alphabet with at least two symbols can be encoded in binary with constant-factor expansion. Binary is convenient for machine-independent theory, while richer alphabets improve readability. The translation argument must include delimiters or fixed-width codes.

**Canonical versus redundant encodings.** Canonical encodings simplify equality and language definition. Redundant encodings may be natural and cheaper to produce. If redundancy is allowed, algorithms must be representation-invariant or state otherwise.

**Self-delimiting versus externally framed encodings.** A self-delimiting representation can be concatenated and decoded without out-of-band lengths, at the cost of overhead. An externally framed input can be simpler but relies on a separate boundary convention.

**Decision versus search.** Decision asks whether a witness exists; search asks for one. They are different problem types even when reductions later connect them. Converting search to repeated decision calls may require self-reducibility and can change resource bounds.

**Total decision problems versus promise problems.** A promise problem specifies yes- and no-instances only inside a promised subset; behavior outside is unconstrained. Hiding a promise inside prose makes a purported decider impossible to assess. This chapter uses total languages unless it explicitly says otherwise.

**Mathematical versus implementation strings.** Mathematical strings are unbounded in potential length but individually finite. Program strings are bounded by address space and APIs and represented by bytes or code units. Implementation experiments illustrate definitions; they do not redefine them.

## Failure Modes and Misconceptions

1. (Σ^0=∅). False: (Σ^0=\{ε\}), which supplies the identity needed by concatenation and induction.
2. (ε=∅). False: one is a string and the other a set.
3. Every language is infinite because (Σ^*) is infinite. False: languages are arbitrary subsets, including finite and empty ones.
4. Members of (Σ^*) may be infinite strings. False: star contains all finite strings.
5. Concatenation is commutative because set union is. False: string order matters, and language concatenation is generally noncommutative.
6. Complement is intrinsic to (L). False: it depends on the ambient alphabet and universe.
7. A parser for valid instances solves the decision problem. False: validity and the yes/no predicate are separate.
8. Multiple encodings automatically invalidate a problem. False: they require a consistent policy, not necessarily canonicalization.
9. Polynomial in numeric value means polynomial time. Not under binary encoding; input length is logarithmic in value.
10. Writing a set of yes-instances proves decidability. False: some precisely defined languages have no decider.

## Worked Examples

### Example 1

**Question:** With (Σ=\{a,b\}), which of `abba`, `abc`, and (ε) are strings over (Σ)?

**Reasoning:** Every symbol in `abba` belongs to (Σ), so `abba` is in (Σ^4⊆Σ^*). `abc` contains `c`, which is not in the alphabet, so it is not a string over this (Σ). The empty string contains no offending symbol and belongs to (Σ^0).

**Conclusion:** Alphabet membership constrains symbols, not minimum length; `abba` and (ε) qualify.

### Example 2

**Question:** Compare (L_1=∅), (L_2=\{ε\}), and (L_3=\{0\}).

**Reasoning:** Their cardinalities are 0, 1, and 1. Only (L_2) contains the empty string. (L_2L_3=\{0\}) because (ε 0=0), while (L_1L_3=∅) because no left operand can be selected. Also (L_1^*=\{ε\}): the zero-fold concatenation contributes (ε), and all positive powers are empty.

**Conclusion:** Empty language, singleton empty-string language, and singleton one-symbol language behave differently under concatenation and star.

### Example 3

**Question:** Show that concatenation is not commutative.

**Reasoning:** Choose (x=01) and (y=1). Then (xy=011), whereas (yx=101). One counterexample refutes the universal claim (xy=yx). Associativity is not contradicted: with any (z), parentheses do not change symbol order.

**Conclusion:** Concatenation is associative with identity (ε), but it is not generally commutative.

### Example 4

**Question:** Enumerate (Σ^0,Σ^1,Σ^2) for (Σ=\{0,1\}) and check their cardinalities.

**Reasoning:** The expected sizes are (2^0=1), (2^1=2), and (2^2=4). The executable enumeration uses a Cartesian product and represents (ε) as an empty host-language string.

<!-- bijux-verify: {"id":"binary-string-powers","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"0: ['ε'] size=1\n1: ['0', '1'] size=2\n2: ['00', '01', '10', '11'] size=4\n","stderr":""}} -->
```python
from itertools import product

alphabet = ("0", "1")
for length in range(3):
    strings = ["".join(symbols) for symbols in product(alphabet, repeat=length)]
    shown = [value or "ε" for value in strings]
    print(f"{length}: {shown} size={len(strings)}")
```

**Conclusion:** Enumeration matches (2^n), including the essential (n=0) base case.

### Example 5

**Question:** Why must complement name its alphabet?

**Reasoning:** Let (L=\{0\}). Over (Σ_1=\{0\}), its complement contains (ε,00,000,…) but not strings containing `1`, because those are outside (Σ_1^*). Over (Σ_2=\{0,1\}), the complement also contains `1`, `01`, and every other binary string except `0`.

**Conclusion:** The same displayed set (L) has different complements in different universes.

### Example 6

**Question:** Is ordinary decimal notation an injective encoding of natural numbers?

**Reasoning:** If leading zeros are allowed, `5`, `05`, and `005` denote the same number, so the encoding relation is not canonical and a function from strings to values is many-to-one. We can prohibit leading zeros except for `0`, or accept all forms and require membership to be invariant under them. An empty string and a plus sign also need policies.

**Conclusion:** Redundancy is manageable only when validity and equivalence are explicit.

### Example 7

**Question:** Encode the decision problem “Does an undirected graph contain an edge?”

**Reasoning:** One scheme numbers (n) vertices and records the upper-triangular adjacency bits after a self-delimiting encoding of (n). Validity checks the prefix and expects exactly (n(n-1)/2) bits. The language contains valid encodings whose adjacency portion contains at least one `1`. Malformed lengths are rejected. Different vertex numberings may encode isomorphic graphs differently, but the predicate is invariant.

**Conclusion:** A decision-language definition includes structural validity, not only the final predicate.

### Example 8

**Question:** Is (Σ^*) finite when (Σ=\{a\})?

**Reasoning:** For each (n≥0), there is exactly one string (a^n). These strings have distinct lengths, so there are infinitely many. They can be listed as (ε,a,aa,aaa,…), proving countability. No member is infinite.

**Conclusion:** A one-symbol nonempty alphabet yields a countably infinite star of individually finite strings.

### Example 9

**Question:** Express primality as a language and identify the encoding-size issue.

**Reasoning:** Under canonical binary encoding, (L_{prime}=\{bin(n)∣ n≥2 and n is prime\}). The integer (n) has input length (⌊log₂ n⌋+1). Trial division through (√n) takes exponentially many steps as a function of bit length in the worst case, even though it is sublinear in numeric value. Malformed strings and leading zeros require a policy.

**Conclusion:** Complexity attaches to representation length; numeric magnitude is not input length.

### Example 10

**Question:** Distinguish decision, search, optimization, and counting versions of a path problem.

**Reasoning:** Decision asks whether an (s)-to-(t) path of length at most (k) exists. Search asks for such a path. Optimization asks for a shortest path. Counting asks how many qualifying paths exist, under a convention preventing infinite repetition. These share instance data but have different outputs and evidence. A yes/no language directly represents only the decision version; other versions need function or relation formulations, though decision procedures may be used as subroutines.

**Conclusion:** Reducing theory to languages is powerful, but the reduction must not erase the original task type.

## Cross-Program Connections

- **Programming Languages & Semantics:** source programs are strings in syntactic languages; meaning requires an additional semantic relation.
- **Compilers:** lexical tokens, parse trees, and accepted source texts refine alphabet and language ideas into implementation pipelines.
- **Algorithm Engineering:** precise inputs, outputs, validity, and constraints precede algorithm selection and performance measurement.
- **Data Structures:** encodings realize abstract objects with concrete representations whose size affects cost.
- **Security Engineering:** parsers operate on adversarial strings; ambiguity and noncanonical representations create validation and signature risks.
- **API Engineering:** wire formats require framing and validity rules before a message can carry a well-defined request.

## References

- Michael Sipser. [*Introduction to the Theory of Computation*, 3rd ed.](https://www.cengage.com/c/introduction-to-the-theory-of-computation-3e-sipser/9781133187790/) Cengage, published 2012, copyright 2013, ISBN 9781133187790. Publisher record checked 2026-08-28.
- John E. Hopcroft, Rajeev Motwani, and Jeffrey D. Ullman. [*Introduction to Automata Theory, Languages, and Computation*, 3rd ed.](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-automata-theory-languages-and-computation/P200000003517). Pearson, 2006/2007. Publisher record checked 2026-08-28.
- Amruth N. Kumar et al. [*Computer Science Curricula 2023*](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm). ACM, IEEE Computer Society, and AAAI, DOI 10.1145/3664191; endorsed 2024. Current report checked 2026-08-28.
- Walter Dean. [“Computability and Complexity.”](https://plato.stanford.edu/entries/computability/) *Stanford Encyclopedia of Philosophy*, first published 2004, substantive revision 2021. Record checked 2026-08-28.
- Walter Dean. [“Computational Complexity Theory.”](https://plato.stanford.edu/archives/sum2024/entries/computational-complexity/) *Stanford Encyclopedia of Philosophy*, Summer 2024 archive. Checked 2026-08-28.

## Exercises

### Exercise 1

Let (Σ=\{x,y\}). List (Σ^0,Σ^1,Σ^2). State whether each of (ε), `xyx`, (∅), and ({xyx\}) is a string, a language, both, or neither under the typed definitions.

### Exercise 2

Prove by induction that (|w^n|=n|w|) for every string (w) and natural number (n). Include the (n=0) case and identify the concatenation fact used in the step.

### Exercise 3

Design an unambiguous binary encoding for a pair of binary strings ((x,y)). Give an algorithm to decode it, analyze encoding length, and show why naive concatenation (xy) is ambiguous.

### Exercise 4

Compare canonical binary and unary encodings of positive integers for the decision problem “is (n) a perfect square?” Explain how an (O(n))-time numeric algorithm appears under each input-length measure and why this does not change the mathematical yes-instances.

### Exercise 5

Define a decision-language formulation for detecting whether a finite schedule contains overlapping intervals. Specify valid instances, encoding, endpoint convention, yes predicate, malformed-input policy, and one boundary case. Then state the related search problem without pretending it has a yes/no output.

## Answers to the Exercises

### Answer 1

(Σ^0=\{ε\}), (Σ^1=\{x,y\}), and (Σ^2=\{xx,xy,yx,yy\}). The object (ε) is a string, as is `xyx`; neither is a language under the strict typed presentation because neither is a set of strings. The empty set (∅) is a language and not a string. The singleton ({xyx\}) is a language and not a string. Informal notation can overload these types, but a proof must preserve them.

### Answer 2

Base case: (w^0=ε), so (|w^0|=0=0|w|). Inductive hypothesis: assume (|w^n|=n|w|). By the recursive definition (w^{n+1}=w^nw) and length additivity,

$$
|w^{n+1}|=|w^nw|=|w^n|+|w|=n|w|+|w|=(n+1)|w|.
$$

Therefore the identity holds for all (n∈ℕ). The proof depends on (|xy|=|x|+|y|) and the zero-power definition.

### Answer 3

One encoding is (1^{|x|}0xy): a unary length prefix for (x), a zero delimiter, then the bits of (x) followed by (y). Decode by counting leading ones until the first zero; call the count (m). Read the next (m) bits as (x), and the remainder as (y). If no zero exists or fewer than (m) bits remain, reject as malformed. The length is (2|x|+|y|+1), linear in the pair's total length. Naive concatenation is ambiguous because `010` could encode (`0`,`10`) or (`01`,`0`), among other splits.

### Answer 4

Canonical binary has length (Θ(log n)); unary has length (Θ(n)). An algorithm taking (O(n)) operations in numeric value is exponential in binary input length but linear in unary input length. Both encodings represent the same abstract positive integers and hence the same predicate, but they induce different string languages and complexity measures. Reasonable-encoding comparisons normally require polynomially related encodings; binary and unary are not polynomially related in both directions.

### Answer 5

Let an instance be a finite list of half-open integer intervals ([s_i,e_i)) with (s_i<e_i). Encode the list length and each signed endpoint using a self-delimiting integer code. Validity requires exactly the declared number of pairs and each start below its end. The yes predicate holds when there exist distinct (i,j) with (s_i<e_j) and (s_j<e_i). Malformed encodings are rejected. The half-open convention makes touching intervals such as ([1,3)) and ([3,5)) nonoverlapping; this is a required boundary case. The search version returns a pair of indices witnessing overlap, or reports none. Its output is a witness rather than a membership bit.
