# Course 2 Study Plan — Ownership, Lifetimes, and Memory

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **How do places, loans, lifetimes, destruction, shared liveness, representation, and address stability determine whether a memory design is valid?** answerable through construction and explanation.

## Daily rhythm

Use a **pinning contract** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 11: Places, Move Paths, and Advanced Borrowing

**Question:** Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?

**Retrieval:** Without notes, restate the invariant carried from Module 10 — Integration and Independent Change. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 11](./module-11-places-move-paths-and-advanced-borrowing/index.md) with a **place and move-path map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-11-places-move-paths-and-advanced-borrowing/workbook.md) before observation. The day’s minimum result is: **Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Borrow Surgery](../labs/module-01-borrow-surgery/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 11 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 12: Lifetime Relationships and Borrowed APIs

**Question:** What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?

**Retrieval:** Without notes, restate the invariant carried from Module 11 — Places, Move Paths, and Advanced Borrowing. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 12](./module-12-lifetime-relationships-and-borrowed-apis/index.md) with a **lifetime constraint graph** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-12-lifetime-relationships-and-borrowed-apis/workbook.md) before observation. The day’s minimum result is: **Translate lifetime syntax into constraints among borrows rather than durations attached to values.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Zero-Copy Records](../labs/module-02-zero-copy-records/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 12 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Translate lifetime syntax into constraints among borrows rather than durations attached to values.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 13: Scoped Access and Escape Prevention

**Question:** Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?

**Retrieval:** Without notes, restate the invariant carried from Module 12 — Lifetime Relationships and Borrowed APIs. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 13](./module-13-scoped-access-and-escape-prevention/index.md) with a **scope and escape table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-13-scoped-access-and-escape-prevention/workbook.md) before observation. The day’s minimum result is: **Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Scoped Visitors](../labs/module-03-scoped-visitors/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 13 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 14: RAII, Drop, Unwinding, and Failure Atomicity

**Question:** Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?

**Retrieval:** Without notes, restate the invariant carried from Module 13 — Scoped Access and Escape Prevention. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 14](./module-14-raii-drop-unwinding-and-failure-atomicity/index.md) with a **destruction trace** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-14-raii-drop-unwinding-and-failure-atomicity/workbook.md) before observation. The day’s minimum result is: **Derive local, field, tuple, temporary, and scope destruction order from documented rules.** Keep one positive case and one causal negative case.

**Laboratory:** Build [RAII Resource Pool](../labs/module-04-resource-pool/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 14 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Derive local, field, tuple, temporary, and scope destruction order from documented rules.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 15: Box, Deref, Dynamically Sized Types, and Cow

**Question:** When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?

**Retrieval:** Without notes, restate the invariant carried from Module 14 — RAII, Drop, Unwinding, and Failure Atomicity. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 15](./module-15-box-deref-dynamically-sized-types-and-cow/index.md) with a **indirection model** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-15-box-deref-dynamically-sized-types-and-cow/workbook.md) before observation. The day’s minimum result is: **Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Boxed Expression Tree](../labs/module-05-boxed-expressions/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 15 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Places, Move Paths, and Advanced Borrowing, Lifetime Relationships and Borrowed APIs, Scoped Access and Escape Prevention, RAII, Drop, Unwinding, and Failure Atomicity, Box, Deref, Dynamically Sized Types, and Cow** as one dependency chain, rerun the two investigations that changed your model most, and describe the current Memory Workspace state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 16: Rc, Weak, and Ownership Graphs

**Question:** Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?

**Retrieval:** Without notes, restate the invariant carried from Module 15 — Box, Deref, Dynamically Sized Types, and Cow. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 16](./module-16-rc-weak-and-ownership-graphs/index.md) with a **liveness graph** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-16-rc-weak-and-ownership-graphs/workbook.md) before observation. The day’s minimum result is: **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Shared Ownership Graph](../labs/module-06-rc-weak-graph/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 16 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 17: Interior Mutability and Runtime Borrows

**Question:** Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?

**Retrieval:** Without notes, restate the invariant carried from Module 16 — Rc, Weak, and Ownership Graphs. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 17](./module-17-interior-mutability-and-runtime-borrows/index.md) with a **runtime-borrow trace** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-17-interior-mutability-and-runtime-borrows/workbook.md) before observation. The day’s minimum result is: **Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Revisioned Interior Cache](../labs/module-07-interior-cache/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 17 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 18: Memory Representation, Validity, and Layout

**Question:** Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?

**Retrieval:** Without notes, restate the invariant carried from Module 17 — Interior Mutability and Runtime Borrows. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 18](./module-18-memory-representation-validity-and-layout/index.md) with a **representation table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-18-memory-representation-validity-and-layout/workbook.md) before observation. The day’s minimum result is: **Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Layout Observatory](../labs/module-08-layout-observatory/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 18 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 19: Subtyping, Variance, PhantomData, and Drop Checking

**Question:** When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?

**Retrieval:** Without notes, restate the invariant carried from Module 18 — Memory Representation, Validity, and Layout. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 19](./module-19-subtyping-variance-phantomdata-and-drop-checking/index.md) with a **variance and substitution table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-19-subtyping-variance-phantomdata-and-drop-checking/workbook.md) before observation. The day’s minimum result is: **State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Variance Branding](../labs/module-09-variance-branding/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 19 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 20: Pinning and Address-Sensitive Design

**Question:** What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

**Retrieval:** Without notes, restate the invariant carried from Module 19 — Subtyping, Variance, PhantomData, and Drop Checking. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 20](./module-20-pinning-and-address-sensitive-design/index.md) with a **pinning contract** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-20-pinning-and-address-sensitive-design/workbook.md) before observation. The day’s minimum result is: **Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Pinned Tracker](../labs/module-10-pinned-tracker/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 20 in the [Memory Workspace guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add document labels and snapshot comparison to Memory Workspace while preserving stale-handle rejection, bounded retention, and borrowed-view provenance.**

Seven days later, rebuild the ten-module sequence and the core **pinning contract** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
