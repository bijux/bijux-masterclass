# Glossary — API Performance, Capacity, and Traffic Engineering

Use this glossary alongside `program-book/glossary.md`. Program terms keep one meaning across all six courses; the entries below add course-specific distinctions.

**Admission control** — deciding whether new work may enter a bounded system.

**Arrival rate** — new work offered per unit of time, conventionally written λ.

**Backpressure** — a mechanism by which downstream capacity constrains upstream production.

**Benchmark envelope** — the complete machine-readable record of workload, environment, correctness, measurements, and identity needed to interpret a run.

**Capacity** — the maximum demand a system can serve while meeting stated correctness and service objectives in a stated environment.

**Closed workload model** — a fixed or bounded population issues a new request after completing or waiting between previous requests; slowdown reduces generated arrival rate.

**Coordinated omission** — a measurement error in which the load generator does not record requests that should have arrived while the system was slow.

**CPU time** — processor time consumed by the process; different from elapsed wall time.

**Event-loop delay** — delay before scheduled event-loop work can run, often caused by synchronous blocking or overload.

**Headroom** — usable capacity intentionally retained above forecast demand.

**Little’s Law** — for a stable system over a compatible interval, average work in the system equals arrival rate multiplied by average time in the system: `L = λW`.

**Load shedding** — rejecting or degrading work before it consumes a resource needed by more valuable or already admitted work.

**Nearest-rank quantile** — the sorted observation at rank `ceil(p × n)` for quantile `p`.

**Open workload model** — arrivals occur according to an external schedule independent of response completion.

**Performance budget** — a versioned bound on latency, throughput, error, queueing, or resource use for a named workload.

**Saturation** — the state in which a resource has no useful spare capacity and additional demand primarily creates waiting or rejection.

**Service demand** — resource time required by one unit of work at a particular resource.

**Tail latency** — latency in the slower part of a distribution, commonly p95 or p99.

**Throughput** — completed work per unit of time. Offered load, admitted load, and completed throughput are distinct.

**Utilization** — fraction of a resource’s capacity in use over an interval.

**Workload identity** — a stable identifier plus content hash for the complete workload definition.
