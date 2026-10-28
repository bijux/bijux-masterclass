## M03C01 – Chaining vs Open Addressing vs Cuckoo Hashing

No visual aids for core concepts: All collision-resolution strategies (chaining, linear probing, cuckoo) are explained purely in text/code with zero diagrams. This makes the differences harder to grasp – e.g. a simple figure of a hash table with chains vs probe sequence would reinforce the concepts.

Heavy jargon without refresher: References to prior module content (e.g. RAPL energy from M02C09, “CV” for timing variance) appear without brief recap. It assumes perfect recall from M02 – a quick reminder would improve clarity.

Minor omission – deletion not implemented: The demo LinearProbe and Cuckoo classes do not handle deletions at all. While deletions weren’t the focus here, it’s worth noting that open addressing requires tombstone handling (mentioned later in text but not demonstrated). This isn’t a correctness bug in context, but it leaves out an important operation in real hash tables.

## M03C02 – CPython dict and set Deep Dive

Missing diagram of layout: The complex “compact dict” structure is described entirely in prose. There is no diagram of the indices array vs entries array. Given the density of detail (embedded indices, tombstones, etc.), a visual schematic is needed for clarity.

Unintroduced term (“free-threading”): The measurement notes mention “free-threading compatibility” – a term not introduced elsewhere in S01. This jargon (referring to the GIL removal efforts) is out-of-scope and likely to confuse, since concurrency isn’t covered in M03. It should be removed or explained.

No forward references beyond scope: (No issues here – M03C02 stays within S01 content and assumes only prior knowledge from M01–M02. All terminology like SipHash, perturbation, etc. is introduced in-module or earlier.)

## M03C03 – When Hash Tables Are the Wrong Tool – Trade-offs

Potential misinterpretation of benchmarks: The demo output juxtaposes a 0.048s array lookup with a 1.268s dict lookup, which naively looks like “array 25× faster than dict.” The text explains not to compare them directly (different probe counts), but this nuance is easy to miss. The core could bluntly warn in the results section itself (e.g. an inline note) to prevent false conclusions.

No tree-based example: The core title includes “trees,” but no actual tree implementation is shown – only a sorted list and a mention of SortedDict (coming later). This could feel like a missing piece. Even a brief discussion of how a tree-based map would behave (in theory) would close the loop.

Lack of visuals for performance cliffs: This core presents a lot of numeric results (ratios, memory usage) in text. A simple chart comparing dict vs bisect vs array on different workloads would make the “cliffs” more intuitive. As is, readers must parse dense numbers to internalize the trade-offs.

## M03C04 – Writing Correct __hash__ + __eq__ for Composite Keys

Structural symmetry intact (0–10), content solid – no major issues. (This core is well-scoped and internally consistent with S01.)

Test case for __eq__ not explained: A property-based test checks that Point.__eq__ returns NotImplemented for unrelated types, but the core never explicitly stated this as a rule. It’s a subtle Python detail (for correct equality behavior) that should be mentioned in the “iron rules.” Without calling it out, the Hypothesis test appears to enforce a requirement that learners weren’t formally taught.

Hypothesis used before introduction: The core includes Hypothesis tests in section 8, even though property-based testing isn’t properly introduced until M03C09. While advanced students can infer what’s happening, this forward use of Hypothesis is abrupt. It would be clearer to either postpone these tests or briefly introduce Hypothesis when it first appears here.

## M03C05 – Sets, Multisets, Maps, Multimaps – Choosing the Right Abstraction

Section numbering off-by-one: This core has 12 sections (0–11) instead of the standard 11. The “Progress note & what’s next” is incorrectly labeled as 11 (should be 10). This breaks the structural consistency – an obvious editing error. No section should be numbered 11 in M03.

Inconsistent “small N” advice: Earlier modules (M03C03, M03C05) say very small collections (up to 500–1000 items) can use lists/tuples, yet the final summary (M03C10) revises this to 50–100. This contradiction in threshold is confusing. Which is it – 1000 or 100? The guidance drifts drastically, undermining credibility. It needs a single, evidence-backed number (likely the lower range is realistic).

OrderedDict mention is dangling: The table in section 2 lists “dict (3.7+) or OrderedDict” for ordered iteration, but the core never discusses OrderedDict again. This could leave a student wondering if they need to learn OrderedDict. The note should explicitly say that modern dict obsoletes OrderedDict for most purposes (which is implied but not stated).

No examples of pitfalls beyond timing: The core asserts the stdlib tools are 2–100× faster or cleaner, but aside from timings it doesn’t show other failure modes of “naïve” approaches. For instance, it could have demonstrated a bug or complexity in a manual multimap vs the simplicity of defaultdict. As is, the argument rests purely on speed/readability claims without concrete contrasting code examples (missed didactic opportunity).

## M03C06 – Ordered Maps via bisect/sortedcontainers – Trade-offs

No major structural or scope issues. (Sections 0–10 are present and content stays within M01–M05 knowledge.)

Reliance on external library without internals: The core asks to pip install sortedcontainers and treats SortedDict as a black box. It delivers performance info but doesn’t diagram how SortedDict works (e.g. B-tree vs skip list). Learners are left accepting “SortedDict is logₙ” on faith. A short explanation or visual of its internals would bolster understanding of why it has higher memory and slower lookups compared to dict.

Slight redundancy from prior core: The “Decision rule – explicit and final” in section 2 repeats the same bullet points from M03C05/M03C03. By now this is the third time seeing “Use dict for X, SortedDict for Y…” verbatim. It starts to feel like copy-paste filler. This could be tightened or referenced rather than repeated wholesale.

No discussion of build costs for SortedDict: The content presents build timings and memory usage, but doesn’t explicitly highlight that inserting into a SortedDict repeatedly is costly. It’s implied by the numbers, but an explicit note like “SortedDict pay a heavy insertion cost (as seen by slower build time)” would drive home the point for those skimming the tables.

## M03C07 – Hash vs Tree vs Flat Array – Performance at Scale

Structural symmetry maintained (0–10) – content largely correct.

Redundant decision matrix recap: Yet again, section 2 recaps which structure to use when, duplicating M03C06’s and earlier advice. By this stage, repeating the same bullet list is tedious. It eats space and adds “noise” before the new content (50M-scale analysis). The core should dive into the four-contender comparison without rehashing prior modules’ guidance.

Confusing performance table ordering: The memory and timing results are solid, but the way they’re presented can be confusing. For example, the text says “tree/flat are >700× faster for range-heavy workloads” immediately after a table where times are in seconds (making it hard to see 700× without calculation). A clearer call-out or chart of the relative speedups at 10^7–10^8 would better illustrate that dramatic 700× factor. Currently, the reader must infer the “× faster” from scattered data points.

No explicit pointer-based tree example: The core continues to refer to “tree vs flat vs hash” at scale, but still no actual tree implementation is shown (SortedDict stands in for “tree-like”). Students never see a true pointer-based tree in action. While SortedDict is a pragmatic stand-in, an explicit note could clarify: e.g. “(SortedDict uses a B-tree internally, representing the ‘tree’ category here).” Otherwise, the takeaway “trees are slower on random lookups” lacks concrete context since a real tree wasn’t illustrated.

## M03C08 – Small Python Map Implementation with Explicit Invariants

Duplicate “carry forward” sections (editorial blunder): This core bizarrely has two summary sections. “What you must carry forward – measured truth only” appears as section 6 and again (slightly rephrased) as section 9. This is clearly a mistake. It breaks the flow and repeats points (e.g. “never ship a pure-Python hash table”) that were already stated a few sections earlier. One of these sections is extraneous and should be removed to restore a logical progression.

Structural count off: Due to the duplication above, the section numbering goes 0–9 and then an unnecessary 9 again, before 10. This means the core technically has 12 numbered sections, violating the expected 11. It’s an alignment error caused by the redundant content.

No mention of tombstone accumulation: The TinyMap implementation handles deletions with tombstones, but the core never addresses the long-term impact (many tombstones can degrade performance unless periodically cleaned up). In real hash tables, a resize or rehash is often triggered by tombstone ratios as well. TinyMap’s _resize only checks load factor of live entries. This omission isn’t a fatal flaw for the demo, but it leaves out an edge-case detail of open addressing (i.e. without tombstone reclamation, performance can degrade even if invariants hold).

Quadratic probe limitation not highlighted: TinyMap uses quadratic probing with a power-of-two table, which does not guarantee visiting every slot (they note this in a code comment but nowhere in the main text). This is an important theoretical caveat. A student might wrongly assume the TinyMap probe is fully robust. The core should explicitly state that real implementations use probe sequences ensuring full coverage (e.g. double hashing or triangular numbers with table prime-sized) – whereas TinyMap chooses simplicity over a “guaranteed hit” probe cycle.

Hypothesis introduced without prelude (again): This core uses Hypothesis (@given decorator in section 5) to validate invariants, yet the concept of property-based testing isn’t formally introduced until M03C09. By now Hypothesis has appeared in two cores with zero explanation. This is a pedagogical miss – the course is using a powerful testing tool without ever teaching it in its own right. Even a brief forward-reference (“we’ll cover Hypothesis in depth in M03C09, but here’s a sneak peek”) would legitimize its usage here.

## M03C09 – Hypothesis-Based Tests + Adversarial Key Distributions

Embedded wrong content (serious error): In the middle of the Hypothesis strategies section, there is an inexplicable insertion of text from M02C09 (loop-soup discussion). Specifically, lines about “M02C09 gives you the mechanical discipline…” through an example of range updates appear out of nowhere. This has nothing to do with hash tables or testing – it’s a copy/paste error that will completely derail the reader. This chunk must be removed; it’s clearly an unrelated fragment erroneously left in the core.

Section 10 is missing: This core only has sections 0–9 (Progress note is numbered 9). It falls short of the 0–10 structure used throughout M03. Likely the “Progress note & what’s next” should have been section 10, not 9. The numbering lapse is another consistency problem, though less egregious than others.

No explicit intro to Hypothesis (finally arrives here): This is the first time the curriculum actually explains Hypothesis and property-based testing – and it does a decent job in showing strategies and tests. However, by this point the student has already encountered Hypothesis code twice without context. The damage is done. The core should have formally introduced Hypothesis before using it in earlier cores. As it stands, the teaching order is backwards.

Adversarial tests lack a failure demo: The property tests given are excellent and thorough (they would catch bugs if present), but the core doesn’t illustrate an actual bug being found. It would be more convincing to deliberately break TinyMap (as suggested in the exercise) and show Hypothesis finding the minimal counterexample. The demonstration section hints at this (testing a BrokenTinyMap), but it’s very brief. A short narrative like “Hypothesis shrunk a failing case to just 2 keys colliding, exposing our resize bug” would drive home how powerful this tool is. Without it, some might underestimate what was achieved (unless they do the exercise).

Mutable-key advice buried: The core wisely notes “Mutable keys are poison” (in carry-forward bullet 5) – meaning you should make such objects unhashable or copy them on insert. However, this crucial point is somewhat buried at the end. Earlier in M03C04 we discussed not mutating keys, but here we finally address making keys immutable or defensive copying. This point deserved more emphasis (perhaps in M03C04 itself). As is, a reader could easily gloss over it.

## M03C10 – Final Summary: When Hash Tables Are the Wrong Tool, and Why

Does not follow required section format at all: This “final summary” core breaks the mold entirely – it has no 0. Why you care section and only uses sections 1–5. It’s essentially a free-form summary. While the content is logically organized, it flagrantly violates the structural symmetry mandated for all cores. Every other core has 11 sections (0–10); this one has half as many. It needs to be retrofitted into the standard template (e.g. a brief section 0 introduction, and possibly splitting content to reach a section 10 conclusion). As it stands, M03C10 sticks out like a sore thumb format-wise.

Forward reference to concepts outside S01: In section 3’s note, it suddenly mentions “databases/B-trees/LSM trees/tries” as alternatives once you need persistence or huge data. These data structures were never covered in S01 (they’re well beyond M03’s scope). Dropping them in a final cheat sheet without context is jarring. It might prompt questions the course isn’t ready to answer. If the intention is to foreshadow S02 content, it should explicitly say so – otherwise this line should be removed to avoid confusion.

Inconsistent small-N cutoff (again): This summary says “very small N (≲50–100) use list/tuple,” directly contradicting M03C03 and M03C05 which said “≲500–1000.” This inconsistency is glaring in a cheat sheet meant to provide clear guidance. Which number should the student trust? This final core undermines earlier advice without explanation. It needs to reconcile this difference (most likely by adopting the smaller 100-element cutoff and clarifying in those earlier cores that 1000 was too high).

No progress note or next module pointer: Since this is the final core of M03, it would typically conclude with a progress note transitioning to M04. There is a brief mention “You are ready for M04: Asymptotics…,” but it isn’t formatted as a Progress note & what’s next section. Given this is the capstone of S01’s hash table module, it should still explicitly label the transition. Right now it’s just a line in section 5. This is a minor structural nitpick, but for consistency one might expect a section 10 saying “M03 complete – next is M04…”.

Overall tone is fine, but opportunity for recap quiz missed: The final summary does a good job listing outcomes and decision matrices. However, it might be pedagogically weak in engagement – it just hands the answers. A common elite-curriculum technique is to pose a few recap questions or challenges to ensure the student internalized the cheat sheet (e.g. “Given scenario X, which structure and why?”). This core could be more interactive. As is, it’s a passive summary (not a “problem” per se, but a missing chance to reinforce learning in an active way).


# 2nd

No, M03 is not yet structurally A+ under your “0–10, symmetric, S01-only” constraints. Here’s the nuclear issue list.

---

## 1. Structural / symmetry violations (0–10 template)

Your stated rule: **each core must have 11 sections, numbered 0–10, with a consistent structure**.

### M03C01, C02, C03, C04, C06, C07, C08

* These mostly follow the 0–10 pattern with “0. Why you care”, “1. Scope reminder”, …, “9. What you must carry forward”, “10. Progress note & what’s next”. That part is fine for:

  * C01 
  * C02 
  * C03 
  * C04 
  * C06 
  * C07 

But there are deviations in others:

### M03C05 – **extra section 11**

* Numbering runs **0–11**, not 0–10.
* After the standard “### 10. What you must carry forward – measured truth only”, there is:

  * **“### 11. Progress note & what’s next in M03”**.
* That breaks the 0–10 template and gives this core 12 sections.

### M03C08 – **duplicated “What you must carry forward”**

* C08 has:

  * **“### 6. What you must carry forward – measured truth only”** with a bullet list. 
  * Later, **“### 9. What you must carry forward – measured truth only”** with a *different* bullet list and the same concluding line “You have crossed the threshold from ‘user’ to ‘builder’ of hash tables.”
* So:

  * Two sections with the same title.
  * The global pattern “section 9 = What you must carry forward” is broken by putting that title also at section 6.
  * The motivational “user → builder” line appears twice.

### M03C09 – **off-by-one numbering**

* C09 runs 0–9 and **stops at 9**:

  * “### 6. What you must carry forward – measured truth only”
  * “### 7. Exercise (mandatory)”
  * “### 8. Demonstration – Hypothesis finds bugs instantly”
  * “### 9. Progress note & what’s next in M03”
* There is **no section 10** here.
* In the rest of S01, “Progress note & what’s next” is consistently section 10, not 9, so this core breaks that symmetry and the “0–10” rule.

### M03C10 – **no section 0, truncated structure**

* C10 has:

  * Title + introductory paragraph, then:
  * “### 1. The measured truth – when hash tables win”
  * “### 2. When hash tables lose – measured cliffs”
  * “### 3. The final decision matrix (your permanent cheat sheet)”
  * “### 4. The measured invariants you now own”
  * “### 5. M03 is complete”
* Problems:

  * There is **no “0. Why you care”** section.
  * Numbering stops at **5**, not 10.
  * There is no explicitly numbered “What you must carry forward – measured truth only” section; it’s implicitly embedded in section 4.
  * There is no “10. Progress note & what’s next” – instead “M03 is complete” is section 5.

**Net effect:** M03 violates your structural symmetry rule in **C05, C08, C09, C10**, plus minor naming drift of “Progress note” vs “M03 is complete”.

---

## 2. Scope leaks beyond S01 (M01–M05) and S01 Python focus

You asked to keep S01 as self-contained as possible and flag references that clearly belong to later series (S02+, S03+, S05+, etc.).

### Explicit forward references to advanced storage / concurrency

* **M03C10** explicitly says:

  > “Once you care about persistence, concurrency, or very large on-disk data, you are choosing between databases / B-trees / LSM trees / tries, not just Python containers.” 
* B-trees, LSM trees, and on-disk index design are clearly S05 topics (M22 etc.), and concurrency is S04; that’s a deliberate forward reference outside S01.

### Cross-language / systems-library references

* **M03C01** uses real-world examples in the comparison table: Rust hashbrown, SwissTable, Abseil, and “C/Rust implementation” as the place where pointer-chasing effects blow up.
* Conceptually fine, but it’s already leaning into S03 (“Systems Programming for DS in Rust/C++”). If you want S01 to be strictly “Python-only foundations,” these cross-ecosystem references are scope creep.

### Within-S01 references (acceptable)

* References from M03 to:

  * M01 object/memory model,
  * M02 perf tooling / RAPL / `perf stat -d` (e.g. in M03C01 “If you have RAPL access (M02C09)…”),
  * M04 (at the end of M03C10: “You are ready for M04…”), 
    are all within S01 and consistent with your stated S01–M01..M05 scope.

---

## 3. Alignment with the M03 toplevel spec (10 bullets vs actual cores)

Compare the S01–M03 bullets to the implemented cores:

1. **Chaining vs open addressing vs cuckoo hashing: trade-offs**

   * M03C01 covers this in detail; aligned.

2. **CPython dict/set: layout, perturbation, order guarantees**

   * M03C02 matches: layout, indices/entries, perturbation, order, memory. 

3. **Load factor, clustering, tombstones, resize policies**

   * Content exists, but it’s **fragmented**:

     * Load factor + clustering in M03C01. 
     * Load factor + resize + tombstones in M03C02. 
     * Invariants (incl. load factor bound, power-of-two size) in M03C08. 
   * There is **no core explicitly titled** with this bullet – the spec suggests a single focused unit, while the material is spread across three cores.

4. **Writing correct `__hash__` + `__eq__` for composites**

   * M03C04 matches cleanly (rules, demos, Hypothesis tests). 

5. **Sets, multisets, maps, multimaps – choosing the right abstraction**

   * M03C05 matches.

6. **Ordered maps via `bisect`/`sortedcontainers` vs tree-based maps**

   * M03C06 covers `dict`+sorted, sorted list + bisect, `SortedDict`. 
   * The **“tree-based maps” part is weak**:

     * There is no actual tree implementation or tree invariants here; just `SortedDict`, which internally uses block-sorted lists rather than a classic tree, and it is not presented as a tree per se in C06.

7. **Hash vs tree vs flat array: performance and memory sketches**

   * M03C07 covers dict vs SortedDict vs flat list + bisect vs dict+sorted keys, including a summary table of operations and memory per entry. 
   * The chapter explicitly admits SortedDict is only a *stand-in* for a tree:

     > “SortedDict is our stand-in for a ‘tree-like’ logarithmic ordered map…” 
   * So again, the “tree” in the spec is somewhat indirect / abstract.

8. **Small Python map implementation with explicit invariants**

   * M03C08 matches well (TinyMap with invariants + tests).

9. **Hypothesis-based tests + adversarial key distributions**

   * M03C09 matches.

10. **When hash tables are the wrong tool, and why**

* Implemented in **two** places:

  * M03C03 – detailed measured trade-offs (dict vs sorted list vs dense array).
  * M03C10 – final decision table + summary.
* This means the tenth bullet’s content is **duplicated**, not cleanly isolated in a single core.

---

## 4. Cross-core duplication and decision-matrix repetition

There’s an intentional “drumbeat” of the same message across cores, but for a canonical reference you should be aware where duplication is highest:

* **M03C03, M03C06, M03C07, M03C10** all state some variant of:

  * “dict wins for random access,”
  * “SortedDict / sorted list + bisect win for range/prefix,”
  * “arrays/bitvectors win for dense integer keys,”
  * “small N → list/tuple is often good enough.”
* **M03C05 and M03C10** both give mapping problem → stdlib tool tables (set/Counter/defaultdict/dict/list).
* **M03C08** repeats the same “You have crossed the threshold from ‘user’ to ‘builder’ of hash tables” line twice.

This isn’t “wrong”, but it is **not minimal**; for a 2030-grade canonical text you probably want C10 to be a pure, deduped, final cheat sheet that doesn’t rehash earlier tables.

---

## 5. Cross-chapter promises vs delivered content

A few small mismatches:

* **M03C02 → M03C03 promise**

  * C02 says C03 will give:

    > “measured trade-offs against trees, flat arrays, and sorted structures at scale.” 
  * C03 actually compares dict vs sorted list + bisect vs dense `array.array`, but **no tree-like structure** appears there; the tree-like/SortedDict comparison only shows up later (C06/C07).

* **M03C07 title vs implementation**

  * Title: “Hash vs Tree vs Flat Array – Performance Sketches at Scale.”
  * Implementation: uses `SortedDict` as a tree proxy, and explains that it is block-structured lists rather than a pointer-based tree. This is honest, but it means the “Tree” word in the title is somewhat approximate, not literal. 

These are small, but they matter if the coursebook is supposed to be extremely precise about what each core does.

---

## 6. Technical nuance / tone consistency

No obvious hard bugs, but a few places where the **tone** conflicts across cores:

* **M03C01**:

  * “In Python: just use dict/set – they are extremely well-tuned open-addressing tables with all necessary defences already built in.” 
* **M03C03/C06/C07/C10**:

  * Repeatedly show when dict is the wrong tool and alternatives win by 10–1000×.
* Not a contradiction (C01 is about **hash-table design choice**, not “never use alternatives”), but the absolutist wording in C01 sits slightly awkwardly with the nuanced decision matrices later.

Also:

* Many tables give **quite specific** timing/memory numbers on one machine and then say “only ratios matter.”
  For a 2030-reference, you may want a more explicit meta-frame on “how to recompute these numbers yourself” rather than anchoring too hard on 2025 hardware.

---

### Bottom line

* **Structurally**: C05, C08, C09, and C10 violate your 0–10, 11-section symmetry; C08 also has duplicated key sections.
* **Scope-wise**: M03 largely stays inside S01, but C10 explicitly points at B-trees/LSM/tries (S05) and C01 leans into Rust/C++ libraries (S03).
* **Spec alignment**: bullets 3, 6, 7, and 10 are either fragmented across cores, only indirectly realised (“tree-like” via SortedDict), or duplicated (C03 vs C10).
* **Content**: technically solid, but with some tone inconsistencies and heavy repetition of the decision matrix story.

If you fix the structural numbering, dedupe the overlapping decision matrices, and tighten the forward references, M03 is very close to the 2030-grade canonical reference you want.
