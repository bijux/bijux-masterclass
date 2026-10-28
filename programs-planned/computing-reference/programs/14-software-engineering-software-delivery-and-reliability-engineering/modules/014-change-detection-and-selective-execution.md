---
module_id: SDRE-014
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 14
title: Change Detection and Selective Execution
status: complete
last_verified: 2026-09-06
---

# Change Detection and Selective Execution

## One-Page Review

### Governing question

How can a CI system skip work safely by proving which outputs and checks may be affected by an exact change, while failing conservatively when its model is incomplete?

### Essential definitions

- a **comparison base** is the exact prior revision against which a candidate is compared;
- a **change set** is the typed addition, modification, deletion, rename, or mode change between two source trees;
- a **target** is an addressable build, test, analysis, packaging, or deployment unit;
- a **dependency graph** records which targets consume other targets or source inputs;
- a **reverse dependency** is a consumer reachable from a changed producer;
- the **affected set** is the conservative closure of changed inputs through relevant dependency and policy relations;
- **selective execution** runs only work justified by the affected set and mandatory baselines;
- a **false negative** skips required work; a **false positive** runs unnecessary work;
- an **undeclared dependency** influences a target without appearing in the selection model;
- a **dynamic dependency** is discovered only during execution;
- a **global invalidator** is a change whose safe affected set is broad, such as toolchain, root policy, or dependency-resolution configuration;
- a **full-run fallback** deliberately selects the complete applicable scope when sound narrowing is unavailable.

### Central model, mechanism, or theorem

Let $G=(V,E)$ have an edge $u\rightarrow v$ when target $v$ depends on $u$. For changed input set $C$, the graph-affected set is

$$
A_G(C)=C\cup\{v\in V\mid\exists c\in C:\ c\leadsto v\}.
$$

Selected work is $S(C)=Checks(A_G(C))\cup B(C)$, where $B$ contains mandatory risk baselines. This selection is sound only relative to a complete, current graph and correct change classification. If those assumptions fail, widen selection or run the full scope.

### Critical invariants

- compare exact source trees using the intended merge base;
- classify additions, deletions, renames, modes, submodules, generated inputs, and configuration changes;
- map every source and external input to owned targets;
- traverse reverse dependencies, not only the changed directory;
- include toolchains, lockfiles, generators, policies, and environment definitions as inputs;
- preserve test-to-target and non-code risk mappings;
- treat unknown files, parse failures, graph-version mismatches, and dynamic uncertainty conservatively;
- bind the selection decision to candidate, base, graph, policy, and selector version;
- run periodic and randomized full scopes to estimate missed-impact risk;
- never reuse passing evidence from a different subject;
- measure false negatives through later failures and shadow runs;
- optimize after preserving the required confidence boundary.

### Common failures

Common failures include diffing against the wrong base, path-prefix selection, ignoring deletions and renames, omitting generated code, treating lockfiles as ordinary leaf files, trusting stale dependency graphs, missing runtime reflection or plugin discovery, excluding documentation that drives builds, skipping security and license baselines, accepting “no changes” after parser failure, and measuring only time saved.

### Compact example

`parser/schema.json` changes. The graph maps it to generator `ast-gen`, generated library `ast`, compiler `compiler`, CLI `tool`, and tests for all four. Reverse closure selects those targets. A repository-wide license scan remains a mandatory baseline. If the generator graph was produced for a different commit, the selector rejects the graph and runs the full applicable suite instead of claiming the CLI is unaffected.

### Connections

[SDRE-013](013-branching-strategies-and-integration-delay.md) fixes the comparison and admission context. [SDRE-015](../ROADMAP.md) next schedules selected work in parallel, and [SDRE-016](../ROADMAP.md) coordinates multiple changing candidates.

## Governing Question

Large repositories cannot always rebuild and retest everything within a useful feedback interval. Yet skipping work can convert fast feedback into false assurance. The engineering problem is therefore not “how do we run fewer jobs?” It is “under which explicit model does this change leave a job's inputs and relevant risks unchanged?”

Safe selection combines exact version-control comparison, declared dependency structure, test and policy mappings, conservative handling of uncertainty, and empirical calibration. A path list is evidence about changed source trees. It is not by itself evidence about downstream effect.

## Why This Matters

Git's current `diff` documentation distinguishes comparisons between trees, index, worktree, commits, merge bases, and merge results [1]. Choosing the wrong pair changes the detected set. In a pull request, comparing only the previous branch commit can miss earlier branch changes; comparing the common ancestor to the candidate identifies the accumulated proposal.

Mokhov, Mitchell, and Peyton Jones separate a build system's dependency model, scheduler, and rebuilder and analyze how systems decide what needs rebuilding [2]. Bazel's official query guidance exposes reverse dependencies precisely because changing a producer can affect consumers outside its directory [3]. These sources support the durable model: detect exact changed inputs, propagate impact through declared relations, then schedule the required closure.

Selective execution controls cost and feedback latency, but its primary risk is asymmetric. A false positive wastes compute. A false negative can admit an untested regression, unsafe artifact, or incomplete evidence set. Policy should reflect that asymmetry.

## Prerequisites and Retrieval

Retrieve source tree, commit, merge base, diff, path, rename, deletion, file mode, submodule, content digest, target, action, dependency, directed graph, reachability, transitive closure, build rule, test mapping, generated source, toolchain, lockfile, cache key, false positive, false negative, precision, recall, shadow evaluation, and risk baseline.

From SDRE-003 and SDRE-004 retrieve hermetic inputs, reproducibility limits, incremental builds, invalidation, and cache correctness. From SDRE-011 through SDRE-013 retrieve exact admitted revisions, mainline health, merge queues, and integration delay. Algorithm Engineering owns graph algorithms; this chapter applies them to CI evidence and risk.

## Learning Objectives

After completing this module, you should be able to:

1. choose and record the correct comparison base;
2. distinguish source-tree changes from affected build and test targets;
3. compute reverse-dependency closure on a directed graph;
4. incorporate generated, configuration, toolchain, and external inputs;
5. design conservative test and policy mappings;
6. explain false-positive and false-negative trade-offs;
7. detect cases that require full-scope fallback;
8. bind selection evidence to exact versions;
9. calibrate selection through shadow, random, and periodic full runs;
10. diagnose unsafe path-based optimization.

## Core Exposition

**Fix the comparison semantics.** A change detector needs two exact trees and a reason for comparing them. For a mainline commit, compare its parent tree to its tree. For a proposed branch, compare the intended merge base with the candidate or construct the exact merge result. For a re-run after mainline moves, recompute both candidate and selection.

Record commit digests, merge-base digest, diff algorithm and options, selector version, and output digest. A label such as `main` is insufficient because it can move. An empty diff is meaningful only if both trees resolved and parsing completed successfully.

**Preserve change types.** Addition, modification, deletion, rename, copy, executable-bit change, symlink change, submodule pointer change, and type change can have different implications. Deleting a test or policy is not “less impact” than adding one. Rename detection is heuristic in many tools; correctness should not depend on a rename being recognized rather than represented as delete-plus-add.

Content equality may allow a move to reuse some work, but location can influence package ownership, visibility, imports, deployment, licensing, and policy. Keep old and new paths and let domain rules decide.

**Map source inputs to targets.** Build systems operate on targets or actions, not arbitrary directory intuition. A target declares source files, generated inputs, dependencies, tools, environment properties, and outputs. The selector first maps each changed item to one or more target nodes. Unknown ownership is a model failure, not proof of no effect.

Files outside ordinary source deserve first-class mapping: lockfiles change resolved dependencies; compiler flags change outputs; container bases change environments; schema files drive generators; CI definitions change evidence; root allowlists alter policy; documentation may generate a site or package metadata.

**Traverse impact in the correct direction.** If application `app` depends on library `lib`, the graph edge can be represented `lib → app` for impact propagation. Changing `lib` selects `lib` and reachable consumers. Traversing ordinary dependency edges from `lib` toward its suppliers answers a different question.

Compute a worklist closure with a visited set. Cycles may appear in coarse module graphs even when build actions are acyclic; the visited set guarantees termination. Preserve why each node was selected so a developer can trace `changed file → owning target → reverse edge → test`.

**Treat tests as dependencies and risk controls.** Some tests map structurally to code targets. Others cover cross-cutting behavior: compatibility, migration, security, performance, packaging, or end-to-end journeys. Maintain explicit test-to-subject and risk-to-change mappings. Directory co-location is a convenience, not a complete model.

Mandatory baselines cover risks poorly represented in the graph. Examples include repository policy validation, secret scanning, license checks, manifest synchronization, and a small smoke suite. Baselines depend on threat and cost; “always run” must still have a stated claim.

**Handle dynamic and undeclared dependencies.** Reflection, runtime plugin discovery, shell globbing, environment reads, network access, implicit compiler search paths, mutable registries, and generated manifests can escape a static graph. Capture dynamic dependencies during execution where possible, then version and validate them. A previous run's dynamic graph can itself be stale if the change alters discovery.

Hermetic builds reduce the problem by rejecting undeclared inputs. Where hermeticity is unavailable, define global invalidators and broader scopes. Never describe an incomplete graph as sound without qualifying the model boundary.

**Invalidate on control inputs.** Selector logic, graph extractor, target definitions, policy, toolchain, lockfile, root configuration, and environment image influence either the computation or the decision. Their change may select a broad set or force a full run. The selection engine cannot safely use yesterday's graph against today's changed graph schema without a compatibility rule.

Generated code creates two edges: generator inputs affect generated outputs; generator executable and configuration also affect them. Check in generated output only if policy defines how source and generated forms remain synchronized. Selecting solely from the generated diff can hide the causal input.

**Choose conservative fallbacks.** Run full applicable scope when the merge base is missing, history is shallow or rewritten unexpectedly, diff parsing fails, a file has no owner, graph construction fails, graph and candidate versions differ, global configuration changes, selector policy is unknown, or dynamic-dependency confidence is inadequate.

A fallback is successful safety behavior, not selector failure. Make its reason visible so teams can improve coverage instead of adding a silent bypass. Bound denial-of-service risk by controlling who can create global invalidations and by provisioning full-run capacity.

**Bind and audit the decision.** A selection record contains candidate and base digests, normalized change set, graph digest, policy and selector versions, selected and skipped targets, derivation paths, baselines, fallback reason, and execution outcomes. Skipped means “not selected under model M,” never “proven irrelevant universally.”

If evidence from a previous build is reused, verify that its complete input key matches the current action. A passing test on artifact `a1` cannot satisfy a gate for `a2` merely because the selector skipped it.

**Calibrate empirically.** Run the full suite in shadow for sampled changes and compare outcomes. Schedule periodic full builds, randomize additional test selection, and examine production or later-stage regressions for selector misses. Seed known dependency mutations to test selection recall. Track model-coverage gaps and fallback frequency.

Observed zero misses does not prove soundness when failures are rare or the sample is small. Report sample count, change distribution, test types, and detection opportunity. Expand full-run sampling after graph or selector changes.

**Measure both safety and value.** Track selected fraction, queue and feedback savings, fallback rate, unknown ownership, graph age, selection-computation latency, shadow disagreements, downstream failures attributable to skips, and time to explain a decision. Segment by change type and target.

Precision is the fraction of selected checks that were necessary under an evaluation oracle; recall is the fraction of truly affected checks selected. In practice, “truly affected” is difficult to observe. A full test passing does not prove a test was unnecessary, and a test failure may be flaky. Use multiple evidence sources and conservative language.

## Definitions and Notation

Let $G=(V,E)$ be a directed impact graph with $(u,v)\in E$ meaning a change to $u$ may affect $v$. For changed nodes $C\subseteq V$, define

$$
A_G(C)=\{v\in V\mid v\in C\lor\exists c\in C:c\leadsto v\}.
$$

Let $Q(v)$ map affected nodes to checks and $B(C)$ return mandatory baselines. Then

$$
S(C)=\bigcup_{v\in A_G(C)}Q(v)\cup B(C).
$$

Given an evaluation set of truly required checks $R$, selection recall and precision are

$$
Recall=\frac{|S\cap R|}{|R|},\qquad Precision=\frac{|S\cap R|}{|S|},
$$

when denominators are nonzero. Safety normally prioritizes recall; the oracle $R$ is itself evidence-limited.

## Mechanisms, Invariants, or Proof Structure

**Closure argument.** Initialize a worklist with $C$. Repeatedly select a node, add each unseen outgoing neighbor, and stop when the worklist is empty. Every reachable node is eventually added by induction on path length; a visited set prevents repeated processing. This proves reachability for the supplied graph, not completeness of the graph.

**Monotonicity.** For fixed $G$, $Q$, and $B$ with monotone baseline policy, if $C_1\subseteq C_2$, then $S(C_1)\subseteq S(C_2)$. An implementation violating this deserves investigation. Changing the graph or policy can invalidate the comparison.

**Counterexample to paths.** `shared/schema.proto` generates clients in three distant directories. A selector running only tests beneath `shared/` omits all consumers even though the path diff is correct. Reverse dependency closure includes them if generator edges are declared.

**Executable closure model.** This model performs graph closure and conservative fallback. It does not inspect Git or prove its graph complete.

<!-- bijux-verify: {"id":"select-affected-checks","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"library_change=['app', 'app-test', 'lib', 'lib-test', 'smoke']\nschema_change=['app', 'app-test', 'generator', 'lib', 'lib-test', 'schema', 'smoke']\nunknown_file=['full-scope']\nstale_graph=['full-scope']\ndeletion=['app', 'app-test', 'lib', 'lib-test', 'smoke']\n","stderr":""}} -->
```python
edges = {
    "lib": {"app", "lib-test"},
    "app": {"app-test"},
    "schema": {"generator"},
    "generator": {"lib"},
}
owned = {"lib", "app", "schema", "generator", "lib-test", "app-test"}

def select(changed, graph_current=True):
    if not graph_current or not changed <= owned:
        return ["full-scope"]
    seen = set(changed)
    work = list(changed)
    while work:
        node = work.pop()
        for consumer in edges.get(node, set()):
            if consumer not in seen:
                seen.add(consumer)
                work.append(consumer)
    return sorted(seen | {"smoke"})

print(f"library_change={select({'lib'})}")
print(f"schema_change={select({'schema'})}")
print(f"unknown_file={select({'mystery.cfg'})}")
print(f"stale_graph={select({'lib'}, graph_current=False)}")
print(f"deletion={select({'lib'})}")
```

## Alternatives and Trade-Offs

**Full execution versus selection.** Full runs minimize model-dependent skipping but cost time and capacity. Selection accelerates feedback while adding graph, policy, and audit complexity. Retain periodic full evidence.

**Static versus dynamic dependencies.** Static graphs are explainable before execution but miss runtime discovery. Dynamic capture observes actual runs but may omit paths not exercised. Combine them and fall back on uncertainty.

**Path rules versus target graphs.** Path rules are easy to start and review. Target graphs express transitive impact. Use path rules for explicit global policies or as conservative additions, not as the sole dependency model in coupled systems.

**Precision versus recall.** Higher precision saves more work; higher recall avoids misses. Critical gates should bias toward recall and use risk baselines. Low-risk exploratory workflows may accept different trade-offs if clearly labeled.

**Central versus owned mappings.** A central selector gives consistency but can become distant from domain changes. Owned target and test metadata stays near code but needs schema and global validation. A shared engine with locally owned declarations is common.

## Failure Modes and Misconceptions

- **“No diff means no change.”** Resolution or parsing may have failed.
- **“The previous commit is always the base.”** Proposals often require a merge-base comparison.
- **“Rename is only a move.”** Location can change ownership and policy.
- **“Deletion cannot affect consumers.”** It can break every dependent target.
- **“Run tests in the changed folder.”** Consumers may live elsewhere.
- **“The build graph contains every dependency.”** Runtime and undeclared inputs may escape it.
- **“A cached dynamic graph is current.”** Discovery logic may have changed.
- **“Lockfile changes affect one package.”** Resolution can alter broad transitive inputs.
- **“Selected tests passed, so the artifact is safe.”** Evidence is bounded to selected claims.
- **“Full fallback is a performance bug.”** It is required safety behavior under uncertainty.
- **“Zero observed misses proves soundness.”** Rare failures and weak sampling limit inference.
- **“Precision is directly observable.”** The true required set is usually uncertain.
- **“Docs never affect builds.”** Documentation can generate packages and sites.
- **“Selector policy is outside the input set.”** It changes the decision.
- **“Skipped means irrelevant.”** It means not selected under recorded assumptions.

## Worked Examples

### Example 1

**Situation.** A pull request has three commits, and only the last commit is diffed against its parent. **Reasoning.** Earlier proposal changes disappear from the detected set. Compare the candidate or exact merge result to the intended merge base. **Conclusion.** Base selection is part of correctness.

### Example 2

**Situation.** `lib` changes and `app` depends on it. **Reasoning.** Reverse closure selects `lib`, `lib-test`, `app`, and `app-test`, plus the smoke baseline. Traversing from `lib` to its suppliers would miss consumers. **Conclusion.** Impact flows toward reverse dependencies.

### Example 3

**Situation.** A source file is deleted. **Reasoning.** The old graph still maps its owning target and consumers. Treat the deletion as a changed input; do not remove the node before computing impact. **Conclusion.** Deletions require old-and-new graph reasoning.

### Example 4

**Situation.** A lockfile changes one visible line. **Reasoning.** Re-resolve and compare dependency identities; transitive packages, licenses, platform variants, and artifacts may change. Select dependent builds and relevant supply-chain gates. **Conclusion.** Diff size does not bound semantic impact.

### Example 5

**Situation.** `schema.proto` changes. **Reasoning.** Select the generator, generated libraries, their consumers, and contract tests through explicit edges. Directory-only selection misses distant clients. **Conclusion.** Generated relationships belong in the graph.

### Example 6

**Situation.** A plugin is loaded by scanning a directory at runtime. **Reasoning.** Static imports omit the edge. Capture and declare plugin metadata or classify the registry as a broad invalidator. Until then, fall back. **Conclusion.** Dynamic discovery requires explicit uncertainty handling.

### Example 7

**Situation.** The selector cannot parse one changed path. **Reasoning.** Returning an empty set converts error to false assurance. Emit a typed reason and select full scope. **Conclusion.** Unknown is not unaffected.

### Example 8

**Situation.** Selection runs 20 of 1,000 tests, and all pass. **Reasoning.** This validates selected claims only. Run sampled shadow full suites and track disagreements; retain mandatory security and manifest baselines. **Conclusion.** Efficiency evidence and safety evidence must both be collected.

### Example 9

**Situation.** Ten shadow full runs find no misses. **Reasoning.** With rare regressions, the sample has little power; report its size and change distribution rather than “100% sound.” Seed known mutations and expand sampling after selector changes. **Conclusion.** Absence of observed misses is bounded evidence.

### Example 10

**Situation.** A root CI policy file changes. **Reasoning.** It can alter which evidence every job produces. Treat it as a global invalidator, validate policy itself, and execute full applicable scope. **Conclusion.** Decision machinery is part of the dependency model.

## Cross-Program Connections

- Algorithm Engineering owns graph traversal complexity and implementation; this chapter owns conservative CI use.
- Data Structures Engineering owns graph representations and worklist behavior.
- Compilers & Language Implementation provides incremental dependency and generated-code examples.
- Testing & Quality Engineering owns test selection validity and mutation-based evaluation.
- Security Engineering owns adversarial bypass and trusted selector execution.
- Platform Engineering owns target metadata, graph services, runner capacity, and developer explanations.
- Data Engineering owns lineage analogies and dynamic data dependencies.
- API & Service Engineering owns cross-repository contract-impact mappings.

## References

1. Git Project, [git-diff Documentation](https://git-scm.com/docs/git-diff) and [git-merge-base Documentation](https://git-scm.com/docs/git-merge-base), current manuals. Retrieved 2026-09-06.
2. Andrey Mokhov, Neil Mitchell, and Simon Peyton Jones, [Build Systems à la Carte](https://www.microsoft.com/en-us/research/publication/build-systems-la-carte/), ICFP 2018; expanded *Journal of Functional Programming* version, 2020.
3. Bazel Project, [Query Quickstart: Finding Reverse Dependencies](https://bazel.build/query/quickstart), official documentation. Retrieved 2026-09-06.
4. Robert C. Martin, *Clean Architecture*, Pearson, 2017, dependency direction and boundary foundations.
5. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, build and test pipeline foundations.

## Exercises

### Exercise 1

Define change detection, affected-set computation, and selective execution, and state one failure each can introduce.

### Exercise 2

Given edges `schema→gen`, `gen→lib`, `lib→api`, `lib→lib-test`, and `api→api-test`, compute the affected set for `{schema}` and for `{api}`.

### Exercise 3

A proposed branch is diffed only against its previous commit, the dependency graph is from yesterday, and an unknown root file appears. Diagnose the required behavior and evidence.

### Exercise 4

Design selection policy for a monorepo containing application code, generated clients, Terraform, documentation that builds a site, a root lockfile, and repository-wide license policy.

### Exercise 5

A selector reports 99% test reduction and no misses across 50 shadow runs. Design an evaluation that could justify continued use for a safety-relevant release gate.

## Answers to the Exercises

### Answer 1

Change detection compares two exact source trees and emits typed changed inputs; a wrong base can omit proposal changes. Affected-set computation propagates those inputs through dependency and risk mappings; an incomplete graph can omit consumers. Selective execution schedules the computed closure and mandatory baselines; bad binding or fallback behavior can reuse irrelevant evidence or skip required work. Each stage records versions and treats uncertainty conservatively.

### Answer 2

For `{schema}`, reachability yields `{schema, gen, lib, api, lib-test, api-test}`. For `{api}`, it yields `{api, api-test}`. Baselines would be unioned afterward. This assumes edges point from producer to possible consumer and the graph is complete; if edges use the opposite convention, traverse reverse adjacency instead.

### Answer 3

The previous-commit diff omits earlier branch changes, so recompute from the intended merge base or exact merge result. Yesterday's graph is not automatically valid for today's candidate; rebuild it or prove compatible binding. The unknown root file has no safe ownership mapping and may be a global control. Emit a selection record naming the base, candidate, diff, graph and policy versions, unknown path, and fallback reason, then run full applicable scope. Do not return no work.

### Answer 4

Map each source to build targets; encode schema-to-generator-to-client-to-consumer edges. Map Terraform to validation, plan, policy, and owned deployment checks. Map documentation inputs to site generation and link checks. Treat the root lockfile as broad dependency invalidation after resolving exact changes. Run repository-wide license and manifest policy as mandatory baselines. Include generator binaries, CI definitions, toolchains, and environment images as control inputs. Any unmapped file, stale graph, or failed parser invokes full scope. Record derivation paths for every selected and skipped target.

### Answer 5

First define the exact gate claims and unacceptable false-negative classes. Stratify a much larger shadow sample by source, deletion, rename, generated, lockfile, policy, toolchain, dynamic dependency, and high-risk subsystem changes. Run full suites on every critical change plus randomized ordinary changes. Seed known mutations and dependency-edge removals to measure recall. Track downstream and production escapes attributable to skips, graph age, unknown ownership, and fallback behavior. Independently review graph completeness and selector changes. Report confidence bounds and detection opportunities; 50 failure-free runs do not establish 100% soundness. Keep full fallback and mandatory safety baselines until evidence supports a bounded policy.
