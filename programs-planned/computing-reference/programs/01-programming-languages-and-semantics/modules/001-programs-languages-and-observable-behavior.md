---
module_id: PLS-001
program: Programming Languages & Semantics
level: 1
module_number: 1
title: Programs, Languages, and Observable Behavior
status: complete
last_verified: 2026-08-28
---

# Programs, Languages, and Observable Behavior

## One-Page Review

### Governing question

What must be specified before two executions can be judged to have the same behavior?

### Essential definitions

- A **program text** is a finite representation; a **program** is that representation interpreted according to a language.
- A **programming language** supplies syntax and meaning. Its **statics** classify well-formed phrases without running them; its **dynamics** describe how execution proceeds and what outcomes it can produce.
- A **configuration** records the program phrase and abstract execution state relevant to the semantic model.
- An **outcome** may be a returned value, a normal or abnormal termination, divergence, or a trace of externally visible events.
- An **observation boundary** states what an observer can distinguish: for example, a return value, output bytes, an exception, persistent writes, or elapsed resources under an explicit cost model.
- Two programs are **observationally equivalent** relative to a boundary and allowed contexts when no permitted observation distinguishes them.

### Central model, mechanism, or theorem

Let (P) be programs, (I) inputs, (O) semantic outcomes, and (B) an observation boundary. A semantic function or relation associates execution with outcomes,

\[
\mathcal{E}:P\times I\to O
\qquad\text{or}\qquad
\langle p,i\rangle\Downarrow o.
\]

The boundary induces an observation function (obs_B:O\to A_B). For deterministic programs considered in isolation,

\[
p\approx_B q
\quad\Longleftrightarrow\quad
\forall i\in I,\;obs_B(\mathcal{E}(p,i))=obs_B(\mathcal{E}(q,i)).
\]

For nondeterministic programs or programs placed in contexts, outcomes become sets or distributions and the quantification must include the allowed contexts. Equality is therefore always relative to a declared semantic model.

### Critical invariants

- Source text, abstract program, execution state, and observed outcome are different objects.
- Syntax alone does not determine behavior without a language definition and execution environment.
- An outcome model must account for termination and divergence; ignoring either changes equivalence claims.
- Hidden steps may differ while observations agree, but changing the observation boundary may expose those steps.
- Tests establish behavior only for the tested inputs, contexts, toolchain, and environment.
- An implementation transformation is correct only with respect to the language behavior it is required to preserve.

### Common failures

Typical failures include equating a file with an execution, treating a compiler as the language definition, comparing only final values while ignoring effects, declaring equivalence from a few tests, treating unspecified resource use as a semantic promise, overlooking divergence or errors, and changing the observer halfway through an argument.

### Compact example

Suppose (p(x)=(x+1)+1) and (q(x)=x+2). Over mathematical integers, both return (x+2), so a final-value observer cannot distinguish them. If each addition emits its intermediate result, (p) emits two values while (q) emits one. The same texts are equivalent under one boundary and distinguishable under another.

### Connections

Retrieve the [curriculum's mathematical and programming foundation](../../../DEPENDENCY_AND_SEQUENCE.md). [PLS-002](../ROADMAP.md) separates concrete text into lexical elements. Formal language syntax connects to [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md), while behavior-preserving translation connects to [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md).

## Governing Question

When someone says that a program “does the same thing,” what exactly is the thing being compared?

A source file is inert data. It becomes a program only relative to rules that identify its phrases and assign those phrases meaning. An execution is then one event in which an implementation applies those rules, or a permitted refinement of them, to a particular input and environment. The observable result might include a value, printed bytes, mutations, exceptions, termination, timing, or interaction with another system. Without fixing those choices, sameness is not a technical claim.

This chapter develops a language-independent vocabulary for making such claims precise. It introduces the semantic boundary shared by interpreters, compilers, testing, verification, and language design. It does not yet construct grammars, inference rules, or compiler passes; later modules own those mechanisms.

## Why This Matters

Most consequential software disagreements conceal a semantic disagreement. A refactoring preserves return values but changes database writes. An optimization preserves ordinary results but makes an exception occur earlier. A test double reproduces values but not cancellation. A service migration returns the same JSON while changing whether a request is processed twice. Each case asks which behavior belongs to the contract.

Programming-language semantics supplies a disciplined answer: state the program model, the possible executions, and the observer. This does not require every engineer to prove a theorem. It does require separating five kinds of statement:

1. a **model** selects the aspects represented;
2. a **language guarantee** constrains all conforming implementations;
3. a **mechanism** explains how one implementation realizes behavior;
4. a **policy** chooses among permitted behaviors;
5. an **observation** reports what happened in one execution.

Confusing these levels causes brittle systems. An empirical observation about one compiler version is not automatically a language guarantee. Conversely, an abstract semantic rule can be useful without predicting cache misses or wall-clock time because those facts may lie outside its boundary.

## Prerequisites and Retrieval

You should be able to read small programs, functions, sets, relations, and universal quantification. Retrieve these ideas:

1. A function maps each input in its domain to one output; a relation may associate an input with zero, one, or many outputs.
2. Equality compares values in a stated domain. Equality of final integers does not imply equality of event sequences.
3. A universal claim such as “for every input” cannot be proved by finitely many examples unless an additional finite-exhaustion argument applies.
4. An abstraction deliberately omits detail. A claim proved in an abstraction applies only when the omitted detail cannot invalidate its assumptions.
5. A trace is an ordered sequence, so event order and multiplicity matter.

Experience with more than one programming language is helpful because familiar punctuation can otherwise be mistaken for universal meaning.

## Learning Objectives

After completing this module, you should be able to:

- distinguish program text, abstract program, execution, configuration, and outcome;
- describe a programming language in terms of syntax, statics, dynamics, and pragmatic implementation constraints;
- define an observation boundary for a concrete software claim;
- model terminating values, errors, divergence, and effect traces;
- explain why observational equivalence is relative to inputs, contexts, and observers;
- test a bounded behavioral model without misrepresenting the test as a proof;
- diagnose claims that confuse implementation evidence with language guarantees;
- state the proof obligations behind a behavior-preserving transformation.

## Core Exposition

A **program text** is a physical or mathematical representation: characters, bytes, tokens, or an abstract syntax tree. Not every text is admitted by a language. Syntax determines which texts or abstract structures count as phrases. Static semantics may reject syntactically valid phrases before execution—for example, because a name is unbound or an operation has incompatible operands. Dynamic semantics determines how admitted phrases evaluate, interact, terminate, or fail.

This decomposition is conceptual, not a demand that every language have a separate type checker. A language can perform most checks dynamically and still have rules describing valid runtime steps. Likewise, an implementation can fuse parsing, checking, and execution without erasing the distinctions in the specification.

A running program is represented abstractly by a **configuration**. A configuration might contain an expression and environment, a command and store, a stack and heap, or several communicating processes. Which fields appear depends on the questions the semantics must answer. A semantics for arithmetic need not contain a filesystem; a semantics for file handles must.

There are two common presentation styles. An **evaluation semantics** relates a starting configuration directly to an outcome. A **transition semantics** relates one configuration to its next possible configuration. In schematic notation,

\[
\langle p,i\rangle\Downarrow o
\qquad\text{and}\qquad
c\longrightarrow c'.
\]

The first makes completed computations concise. The second exposes intermediate steps, nondeterminism, concurrency, and divergence. Both are models; neither is the literal motion of electrons in hardware.

Outcomes must be rich enough for the intended claims. A minimal deterministic model might use

\[
O=\operatorname{Return}(v)\mid\operatorname{Error}(e)\mid\operatorname{Diverge}.
\]

An interactive model can pair an outcome with a trace (t=e_1e_2\cdots), where events record externally relevant reads, writes, messages, or emissions. A concurrent model may admit a set of traces. A probabilistic model may assign distributions. Choosing a plain value when the program performs effects silently discards evidence.

An **observer** is not necessarily a human. It is the formal projection of an execution that the contract allows a surrounding program, client, test harness, or operator to detect. If the boundary exposes only returned integers, two allocation strategies may be indistinguishable. If memory consumption is contractual, the observer also measures a cost. Resource observations require an explicit cost model and environment; raw wall-clock measurements do not become timeless semantic facts.

An **execution context** is a larger program with a hole into which a component can be placed. Contextual comparison matters because a component may reveal behavior only when called twice, passed an alias, interrupted, or supplied a callback. The strongest common notion says that no allowed context distinguishes the two components. Module 056 develops that notion formally; here it is enough to make the quantifier visible.

The practical workflow is therefore:

1. identify the artifacts and inputs being compared;
2. declare the language and semantic assumptions;
3. enumerate possible termination, error, and interaction outcomes;
4. choose the observer and allowed contexts;
5. derive or measure observations;
6. state the strength and limits of the conclusion.

## Definitions and Notation

Let:

- (P) be a set of admitted programs or program components;
- (I) be a set of inputs;
- (C) be machine configurations;
- (O) be semantic outcomes;
- (T=E^*) be finite traces over observable event alphabet (E);
- (B) be an observation boundary;
- (A_B) be the observations visible at boundary (B).

For a deterministic terminating model, (\mathcal{E}:P\times I\to O). A relation (\mathcal{R}\subseteq(P\times I)\times O) is more general: it can represent stuck configurations or several permitted outcomes. Write (\langle p,i\rangle\Downarrow o) for a terminating derivation and (\langle p,i\rangle\Uparrow) for divergence.

The projection (obs_B:O\to A_B) deliberately forgets hidden details. For isolated deterministic programs,

\[
p\approx_B q
\iff
\forall i\in I,\;obs_B(\mathcal{E}(p,i))=obs_B(\mathcal{E}(q,i)).
\]

If programs may produce several outcomes, define (Out(p,i)=\{o\mid\langle p,i\rangle\Downarrow o\}) and compare the projected sets, while separately accounting for divergence. Equality of may-outcomes, must-outcomes, and probability distributions are different equivalences.

A context (K[-]) is an admitted program phrase containing one component hole. A contextual relation has the shape

\[
p\simeq_B q
\iff
\forall K\in\mathcal{K},\forall i\in I,
\;Obs_B(K[p],i)=Obs_B(K[q],i).
\]

The notation does not itself prove anything: the sets of contexts, inputs, and observations must be defined.

## Mechanisms, Invariants, or Proof Structure

**Semantic well-formedness.** Every comparison must be typed at the model level. Comparing source bytes with a runtime value is meaningless until a parser and evaluation relation connect them. Comparing a single trace with a set of possible traces is likewise a category error.

**Outcome completeness relative to the boundary.** If exceptions are visible, (O) must distinguish them. If nontermination is visible because a client waits forever, divergence cannot be omitted. Completeness is relative: a model can legitimately ignore allocation addresses when clients cannot inspect them.

**Observation stability.** The boundary must remain fixed throughout an equivalence argument. A proof cannot compare final values, encounter a counterexample in output order, and dismiss output as “internal” unless the original contract excluded it.

**Congruence requirement.** A replacement principle needs more than isolated input-output equality. If replacing (p) with (q) inside any allowed context preserves observations, the relation is a congruence for those contexts. Without that property, local reasoning may fail under composition.

**Behavior-preservation obligation.** For a translator (T) from source programs to target programs, a basic deterministic obligation is

\[
obs_B(\mathcal{E}_S(p,i))=obs_B(\mathcal{E}_T(T(p),i))
\]

for every admitted (p) and input (i), under stated source-target correspondence assumptions. Real compiler correctness may permit target stuttering steps, relate memories, or qualify undefined source behavior; those refinements belong to the compiler program.

**A small proof.** Over mathematical integers, let (p(x)=(x+1)+1) and (q(x)=x+2). Associativity of integer addition gives

\[
(x+1)+1=x+(1+1)=x+2.
\]

Thus (p\approx_B q) for a total final-integer observer over all integer inputs. This is a proof under explicit assumptions, not empirical evidence about overflow, floating-point arithmetic, callbacks, or logging.

## Alternatives and Trade-Offs

**Big-step versus small-step models.** Big-step evaluation makes final outcomes and inductive interpreters readable. It needs additional machinery to distinguish divergence from an absent derivation and can conceal intermediate effects. Small-step transitions expose order and interleaving but create longer derivations. The choice follows the question.

**Functions versus relations.** A function is convenient for deterministic, total behavior. A relation naturally represents nondeterminism, underspecification, failure to make progress, and multiple executions. Forcing nondeterminism into an arbitrary implementation policy changes the language model.

**Values versus traces.** Value semantics supports simple algebraic reasoning. Trace semantics captures protocols and effects. Traces reveal more behavior, so equivalence becomes harder to establish but more useful for interactive systems.

**Language-level versus implementation-level observation.** Language specifications commonly abstract from instruction counts, addresses, and cache behavior. Performance engineering intentionally exposes some of them. Both boundaries are valid if labeled; neither should silently borrow guarantees from the other.

**Exact equivalence versus refinement.** Exact equality may be too strict. A new component can permit fewer failures, reveal less secret information, or meet a latency bound while preserving required outputs. A preorder expressing “every new behavior is allowed by the old contract” may fit better than equality, but the direction of refinement must be stated.

**Proof versus testing.** Proof covers a formally delimited class when its assumptions hold. Testing samples real implementations and can reveal modeling mistakes. Strong engineering uses each for its proper evidence: executable examples calibrate understanding, while universal equivalence needs derivation, exhaustive finite analysis, or a proof.

## Failure Modes and Misconceptions

1. **The source file is the program execution.** It is a representation consumed by an implementation; one text can have many executions.
2. **The compiler defines the language.** A compiler supplies implementation evidence. It may contain bugs or make choices where the language permits several behaviors.
3. **Same return value means same behavior.** Output, state changes, errors, timing contracts, and divergence may distinguish executions.
4. **Passing tests proves equivalence.** Tests cover their sampled inputs and contexts unless the state space is finite and exhaustively enumerated.
5. **Every internal step is observable.** Semantic models intentionally hide steps; observability comes from a declared boundary.
6. **No returned value means no outcome.** Normal completion, emitted events, or store changes can be the outcome.
7. **A missing derivation always means divergence.** It may instead mean a stuck term, malformed program, or incomplete semantics.
8. **Nondeterminism is implementation noise.** It can be permitted language behavior and must then be represented as alternatives or distributions.
9. **Faster is semantically equivalent.** Performance is relevant only under a stated resource model, and faster execution can still change functional effects.
10. **Formal notation creates rigor by itself.** Undefined domains, contexts, or observers make a formula precise-looking but indeterminate.

## Worked Examples

### Example 1

**Question:** Are the bytes in a script file, its parsed syntax tree, and a running process the same program object?

**Reasoning:** The byte sequence is a concrete representation. Parsing maps it to an abstract phrase if the syntax is valid. Starting that phrase with input and an environment creates a configuration whose state changes during execution. The artifacts are connected by relations, but they have different types and lifetimes. Two files may parse to the same abstract phrase after comments are discarded; one phrase may be executed many times.

**Conclusion:** Program text, abstract program, and execution are distinct objects even when everyday speech calls all three “the program.”

### Example 2

**Question:** Does the text `1 / 2` determine one result across programming languages?

**Reasoning:** Its surface syntax suggests division, but a language may define integer operands to yield integer quotient, a rational value, a floating-point value, or a type error. Static rules decide whether the operands are admissible; dynamic rules choose the operation and outcome. Punctuation alone supplies neither.

**Conclusion:** Behavior is assigned by a language definition, not recovered from familiar characters alone.

### Example 3

**Question:** Are “increment twice” and “add two once” observationally equivalent?

**Reasoning:** The following bounded model treats the final state and emitted trace as observable. Programs `p` and `q` agree, while `r` emits an additional event. The test covers one input in this deliberately tiny language; it illustrates the model but does not prove general contextual equivalence.

<!-- bijux-verify: {"id":"observable-trace-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"p: value=5 trace=(5,)\nq: value=5 trace=(5,)\nr: value=5 trace=(5, 5)\np~q: True\np~r: False\n","stderr":""}} -->
```python
def run(program, input_value):
    state = input_value
    trace = []
    for operation, argument in program:
        if operation == "add":
            state += argument
        elif operation == "emit":
            trace.append(state)
        else:
            raise ValueError(f"unknown operation: {operation}")
    return state, tuple(trace)


programs = {
    "p": (("add", 1), ("add", 1), ("emit", None)),
    "q": (("add", 2), ("emit", None)),
    "r": (("add", 2), ("emit", None), ("emit", None)),
}
observations = {}
for name, program in programs.items():
    observations[name] = run(program, 3)
    value, trace = observations[name]
    print(f"{name}: value={value} trace={trace}")
print("p~q:", observations["p"] == observations["q"])
print("p~r:", observations["p"] == observations["r"])
```

**Conclusion:** Equivalence follows the selected observation tuple; final-value equality alone would incorrectly equate all three.

### Example 4

**Question:** Two command-line tools print the same data. Can a shell script distinguish them?

**Reasoning:** Tool A writes the data to standard output and exits 0. Tool B writes it to standard error and exits 2. A human terminal may display visually similar text, but a context can redirect the streams separately and branch on the exit status.

**Conclusion:** For command-line programs, stream identity and exit status commonly belong to observable behavior.

### Example 5

**Question:** Does a function that loops forever have the same behavior as one that immediately returns no value?

**Reasoning:** A model containing only returned payloads may map both to “no payload,” but that projection is too coarse for a caller that must regain control. In an outcome domain with (Return(unit)) and (Diverge), the results differ. A timeout can observe the difference operationally, although its duration is an environmental policy.

**Conclusion:** Termination behavior must be represented whenever continued control flow is observable.

### Example 6

**Question:** Are raising an exception and returning an error value interchangeable?

**Reasoning:** A caller can inspect a returned tagged value using ordinary control flow. An exception may unwind frames and run cleanup handlers before reaching a different handler. Even if both ultimately display the word `error`, contexts with cleanup or recovery can distinguish them.

**Conclusion:** Error channel and control transfer are semantic behavior, not merely message formatting.

### Example 7

**Question:** May an implementation replace ten temporary allocations with one?

**Reasoning:** If allocation identity, memory use, finalizers, and timing are hidden, the change may preserve all language observations. If the language exposes object identity, weak references, allocation failure, or finalization, the proof obligation expands. Under a performance contract, peak memory may also be observable.

**Conclusion:** An optimization is valid relative to specified observations; “internal allocation” is not universally invisible.

### Example 8

**Question:** How should a language model a scheduler that may choose either ready task first?

**Reasoning:** A deterministic function would choose one order and accidentally promote an implementation policy to a language guarantee. A relation can associate the starting configuration with both traces, such as (`a`,`b`) and (`b`,`a`). Safety analysis checks every permitted trace; a may-test asks whether one trace exists.

**Conclusion:** Nondeterministic semantics preserves permitted alternatives and forces may-versus-must claims to be explicit.

### Example 9

**Question:** What must be shown to replace `(x + 1) + 1` with `x + 2`?

**Reasoning:** Over mathematical integers, associativity proves equality for every (x). With fixed-width trapping arithmetic, both expressions overflow on the same mathematical threshold if evaluation uses the shown constants, but details such as literal conversion and intermediate precision still require rules. With floating-point values, reassociation is not generally valid. If addition invokes user code or logs operations, call count is observable.

**Conclusion:** An algebraic rewrite inherits the language's numeric and effect assumptions; surface algebra alone is insufficient.

### Example 10

**Question:** Two stack implementations return the same sequence from `pop`. Are they interchangeable?

**Reasoning:** A context may also call `isEmpty`, retain aliases to pushed mutable objects, trigger capacity limits, or observe errors on an empty stack. Representation differences are harmless only if every operation in the public interface preserves its relational invariant across all allowed call sequences.

**Conclusion:** Component equivalence is contextual and protocol-shaped, not established by one operation on one state.

## Cross-Program Connections

- **Theory of Programming:** program logics turn behavioral claims into proof obligations over states and executions.
- **Compilers:** translation correctness relates source and target observations despite different internal steps and representations.
- **Software Engineering, Testing & Quality Engineering:** test oracles are executable observation boundaries; incomplete oracles miss behavior.
- **Operating Systems:** processes, exit status, signals, files, and scheduling make many observations concrete.
- **Concurrent & Parallel Programming:** possible traces, fairness, and interference require relational rather than single-result models.
- **Security Engineering:** noninterference asks whether changes in secret data can alter observations available to an attacker.
- **API Engineering:** protocol compatibility depends on observable requests, responses, errors, ordering, and timing promises.
- **Systems Design & Distributed Models:** partial failure and retries expand outcomes beyond local return values.

## References

- Benjamin C. Pierce. [*Types and Programming Languages*](https://mitpress.mit.edu/9780262303828/types-and-programming-languages/). MIT Press, 2002, ISBN 9780262162098 (hardcover) and 9780262303828 (eBook). Publisher record checked 2026-08-28.
- Robert Harper. [*Practical Foundations for Programming Languages*, 2nd ed.](https://www.cambridge.org/core/books/practical-foundations-for-programming-languages/3D852B5A14F48F85C60B95A0BBCAB7D9). Cambridge University Press, 2016, DOI 10.1017/CBO9781316576892. Publisher record checked 2026-08-28.
- Gordon D. Plotkin. [“A Structural Approach to Operational Semantics.”](https://homepages.inf.ed.ac.uk/gdp/publications/sos_jlap.pdf) *Journal of Logic and Algebraic Programming* 60–61, 2004, revised from the 1981 Aarhus lecture notes. Author-hosted paper checked 2026-08-28.
- Franklyn Turbak and David Gifford, with Mark Sheldon. [*Design Concepts in Programming Languages*](https://mitpress.mit.edu/9780262201759/design-concepts-in-programming-languages/). MIT Press, 2008, ISBN 9780262201759. Publisher record checked 2026-08-28.
- Peter Van Roy and Seif Haridi. [*Concepts, Techniques, and Models of Computer Programming*](https://mitpress.mit.edu/9780262220699/concepts-techniques-and-models-of-computer-programming/). MIT Press, 2004, ISBN 9780262220699. Publisher record checked 2026-08-28.

## Exercises

### Exercise 1

For each item, classify it as program text, abstract program, configuration, outcome, or observation: a UTF-8 source file; an abstract syntax tree; an expression paired with a store; an uncaught exception; the exit code recorded by a shell. Explain any dependence on the chosen model.

### Exercise 2

A tiny state machine starts with integer (x) and supports `add n`, `emit`, and `fail`. `add` changes the state, `emit` appends the current state to a trace, and `fail` terminates with an error. Derive the complete outcome of `add 3; emit; add -1; emit` from (x=4), including final state and trace. Then derive `add 3; fail; emit` under a rule that no steps occur after failure.

### Exercise 3

Let (p(x)=(x+2)+3) and (q(x)=x+5) over mathematical integers. Prove final-value equivalence for all inputs. Then construct one plausible effectful meaning of addition under which they are distinguishable, and identify the distinguishing observation.

### Exercise 4

Compare two observation boundaries for a sorting function: (B_1) exposes only the returned sequence; (B_2) also exposes mutation of the input object and the number of comparisons. State when an in-place quicksort and a copying mergesort could be equivalent under each boundary. Do not assume a particular implementation beyond facts you state.

### Exercise 5

A message-processing component receives one command and may write a database row, publish an event, and acknowledge the command. Define a trace alphabet and a required observation policy suitable for judging a retrying implementation. Give two traces that have the same final database row but should not be considered equivalent, and explain the production fault exposed by the distinction.

## Answers to the Exercises

### Answer 1

The UTF-8 file is program text. The abstract syntax tree is an abstract program representation after parsing. The expression-store pair is a configuration because it contains a phrase and execution state. The uncaught exception is an outcome if the model ends execution with (Error(e)); a lower-level model could instead represent unwinding configurations before reaching it. The exit code is an observation projected from process termination. The qualifications matter because models choose their boundaries, but they do not erase the type distinctions within one chosen model.

### Answer 2

Starting from 4, `add 3` produces state 7. The first `emit` appends 7, giving trace ((7)). `add -1` produces state 6, and the second `emit` gives ((7,6)). The complete successful observation is final state 6 with trace ((7,6)). In the second program, `add 3` reaches 7 and `fail` produces (Error) with the empty trace. The trailing `emit` is unreachable under the stated terminal-failure rule. If the error payload or state-at-failure is observable, it must also be included explicitly.

### Answer 3

For every mathematical integer (x), associativity gives ((x+2)+3=x+(2+3)=x+5), so final returned integers agree. For a distinguishing effectful meaning, let every addition emit its result. Then (p) emits ((x+2,x+5)) while (q) emits only ((x+5)). A trace observer distinguishes them by event count and first event, although a final-value observer does not. This countermodel does not refute the integer proof; it changes the semantic assumptions.

### Answer 4

Under (B_1), the algorithms can be equivalent if both return a sequence containing exactly the input elements in the required sorted order for every admitted input, including duplicates and boundary values. Whether either mutates the original or uses more comparisons is hidden. Under (B_2), an in-place algorithm and a copying algorithm differ whenever the caller can observe the original object's mutation. Their comparison counts can also differ by input; equivalence would require those counts to match under a shared definition of “comparison.” Algorithm-family names alone do not settle either claim because concrete partitioning, stability, allocation, and comparator behavior must be stated.

### Answer 5

Use events such as (Write(id,value)), (Publish(id,payload)), (Ack(id)), and (Fail(stage)). A suitable policy observes event order and multiplicity per command identifier, not only final state. For example, trace (Write(c,v),Publish(c,e),Ack(c)) differs from (Write(c,v),Publish(c,e),Fail,Write(c,v),Publish(c,e),Ack(c)): the database may upsert to the same row, but the second trace publishes the event twice. Another bad trace is (Ack(c),Fail,Write(c,v)), which may lose the command after the sender stops retrying. Idempotent database state therefore does not establish protocol equivalence; duplicate external effects and premature acknowledgment remain observable production faults.
