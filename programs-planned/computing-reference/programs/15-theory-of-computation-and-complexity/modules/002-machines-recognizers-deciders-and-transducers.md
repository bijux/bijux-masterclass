---
module_id: TOCC-002
program: Theory of Computation & Complexity
level: 1
module_number: 2
title: Machines, Recognizers, Deciders, and Transducers
status: complete
last_verified: 2026-08-29
---

# Machines, Recognizers, Deciders, and Transducers

## One-Page Review

### Governing question

How do formal machines turn finite inputs into runs, language judgments, or outputs, and which obligations distinguish acceptance, recognition, decision, and transduction?

### Essential definitions

- A **machine model** specifies configurations, legal initial configurations, a transition relation, and observable terminal outcomes.
- A **configuration** is a complete abstract snapshot needed to determine possible next steps: control state plus relevant input position, stack, tape, registers, or output.
- A **run/computation** is a finite or infinite sequence of configurations connected by legal transitions.
- An **acceptor** uses accepting runs to define a language.
- A **recognizer** (semidecider) for $L$ accepts exactly strings in $L$; on a nonmember it may reject or run forever.
- A **decider** for $L$ halts on every input, accepting members and rejecting nonmembers.
- A language is **Turing-recognizable** if some Turing-equivalent machine recognizes it and **decidable** if some such machine decides it.
- A **transducer** maps inputs to outputs rather than only yes/no verdicts. It may be partial, total, deterministic, nondeterministic, functional, or relational.
- A **deterministic** transition system has at most one next configuration per nonterminal configuration; a **nondeterministic** one may branch.
- **divergence** is an infinite run or failure to reach a required result. It is not the same as rejection.

### Central model, mechanism, or theorem

Represent a machine operationally as

$$
M=(C,init,\longrightarrow,F_{acc},F_{rej},out),
$$

where $C$ is the configuration set, $init(w)$ begins input $w$, $\longrightarrow$ is the step relation, and terminal configurations may accept, reject, or produce output.

The recognized language is

$$
L(M)=\{w\in\Sigma^*\mid init(w)\longrightarrow^* c
\text{ for some }c\in F_{acc}\}.
$$

A decider additionally requires every maximal computation on every input to terminate with a defined verdict under the model’s nondeterminism convention. For deterministic machines this means the unique run halts. Every decider is a recognizer; not every recognizer is a decider.

### Critical invariants

- Fix input alphabet, malformed-input policy, initial configuration, transition semantics, and acceptance convention.
- Distinguish machine description, configuration, one step, run, and mathematical function/language induced by all runs.
- Acceptance means reaching an accepting outcome; halting alone may reject, error, or produce output.
- A recognizer has one-sided termination: member inputs must be accepted; nonmembers need not halt.
- A decider’s totality obligation ranges over all input strings, not just examples or valid-looking cases.
- Under existential nondeterministic acceptance, one accepting branch suffices; an infinite or rejecting branch does not erase it.
- A runtime timeout supplies bounded non-observation, not proof of nonmembership or divergence.
- Transducer output semantics must say when output is committed and whether multiple outputs are permitted.
- Machine power depends on storage/access restrictions, not on state names or diagram aesthetics.
- Implementation experiments illustrate finite cases; they do not prove unbounded language classification.

### Common failures

Common failures include calling every program a decider; treating nontermination as reject; treating timeout as proof of looping; defining a recognizer only on yes-instances; forgetting malformed inputs; assuming nondeterminism means randomness; requiring every nondeterministic branch to accept; accepting because one prefix reached an accepting state when the model requires full-input consumption; confusing a machine’s finite description with finite configuration space; calling an output-producing program an acceptor without specifying its relation; assuming a transducer is total or functional; and inferring computability or complexity from a few executions.

### Compact example

A machine for strings containing a `1` can scan left to right, accept as soon as it sees `1`, and reject at end of input otherwise. It halts on every binary string, so it decides the language. A recognizer for a more difficult language might accept when it discovers a certificate but search forever when none exists; absence of discovery is not rejection. A bit-complement transducer instead emits one output symbol per input symbol and has no inherent yes/no language until an acceptance predicate is added.

### Connections

[TOCC-001](./001-alphabets-strings-languages-and-decision-problems.md) supplies strings, languages, and decision problems. [TPROG-002](../../07-programming-languages-theory-of-programming/modules/002-natural-deduction.md) relates transition rules to derivations. [COMP-001](../../08-compilers-and-language-implementation/modules/001-language-implementation-pipelines.md) uses recognizers and transducers in implementation pipelines. [TOCC-003](../ROADMAP.md) makes machine and instance encodings effective.

## Governing Question

What exactly must a formal machine do on every input for us to say that it recognizes a language, decides a problem, or computes an output—and how do its configurations, storage, branching, and terminal conventions support that claim?

The word “machine” is not a physical claim. It is a mathematical transition system chosen to expose capabilities and limits. A finite automaton, pushdown automaton, Turing machine, register machine, circuit, grammar recognizer, and program semantics can all be described through configurations and steps, yet their storage and observation rules induce different language classes and functions.

## Why This Matters

Computability proofs fail when acceptance, halting, and rejection are blurred. A program that eventually confirms every yes-instance may still run forever on no-instances; it recognizes but does not decide. This distinction later supports the halting problem, reductions, enumerable languages, and the boundary between partial and total computation.

The same discipline matters in engineering. Parsers are recognizers with diagnostic/output behavior; protocol controllers are finite-state transducers; compilers transform strings/trees; model checkers explore branching transition systems; services can return, reject, fail, or never respond. Formal terminology prevents a timeout policy from being mistaken for a proof of nonmembership or a partial implementation from being advertised as total.

Machine models also separate finite descriptions from potentially unbounded behavior. A Turing machine has finitely many states and transition rules, but its tape yields infinitely many possible configurations. A pushdown automaton has finite control and an unbounded stack. A finite automaton has only finite control. The storage boundary, not the diagram size alone, explains power.

## Prerequisites and Retrieval

Retrieve:

- finite alphabet, string, empty string, language, complement, and language membership;
- relation, function, partial function, total function, domain, range, and composition;
- directed graph, path, reachability, finite/infinite sequence, and reflexive-transitive closure;
- predicate, existential/universal quantification, implication, and counterexample;
- state, transition, stack, tape, input cursor, output buffer, and invariant;
- deterministic algorithm, termination, error, malformed input, and timeout.

You should be able to distinguish $w\in L$ from “a procedure has so far not accepted $w$,” and explain why a finite ruleset can generate an infinite run.

## Learning Objectives

After completing this module, you should be able to:

1. define a machine through configurations, initialization, transition relation, and observations;
2. trace deterministic and nondeterministic computations step by step;
3. distinguish acceptance, rejection, halting, error, stuckness, and divergence;
4. derive the language recognized by an acceptor under a stated acceptance convention;
5. prove that a machine is a decider by showing correctness and termination on all inputs;
6. distinguish recognizers from deciders and prove basic relationships between recognizable and decidable languages;
7. define deterministic and relational transducers, including partiality and output commitment;
8. compare finite-control, stack, bounded-tape, and unbounded-tape machine resources;
9. diagnose invalid timeout, sampling, nondeterminism, and malformed-input arguments;
10. constrain high-consequence uses of formal machines with model validation and qualified human authority.

## Core Exposition

### Start from configurations, not pictures

A state diagram often hides the data that makes a transition possible. For a deterministic finite automaton, a configuration can be $(q,i)$: control state and input position. For a pushdown automaton it also includes stack content. For a single-tape Turing machine it includes control state, entire finite nonblank tape content, and head position. For a transducer it may include accumulated output.

The transition relation $c\to c'$ defines one legal computation step. Its reflexive-transitive closure $c\to^*c'$ means zero or more steps. A run begins at $init(w)$ and follows transitions. It can:

- enter an accepting terminal configuration;
- enter a rejecting terminal configuration;
- enter an error/stuck configuration if the model permits one;
- continue forever;
- branch into several possible successor runs in a nondeterministic model.

These outcomes must be defined, not inferred from implementation behavior. A missing transition in a DFA is often completed by an implicit rejecting sink; a missing rule in another semantics may mean stuck/error. Full input consumption may be required before acceptance. State the convention.

### Acceptance defines a language

For existential nondeterministic acceptance, $w$ is accepted if at least one finite run from $init(w)$ reaches $F_{acc}$. Then $L(M)$ is the set of accepted strings. Rejected, stuck, and divergent runs do not themselves add a string to the language.

This definition is extensional: two machines recognize the same language if they accept exactly the same strings, even when their internal steps, rejection behavior, or running times differ. Machine equivalence can therefore mean language equivalence, function equivalence, trace equivalence, or bisimulation; never use “equivalent” without the observation.

An acceptance convention matters. A pushdown automaton may accept by final state or empty stack; standard constructions relate these conventions under stated definitions. A transducer may produce output before it accepts. A Turing-style machine may halt in a designated accept state. Later modules give model-specific definitions; the current abstraction makes their common obligations visible.

### Recognizers provide one-sided evidence

A recognizer $R$ for $L$ satisfies:

$$
w\in L\Rightarrow R(w)\text{ eventually accepts},
$$
$$
w\notin L\Rightarrow R(w)\text{ never accepts}.
$$

On a nonmember, it may explicitly reject or run forever. Thus a finite accepting computation is evidence of membership, while waiting without acceptance is not evidence of nonmembership.

Recognizers correspond naturally to effective witness search. Enumerate candidate derivations or certificates; verify each; accept when one works. If a witness exists and enumeration is fair, acceptance eventually occurs. If none exists, search continues. This idea underlies recursively enumerable/Turing-recognizable languages, although model-specific equivalences are proved later.

A recognizer must still be specified for every input string. “For members, run this process” is incomplete because it gives no operational behavior on nonmembers or malformed strings. It may be a valid partial algorithm after those cases are defined, but its recognition proof must exclude false acceptance.

### Deciders require total termination and correctness

A decider $D$ for $L$ has a total characteristic behavior:

$$
D(w)=
\begin{cases}
accept & w\in L,\\
reject & w\notin L,
\end{cases}
\quad\text{and }D\text{ halts for every }w\in\Sigma^*.
$$

Proving decision requires two independent obligations:

1. **partial correctness:** whenever the machine returns accept/reject, that verdict matches membership;
2. **termination:** every permitted computation reaches a verdict on every input.

Testing many cases cannot discharge universal termination. Typical proofs use a decreasing well-founded measure, bounded input consumption, finite configuration exploration with visited-state detection, structural recursion, or a known terminating subroutine. “No loop was observed” is not a termination proof.

For deterministic machines, one run must halt. For nondeterministic “decider” conventions, clarify whether all branches halt and whether acceptance is existential. A breadth-first dovetailing simulator can sometimes turn branching search into a deterministic recognizer, but infinite branching or unfair depth-first search can invalidate naive arguments.

### Every decider recognizes, but the converse can fail

If $D$ decides $L$, using $D$ as a recognizer works immediately: it accepts members and rejects nonmembers. Therefore every decidable language is recognizable.

The converse is not true in Turing-complete models: some languages are recognizable but not decidable. The recognizer’s divergence on nonmembers is exactly the missing negative decision procedure. This is not shown merely by presenting a loop; later undecidability proofs establish that no alternative decider exists.

Decidable languages are closed under complement at this elementary level. Given decider $D$ for $L$, run it and swap accept/reject. Termination is preserved, so the new machine decides $\overline L$.

A deeper characterization is:

$$
L\text{ decidable}\iff L\text{ and }\overline L
\text{ are both recognizable}.
$$

The forward direction uses complement closure. For the reverse direction, dovetail recognizers $R_L(w)$ and $R_{\overline L}(w)$: simulate one step of each alternately. Exactly one side contains $w$, so its recognizer eventually accepts; return the corresponding verdict. Sequentially running $R_L$ first is wrong because it may diverge before $R_{\overline L}$ gets a step.

### Halting, rejection, error, and timeout differ

Halting means no further machine step is taken under the model. A halt may accept, reject, produce an output, or signal an error. A stuck configuration may count as rejection in one automaton convention and an undefined computation in another.

Divergence is a property of an infinite computation. A finite observation cannot generally establish it. A wall-clock timeout implements a new total policy:

$$
D_T(w)=
\begin{cases}
M(w)\text{ verdict} & \text{if observed within }T,\\
timeout & \text{otherwise}.
\end{cases}
$$

If timeout is coerced to reject, $D_T$ decides a bounded operational approximation, not necessarily $L(M)$. A member whose accepting run needs more than $T$ becomes a false rejection. Time bounds can be valid when proved from input size/model; an arbitrary operational deadline is not a computability theorem.

### Determinism and nondeterminism are semantic choices

Determinism means each applicable configuration has at most one successor. Nondeterminism means the transition relation may offer several. It is mathematical branching, not probabilistic choice unless probabilities are added.

For language recognition under existential semantics, an accepting branch suffices. A concrete implementation cannot simply “guess correctly”; it simulates branches by breadth-first search, dovetailing, subset construction, dynamic programming, or model-specific methods. Whether this preserves machine power and how much time/space it costs depends on the model.

Universal branching—accept only if every branch accepts—defines another semantics. Alternating and probabilistic machines introduce still others. Always state branch quantification. A diagram with two outgoing edges is not enough.

### Transducers compute outputs

An acceptor induces a predicate/language. A deterministic transducer induces a partial function

$$
f_M:\Sigma^*\rightharpoonup\Gamma^*,
$$

where $f_M(w)=y$ only if the computation terminates successfully with committed output $y$. A total transducer terminates with one output for every valid input (and has a stated malformed-input policy).

A nondeterministic transducer can induce a relation

$$
T_M\subseteq\Sigma^*\times\Gamma^*,
$$

containing every input/output pair produced by an accepting run. It is functional only if each input relates to at most one output, even if several runs produce that same output. It is total on a domain if every domain input has at least one output.

Output timing matters. A Mealy-style finite transducer labels transitions with output; a Moore-style machine associates output with states. A Turing transducer can write an output tape. Streaming output may be externally irreversible before later rejection, so an abstract “output on halt” function may not model actual traces. Choose value, trace, or transactional semantics according to the claim.

### Machine storage determines capability

Compare common resources:

- **finite-state machine:** finite control, no unbounded auxiliary memory; configuration count is bounded by state and finite input position for a fixed input;
- **pushdown machine:** finite control plus an unbounded last-in/first-out stack; can retain nested structure;
- **linear-bounded machine:** tape/storage bounded linearly by input length under a conventional model;
- **Turing machine:** finite control plus unbounded (but finitely used at each finite time) read/write tape;
- **transducer variants:** attach output to any of these storage models.

“Unbounded” is mathematical potential, not infinite material present at a moment. An individual terminating run uses finite time and visits finitely many cells. Model comparisons later require explicit simulations and encodings; informal statements that “more memory is stronger” are not proofs.

### Programs implement machines only relative to an abstraction

A program with finite hardware state is technically a finite transition system, yet theory often idealizes unbounded integers/memory to study algorithms independent of a fixed device limit. State the abstraction. Implementation integers overflow; queues fill; operating systems interrupt; processes crash.

When a parser, controller, or compiler is called a recognizer/transducer, identify observable semantics and resource assumptions. Error recovery can make a parser a relation from malformed inputs to diagnostics/trees, not merely a language acceptor. A compiler that terminates only on valid source is a partial transducer unless invalid-input behavior is defined.

## Definitions and Notation

Let $C$ be configurations and $\to\subseteq C\times C$ the step relation. Write $\to^*$ for its reflexive-transitive closure. A run on $w$ is $c_0,c_1,\ldots$ with $c_0=init(w)$ and $c_i\to c_{i+1}$.

A finite run is **maximal** if its last configuration has no successor. An infinite run is maximal automatically. Terminal outcome sets $F_{acc},F_{rej},F_{err}$ should be disjoint. Under existential acceptance:

$$
Accept_M(w)\iff\exists c\in F_{acc}:init(w)\to^*c.
$$

For deterministic $M$, define:

$$
Recognizes(M,L)\iff
\forall w\,[Accept_M(w)\leftrightarrow w\in L].
$$

$$
Decides(M,L)\iff Recognizes(M,L)\land
\forall w\,\exists c\in F_{acc}\cup F_{rej}:init(w)\to^*c,
$$

assuming the terminal sets and transition semantics ensure a unique verdict. For nondeterministic decider definitions, add the exact all-branches termination and branch-acceptance convention.

A deterministic transducer’s partial function is $f_M(w)=out(c)$ when its unique run reaches a successful output terminal $c$; otherwise undefined. A relational transducer has

$$
\mathcal{T}_M=\{(w,y)\mid init(w)\to^*c,\ c\text{ is output-accepting},\
out(c)=y\}.
$$

## Mechanisms, Invariants, or Proof Structure

Analyze or construct a machine with this discipline:

1. **Fix the problem:** alphabet, valid/malformed inputs, language or input/output relation.
2. **Choose a model:** finite control, stack, bounded/unbounded tape, counters, and output mechanism.
3. **Define configurations:** include every component on which a next step depends.
4. **Define initialization and transitions:** specify determinism, branching, end markers, and missing-rule behavior.
5. **Define observations:** accepting/rejecting/error terminals, full-input rule, output value/trace, and commitment.
6. **Trace representative runs:** member, nonmember, empty, malformed, boundary, and divergent/branching cases.
7. **Prove soundness:** every accepted input/output satisfies the specification.
8. **Prove completeness:** every specified member/output has an accepting computation.
9. **Prove totality when claiming decision/function:** all relevant computations terminate with defined results.
10. **State limits:** storage abstraction, encoding, resource bounds, implementation correspondence, and unproved claims.

The invariants are legal-step preservation, explicit terminal meaning, no divergence-as-rejection, branch quantification, totality only with proof, and output relation/function distinction.

This finite-state machine is simultaneously a total transducer on binary strings and a decider for strings containing an even number of `1` symbols. It complements each bit while tracking parity. Invalid symbols follow a separate malformed-input policy. The execution proves only these listed finite traces and the code path; the general classification follows from the transition invariant, not sampling.

<!-- bijux-verify: {"id":"parity-complement-transducer","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input=ε output=ε final=even verdict=accept\ninput=101 output=010 final=even verdict=accept\ninput=111 output=000 final=odd verdict=reject\ninput=10x verdict=error symbol=x\n","stderr":""}} -->
```python
def run_machine(text):
    state = "even"
    output = []
    for symbol in text:
        if symbol not in {"0", "1"}:
            return f"input={text or 'ε'} verdict=error symbol={symbol}"
        output.append("1" if symbol == "0" else "0")
        if symbol == "1":
            state = "odd" if state == "even" else "even"
    verdict = "accept" if state == "even" else "reject"
    rendered_input = text or "ε"
    rendered_output = "".join(output) or "ε"
    return (
        f"input={rendered_input} output={rendered_output} "
        f"final={state} verdict={verdict}"
    )

for sample in ("", "101", "111", "10x"):
    print(run_machine(sample))
```

Loop invariant after consuming prefix $x$: state is `even` exactly when $x$ contains an even number of ones, and accumulated output is the bitwise complement of $x$. Each transition preserves it. Finite input consumption proves termination, so binary inputs receive both a total output and a correct parity verdict.

## Alternatives and Trade-Offs

**Acceptor versus transducer.** Acceptor models focus language membership and support clean class theory. Transducers capture parsers, compilers, protocols, and functions but require output equality/relation and commitment semantics. Add only observations needed for the question.

**Explicit reject versus stuck-as-reject.** Explicit reject states make proofs and implementations clear. Implicit rejection can simplify diagrams but risks confusing malformed, incomplete, and negative cases. Complete the transition system or state the convention.

**Deterministic versus nondeterministic models.** Nondeterminism expresses existential search concisely and can reveal structural classes. Deterministic machines match direct execution. Equivalence in language power does not imply equal succinctness or resource cost; prove model-specific simulations.

**Final-state versus empty-storage acceptance.** Alternative conventions can be equivalent for a machine class under constructions, but mixing them within a proof changes the language. Declare one and show conversions rather than assuming.

**Partial recognizer versus total decider.** A recognizer may be easier or the strongest computable result. A decider gives reliable negative answers but requires a termination argument. Operationally imposing a timeout changes the specification rather than proving totality.

**Value versus trace transduction.** Final output abstracts intermediate effects and supports function reasoning. Trace semantics exposes streaming, rollback, retries, and interaction but enlarges equivalence proofs. Use transactional value semantics only when intermediate output is unobservable or controlled.

**Idealized unbounded versus finite implementation state.** Unbounded models yield robust asymptotic/computability theory. Bounded implementations support exhaustive exploration in principle but can be astronomically large and differ across platforms. Keep model correspondence explicit.

## Failure Modes and Misconceptions

- **“A machine is its diagram.”** The semantics include configurations, transition rules, input/end conventions, storage, and observations.
- **“Finite description means finitely many configurations.”** Stacks, tapes, counters, and input positions can generate unbounded configuration sets.
- **“It halted, so it accepted.”** Halting can reject, error, or output; accepting states are designated.
- **“It did not accept, so it rejected.”** It may still be running, stuck under another convention, or awaiting a branch.
- **“A timeout detects nontermination.”** It only detects failure to finish within a bound.
- **“A recognizer answers membership.”** It confirms members eventually but may never answer nonmembers.
- **“A decider works on valid examples.”** Totality covers every string and malformed-input policy.
- **“Nondeterminism is randomness.”** Branching has existential/universal semantics unless probabilities are defined.
- **“Every nondeterministic branch must accept.”** Not under standard existential language acceptance.
- **“One accepting prefix is sufficient.”** Only if the acceptance convention permits early acceptance; many automata require input consumption.
- **“A transducer always computes a function.”** Nondeterminism may yield multiple outputs; divergence makes it partial.
- **“Same accepted language means identical machines.”** They may differ in outputs, traces, termination on nonmembers, and resources.
- **“A looping recognizer proves undecidability.”** It proves that implementation is not a decider, not that no decider exists.
- **“Simulation on large samples proves the language.”** Universal soundness/completeness and termination need mathematical arguments.

## Worked Examples

### Example 1

**Question:** A machine halts in state `q_done`. Did it accept?

**Reasoning:** A state name has no semantics by itself. If `q_done∈F_acc`, yes; if it is rejecting or output-only, no. If terminal sets were never declared, the machine specification is incomplete.

**Conclusion:** Halting and acceptance are distinct observations.

### Example 2

**Question:** A binary-string procedure scans to the end and accepts exactly when the count of ones is even. Is it a decider?

**Reasoning:** The parity invariant proves the verdict. Each step advances the input cursor, so after $|w|$ steps it reaches the end for every binary string. A separate finite malformed-input path handles nonbinary symbols.

**Conclusion:** Correctness plus a decreasing remaining-length measure establishes decision.

### Example 3

**Question:** A procedure enumerates all proofs in a sound formal system and accepts when it finds a proof of formula $\varphi$. What kind of machine is it?

**Reasoning:** If proof checking and fair enumeration are effective, provable $\varphi$ is eventually accepted. If no proof exists, enumeration may continue forever. It recognizes the set of provable formulas; it decides it only with an additional terminating negative method.

**Conclusion:** Effective witness enumeration naturally yields recognition, not automatically decision.

### Example 4

**Question:** Can a five-second timeout turn any recognizer into a decider for its language?

**Reasoning:** It makes the implementation terminate, but it rejects members whose accepting computation needs more than five seconds. The new machine decides “accepted within five seconds under this execution model,” not the original language.

**Conclusion:** Operational totality obtained by cutoff can destroy semantic correctness.

### Example 5

**Question:** A nondeterministic machine has one accepting branch, one rejecting branch, and one infinite branch. Is the input accepted?

**Reasoning:** Under existential acceptance, yes: the finite accepting run is enough. Under universal acceptance, no. Under a probabilistic model, probabilities are needed. The problem is under-specified until branch semantics are named.

**Conclusion:** Branch quantification is part of the machine definition.

### Example 6

**Question:** Why does running recognizer $R_L$ to completion and then $R_{\overline L}$ not decide $L$?

**Reasoning:** If $w\notin L$, $R_L(w)$ may diverge, so the complement recognizer never starts. Alternating one simulation step of each is fair. Exactly one recognizer must eventually accept, yielding the correct verdict.

**Conclusion:** Dovetailing, not sequential composition, converts two complementary recognizers into a decider.

### Example 7

**Question:** A nondeterministic transducer emits `ab` on one accepting run and `ba` on another for the same input. Does it compute a function?

**Reasoning:** Its induced relation contains both $(w,ab)$ and $(w,ba)$. Because one input has two distinct outputs, the relation is not functional unless an external selection/canonicalization rule changes the semantics.

**Conclusion:** Successful output does not imply functional transduction.

### Example 8

**Question:** A parser accepts valid programs and returns syntax trees but recovers from malformed input with diagnostics. Is it only a recognizer?

**Reasoning:** Validity acceptance defines a language, while tree/diagnostic production defines a richer transduction. Error recovery can yield several possible trees or partial outputs. Specify both acceptance and output/trace relations.

**Conclusion:** Practical processors often combine acceptor and transducer semantics.

### Example 9

**Question:** A formally proved finite-state controller decides whether an infusion pump may start. Does that prove clinical safety?

**Reasoning:** The proof can establish transition properties of the modeled inputs/states. It cannot alone validate sensor semantics, drug units, workflow, hardware faults, hazards, patient populations, timing correspondence, or acceptable residual risk. No external academic, clinical, safety, regulatory, or practitioner review is claimed. Named qualified clinical, pharmacy, safety, human-factors, hardware, software, cybersecurity, quality/independent-assurance, and regulatory authorities must validate the model and authorize use.

**Conclusion:** Machine correctness is conditional on model correspondence and cannot replace high-consequence authority.

### Example 10

**Question:** Does a Turing machine use an actually infinite amount of tape on every input?

**Reasoning:** The model offers unbounded potential tape. After any finite number of steps, only finitely many cells have been visited. A terminating run therefore uses finite tape, although no single finite bound must cover every possible input.

**Conclusion:** Unbounded capacity is not completed infinity in one computation.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) interprets programs through transition systems and observable behavior.
- [Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md) supplies inference rules, operational semantics, partial correctness, and termination reasoning.
- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) composes lexical/syntactic recognizers and semantic/code transducers.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) implements terminating procedures and analyzes empirical/resource behavior without changing computability claims.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects abstract state machines to validated system boundaries and assurance.

## References

1. Michael Sipser. *Introduction to the Theory of Computation*, third edition, Cengage, 2013. Formal machine definitions, recognizers, deciders, transducers, decidability, and model equivalences.
2. John E. Hopcroft, Rajeev Motwani, and Jeffrey D. Ullman. *Introduction to Automata Theory, Languages, and Computation*, third edition, Pearson, 2006. Automata configurations, acceptance, transducers, grammars, and computability.
3. Alan M. Turing. [“On Computable Numbers, with an Application to the Entscheidungsproblem”](https://doi.org/10.1112/plms/s2-42.1.230), *Proceedings of the London Mathematical Society* 42, 1936, pp. 230–265; correction 43, 1937. Primary machine-based formulation of effective computation.
4. Michael O. Rabin and Dana Scott. [“Finite Automata and Their Decision Problems”](https://doi.org/10.1147/rd.32.0114), *IBM Journal of Research and Development* 3(2), 1959, pp. 114–125. Foundational deterministic/nondeterministic finite-automata theory.
5. George H. Mealy. “A Method for Synthesizing Sequential Circuits.” *Bell System Technical Journal* 34(5), 1955, pp. 1045–1079. Transition-output finite transducers.
6. Edward F. Moore. “Gedanken-Experiments on Sequential Machines.” In *Automata Studies*, Princeton University Press, 1956, pp. 129–153. State-output machines and distinguishability.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023*](https://doi.org/10.1145/3664191), endorsed 2024, Algorithmic Foundations—Computational Models and Formal Languages. Current curricular scope for finite-state, pushdown, linear-bounded, and Turing machines, languages, decidability, and halting; consulted 2026-08-29.

## Exercises

### Exercise 1

Given an abstract transition system, distinguish its description, configuration, step, run, terminal state, and recognized language.

### Exercise 2

Prove that the parity/complement machine in this chapter is a total transducer and a decider over binary strings.

### Exercise 3

Diagnose a team’s claim: “Our recognizer rejected the input because it did not finish in CI, so the language is decidable after adding a timeout.”

### Exercise 4

Prove both directions of: a language is decidable if and only if it and its complement are recognizable.

### Exercise 5

Specify and review an abstract controller/transducer for autonomous railway door authorization. Separate formal machine claims from system validation and human authority.

## Answers to the Exercises

### Answer 1

The description is the finite mathematical specification $M=(C,init,\to,F_{acc},F_{rej},out)$ or its model-specific equivalent. A configuration is one complete instantaneous abstract state, such as control, unread input, stack/tape/head, and accumulated output. A step is one pair in $\to$. A run is a finite or infinite sequence beginning at $init(w)$ with adjacent legal steps. A terminal configuration has no successor or is designated halting by convention; its membership in accept/reject/error/output sets determines meaning.

Under existential acceptance, the recognized language contains exactly inputs having some finite path from initialization to an accepting configuration. This language is an extensional observation of all runs, not the diagram, one trace, or the set of halting inputs.

### Answer 2

Invariant after reading prefix $x$: (1) state is even exactly when the number of `1` symbols in $x$ is even; (2) output equals the bitwise complement of $x$. Base $x=\epsilon$: zero ones is even and output is empty. On `0`, parity is unchanged and `1` is appended, preserving both clauses. On `1`, parity toggles and `0` is appended, also preserving both.

After the finite input is consumed, the invariant proves accept exactly for even parity and output exactly the complement. Each iteration consumes one symbol, so remaining length decreases to zero; therefore every binary input halts with one verdict and one output. Determinism makes the relation functional. A nonbinary symbol halts under the stated error policy, outside the binary transducer domain rather than silently rejecting parity.

### Answer 3

CI noncompletion can mean genuine divergence, slow finite computation, deadlock/resource/environment failure, unfair branch exploration, or lost evidence. A finite timeout cannot distinguish them. Coercing timeout to reject creates a total bounded procedure but may reject genuine members accepted after the deadline, violating recognizer correctness for the original language.

Preserve timeout as timeout/error, capture configuration/progress evidence, and state the bounded operational property. To claim a decider for the original language, prove partial correctness and termination for all inputs—perhaps by a decreasing measure or finite-state exploration. One looping implementation also cannot prove the language undecidable; that requires showing no decider exists, normally by reduction/diagonal argument.

### Answer 4

Forward: suppose $D$ decides $L$. It is already a recognizer for $L$. Construct $D^c$ that runs $D$, swaps accept and reject, and halts when $D$ halts. Since $D$ is total and correct, $D^c$ recognizes (indeed decides) $\overline L$.

Reverse: suppose $R$ recognizes $L$ and $S$ recognizes $\overline L$. On input $w$, dovetail their simulations: one step of $R(w)$, one of $S(w)$, repeatedly, retaining configurations. Because every string lies in exactly one of $L,\overline L$, the corresponding recognizer eventually accepts. If $R$ accepts, accept; if $S$ accepts, reject. Soundness prevents the wrong recognizer from accepting, and fair alternation prevents either divergence from starving the other. Thus the constructed machine halts correctly on every input and decides $L$.

### Answer 5

Define input alphabet/encoding for train identity, platform/side, localization, verified stop, speed, door state, obstruction sensors, command freshness, communication status, and degraded-mode authority. A configuration includes controller state plus all modeled inputs/history needed for the next transition. The transducer emits authorize/deny/fault and an auditable reason; acceptance can denote authorize. Specify deterministic/nondeterministic semantics, malformed/stale input, time, missing sensors, output commitment, fail-safe states, and termination.

Prove transition invariant such as “authorize implies modeled train is stopped within bound, correctly berthed, permitted side selected, command fresh/authenticated, and no modeled obstruction/fault.” Prove every input reaches authorize/deny/fault within the model’s step bound. Model-check finite abstractions and test implementation correspondence, boundaries, sensor faults, timing, and recovery. These prove only model-relative properties.

No external academic, railway, regulatory, safety, or practitioner review is claimed. Named qualified railway-domain, operations, control, safety, human-factors/accessibility, hardware/sensor, software, cybersecurity, quality/independent-assurance, and regulatory authorities must validate hazards, physical assumptions, sensor/actuator behavior, timing, degraded/manual/emergency modes, passenger behavior, evidence independence, residual risk, and release/change authority. An unresolved critical model-correspondence or hazard claim blocks deployment even if the abstract transition proof passes.
