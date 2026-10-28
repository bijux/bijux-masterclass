---
module_id: ALGE-099
program: Algorithm Engineering
level: 2
module_number: 99
title: Reading and Reproducing an Algorithm Paper
status: complete
last_verified: 2026-09-05
---

# Reading and Reproducing an Algorithm Paper

## One-Page Review

### Governing question

How do we turn an algorithm paper's prose, theorems, pseudocode, experiments, and artifacts into a claim-by-claim reproduction whose agreements, deviations, and limits are independently auditable?

### Essential definitions

- A **claim inventory** lists each formal, algorithmic, empirical, and scope claim with its evidence obligation.
- A **claim-to-evidence graph** links a claim to tables or figures, analysis, raw observations, runs, code, build, environment, inputs, and protocol.
- An **artifact** is a concrete research product such as code, data, scripts, environment description, or run output.
- A **reproduction** here means obtaining a stated result using a declared relationship to the original artifacts and environment; the exact terminology must be named because communities differ.
- A **replication or generalization study** intentionally changes team, implementation, data, environment, or population to test transfer.
- A **deviation ledger** records every difference from the paper or artifact, why it occurred, when it was discovered, and its likely effect.
- A **computational result** is a value, table, figure, trace, or verdict produced by a versioned executable workflow.
- A **blocked result** cannot be honestly evaluated because a required dependency, input, authority, specification, or resource is unavailable.

### Central model, mechanism, or theorem

Treat the paper as a set of typed claims, not one truth value. For claim $c$, define expected result $E_c$, observed result $O_c$, comparison rule $R_c$, and provenance graph $G_c$. The outcome is

$$
\operatorname{outcome}(c)=R_c(E_c,O_c;G_c)\in
\{\text{reproduced},\text{not reproduced},\text{inconclusive},\text{blocked}\}.
$$

The rule must match the claim: exact equality for a checksum or discrete optimum, proof review for a theorem, tolerance plus numeric model for a floating result, and statistical compatibility plus effect comparison for noisy performance. One reproduced headline does not validate untested claims; one mismatch does not identify whether the cause is paper error, artifact drift, environment, underspecification, or reproduction defect.

### Critical invariants

- The problem definition, theorem hypotheses, algorithm variant, baselines, metrics, units, datasets, and exclusions are recovered before execution.
- Every run binds immutable source, dependencies, inputs, configuration, seed, command, environment, and outputs.
- Raw observations remain distinct from processed data, figures, and narrative.
- Expected outcomes and comparison tolerances are frozen before viewing reproduction results when possible.
- Manual interventions and all deviations are recorded; no failed run disappears.
- Artifact use, reimplementation, replication, and extension are labeled separately.
- Checksums establish byte identity, not correctness, completeness, or trustworthiness.
- Conclusions are issued per claim and never exceed the tested systems, versions, populations, and resources.

### Common failures

Reading only the abstract; implementing from pseudocode before recovering semantics; treating asymptotic equivalence as implementation identity; using a modern library while claiming the historical implementation; changing preprocessing or stopping rules silently; choosing a favorable seed; extracting data from plots when raw tables exist; rebuilding figures from already aggregated values; accepting a container as complete provenance; treating successful execution as result reproduction; using the same script as its own oracle; ignoring negative or null results; replacing unavailable inputs with convenient ones without relabeling; and reporting “the paper reproduced” when only one checksum or toy example matched.

### Compact example

A paper reports a 10% aggregate latency reduction and 2.5 ms mean paired reduction over four sessions. The archived run table contains baseline/candidate pairs 10/8, 20/17, 30/29, and 40/36 ms. A clean recomputation obtains both numbers and binds the normalized claim, protocol, and pairs to SHA-256 digest `03f2b0eb7b10ac73a7c592bbf56af5367f5b5dd2b47d47a2d9d1aabb474b61d6`. This supports those arithmetic claims for those bytes; it does not validate workload representativeness, timing validity, code correctness, or general performance.

### Connections

[ALGE-002](./002-preconditions-postconditions-and-correctness.md) supplies proof obligations, [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md) separates evidence types, [ALGE-092](./092-benchmark-design-and-reproducibility.md) governs experiments, [ALGE-096](./096-comparing-implementations-statistically.md) governs comparison, and [ALGE-098](./098-numerical-stability-in-algorithm-implementation.md) governs numeric equivalence. ALGE-100 next assembles such evidence into a defensible engineering choice.

## Governing Question

For every material claim in an algorithm paper, what exact evidence, artifact lineage, independent check, comparison rule, and scope are required to say reproduced, not reproduced, inconclusive, or blocked?

## Why This Matters

Papers compress years of design into a few pages. Definitions can be split across captions and appendices; pseudocode omits data layouts and tie rules; benchmark artifacts drift; and plots hide raw observations. A successful build shows only that some software executed. A credible reproduction reconstructs the claim, checks the evidence chain, and distinguishes what was learned from what remains unknown.

Reproduction is also an engineering method. It exposes underspecified contracts, environment dependencies, brittle scripts, inaccurate baselines, numeric instability, and hidden tuning. The goal is not ceremonial agreement or adversarial debunking. It is an auditable account of which result survived which independent procedure.

## Prerequisites and Retrieval

Retrieve correctness obligations from [ALGE-002](./002-preconditions-postconditions-and-correctness.md), theorem structure from [ALGE-004](./004-inductive-correctness-proofs.md), model costs from [ALGE-009](./009-machine-models-and-hidden-constants.md), mixed formal/empirical evidence from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), representative workloads from [ALGE-091](./091-representative-workload-construction.md), reproducible benchmarks from [ALGE-092](./092-benchmark-design-and-reproducibility.md), adversarial inputs from [ALGE-094](./094-adversarial-and-pathological-inputs.md), tuning separation from [ALGE-095](./095-parameter-tuning-without-overfitting.md), statistical comparison from [ALGE-096](./096-comparing-implementations-statistically.md), and numeric stability from [ALGE-098](./098-numerical-stability-in-algorithm-implementation.md).

## Learning Objectives

After this module, you should be able to:

1. inventory and type a paper's formal, semantic, implementation, empirical, and scope claims;
2. reconstruct problem, algorithm, theorem, experiment, and decision contracts;
3. build an immutable claim-to-evidence graph from source through reported result;
4. distinguish rerun, reproduction, reimplementation, replication, extension, and audit;
5. design independent formal, numeric, code, data, and statistical checks;
6. manage missing artifacts, ambiguity, deviations, communication, and blocked results honestly;
7. compare outcomes using prespecified exact, tolerance, proof, and statistical rules; and
8. publish a bounded reproduction report that another investigator can audit and extend.

## Core Exposition

### Start with a claim inventory

Read title, abstract, contributions, definitions, theorems, algorithms, figures, tables, captions, appendices, limitations, and artifact instructions. Rewrite each material claim in testable form. Classify it as definitional, mathematical, semantic/correctness, complexity, implementation, numerical, empirical, causal, comparative, or generality.

Record exact location and qualifiers. “Faster” might mean mean wall time on one suite after exclusions; “linear” might be an asymptotic theorem under a word-RAM model; “optimal” might mean best configuration found. A headline often combines claims with different evidence. Split them.

### Recover the problem and algorithm contract

Specify input encoding, validity, output, equivalence, tie behavior, numeric semantics, randomness, mutation, failure, and resource constraints. Map notation consistently. Trace theorem hypotheses to the implemented experiment: nonnegative weights, metric costs, connected inputs, exact arithmetic, independence, or distribution assumptions cannot disappear between sections.

Turn pseudocode into a state-transition description. Identify abstract operations, pre/postconditions, loop invariants, termination measure, data-structure requirements, and nondeterministic choices. List decisions left to implementation: layout, queue discipline, precision, stopping, parallel ordering, libraries, preprocessing, and error handling.

### Build the evidence graph

For every figure cell or table row, trace backward:

1. narrative claim and comparison rule;
2. plotted or tabulated statistic;
3. analysis script and parameters;
4. cleaned or transformed data;
5. raw observations and run identities;
6. exact executable, configuration, and command;
7. source revision, build, compiler, dependencies, and flags;
8. input bytes, generator, seed, license, and provenance;
9. hardware, operating system, runtime, locale, clock, and resource controls.

Store content digests and durable identifiers. A digest detects byte changes but does not show that the file is complete, safe, or the one used by the paper. Provenance must also explain meaning and transformation.

### Choose the reproduction relationship

A rerun uses provided artifacts in a closely matched environment. A clean reimplementation derives code from the specification and can test whether the prose is sufficient. A replication changes team, artifacts, environment, or data. An extension asks a new question. An audit may inspect claims without rerunning costly experiments.

Name the terminology used by the venue. ACM's current artifact policy distinguishes artifact availability/evaluation from results reproduced or replicated and states its team/artifact relationships [1]. Because scientific communities have historically swapped “reproduce” and “replicate,” define operations, not just labels.

### Freeze a protocol before results

Declare targeted claim IDs, stopping rule, resource budget, environment matching, input inclusion, baseline construction, seeds, repetitions, failure handling, tolerance, statistical method, and success categories. Prioritize central and feasible claims; do not imply completeness.

Record a timestamped protocol digest. Exploratory debugging is expected, but it belongs in a separate lane. If evidence changes the protocol, version it, explain why, and use fresh evidence for confirmatory conclusions. Do not tune the reproduction until the headline matches.

### Acquire artifacts safely

Inventory paper, supplement, repository, archive, data, images, containers, build files, dependency locks, checksums, and licenses. Preserve originals read-only and work on derived copies. Scan untrusted artifacts, inspect scripts before execution, remove external credentials, deny unintended network and writes, constrain CPU/memory/time, and use an isolated environment.

Never execute a paper's code merely because it is peer reviewed or archived. Containers preserve some user-space bytes but not host kernel, microarchitecture, accelerators, firmware, external services, nondeterminism, expired registries, or licenses. Record every fetched immutable reference and acquisition date.

### Reconstruct the environment

Follow the documented build first. Record exact compiler/interpreter, dependencies including transitive versions, flags, environment variables, locale, time zone, hardware topology, memory, storage, accelerators, kernel, and relevant mitigations. Capture commands and logs automatically.

When exact recovery is impossible, classify the mismatch: unavailable historical hardware, withdrawn data, proprietary solver, broken registry, missing seed, or ambiguous version. Choose a principled substitute only if it preserves the claim; otherwise narrow the claim or mark it blocked. “Modern equivalent” is a new experiment unless equivalence is established.

### Validate before measuring

Run known examples, unit/property tests, independent checkers, small exhaustive instances, and adversarial cases. Confirm input counts, checksums, schemas, exclusions, and transformations. Recompute derived datasets from raw inputs where possible. A benchmark of wrong output reproduces no performance claim.

For theorem-linked code, inspect whether the implementation realizes the proved variant. Verify invariants and certificates. For numeric code, use higher precision or certified bounds and record tolerances. For randomized code, validate seed propagation and preserve every run.

### Execute a claim-bound recomputation

The reference normalizes a small artifact, computes its digest, and independently recomputes the two declared effects. Canonical serialization is part of the digest protocol.

<!-- bijux-verify: {"id":"claim-bound-recomputation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"artifact_sha256: 03f2b0eb7b10ac73a7c592bbf56af5367f5b5dd2b47d47a2d9d1aabb474b61d6\nmean_paired_reduction_ms: 2.5\naggregate_reduction_percent: 10.0\nclaim_check: passed\n","stderr":""}} -->
```python
import hashlib


artifact = {
    "claim": "candidate_mean_lower",
    "pairs": [
        ["g1", 10, 8],
        ["g2", 20, 17],
        ["g3", 30, 29],
        ["g4", 40, 36],
    ],
    "protocol": {"metric": "wall_ms", "pairing": "session", "version": 1},
}
payload = b'{"claim":"candidate_mean_lower","pairs":[["g1",10,8],["g2",20,17],["g3",30,29],["g4",40,36]],"protocol":{"metric":"wall_ms","pairing":"session","version":1}}'
digest = hashlib.sha256(payload).hexdigest()
paired = sum(baseline - candidate for _, baseline, candidate in artifact["pairs"]) / len(artifact["pairs"])
baseline_total = sum(baseline for _, baseline, _ in artifact["pairs"])
candidate_total = sum(candidate for _, _, candidate in artifact["pairs"])
aggregate = 100 * (baseline_total - candidate_total) / baseline_total
print("artifact_sha256:", digest)
print("mean_paired_reduction_ms:", paired)
print("aggregate_reduction_percent:", aggregate)
print("claim_check:", "passed" if paired == 2.5 and aggregate == 10.0 else "failed")
```

The check binds exact bytes to arithmetic. It does not establish that these are the paper's original raw observations unless acquisition provenance does, nor that the protocol measured valid latency. Each upstream edge needs separate evidence.

### Reproduce formal and complexity claims

Restate each theorem with quantifiers and hypotheses. Check definitions, premise use, base cases, inductive steps, inequalities, probability space, and termination. Search for counterexamples at boundaries. Mechanization or exhaustive finite search can support review but does not replace reasoning beyond the checked domain.

Map complexity terms to counted operations and data structures. A proof of $O(m\log n)$ does not imply faster wall time, and an implementation using a different queue may have another bound. If constants, cache behavior, or numeric precision matter, state which are theorem, model, and measurement.

### Reproduce empirical claims

Execute the frozen workflow and preserve all outcomes. Recompute tables and figures from raw rows, not screenshots. Check units, denominators, weights, pairing, aggregation, confidence intervals, multiple comparisons, and exclusions. Compare effect sizes and uncertainty, not only threshold decisions.

Exact equality may be appropriate for deterministic hashes or small integer outputs. Performance needs an equivalence or compatibility rule that reflects noisy units and practical thresholds. A different point estimate can still support a bounded claim; an identical mean can hide different failures or tails.

### Triangulate independently

Use at least one independent path where material: clean implementation, alternative theorem derivation, exact small-instance enumeration, separate output checker, higher-precision calculation, independent parser, second measurement tool, or new held-out input family. Independence reduces common-mode error.

Do not force independence cosmetically. Two wrappers around the same library are one computational core. Document shared components. When independent checks disagree, preserve both and investigate semantics, input, numeric behavior, nondeterminism, or bugs before assigning fault.

### Maintain the deviation ledger

Record intended and accidental changes: newer compiler, replacement hardware, unavailable input, patched build, corrected script, changed timeout, additional warm-up, reconstructed baseline, or clarified formula. Include discovery time, rationale, evidence, affected claims, and whether the deviation was made before or after seeing outcomes.

Run sensitivity around plausible interpretations rather than silently selecting one. Ask authors focused factual questions with a minimal reproducer when appropriate, but retain independent judgment and report nonresponse neutrally. A private clarification that changes the method belongs in the public provenance.

### Classify outcomes claim by claim

Use four outcomes. **Reproduced** means the prespecified rule passed with adequate provenance. **Not reproduced** means an executable adequate test contradicted the expected result under the declared protocol. **Inconclusive** means evidence ran but uncertainty or ambiguity prevents classification. **Blocked** means a prerequisite was unavailable.

Then assess likely causes separately. Do not label a paper wrong from an environment mismatch, or a reproduction wrong merely because it disagrees. State the smallest result: “Table 3 latency ratio for dataset X was not reproduced under environment Y,” followed by evidence and alternatives.

### Package the report for another investigator

Include claim matrix, scope, terminology, artifact inventory and licenses, protocol digest, environment, commands, raw and derived data, logs, analysis, independent checks, deviations, outcomes, limitations, and costs. Connect every narrative number to a machine-readable result. Preserve negative and failed runs.

Availability is not functionality, functionality is not reusability, and any artifact badge or venue review covers its own criteria and time. Do not claim external review without named evidence. Archive immutable, legally shareable materials; where data cannot be shared, publish schema, generator or access procedure, digests, and the exact limitation.

## Definitions and Notation

Let $C=\{c_1,\ldots,c_k\}$ be targeted claims. Each claim has type $\tau(c)$, expected result $E_c$, observed result $O_c$, comparison rule $R_c$, and evidence graph $G_c=(V_c,E_c^{\mathrm{edge}})$. The superscript distinguishes graph edges from the expected result.

A **protocol digest** binds a canonical protocol serialization. An **environment lock** identifies recoverable software inputs but does not freeze hardware or external services. **Provenance** records origin and transformation; **lineage** orders derived artifacts. **Sensitivity analysis** varies justified ambiguous choices. **Counterfactual independence** asks whether a check could fail when the original pipeline shares a defect.

## Mechanisms, Invariants, or Proof Structure

### Claim decomposition

If headline $H$ is a conjunction $c_1\land\cdots\land c_k$, reproducing one $c_i$ does not prove $H$. Conversely, failure of a nonessential claim does not logically refute every other claim. The inventory makes this structure explicit.

### Digest invariant

For collision-resistant hash $h$, matching $h(B)=h(B')$ is evidence that compared byte sequences match under the operational protocol. It is not evidence about semantics, provenance, completeness, safety, or correctness. Canonicalization must itself be versioned or logically identical data can hash differently.

### Evidence-graph invariant

Every reported result has an unbroken path to raw observations, run identity, executable/build, configuration, environment, and input. Every transformation is executable or fully specified. Missing edges produce a scoped limitation or blocker rather than invented provenance.

### Comparison invariant

The comparison rule is chosen from claim type and frozen protocol: proof audit for theorems, exact checking for discrete deterministic results, conditioned tolerances for numeric results, and design-compatible effect/uncertainty comparison for experiments. Passing one rule cannot be substituted for another.

## Alternatives and Trade-Offs

| Approach | Strength | Limitation | Appropriate use |
|---|---|---|---|
| original artifact rerun | closest operational path | common-mode code/data defects | recover reported pipeline |
| clean reimplementation | tests specification sufficiency | interpretation and engineering divergence | semantic/algorithmic claims |
| container or VM | captures much user space | host/hardware/service drift | environment approximation |
| proof audit | checks formal argument | does not measure implementation | theorem and complexity claims |
| exact small-instance oracle | strong finite correctness evidence | limited scale/domain | algorithm semantics |
| benchmark reproduction | checks measured effects | costly and environment-sensitive | empirical performance |
| new data/hardware replication | probes generality | answers broader question | transfer and robustness |

The best design is usually a portfolio: first rerun to recover the pipeline, then independently recompute or reimplement the most consequential claims. Resource limits justify a smaller explicit scope, not vague claims of reproducing an entire paper.

## Failure Modes and Misconceptions

- **“The code ran, so the result reproduced.”** Execution must yield the targeted result under its comparison rule.
- **“A matching plot is enough.”** Plot appearance can hide data, units, exclusions, and uncertainty.
- **“The container is the environment.”** Host, hardware, services, registries, and nondeterminism remain.
- **“Checksums prove validity.”** They prove operational byte identity, not truth or provenance.
- **“Peer review already checked artifacts.”** Review scope varies and never transfers automatically to a new claim.
- **“Modern replacements are equivalent.”** Equivalence is a claim requiring evidence.
- **“One mismatch refutes the paper.”** Classify the exact claim and plausible causes.
- **“Author instructions override observed evidence.”** Clarifications are evidence and deviations, not authority to hide conflict.
- **“Only successful runs matter.”** Failures, retries, exclusions, and search history affect the result.
- **“Reproduction is all-or-nothing.”** Honest per-claim outcomes are more informative.

## Worked Examples

### Example 1

**Situation.** A paper claims $O(n\log n)$ time and a 2x measured speedup.

**Reasoning.** Split the theorem from the experiment. Audit the operation-count proof and data-structure assumptions separately from inputs, implementation, baseline, hardware, metric, repetitions, and statistics. Either claim can pass while the other fails.

**Conclusion.** Different claim types require different evidence paths.

### Example 2

**Situation.** Pseudocode says “extract minimum” but never specifies decrease-key behavior or ties.

**Reasoning.** Recover the mathematical requirement, inspect proof premises, and list admissible queue semantics. Implementations using lazy duplicates and true decrease-key may both be correct but have different memory and constant behavior. Freeze which variant is reproduced.

**Conclusion.** Pseudocode must be converted into a precise algorithm and implementation contract.

### Example 3

**Situation.** The artifact builds only after upgrading a dependency and changing two APIs.

**Reasoning.** Preserve the original failure log, patch in a derived branch, record exact edits and dependency versions, and classify the run as a ported-artifact reproduction. Test whether the patch changes results on known cases. Do not overwrite the archived source.

**Conclusion.** A transparent port can yield evidence without pretending byte-identical execution.

### Example 4

**Situation.** A figure matches visually, but the regenerated CSV omits every timeout.

**Reasoning.** The figure is derived evidence. Trace exclusions to raw run identities and the paper's failure policy. Restore timeouts as censored or declared penalty outcomes and recompute. The visual match may expose the same biased filter rather than valid reproduction.

**Conclusion.** Provenance and failure semantics outrank graphical resemblance.

### Example 5

**Situation.** A checksum matches an archived dataset.

**Reasoning.** Byte identity supports acquisition integrity. It does not show the dataset represents the claimed population, was legally collected, has correct labels, or was the exact input after preprocessing. Trace generation and transformation separately.

**Conclusion.** Hashes secure one evidence edge, not the whole claim.

### Example 6

**Situation.** New hardware produces a 1.7x rather than 2x speedup, with both confidence intervals excluding one.

**Reasoning.** Check baseline/compiler fairness, bottleneck profiles, feature changes, and practical threshold. The historical claim may reproduce only on the original platform; the new result can be a valid generalization failure rather than an arithmetic contradiction.

**Conclusion.** Environment changes can reveal bounded scope instead of a single guilty implementation.

### Example 7

**Situation.** A clean reimplementation matches outputs on examples but is 30% slower.

**Reasoning.** Correctness evidence and performance evidence separate. Compare data layout, allocator, vectorization, preprocessing, stopping, precision, and compiler. If the prose omits a decisive optimization, record underspecification; do not copy artifact internals and retain the “clean” label.

**Conclusion.** Reimplementation tests specification sufficiency as well as algorithm semantics.

### Example 8

**Situation.** A stochastic result matches only after trying 50 seeds and reporting the nearest.

**Reasoning.** This outcome-based seed selection invalidates confirmation. Use prespecified or sampled seeds, preserve all runs, reproduce aggregation and uncertainty, and account for original seed policy. The selected match becomes exploratory evidence only.

**Conclusion.** Search for agreement creates the same selection bias as search for significance.

### Example 9

**Situation.** The original proprietary dataset and solver license are unavailable.

**Reasoning.** Mark affected claims blocked. Reproduce open toy correctness claims and run a separately labeled extension on a public substitute if useful. State why the substitute does not test the original population or solver comparison.

**Conclusion.** Partial progress and an exact blocker are more credible than silent substitution.

### Example 10

**Situation.** An independent checker rejects 2 of 1,000 outputs that the paper's bundled checker accepts.

**Reasoning.** Preserve instances and both checker traces. Inspect shared parsing, tolerance, feasibility, and objective semantics; use an exact small oracle if possible. Recompute performance only over outcomes classified under the resolved contract and report remaining ambiguity.

**Conclusion.** Independent disagreement is diagnostic evidence, not a vote.

## Cross-Program Connections

- [Testing and Quality Engineering STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) develops independent and partial oracle portfolios.
- [Data Structures Engineering DSE-010](../../17-data-structures-engineering/modules/010-benchmarking-a-structure-without-misleading-results.md) connects representation benchmarks to claim scope.
- [Data Engineering DE-089](../../19-data-engineering/modules/089-auditability-and-provenance.md) supplies lineage and immutable evidence design.
- [Concurrent and Parallel Programming CONPAR-092](../../04-programming-languages-concurrent-and-parallel-programming/modules/092-roofline-and-operational-intensity-analysis.md) illustrates hardware-sensitive performance models.
- [Systems Engineering SYSENG-043](../../26-systems-engineering/modules/043-cost-schedule-performance-and-risk.md) makes reproduction cost, uncertainty, and residual risk explicit.
- [Platform Engineering PLAT-021](../../29-platform-engineering/modules/021-container-images-as-platform-artifacts.md) governs container identity, provenance, and environment limits.

## References

1. Association for Computing Machinery, “Artifact Review and Badging Version 1.1,” 2020. [Current official policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current). Terminology, artifact criteria, and result-validation relationships checked 2026-09-05.
2. Catherine C. McGeoch, *A Guide to Experimental Algorithmics*, Cambridge University Press, 2012. [doi:10.1017/CBO9780511843747](https://doi.org/10.1017/CBO9780511843747). Authoritative algorithm-experiment methodology; publisher record checked 2026-09-05.
3. Geir Kjetil Sandve, Anton Nekrutenko, James Taylor, and Eivind Hovig, “Ten Simple Rules for Reproducible Computational Research,” *PLOS Computational Biology* 9(10), 2013, e1003285. [doi:10.1371/journal.pcbi.1003285](https://doi.org/10.1371/journal.pcbi.1003285). Workflow and provenance guidance; journal record checked 2026-09-05.
4. Roger D. Peng, “Reproducible Research in Computational Science,” *Science* 334(6060), 2011, 1226–1227. [doi:10.1126/science.1213847](https://doi.org/10.1126/science.1213847). Perspective on computational reproducibility and evidence; publisher record checked 2026-09-05.
5. David L. Donoho, Arian Maleki, Inam Ur Rahman, Morteza Shahram, and Victoria Stodden, “Reproducible Research in Computational Harmonic Analysis,” *Computing in Science & Engineering* 11(1), 2009, 8–18. [doi:10.1109/MCSE.2009.15](https://doi.org/10.1109/MCSE.2009.15). Case-based reproducible computational research framework; publisher record checked 2026-09-05.
6. Victoria Stodden, Friedrich Leisch, and Roger D. Peng, eds., *Implementing Reproducible Research*, CRC Press, 2014. [Publisher record](https://www.routledge.com/Implementing-Reproducible-Research/Stodden-Leisch-Peng/p/book/9781466561595). Practices and case studies; record checked 2026-09-05.
7. Tomas Kalibera and Richard Jones, “Rigorous Benchmarking in Reasonable Time,” *ISMM 2013*, 63–74. [doi:10.1145/2464157.2464160](https://doi.org/10.1145/2464157.2464160). Primary experimental-design and uncertainty method for performance systems; ACM record checked 2026-09-05.
8. Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002. [doi:10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027). Reference for reproducing numeric claims under finite arithmetic; publisher record checked 2026-09-05.

## Exercises

### Exercise 1

Define claim inventory, evidence graph, artifact, reproduction, replication/generalization, deviation ledger, computational result, and blocked result for an algorithm-paper review.

### Exercise 2

A paper reports candidate/baseline ratios 0.8, 0.9, and 1.1 and says “20% faster on average.” Compute the arithmetic mean ratio, mean per-instance reduction, and geometric mean ratio. Explain what must be recovered before judging the prose.

### Exercise 3

An artifact builds in a container, downloads an unversioned dataset, chooses the fastest of ten seeds, drops timeouts, and regenerates a matching plot. Classify the evidence and specify the repairs.

### Exercise 4

Compare an original-artifact rerun, clean reimplementation, proof audit, and new-hardware replication for a paper claiming correctness, $O(n\log n)$ work, and lower latency.

### Exercise 5

Design a reproduction of a parallel graph-algorithm paper whose artifact requires old hardware and proprietary inputs. Include claim scope, acquisition, safety, environment, substitutes, correctness, numeric checks, benchmark design, statistics, deviations, outcomes, and report.

## Answers to the Exercises

### Answer 1

A claim inventory lists each formal, semantic, implementation, empirical, and scope assertion with its evidence obligation. An evidence graph connects a claim through reported result, analysis, raw observations, runs, executable/build, configuration, environment, and inputs. An artifact is a concrete code, data, script, environment, or output product. Reproduction obtains a stated result under a declared relationship to original artifacts/environment; replication or generalization deliberately changes team, implementation, data, or environment to test transfer. A deviation ledger records every difference and its likely effect. A computational result is a versioned workflow's output. A blocked result lacks a prerequisite needed for an honest test. The report must also state the venue terminology used.

### Answer 2

The arithmetic mean ratio is $(0.8+0.9+1.1)/3=0.9333$, corresponding to 6.67% reduction if this ratio mean is the estimand. Per-instance reductions are 20%, 10%, and -10%, also averaging 6.67% because each is $1-r_i$. The geometric mean ratio is $(0.8\cdot0.9\cdot1.1)^{1/3}\approx0.925$, or about 7.5% multiplicative-center reduction. None supports “20% faster on average.” Recover ratio direction, raw times, weights, aggregation, failures, pairing, uncertainty, and whether “20%” meant one dataset, aggregate totals, median, or a selected result.

### Answer 3

The container supports exercisability but not dataset identity or result validity. The download is mutable provenance; archive exact bytes, license, source, checksum, schema, and acquisition date. Fastest-of-ten selection changes the stochastic procedure and biases the reported run; freeze a seed rule and retain all seeds. Dropping timeouts selects survivors; restore them as censored or declared penalty/failure outcomes. A matching plot may reproduce the same flawed transformations. Inspect code safely, bind all versions and commands, validate outputs independently, recompute from raw rows, freeze comparison rules, and report the original rerun plus repaired analysis as separate protocols.

### Answer 4

The artifact rerun most directly tests whether the provided workflow yields its outputs but shares its code and data defects. A clean reimplementation tests whether prose and pseudocode specify a correct algorithm, but implementation differences limit direct latency comparison. A proof audit checks hypotheses, correctness, and the $O(n\log n)$ derivation, not machine performance. A new-hardware replication tests latency transfer and mechanism but is not an exact historical rerun. Use all four selectively: proof audit and small independent oracle for formal claims; rerun for pipeline recovery; clean implementation for semantic independence; and controlled new-hardware study for generality, each with its own outcome.

### Answer 5

Inventory theorem, correctness, work/span, and latency claims separately. Archive the paper and legally available artifacts read-only; inspect code before isolated execution. Record old hardware and proprietary data as blockers with exact required properties. Reconstruct the software stack and emulate hardware only where equivalence is evidence-backed. Rerun public toy cases, audit proofs/hypotheses, implement an independent checker, enumerate small graphs, and use higher precision for numeric predicates. Run a separately labeled replication on public representative and adversarial graph families and current hardware, matching algorithm variants, baselines, total resources, affinity, warm-up, repetitions, failures, and timing hierarchy. Prespecify effects and uncertainty. Maintain a deviation ledger for ports, substitutes, and environment gaps. Classify original-input/hardware performance blocked, public correctness or theorem claims per evidence, and new-hardware results as replication/generalization. Publish claim matrix, digests, provenance, commands, raw rows, analysis, failures, statistics, costs, and limitations without claiming the whole paper reproduced.
