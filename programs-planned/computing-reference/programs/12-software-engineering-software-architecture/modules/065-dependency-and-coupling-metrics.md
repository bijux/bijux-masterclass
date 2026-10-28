---
module_id: SARCH-065
program: Software Engineering: Software Architecture
level: 2
module_number: 65
title: Dependency and Coupling Metrics
status: complete
last_verified: 2026-09-06
---

# Dependency and Coupling Metrics

## One-Page Review

### Governing question

Which dependencies make change, failure, authority, or delivery propagate across architectural boundaries, and which measurements reveal that exposure without rewarding superficial graph manipulation?

### Essential definitions

- A **dependency** exists when one element's correct construction, execution, change, deployment, authority, or recovery relies on another.
- **coupling** is the degree and consequence of interdependence; it is multidimensional, not one edge count.
- **afferent coupling** $C_a$ counts selected external elements depending on an element; **efferent coupling** $C_e$ counts selected external elements it depends on.
- **instability** $I=C_e/(C_a+C_e)$ is a structural ratio between 0 and 1 when the denominator is nonzero; it is not operational failure probability.
- **fan-in** and **fan-out** count incoming and outgoing relations under a declared graph extraction.
- A **strongly connected component (SCC)** is a maximal set whose nodes are mutually reachable; an SCC with multiple nodes represents a dependency cycle.
- **propagation cost** measures the fraction of ordered node pairs connected by direct or transitive dependency in a declared design-structure matrix.
- **change coupling** measures co-change history; **runtime coupling** measures call, message, state, timing, or capacity dependence during execution.
- **deployment coupling** means elements must coordinate release, configuration, migration, or rollback.
- **semantic coupling** arises from shared meanings, invariants, protocols, identities, or policy even without a visible code edge.

### Central model, mechanism, or theorem

Model an architecture as a typed directed multigraph $G=(V,E,\tau)$, where $\tau(e)$ identifies dependency kind. Counts require a selected edge projection; combining imports, calls, data, authority, and deployment into one untyped graph destroys meaning.

For $n=|V|$, let $R_{ij}=1$ when $j$ is reachable from $i$, including direct edges but excluding self-reachability. A simple propagation cost is

$$
PC=\frac{\sum_{i\ne j}R_{ij}}{n(n-1)}.
$$

This quantifies potential structural reachability only. Direction, edge type, likelihood, change size, runtime condition, ownership, and consequence require separate evidence.

### Critical invariants

- every metric names nodes, edge type, direction, extraction, scope, revision, and exclusions;
- direct and transitive dependency remain distinct;
- cycles are evaluated by responsibility and consequence, not condemned by shape alone;
- code, runtime, data, authority, deployment, change, and organizational graphs are not silently merged;
- high fan-in is not automatically bad and low fan-out is not automatically good;
- generated facades, brokers, registries, and shared libraries do not erase semantic or operational coupling;
- co-change is evidence for investigation, not proof of causal dependency;
- thresholds derive from scenarios and baselines rather than universal “good” numbers;
- graph reduction cannot pass while failure, change, or authority propagation worsens;
- decisions pair metrics with qualitative trace, tests, and stakeholder consequences.

### Common failures

Common failures include counting imports only; mixing node granularity; interpreting instability as defect probability; minimizing fan-out by creating a god module; hiding edges behind a shared library or event bus; calling asynchronous systems decoupled; ignoring schema, identity, time, and control dependencies; treating all cycles alike; inferring cause from co-change; averaging away a critical hub; comparing graphs from different extractors; optimizing a threshold through renames; and claiming lower coupling without measuring deployment or failure propagation.

### Compact example

For modules `web -> billing -> ledger` and `web -> identity`, billing has $C_a=1$, $C_e=1$, so $I=1/2$. Ledger has $C_a=1$, $C_e=0$, so $I=0$. These ratios describe the selected import graph. If ledger and billing share one schema migration and must deploy together, their deployment coupling remains high even though ledger has no outgoing import.

### Connections

[SARCH-064](064-architecture-fitness-functions.md) shows how to guard selected boundaries. [SARCH-066](../ROADMAP.md) next develops performance and capacity models. Programming-language and design programs own lower-level modularity; this module owns architectural interpretation across dependency graphs.

## Governing Question

Coupling is where architecture becomes consequence. A compile-time edge can spread changes; a synchronous call can spread latency; shared data can spread schema coordination; a global authority can spread outage or compromise; a shared deployment can spread release risk.

Metrics make structure inspectable, but only after defining what the graph represents. The evaluator's job is to connect graph observations to quality scenarios, not to optimize aesthetically pleasing numbers.

## Why This Matters

Large systems often look modular in source while remaining inseparable in production. Services may own repositories yet share one database, release train, identity issuer, or incident fate. Conversely, deliberate stable dependencies on a trusted foundation may reduce duplication and improve change.

Typed measurements reveal hubs, cycles, propagation paths, coordination, and drift. They support refactoring and investment when combined with ownership, runtime, change, failure, and business evidence.

## Prerequisites and Retrieval

Retrieve module, responsibility, information hiding, cohesion, dependency, coupling, directed graph, multigraph, degree, path, reachability, cycle, SCC, fan-in, fan-out, afferent, efferent, instability, design-structure matrix, transitive closure, centrality, co-change, correlation, confounder, schema, authority, deployment, blast radius, and fitness function.

From SARCH-031 through SARCH-040 retrieve modular styles. SARCH-041 through SARCH-050 supply integration, data, deployment, and tracing. SARCH-051 through SARCH-060 supply failure propagation. SARCH-061 through SARCH-064 supply scenarios, sensitivity, and governed measurement.

## Learning Objectives

After completing this module, you should be able to:

1. define typed architecture graphs at a defensible granularity;
2. compute and interpret fan-in, fan-out, afferent/efferent coupling, and instability;
3. find cycles, SCCs, transitive reachability, and propagation cost;
4. distinguish static, runtime, data, authority, deployment, change, and organizational coupling;
5. identify hubs, hidden dependencies, and common causes;
6. avoid causal and quality claims unsupported by graph measures;
7. normalize and compare revisions without metric gaming;
8. combine dependency metrics with scenarios, evidence, and ownership;
9. design fitness functions for meaningful coupling constraints;
10. select architectural changes based on consequences rather than universal thresholds.

## Core Exposition

**Define nodes by responsibility.** Nodes may be packages, modules, services, databases, teams, deployment units, data products, or control authorities. A mixed graph can be useful only when node types are explicit. Granularity changes counts: merging ten packages into one “platform” reduces visible edges without changing work.

Choose nodes that match the scenario. Source modules suit compile-time change; services and stores suit runtime failure; deployable units suit release independence; authorities suit safety and security.

**Type every edge.** Import, call, message, shared schema, shared database, lock, transaction, timing deadline, resource, identity, configuration, deployment, ownership, and recovery are different relations. Record direction: consumer depends on provider, but provider may also depend on consumer throughput or schema behavior.

Edges can carry weight, criticality, frequency, latency budget, version, optionality, and failure semantics. Do not add incompatible weights merely to create one score.

**Extract static dependencies.** Parse imports, symbols, build manifests, generated code, reflection configuration, plugin registries, and infrastructure definitions. Store extractor and version. Validate with known legal and illegal fixtures.

Static graphs reveal structural reachability but miss dynamic loading, data contracts, operational procedures, and environment topology. A facade may reverse source direction while leaving semantic dependence intact.

**Count degree carefully.** Fan-out or $C_e$ estimates how many selected external elements a node relies on; fan-in or $C_a$ estimates how many rely on it. High fan-in can indicate a stable shared abstraction or a high-blast-radius bottleneck. High fan-out can indicate orchestration or poorly bounded responsibility.

Use distributions and identify named hubs. The average degree of a sparse graph can look low while one identity or schema node connects every critical path.

**Interpret instability narrowly.** $I=C_e/(C_a+C_e)$ is 0 for a node with only incoming edges and 1 for only outgoing edges. A node with no incident selected edges has undefined $0/0$; choose and document an output such as `not applicable`, not an invented zero.

The ratio says nothing about cohesion, quality, volatility, correctness, runtime availability, or whether dependency direction matches policy. Use it as a structural descriptor alongside abstractness and responsibility reasoning where relevant.

**Find cycles and SCCs.** A directed acyclic dependency graph supports ordering and isolated reasoning. SCC condensation collapses each strongly connected set into one node and always produces a DAG.

Not every cycle has equal cost. A compile-time cycle may block independent builds; a transaction cycle may be a legitimate atomic boundary; an authority cycle may deadlock recovery. Analyze scenario and edge type before treatment.

**Measure transitive propagation.** Direct edges understate change reach. Compute transitive closure or a design-structure matrix visibility measure. Propagation cost estimates how much of the graph is reachable and therefore potentially exposed.

Reachability is possibility, not certainty. Stable contracts can stop semantic change, feature flags can condition paths, and one reachable safety authority may matter more than hundreds of optional analytical nodes.

**Measure runtime coupling.** Trace calls, queues, shared stores, caches, locks, resource pools, deadlines, and retry paths. Record workload and sampling. Synchronous latency coupling differs from asynchronous backlog and freshness coupling.

Messaging moves temporal coupling but retains schema, semantic, delivery, capacity, ordering, replay, and operational dependencies. A broker can become a hub. “Asynchronous” is not “decoupled.”

**Map data and authority.** Shared database tables, identifiers, invariants, schemas, lineage, residency, keys, and deletion create coupling. Authority edges show who can write, revoke, configure, promote, or actuate.

These graphs often reveal more consequential paths than imports. A locally autonomous edge site may still depend on central policy expiry, while a nominally independent region may share one credential issuer.

**Measure deployment coupling.** Use release histories, compatibility windows, schema migrations, configuration, shared pipelines, coordinated approvals, and rollback constraints. Two units are deployment-coupled when safe change requires coordination even if code repositories differ.

Measure forced co-deployment with stated causes. Frequent voluntary joint release does not prove necessity. Test one-sided mixed-version change and rollback to establish independence.

**Use change coupling as a signal.** Mine version-control changes by logical change identity, excluding bulk formatting, generated files, vendor updates, and mechanical renames. Compare co-change with static and ownership graphs.

Correlation can arise from feature scope, one team, release process, or repository layout. Investigate the reason before extracting a service or forbidding a dependency.

**Include organizational coupling.** Shared on-call, approvals, expertise, budget, suppliers, and decision authority affect change and recovery. Architecture and organization may mirror each other, but the relationship is neither perfect nor automatically causal [5].

Do not use organization metrics for employee ranking. They expose coordination design and single-person dependencies, which require ethical handling and context.

**Analyze failure propagation.** Overlay failure modes on runtime and control graphs. Ask whether timeout, retry, backlog, stale state, compromise, or quota exhaustion crosses the edge. Identify containment and alternate paths.

Graph separation does not prove failure independence. Common software, provider, facility, identity, deployment, or operator dependencies can join apparently separate components.

**Normalize comparisons.** Compare the same node and edge definitions, extractor, exclusions, revision type, and observation window. Report system size and distributions. A falling raw edge count after merging nodes is not improvement.

Keep stable identities across renames. Review metric changes beside scenario outcomes: lead time, failure blast radius, recovery, correctness, and ownership.

**Set contextual thresholds.** Forbid particular directions because they violate information hiding, trust, authority, or deployability. Use warning thresholds for hubs or propagation that warrant review. Ratchet legacy exposure by stable edge identity.

Universal coupling cutoffs ignore domain and graph size. A kernel, plugin platform, data pipeline, and regulated controller need different boundaries.

**Design against gaming.** Detect layer facades that simply forward, shared “common” buckets, event buses with undocumented semantics, node mergers, hidden generated code, and excluded runtime paths. Pair a structural metric with outcome fitness functions.

Metrics should make bad architecture harder to hide, not reward the production of low numbers.

**Choose interventions.** Introduce information-hiding interfaces, split responsibility, invert dependency, isolate data ownership, version contracts, allocate authority, add bulkheads, separate deployment, or accept deliberate coupling within one cohesive boundary.

Every intervention has cost. More services add network, data, operational, and organizational coupling. Optimize total consequences, not source-graph purity.

**Keep evidence bounded.** Report graph source, completeness, extractor, versions, missing dynamic edges, observation window, sampling, uncertainty, and stakeholder review. Metrics are evidence for architecture decisions, not proof of modularity or team quality.

## Definitions and Notation

Let $G=(V,E,\tau)$ be a typed directed multigraph, $n=|V|$, and:

- $C_a(v)$ count selected external nodes with edges into $v$;
- $C_e(v)$ count selected external nodes receiving edges from $v$;
- $I(v)=C_e(v)/(C_a(v)+C_e(v))$ when the denominator is positive;
- $R$ be transitive reachability excluding self pairs;
- $PC=\sum_{i\ne j}R_{ij}/[n(n-1)]$ for $n>1$;
- $J(A,B)=|A\cap B|/|A\cup B|$ be Jaccard similarity for nonempty change sets;
- $w(e)$ be a declared edge weight with one stated meaning;
- **condensation graph** mean the DAG produced by collapsing each SCC;
- **hub** mean a node with exceptional consequence or connectivity under a stated metric;
- **logical change** mean one reviewed intent, not merely one commit or file edit.

Metric values are undefined when their mathematical or extraction prerequisites fail. Report `not applicable` or `unavailable` rather than silently substituting zero.

## Mechanisms, Invariants, or Proof Structure

### Analysis procedure

1. Select quality scenario and propagation consequence.
2. Choose node granularity and typed directed edges.
3. Define extractor, revision, window, weights, exclusions, and missing paths.
4. Validate extraction with fixtures and manual samples.
5. Calculate direct degree, SCCs, reachability, and contextual metrics.
6. Compare static, runtime, data, authority, deployment, change, and organization views.
7. Investigate hubs, cycles, hidden dependencies, common causes, and outliers.
8. Connect observations to outcome evidence and stakeholder ownership.
9. Choose boundary, interface, isolation, coordination, or accepted-coupling intervention.
10. Guard meaningful constraints with stable fitness functions and reevaluate after change.

### Executable metric example

The example computes $C_a$, $C_e$, and instability for a fixed import graph. It proves only these counts under the supplied edge semantics.

<!-- bijux-verify: {"id":"structural-coupling","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"billing Ca=1 Ce=1 I=0.50\nledger Ca=1 Ce=0 I=0.00\nweb Ca=0 Ce=2 I=1.00\n","stderr":""}} -->
```python
graph = {
    "web": {"billing", "identity"},
    "billing": {"ledger"},
    "ledger": set(),
    "identity": set(),
}

for node in ("billing", "ledger", "web"):
    ce = len(graph[node])
    ca = sum(node in targets for targets in graph.values())
    instability = ce / (ca + ce)
    print(f"{node} Ca={ca} Ce={ce} I={instability:.2f}")
```

### Invariants

- no metric lacks graph type, direction, granularity, extractor, and scope;
- no undefined value becomes zero;
- no structural count becomes a probability or quality verdict;
- no co-change correlation becomes causal proof;
- no refactoring passes by hiding or reclassifying consequential edges;
- no lower coupling claim ignores runtime, data, authority, deployment, or recovery outcomes.

## Alternatives and Trade-Offs

- **Package versus service nodes:** packages expose code structure; services expose runtime and deployment but hide internals.
- **Untyped versus typed graph:** untyped graphs simplify algorithms; typed graphs preserve architectural meaning.
- **Direct degree versus reachability:** degree localizes immediate edges; reachability exposes propagation but can overstate actual change.
- **Edge count versus weighted consequence:** counts are reproducible; weights add context but require justified scales.
- **Static versus dynamic extraction:** static analysis is repeatable; runtime tracing sees realized paths but misses unobserved possibilities.
- **Code versus co-change:** code shows declared structure; history shows past coordination but includes confounders.
- **Acyclicity versus cohesive transaction:** removing cycles improves ordering; some mutually dependent behavior belongs inside one boundary.
- **Shared library versus duplicated logic:** sharing centralizes change; duplication reduces dependency but risks semantic divergence.
- **Synchronous versus asynchronous:** synchronous calls expose immediate time coupling; messaging adds backlog, schema, ordering, and operation.
- **Centralization versus federation:** central services standardize policy; federated ownership contains failure but complicates consistency.
- **Fine versus coarse granularity:** fine graphs diagnose precisely; coarse graphs communicate but can hide hubs and cycles.
- **Automated threshold versus expert review:** automation constrains known patterns; review interprets consequence and novel dependency.

## Failure Modes and Misconceptions

1. **“Coupling is one number.”** It spans code, runtime, data, authority, deployment, change, and people.
2. **“High fan-in is bad.”** It can indicate stable reuse or dangerous blast radius; scenario decides.
3. **“Low fan-out is good.”** A god module can hide many internal responsibilities behind one edge.
4. **“Instability predicts failure.”** It is a structural dependency ratio only.
5. **“Zero edges means independent.”** Extraction may miss semantics, runtime, data, control, or organization.
6. **“Events decouple services.”** Schema, broker, ordering, capacity, replay, and meaning remain.
7. **“All cycles are defects.”** Edge type, boundary, and consequence matter.
8. **“Reachability predicts actual change.”** It expresses potential paths, not probability or semantic propagation.
9. **“Co-change proves dependency.”** Features, teams, tooling, and bulk edits confound it.
10. **“Microservices reduce coupling.”** They can exchange compile coupling for network, data, deployment, and operational coupling.
11. **“A facade removes coupling.”** It may only conceal or concentrate it.
12. **“Average degree describes risk.”** A critical hub or minority path can dominate harm.
13. **“Thresholds are universal.”** Context, graph size, quality scenario, and extraction define meaning.
14. **“Renaming resets the baseline.”** Stable identity is required to prevent gaming.
15. **“Teams should be ranked by coupling.”** Metrics describe system coordination and need ethical context.
16. **“Correlation direction is obvious.”** Organization can shape architecture and architecture can shape organization.
17. **“Fewer dependencies always improve design.”** Deliberate stable dependencies can reduce duplication and inconsistency.
18. **“Metrics prove modularity.”** They support bounded decisions and require qualitative and outcome evidence.

## Worked Examples

### Example 1

**Interpret degree and instability.**

**Situation.** In the executable graph, `web` depends on billing and identity, while billing depends on ledger.

**Reasoning.** Web has $C_a=0,C_e=2,I=1$; billing has $1,1,0.5$; ledger has $1,0,0$. Web is maximally outward-dependent in this projection, but that does not mean it is defective. Ledger appears stable structurally, yet its correctness and operational availability remain unmeasured.

**Conclusion.** The ratios describe direction under one graph, not quality or risk.

### Example 2

**Handle an undefined ratio.**

**Situation.** A standalone migration utility has no selected import edges.

**Reasoning.** $C_a+C_e=0$, so $I=0/0$ is undefined. Recording zero would make it look maximally stable and distort averages. Report not applicable and inspect its database, schema, credentials, deployment, and operator dependencies in other graphs.

**Conclusion.** Honest missing semantics are better than a convenient zero.

### Example 3

**Compute propagation cost.**

**Situation.** A four-node chain is $A\to B\to C\to D$.

**Reasoning.** Reachable ordered pairs are $(A,B),(A,C),(A,D),(B,C),(B,D),(C,D)$: six. There are $4\cdot3=12$ nonself ordered pairs, so $PC=6/12=0.5$. Reversing the chain preserves the value; edge semantics and ownership determine whether either direction is preferable.

**Conclusion.** Propagation cost measures reachability volume, not appropriate direction.

### Example 4

**Collapse a cycle.**

**Situation.** Pricing depends on catalog, catalog on promotion, and promotion on pricing; checkout depends on pricing.

**Reasoning.** The three mutually reachable nodes form one SCC. Under the consumer-to-provider dependency orientation used here, its condensation contains `checkout -> {pricing,catalog,promotion}`. Independent deployment within the SCC is suspect. Review may create one cohesive boundary or break semantic responsibilities with explicit contracts.

**Conclusion.** SCC detection localizes inseparability; it does not choose the repair.

### Example 5

**Expose asynchronous coupling.**

**Situation.** Order and inventory share no synchronous calls; they communicate through a broker.

**Reasoning.** The dependency graph includes event schema and meaning, partition key, ordering, retention, consumer lag, replay, deduplication, broker capacity, and reconciliation. If inventory must reserve within 30 seconds, backlog age is temporal coupling. Broker loss or schema drift can still block the outcome.

**Conclusion.** Asynchrony changes coupling shape and time, not its existence.

### Example 6

**Reject a facade game.**

**Situation.** Twenty forbidden module imports are replaced by one import of `common`, which forwards to the same modules.

**Reasoning.** Direct fan-out falls, but transitive reachability and responsibility concentration do not. Runtime and change graphs show the same propagation, while `common` becomes a hub. The fitness function inspects transitive paths and forbids catch-all ownership.

**Conclusion.** A metric improvement without consequence improvement is gaming.

### Example 7

**Investigate co-change.**

**Situation.** Billing and notification changed together in 18 of 20 releases.

**Reasoning.** History review finds 12 changes were bulk dependency upgrades, four were coordinated features, and two were truly incompatible event changes. The adjusted signal points to event-versioning weakness, not a need to merge services. Mixed-version contract tests supply causal evidence.

**Conclusion.** Co-change prioritizes investigation after confounders are removed.

### Example 8

**Find hidden regional coupling.**

**Situation.** Two regions have separate compute and databases and no cross-region request edges.

**Reasoning.** Authority and recovery graphs reveal one identity issuer, DNS controller, artifact registry, and deployment pipeline. Cold bootstrap and credential rotation require those global nodes. Failure tests confirm both regions can serve warm traffic during identity loss but neither can recover cold.

**Conclusion.** Runtime request separation did not establish control or recovery independence.

### Example 9

**Compare deployment and code graphs.**

**Situation.** Profile and preference services share no source dependencies but always release together.

**Reasoning.** They share a database migration, one unversioned schema, and rollback ordering. Deployment coupling is causal even though code fan-out is zero. Introduce schema ownership, expand-contract migration, and mixed-version tests; then measure whether independent rollback succeeds.

**Conclusion.** Repository separation is insufficient evidence of release independence.

### Example 10

**Use coupling to guide a safety boundary.**

**Situation.** A local pump interlock depends on a cloud optimizer for configuration and current time.

**Reasoning.** Authority and timing edges put the hard safety loop behind network, cloud identity, and clock dependencies. The architecture moves invariant enforcement and bounded time holdover local, keeps optimization advisory, signs expiring envelopes, and tests disconnection. Cloud telemetry remains coupled for fleet analysis but not immediate actuation.

**Conclusion.** Consequence-directed graph analysis removes critical coupling while preserving useful coordination.

## Cross-Program Connections

- **Data Structures Engineering:** owns graph representations, traversal, reachability, SCC algorithms, and complexity.
- **Algorithm Engineering:** owns graph metrics, approximation, scaling, and adversarial analysis.
- **Software Engineering Patterns:** owns module- and pattern-level coupling and cohesion mechanisms.
- **Software Delivery and Reliability Engineering:** owns co-change, deployment, incident, and failure-propagation evidence.
- **Distributed Systems Engineering:** owns runtime dependencies, consensus, replication, failure models, and causality.
- **Data Architecture Engineering:** owns schema, authority, lineage, lifecycle, and shared-data coupling.
- **Platform Engineering:** owns shared control, identity, deployment, routing, and observability dependencies.
- **Security Engineering:** owns trust, privilege, key, compromise, and recovery coupling.
- **Systems Engineering:** owns organizational, supplier, physical, safety, and lifecycle dependencies.
- **Programming Languages:** supplies module, type, interface, information-hiding, and linking mechanisms.

## References

1. David L. Parnas, “On the Criteria to Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972. <https://doi.org/10.1145/361598.361623>
2. Wayne P. Stevens, Glenford J. Myers, and Larry L. Constantine, “Structured Design,” *IBM Systems Journal* 13(2), 1974. <https://doi.org/10.1147/sj.132.0115>
3. Shyam R. Chidamber and Chris F. Kemerer, “A Metrics Suite for Object Oriented Design,” *IEEE Transactions on Software Engineering* 20(6), 1994. <https://doi.org/10.1109/32.295895>
4. Robert C. Martin, *Clean Architecture*, Pearson, 2017.
5. Alan MacCormack, John Rusnak, and Carliss Y. Baldwin, “Exploring the Duality between Product and Organizational Architectures: A Test of the Mirroring Hypothesis,” *Research Policy* 41(8), 2012. <https://doi.org/10.1016/j.respol.2012.04.011>
6. Carliss Y. Baldwin and Kim B. Clark, *Design Rules, Volume 1: The Power of Modularity*, MIT Press, 2000.
7. Neeraj Sangal, Ev Jordan, Vineet Sinha, and Daniel Jackson, “Using Dependency Models to Manage Complex Software Architecture,” *Proceedings of OOPSLA 2005*. <https://doi.org/10.1145/1094811.1094824>
8. Mark E. J. Newman, *Networks*, 2nd ed., Oxford University Press, 2018.
9. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
10. Matthew Skelton and Manuel Pais, *Team Topologies*, 2nd ed., IT Revolution, 2025.

## Exercises

### Exercise 1

Define dependency, coupling, afferent coupling, efferent coupling, instability, fan-in, fan-out, path, reachability, SCC, condensation graph, propagation cost, runtime coupling, data coupling, authority coupling, deployment coupling, change coupling, semantic coupling, and hub.

### Exercise 2

For graph $A\to B$, $A\to C$, $B\to C$, $C\to D$, compute $C_a$, $C_e$, and instability for each node, marking undefined values correctly. Compute propagation cost excluding self pairs.

### Exercise 3

Diagnose a dashboard that counts only direct imports, merges all platform modules into one node, treats undefined instability as zero, interprets co-change as causation, and rewards lower fan-out after adding a forwarding facade. Design corrected extraction and evidence.

### Exercise 4

Compare compile-time, runtime, data, authority, deployment, change, and organizational coupling for a multi-region payment service. Identify which metrics, experiments, and qualitative traces can establish each and where they conflict.

### Exercise 5

Design dependency and coupling analysis for an international food cold-chain platform with farm sensors, trucks, border agencies, warehouses, retailers, payments, intermittent links, privacy, safety limits, supplier software, and cloud analytics. Cover graph types, granularity, extraction, metrics, hidden dependencies, cycles, failure propagation, organization, gaming, interventions, evidence, and residual risk.

## Answers to the Exercises

### Answer 1

A **dependency** is reliance on another element for construction, execution, change, deployment, authority, or recovery. **Coupling** is degree and consequence of interdependence. **Afferent** $C_a$ counts selected incoming external dependents; **efferent** $C_e$ counts selected outgoing external dependencies. **Instability** is $C_e/(C_a+C_e)$ when defined. **Fan-in/out** are incoming/outgoing counts. A **path** is an edge sequence; **reachability** means a path exists. An **SCC** is a maximal mutually reachable set; its **condensation graph** collapses SCCs into a DAG. **Propagation cost** is a declared reachable-pair fraction. Runtime, data, authority, deployment, change, and semantic coupling name their dependency dimensions. A **hub** has exceptional connectivity or consequence under a stated measure.

### Answer 2

$A$ has $C_a=0,C_e=2,I=1$. $B$ has $C_a=1,C_e=1,I=0.5$. $C$ has $C_a=2,C_e=1,I=1/3$. $D$ has $C_a=1,C_e=0,I=0$. No node is isolated, so no denominator is zero.

Reachable pairs are $A\to B,C,D$ (three), $B\to C,D$ (two), and $C\to D$ (one), totaling six. With four nodes there are $4(3)=12$ nonself ordered pairs, so $PC=6/12=0.5$. The value needs edge semantics and cannot determine whether directions or responsibilities are appropriate.

### Answer 3

Define stable responsibility-level nodes and preserve internal platform nodes in detailed views. Extract direct and transitive imports plus build, generated, reflection, plugin, and infrastructure paths. Report isolated-node instability as not applicable. Keep raw graph, extractor/version, revision, exclusions, and manual fixture validation.

Treat co-change as a signal: remove formatting, generated, dependency-update, and bulk-move confounders; inspect feature and schema causes; use mixed-version tests. Detect forwarding facades by transitive reachability, ownership, change, and runtime graphs. Pair metrics with deployment independence, latency/failure propagation, data authority, and business-outcome evidence. Thresholds protect named boundaries; they do not reward raw count reduction.

### Answer 4

Compile coupling comes from imports, symbols, builds, generated code, plugins, and manifests; use degree, SCC, reachability, and forbidden-direction rules. Runtime coupling comes from calls, messages, queues, deadlines, retries, resources, and failure; use traces, dependency maps, load and fault tests. Data coupling comes from stores, schemas, identifiers, invariants, lineage, residency, and deletion; use catalogs plus observed flows and reconciliation.

Authority coupling maps identity, write, promotion, configuration, key, and emergency powers; test partition, revocation, stale authority, and recovery. Deployment coupling uses migrations, compatibility, release/rollback ordering, pipelines, and approvals; verify one-sided mixed-version deployment. Change coupling uses cleaned logical-change history and is correlational. Organizational coupling maps ownership, on-call, expertise, approvals, suppliers, and incident coordination with ethical safeguards.

Separate regional compute can lower runtime coupling while shared identity, DNS, artifact, data, or operators retain authority and recovery coupling. Asynchronous payments reduce temporal call coupling but add broker, schema, replay, capacity, and reconciliation coupling. No graph alone establishes financial integrity, security, or resilience.

### Answer 5

Use typed graphs at device, site, vehicle, warehouse, agency, payment, retailer, data product, team, supplier, deployment, and authority granularity. Edges cover protocols, events, temperature data, shipment identity, custody, payment, command authority, clock, configuration, firmware, cloud control, residency, deployment, support, and recovery. Extract code/build/configuration, gateway and network inventory, schemas/catalogs, runtime traces, release history, contracts, incident evidence, and interviews; validate missing offline and legacy paths.

Calculate direct degree, named hubs, SCCs, transitive reachability, propagation cost, deployment and cleaned co-change signals per typed projection. Inspect shared identity, border interfaces, cloud registry, time, carrier, supplier updates, refrigeration power, and human approval as hidden common causes. Analyze cycles in custody/payment correction and command authority by consequence. Fault scenarios cover sensor loss/spoofing, truck isolation, border delay, warehouse outage, stale command, cloud loss, bad update, full buffer, payment ambiguity, and reconnect surge.

Prevent gaming through stable identities, granular platform views, transitive checks, generated/plugin coverage, and outcome guardrails. Interventions include local safety envelopes, bounded offline rights, versioned events, authoritative shipment identity, gateway trust boundaries, cells, bulkheads, separate deployments, compatible migrations, supplier contracts, and accepted cohesive transactions. Evidence combines graph fixtures, mixed-version tests, load/fault/recovery exercises, physical temperature and refrigeration tests, reconciliation, privacy/security review, and representative operators. Food-safety, customs, privacy, financial, security, supplier, worker, and regulatory owners retain residual authority; metrics do not certify safety or compliance.
