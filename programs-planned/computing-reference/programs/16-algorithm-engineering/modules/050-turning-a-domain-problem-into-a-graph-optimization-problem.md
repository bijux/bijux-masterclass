---
module_id: ALGE-050
program: Algorithm Engineering
level: 1
module_number: 50
title: Turning a Domain Problem into a Graph Optimization Problem
status: complete
last_verified: 2026-09-05
---

# Turning a Domain Problem into a Graph Optimization Problem

## One-Page Review

### Governing question

How do we turn an ambiguous domain decision into the right graph optimization problem, prove that the translation answers the intended question, and validate the complete data-to-decision chain?

### Essential definitions

- A **decision specification** identifies choices, hard constraints, objectives, units, time horizon, uncertainty, and acceptable evidence.
- A **conceptual model** names domain entities and relationships without committing to an algorithm.
- A **formal model** gives sets, variables, constraints, and an objective.
- A **reduction** maps domain instances and solutions to graph instances and witnesses.
- **Soundness** means every accepted graph witness projects to a valid domain decision.
- **Completeness** means every intended domain decision can be represented.
- **Objective preservation** means the mapping retains the intended ordering or value of decisions.
- **Verification** asks whether the model and software were built as specified; **validation** asks whether the specification is fit for its purpose.
- A **certificate** is independently checkable evidence for feasibility or optimality on one immutable snapshot.

### Central model, mechanism, or theorem

Use a traceable chain:

$$
\text{purpose}\to\text{decision specification}\to\text{conceptual model}
\to\text{formal model}\to\text{graph instance}\to\text{solver witness}
\to\text{certificate}\to\text{domain decision}.
$$

For each arrow, state ownership, assumptions, invariants, failure states, and tests. Algorithm correctness covers only the solver arrow. An operationally trustworthy result requires the entire chain.

### Critical invariants

- Every authoritative entity has stable identity and declared multiplicity.
- Hard constraints are structural; soft preferences have meaningful coefficients.
- Objective direction, units, priority, and tie policy are explicit.
- The chosen graph family matches conservation, reuse, divisibility, and interaction assumptions.
- Soundness, completeness, and objective preservation are proved separately.
- Tiny exact oracles and metamorphic tests check the implementation of the reduction.
- Input, graph, witness, certificate, and projection share a digest and schema version.

### Common failures

Common failures include solving a proxy metric; treating missing data as zero; encoding hard rules as weak penalties; choosing shortest path when choices interact; choosing flow when items are indivisible or commodities couple; forgetting negative weights or cycles; assuming integrality survives side constraints; benchmarking only easy instances; accepting solver status without a certificate; projecting stale identifiers; and deploying an optimum without monitoring model drift.

### Compact example

A route planner minimizes monetary tolls although the stated goal is emergency arrival time. Its shortest-path implementation and certificate may be flawless, but the objective is invalid. Replacing edge weights with validated time estimates repairs the formal intent only if time is additive and static over the route; otherwise a time-dependent model is required.

### Connections

[ALGE-049](./049-network-flow-modeling-patterns.md) gives reusable transformations. [ALGE-051](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) begins Level II with specialized sequence models. Systems Engineering owns requirements and acceptance; Data Engineering owns feature provenance; Software Architecture owns solver and verifier boundaries.

## Governing Question

Starting from a real decision rather than a named algorithm, how can we identify the mathematical structure, select an appropriate graph problem, prove the translation correct, test its implementation, and communicate evidence and limitations to decision owners?

The objective is disciplined modeling, not forcing every domain into a graph. A correct conclusion may be that shortest path, matching, or flow is appropriate; that a richer graph model is needed; or that graph optimization is the wrong abstraction.

## Why This Matters

Algorithm courses often begin with a graph already supplied. Production systems begin with policies, records, forecasts, partial observations, and stakeholders who use words such as “best,” “available,” and “fair” differently. The most damaging errors arise before the solver runs: incorrect identity, omitted constraints, mixed units, wrong objective priority, or an abstraction that permits impossible decisions.

A disciplined workflow makes these errors reviewable. It distinguishes theorem-backed evidence about a formal instance from evidence that the instance represents reality. It also makes later change safer: when policy or data semantics change, engineers can identify which transformation, proof, test, and certificate must change.

## Prerequisites and Retrieval

Retrieve graph representations, shortest paths, spanning trees, matching, cuts, maximum and minimum-cost flow, reductions, asymptotic complexity, invariants, counterexamples, and test oracles. Review [ALGE-049](./049-network-flow-modeling-patterns.md) for concrete gadgets and [ALGE-045](./045-max-flow-min-cut-theorem.md) for certificate reasoning.

## Learning Objectives

After completing this module, you should be able to:

1. turn stakeholder language into a bounded decision specification;
2. define entities, choices, constraints, objectives, units, and time semantics;
3. select among reachability, shortest path, spanning tree, matching, cut, and flow;
4. recognize when graph assumptions fail;
5. prove reduction soundness, completeness, and objective preservation;
6. design normalized graph and witness schemas;
7. use tiny oracles, adversarial cases, and metamorphic tests;
8. separate model, solver, certificate, and projection evidence;
9. review performance and lifecycle risks; and
10. publish a decision with limitations and monitoring triggers.

## Core Exposition

### Begin with the decision, not the algorithm

Write one sentence naming the decision maker, decision, horizon, hard constraints, objective order, and evidence threshold. Replace vague words with observable definitions. “Find the best route” becomes: “For the road snapshot at time $T$, find an allowed origin-to-destination route minimizing the sum of declared expected traversal seconds, subject to vehicle restrictions; return a path and shortest-distance certificate.”

List outputs and failure states before inputs. Distinguish `INFEASIBLE`, `UNREACHABLE`, `UNBOUNDED`, `OPTIMAL`, `APPROXIMATE`, `TIME_LIMIT`, invalid input, and stale data where applicable. Decide whether an empty solution is valid, whether partial service is allowed, and how ties are handled.

### Build a conceptual model

Identify domain entities, relationships, resources, events, and policies. Ask:

- Is identity stable, or can records duplicate one entity?
- Is a relationship directed, symmetric, or time-dependent?
- Is a quantity divisible and conserved?
- Can an entity be reused, and how often?
- Are costs additive and independent?
- Do choices interact through shared capacity, sequence, or failure domain?
- Which missing values mean forbidden, unknown, zero, or unlimited?

Draw a small example in domain language and enumerate valid decisions manually. A conceptual model is useful precisely because it can reveal that a graph edge would hide an important state variable.

### Choose the graph family by invariant

Match the dominant invariant rather than surface vocabulary:

- **Reachability:** whether a permitted connection sequence exists.
- **Shortest path:** one walk with additive edge cost and appropriate cycle assumptions.
- **Minimum spanning tree:** connect every vertex in an undirected graph with minimum total selected-edge weight; it is not a route from one source.
- **Bipartite matching/assignment:** conflict-free one-to-one compatibility, optionally with additive pair cost.
- **Maximum flow:** divisible single-commodity throughput under local conservation and capacities.
- **Minimum-cost flow:** required conserved quantities with separable linear arc costs.
- **Minimum cut:** cheapest separation or closure pattern after a valid reduction.
- **Directed acyclic graph optimization:** precedence or state transitions with no cycles.

If the state needed to make future cost independent of history is small, expand vertices to include it. If expansion is exponential or constraints are global and logical, consider dynamic programming, integer programming, constraint programming, or a specialized method.

### Define the formal graph schema

Specify vertex and edge types, orientation, attributes, units, allowed multiplicity, defaults, and validation. Do not let a library's defaults become domain policy. An omitted capacity might mean infinity to a tool and “invalid record” to the application.

Use stable edge identity for multigraphs. Canonicalize ordering and numeric representation before hashing. Record source data versions, transformation version, time zone, observation time, and rounding policy. Reject undeclared endpoints, invalid self-loops, NaN, reversed bounds, overflow-prone values, and inconsistent units before solving.

### Prove the reduction in both directions

For a domain solution $D$, construct a graph witness $W(D)$ and show every graph constraint. Then take any accepted graph witness $W$, project it to $D(W)$, and show every domain constraint. Finally prove

$$
\operatorname{domainValue}(D)=\operatorname{graphValue}(W(D))
$$

or the exact monotone/decision correspondence required.

State where integrality enters. An integral flow can represent units only if one unit has the intended meaning and projection does not split an indivisible domain object across paths. Additional constraints may destroy total unimodularity. A reduction proof should include empty, minimum-size, disconnected, duplicated, and infeasible cases.

### Separate hard constraints, objectives, and evidence

A hard rule belongs in feasibility. A preference belongs in the objective only with a meaningful scale or declared priority. Lexicographic objectives first optimize the highest priority, fix its optimum, then optimize the next. A weighted sum reproduces that policy only with proved bounds.

Evidence has layers:

1. schema evidence: the input is well formed;
2. transformation evidence: graph rows trace to domain records;
3. witness evidence: the solver output is feasible;
4. optimality evidence: a path potential, cut, cover, dual vector, or bound closes the gap;
5. projection evidence: the domain decision obeys original rules;
6. fitness evidence: domain review, sensitivity analysis, and monitoring support intended use.

Passing an earlier layer does not imply a later one.

### Use tiny exact oracles

For small instances, enumerate domain decisions directly and compare them with the graph solver. This catches transformation defects without relying on a second copy of the same reduction. Generate boundary and adversarial cases: no entities, one entity, parallel relationships, unreachable targets, zero and negative weights, maximum capacities, ties, invalid records, and contradictory rules.

When exhaustive search is impossible, use an independent algorithm, relaxation bounds, or manually verified cases. Treat randomized fuzzing as evidence over sampled inputs, not proof over all inputs.

### Apply metamorphic testing

Metamorphic properties generate related instances with predictable outcomes:

- permuting stable IDs should not change objective value;
- adding an isolated irrelevant vertex should not change a route;
- multiplying all costs by positive $k$ should preserve minimizers and scale value by $k$;
- increasing capacity cannot reduce maximum-flow value;
- adding a forbidden edge with zero capacity should change nothing;
- tightening a hard constraint cannot enlarge the feasible set.

Each property has hypotheses. Adding a zero-cost edge is not irrelevant, and scaling floating costs may change rounding or tie behavior.

### Reproduce an end-to-end shortest-path reduction

This program compiles a small road snapshot, omits a blocked road as a hard constraint, solves the resulting nonnegative shortest-path instance, enumerates all simple domain routes as an independent oracle, and verifies shortest-distance potentials.

<!-- bijux-verify: {"id":"domain-to-shortest-path","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"path=('depot', 'north', 'hospital') cost=7\nblocked_absent=True\noracle_cost=7 agrees=True\ncertificate=True\n","stderr":""}} -->
```python
from heapq import heappop, heappush

roads = (
    ("depot", "north", 3, True),
    ("north", "hospital", 4, True),
    ("depot", "south", 2, True),
    ("south", "hospital", 8, True),
    ("north", "south", 1, False),
)
edges = {(u, v): seconds for u, v, seconds, allowed in roads if allowed}
vertices = sorted({x for u, v in edges for x in (u, v)})

distance = {vertex: float("inf") for vertex in vertices}
distance["depot"] = 0
parent = {}
queue = [(0, "depot")]
while queue:
    value, u = heappop(queue)
    if value != distance[u]:
        continue
    for (tail, v), weight in edges.items():
        if tail == u and value + weight < distance[v]:
            distance[v] = value + weight
            parent[v] = u
            heappush(queue, (distance[v], v))

path = ["hospital"]
while path[-1] != "depot":
    path.append(parent[path[-1]])
path = tuple(reversed(path))


def enumerate_routes(u, target, visited):
    if u == target:
        yield (u,), 0
    for (tail, v), weight in edges.items():
        if tail == u and v not in visited:
            for suffix, cost in enumerate_routes(v, target, visited | {v}):
                yield (u,) + suffix, weight + cost


oracle_path, oracle_cost = min(enumerate_routes("depot", "hospital", {"depot"}), key=lambda x: (x[1], x[0]))
blocked_absent = ("north", "south") not in edges
certificate = all(distance[v] <= distance[u] + w for (u, v), w in edges.items())

print(f"path={path} cost={distance['hospital']}")
print(f"blocked_absent={blocked_absent}")
print(f"oracle_cost={oracle_cost} agrees={oracle_cost == distance['hospital']}")
print(f"certificate={certificate}")
```

The distance inequalities provide lower-bound evidence: every route telescopes to cost at least $d(\text{hospital})-d(\text{depot})=7$, and the returned path attains seven. The execution demonstrates one snapshot; it does not establish that expected seconds are accurate or time independent.

### Review algorithmic and operational complexity

Measure the generated graph, not only the domain record count. State $|V|$, $|E|$, density, numeric ranges, expected updates, memory representation, and worst-case behavior. State-expansion and time-expansion models can multiply size. An asymptotically good solver may still fail latency or memory objectives because transformation and certificate generation dominate.

Benchmark representative and adversarial distributions with recorded versions and resource limits. Separate cold parsing, transformation, solving, verification, and projection times. A successful benchmark supports the observed environment only.

### Govern deployment and change

Publish the decision specification, schema versions, transformation version, input digest, solver/version, status, witness, certificate, projection, objective, limitations, and timestamps. Retain enough data to reproduce or explain a decision without exposing prohibited sensitive data.

Monitor invalid-input rate, infeasibility, constraint slack, objective distribution, unmatched or unserved groups, certificate failures, solver limits, data age, and divergence from observed outcomes. Policy, units, feature semantics, topology, and workload changes trigger renewed model validation. A certificate remains correct for an old snapshot but cannot authorize a new decision.

### Know when to stop modeling

Stop and escalate when requirements conflict, objective ownership is unclear, authoritative data is missing, a hard constraint cannot be represented, uncertainty dominates deterministic differences, or deployment consequences exceed available validation. Returning “no justified model” is more honest than optimizing an arbitrary proxy.

## Definitions and Notation

- **purpose:** real decision and consequence the model is intended to support.
- **decision specification:** bounded choices, rules, objective, horizon, and evidence.
- **conceptual model:** domain-level entities and mechanisms.
- **formal model:** mathematical variables, constraints, and objective.
- **reduction:** instance and witness mapping between models.
- **verification:** evidence that an artifact implements its specification.
- **validation:** evidence that the specification is fit for intended use.
- **oracle:** independent source of expected results for a bounded instance.
- **metamorphic relation:** predictable relation between results of transformed inputs.
- **certificate:** compact independently checkable mathematical evidence.
- **model drift:** change that weakens correspondence between model and intended domain.

## Mechanisms, Invariants, or Proof Structure

Start with an owned decision specification, identify the dominant invariant, and select a graph family only when its assumptions match. Define a normalized schema, then prove soundness, completeness, and objective preservation. Implement transformation and projection with traceable identities. Compare tiny cases to direct domain oracles and exercise metamorphic properties. Validate solver witnesses and mathematical certificates separately from domain fitness. Bind the whole chain to versions and digests, then monitor assumptions after deployment.

## Alternatives and Trade-Offs

- **Direct domain enumeration:** excellent tiny oracle; exponential at scale.
- **Specialized graph algorithm:** strong structure and certificates; narrower modeling language.
- **Generic mathematical programming:** expressive; may lose specialized integrality and performance.
- **State expansion:** restores Markov/additive structure; can explode graph size.
- **Hard constraints:** preserve prohibitions; may reveal genuine infeasibility.
- **Penalties:** express trade-offs; require meaningful scales and cannot silently replace hard rules.
- **Exact certificates:** independently checkable; apply to the formal snapshot, not domain truth.
- **Independent solver comparison:** detects some implementation defects; shared modeling errors remain.
- **Historical replay:** tests observed cases; past data may omit future adversarial conditions.
- **Human domain review:** tests purpose and assumptions; must be named evidence, not implied peer review.

## Failure Modes and Misconceptions

- A named graph algorithm is not a decision specification.
- Correct code can optimize the wrong objective.
- Missing, zero, forbidden, and unlimited are different data states.
- Undirected, directed, static, and time-dependent relationships are not interchangeable.
- Shortest path assumes an additive route objective with algorithm-compatible weights.
- Minimum spanning tree is not a shortest route tree from one source.
- Flow assumes local conservation and divisible interchangeable units unless structure proves otherwise.
- Integrality of a base model may disappear after side constraints.
- A solver status is not an independently validated certificate.
- A graph certificate does not validate projection or domain fitness.
- Passing sampled tests is not universal proof.
- An optimal historical snapshot can be unsafe after policy or data drift.

## Worked Examples

### Example 1

**Situation.** “Choose the best supplier” lacks a metric and horizon. **Reasoning.** Cost, reliability, emissions, and lead time may conflict; no objective ownership exists. **Conclusion.** Clarify the decision before constructing vertices.

### Example 2

**Situation.** A road record lacks travel time and the importer uses zero. **Reasoning.** The missing road becomes artificially free and can dominate every route. **Conclusion.** Missing is not zero; reject, impute under policy, or mark unavailable.

### Example 3

**Situation.** A team needs pairwise compatible assignments. **Reasoning.** Bipartite matching captures agent-task conflicts, while shortest independent edges can reuse endpoints. **Conclusion.** Choose the family by the reuse invariant.

### Example 4

**Situation.** An undirected connected network needs minimum total build cost. **Reasoning.** Minimum spanning tree addresses global connection; repeated shortest paths from headquarters optimize another quantity. **Conclusion.** Similar graph vocabulary can hide different objectives.

### Example 5

**Situation.** Two commodities share link capacity. **Reasoning.** Separate maximum-flow solves can each consume the full link. **Conclusion.** Independent single-commodity models are unsound for coupled capacity.

### Example 6

**Situation.** A route has time-dependent travel where entering at 08:10 costs more than at 07:50. **Reasoning.** A static edge weight cannot represent arrival-dependent cost. **Conclusion.** Use a time-dependent or expanded-state model and prove its temporal assumptions.

### Example 7

**Situation.** Tiny exhaustive enumeration and the graph solver disagree after IDs are permuted. **Reasoning.** Objective truth should be label invariant, so ordering leaked into transformation or tie policy. **Conclusion.** Metamorphic failure exposes an implementation defect.

### Example 8

**Situation.** A matching and cover certify value 20, but projection emits 19 assignments. **Reasoning.** The graph optimum is valid; projection lost or merged an identity. **Conclusion.** Certificate and projection are distinct verification layers.

### Example 9

**Situation.** Production instances contain ten times more generated edges than benchmarks. **Reasoning.** Solver latency and memory depend on the normalized graph, not only domain rows. **Conclusion.** Monitor expansion ratios and benchmark generated distributions.

### Example 10

**Situation.** A capacity plan remains mathematically optimal after demand patterns change. **Reasoning.** The old certificate concerns the old snapshot and objective. **Conclusion.** Drift triggers data refresh and model revalidation, not certificate reuse.

## Cross-Program Connections

- **Systems Engineering:** owns requirements, hazards, acceptance criteria, and change impact.
- **Data Engineering:** owns lineage, freshness, feature computation, and missing-value semantics.
- **Software Architecture:** separates compilers, solvers, verifiers, and projectors by trust boundary.
- **Database Engineering:** provides immutable snapshots, stable identity, and reproducible queries.
- **Testing Engineering:** supplies oracles, property tests, adversarial cases, and coverage claims.
- **API Engineering:** exposes explicit status, versions, evidence, limitations, and idempotent snapshot identity.

## References

1. H. P. Williams, *Model Building in Mathematical Programming*, 5th ed., Wiley, 2013, [publisher record](https://www.wiley-vch.de/de/fachgebiete/finanzen-wirtschaft-recht/model-building-in-mathematical-programming-978-1-118-44333-0). Model construction, interpretation, and limitations.
2. R. K. Ahuja, T. L. Magnanti, and J. B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, [MIT record](https://dspace.mit.edu/handle/1721.1/49424). Network models, reductions, and applications.
3. T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, [publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/). Graph algorithms, reductions, correctness, and analysis.
4. A. Schrijver, *Combinatorial Optimization: Polyhedra and Efficiency*, Springer, 2003, [publisher record](https://link.springer.com/book/9783540443896). Graph optimization structure and polyhedral foundations.
5. M. Oral and O. Kettani, “The Facets of the Modeling and Validation Process in Operations Research,” *European Journal of Operational Research* 66(2), 1993, pp. 216–234, [doi:10.1016/0377-2217(93)90314-D](https://doi.org/10.1016/0377-2217(93)90314-D). Model, situation, decision, and validation distinctions.
6. G. Shao, C. R. McLean, A. Brodsky, and P. Ammann, “Parameter Validation Using Constraint Optimization for Modeling and Simulation,” NIST, 2009, [official record](https://www.nist.gov/publications/parameter-validation-using-constraint-optimization-modeling-and-simulation). Verification and validation lifecycle; retrieved 2026-09-05.

## Exercises

### Exercise 1

Write a decision specification for assigning emergency technicians to incidents. Identify choices, hard rules, objective order, horizon, units, and statuses before selecting an algorithm.

### Exercise 2

A team proposes minimum spanning tree for delivering one package from depot to hospital. Diagnose the mismatch and formulate the closest graph problem, including weight assumptions and a certificate.

### Exercise 3

Design oracle and metamorphic tests for a domain-to-bipartite-matching transformation with eligibility, one-use endpoints, and duplicate source records.

### Exercise 4

Compare a specialized flow reduction with generic integer programming for indivisible placement with host capacity, rack anti-affinity, and fixed activation costs.

### Exercise 5

An optimization API returns “optimal,” a decision list, and cost. Design an evidence-bearing production contract and review process that can detect data, transformation, solver, projection, and drift failures.

## Answers to the Exercises

### Answer 1

Decision: every five minutes, assign available qualified technicians to active incidents. Hard rules: one simultaneous incident per technician, required certification, travel-time reachability before deadline, working-hours compliance, and no assignment of stale/unavailable staff. Objective is lexicographic: maximize incidents meeting safety priority, then minimize predicted arrival seconds, then apply a declared stable tie-break. Inputs carry technician, incident, certification, location, availability, deadline, priority, and snapshot identities with seconds as the travel unit. Statuses include invalid input, infeasible full coverage, optimal partial assignment, time limit, and stale snapshot. This suggests matching or min-cost flow only after capacity, time, and priority semantics are validated.

### Answer 2

A minimum spanning tree minimizes the total weight needed to connect every vertex; it does not minimize one depot-hospital route. Use shortest path on a directed or undirected road graph. Edge weight must represent an additive quantity such as static nonnegative travel seconds; restrictions remove edges. Return a valid path and cost plus distance labels satisfying $d(v)\le d(u)+w(u,v)$ for every edge and equality along the returned path from source distance zero. If travel time depends on arrival time, use a time-dependent algorithm under a FIFO assumption or a time-expanded state model rather than static shortest path.

### Answer 3

For tiny sets, enumerate all subsets of eligible pairs, reject endpoint reuse, and compute maximum size; compare with the transformed solver after deduplicating logical pairs under documented provenance rules. Include empty sides, isolated vertices, one pair, complete graphs, Hall-deficient groups, repeated identical records, conflicting endpoint identities, and multiple optima. Metamorphic tests permute IDs, reorder records, duplicate an already-present logical edge, add an isolated vertex, and remove eligibility; objective should remain invariant for the first four transformations and cannot increase after removal. Directly validate every projected pair and endpoint count.

### Answer 4

Flow handles divisible scalar capacity and some anti-affinity via quota gadgets, but fixed host activation cost is not linear per unit, and indivisible heterogeneous placements may not project from scalar integral flow. Gadget expansion may also be large. Integer programming expresses binary placement and activation, multidimensional host capacity, per-rack limits, and activation implication directly, at the cost of harder solving and certificates usually expressed as bounds/gaps rather than a simple cut. Use flow only if objects and resources reduce honestly to interchangeable integral units and fixed costs can be removed; otherwise prefer the integer model and independently validate feasibility and objective.

### Answer 5

The contract should include schema and transformation versions, canonical input digest and timestamp, objective and units, explicit status, solver/version and resource limits, normalized graph digest, graph witness, feasibility residuals, certificate or lower/upper bounds, projected domain decisions, recomputed cost, tie policy, and limitations. Reviewers validate input provenance, trace generated elements to domain records, check the witness and certificate independently, and recheck projected decisions against original rules. Tiny oracle, metamorphic, adversarial, replay, and performance tests cover implementation risks. Production monitoring tracks invalid data, infeasibility, certificate failure, expansion, latency, objective and constraint distributions, data age, and outcome drift. External domain approval must be named rather than implied.
