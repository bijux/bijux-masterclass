---
module_id: ALGE-056
program: Algorithm Engineering
level: 2
module_number: 56
title: Suffix Trees and Automata
status: complete
last_verified: 2026-09-05
---

# Suffix Trees and Automata

## One-Page Review

### Governing question

How do suffix trees and suffix automata encode every substring of one text in linear-size topology, and which invariants, construction assumptions, and representation choices make their strong query guarantees honest in production?

### Essential definitions

- A **suffix tree** is the path-compressed trie of all suffixes of $T\cdot\bot$, where $\bot$ is a unique terminator under the chosen convention.
- An **explicit node** is a stored branching point or leaf; an **implicit locus** lies inside a compressed edge.
- An edge label is represented by an interval into the immutable text rather than a copied string.
- A **suffix link** maps a node for $c\alpha$ to a node for $\alpha$ when that explicit locus exists.
- A **suffix automaton** (SAM) is the minimal partial deterministic automaton recognizing all substrings of one text.
- Two substrings are **end-position equivalent** when they end at the same set of text positions; one SAM state represents one such class.
- `len[v]` is the greatest length represented by state $v$; `link[v]` leads to the class of its longest proper suffix outside the class.
- A **clone** splits an automaton state when one transition target must represent two different length contexts.

### Central model, mechanism, or theorem

A suffix-tree path spells a substring, possibly ending inside an edge. Following $m$ pattern symbols reaches its locus in $O(m)$ navigation under a constant-time transition model; descendant leaves identify occurrences. In a SAM, following $m$ transitions decides substring membership. For every noninitial SAM state $v$, it represents exactly the length interval

$$
len[link[v]]+1,\ldots,len[v].
$$

Therefore the number of distinct nonempty substrings is $\sum_{v\ne root}(len[v]-len[link[v]])$. Both structures have $O(n)$ states or nodes, but constants, construction algorithms, alphabets, occurrence metadata, and query capabilities differ.

### Critical invariants

- Edge labels and positions refer to one immutable encoded text generation.
- Outgoing tree edges begin with distinct symbols; paths are compared against interval labels exactly.
- Every terminated suffix ends at one tree leaf under the explicit-sentinel convention.
- SAM transitions are deterministic and increase `len`.
- For every nonroot SAM state, $0\le len[link[v]]<len[v]$.
- A nonclone extension state initially contributes one terminal position; clones initially contribute none.
- Occurrence counts propagate along suffix links in descending `len` order.
- Alphabet maps, terminators, document boundaries, offsets, and output ordering are part of the contract.

### Common failures

Common failures include materializing edge strings; calling a suffix trie a suffix tree; assuming pointer-heavy nodes are compact; forgetting implicit loci; inserting a terminator already present in input; mixing inclusive and exclusive edge endpoints; applying a linear-time theorem without its alphabet model; corrupting open leaf endpoints during online construction; omitting SAM clones; initializing clones as new occurrences; propagating counts in arbitrary order; treating a SAM state as one substring; and assuming membership navigation alone returns positions.

### Compact example

For `banana`, a suffix tree has a path spelling `ana`; leaves below its locus correspond to starts 1 and 3. A SAM follows transitions `a`, `n`, `a` and reaches a state whose propagated end-position count is 2. The tree retains hierarchical occurrence locations naturally; the minimal automaton merges substrings with the same future behavior and end-position class. Both answer membership in pattern length, but their metadata and traversal tasks are not interchangeable.

### Connections

[ALGE-055](./055-suffix-arrays-and-lcp.md) represents suffix order and adjacent common prefixes with arrays. [ALGE-057](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) moves from exact indexing to edit distance. Automata theory supplies minimization and language semantics; Systems Engineering governs memory layout, persistence, and bounded traversal.

## Governing Question

Given one stable sequence, how can we represent all of its substrings without quadratic copied text, build the representation under stated alphabet and machine assumptions, and choose between suffix-tree topology and suffix-automaton equivalence classes for exact queries, occurrence analysis, and production constraints?

The phrase “linear-size full-text index” hides important choices. Suffix trees compress common path segments; suffix automata quotient substrings by indistinguishable continuation behavior. Their linear bounds describe abstract topology, not automatically the byte footprint of maps, objects, allocators, labels, document metadata, and construction temporaries.

## Why This Matters

Suffix structures support repeated exact queries, longest repeated and common substring problems, repeat statistics, document analysis, and components of compression and biosequence tooling. They expose relationships that repeated window scans do not reuse.

They are also unusually easy to implement almost correctly. A wrong edge endpoint can pass many queries. A missing clone can preserve membership for early prefixes while breaking minimality and occurrence counts. An unrestricted hash map per state can dominate text storage. A cross-document path can manufacture a substring that never occurred in one document.

Studying both structures makes representation choice concrete: equivalent asymptotic size does not imply equivalent operations, locality, construction complexity, or failure surface.

## Prerequisites and Retrieval

Retrieve tries, path compression, deterministic finite automata, language recognition, equivalence relations, trees, amortized analysis, immutable text snapshots, and stable alphabet encodings. Complete [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md) through [ALGE-055](./055-suffix-arrays-and-lcp.md).

This chapter uses **substring** and **factor** synonymously for a contiguous slice. A suffix-tree discussion assumes a unique sentinel unless it explicitly describes an implicit tree. The executable automaton rejects an empty query as an API policy even though formal factor languages normally include the empty word.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish suffix tries, suffix trees, implicit loci, and suffix automata;
2. state the text, alphabet, sentinel, and machine assumptions behind size and time bounds;
3. trace compressed-edge pattern navigation and occurrence enumeration;
4. explain suffix links in trees and automata without conflating their state semantics;
5. derive SAM length intervals from end-position equivalence;
6. trace online SAM extension, redirect transitions, and justify cloning;
7. compute membership, occurrence counts, and distinct-substring counts;
8. compare suffix trees, suffix automata, suffix arrays, and compressed indexes by workload;
9. design collection boundaries, persistence, resource limits, and validation; and
10. separate mathematical invariants, local execution, exhaustive tests, and performance evidence.

## Core Exposition

### Begin with the suffix trie, then compress paths

Insert every suffix of $T\cdot\bot$ into a trie. Each root-to-leaf path spells one terminated suffix; every substring of $T$ is a prefix of some suffix and therefore labels a path from the root. The uncompressed trie can contain $\Theta(n^2)$ nodes.

A suffix tree compresses every maximal nonbranching path into one edge. Store an edge label as a half-open interval $[l,r)$ into the immutable text, not as copied symbols. Each internal nonroot node then branches, so the explicit topology is $O(n)$. The original text still owns label bytes, and a query may stop at an implicit locus inside an edge.

For a pattern $P$, choose the outgoing edge whose first symbol matches the next pattern symbol, compare along its label, and continue at the next explicit node. A mismatch proves absence. Consuming all $m$ symbols proves membership even if the locus is implicit. Under constant-time outgoing-edge lookup, navigation costs $O(m)$ symbol inspections. Enumerating descendant leaves adds $O(z)$ for $z$ reported occurrences.

### Treat the terminator as a proof device and format rule

Appending a unique terminator smaller than or merely distinct from every input symbol ensures no suffix is a prefix of another and gives every suffix its own leaf. If the empty suffix is included, $T\cdot\bot$ has $n+1$ suffix starts; conventions vary on whether the exported tree exposes the terminator-only suffix.

The terminator must be an out-of-band alphabet value, not a character guessed to be absent. Byte alphabets already occupy 256 values, so an implementation can widen symbols to integers and reserve 256. Persist the transformation. Query input normally excludes the terminator.

For collections, distinct terminators simplify generalized-tree proofs but can enlarge the alphabet. Boundary-aware comparison with document metadata is another design. In either case, paths must not treat a document suffix plus the next document prefix as one valid factor.

### Understand tree suffix links

If an internal node's path label is $c\alpha$, its suffix link points to the explicit node labeled $\alpha$. Suffix links reuse work between related suffixes during construction and later traversals. They are auxiliary edges, not child edges and not occurrence links.

Weiner, McCreight, and Ukkonen constructions achieve linear time under their respective assumptions and strategies. Ukkonen processes prefixes online, maintains an active point and remaining extensions, shares an open end among leaves, and uses suffix links to avoid restarting from the root. Its proof relies on compressed implicit states and amortization. A naive “insert each suffix into a compressed trie” implementation does not inherit Ukkonen's bound.

Alphabet transition representation matters. Fixed arrays can give constant lookup but cost $\Theta(|\Sigma|)$ per node. Balanced maps give logarithmic lookup. Hash tables give expected lookup under a threat model. Small sorted vectors can improve locality. Include these costs when stating $O(m)$ navigation.

### Define the suffix automaton language

A suffix automaton is the minimal partial DFA whose accepted paths from the initial state spell exactly the substrings of $T$. In common implementations every reached state is accepting for membership; terminal-state markings have a separate role when recognizing suffixes or propagating properties.

For a substring $x$, let $endpos(x)$ be the set of positions where an occurrence of $x$ ends. Substrings with the same end-position set form one equivalence class and one SAM state. This explains why a state is not one substring: state $v$ represents all suffixes of one longest representative having lengths

$$
len[link[v]]+1\le |x|\le len[v].
$$

The suffix link goes from a class to the class containing its longest proper suffix with a different end-position set. Transition edges add one symbol to represented paths; suffix links remove leading context semantically. These are different relations.

### Extend a suffix automaton online

Maintain `last`, the state representing the entire processed prefix. Appending symbol $c$ creates state `cur` with `len[cur]=len[last]+1` and one new terminal-position contribution. Walk suffix links from `last`, adding missing $c$ transitions to `cur`.

If the walk reaches the imaginary state before the root, link `cur` to the root. Otherwise an existing transition $p\xrightarrow{c}q$ is found:

- if $len[p]+1=len[q]$, link `cur` directly to $q$;
- otherwise clone $q$ with copied transitions and suffix link, set $len[clone]=len[p]+1$, redirect every suffix-chain $c$ transition that formerly reached $q$, and link both $q$ and `cur` to the clone.

The clone separates contexts while preserving the recognized language. It is not a newly observed ending, so its initial occurrence contribution is zero. A linear bound follows from the limited number of states, transitions, and suffix-link redirections under the standard construction; a language runtime's map operations add their own cost model.

### Reproduce automaton membership and counts

The following dependency-free implementation builds the SAM for one Python string. It propagates occurrence contributions in descending `len` order so every state's end-position count flows to its suffix-link ancestor.

<!-- bijux-verify: {"id":"suffix-automaton-membership-counts","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"states=10 transitions=11\nana=True count=2\nnana=True count=1\napple=False count=0\ndistinct=15\n","stderr":""}} -->
```python
class State:
    def __init__(self):
        self.next = {}
        self.link = -1
        self.length = 0
        self.occurrences = 0


class SuffixAutomaton:
    def __init__(self):
        self.states = [State()]
        self.last = 0

    def extend(self, symbol):
        cur = len(self.states)
        self.states.append(State())
        self.states[cur].length = self.states[self.last].length + 1
        self.states[cur].occurrences = 1
        p = self.last
        while p >= 0 and symbol not in self.states[p].next:
            self.states[p].next[symbol] = cur
            p = self.states[p].link
        if p < 0:
            self.states[cur].link = 0
        else:
            q = self.states[p].next[symbol]
            if self.states[p].length + 1 == self.states[q].length:
                self.states[cur].link = q
            else:
                clone = len(self.states)
                self.states.append(State())
                self.states[clone].length = self.states[p].length + 1
                self.states[clone].next = self.states[q].next.copy()
                self.states[clone].link = self.states[q].link
                while p >= 0 and self.states[p].next.get(symbol) == q:
                    self.states[p].next[symbol] = clone
                    p = self.states[p].link
                self.states[q].link = clone
                self.states[cur].link = clone
        self.last = cur

    def finish_occurrences(self):
        order = sorted(
            range(1, len(self.states)),
            key=lambda v: self.states[v].length,
            reverse=True,
        )
        for v in order:
            parent = self.states[v].link
            self.states[parent].occurrences += self.states[v].occurrences

    def state_for(self, pattern):
        if not pattern:
            raise ValueError("empty-pattern policy is external")
        state = 0
        for symbol in pattern:
            target = self.states[state].next.get(symbol)
            if target is None:
                return None
            state = target
        return state

    def count(self, pattern):
        state = self.state_for(pattern)
        return 0 if state is None else self.states[state].occurrences

    def distinct_substrings(self):
        return sum(
            state.length - self.states[state.link].length
            for state in self.states[1:]
        )


sam = SuffixAutomaton()
for character in "banana":
    sam.extend(character)
sam.finish_occurrences()
transitions = sum(len(state.next) for state in sam.states)
print(f"states={len(sam.states)} transitions={transitions}")
for pattern in ("ana", "nana", "apple"):
    state = sam.state_for(pattern)
    print(f"{pattern}={state is not None} count={sam.count(pattern)}")
print(f"distinct={sam.distinct_substrings()}")
```

`finish_occurrences` is a one-way finalization for this simple implementation. Extending afterward and propagating again would double-count prior contributions. A mutable service needs a different lifecycle or a rebuilt snapshot.

### Derive occurrence and distinct-substring metadata

Each ordinary extension state initially represents one new prefix endpoint. Clones represent reorganized equivalence classes and start at zero. Processing states from greatest to least `len` adds each state's count to its suffix-link parent; this unions endpoint contributions along suffix relationships. After propagation, a state's count is the size of its end-position class, hence the occurrence count of every substring represented by that state.

State $v$ represents one substring for every length in $(len[link[v]],len[v]]$. Those intervals partition the distinct nonempty substrings by end-position class, so

$$
\#distinct(T)=\sum_{v\ne root}(len[v]-len[link[v]]).
$$

Membership needs transitions only. Counting needs correctly finalized endpoint metadata. Reporting positions needs endpoint sets, sorted occurrence lists, a suffix-link tree with offline aggregation, or verification against another index; storing every set eagerly can become quadratic.

### Find a longest common substring with a SAM

Build a SAM for $T$ and scan another sequence $U$. Track the current state and matched length $h$. On a missing transition, follow suffix links until a transition exists or the root is reached, reducing $h$ to the surviving state's `len`. Advance on the next transition and update the best $h$ and endpoint.

The invariant is that the tracked state and $h$ represent the longest suffix of the scanned prefix of $U$ that occurs in $T$. This yields linear navigation under the same transition-cost assumptions. Recovering all ties, document identities, or bounded-memory streams adds policy and metadata.

### Relate tree, automaton, and array information

A suffix tree distinguishes prefixes by branching paths and exposes occurrence leaves. A SAM merges substrings with identical end-position behavior and exposes transitions in the factor language. A suffix array orders complete suffixes and stores no explicit branching topology. LCP intervals can reconstruct much suffix-tree hierarchy; a suffix-link tree organizes SAM states by proper-suffix classes.

These structures answer overlapping questions but are not drop-in encodings of identical nodes. Converting or comparing them requires a stated sentinel convention, substring coordinates, and metadata mapping.

### Engineer storage and validation

Object-per-node designs can spend far more than the $O(n)$ topology suggests. Consider structure-of-arrays layouts, packed edge endpoints, compact transition tables, pooled maps, and breadth- or depth-aware ordering. Measure bytes per input symbol, peak construction memory, cache misses, and serialization time—not node count alone.

Persist text generation/digest, encoding and normalization, sentinel and document policy, offset/state widths, root and invalid-link conventions, construction version, array/map lengths, and checksums. Validate bounds before dereferencing. Cap query length, traversal steps, occurrence output, recursion depth, memory mapping, and concurrent readers.

Differentially compare membership with direct search over exhaustive short strings. For trees, validate every leaf suffix, outgoing first-symbol uniqueness, interval bounds, parent depth, and suffix links. For SAMs, validate deterministic transitions, increasing transition lengths, decreasing suffix links, clone contribution rules, finite-language membership, occurrence counts, and the distinct-substring identity.

## Definitions and Notation

Let $T\in\Sigma^n$ under a stable finite-symbol representation.

- $T\cdot\bot$ is a terminated text with $\bot\notin\Sigma$ under the tree convention.
- A tree edge interval $[l,r)$ denotes symbols $l$ through $r-1$ of $T\cdot\bot$.
- The **string depth** of a tree locus is the number of symbols from the root to it.
- A **leaf label** is the start offset of its represented terminated suffix.
- $endpos(x)=\{j:T[j-|x|+1:j+1]=x\}$.
- $len[v]$ is the maximum substring length in SAM state $v$.
- $link[v]$ is the suffix link of $v$; the root uses a declared invalid link.
- $next[v,c]$ is the deterministic transition from state $v$ on symbol $c$ when defined.
- A **clone** copies transitions and a suffix link while receiving a shortened maximum length and zero initial endpoint contribution.
- $z$ is the number of occurrences emitted, not merely counted.

Claims of constant-time transitions assume an appropriate alphabet mapping or expected-time hash lookup. Claims of linear construction assume the named algorithm, representation, and computation model.

## Mechanisms, Invariants, or Proof Structure

### Tree path-compaction theorem

**Theorem.** The compacted trie of $N$ terminated suffixes has $O(N)$ explicit nodes.

**Proof.** It has $N$ leaves. Every internal nonroot node has at least two children after maximal nonbranching paths are compressed. In any rooted tree with that property, internal nodes are fewer than leaves, apart from the root convention. Thus explicit nodes and edges are linear in $N$. Edge-label lengths do not count as stored nodes because labels are text intervals. $\square$

### Tree query theorem

**Theorem.** Exact navigation for a length-$m$ pattern examines at most $m$ matched pattern symbols before reaching its locus or finding a mismatch.

**Proof.** Every successful edge-label comparison consumes new pattern symbols, and compressed edges on one root path do not overlap in pattern coordinates. A mismatch stops immediately. Transition lookup and result enumeration are separate costs. $\square$

### SAM length-interval invariant

For every nonroot state $v$,

$$
0\le len[link[v]]<len[v].
$$

All lengths greater than $len[link[v]]$ through $len[v]$ share $v$'s end-position set. The next shorter suffix belongs to the suffix-link state. These disjoint state intervals establish the distinct-substring sum.

### Clone correctness obligation

When $p\xrightarrow{c}q$ exists but $len[p]+1<len[q]$, linking `cur` directly to $q$ would place a shorter context into a state whose interval boundary is too large. Clone $q$ at maximum length $len[p]+1$, preserve its future transitions and prior suffix link, redirect precisely the affected $c$ transitions, and make $q$ and `cur` suffix-link children of the clone. The language is preserved while end-position classes regain valid length intervals.

### Occurrence propagation invariant

Before processing a state $v$ in descending `len`, its count contains all ordinary extension endpoints from its suffix-link descendants already processed. Adding it once to $link[v]$ transfers exactly those endpoints to the proper-suffix class. Descending order is essential because suffix links strictly decrease `len`.

### Evidence boundaries

- Automata theory and combinatorial arguments prove topology and language properties under the model.
- Execution checks one implementation and runtime.
- Exhaustive tests prove agreement only over their finite domain.
- Serialization and corruption tests establish behavior for named formats and faults.
- Benchmarks describe workloads and hardware, not universal superiority.
- Neither structure alone authenticates the indexed text or makes mutable offsets stable.

## Alternatives and Trade-Offs

| Structure | Membership navigation | Occurrences | Typical representation | Strength | Main cost |
|---|---:|---:|---|---|---|
| Suffix tree | $O(m)$ plus transition cost | descendant leaves, $O(z)$ | nodes plus text intervals | rich locus hierarchy | complex, pointer-heavy construction |
| Suffix automaton | $O(m)$ plus transition cost | counts easy; positions need metadata | states, links, transitions | minimal factor-language DFA | states merge many substrings |
| Suffix array + LCP | baseline binary search; enhanced variants improve comparisons | contiguous suffix ranks | integer arrays | locality and persistence | less direct navigation |
| FM/compressed index | implementation-specific near-pattern time | locate samples/additional work | compressed transform/rank data | reduced space, self-indexing options | construction and locate complexity |
| Direct scan | $O(n+m)$ per pattern | direct positions | text only | simple and mutable | no reusable index |

Choose by operations, update lifecycle, and memory hierarchy. A tree is natural for explicit path topology and occurrence subtrees. A SAM is elegant for factor membership, distinct counts, and longest-common-substring scans. Arrays often win for compact immutable deployment. Compressed indexes address scale when raw topology or arrays are too large.

## Failure Modes and Misconceptions

1. **“A suffix trie is already linear.”** Without path compression it can contain quadratic nodes.
2. **“An edge stores its label string.”** Copying labels can destroy the linear-space representation.
3. **“Every match ends at an explicit tree node.”** A pattern can end inside a compressed edge.
4. **“A sentinel is just `$`.”** It must be a reserved symbol outside the admitted input alphabet.
5. **“Ukkonen makes any suffix-tree code linear.”** The bound belongs to its active-point, suffix-link, endpoint, and transition invariants.
6. **“A SAM state is a substring.”** It represents an end-position equivalence class and a range of lengths.
7. **“Suffix links are transitions.”** They express proper-suffix structure and consume no query symbol.
8. **“Clones are optional optimization.”** They are required to preserve state-class and length invariants.
9. **“A clone adds one occurrence.”** It copies structure but initially represents no new text endpoint.
10. **“Membership gives positions.”** It proves existence; reporting requires additional occurrence metadata.
11. **“Linear nodes means low memory.”** maps, objects, pointers, allocators, and temporaries can dominate.
12. **“Appending documents preserves semantics.”** Uncontrolled boundaries create false cross-document factors.

## Worked Examples

### Example 1

**Situation.** Contrast a suffix trie and suffix tree for `aaaa$`.

The suffixes share long runs of `a`. A trie stores one node per prefix occurrence along many suffix paths. Path compression replaces each maximal nonbranching run with one interval-labeled edge while retaining branch points where a suffix reaches `$`.

**Conclusion.** Compression changes representation size, not the set of root-path strings.

### Example 2

**Situation.** Search `ana` in a suffix tree for `banana$`.

Follow the root edge beginning with `a`, compare its interval symbols, then follow the `n` continuation and consume the final `a`. The locus may be explicit or internal to an edge. Leaves below it carry starts 1 and 3.

**Conclusion.** Membership costs the three consumed symbols under constant transition lookup; reporting adds two leaves.

### Example 3

**Situation.** Explain why a text edge interval becomes invalid after mutation.

Suppose an edge stores $[2,6)$ into generation G. Inserting one symbol before position 2 in place shifts its content and every later offset. The old topology can now spell different labels even if pointers remain valid.

**Conclusion.** Indexed text must be immutable, or every topology and coordinate must be rebuilt under a new generation.

### Example 4

**Situation.** A SAM state has `len=7` and its suffix-link parent has `len=3`.

The state represents one substring for each length 4, 5, 6, and 7: four distinct substrings sharing one end-position class. Its contribution to the distinct-substring sum is $7-3=4$.

**Conclusion.** State count and distinct-substring count are different quantities.

### Example 5

**Situation.** Trace why a clone starts with zero occurrences.

Appending one symbol creates one new prefix endpoint, assigned to `cur`. A clone only splits the prior state $q$ so shorter contexts have the correct maximum length; no new text position was appended for the clone itself. Later descending suffix-link propagation transfers actual endpoint contributions into it.

**Conclusion.** Setting a clone's initial count to one overcounts occurrences.

### Example 6

**Situation.** Count occurrences of `ana` in the `banana` SAM.

Following `a`, `n`, `a` reaches one state. Ordinary extension endpoints were initialized once, then propagated from longer states to suffix-link ancestors in descending length. The reached end-position class contains endpoints 3 and 5, so its count is 2.

**Conclusion.** One reached state answers the count only after correct offline propagation.

### Example 7

**Situation.** Count distinct substrings of `banana` from SAM states.

Summing $len[v]-len[link[v]]$ over the nine nonroot states produced by the executable implementation gives 15. ALGE-055 independently obtained $6\cdot7/2-\sum LCP=15$.

**Conclusion.** Agreement of two representations is valuable differential evidence, though both still rely on the same sequence semantics.

### Example 8

**Situation.** Index byte documents when every byte value may occur.

Choosing byte `0x00` as a separator is unsafe. Widen input bytes to integers 0 through 255 and reserve out-of-band integer 256, or use boundary metadata that terminates comparisons. Reject query symbols outside the declared input alphabet.

**Conclusion.** Sentinel uniqueness is an encoding invariant, not a corpus sample assumption.

### Example 9

**Situation.** Compare memory layouts for one million SAM states.

An object with a hash map, allocator header, pointers, and boxed integers can occupy dozens or hundreds of bytes even when it has one transition. Packed `len`, `link`, transition-offset, and degree arrays plus pooled symbol/target pairs avoid much per-object overhead.

**Conclusion.** Report measured bytes per state and input symbol alongside linear asymptotics.

### Example 10

**Situation.** A service exposes unbounded occurrence positions for pattern `a` in a billion-symbol all-`a` text.

Navigation is constant in pattern length, but output contains one billion positions. The service needs a count-only mode, stable pagination tied to the index generation, result caps, cancellation, and explicit truncation status.

**Conclusion.** $O(m+z)$ is operationally dominated by $z$ when matches are dense.

## Cross-Program Connections

- **Theory of Computation:** minimal DFA semantics, right congruences, deterministic transitions, and accepted factor languages explain SAM state merging.
- **Data Structures Engineering:** compressed tries, pooled adjacency, maps, trees, and array layouts determine real memory and transition costs. See the [Data Structures Engineering roadmap](../../17-data-structures-engineering/ROADMAP.md).
- **Operating Systems:** virtual memory, memory mapping, page locality, offset width, and crash-safe publication shape large immutable indexes.
- **Data Engineering:** canonical encoding, document boundaries, snapshot lineage, rebuilds, and verification keep positions meaningful.
- **Security Engineering:** malformed serialized topology, offset overflow, hash-map attacks, traversal exhaustion, and output amplification require validation and quotas.
- **API and Service Engineering:** membership, count, locate, result order, pagination, empty-pattern behavior, and generation identity are separate endpoints or contracts.
- **Algorithms:** [ALGE-055](./055-suffix-arrays-and-lcp.md) offers array-oriented suffix structure; [ALGE-057](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) introduces inexact matching costs.

## References

1. Edward M. McCreight, “A Space-Economical Suffix Tree Construction Algorithm,” *Journal of the ACM* 23(2), April 1976, pp. 262–272. [Official ACM DOI 10.1145/321941.321946](https://doi.org/10.1145/321941.321946). Retrieved 2026-09-05.
2. Esko Ukkonen, “On-Line Construction of Suffix Trees,” *Algorithmica* 14(3), September 1995, pp. 249–260. [Official publisher DOI 10.1007/BF01206331](https://doi.org/10.1007/BF01206331). Retrieved 2026-09-05.
3. A. Blumer, J. Blumer, David Haussler, Andrzej Ehrenfeucht, M. T. Chen, and Joel I. Seiferas, “The Smallest Automaton Recognizing the Subwords of a Text,” *Theoretical Computer Science* 40, 1985, pp. 31–55. [Official publisher DOI 10.1016/0304-3975(85)90157-4](https://doi.org/10.1016/0304-3975(85)90157-4). Retrieved 2026-09-05.
4. Peter Weiner, “Linear Pattern Matching Algorithms,” *14th Annual Symposium on Switching and Automata Theory*, 1973, pp. 1–11. [Official IEEE DOI 10.1109/SWAT.1973.13](https://doi.org/10.1109/SWAT.1973.13). Retrieved 2026-09-05.
5. Maxime Crochemore, Christophe Hancart, and Thierry Lecroq, *Algorithms on Strings*, Cambridge University Press, 2007. [Official publisher record and DOI 10.1017/CBO9780511546853](https://doi.org/10.1017/CBO9780511546853). Retrieved 2026-09-05.
6. Dan Gusfield, *Algorithms on Strings, Trees, and Sequences*, Cambridge University Press, 1997, Part II. [Official publisher record and DOI 10.1017/CBO9780511574931](https://doi.org/10.1017/CBO9780511574931). Retrieved 2026-09-05.

## Exercises

### Exercise 1

For a SAM state with `len=11` and suffix-link parent `len=6`, state exactly which substring lengths it represents and its contribution to the distinct-substring count.

### Exercise 2

Trace the occurrence-contribution lifecycle for three ordinary extension states and one clone. Explain why descending `len` order is necessary.

### Exercise 3

A suffix-tree implementation stores copied edge strings, uses dictionary transitions, and advertises $O(n)$ bytes and deterministic $O(m)$ query time. Diagnose both claims and give the metadata needed to measure them honestly.

### Exercise 4

Design an immutable exact-substring service that may use a suffix tree, SAM, or suffix array. Compare membership, count, locate, memory, construction, persistence, and adversarial behavior, then select one design for a read-heavy byte corpus.

### Exercise 5

Design a generalized index that finds a longest substring shared by at least two of many documents. Prevent cross-boundary matches, define document identity and ties, and specify differential and corruption evidence.

## Answers to the Exercises

### Answer 1

The represented lengths are the integers strictly greater than the parent's maximum and no greater than the state's maximum: 7, 8, 9, 10, and 11. The state contributes $11-6=5$ distinct substrings. A complete answer must say that these are suffixes of a longest representative sharing one end-position class, not five arbitrary strings.

### Answer 2

Each of the three ordinary extension states receives initial contribution one because each appended prefix creates one new endpoint. The clone receives zero because splitting an existing equivalence class appends no text. Every state's endpoint set is contained in its suffix-link parent's endpoint set, so propagation adds child counts to parents.

Process greater `len` first. If a parent were processed before a longer child, the parent's current count would flow upward and the later child contribution would never reach higher ancestors unless the parent were processed twice. Strictly decreasing suffix links make descending length a topological order. Tests should compare every nonempty substring count with direct enumeration and specifically include strings that create clones, such as repeated and branching contexts.

### Answer 3

The abstract tree has $O(n)$ nodes and total interval labels, but copied edge strings can store $\Theta(n^2)$ symbols across long labels. Replace copies with validated $[l,r)$ intervals into an immutable text generation. Even then, object headers, maps, pointers, allocators, construction temporaries, and the text itself determine bytes.

Dictionary transitions give expected lookup only under the runtime's hashing and adversary model; deterministic $O(m)$ does not follow automatically. Fixed alphabet arrays offer deterministic constant lookup at high per-node space; balanced maps offer deterministic logarithmic lookup; sorted small vectors trade comparison work for locality.

Record input bytes/symbols, nodes, edges, interval width, transition representation and load, object/pool bytes, allocator overhead, text bytes, temporary peak, alphabet size/distribution, hash policy, query symbol inspections, transition probes, cache misses, hardware, runtime, and adversarial fixtures. State complexity in symbol comparisons and map operations separately.

### Answer 4

All three structures support exact membership for immutable text. A suffix tree naturally enumerates descendant leaves and exposes loci but has complex construction and topology. A SAM gives compact language membership and counts after propagation, but positions require extra endpoint metadata. A suffix array uses compact sortable integer arrays, returns occurrences as a rank interval, and has strong locality; baseline search may cost $O(m\log n)$ symbol comparisons unless LCP-aware search is implemented.

For a read-heavy byte corpus requiring membership and paginated locations, choose suffix array plus LCP and optional RMQ: stable byte order, packed 64-bit offsets, immutable text mapping, and simple generation files make validation and deployment tractable. Build offline with a named scalable constructor, persist checksums and encoding/width metadata, validate permutation/order and direct query samples, then atomically publish the generation.

Cap pattern size, comparisons, locate results, mapped bytes, and concurrency. Return generation ID, result order, cursor, truncation, and count semantics. A SAM is a valid alternative for dominant membership/count workloads if endpoint metadata and finalization lifecycle are specified; a tree is valid when topology operations justify its memory and implementation risk.

### Answer 5

Encode each immutable document with an ID and local offsets. For a generalized suffix tree, use excluded distinct terminators or boundary-aware edge comparisons; annotate each subtree with the set or count of distinct document IDs and choose the deepest locus represented in at least two. For a suffix array, maintain a document array and maximize the minimum LCP over rank windows containing at least two distinct IDs. For a generalized SAM, propagate document-presence sets or a compact offline equivalent along suffix links, taking care that duplicate occurrences in one document count once.

Cap every candidate length at source document boundaries. Define whether duplicate document content with different IDs counts as distinct, how normalization is versioned, and whether all tied longest strings or one deterministic tie is returned. Verify each reported slice directly in two immutable source generations.

Evidence should compare with exhaustive substring-set intersection on small multi-document corpora; include empty and duplicate documents, separator-like symbols, common prefixes at boundaries, Unicode/byte differences, many ties, one huge repeated document, and result limits. Corrupt index intervals, document IDs, counts, checksums, and generation pointers and require rejection or rollback rather than partial results. A valid alternative structure must preserve the same factor, distinct-document, boundary, and source-verification invariants.
