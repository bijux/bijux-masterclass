---
module_id: ALGE-052
program: Algorithm Engineering
level: 2
module_number: 52
title: Knuth-Morris-Pratt
status: complete
last_verified: 2026-09-05
---

# Knuth-Morris-Pratt

## One-Page Review

### Governing question

How does Knuth-Morris-Pratt turn the borders of one pattern into a reusable failure mechanism that scans a text once, reports overlaps, and retains only pattern-sized state?

### Essential definitions

- A **border** of a sequence is a proper prefix that is also a suffix.
- The **prefix function** $\pi[i]$ is the length of the longest border of $P[0:i+1]$.
- A **matched length** $q$ means $P[0:q]$ equals the suffix of the text prefix processed so far.
- A **fallback** replaces $q$ with $\pi[q-1]$, the longest smaller candidate border, without moving backward in the text.
- A **failure chain** is $q,\pi[q-1],\pi[\pi[q-1]-1],\dots,0$.
- A **match transition** consumes one text symbol and increases $q$ by one.
- After a full match, setting $q=\pi[m-1]$ preserves the longest border and permits overlapping occurrences.
- A **streaming state** contains the immutable pattern, its prefix table, current $q$, and the absolute count of consumed symbols.

### Central model, mechanism, or theorem

After processing text prefix $T[0:i]$, maintain

$$
q=\max\{k\mid 0\le k\le m\land P[0:k]
=T[i-k+1:i+1]\}.
$$

When the next symbol conflicts with $P[q]$, any surviving candidate must be a border of the already matched pattern prefix, so follow $q\leftarrow\pi[q-1]$ until equality is possible or $q=0$. Text index $i$ never retreats. Prefix construction is $O(m)$, search is $O(n+z)$ including $z$ emitted matches, and stored matcher state is $O(m)$.

### Critical invariants

- $0\le\pi[i]\le i$ and $P[0:\pi[i]]=P[i-\pi[i]+1:i+1]$.
- Before consuming a text symbol, $q$ is the longest pattern prefix matching a suffix of the consumed text.
- Every fallback is a strictly shorter border, so failure traversal terminates.
- No occurrence ending before the current text position remains unreported.
- The text cursor advances exactly once per input symbol; only the pattern-state cursor falls back.
- After reporting a match, fallback to $\pi[m-1]$ retains overlap information.
- Stream boundaries do not reset $q$ or absolute position unless a new logical text begins.

### Common failures

Common failures include mixing prefix-function conventions; using $\pi[q]$ instead of $\pi[q-1]$; permitting the full string as its own border; incrementing the text cursor during fallback; resetting state between chunks; resetting $q$ to zero after a match and losing overlaps; reading $P[q]$ when $q=m$; changing pattern or equality semantics without rebuilding the table; reporting transformed offsets as original offsets; and claiming constant space while retaining all results.

### Compact example

For $P=\texttt{ababaca}$, $\pi=(0,0,1,2,3,0,1)$. If five symbols `ababa` have matched and the next text symbol is `b` rather than pattern `c`, KMP falls from $q=5$ to $\pi[4]=3$. The suffix `aba` is already known to equal the pattern prefix `aba`; the same text symbol is tested against $P[3]=\texttt{b}$ and extends the match to four without rereading text.

### Connections

[ALGE-051](./051-naive-and-prefix-based-pattern-matching.md) defines exact matching, derives the Z-prefix method, and fixes text semantics. [ALGE-053](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) develops right-to-left comparisons and skip heuristics. Automata theory explains KMP state, concurrent programming governs safe sharing of compiled patterns, and API engineering governs stream lifecycle and coordinate semantics.

## Governing Question

Given a fixed pattern and a resident or streaming text, how can we preprocess only the pattern, reuse every proved border after a mismatch, report all exact occurrences without backing up the input, and justify correctness, linear time, state lifecycle, and operational limits?

KMP is sometimes taught as a pair of memorized loops. That misses the central idea: the current matched prefix contains a complete, ordered set of candidates that could remain valid after failure. The prefix table encodes those candidates. The implementation is trustworthy when every index operation can be derived from that border invariant.

## Why This Matters

KMP provides deterministic linear worst-case search with $O(m)$ pattern-owned state. Unlike the direct Z reduction in [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md), it does not need the complete text or a text-sized array. This makes it a natural foundation for sockets, files, event streams, incremental parsers, and repeated searches with a compiled pattern.

The deeper lesson is state compression. The processed text can be discarded because all future-relevant information is summarized by one integer $q$: the length of its longest suffix that is also a pattern prefix. The prefix table makes mismatch recovery a transition among these summary states.

KMP controls comparison work under adversarial repetition, but it does not decide whether symbols are bytes, code points, grapheme clusters, or records. It also does not bound output volume, decoding cost, normalization buffering, or slow user-defined equality. Those remain explicit surrounding contracts.

## Prerequisites and Retrieval

Retrieve the exact-matching specification, overlap and empty-pattern policies, Z-values, borders, loop invariants, amortized analysis, finite-state machines, and streaming coordinates. Complete [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md) first. Review [ALGE-015](./015-heapsort.md) for array invariants and [ALGE-006](./006-best-worst-expected-and-amortized-cost.md) for aggregate charging.

This chapter uses zero-based arrays and half-open slices. It defines $\pi[i]$ as a length, not an index, and defines a border as proper. Other conventions can be correct, but combining formulas from different conventions is unsafe.

## Learning Objectives

After completing this module, you should be able to:

1. compute a pattern's prefix function by hand and in code;
2. derive every fallback from the border relation;
3. state and prove the prefix-table construction invariant;
4. state and prove the KMP search invariant;
5. explain why the text cursor never moves backward;
6. prove $O(m+n+z)$ total time with amortized reasoning;
7. preserve overlapping matches and cross-chunk state;
8. design a reusable compiled-pattern interface;
9. diagnose convention, indexing, mutation, and lifecycle faults; and
10. validate correctness and performance under boundary and adversarial inputs.

## Core Exposition

### Begin with borders

Let $P=P[0]P[1]\dots P[m-1]$. A border of $P[0:i+1]$ is a sequence $P[0:k]$ with $0\le k<i+1$ that also equals its suffix $P[i-k+1:i+1]$. The empty sequence, of length zero, is always a border. The complete substring is excluded because falling back to the same state would make no progress.

Define

$$
\pi[i]=\max\{k\mid 0\le k\le i\land
P[0:k]=P[i-k+1:i+1]\}.
$$

For $P=\texttt{ababaca}$, the prefixes yield $\pi=(0,0,1,2,3,0,1)$. At position 4 the substring `ababa` has longest border `aba`, length 3. At position 5 the substring `ababac` has no nonempty border, so its value is zero.

Borders nest. If a string has border length $q$, then every smaller border candidate is a border of $P[0:q]$. Consequently, after a mismatch following $q$ matched symbols, the next largest possible surviving matched length is $\pi[q-1]$.

### Construct the prefix table

Suppose $\pi[0:i]$ is already exact and we want $\pi[i]$. Let $q=\pi[i-1]$. The prefix $P[0:q]$ is the longest border of $P[0:i]$, the substring ending just before $P[i]$.

If $P[q]=P[i]$, append the new symbol to both equal sequences and set $\pi[i]=q+1$. If they differ, a border of length $q+1$ is impossible. The next candidate must be a border of the prefix of length $q$, so replace $q$ with $\pi[q-1]$ and try the same $P[i]$ again. Continue until a symbol matches or $q=0$. At zero, equality with $P[0]$ yields one; otherwise the result stays zero.

This construction applies KMP to the pattern itself. The processed prefix of $P$ acts as text, while the same prefix table provides failure transitions.

### Interpret KMP as a state machine

Search state $q\in\{0,\dots,m\}$ records how many leading pattern symbols match the suffix of all text consumed so far. Given next symbol $x$:

1. while $q>0$ and $P[q]\ne x$, set $q=\pi[q-1]$;
2. if $P[q]=x$, increment $q$;
3. if $q=m$, report a match ending at the current absolute position, then set $q=\pi[m-1]$.

The implementation must handle the full-match state before trying to access another $P[q]$. In the standard loop, reporting and fallback occur immediately, so the next input symbol sees $q<m$.

The fallback transition consumes no text. It changes only the interpretation of the already matched suffix. When a mismatch occurs after matching $P[0:q]$, the text suffix is exactly that prefix. Any shorter pattern prefix that could still match must also be a suffix of $P[0:q]$; its longest candidate has length $\pi[q-1]$.

### Preserve overlaps

Suppose $P=\texttt{aba}$ and $T=\texttt{ababa}$. After the match ending at text position 2, the matched pattern has border `a`, so $\pi[2]=1$. Keeping $q=1$ means the final `a` of the first occurrence is already the first `a` of a possible next occurrence. Processing text positions 3 and 4 then reports shift 2.

Resetting $q$ to zero after a match still finds nonoverlapping later matches, but it discards a valid suffix and can miss overlaps. Overlap behavior is therefore encoded in the post-match transition.

### Prove the search invariant

After consuming $T[0:i+1]$, define

$$
Q_i=\max\{k\mid 0\le k\le m\land
P[0:k]=T[i-k+1:i+1]\}.
$$

The invariant is $q=Q_i$ after reporting any complete match and applying its border fallback, except that the just-reported full length $m$ is represented by its longest proper border for future processing.

Assume the invariant before consuming $x=T[i]$. If $P[q]=x$, extending the longest suffix-prefix match yields length $q+1$. No longer candidate can exist, because removing its last symbol would contradict maximality of the previous $q$. If the symbols differ, length $q+1$ is impossible. Any surviving candidate is a border of $P[0:q]$, and the failure chain enumerates those borders from longest to shortest. The first one extendable by $x$ is therefore the new maximum. If none extends, the maximum is zero. A state of $m$ proves precisely that $P=T[i-m+1:i+1]$, so reporting $i-m+1$ is sound. Every occurrence reaches state $m$ at its ending position, so reporting is complete.

### Prove preprocessing and search are linear

During prefix construction, the outer index $i$ advances $m-1$ times. A successful extension increases $q$ by one; a fallback strictly decreases $q$. Across the run, $q$ cannot decrease more often in total than it has increased plus its initial value. Failed comparisons at $q=0$ contribute at most one per outer iteration. Thus construction is $O(m)$.

During search, each of the $n$ text symbols is presented once. Successful match transitions increase $q$; failure transitions decrease it without changing the text position. Across the whole scan, decreases are bounded by prior increases, and each text position contributes at most one terminal comparison at $q=0$ or one successful comparison. Hence search is $O(n)$ before output emission and $O(n+z)$ with $z$ reports.

This potential argument can use $q$ as the potential. Text progress pays the constant work, and decreases in $q$ spend potential accumulated by earlier increases. There is no hidden rescan of the text.

### Reproduce prefix construction, overlaps, and streaming

The following dependency-free implementation separates the compiled pattern from mutable stream state. It rejects an empty pattern because a potentially unbounded stream has infinitely many future boundaries; a finite all-boundaries helper could adopt a different explicit policy.

<!-- bijux-verify: {"id":"kmp-compiled-stream","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"prefix=(0, 0, 1, 2, 3, 0, 1)\nresident=(6,)\noverlap=(0, 2)\nstreamed=(6,)\n","stderr":""}} -->
```python
from dataclasses import dataclass


def prefix_function(pattern):
    prefix = [0] * len(pattern)
    for i in range(1, len(pattern)):
        matched = prefix[i - 1]
        while matched > 0 and pattern[matched] != pattern[i]:
            matched = prefix[matched - 1]
        if pattern[matched] == pattern[i]:
            matched += 1
        prefix[i] = matched
    return tuple(prefix)


@dataclass(frozen=True)
class CompiledPattern:
    pattern: tuple
    prefix: tuple

    @classmethod
    def build(cls, pattern):
        immutable = tuple(pattern)
        if not immutable:
            raise ValueError("streaming KMP requires a nonempty pattern")
        return cls(immutable, prefix_function(immutable))


@dataclass
class StreamState:
    compiled: CompiledPattern
    matched: int = 0
    consumed: int = 0

    def feed(self, chunk):
        starts = []
        pattern = self.compiled.pattern
        prefix = self.compiled.prefix
        for symbol in chunk:
            while self.matched > 0 and pattern[self.matched] != symbol:
                self.matched = prefix[self.matched - 1]
            if pattern[self.matched] == symbol:
                self.matched += 1
            self.consumed += 1
            if self.matched == len(pattern):
                starts.append(self.consumed - len(pattern))
                self.matched = prefix[self.matched - 1]
        return tuple(starts)


def search(pattern, text):
    state = StreamState(CompiledPattern.build(pattern))
    return state.feed(text)


print(f"prefix={prefix_function(tuple('ababaca'))}")
print(f"resident={search('ababaca', 'bacbabababacaca')}")
print(f"overlap={search('aba', 'ababa')}")
state = StreamState(CompiledPattern.build('ababaca'))
streamed = sum((state.feed(chunk) for chunk in ('bacba', 'babab', 'acaca')), ())
print(f"streamed={streamed}")
```

The tuple conversion freezes the pattern's symbol sequence for this object. It does not make the elements deeply immutable; production code using mutable records must define stable identity or copy them appropriately. The local run checks concrete behavior, while the invariant and amortized argument carry the general claims.

### Design a compiled-pattern API

Separate immutable preprocessing from per-search mutable state:

- `compile(pattern, equality_policy, semantic_version)` returns an immutable pattern and prefix table;
- `new_state(compiled_pattern, stream_id)` returns $q=0$ and absolute position zero;
- `feed(state, chunk)` returns occurrence coordinates and updated state;
- `finish(state)` resolves decoder or normalization tails and marks the logical text closed;
- `reset(state)` starts a new logical text only when explicitly requested.

One compiled pattern can be shared across threads if its elements and equality behavior are immutable. Each concurrent stream needs its own $q$, decoder state, absolute coordinate, output/backpressure state, and lifecycle. Sharing mutable stream state interleaves unrelated texts and invalidates the suffix invariant.

Version the compiled pattern with the symbol representation, normalization/case policy, equality implementation, and pattern digest. Rebuild it whenever any of those change. Persisted stream checkpoints must identify the exact compiled version and enough decoder state to resume at a symbol boundary.

### Bound operational resources

KMP's algorithmic state is $O(m)$, but a service can still consume unbounded memory through queued chunks or retained results. Apply limits to pattern size, decoded symbol expansion, number of concurrent states, chunk size, output rate, and checkpoint retention. Use pull-based iteration, bounded queues, or callbacks with backpressure rather than accumulating every occurrence.

For a one-symbol pattern in a repeated-symbol stream, $z=n$. KMP is optimally linear but the consumer may still be overwhelmed. A result limit changes the interface: it should return a truncation status or resumable cursor rather than silently omit occurrences.

### Validate the implementation independently

Compare KMP with the naive oracle from ALGE-051 over exhaustive short sequences and randomized larger sequences. Vary alphabet size, pattern length, text length, border depth, match density, and chunk partition. For each finite text, feed every possible split—or random multi-splits—and require identical absolute output.

Validate the prefix table independently: for each $i$, enumerate all $k\le i$ and select the greatest proper prefix equal to the suffix. Check $0\le\pi[i]\le i$, border equality, and failure-chain strict decrease. Mutation tests should alter `q = prefix[q - 1]`, post-match fallback, or absolute-position arithmetic and confirm the suite detects the defect.

Benchmark preprocessing separately from scanning. A compiled pattern amortizes preprocessing across many texts; one-shot search may not. Record equality cost, pattern distribution, match density, chunks, runtime, compiler, hardware, allocations, and output policy. KMP's worst-case guarantee is stable, while observed throughput remains implementation- and workload-specific.

## Definitions and Notation

Let $P\in\Sigma^m$ be a nonempty pattern and $T\in\Sigma^n$ a text under the sequence semantics fixed in ALGE-051.

- $P[a:b]$ and $T[a:b]$ are half-open slices.
- $\pi[i]$ is the length of the longest proper prefix of $P[0:i+1]$ that is also its suffix.
- $q$ is the current matched-prefix length, not a pattern index.
- $i$ is the zero-based absolute index of the current text symbol in resident notation.
- A **failure transition** maps positive $q$ to $\pi[q-1]$ without consuming text.
- An **advance transition** consumes a symbol and maps $q$ to $q+1$ when equality holds.
- A **report transition** at $q=m$ emits $i-m+1$ and maps $q$ to $\pi[m-1]$.
- $z$ is the number of emitted occurrences.
- A **compiled pattern** is the immutable pair $(P,\pi)$ plus equality/representation metadata.
- A **stream state** is $(q,c,d)$, where $c$ is the number of consumed symbols and $d$ is any required decoder or transformation state.
- A **logical text boundary** is a lifecycle event at which matching state may be reset.

The cost model treats symbol equality and prefix-table indexing as $O(1)$. If equality inspects variable-size records, the time bound must multiply or otherwise account for that cost. Input decoding, normalization, and coordinate projection are outside the abstract KMP loop but inside end-to-end service cost.

## Mechanisms, Invariants, or Proof Structure

### Prefix-table invariant

Immediately before constructing entry $i$:

1. $\pi[0:i]$ is exact;
2. `matched` is a border length of $P[0:i]$;
3. every border longer than `matched` has already been ruled out for extension by $P[i]$;
4. following a failure transition strictly decreases `matched`.

On equality, appending $P[i]$ constructs a border one symbol longer. On exhaustion at zero, either the length-one prefix extends or no nonempty border exists. This establishes $\pi[i]$ and the induction.

### Search invariant

Immediately before consuming the next text symbol:

1. $0\le q<m$;
2. $P[0:q]$ equals the suffix of the consumed text of length $q$;
3. no longer proper pattern prefix equals such a suffix;
4. every occurrence wholly contained in consumed text has been reported exactly once;
5. `consumed` is the absolute number of symbols already processed.

Fallback preserves clause 2 because it selects a border of the matched prefix. Its ordering and exact table preserve clause 3 once an extendable candidate is found. A full state $m$ establishes a new occurrence; report fallback restores clauses 1 through 3 while retaining overlaps.

### Prefix-function theorem

**Theorem.** The construction loop computes the exact $\pi[i]$ for every $0\le i<m$.

**Proof.** The base entry is zero because a length-one sequence has no nonempty proper border. For the inductive step, begin with the longest border of $P[0:i]$. If it extends with $P[i]$, it gives the longest border at $i$; a longer one would imply a longer border before extension. If it does not extend, every remaining candidate must be a border of that border, and the exact prior prefix values enumerate these in descending length. The first extendable candidate is maximal; if none exists, only the empty border remains. $\square$

### KMP theorem

**Theorem.** KMP reports exactly every occurrence of nonempty $P$ in $T$, including overlaps, in $O(m+n+z)$ time and $O(m)$ matcher storage excluding outputs.

**Proof.** Prefix construction correctness follows from the preceding theorem and costs $O(m)$ by the matched-length potential. The search invariant proves soundness at each report and completeness at each occurrence ending. Every input symbol is consumed once. Failure transitions strictly lower $q$ and total decreases cannot exceed total prior increases, giving $O(n)$ scan work. Each report costs $O(1)$ plus emission, totaling $O(z)$. The immutable pattern and prefix table use $O(m)$ space, and stream state beyond them is constant-sized. $\square$

### Automaton interpretation

KMP implements a deterministic transition system lazily. State $q$ represents the language of consumed strings whose longest suffix in the set of pattern prefixes has length $q$. A complete DFA could precompute a transition for every $(q,x)\in\{0,\dots,m\}\times\Sigma$, offering one table lookup per symbol but using $O(m|\Sigma|)$ space for a finite alphabet. KMP stores only failure links and resolves a transition by following them, retaining $O(m)$ pattern state and linear aggregate time.

### Evidence boundaries

- Border and search proofs establish abstract exact matching under stable equality.
- Exhaustive and differential checks validate tested implementation states.
- Stream partition tests validate tested lifecycle and coordinate behavior.
- Complexity proofs bound abstract operations, not decoding or remote I/O.
- Benchmarks describe observed throughput, not semantic correctness or universal dominance.
- Product review must still approve text units, transformation, offset projection, and resource policy.

## Alternatives and Trade-Offs

| Design | Preprocessing | Scan | Pattern state | Best fit | Principal trade-off |
|---|---:|---:|---:|---|---|
| Naive | none | worst-case $O(nm)$ | $O(1)$ | oracle, tiny bounded inputs | repeated-prefix comparison blowup |
| Direct Z reduction | $O(n+m)$ combined | included in $O(n+m)$ | $O(n+m)$ direct | batch prefix analysis | text-sized state |
| KMP failure links | $O(m)$ | $O(n+z)$ | $O(m)$ | streaming, reusable pattern | sequential failure dependencies |
| Full pattern DFA | $O(m|\Sigma|)$ typical | $O(n+z)$ | $O(m|\Sigma|)$ | small fixed alphabet, many scans | transition-table size |
| Boyer-Moore family | pattern tables | variant-dependent | pattern-dependent | resident random access | less natural streaming; guarantees vary |
| Built-in search | runtime-specific | runtime-specific | opaque | ordinary application use | semantics and algorithm may vary by version |

KMP is compelling when deterministic worst-case bounds, sequential input, and reusable pattern preprocessing matter. It does not necessarily win small-input latency: setup, interpretation overhead, and optimized native routines can dominate. It is also not a multi-pattern solution; a trie with failure links, developed in multi-pattern string matching, shares prefixes across many patterns.

A complete DFA pays memory to make every transition constant-time in the worst case. KMP pays occasional failure traversals but proves them linear in aggregate. Choosing between them depends on alphabet size, memory hierarchy, pattern reuse, and latency distribution—not asymptotics alone.

For immutable resident strings, Z and KMP both give linear exact search. Z additionally exposes every prefix match in the combined sequence; KMP retains only the current suffix-prefix state and therefore streams naturally. That difference is data ownership, not merely coding style.

## Failure Modes and Misconceptions

1. **“$\pi[i]$ is a position.”** In this chapter it is a length. Treating it as an index shifts every fallback.
2. **“A prefix is always its own border.”** Borders are proper here; otherwise failure may not decrease and the loop may not terminate.
3. **“On mismatch, use $\pi[q]$.”** The matched substring ends at pattern index $q-1$, so its next border is $\pi[q-1]$.
4. **“Fallback consumes the mismatching symbol.”** The same symbol must be retried against each surviving candidate until it matches or state reaches zero.
5. **“KMP backs up a little.”** Only $q$ retreats. The text cursor never does.
6. **“After reporting, reset to zero.”** That loses overlaps whenever the pattern has a nonempty border.
7. **“State can be reset at every chunk.”** A chunk is transport framing, not a logical text boundary.
8. **“The prefix table survives pattern mutation.”** It is derived from exact pattern contents and equality semantics; mutation invalidates it.
9. **“$O(m)$ space includes all results.”** An all-match stream can produce unbounded output; results must be emitted or bounded.
10. **“Linear comparisons guarantee linear wall time.”** Equality, decoding, allocation, output, and backpressure have their own costs.
11. **“KMP makes normalization unnecessary.”** Algorithm speed does not choose text equivalence or coordinate semantics.
12. **“A passed sample proves the fallback table.”** Exhaustive border checks and invariant review are needed in addition to examples.

## Worked Examples

### Example 1

**Situation.** Compute the prefix table for $P=\texttt{ababaca}$.

The first symbol has no proper nonempty border, so $\pi[0]=0$. Prefix `ab` has none, giving 0. Prefix `aba` has border `a`, giving 1. Prefix `abab` has border `ab`, giving 2. Prefix `ababa` has border `aba`, giving 3. For `ababac`, candidate `abab` does not extend because pattern `a` at candidate index 3 differs from `c`; its border `ab` also does not extend, nor does the empty candidate, so the value is 0. Finally, `ababaca` has border `a`, giving 1.

**Conclusion.** $\pi=(0,0,1,2,3,0,1)$; each value is a border length of the prefix ending at that position.

### Example 2

**Situation.** Trace fallback after matching `ababa` from pattern `ababaca` and seeing text symbol `b`.

The current state is $q=5$, where the next expected symbol is $P[5]=\texttt{c}$. It mismatches `b`. Set $q=\pi[4]=3$; the already consumed suffix `aba` equals $P[0:3]$. Now $P[3]=\texttt{b}$ matches the same text symbol, so consume it and set $q=4$.

**Conclusion.** KMP reinterprets the existing suffix and consumes the symbol once; it does not reread the five earlier text symbols.

### Example 3

**Situation.** Report overlaps for $P=\texttt{aaa}$ in $T=\texttt{aaaaa}$.

The prefix table is $(0,1,2)$. Text positions 0, 1, and 2 reach $q=3$, reporting shift 0. Post-match fallback sets $q=\pi[2]=2$. Position 3 immediately restores $q=3$ and reports shift 1; fallback again gives 2. Position 4 reports shift 2.

**Conclusion.** The result is $(0,1,2)$. The post-match border state is exactly what preserves overlapping occurrences.

### Example 4

**Situation.** Explain why fallback candidates are complete, not just plausible.

Assume $q$ symbols have matched and a shorter length $k<q$ could remain valid before testing the mismatching symbol again. Then $P[0:k]$ equals a suffix of the consumed text. That consumed suffix is also a suffix of the matched sequence $P[0:q]$. Hence $P[0:k]$ is a border of $P[0:q]$. The failure chain enumerates the longest border, then the longest border of that border, continuing to zero.

**Conclusion.** No viable candidate lies outside the failure chain; skipping directly among borders is sound and complete.

### Example 5

**Situation.** Diagnose `q = prefix[q]` after a mismatch with $q>0$.

Here $q$ is a length, so the matched pattern substring is $P[0:q]$ and ends at index $q-1$. Its longest border length is stored in $\pi[q-1]$. Entry $\pi[q]$ describes the different, longer prefix ending at index $q$—including a pattern symbol that has not matched. At $q=m$, accessing $\pi[q]$ is also out of range.

**Conclusion.** The only convention-consistent fallback is $q\leftarrow\pi[q-1]$.

### Example 6

**Situation.** Compare direct-DFA memory with KMP for a pattern of length 10,000 over all Unicode scalar values.

A dense table with a transition for every state and scalar value is infeasible: its theoretical cell count is on the order of $10^4\cdot 1.1\times10^6$. Sparse transitions reduce actual storage but require maps and default/failure behavior. KMP stores 10,000 prefix lengths plus the pattern and resolves missing transitions through failure links.

**Conclusion.** Failure links are a compact representation of transition structure; the full DFA trade-off is unattractive for a huge alphabet.

### Example 7

**Situation.** A network pattern begins in chunk `xxab` and ends in chunk `aba`, with $P=\texttt{ababa}$.

After the first chunk, KMP state is $q=2$ because the consumed text ends in `ab`; `consumed=4`. Feeding the next chunk begins from that state. Symbols `a`, `b`, `a` extend to $q=5$, and the match ends after seven total symbols, so its absolute start is $7-5=2$. Resetting at the chunk boundary would miss it.

**Conclusion.** Transport chunking is invisible to the matching invariant when $q$ and absolute position persist.

### Example 8

**Situation.** A compiled matcher stores a mutable list pattern, and another thread changes one element after preprocessing.

The prefix table describes the old list, while equality checks read the new one. Failure links are no longer guaranteed to name borders of the current pattern, so both correctness and time reasoning collapse. Locking only the table does not help; pattern contents and equality policy form one derived immutable unit.

**Conclusion.** Freeze or defensively copy the pattern and version all semantics used to derive the table.

### Example 9

**Situation.** Validate KMP for every short binary input.

Enumerate all binary patterns up to a selected length and all binary texts up to a selected length. Compute expected shifts by direct slice equality and actual shifts by KMP. Independently compute each $\pi[i]$ by testing every proper prefix length. Include empty patterns only under a separately declared finite-input policy, because this chapter's streaming implementation rejects them.

**Conclusion.** Exhaustive finite-domain comparison is strong implementation evidence and targets border-heavy binary cases, while the proof remains necessary to generalize beyond tested lengths.

### Example 10

**Situation.** A log service uses KMP and remains memory-exhaustible on input consisting entirely of the one-symbol pattern.

The matcher performs linear work and reports every position, but the service appends every result to an in-memory list while its consumer is slow. The list grows without bound. Replace retention with a bounded channel and backpressure, or impose a result limit that returns explicit truncation and continuation state.

**Conclusion.** Algorithmic $O(m)$ state excludes outputs and queues; operational bounds must include the entire data path.

## Cross-Program Connections

- **Theory of Computation and Computability:** KMP states are equivalence classes of processed prefixes with respect to future pattern completion; a full pattern automaton makes the transition function explicit.
- **Data Structures Engineering:** immutable arrays, compact integer widths, and cache layout determine prefix-table storage and access cost. See the [Data Structures Engineering roadmap](../../17-data-structures-engineering/ROADMAP.md).
- **Concurrent and Parallel Programming:** immutable compiled patterns can be shared, while each stream's mutable state requires isolation and lifecycle ownership.
- **Operating Systems:** sequential file and socket reads suit no-backtracking search; decoder state and checkpoint recovery must align with I/O boundaries.
- **Security Engineering:** worst-case comparison guarantees reduce one denial-of-service dimension, while pattern size, output rate, decoding, and queues still need caps.
- **API and Service Engineering:** compiled-pattern identity, stream reset, finish, pagination, cancellation, and coordinate units belong in the external contract.
- **Algorithms:** [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md) provides the reference oracle and Z alternative; [ALGE-053](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) changes comparison direction to enable larger skips on resident text.

## References

1. Donald E. Knuth, James H. Morris Jr., and Vaughan R. Pratt, “Fast Pattern Matching in Strings,” *SIAM Journal on Computing* 6(2), June 1977, pp. 323–350. [Primary paper and DOI 10.1137/0206024](https://doi.org/10.1137/0206024). Retrieved 2026-09-05.
2. Dan Gusfield, *Algorithms on Strings, Trees, and Sequences: Computer Science and Computational Biology*, Cambridge University Press, 1997, Part I, “Exact String Matching.” [Publisher record and DOI 10.1017/CBO9780511574931](https://doi.org/10.1017/CBO9780511574931). Retrieved 2026-09-05.
3. Maxime Crochemore, Christophe Hancart, and Thierry Lecroq, *Algorithms on Strings*, Cambridge University Press, 2007, especially Chapters 1–2. [Publisher record and DOI 10.1017/CBO9780511546853](https://doi.org/10.1017/CBO9780511546853). Retrieved 2026-09-05.
4. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 32, “String Matching.” [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/). Retrieved 2026-09-05.
5. Gonzalo Navarro and Mathieu Raffinot, *Flexible Pattern Matching in Strings: Practical On-Line Search Algorithms for Texts and Biological Sequences*, Cambridge University Press, 2002. [Publisher record and DOI 10.1017/CBO9781316135228](https://doi.org/10.1017/CBO9781316135228). Retrieved 2026-09-05.

## Exercises

### Exercise 1

Define $\pi[i]$ precisely under this chapter's convention. Compute the prefix table for $P=\texttt{aabaaab}$ and identify the longest border of the complete pattern.

### Exercise 2

Trace KMP for $P=\texttt{abab}$ over $T=\texttt{ababab}$. Show $q$ after each text symbol, every reported shift, and the post-match fallback that retains overlap.

### Exercise 3

A streaming implementation reports `consumed - m + 1` after incrementing `consumed` as a count of processed symbols. Diagnose the coordinate error, give a minimal failing example, and correct the formula.

### Exercise 4

Compare KMP failure links with a complete DFA transition table for a byte alphabet and a pattern used to scan ten million short messages. State what measurements and constraints would determine the design.

### Exercise 5

Design checkpoint and recovery for KMP over a normalized event stream. The service may restart between arbitrary input chunks, patterns are versioned, and duplicate reports are forbidden. Specify persisted state, invariants, failure handling, and validation evidence.

## Answers to the Exercises

### Answer 1

$\pi[i]$ is the maximum $k$ with $0\le k\le i$ such that the length-$k$ prefix $P[0:k]$ equals the length-$k$ suffix of $P[0:i+1]$; the complete prefix is excluded. For `aabaaab`, the values are $(0,1,0,1,2,2,3)$. In detail, prefixes ending at positions 0 through 4 have longest borders of lengths 0, 1, 0, 1, and 2. Prefix `aabaaa` has longest border `aa`, length 2, and the full pattern `aabaaab` has border `aab`, length 3. Therefore the complete pattern's longest border is `aab`.

### Answer 2

The prefix table for `abab` is $(0,0,1,2)$. Reading text positions 0 through 3 produces $q=1,2,3,4$ and reports shift $3-4+1=0$. The post-match fallback is $q=\pi[3]=2$, preserving suffix `ab`. Text position 4 contains `a`, extending $q$ to 3; position 5 contains `b`, extending to 4 and reporting shift $5-4+1=2$. Fallback again yields 2. The output is $(0,2)$. A trace that resets to zero after the first report is incorrect because it loses the overlap.

### Answer 3

After increment, `consumed` is a count, so the current zero-based index is `consumed - 1`. A match of length $m$ begins at `(consumed - 1) - m + 1 = consumed - m`. The faulty `consumed - m + 1` is one too large. For pattern `a` and text `a`, after processing the symbol `consumed=1`; the faulty expression reports 1 although the only valid start is 0. Use `consumed - m`, as in the executable implementation, and test matches at absolute start zero and across chunk boundaries.

### Answer 4

Both designs can scan each message in linear time. KMP stores $O(m)$ prefix lengths and may traverse multiple failure links on an individual byte while remaining linear in aggregate. A dense byte DFA stores roughly $(m+1)\times256$ transitions and performs one predictable lookup per byte. For a pattern reused across ten million messages, preprocessing is heavily amortized, so the decision turns on memory footprint, cache residency, branch behavior, message lengths, concurrency, and throughput/latency distribution.

Benchmark compiled implementations on production hardware with the real pattern-length and byte distributions, adversarial repeated prefixes, match-heavy inputs, and identical output handling. Measure preprocessing separately, resident memory per shared compiled pattern, per-stream state, cache misses, tail latency, and update cost. Confirm the memory limit and whether patterns are shared across workers. Choose the DFA only if its larger table fits the memory/cache budget and measured transition advantage matters; choose KMP when compactness, large or variable alphabets, or simpler preprocessing dominates. Either answer is acceptable with explicit constraints and reproducible evidence.

### Answer 5

Persist an atomic checkpoint containing stream identity, source offset at a confirmed event boundary, count of normalized symbols consumed, current $q$, compiled-pattern digest and semantic version, normalization/decoder version and residual state, last durably acknowledged match coordinate, and checkpoint checksum. The invariant is that $P[0:q]$ equals the suffix of the normalized event sequence through the checkpoint, every earlier match has been durably emitted exactly once, and source/normalized coordinates share one transformation version.

On recovery, load the exact compiled pattern and semantic policy, verify the checksum and source generation, restore transformation state, $q$, and coordinates, then resume after the checkpointed source boundary. If the pattern version is unavailable or source data changed, reject recovery rather than combining incompatible state. Use an idempotency key such as `(stream_id, pattern_digest, match_start)` at the output boundary, or atomically checkpoint the last acknowledgement with source progress, to suppress replay duplicates.

Validate by comparing uninterrupted output with recovery after every possible boundary on finite fixtures, including a match spanning the restart. Inject crashes before and after output acknowledgement and checkpoint persistence. Add normalization expansion, partial encoded input, deep failure chains, overlapping matches, pattern upgrades, corrupted checkpoints, backpressure, and result floods. A complete answer must connect persisted fields to the suffix invariant and exactly-once report protocol; storing only $q$ is insufficient.
