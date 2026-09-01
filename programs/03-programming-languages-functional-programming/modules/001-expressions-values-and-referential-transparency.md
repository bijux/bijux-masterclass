---
module_id: FP-001
program: Programming Languages: Functional Programming
level: 1
module_number: 1
title: Expressions, Values, and Referential Transparency
status: complete
last_verified: 2026-08-28
---

# Expressions, Values, and Referential Transparency

## One-Page Review

### Governing question

When may a program phrase be replaced by its result without changing the program's observable behavior?

### Essential definitions

- An **expression** is a program phrase evaluated to produce a result, possibly with effects, failure, or divergence according to its language.
- A **value** is a completed result recognized by the language's evaluation rules; values do not require the same immediate evaluation step as reducible expressions.
- An **evaluation context** $C[-]$ is a surrounding program with one distinguished hole.
- Two expressions are **contextually equivalent** relative to observations when every admitted context observes the same behavior from each.
- An expression is **referentially transparent** in a stated context when replacing it by its value preserves observable behavior.
- **Equational reasoning** transforms program expressions using laws justified by their semantics, much as algebra transforms mathematical expressions.
- A **side effect** is an observable interaction beyond delivering a value, such as mutation, I/O, clock access, random sampling, or exception propagation.

### Central model, mechanism, or theorem

Write $e\Downarrow v$ when expression $e$ evaluates to value $v$, and $Obs(C[e])$ for the observation of placing $e$ in context $C$. The substitution principle desired by functional reasoning is

$$
e\Downarrow v
\quad\Longrightarrow\quad
\forall C\in\mathcal{C},\;Obs(C[e])=Obs(C[v]).
$$

This implication is not automatic. It depends on the language, evaluation strategy, admitted contexts, termination behavior, effects, and observation boundary. Pure, deterministic, terminating expressions under functional observations provide the simplest reliable setting.

### Critical invariants

- Expression, value, and textual representation are different objects.
- Replacing an expression can duplicate or eliminate its evaluation; hidden effects make that observable.
- Equal returned values do not erase different output, mutation, exceptions, or divergence.
- Referential transparency is a semantic property, not a keyword or formatting style.
- Algebraic rewrites require the laws of the actual value domain; machine integers and floating point do not inherit every law of mathematical numbers.
- Performance equivalence is separate unless cost belongs to the observer.

### Common failures

Typical errors are calling every expression pure, confusing deterministic output with absence of effects, treating immutability as sufficient for referential transparency, substituting calls that read time or state, reassociating floating-point arithmetic as real arithmetic, ignoring exceptions and nontermination, and declaring a test sample to be a universal program law.

### Compact example

The arithmetic expression `(4 + 2) * 6` can be rewritten by binding `x = 4 + 2` and using `x * 6`; both yield 36. If `next()` increments hidden state, `next() + next()` yields $1+2=3$, while binding `x = next()` and using `x + x` yields $1+1=2$. The substitution is safe in the first case and observable in the second.

### Connections

Retrieve [PLS-001's model of expressions and observable behavior](../../01-programming-languages-and-semantics/modules/001-programs-languages-and-observable-behavior.md). [FP-002](../ROADMAP.md) develops pure functions and explicit inputs. Formal proof connects to [Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md), while effects connect to [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md).

## Governing Question

What makes a program calculation behave enough like an equation that we may reason by substitution?

Functional programming places expressions at the center. Instead of reading a program primarily as a sequence of commands that change a store, we read it as a composition of computations that produce values. That perspective becomes powerful when an expression can be replaced by an equal expression without changing the surrounding program. Local definitions can be expanded, repeated calculations can be shared, and implementations can be derived from specifications through justified equations.

The slogan “replace an expression by its value” is only the beginning. An expression may print, mutate, read a clock, throw, fail to terminate, or consume observable resources. A language can also evaluate arguments strictly, lazily, or with sharing. We therefore need an explicit observation boundary and honest assumptions before substitution becomes a law.

## Why This Matters

Referential transparency reduces the amount of history needed to understand code. If `tax(invoice)` depends only on the explicit invoice value and a stated tax policy, a reviewer can reason locally. If it also reads mutable global configuration, current time, locale, or a remote feature flag, its apparent expression hides a protocol with the outside world.

Local equational reasoning supports several engineering practices:

- extracting or inlining an expression while preserving behavior;
- testing a calculation with ordinary input-output examples;
- memoizing a result under a sound key;
- evaluating independent expressions in parallel;
- replacing an implementation with a proven equivalent one;
- separating a deterministic core from effectful boundaries.

These are consequences under conditions, not automatic benefits of using `map`, lambdas, or immutable syntax. A functional style is valuable because it makes dependencies and composition more explicit, not because it changes the laws of the host language by declaration.

## Prerequisites and Retrieval

You should understand variables, function calls, arithmetic expressions, sets, equality, and basic program execution. Retrieve these facts:

1. An equality is valid only in a specified domain.
2. A universal statement needs proof or exhaustive finite evidence, not a handful of examples.
3. Evaluation may terminate with a value, terminate abnormally, or diverge.
4. A surrounding context can observe more than a returned payload.
5. Replacing one occurrence and duplicating an occurrence are different syntactic transformations.

No lambda-calculus machinery is required. Modules 051–060 later provide the formal functional foundation.

## Learning Objectives

After completing this module, you should be able to:

- distinguish expressions from values and commands;
- identify the observation boundary relevant to a substitution;
- state referential transparency using an evaluation context;
- determine why hidden state, I/O, randomness, time, exceptions, or divergence can invalidate a rewrite;
- perform small equational derivations with explicit domain assumptions;
- distinguish functional equality from resource equivalence;
- use executable examples as calibration evidence without treating them as proofs;
- refactor a calculation so environmental dependencies become explicit inputs.

## Core Exposition

An **expression** is a phrase whose language semantics describes evaluation toward a result. Literals are usually already values. Arithmetic applications, conditionals, function calls, and record construction are expressions in many languages. Some languages distinguish expressions sharply from statements; others make blocks, branches, and loops expression-oriented. Surface category matters less than the semantic question: does the phrase denote a result that can participate in a larger expression?

A **value** is language-relative. Integers, booleans, tuples, and functions may be values; a reducible addition is not yet a value. In a lazy language, a data constructor can count as a value before all of its fields are evaluated. A value is therefore not “anything stored in memory” and not necessarily a fully traversed data structure.

Evaluation can be modeled as $e\Downarrow v$ for a terminating computation. The notation deliberately excludes effects at first. A richer model records an outcome such as $\langle v,t\rangle$, where $t$ is a trace, or distinguishes errors and divergence. Referential transparency must use the richer model whenever the observer can see those facts.

An **evaluation context** $C[-]$ represents a surrounding program awaiting an expression. Examples include `[-] + 1`, `print([-])`, a branch condition, or a larger function application. If every admitted context observes $e$ and $v$ alike, replacement is behavior-preserving. The quantification prevents a convenient test context from hiding a difference that another legal context exposes.

Functional programming aims to make substitution routine by controlling effects. A pure calculation receives its dependencies as explicit values and returns a result without changing or consulting hidden state. Module 002 defines purity carefully. This chapter focuses on what purity enables: an expression can be named, expanded, shared, or transformed using justified laws.

Consider a let binding:

$$
\operatorname{let}\;x=e\;\operatorname{in}\;b.
$$

Inlining substitutes $e$ for free occurrences of $x$ in $b$, written $b[e/x]$. If $x$ occurs twice, inlining may evaluate $e$ twice rather than once. If it occurs zero times, inlining may eliminate evaluation. For a pure total expression under value observations, this preserves the result. For effects, exceptions, divergence, or observable cost, it may not.

Equational reasoning proceeds in small justified steps. For mathematical integers,

$$
(x+2)+3=x+(2+3)=x+5.
$$

Each equality cites associativity and literal evaluation. The same rewrite is not universally valid for bounded overflow, floating point, overloaded operators, or effectful addition. Functional programmers do not get free algebra; they work to design representations whose laws are clear.

Referential transparency is also compatible with explicit effects. A program may represent an action as a value and compose descriptions before a runtime executes them. Alternatively, a pure function can transform an explicit state value and return a new state. The effect still occurs somewhere; functional design makes its boundary and sequencing visible. Modules 041–046 develop those approaches.

## Definitions and Notation

Let:

- $E$ be a set of expressions;
- $V\subseteq E$ be values;
- $C[-]$ be a one-hole program context;
- $\mathcal{C}$ be the admitted contexts;
- $O$ be observations;
- $\operatorname{Obs}$ maps complete executions to $O$.

Write $e\Downarrow v$ for terminating evaluation and $e\Uparrow$ for divergence. Write $e_1\simeq e_2$ when

$$
\forall C\in\mathcal{C},\;Obs(C[e_1])=Obs(C[e_2]).
$$

An occurrence of $e$ is referentially transparent with value $v$ when $e\Downarrow v$ and $e\simeq v$ under the declared observations. In practice, authors often say a language fragment is referentially transparent when its expressions systematically support this replacement principle.

For substitution, $b[e/x]$ means replace free occurrences of $x$ in $b$ with $e$, avoiding variable capture. Detailed substitution is deferred to FP-052. Here, the critical operational fact is the number and location of occurrences.

Separate **functional observation** from **cost observation**:

$$
Obs_f(e)=\text{returned value, error, and declared effects},
\qquad
Obs_c(e)=\text{time, allocations, or other modeled resources}.
$$

Two expressions can be equivalent under $\operatorname{Obs}_f$ and different under $\operatorname{Obs}_c$.

## Mechanisms, Invariants, or Proof Structure

**Congruence.** Useful expression equality must survive placement in admitted contexts: from $e_1\simeq e_2$, infer $C[e_1]\simeq C[e_2]$. Without this property, local replacement cannot support compositional reasoning.

**Dependency completeness.** Every changing fact that affects a result must appear as an explicit input or an explicitly modeled effect. A function that reads hidden configuration violates this condition even if the configuration happens not to change during one test.

**Substitution accounting.** Before inlining, count occurrences of the bound name. Zero occurrences may remove evaluation; multiple occurrences may duplicate it; one occurrence may change evaluation order. Purity, termination, and the observer determine whether these differences matter.

**Domain-law obligation.** A rewrite must cite a law valid for the represented values. For mathematical integers, associativity and distributivity apply. Fixed-width, saturating, checked, approximate, or user-defined operations require their own laws and failure models.

**A derivation.** Let $f(x)=2(x+3)$ over mathematical integers. Then

$$
f(x)=2(x+3)=2x+2\cdot3=2x+6
$$

by distributivity and multiplication of literals. Therefore replacing `2 * (x + 3)` with `2 * x + 6` preserves integer value for every $x$. The conclusion excludes overflow and floating-point rounding unless those domains separately validate the law.

**Effect counterexample.** Let (next()) increment hidden state and return the new count. Starting at zero, $next()+next()=1+2=3$. Binding $y=next()$ and replacing both calls with $y$ yields $y+y=1+1=2$. One counterexample disproves the unrestricted substitution law.

## Alternatives and Trade-Offs

**Expression orientation versus command sequencing.** Expressions compose directly and expose results. Commands can model ordered interaction naturally. Functional systems commonly use expressions to construct or transform explicit descriptions of commands rather than pretending interaction does not exist.

**Eager versus lazy evaluation.** Eager evaluation computes arguments before calls; lazy evaluation computes when demanded and may share results. Both can support referentially transparent functional semantics, but termination and cost differ. Module 007 owns the detailed comparison.

**Inline versus share.** Inlining can enable simplification but duplicate work. A binding can share a computation. Under functional observations the results may agree, while under cost observations they differ substantially.

**Total versus partial expressions.** Total expressions return a value for every admitted input. Partial expressions may error or diverge. Totality makes substitution easier, but practical functional languages also represent failure explicitly or contain partial operations. Omitting the outcome is not a proof technique.

**Exact versus approximate numeric laws.** Exact integers and rationals support familiar algebra subject to representation limits. Floating-point operations prioritize bounded approximation and performance; reassociation can change rounding, overflow, NaN propagation, and signed zero behavior.

**Implicit environment versus explicit parameters.** Implicit access is concise but hides dependencies. Explicit values increase call-site information and make tests and memoization trustworthy. Reader-like abstractions can package explicit dependency passing without returning to ambient globals.

## Failure Modes and Misconceptions

1. **Every syntactic expression is referentially transparent.** A call expression can perform arbitrary effects.
2. **Same result twice proves purity.** Hidden dependencies may simply have remained stable during the sample.
3. **Deterministic means effect-free.** Appending the same log line deterministically is still an effect.
4. **Immutable input guarantees transparency.** A function can read time or mutate a global despite immutable arguments.
5. **Referential transparency means no I/O program exists.** Effects can be explicit values or isolated runtime boundaries.
6. **Inlining is merely textual.** It can change evaluation count, order, capture, termination, and cost.
7. **Algebra over reals applies to floating point.** Representation and rounding invalidate some identities.
8. **Exceptions are just values.** They alter control flow unless the language models them explicitly as ordinary result variants.
9. **Memoization is always safe for functions.** Hidden inputs and mutable results make cache reuse unsound.
10. **Passing tests proves an equation.** Tests sample; a program law needs assumptions and a derivation or exhaustive analysis.

## Worked Examples

### Example 1

**Question:** Is `2 + 3` an expression or a value?

**Reasoning:** In a standard eager arithmetic semantics, `2` and `3` are values, while `2 + 3` is a reducible expression. Evaluation yields value `5`. A compiler may constant-fold the expression before runtime, but that implementation timing does not change the semantic distinction.

**Conclusion:** An expression denotes a computation; its evaluated result is a value under the language rules.

### Example 2

**Question:** Does naming a pure arithmetic subexpression change its result?

**Reasoning:** The direct expression `(4 + 2) * 6` yields 36. Binding `x = 4 + 2` and evaluating `x * 6` also yields 36. Substitution replaces $x$ with its value 6, and integer multiplication observes no difference.

**Conclusion:** Pure terminating integer calculation supports this local replacement.

### Example 3

**Question:** Why does hidden mutation invalidate sharing and duplication?

**Reasoning:** The executable comparison evaluates one pure and one stateful case. Its fixed output is calibration evidence for this program, not a universal proof.

<!-- bijux-verify: {"id":"substitution-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"pure direct: 36\npure bound: 36\neffectful twice: 3\neffectful shared: 2\n","stderr":""}} -->
```python
print("pure direct:", (4 + 2) * 6)
pure_value = 4 + 2
print("pure bound:", pure_value * 6)

hidden_count = 0


def next_number():
    global hidden_count
    hidden_count += 1
    return hidden_count


hidden_count = 0
print("effectful twice:", next_number() + next_number())
hidden_count = 0
shared_value = next_number()
print("effectful shared:", shared_value + shared_value)
```

**Conclusion:** Replacing two stateful calls with one shared result changes both evaluation count and value.

### Example 4

**Question:** Is a call to `current_time()` referentially transparent if it does not mutate memory?

**Reasoning:** Two evaluations can return different timestamps because the clock is a hidden input. Replacing both calls with one earlier value changes elapsed-time calculations. Passing an explicit timestamp or clock capability makes the dependency visible, but executing that capability remains an effect.

**Conclusion:** Reading changing external state violates value substitution even without an assignment statement.

### Example 5

**Question:** Can a deterministic logging function be referentially transparent?

**Reasoning:** Suppose `square(4)` always returns 16 and always appends `squared 4` to a log. Replacing two calls with one shared value preserves the numeric result but reduces log entries from two to one. A value-only observer equates them; the production observer that includes logs does not.

**Conclusion:** Determinism does not remove effects, and transparency depends on the declared observations.

### Example 6

**Question:** May `(a + b) + c` always be rewritten as `a + (b + c)`?

**Reasoning:** It is valid for mathematical integers. For floating point, choose $a=10^{16}$, $b=-10^{16}$, and $c=1$. The left grouping first produces approximately 0 then 1; the right grouping may round $(-10^{16})+1$ back to $-10^{16}$, then produce 0. The represented operation is not real-number addition.

**Conclusion:** Equational laws belong to value domains, not surface operator spellings.

### Example 7

**Question:** Is replacing an unused binding safe when its expression fails?

**Reasoning:** In a strict language, `let x = fail() in 7` evaluates `fail()` before producing 7, so deleting the unused binding changes an error into success. In a lazy language, the unused expression may never be demanded, so both versions produce 7. If failure is represented as an explicit value that must be combined, the dependency is visible again.

**Conclusion:** Evaluation strategy and abnormal outcomes are part of a substitution proof.

### Example 8

**Question:** Why is a pure normalization pipeline easier to test?

**Reasoning:** Let `normalize(records, policy)` return new canonical records solely from its two inputs. A test supplies both values and compares the result. If locale, current schema, and default units are globals, identical record arguments can produce different results across environments. Making the policy explicit restores dependency completeness.

**Conclusion:** Explicit inputs turn environmental variation into ordinary test data.

### Example 9

**Question:** When is memoizing `price(order)` sound?

**Reasoning:** It is sound under a key that captures every relevant immutable input and when the returned value cannot be mutated through an alias. It is unsound if price also reads current exchange rates, customer tier, time, or mutable inventory without including their versions. Caching then replaces a fresh effectful computation with an old observation.

**Conclusion:** Memoization relies on referential transparency plus a complete, stable key.

### Example 10

**Question:** How can a production service preserve a functional core while performing I/O?

**Reasoning:** The boundary reads request bytes, configuration version, clock value, and database snapshot. A pure decision expression transforms those explicit values into a response and a list of intended effects. The shell validates and executes the effects, records outcomes, and handles retries. Replaying the pure decision with the same captured inputs yields the same description, while the shell remains honestly effectful.

**Conclusion:** Functional reasoning scales by isolating and representing effects, not denying that systems interact.

## Cross-Program Connections

- **Programming Languages & Semantics:** evaluation contexts and contextual equivalence formalize replacement.
- **Theory of Programming:** program equations become proof obligations and refinement steps.
- **Algorithm Engineering:** transformations must preserve outputs while cost models may distinguish implementations.
- **Testing & Quality Engineering:** deterministic explicit-input calculations admit compact example and property oracles.
- **Concurrent & Parallel Programming:** independent transparent expressions can often be reordered or evaluated in parallel under a separate cost model.
- **Data Engineering:** deterministic transformations improve reproducibility only when schemas, configuration, and source versions are explicit inputs.
- **Software Architecture:** pure-core/effectful-shell boundaries localize environmental protocols.
- **Security Engineering:** hidden ambient authority is an implicit effect; explicit capabilities make authority reviewable.

## References

- Richard Bird. [*Thinking Functionally with Haskell*](https://www.cambridge.org/core/books/thinking-functionally-with-haskell/79F91D976F0C7229082325B41824EBBC). Cambridge University Press, 2014, DOI 10.1017/CBO9781316092415. Publisher record checked 2026-08-28.
- Graham Hutton. [*Programming in Haskell*, 2nd ed.](https://www.cambridge.org/highereducation/books/programming-in-haskell/8FED82E807EF12D390DE0D16FDE217E4). Cambridge University Press, 2016, ISBN 9781316626221. Publisher record checked 2026-08-28.
- John Backus. [“Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs.”](https://doi.org/10.1145/359576.359579) *Communications of the ACM* 21(8), 1978, pp. 613–641, DOI 10.1145/359576.359579. ACM DOI record checked 2026-08-28.
- John Hughes. [“Why Functional Programming Matters.”](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/whyfp.pdf) *The Computer Journal* 32(2), 1989, pp. 98–107, DOI 10.1093/comjnl/32.2.98. Archival paper and DOI metadata checked 2026-08-28.
- Benjamin C. Pierce. [*Types and Programming Languages*](https://mitpress.mit.edu/9780262303828/types-and-programming-languages/). MIT Press, 2002, ISBN 9780262162098. Publisher record checked 2026-08-28.

## Exercises

### Exercise 1

Classify each phrase under a conventional strict language: integer literal `4`; `2 + 2`; a completed pair `(4, 5)`; `print("hi")`; an infinite loop. State whether it is an expression, a value, effectful, terminating, or divergent; categories may overlap.

### Exercise 2

Starting from $g(x)=3(x+4)$, derive an equivalent expanded expression over mathematical integers. Name every algebraic law. Then explain why the derivation alone does not establish equality for all fixed-width or floating-point implementations.

### Exercise 3

Given `let y = read_counter() in y - y`, compare it with `read_counter() - read_counter()` when each call returns the current counter and then increments it. Start at 10 and trace results and final counter states. Diagnose which substitution changed behavior.

### Exercise 4

Compare two designs for `shipping_total(order)`: Design A reads global exchange rates and current promotion state; Design B receives `order`, `rates`, and `promotion` values. State what must be true for memoization, deterministic testing, and parallel evaluation in each design. Include mutable-result aliasing in your analysis.

### Exercise 5

A fraud decision depends on transaction data, a model version, feature configuration, current sanctions data, and a request timestamp, and it emits an audit event. Design a pure decision boundary and an effectful shell. Specify the input and output values, how failures are represented, which artifacts must be versioned for replay, and what claim referential transparency permits.

## Answers to the Exercises

### Answer 1

`4` is both an expression and already a value; it terminates without an effect. `2 + 2` is an expression that terminates to value 4 under ordinary integer assumptions but is not initially a value. The completed pair is an expression and typically a value if both components are values, subject to the language's evaluation strategy. `print("hi")` is an effectful expression in a language where calls return a unit-like value; it terminates only if the output operation does. An infinite loop is an expression or command according to syntax and diverges, so it produces no terminating value. These classifications require language rules rather than punctuation alone.

### Answer 2

For mathematical integers,

$$
g(x)=3(x+4)=3x+3\cdot4=3x+12.
$$

The first rewrite uses distributivity of multiplication over addition; the second evaluates the integer literal product. The derivation assumes exact, unbounded integer operations. Fixed-width arithmetic may overflow, trap, wrap, or saturate at different intermediate points. Floating-point distribution can change rounding and special-value propagation. Those domains require separate semantics and evidence.

### Answer 3

Starting at 10, the binding calls `read_counter()` once, obtains 10, increments the hidden counter to 11, and computes $10-10=0$. The duplicated version makes the first call return 10 and advance to 11, then the second return 11 and advance to 12, producing $10-11=-1$. Replacing the shared variable occurrences with the effectful expression duplicated evaluation, changing both the numeric result and final hidden state. The unrestricted inlining step is invalid.

### Answer 4

Design A lacks a complete key unless the cache captures order plus exact exchange-rate and promotion versions; ordinary order-only memoization is unsound. Tests must control or replace both globals, and parallel calls can observe different versions or contend on shared state. Design B can be memoized by a stable representation of all three explicit inputs when the calculation has no other effects. Tests directly provide fixtures, and independent calls can be evaluated in parallel under resource constraints. In either design, returning a mutable cached object lets one caller change what another receives; return an immutable value or defensive representation and state its equality policy.

### Answer 5

The shell captures validated transaction data, model artifact ID and digest, feature-configuration version, sanctions snapshot ID and digest, and request timestamp. The pure core receives one immutable `DecisionInput` containing those facts and returns a `DecisionResult` variant such as `Approve`, `Review(reasons)`, or `Reject(reasons)`, plus an immutable audit-event description. Validation or unavailable dependencies are explicit failure variants, not hidden exceptions inside the decision. The shell loads and verifies versioned artifacts, calls the core, durably writes the audit event, and maps failures to service responses. Replay requires the exact input and every referenced artifact/version. Referential transparency permits the bounded claim that the same validated decision input under the same core implementation yields the same decision and event description; it does not claim that external loading, publication, or current-world facts are effect-free.
