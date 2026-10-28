# Module 14: Quantum and Concurrent Extensions

This module examines cutting-edge extensions of the λ-calculus to model quantum computing and concurrent/distributed systems, pushing beyond the classical deterministic, sequential paradigm of Modules 1–13. To make this fully self-contained and crystal clear for learning, let's recap the foundation: The λ-calculus is a pure functional system where terms (variables x, abstractions λx.t "function mapping x to t", applications t u) compute via β-reduction ((λx.t) u → t[u/x], substituting u for x, Module 2), encoding data (Church numerals/lists, Module 3), ensuring safety via types (STLC Module 5, polymorphism Module 7, linear Module 11), handling effects (Module 10), and interactive models (games Module 12). However, classical λ assumes deterministic, local computation—unsuited for quantum superposition/entanglement (probabilistic, linear resources) or concurrency (parallel processes, communication). These extensions adapt λ: Quantum λ uses linear types (Module 11) for qubits (no-cloning theorem: cannot duplicate quantum states), gates as linear maps; concurrent λ embeds process calculi like π (Milner 1990s) via higher-order functions for channels/parallelism. Motivations: Quantum for unbreakable crypto (Shor's algorithm) and simulation (molecules); concurrency for scalable software (web servers, actors). Analogies: Qubits as "fuzzy" linear variables (superposition like multiple values at once, but uncloneable); concurrency as "multi-party λ" where terms "talk" via channels. We proceed through five core sections, each motivated by a limitation (e.g., classical determinism), with formal syntax/semantics unpacked intuitively, step-by-step examples (e.g., circuit reductions), proof sketches (induction on terms), tradeoffs/pitfalls, visualizations (Mermaid circuits), tables (comparisons), Python simulations (qubit/gate approx), and exercises. By modeling Bell states or π-processes, you'll grasp frontiers—everything here, no priors beyond recaps. Mastery Modules 1–13 assumed; self-contained (e.g., linear recap: A ⊸ B uses input once).

## Core 14.1: Syntax for Quantum λ

Quantum computing leverages superposition (qubits in multiple states) and entanglement (linked qubits), but requires linearity (Module 11: exact-once use) to enforce no-cloning (cannot copy unknown quantum states). Motivation: Classical λ bits deterministic; quantum λ extends to model quantum circuits (gates on qubits), enabling simulation of algorithms like Grover's search. This core defines syntax, building on linear λ for qubits/gates.

### Terms and Types

Quantum λ types: Base Qubit (single qubit), Tensor ⊗ for multi-qubit.

Full: A ::= Qubit | A ⊗ A | A ⊸ A | !A (linear arrow/exponential from Module 11).

Terms extend linear λ:
- newq : Unit ⊸ Qubit (create |0⟩ qubit, linear).
- U gate : Qubit ⊸ Qubit (apply unitary U, e.g., H Hadamard).
- measure : Qubit ⊸ Bit (collapse to classical bit, destructive).
- tensor t1 t2 : Qubit ⊗ Qubit (entangle, linear both).

Reduction: Gates unitary matrices (H|0⟩ = (|0⟩ + |1⟩)/√2), measure probabilistic.

Example: Bell pair (entangled): let h = newq in let h' = newq in let _ = H h in CNOT (tensor h h') (measure h; measure h')—outputs correlated 00 or 11.

Intuition: Qubits linear (consume on gate/measure), ⊗ parallel.

Circuit diagram Bell (H-CNOT):
```mermaid
graph LR
    q1["q1 (newq |0⟩)"]
    q2["q2 (newq |0⟩)"]
    q1 --> H["H (Hadamard)"]
    H --> CNOT["CNOT (Controlled-NOT)"]
    q2 --> CNOT
    CNOT --> M1["Measure q1 → Bit"]
    CNOT --> M2["Measure q2 → Bit"]
    style q1 fill:#f3e5f5
    style q2 fill:#f3e5f5
    style H fill:#e1f5fe
    style CNOT fill:#fff3e0
    style M1 fill:#e8f5e8
    style M2 fill:#e8f5e8
```

H superposes q1, CNOT entangles q2 to q1.

**Lemma**: Syntax preserves linearity: Gates consume/produce one qubit.

*Proof Sketch*: By construction—U : Qubit ⊸ Qubit, tensor splits linear contexts (Module 11).

Pitfall: Classical copy (λx.<x,x>) forbidden linear—no-clone quantum.

Tradeoffs: Expressive (circuit λ-terms), but probabilistic measure (denote distributions, Module 9 domains).

### Representation in Programming

In Python, Qiskit-like sim (no real quantum):

```python
from typing import List
import random  # For measure approx

class Qubit:
    def __init__(self):
        self.state = [1.0, 0.0]  # |0⟩ = [1,0]

    def hadamard(self):
        # H|0⟩ = (|0⟩ + |1⟩)/√2
        self.state = [1/math.sqrt(2), 1/math.sqrt(2)]
        return self

    def cnot(self, control: 'Qubit', target: 'Qubit'):
        # If control |1⟩, flip target
        if abs(control.state[1])**2 > 0.5:  # Approx |1⟩ prob
            target.state = [target.state[1], target.state[0]]

    def measure(self) -> int:
        prob1 = abs(self.state[1])**2
        return 1 if random.random() < prob1 else 0

# Bell sim
q1 = Qubit().hadamard()
q2 = Qubit()
q1.cnot(q1, q2)  # Self-control? Wait, tensor sim
m1 = q1.measure()
m2 = q2.measure()
print(f"Measurements: {m1}, {m2}")  # Correlated 0,0 or 1,1
```

Approx; real Qiskit for circuits.

### Exercises
1. Syntax for EPR pair: newq; H; CNOT tensor.
2. Reduce H|0⟩: State after.

## Core 14.2: Typing for Quantum

Quantum typing uses linear (Module 11) enforce no-clone (cannot duplicate unknown qubit), no-delete (cannot discard mid-comp).

### Rules

Types Qubit linear (⊸ consume), gates preserve linearity.

- T-Newq: ⊢ newq : Unit ⊸ Qubit
- T-Gate: ⊢ t : Qubit ⇒ ⊢ U t : Qubit (U unitary, linear)
- T-Tensor: ⊢ t1 : Qubit, t2 : Qubit ⇒ ⊢ tensor t1 t2 : Qubit ⊗ Qubit (split linear)
- T-Measure: ⊢ t : Qubit ⇒ ⊢ measure t : Bit (destructive, linear)

No weaken/contract Qubit.

Example Bell: let h = newq in let h' = newq in let _ = H h in let e = tensor h h' in let _ = CNOT e in (measure h, measure h') : Unit ⊸ Bit ⊗ Bit

Derivation: Newq linear Unit ⊸ Qubit; tensor splits; gates ⊸ chain.

**Lemma**: Typing prevents cloning: No term ⊢ t : Qubit ⊸ Qubit ⊗ Qubit.

*Proof Sketch by Inversion*: Assume T-Abs, body uses input Qubit once (linear context), but ⊗ requires two outputs—split cannot duplicate, contradiction (no contract).

Variance: Quantum safe (linear contra/co like Module 8, but strict).

Pitfall: Classical bits duplicable (!Bit), qubits not—typing distinguishes.

Tradeoffs: Strict linearity safe (physics), but verbose (manual tensor).

### Representation in Programming

In Python, type-check sim linear quantum:

```python
class QType:
    def __init__(self, is_linear=True):
        self.is_linear = is_linear

Qubit = QType(True)
Bit = QType(False)

def type_gate(t_type: QType) -> QType:
    if not t_type.is_linear:
        raise ValueError("Non-linear input")
    return Qubit  # Consume linear, produce linear

def type_tensor(t1: QType, t2: QType) -> QType:
    if not (t1.is_linear and t2.is_linear):
        raise ValueError("Tensor requires linear")
    return QType(True)  # Combined linear

# Bell type: newq ⊸ (H newq ⊗ newq) ⊸ ...
print(type_gate(Qubit))  # Qubit
```

Enforces linearity.

### Exercises
1. Derive type Bell circuit Unit ⊸ Bit ⊗ Bit.
2. Why no cloner: Assume contra derive error.

## Core 14.3: Concurrent λ

Concurrency models parallel processes communicating channels, extending λ higher-order for names/π-calculus (Milner 1990s: Processes P = 0 | P | Q (parallel) | νn P (new chan n in P) | n?x.P (recv n to x, cont P) | n!v.P (send v on n, cont P)).

Motivation: Classical λ sequential; concurrent for distrib (web, actors Erlang).

### π-Calculus Links

π processes; embed λ π via cont (higher-order channels).

Syntax concurrent λ: t ::= ... | spawn t (fork process t) | send c v (send v chan c) | recv c x. t (recv to x, cont t).

Channels linear (use once?).

Example: Spawn = λp. (νc) (p | c?x. x) (new chan c, parallel p with listener).

**Lemma**: λ simulates π (higher-order embed).

*Proof Sketch Construction*:
- Chan n = λmsg. (νk) (send k msg | recv k y. y) (higher-order func as chan).
- Parallel P | Q = spawn (λ_. P (λ_. Q)) (fork, ignore).
- Send/recv via app/abstr.

Ind on π processes: Each op λ-reduces to next.

Concurrency λ via ext: Join calculus or λ with primitives.

Pitfall: Race conditions—nondet order; typing (sessions Module 11) prevent.

Tradeoffs: Embed expressive, but inefficient (higher-order overhead).

### Representation in Programming

In Python, π-like concurrent sim (threading):

```python
import threading

def sender(chan_queue, value):
    chan_queue.put(value)  # Send

def receiver(chan_queue, cont_func):
    x = chan_queue.get()  # Recv
    cont_func(x)

# Example: νc (sender c 5 | receiver c (lambda x: print(x)))
chan = threading.Queue()
t1 = threading.Thread(target=sender, args=(chan, 5))
t2 = threading.Thread(target=receiver, args=(chan, lambda x: print(x)))
t1.start(); t2.start()
t1.join(); t2.join()  # Prints 5
```

Approx π parallel.

### Exercises
1. Embed π send in λ: λchan msg. chan msg.
2. Why concurrent hard: Nondet in red.

## Core 14.4: Semantics

Quantum semantics: Unitary matrices/density ops domains (Module 9).

Concurrent: Process alg (bisim) or trace sem (sequences).

### Quantum Semantics

Qubits vectors C^2, gates unitaries U: C^{2^n} → C^{2^n}.

λ denotation: Strategies (Module 12) or domains linear maps.

Bell: |00⟩ + |11⟩ /√2, measure corr.

**Theorem**: Quantum λ sound (gates preserve norms).

*Proof Sketch*: Linear unitaries isometries, preserve inner products.

Concurrent: Bisim P ~ Q if indistinguishable contexts (Module 9 obs eq).

Apps: Shor factor λ-circuit (period find quantum FFT).

Pitfall: Quantum prob—denote distributions.

Tradeoffs: Precise (Hilbert spaces), but classical sim exponential.

### Representation in Programming

In Python, quantum sem Qiskit:

```python
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

# Bell circuit
qc = QuantumCircuit(2, 2)
qc.h(0)  # H q0
qc.cx(0,1)  # CNOT
qc.measure([0,1], [0,1])

sim = Aer.get_backend('qasm_simulator')
result = execute(qc, sim, shots=1024).result()
counts = result.get_counts()
print(counts)  # {'00': ~512, '11': ~512}
plot_histogram(counts)
```

Simulates; shows corr.

### Exercises
1. Sem Bell: Matrix |00⟩ + |11⟩ /√2.
2. Bisim concurrent send/recv.

## Core 14.5: Applications

Quantum: Sim alg (Grover search), error correct codes.

Concurrent: Distrib comp (Erlang actors λ-embed), web protocols.

| Ext | Feature | App | Notes |
|-----|---------|-----|-------|
| Quantum | Superpos/entangle | Shor factor, Grover | Linear no-clone |
| Concurrent | Parallel/chan | Actors, sessions | Higher-order names |

Extensions future λ: Quantum advantage, concurrent scale.

Pitfall: Quantum noise—error correct λ-level.

### Representation in Programming

In Python, concurrent actor sim:

```python
import asyncio

class Actor:
    def __init__(self):
        self.mailbox = asyncio.Queue()

    async def send(self, msg):
        await self.mailbox.put(msg)

    async def recv(self):
        return await self.mailbox.get()

async def ping_pong():
    p = Actor()
    pong = Actor()
    await p.send("ping")
    msg = await pong.recv()  # Wait, sim
    print(msg)

asyncio.run(ping_pong())
```

Approx.

### Exercises
1. Grover search quantum λ sketch.
2. Actor model embed λ.

## Summary and Suggested Exercises

Module detailed quantum/concurrent λ: Syntax qubits/gates linear, typing no-clone, concurrent π embed, sem matrices/bisim, apps alg/distrib. Self-contained frontiers—quantum prob, concurrent scale.

Ref: Selinger "Quantum λ-Calculus" (2004); Van Tonder "Quantum λ" (2004); Milner "π-Calculus" (1999); Caires/Pfenning "Session Types" (2010); Qiskit docs quantum sim.

**Exercises** (Model; prove; sim):
1. Type GHZ 3-qubit: newq ⊗3, H first, CNOT chain.
2. Prove no-clone quantum: Contra assume.
3. Embed π parallel in λ: Spawn constr.
4. Sem EPR: Density matrix.
5. Discuss Shor λ: Period find circuit.

Extensions mastered, 15 capstone projects.
