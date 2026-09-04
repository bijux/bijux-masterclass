---
module_id: CA-027
program: Computer Architecture
level: 1
module_number: 27
title: Control Hazards
status: complete
last_verified: 2026-09-04
---

# Control Hazards

## One-Page Review

### Governing question

How can a processor keep its front end productive before the next architectural PC is known, then recover exactly when a prediction or provisional path is wrong without allowing wrong-path tokens to commit or create forbidden effects?

### Essential definitions

- A **control-flow instruction** can select a next PC other than ordinary sequential progression.
- A **control hazard** arises when fetch must choose a path before the controlling instruction's outcome or target is definitive.
- A **prediction** is a provisional direction, target or return choice used to continue fetching.
- **direction prediction** estimates whether a conditional branch is taken.
- **target prediction** estimates the next address if control transfers.
- A **branch target buffer** (`BTB`) caches control-flow identity and predicted targets/metadata.
- A **branch history table** (`BHT`) uses state such as saturating counters to predict direction.
- A **return-address stack** (`RAS`) predicts return targets using call/return nesting.
- A **misprediction** occurs when predicted direction, target, length/type or path identity disagrees with the resolved outcome.
- **resolution** is the point at which actual control-flow outcome and required checks are definitive.
- A **redirect** installs the correct fetch PC and invalidates incompatible younger work.
- A **fetch epoch** or generation tags work so responses from an obsolete path can be rejected.
- **prediction penalty** is lost work/cycles attributable to recovery, not simply pipeline depth.
- **speculative state** is microarchitectural state updated before architectural commit under a recovery/security contract.
- A **wrong-path instruction** was fetched under a prediction that will not become the architectural path.

### Central model, mechanism, or theorem

For control instruction token `b` with architectural pre-state `S`, predictor `P` selects provisional next PC `p_hat` and prediction identity `e`. Resolution computes permitted next PC `p=NextISA(S,b)` or a precise trap. If `p_hat=p` with compatible type/length/context, younger tokens may remain. Otherwise redirect to `p`, advance the fetch epoch, and invalidate exactly the younger tokens and stale responses belonging to the old path. Correctness requires that only the resolved architectural path can commit and that predictor/speculative updates cannot alter architectural results or cross prohibited security boundaries.

### Critical invariants

- Every fetched token carries PC, instruction identity and enough prediction/epoch metadata for recovery.
- Sequential, direct, indirect, return, exception and interrupt next-PC sources have explicit priority.
- Resolution compares both direction and target/type context, not direction alone.
- Redirect preserves older work and the resolving instruction's permitted effect while killing incompatible younger work.
- Wrong-path or stale-epoch tokens cannot write architectural state, issue forbidden side effects or retire.
- Outstanding instruction responses are discarded or reclassified only under a proven epoch/tag rule.
- Predictor lookup/training uses the intended PC/context and updates at a named safe point.
- A killed branch cannot train state unless the policy explicitly permits and security analysis covers it.
- Return prediction cannot substitute for architectural return semantics or privilege checks.
- Performance claims combine frequency, control-flow mix, accuracy, penalty and recovery bandwidth.

### Common failures

Common failures include assuming every branch is conditional, predicting direction without a target, comparing only taken/not-taken while using a wrong target, updating PC twice, flushing the resolving branch, letting a stall defeat a redirect, accepting late wrong-path fetch data, training on killed instructions, aliasing predictor entries across contexts without policy, underflowing/overflowing a RAS silently, trusting an indirect target before alignment/permission checks, counting accuracy without weighting penalty, using total pipeline depth as universal penalty, and treating noncommitting speculation as free of security-visible effects.

### Compact example

For a synthetic 1,000-instruction finite run with 20% branches and a five-stage base of 1,004 cycles, resolving every branch with two lost cycles gives 1,404 cycles at 1.25 ns, or 569.80 MIPS. A 70%-accurate static predictor gives 1,124 cycles at 1.32 ns, or 674.00 MIPS. A 92%-accurate dynamic predictor gives 1,036 cycles but its 1.48 ns period yields 652.20 MIPS. Reducing dynamic recovery to one cycle gives 1,020 cycles and 662.43 MIPS. Higher accuracy alone does not prove higher throughput.

### Connections

Control hazards connect ISA next-PC semantics, pipeline flushes, prediction tables, cache/fetch protocols, precise exceptions, speculation security, formal trace refinement, compiler layout and performance measurement.

## Governing Question

Fetch needs an address before later stages may know whether a branch is taken or where an indirect jump lands. Waiting preserves correctness but wastes potential overlap. Prediction uses a reversible guess to trade recovery work for front-end utilization.

The controlling principle is asymmetry: provisional microarchitectural work may occur only within a contract that guarantees wrong-path architectural effects are suppressed and security-relevant effects are analyzed. Correct-path performance does not relax that boundary.

## Why This Matters

Branch behavior limits pipeline throughput as resolution moves later or issue width grows. A front end can fetch many wrong instructions during a few unresolved cycles, increasing energy and recovery pressure.

Direction accuracy is only one variable. Target availability, instruction alignment, predictor latency, redirect bandwidth, cache response cancellation, pipeline period and workload distribution determine useful speed.

Speculation can affect caches, predictors, translation structures and contention even when instructions never retire. Architectural correctness and confidentiality/integrity assurance require distinct evidence.

## Prerequisites and Retrieval

Before studying this module, be able to:

- derive sequential and control-transfer PCs from an ISA;
- trace valid/age-tagged tokens through a pipeline;
- distinguish stalls, bubbles, kills and redirects;
- explain precise commit and exceptions;
- compute CPI, frequency and throughput.

Retrieve exact ISA/profile/extensions and compressed/variable-length rules; conditional/direct/indirect/call/return encodings; target arithmetic and alignment; exception priorities; pipeline/fetch stages; resolution points; prediction sources and priority; BTB/BHT/RAS structures, indices, tags, context partitioning and replacement; history/checkpoint state; update/training policy; fetch request/response protocol; epochs/tags and wrap bound; redirect/flush equations; caches/TLB/predecode; interrupt/debug/reset interaction; speculative side-effect inventory and threat model; compiler/binary/control-flow traces; counters; synthesis/STA/area/power; formal properties/refinement; tests/coverage; hardware/errata; and exact RTL/configuration/tool/library/revision data.

## Learning Objectives

After completing this module, you should be able to:

1. derive the actual next PC for sequential, branch, jump, return and trap cases;
2. distinguish direction, target, type and return prediction;
3. design static and dynamic predictor state with explicit identity/context;
4. attach prediction metadata and epochs to pipeline tokens;
5. resolve control flow and generate an age-correct redirect;
6. suppress or contain wrong-path and stale-response effects;
7. integrate predictor training, exceptions, interrupts, debug and reset;
8. compute accuracy-, penalty- and period-adjusted performance;
9. verify safety, recovery, progress and ISA refinement;
10. scope speculative security claims separately from architectural correctness.

## Core Exposition

### Start with architectural next-PC semantics

For every instruction class, define sequential PC, taken condition, direct/indirect target, link value, alignment requirements and possible traps. Include actual instruction length where compressed or variable-length encodings exist.

Prediction does not change these semantics. Resolution must reproduce the ISA transition using the instruction's architectural operands and PC.

### Identify the uncertainty window

Mark when fetch needs a next PC and when direction/target become definitive. The cycles and fetch width between those points bound wrong-path work, but buffers and memory latency can extend recovery effects.

Moving resolution earlier can reduce penalty while lengthening decode/compare/target timing or requiring additional forwarding.

### Establish a correct wait baseline

A no-prediction controller can stop fetch until control flow resolves. This is a useful correctness reference and may suit very small cores.

It still needs exact hold/advance logic and must handle direct jumps, returns, traps and late fetch responses. “Do nothing” is not a complete protocol.

### Use static policies deliberately

Always-not-taken continues sequentially and redirects taken branches. Always-taken needs a target early. Direction by displacement or compiler hint can exploit workload patterns but remains a prediction.

Measure policy per control-flow class. Unconditional direct jumps should not be counted as direction-prediction failures if their targets are available deterministically.

### Predict direction dynamically

A one-bit entry remembers the last outcome; a two-bit saturating counter resists changing prediction after one anomaly. Indexing by PC bits creates aliasing when several branches share an entry.

Global/local histories can capture correlations but increase state, latency and recovery complexity. State width is not a substitute for measured accuracy and timing.

### Predict targets

A BTB supplies target and often branch type/metadata before decode. Tags reduce destructive aliasing; partial tags trade storage against false hits.

Validate the predicted instruction boundary and context. A BTB hit on a non-control instruction or stale mapping must resolve and recover safely.

### Predict returns

Calls push a predicted return address; returns pop or peek it. Tail calls, exceptions, context switches, recursion depth, speculative calls and mismatched paths complicate the stack.

Checkpoint or repair RAS state on recovery. Underflow/overflow has a defined fallback such as BTB/indirect prediction or waiting; it cannot invent architectural semantics.

### Predict indirect branches

Indirect targets depend on a register value and may have many destinations. Target caches/history/context can improve prediction. Architectural alignment and privilege/memory checks remain mandatory at resolution/fetch.

Security policies may restrict sharing or speculation for indirect targets. Mitigations and threat assumptions must be explicit and current for the deployed design.

### Attach prediction metadata

Each token carries predicted next PC or sufficient reconstruction, prediction source/type, history/checkpoint identifier, fetch epoch and instruction identity. Resolution compares the actual outcome against the exact prediction made.

Without attached metadata, looking up current predictor state later can compare against a different entry/version and misclassify recovery.

### Resolve direction and target

Use forwarded architectural source values, definitive instruction PC/length and decoded immediate. Resolve traps such as misalignment according to ISA priority.

A direction-correct prediction with a wrong target is still a misprediction. Type errors, e.g. return predicted as ordinary indirect jump, may require metadata repair even if address matches.

### Redirect atomically

One control event selects the correct PC, increments/changes epoch as needed, kills targeted younger tokens and repairs speculative predictor state. Its priority relative to older exceptions, reset and debug is explicit.

Do not let separate PC-write and flush equations disagree. A redirect that changes PC but leaves a wrong-path store live is incorrect.

### Kill exactly the younger set

The resolving branch/jump normally survives and may write its link destination; older instructions continue. Younger incompatible tokens are invalidated before forwarding, requests, writeback or commit.

Stage position can establish age in a simple in-order pipeline. Queues, multiple issue and replay require sequence identities and age comparison.

### Handle outstanding fetches

Instruction-cache or memory responses may return after redirect. Tag each request with epoch/identity, cancel only if protocol permits, or receive and discard stale responses without converting them into tokens.

Epoch wrap must not alias a still-outstanding old response. Prove a bound or use enough identity/retirement discipline.

### Govern wrong-path side effects

Architectural writes from killed tokens are forbidden. Memory writes and irreversible requests must not be issued from unvalidated wrong-path instructions unless a stronger transactional recovery contract exists.

Microarchitectural reads and updates can change cache/predictor/TLB state or contention. Functional retirement checks do not prove confidentiality; apply a threat model, partitioning/flushing/serialization/constant-time policies and security testing as appropriate.

### Train at a named point

Predictor update can occur at resolution for timeliness or at commit for certainty. Resolution-time training needs rollback/suppression for branches later killed by older faults; commit-time training may lag.

Specify outcome, target, type, history and RAS update independently. Avoid double training during replay.

### Recover speculative history

If prediction shifts global/local history before resolution, checkpoint enough state to restore the correct prefix or recompute it. Multiple unresolved branches require nested or tagged checkpoints.

Recovery should apply actual resolved outcome once, then discard younger speculative contributions. Assertions can compare history against a shadow committed/resolved model.

### Integrate data hazards

Branch comparison and indirect targets consume registers. If operands are pending, forward or stall; resolving from stale data creates a false redirect.

Earlier resolution often adds bypass paths into decode. Include their mux/compare delay in frequency analysis.

### Integrate structural hazards

Redirect fetch competes with sequential fetch, instruction-cache ports and translation resources. Give recovery sufficient priority/capacity so a full queue cannot prevent correction.

Predictor tables may have limited read/write ports. Simultaneous lookup and training require defined arbitration or banking/bypass behavior.

### Integrate precise exceptions

An older fault dominates a younger branch redirect. The faulting token produces trap state; younger control-flow effects and training are killed according to policy.

A fault on the branch itself uses its PC/cause and suppresses normal target/link effects. Trap vectors are architectural/system control flow, not branch predictions.

### Integrate interrupts and debug

Interrupt acceptance at an architectural boundary selects a trap PC and invalidates younger provisional work. Predictor state treatment follows the implementation/security policy.

Debug halt and single-step require an exact stopped PC and no wrong-path commit. Breakpoints in fetch versus commit have different speculative observability.

### Reset predictor and path identity safely

Reset invalidates live pipeline tokens and fetch responses. Predictor structures may reset to a policy state, retain state, or be scrubbed; document confidentiality/integrity implications.

Epoch and RAS/history state need deterministic safe initialization. Reset release follows clock/interface timing requirements.

### Compute meaningful accuracy

Report denominator and classes: conditional direction, BTB targets, returns, indirects and all redirects. Accuracy can be per prediction, branch or instruction; mixing definitions misleads.

Weight misses by actual recovery cost. A late indirect target miss can cost more than an early conditional correction.

### Compute instruction time

A simple model is `CPI = CPI_base + sum_i f_i*m_i*P_i`, where `f_i` is event frequency per instruction, `m_i` miss probability and `P_i` nonoverlapped penalty. Time is `CPI*T_clk`.

Include fill/drain, cache interaction, redirect bandwidth and overlapping causes. Predictor lookup/muxing may lengthen `T_clk` even as misses fall.

### Measure energy and capacity

Wrong-path fetch/decode consumes energy and bandwidth. Larger predictors add access/clock/leakage energy. Track useful versus squashed work and energy per retired instruction.

Capacity/access patterns can change physical layout and frequency. Evaluate actual macros and routing, not entry counts alone.

### Verify control-flow safety

Assert actual next-PC arithmetic, metadata coherence, direction/target comparison, one redirect, age-correct kill, stale-epoch rejection, killed-side-effect suppression, training policy and RAS/history recovery.

Use symbolic branch identities and random response timing. Compare commit/trap PC traces to an independent ISA model.

### Prove recovery progress

Under eventual fetch/memory response and downstream progress assumptions, a redirect must eventually admit the correct-path token. Repeated stale responses or a full queue cannot starve recovery.

Bound or measure redirect latency. Safety alone permits permanent front-end deadlock.

### Gather layered evidence

Use directed branch/jump/return/indirect cases; target/alignment boundaries; nested histories; aliasing; simultaneous stalls/faults/redirects; random outcomes and fetch latency; reset/debug/interrupt; formal safety/liveness/refinement; synthesis/STA/area/power; counter validation; workload traces; hardware testing and errata review.

Bind evidence to exact ISA/configuration, RTL, predictor geometry/initialization, cache/TLB, constraints, tools/libraries, compiler/binary, workload/seeds, hardware and mitigations. Prediction results do not generalize without those identities.

## Definitions and Notation

- `b`: resolving control-flow instruction token.
- `S`: architectural pre-state for `b`.
- `p_hat`: predicted next PC attached to the token.
- `p`: actual ISA-permitted next PC or trap destination.
- `e`: fetch epoch/generation identity.
- `f_i`: frequency per retired instruction of control-flow class `i`.
- `m_i`: misprediction probability for class `i` under a stated denominator.
- `P_i`: nonoverlapped recovery penalty in cycles for class `i`.
- `T_clk`: implemented clock period including predictor/redirect paths.
- **correct path:** instruction sequence selected by resolved architectural control flow.
- **wrong path:** provisional sequence incompatible with a later resolution.
- **training:** update of predictor state from a resolved/committed event.
- **checkpoint:** saved speculative state used to recover an older prefix.
- **aliasing:** distinct control-flow contexts map to shared predictor state.
- **path identity:** metadata distinguishing requests/tokens from different provisional fetch streams.

## Mechanisms, Invariants, or Proof Structure

1. **Semantics obligation:** actual sequential, branch, jump, return and trap PCs match the exact ISA/configuration.
2. **Metadata obligation:** every predicted token carries coherent PC, length/type, predicted target/source and path identity.
3. **Resolution obligation:** definitive operands and checks determine actual direction/target exactly once.
4. **Comparison obligation:** direction, target, type/context and exception outcome are compared against the attached prediction.
5. **Redirect obligation:** a mismatch atomically selects the correct PC and recovery state.
6. **Age obligation:** redirect preserves permitted older/resolving work and kills exactly incompatible younger tokens.
7. **Stale-response obligation:** old-path fetch responses cannot become current live tokens, including across epoch wrap.
8. **Side-effect obligation:** wrong-path/killed tokens cannot perform prohibited architectural or irreversible effects.
9. **Training obligation:** lookup and update use correct identity and named resolution/commit/kill policy exactly once.
10. **History/RAS obligation:** speculative state checkpoints, recovery, underflow/overflow and context behavior are defined.
11. **Exception obligation:** older/faulting events have precise priority and suppress incompatible redirects/training.
12. **Reset/debug obligation:** reset, interrupt and debug yield a defined architectural PC with no stale-path revival.
13. **Progress obligation:** under stated fairness, redirect recovery eventually fetches/adopts the correct path.
14. **Timing/security obligation:** prediction/redirect paths meet timing and speculative effects satisfy the declared threat policy.
15. **Evidence obligation:** accuracy, penalty, performance and security claims bind to exact implementation/workload artifacts.

## Alternatives and Trade-Offs

1. **Wait versus predict:** waiting is compact/predictable; prediction improves utilization with recovery/state cost.
2. **Static versus dynamic:** static policy is small; dynamic state adapts to behavior and can alias.
3. **One-bit versus two-bit:** one-bit adapts quickly; hysteresis resists isolated reversals.
4. **Local versus global history:** local captures per-branch patterns; global captures correlation and interference.
5. **Small versus large tables:** small structures are fast/cheap; capacity reduces aliasing at access/energy cost.
6. **Partial versus full tags:** partial tags save storage; fuller identity reduces false target hits.
7. **BTB versus decode target:** early target prediction reduces bubbles; decode calculation avoids stale target state.
8. **RAS versus indirect predictor:** RAS exploits call structure; indirect prediction is general and may be less precise for returns.
9. **Early versus late resolution:** early cuts penalty; late has definitive operands and easier timing.
10. **Resolution-time versus commit-time training:** early update adapts quickly; commit update avoids killed-branch pollution.
11. **Checkpoint versus recompute history:** checkpoints recover quickly with storage; recomputation needs retained trace/time.
12. **Cancel versus discard fetch:** cancellation saves work if protocol supports it; epoch discard is composable but consumes bandwidth.
13. **Shared versus partitioned predictor:** sharing improves capacity; partitioning reduces interference/security coupling.
14. **Deeper speculation versus bounded window:** depth increases overlap; bounds simplify recovery, energy and assurance.
15. **Accuracy versus instruction time:** a more accurate predictor can lose if access/redirect paths lengthen the clock.

## Failure Modes and Misconceptions

1. “All branches are conditional.” Direct jumps, indirects, calls and returns differ.
2. “Direction prediction supplies a target.” Taken fetch still needs an address.
3. “Correct direction means correct prediction.” Wrong target/type is a miss.
4. “Sequential PC is always PC+4.” Instruction length may vary.
5. “A BTB hit proves the instruction is a branch.” Aliasing/stale entries require validation.
6. “Returns are ordinary indirect jumps.” Call-stack structure offers distinct prediction and failure modes.
7. “RAS state cannot mispredict.” Speculation, depth and unusual control flow disrupt it.
8. “The predictor can be queried again at resolution.” Attached metadata identifies the prediction actually used.
9. “Flush every token on redirect.” Older and resolving work normally survives.
10. “Flush the younger stages later.” They may issue effects before invalidation.
11. “Stall should defeat redirect.” That can retain an obsolete path.
12. “Changing PC is sufficient recovery.” Tokens, requests, history and side effects also need repair.
13. “The cache cancels wrong-path requests.” Only its protocol determines cancellation.
14. “A wide epoch counter cannot wrap incorrectly.” Prove outstanding lifetime/window bounds.
15. “Wrong-path instructions do nothing.” They may alter microarchitectural timing/state.
16. “No wrong-path retirement proves security.” Side channels require separate threat evidence.
17. “Train every resolved branch.” An older fault may later kill it.
18. “Commit-only training is always best.” Delayed learning can reduce performance and needs design evaluation.
19. “Older exception and younger redirect can both win.” Architectural priority selects one path.
20. “Branch operands are always ready.” Data hazards can delay correct resolution.
21. “Pipeline depth equals miss penalty.” Resolution, buffers and redirect/fetch latency determine it.
22. “Accuracy alone ranks predictors.” Frequency, penalty, clock, energy and workload matter.
23. “Average accuracy captures indirects.” Class-specific distributions and targets matter.
24. “Resetting predictor state is only functional.” Retention/scrubbing affects confidentiality and reproducibility.
25. “Simulation of branch tests proves recovery.” Adversarial stalls/responses/faults expose path bugs.
26. “One workload's predictor result generalizes.” Binary layout, history and configuration change outcomes.

## Worked Examples

### Example 1

Always-not-taken fetches sequentially; a taken conditional branch redirects and kills only its younger tokens.

### Example 2

A branch predicts taken with the correct direction but stale BTB target. Resolution treats the target mismatch as a misprediction.

### Example 3

A late instruction-cache response carries the old epoch after redirect. It is consumed/discarded and never becomes a valid token.

### Example 4

An older load fault and younger taken branch resolve together. The precise load trap wins; branch redirect/training and younger effects are killed.

### Example 5

A two-bit counter remains predicting taken after one not-taken outcome, then changes after the second consecutive contrary outcome.

### Example 6

Two PCs alias in a BHT entry. Functional recovery remains correct, but accuracy suffers; tags or different indexing trade storage/timing for interference.

### Example 7

A speculative call pushes the RAS. When an older branch redirects, recovery restores the checkpoint so a later real return sees the correct entry.

### Example 8

An indirect target is predicted but violates alignment at resolution. The instruction produces the ISA-specified fault, not a normal redirect/commit.

### Example 9

Moving branch comparison to decode removes one penalty cycle but adds forwarding and compare logic to the clock path; STA and workload time decide value.

### Example 10

This deterministic model compares synthetic control-hazard policies including predictor clock impact.

<!-- bijux-verify: {"id":"control-hazard-performance-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"wait_cycles=1404 effective_cpi=1.404 time_ns=1755.00 throughput_mips=569.80\nstatic_cycles=1124 effective_cpi=1.124 time_ns=1483.68 throughput_mips=674.00\ndynamic_cycles=1036 effective_cpi=1.036 time_ns=1533.28 throughput_mips=652.20\ndynamic_early_cycles=1020 effective_cpi=1.020 time_ns=1509.60 throughput_mips=662.43\n"}} -->
```python
instructions = 1000
depth = 5
branches = round(instructions * 0.20)
base_cycles = instructions + depth - 1

def report(name, cycles, period_ns):
    time_ns = cycles * period_ns
    print(
        f"{name}_cycles={cycles} effective_cpi={cycles / instructions:.3f} "
        f"time_ns={time_ns:.2f} throughput_mips={1000 * instructions / time_ns:.2f}"
    )

report("wait", base_cycles + branches * 2, 1.25)
report("static", base_cycles + round(branches * (1 - 0.70)) * 2, 1.32)
report("dynamic", base_cycles + round(branches * (1 - 0.92)) * 2, 1.48)
report("dynamic_early", base_cycles + round(branches * (1 - 0.92)), 1.48)
```

The model uses invented accuracy, fixed nonoverlapped penalties and periods. Real evaluation requires exact binaries, control-flow classes, cache effects, physical timing, energy and validated counters.

## Cross-Program Connections

- **ISA:** exact next-PC, link and exception semantics govern resolution.
- **Data Structures:** tables, tags, histories, stacks and checkpoints hold predictor state.
- **Compilers:** code layout, inlining and branch transformations change predictor demand.
- **Operating Systems:** context switching, mitigations, counters, interrupts and debug interact with speculation.
- **Security Engineering:** wrong-path microarchitectural effects require explicit threat analysis.
- **Formal Methods:** age-tagged kills, epoch freshness, progress and commit traces express recovery.
- **Performance Engineering:** frequency, class mix, accuracy, penalty, energy and useful work must be combined.
- **Systems Engineering:** configuration, update/mitigation state, evidence and errata span design through operation.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), current branch/jump, PC, alignment and architectural outcome semantics; retrieved 2026-09-04.
2. lowRISC, [Ibex Pipeline Details](https://ibex-core.readthedocs.io/en/latest/03_reference/pipeline_details.html), current branch behavior, stalls and pipeline details; retrieved 2026-09-04.
3. lowRISC, [Ibex Instruction Decode and Execute](https://ibex-core.readthedocs.io/en/latest/03_reference/instruction_decode_execute.html), current controller, branch decision and multicycle behavior; retrieved 2026-09-04.
4. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), current integrated core configuration, security and verification context; retrieved 2026-09-04.
5. Berkeley Architecture Research, [BOOM Branch Prediction](https://docs.boom-core.org/en/latest/sections/branch-prediction/index.html), current open predictor overview and recovery concepts; retrieved 2026-09-04.
6. Berkeley Architecture Research, [BOOM Backing Predictor](https://docs.boom-core.org/en/latest/sections/branch-prediction/backing-predictor.html), current history, prediction and update details; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), pipeline/control-hazard teaching resources; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), independent executable ISA next-PC and trap semantics; retrieved 2026-09-04.

## Exercises

### Exercise 1

Specify next-PC and redirect logic for sequential, conditional branch, direct jump, indirect jump and precise trap cases in an in-order pipeline.

### Exercise 2

Design metadata and recovery for a BTB plus two-bit BHT using multiple outstanding fetch requests and finite-width epochs.

### Exercise 3

Define RAS speculation and recovery for nested unresolved calls/returns, underflow, overflow, exception and context switch.

### Exercise 4

Recompute the executable policies and explain why the 92%-accurate predictor loses to the 70%-accurate policy in the synthetic run.

### Exercise 5

Write an assurance plan that separately covers architectural control-flow correctness, performance and speculative security.

## Answers to the Exercises

### Answer 1

Validated instruction length supplies sequential PC. Decode plus definitive forwarded operands supplies branch direction, direct PC-relative target or normalized indirect target; alignment/legality can instead select a synchronous trap. An older precise fault/reset/debug/accepted interrupt follows explicit priority over a younger redirect.

Attach predicted PC/type to the token. On mismatch, preserve older/resolving permitted work, kill younger tokens, update PC/epoch atomically and reject old fetch responses. Normal link writes occur only if the jump survives and commits.

### Answer 2

Each request/token carries request ID, epoch, PC, predicted target/type/source and BHT counter/history checkpoint. BTB tags/context validate target identity; BHT index/tag policy documents aliasing. Resolution compares attached prediction, repairs history, updates only at the declared safe point and redirects once.

Keep an outstanding table so every response matches a request. After redirect, old epochs are discarded. Finite epoch reuse is delayed until no outstanding token/response can carry the value, or the identity space/window proof prevents alias. Assert no stale response becomes valid and no branch trains twice.

### Answer 3

On predicted call, checkpoint stack pointer/top and push the actual sequential return address derived from instruction length. On predicted return, checkpoint then pop/peek. Tag speculative modifications by branch/path identity so redirect restores the older checkpoint and applies only surviving actual events.

Define bounded depth, underflow/overflow fallback, unusual call/return encodings, exceptions and context policy. Context switch may save/restore, flush or partition state under performance/security requirements. RAS provides only a prediction; architectural target and checks resolve independently.

### Answer 4

The wait policy uses 1,404 cycles at 1.25 ns (1,755.00 ns, 569.80 MIPS). Static uses 1,124 cycles at 1.32 ns (1,483.68 ns, 674.00 MIPS). Dynamic uses only 1,036 cycles, but its 1.48 ns period takes 1,533.28 ns (652.20 MIPS). One-cycle dynamic recovery takes 1,509.60 ns (662.43 MIPS).

Thus accuracy reduces cycles but the assumed predictor path lengthens every cycle. The result also depends on branch frequency, penalty rounding, class mix, cache/fetch behavior, energy and finite-run effects; it is not a general ranking.

### Answer 5

Architectural evidence covers exact next-PC/link/trap arithmetic, attached prediction comparison, age-correct kill, stale-response rejection, exception/interrupt/debug/reset priority, no killed effects, progress and ISA commit-trace refinement. Performance evidence covers class-specific denominators, accuracy/target misses, recovery distribution, frequency, cache interaction, energy and exact workload binaries/counters.

Security separately inventories wrong-path cache/TLB/predictor/interconnect effects, principals/context sharing, secrets/observations, mitigations and residual risk; use adversarial tests and appropriate information-flow/constant-time analysis. Bind all evidence to exact RTL/configuration, predictor state, constraints, tools, compiler/binary, workload, hardware, firmware/mitigations and errata. Internal review claims no independent certification.
