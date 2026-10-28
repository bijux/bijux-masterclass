---
module_id: DE-015
program: Data Engineering
level: 1
module_number: 15
title: Snapshot and Accumulating Fact Tables
status: complete
last_verified: 2026-09-02
---

# Snapshot and Accumulating Fact Tables

## One-Page Review

### Governing question

When should a process be modeled as event transactions, periodic observations, or one evolving workflow row—and which time, density, additivity, mutation and reconciliation rules make each representation trustworthy?

### Essential definitions

- A **transaction fact** records one measurement event at a point in business time and usually exists only when the event occurs.
- A **periodic snapshot fact** records state or summarized activity for every governed entity combination at a regular period/cutoff grain.
- An **accumulating snapshot fact** records one process instance and is updated as predictable milestones occur.
- A **stock** is state at an instant, such as closing inventory. A **flow** is change during an interval, such as receipts and shipments.
- A **snapshot cutoff** defines the business instant and timezone at which state is observed; a period label alone is insufficient.
- A **dense snapshot** emits all expected entity-period combinations, including zero/inactive rows under policy. A **sparse snapshot** emits only observed or active combinations.
- A **milestone role** is a separately named date/time foreign key or timestamp for a workflow stage, such as opened, approved or closed.
- A **lag/duration fact** measures elapsed time between declared milestones under calendar or business-clock rules.
- A **restatement** replaces/reissues a snapshot or workflow state after late or corrected evidence, with version/audit semantics.
- A **timespan accumulating snapshot** versions workflow state over effective intervals when historical pipeline state must be directly queryable.

### Central model, mechanism, or theorem

Let $B_{g,t}$ be a periodic stock for governed entity group $g$ at cutoff $t$, and let signed flows during $(t_0,t_1]$ be $\Delta_{g,e}$. With all adjustments and boundary rules included,

$$
B_{g,t_1}=B_{g,t_0}+\sum_{e\in(t_0,t_1]}\Delta_{g,e}.
$$

This is a reconciliation invariant, not permission to sum snapshots through time. For an accumulating row with milestone instants $m_0,\ldots,m_k$, each applicable forward transition should satisfy $m_{i+1}\geq m_i$ and duration $d_i=m_{i+1}-m_i$ under the declared clock. Skips, repeats, reopenings and reversals require explicit workflow policy rather than forced monotonicity.

### Critical invariants

- Each table declares transaction, periodic snapshot or accumulating snapshot grain independently.
- Snapshot period, cutoff instant, timezone, density and missing-row semantics are explicit.
- Stock measures have declared aggregation rules across entities and time; repeated balances are not summed accidentally.
- Snapshot rows are unique at the complete entity-period grain and reconcile to authoritative state or flows.
- An accumulating row is unique per governed process instance, not per milestone event.
- Milestone date roles, not-applicable/not-yet-known states and duration clocks are distinct.
- Workflow updates are idempotent, order-aware and atomically published.
- Repeated, skipped, out-of-order, reopened and canceled workflows have modeled behavior.
- Transaction facts remain available when event sequence/audit cannot be recovered safely from snapshots.
- Late events and corrections follow versioned restatement rules with affected-period evidence.

### Common failures

Calling every daily table a snapshot; using ingestion date as cutoff; storing only a date label; summing balances over days; treating absent sparse rows as zero; building a dense Cartesian product without eligibility rules; carrying stale state forward invisibly; mixing daily and monthly rows; replacing transaction history with snapshots; using one generic milestone date; storing zero instead of not-yet-reached; computing elapsed hours without timezone/business calendars; overwriting accumulating rows without audit; assuming workflow order is universal; losing repeated/reopened stages; generating new rows for retries; applying late events only to today's snapshot; confusing a database table snapshot with a periodic fact; and claiming grand-total reconciliation proves row-level completeness.

### Compact example

Inventory opens at 10 units. Four signed movements, +5, -2, -4 and +1, yield daily closing snapshots 13 and 10. The final balance reconciles as $10+5-2-4+1=10$; summing the two closing balances produces 23 unit-days, not closing inventory. Separately, a claim opened on day 1, approved on day 3 and closed on day 6 has approval lag 2 and cycle lag 5 under an integer-day teaching clock. A second open claim has missing future milestones, not zero dates.

### Connections

[DE-011](011-grain-and-the-meaning-of-a-row.md) defines transaction/snapshot grain, [DE-012](012-facts-dimensions-and-measures.md) classifies stock and flow, [DE-013](013-star-and-snowflake-schemas.md) defines dimensional paths, and [DE-014](014-slowly-changing-dimensions.md) supplies interval/history semantics. Planned DE-016 develops event/activity models and appears in the [Data Engineering roadmap](../ROADMAP.md). Workflow correctness connects to [Systems Engineering](../../26-systems-engineering/ROADMAP.md), event ordering to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and reliable publication to [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

Can a model owner point to one row and say whether it means “an event happened,” “this state held at this cutoff,” or “this process instance has reached these milestones”—then prove how it behaves when time advances or evidence arrives late?

These fact types are complementary, not maturity levels. A transaction table preserves event detail. A periodic snapshot makes regular state/trend questions direct. An accumulating snapshot makes pipeline progress and milestone lags direct. One process may need all three because no single grain answers every question safely.

The [Kimball transaction-fact guidance](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/transaction-fact-table/) defines a row as a measurement event at a point in space and time. The [periodic snapshot guidance](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/periodic-snapshot-fact-table/) makes the period itself the grain. The [accumulating snapshot guidance](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/accumulating-snapshot-fact-table/) uses one row per predictable workflow instance and revisits that row as milestones occur.

The correct choice begins with the business question. “How many shipments happened?” asks for events. “What was inventory at each day-end?” asks for periodic state. “Where are orders in fulfillment and how long between stages?” asks for accumulating progress. Modeling all three as generic “daily facts” destroys these distinctions.

## Why This Matters

Stock and flow have different algebra. Receipts can be summed across days; end-of-day inventory usually cannot. If both are numeric columns without measure contracts, a dashboard can return a plausible but meaningless monthly total.

Periodic snapshots make absence explicit only when density is defined. In a dense account-day table, an expected missing row is a quality defect. In a sparse active-account table, absence might mean inactive, zero, unknown or failed extraction. Consumers need the rule before interpreting counts.

Accumulating snapshots trade append-only simplicity for query convenience. One claim row with opened, reviewed and closed milestones supports backlog and cycle-time analysis without reconstructing every transition. Updates, however, must handle retries, late events, repeated stages and reopenings without corrupting sequence.

Transactions preserve forensic detail but can be expensive to replay for state at every cutoff. Snapshots materialize that state and freeze business calendars/cutoffs. Reconciliation between them detects lost, duplicated or misclassified movements.

Operational table time travel is not the same as an analytical periodic fact. A storage snapshot captures bytes or table state for recovery. A periodic fact applies business grain, eligibility, units, dimensions and cutoff rules. Confusing them leaves business semantics undefined.

## Prerequisites and Retrieval

Retrieve the business process and row grains; source event identities; event, effective and ingestion timestamps; source ordering/sequence; signed movements and reversals; state source and authoritative controls; entity eligibility periods; desired snapshot cadence; business cutoff and timezone; holiday/business calendar; dense/sparse policy; zero/null/missing distinctions; late-arrival distribution; correction/restatement rules; retention horizon; existing transaction history; process-instance identity; workflow definition and version; milestone names and roles; optional/skipped/repeated/reopened paths; terminal and canceled states; expected stage order; service-level clocks; pause/wait intervals; current status derivation; dimension keys at each milestone; slowly changing dimension resolution; update concurrency; idempotency key; snapshot/build watermark; atomic publication mechanism; partitioning/clustering; common trend/backlog/cohort queries; aggregate semantics; reconciliation tolerances; security/privacy retention; and downstream refresh dependencies.

Distinguish event from state; transaction from transaction-date aggregate; point-in-time stock from interval flow; observation cutoff from load completion; snapshot period from event period; dense from sparse; zero from no row, null and not applicable; carry-forward from measured state; calendar time from business time; event date from each milestone role; process instance from event occurrence; current accumulating state from historical workflow state; update from correction; late event from late snapshot production; retry from repeated business milestone; reopen from duplicate; terminal from inactive; derived snapshot from source-native state; snapshot fact from storage/table snapshot; versioned snapshot from overwritten row; and grand-total equality from row-level preservation.

Build small timelines before schema DDL. Include an entity with no activity but nonzero state, a zero state, a missing source observation, exact cutoff events, late movement, negative correction, workflow with skipped stage, repeated review, cancellation, reopening and two events with the same timestamp. Hand-compute expected events, snapshots, backlog and durations.

## Learning Objectives

After completing this module, you should be able to:

1. choose transaction, periodic snapshot and accumulating snapshot facts by business question;
2. declare period/cutoff, density and state-versus-flow semantics;
3. classify snapshot measures by valid aggregation dimensions;
4. reconcile stock snapshots to signed event flows;
5. model workflow milestone roles and duration facts;
6. handle partial, skipped, repeated, canceled and reopened processes;
7. implement idempotent snapshot builds and accumulating updates;
8. manage late evidence, corrections and historical restatement;
9. test and observe uniqueness, completeness, order and reconciliation; and
10. combine complementary fact tables without mixing their grains.

## Core Exposition

### Choose by row proposition

Start every design with “one row per …”. A transaction might be one inventory movement. A periodic snapshot might be one product-location at local day-end. An accumulating snapshot might be one fulfillment line across its lifecycle.

Do not choose based on source table shape. A mutable source order row may encode current workflow state, while its change log contains transactions. A daily export may be a source snapshot but still need eligibility and cutoff modeling.

Write inclusion rules, identity, time and units for each candidate fact independently.

### Understand transaction facts

Transaction facts are sparse in time: rows appear when events occur. They retain atomic dimensional context and typically append, with corrections represented by governed updates or adjustment events.

They answer sequence, volume, exact-time and audit questions. Additive signed flows can be summed across time when units and population agree.

Events alone may derive state only if history is complete, ordered, interpretable and begins from a known baseline.

### Understand periodic snapshots

A periodic snapshot summarizes state or activity over a standard day, week, month or other interval. Its grain includes the governed dimensions plus the period/cutoff identity.

The row may contain closing balance, active count, cumulative-to-date value and interval activity components. Each measure needs independent additivity rules.

The period label must resolve to an exact business interval/cutoff. “2026-09-01” could mean start, end, local midnight or reporting day.

### Understand accumulating snapshots

An accumulating snapshot represents one bounded workflow instance and carries multiple milestone date/time roles. It is inserted near process start and updated as stages occur.

Typical facts include milestone-completion indicators and durations between opened, accepted, shipped and closed. Future milestones use explicit not-yet-reached/not-applicable members or null semantics agreed with the semantic layer.

It works best for predictable, finite workflows. Highly branching, repeating or unbounded processes may need event facts plus derived current-state views.

### Treat the fact types as complementary

The [Kimball complementary-fact discussion](https://www.kimballgroup.com/2014/06/design-tip-167-complementary-fact-table-types/) argues that transaction, periodic and accumulating facts can each serve a distinct view of one process.

For claims, event facts preserve every status change; a daily periodic snapshot gives backlog by state; an accumulating row gives current milestones and cycle lags. Shared conformed dimensions let summaries compare without joining atomic rows directly.

Choose the minimal combination that answers required questions and can be reconciled.

### Define the periodic grain precisely

“One row per account per day” is incomplete. Specify active/eligible account, currency, balance type, legal entity, local business day and cutoff after accepted postings.

If snapshots are monthly, decide calendar versus fiscal period and whether month-end means final calendar instant, final business-day close or regulatory cutoff.

Partitioning date is physical metadata; it does not replace business snapshot date.

### Define snapshot cutoff and timezone

A cutoff is an instant or fully specified interval boundary. Resolve local timezone and daylight-saving transitions using the business calendar.

State whether an event exactly at cutoff belongs to the ending or following snapshot. A half-open convention such as $(t_0,t_1]$ for movements must agree with snapshot selection.

Record source watermarks and observation freshness. A snapshot completed at 02:00 can still represent prior day 23:59:59.999... under policy.

### Choose dense or sparse periodic capture

Dense snapshots produce every eligible entity-period combination. They simplify absence and zero analysis but can grow as entity cardinality times periods.

Sparse snapshots reduce rows by emitting active/changed/nonzero combinations. They require explicit interpretation of absence and often a coverage table to distinguish zero from missing.

Never densify the Cartesian product of all dimension members blindly. Eligibility intervals and compatible combinations define expected rows.

### Separate stock from flow

Stock is measured at a cutoff; flow accumulates over an interval. Inventory closing balance is stock. Receipts, shipments and adjustments are flows.

Stock can often be summed across products or locations at one instant, subject to unit compatibility. It is semi-additive across time. Flow is often additive across time.

Name units: units, unit-days, currency, account-days. Summing daily balance deliberately computes exposure, not closing balance.

### Derive snapshots from events

Given known opening state and complete signed events, derive closing state by cumulative sum under boundary and ordering rules.

Events need stable identity, exact sign, effective time, unit and correction semantics. Duplicate or missing movements corrupt every subsequent state.

Persist snapshot lineage: opening checkpoint, event interval, event count/digest, rule version and output cutoff.

### Capture source-native state

Sometimes the source provides authoritative end-of-period state independent of movements. Load it as an observation with source timestamp/version.

Compare derived and observed state when both exist. Differences can reveal unmodeled adjustments, late events, cutoff mismatch or source errors.

Do not silently force one to equal the other. Record reconciliation difference and resolution.

### Apply state–flow reconciliation

For compatible units and population:

$$
\text{closing}=\text{opening}+\text{inflow}-\text{outflow}+\text{adjustments}.
$$

Reconcile per full grain and rollup. Grand totals can hide one duplicated and one missing entity.

Define tolerance only for justified rounding/measurement uncertainty. Integer unit counts should usually match exactly.

### Govern semi-additive snapshot measures

For a requested time range, specify last-valid, first, minimum, maximum, average daily, duration-weighted average or change. Do not leave the BI tool to choose sum.

Last-valid requires freshness and tie-break rules. Average daily requires a denominator policy for missing days. Duration-weighted exposure needs validity intervals.

Retain numerator/denominator components for averages and rates in periodic rows.

### Avoid double-counting cumulative fields

A snapshot may carry month-to-date or lifetime totals. These already accumulate through time and must not be summed across consecutive snapshots.

Use the last applicable cumulative value or compute changes. Label fields with their window and reset behavior.

Reconcile cumulative change to interval activity, accounting for resets and corrections.

### Define accumulating process identity

Choose the stable workflow instance: claim, application, order line, shipment or support case. Retries and milestone messages update the same instance when they represent the same business progression.

One customer can have many processes; customer ID is not enough. Reopened work may remain one instance with cycles or create a successor instance under policy.

Enforce one current accumulating row per instance unless using an explicitly versioned timespan form.

### Define milestone roles

Name each date/time role by event: `opened_at`, `approved_at`, `shipped_at`, `closed_at`. Keep business time distinct from loaded time.

If users group by calendar attributes, resolve each role to a date dimension key. Retain precise timestamps for duration when required.

Not-yet-reached, skipped, not-applicable and unknown are different. A zero date or generic null can erase this distinction.

### Compute milestone durations

For adjacent milestones $m_i,m_j$, elapsed duration is $m_j-m_i$ under a declared clock. Calendar elapsed time differs from business hours that exclude weekends, holidays or paused states.

Negative duration may signal out-of-order evidence, clock error, backdated correction or valid domain behavior. Classify before rejection.

PostgreSQL's current [window-function documentation](https://www.postgresql.org/docs/current/functions-window.html) includes `lag` and `lead`, useful for deriving adjacent event intervals. Deterministic ordering still needs a unique tie-breaker.

### Handle optional and skipped stages

Not every process visits every milestone. Model applicability from workflow type/version and status, not from null alone.

Durations can span the next actually reached milestone or remain defined only for named pairs. Do not quietly reinterpret `approval_to_ship` when approval is skipped.

Completion counters and status dimensions help distinguish pending from skipped.

### Handle repeated stages

An accumulating row with one `reviewed_at` cannot represent three review cycles. Decide whether to store first, last, current-cycle or a summary count/duration.

Keep the event transaction table for every occurrence. If repeats are analytically important, add a stage-cycle fact at `(process,stage,occurrence)` grain.

Document which occurrence populates each accumulating milestone.

### Handle reopenings

Reopening can clear terminal status, add another cycle or create a successor process. Overwriting the original closed timestamp destroys prior cycle evidence.

For one-row current progress, retain first/last close, reopen count and current cycle as governed fields while events preserve all transitions.

If each cycle is independently measured, use cycle identity in a separate accumulating or transaction fact.

### Handle out-of-order events

Ingestion order is not workflow order. Use source sequence, event/effective time and precedence rules. Buffer or recompute state within an allowed lateness window.

An approval event arriving after shipment processing may still have an earlier business time. Update milestones and recalculate derived durations atomically.

Conflicting same-precedence events require quarantine or deterministic domain resolution, not arbitrary arrival order.

### Make accumulating updates idempotent

Identify each source event and process instance. Reprocessing the same event must not increment counts or change milestones again.

Use compare-and-set/version checks or deterministic rebuild from events to avoid concurrent lost updates. Store source watermark/version and row digest.

Test replay, reordered batches and concurrent updates for the same instance.

### Publish workflow state atomically

Milestones, status, duration facts and audit/version metadata form one row contract. Consumers should not see a new close date with stale cycle duration.

Use database transactions, atomic table swaps or snapshot commits supported by the platform. Validate the candidate before promotion.

If semantic aggregates depend on the row, refresh or invalidate them as part of the publication contract.

### Preserve workflow history when required

A standard accumulating snapshot exposes current/final process state, not every state previously published. Pair it with transaction events for audit.

When analysts need “pipeline as known/valid on date,” use periodic snapshots or a timespan accumulating design with effective/expiration intervals.

The [Kimball timespan accumulating guidance](https://www.kimballgroup.com/2012/05/design-tip-145-time-stamping-accumulating-snapshot-fact-tables/) describes versioning changed pipeline rows and pairing accumulating state with transaction events. This adds Type 2-like interval complexity.

### Handle late transaction events

A late movement effective for a closed snapshot period can alter every downstream balance. Define the maximum correction horizon and whether snapshots are restated or adjustment facts are applied prospectively.

If restating, rebuild from the nearest trusted checkpoint, issue new snapshot versions and identify affected reports. Preserve prior published evidence if reproducibility requires it.

Do not insert the event into today's flow solely to avoid backfill; that changes period meaning.

### Handle late snapshot production

A snapshot generated late can still represent its intended cutoff if source data are complete to that watermark. Production time and business cutoff are distinct.

Track scheduled cutoff, actual build time, source high-water marks, completeness and version. Consumers can assess freshness without confusing it with state time.

If the source could not reconstruct the cutoff, label the observation estimated/incomplete rather than backdating current state.

### Handle corrections and restatements

Choose overwrite, append version, or correction-delta policy. Overwrite is simple but loses what was published before. Append versions retain audit and require current-version selection.

Restatement reason, source evidence, actor/process, affected period and previous digest should be recorded.

Reconcile changed entity-period keys, not only net total movement.

### Distinguish storage snapshots

Google Cloud's [BigQuery table-snapshot documentation](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro) defines a read-only point-in-time copy of a physical table. Similar platform features support backup, recovery and reproducibility.

They do not establish a periodic fact's business grain, dense population, cutoff, measures or additivity. A physical snapshot can preserve the bytes of an incorrectly modeled table.

Use storage snapshots as operational evidence where helpful, while building analytical snapshots from explicit contracts.

### Load periodic snapshots reproducibly

Resolve one run to an immutable input set and business cutoff. Generate expected eligible keys, join observed/derived state, classify missingness and enforce uniqueness.

Partition output by snapshot period but include complete grain keys. Use deterministic formulas and stable dimension resolution.

Before publish, compare row/key sets, source watermarks, control totals and state–flow identities. A rerun from the same inputs should produce the same semantic rows.

### Load accumulating snapshots reproducibly

Stage new workflow events, deduplicate by event identity, order deterministically and apply transition policy to existing process state or rebuild it.

Validate allowed transitions, milestone order, status, duration, dimension resolution and source version. Detect concurrent target changes before commit.

Publish the new row version atomically and retain change evidence. Replaying the same event set should be a no-op.

### Partition and cluster by access pattern

Periodic snapshots often partition by snapshot date and cluster by high-use entity dimensions. Accumulating rows may be accessed by open status, milestone date and process identity.

Partitioning mutable accumulating tables by a milestone that changes can cause expensive relocation or skew. Evaluate platform behavior.

Physical layout follows measured pruning, scan, update and concurrency patterns while preserving semantic keys.

### Test periodic snapshots

Test full-grain uniqueness, expected dense/sparse key coverage, cutoff/timezone, zero/null/missing states, dimension resolution and measurement units.

Test stock–flow reconciliation from trusted openings and signed movements. Compare observed versus derived state and classify differences.

Test last-value/average/change measures across one period, multiple periods, missing periods and mixed units.

### Test accumulating snapshots

Test one row per process instance, allowed status transitions, milestone applicability, temporal order, deterministic duration and correct current/final state.

Test retries, duplicate messages, out-of-order delivery, same-time ties, skips, repeats, cancellation, reopening and late correction.

Compare accumulating milestone summaries with the authoritative transaction-event sequence.

### Observe both models

For periodic facts, monitor expected/actual row coverage, late builds, stale observations, null/zero rates, restatement volume and reconciliation differences.

For accumulating facts, monitor open age, stage backlog, impossible transitions, negative lags, duplicate instances, update conflicts, skipped/reopened rates and event-summary mismatches.

Slice by source, workflow version, timezone and special-member class. Global health can hide one broken population.

### Evolve fact types safely

Changing daily to hourly snapshot grain, sparse to dense policy, cutoff timezone or milestone semantics is a breaking change. Version tables/measures or dual-publish.

Adding an accumulating snapshot from existing events is feasible only if event identity, completeness and ordering support deterministic reconstruction. State limitations explicitly.

Before retiring a fact type, inventory consumers and prove required questions remain answerable. Complementary facts should not be removed solely because their totals agree.

## Definitions and Notation

Let transaction event set $E$ contain events $e$ with identity $id(e)$, entity grain $g(e)$, effective time $t(e)$ and signed flow $\Delta(e)$ in declared units.

For consecutive cutoffs $t_0<t_1$, the state–flow relation is

$$
B(g,t_1)-B(g,t_0)=\sum_{e:g(e)=g,\ t_0<t(e)\leq t_1}\Delta(e)+A(g,t_0,t_1),
$$

where $A$ contains only explicitly modeled adjustments not represented as ordinary events. The residual

$$
R=B(g,t_1)-B(g,t_0)-\sum\Delta(e)-A
$$

should be zero or within a declared measurement tolerance.

A periodic row key is $K_P=(g,p,c,v)$: entity/dimension grain $g$, period $p$, cutoff contract $c$ and optional snapshot version $v$. A standard current-only accumulating row key is $K_A=q$, the durable process-instance identity.

Let milestone vector $M(q)=(m_0,\ldots,m_k)$ with applicability $a_i(q)$ and completion $z_i(q)$. Duration $d_{ij}=C(m_i,m_j)$ uses clock function $C$, which may represent elapsed or governed business time. Missing $m_j$ is not numeric zero.

For a forward-only workflow and applicable completed adjacent milestones, require $m_{i+1}\geq m_i$. Repeated/reopened workflows require an occurrence/cycle index or another policy; collapsing them into one vector loses sequence information.

## Mechanisms, Invariants, or Proof Structure

Use this mechanism for every snapshot design:

1. Select the process and write separate transaction, periodic and accumulating row propositions.
2. Inventory event identity/order, authoritative state, workflow stages and consumer questions.
3. Choose the minimal complementary fact types that preserve required evidence.
4. Define period, exact cutoff, timezone, inclusion boundaries and calendar.
5. Define dense/sparse eligibility and zero/null/no-row semantics.
6. Classify stock, flow, cumulative, ratio and duration measures by aggregation.
7. Define workflow instance identity, milestone roles, optionality, repeats and reopenings.
8. Resolve dimensions and SCD versions at the correct event/cutoff/milestone time.
9. Implement deterministic, idempotent transaction ingestion and snapshot derivation.
10. Publish periodic rows and accumulating updates atomically with run/version evidence.
11. Reconcile stock to flows and accumulating rows to event sequences.
12. Apply late/correction/restatement policy from trusted checkpoints.
13. Test uniqueness, coverage, boundary time, transition and aggregation adversaries.
14. Monitor freshness, residuals, restatements, backlog and impossible states.
15. Version changes to grain, cutoff, density, workflow or measure contracts.
16. Retain lineage, rollback and consumer acceptance evidence.

The executable fixture uses integer day positions and exact unit flows. It demonstrates algebra and milestone state, not a real calendar, database or distributed update protocol.

<!-- bijux-verify: {"id":"snapshot-workflow-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"event_count=4\nclosing_balance=10\nsummed_balances=23\nstate_flow_reconciles=True\nprocesses=2\ncompleted=1\nopen=1\napproval_lags=[2]\ncycle_lags=[5]\nmilestone_order_valid=True\n","stderr":""}} -->
```python
opening_balance = 10
movements = (
    {"day": 1, "delta": 5},
    {"day": 1, "delta": -2},
    {"day": 2, "delta": -4},
    {"day": 2, "delta": 1},
)
snapshots = {1: 13, 2: 10}
processes = (
    {"id": "C1", "opened": 1, "approved": 3, "closed": 6},
    {"id": "C2", "opened": 2, "approved": None, "closed": None},
)

closing_balance = opening_balance + sum(event["delta"] for event in movements)
approval_lags = [row["approved"] - row["opened"] for row in processes if row["approved"] is not None]
cycle_lags = [row["closed"] - row["opened"] for row in processes if row["closed"] is not None]
milestone_order_valid = all(
    (row["approved"] is None or row["opened"] <= row["approved"])
    and (row["closed"] is None or row["opened"] <= row["closed"])
    and (row["approved"] is None or row["closed"] is None or row["approved"] <= row["closed"])
    for row in processes
)

print("event_count=" + str(len(movements)))
print("closing_balance=" + str(closing_balance))
print("summed_balances=" + str(sum(snapshots.values())))
print("state_flow_reconciles=" + str(closing_balance == snapshots[2]))
print("processes=" + str(len(processes)))
print("completed=" + str(sum(row["closed"] is not None for row in processes)))
print("open=" + str(sum(row["closed"] is None for row in processes)))
print("approval_lags=" + str(approval_lags))
print("cycle_lags=" + str(cycle_lags))
print("milestone_order_valid=" + str(milestone_order_valid))
```

Critical invariants are:

- **Grain:** each fact type has one explicit event, entity-period or process-instance proposition.
- **Cutoff:** snapshot time, timezone, boundary and source watermark are fixed.
- **Coverage:** dense/sparse expected keys and missing meanings are testable.
- **Additivity:** stock, flow, cumulative and duration measures expose valid operators.
- **Reconciliation:** closing state equals opening plus complete signed flow and governed adjustments.
- **Workflow identity:** retries update the intended process rather than create duplicates.
- **Milestones:** roles, applicability, order, occurrence and clock semantics are explicit.
- **Atomicity:** derived state, status, durations and audit metadata publish consistently.
- **History:** late/corrected state retains required prior publication evidence.
- **Complementarity:** event and snapshot facts reconcile without being joined at incompatible grains.

**Proof sketch — stock–flow telescoping across consecutive periods.** Suppose every consecutive pair satisfies $B_t=B_{t-1}+F_t$, where $F_t$ is the complete signed flow (including governed adjustments) for period $t$. Summing differences from $1$ through $n$ gives $\sum_t(B_t-B_{t-1})=\sum_tF_t$. Intermediate balances cancel, leaving $B_n-B_0=\sum_tF_t$, so $B_n=B_0+\sum_tF_t$. This proves final-state reconciliation under completeness and consistent boundaries; it does not make $\sum_tB_t$ a closing balance.

## Alternatives and Trade-Offs

**Transaction versus periodic snapshot.** Transactions preserve atomic events and flexible intervals but require replay for state. Periodic snapshots answer trend/state questions directly but discard within-period sequence unless paired with events.

**Periodic versus accumulating snapshot.** Periodic rows track every entity/process at each cutoff; accumulating rows track one lifecycle current/final state. Historical backlog usually favors periodic/timespan data; current cycle-time favors accumulating.

**Dense versus sparse periodic.** Dense capture makes expected absence visible and rates easier, at high row volume. Sparse capture reduces volume but demands eligibility/coverage semantics.

**Observed versus derived state.** Observed state follows source authority; derived state provides lineage to events. Keeping both enables reconciliation but creates two measures that must be named.

**Overwrite versus versioned snapshot.** Overwrite simplifies current queries but loses prior publication. Versioning supports audit/reproducibility at storage and selection cost.

**Mutable accumulating row versus rebuild.** Incremental updates are efficient but vulnerable to ordering/concurrency bugs. Deterministic rebuild from events is robust when event history is complete, at compute cost.

**Standard versus timespan accumulating.** Standard rows expose latest/final milestones simply. Timespan versions make historical pipeline states direct but add interval growth and Type 2-like joins.

**Calendar versus business duration.** Calendar duration is reproducible from timestamps. Business duration better represents service expectations but depends on versioned calendars, pauses and timezone rules.

**Null versus special milestone member.** Null is compact but ambiguous. Special date/status members express not-yet/not-applicable/unknown clearly but need semantic-tool support and must not enter arithmetic.

**Restate versus prospective adjustment.** Restatement improves past valid-time truth but changes reports. Prospective adjustments preserve closed reports but shift activity. Choose and label by governance requirements.

**Physical table snapshot versus analytical snapshot fact.** Physical snapshots help recovery and byte-level history. Analytical snapshots encode business grain/measures. They can complement but cannot substitute for each other.

**One fact versus complementary facts.** One table is simpler operationally but may force expensive reconstruction or information loss. Multiple facts add pipelines and reconciliation while keeping each row meaning clean.

## Failure Modes and Misconceptions

- **“A dated table is a periodic snapshot.”** The row must represent governed state/summary at a cutoff grain.
- **“Snapshot date equals load date.”** Business cutoff and production time differ.
- **“Daily means midnight UTC.”** Business timezone/cutoff may differ.
- **“Balances are additive because they are numbers.”** They are generally semi-additive across time.
- **“Sum of snapshots is closing state.”** It usually produces a state-time exposure unit.
- **“No sparse row means zero.”** It can mean inactive, ineligible, missing or failed capture.
- **“Dense means every Cartesian combination.”** Only governed eligible combinations are expected.
- **“Carry-forward is observation.”** It is an imputation that needs freshness and lineage.
- **“Grand totals prove reconciliation.”** Offsetting key-level defects can hide.
- **“Transactions always reconstruct state.”** Opening state, completeness and correction semantics are required.
- **“Snapshots replace transactions.”** They omit within-period events and sequence.
- **“An accumulating snapshot is append-only.”** Standard rows are revisited as milestones arrive.
- **“One row per customer is a workflow.”** Process-instance identity is required.
- **“Null milestone means pending.”** It might be skipped, unknown or not applicable.
- **“Zero date is a safe sentinel.”** It can group/arithmetic as a real date.
- **“Every workflow is monotone.”** Repeats, regressions and reopenings exist.
- **“Latest arrival defines milestone order.”** Effective/source order can differ.
- **“A retry is a new milestone.”** Stable event identity should make it a no-op.
- **“Negative lag is always bad data.”** It can expose backdating, clocks or allowed sequence.
- **“Elapsed hours equal service hours.”** Business calendars and pauses change the clock.
- **“Updating close date alone is sufficient.”** Status, durations and audit must agree atomically.
- **“Current accumulating state provides history.”** Prior overwritten states are absent without events/versions.
- **“Late events belong in today's period.”** Effective-time meaning must be preserved or explicitly adjusted.
- **“A storage snapshot is a business snapshot.”** Physical point-in-time bytes lack analytical contracts.
- **“Matching final balance validates every day.”** Intermediate snapshot errors can cancel.
- **“Same period label means compatible grain.”** Dimensions, cutoff and density must also align.

## Worked Examples

### Example 1

A warehouse stores every inventory movement and an end-of-day product-location balance. Receipts and shipments sum through time; closing balance does not.

Each daily snapshot records local cutoff, source watermark and version. Product-location reconciliation compares opening plus signed movements to closing exactly. Monthly reports use last-valid closing and sum interval flows separately.

### Example 2

A bank creates rows only for accounts with transactions. An account with a 100 balance and no activity disappears from the daily table, understating deposits.

The design uses eligible open-account coverage and emits a dense account-day closing snapshot, or explicitly carries source-observed state with freshness. Zero, missing and closed accounts remain distinct.

### Example 3

An order fulfillment accumulating row has placed, picked, shipped and delivered roles. Some digital products skip pick/ship.

Workflow type determines milestone applicability. Digital rows use not-applicable states rather than pending nulls; duration measures have separate physical and digital definitions. Events retain every transition.

### Example 4

A claim is reviewed three times. The accumulating table overwrites `reviewed_at`, making first-response SLA and rework invisible.

Review events stay at `(claim,review_occurrence)` grain. The accumulating row publishes first review, latest review, review count and current status with explicit meanings. Rework analysis uses event/cycle facts.

### Example 5

A support ticket closes and reopens. Clearing the close date makes the original resolution vanish; keeping it makes the ticket appear closed.

The model retains first close, latest close, reopen count and current cycle/status, while transaction events preserve sequence. If cycle SLAs matter, a ticket-cycle fact provides one row per lifecycle cycle.

### Example 6

A shipment event effective just before day-end arrives after the snapshot build. Adding it only to the next day's flow produces a permanent reconciliation shift.

The late-event policy rebuilds from the last trusted checkpoint, versions affected snapshots and refreshes reports within the restatement window. Outside the window, a named prospective adjustment may be required.

### Example 7

A monthly snapshot includes month-to-date revenue. An analyst sums twelve monthly rows and gets the correct annual result only because the cumulative value resets monthly; summing daily month-to-date rows would overcount.

The field name includes window/reset, and semantic aggregation uses final value per month before annual sum. Daily interval revenue remains a separate additive measure.

### Example 8

Two approval messages share a timestamp but disagree. The loader chooses whichever file is listed first, making cycle duration nondeterministic.

Source sequence and event identity provide a total order, or the conflict is quarantined. File/list order is never a precedence rule. Replays produce the same milestone state.

### Example 9

An insurer needs pipeline distribution as it appeared on each quarter-end, not only final claim milestones. Reconstructing from mutable accumulating rows is impossible.

The system retains transaction state-change facts and derives quarter-end periodic pipeline snapshots, or versions accumulating rows over effective spans. Counts reconcile by claim identity and status at each cutoff.

### Example 10

A team relies on a cloud warehouse table snapshot of `orders` and calls it an analytical daily order snapshot. It contains current order rows but no eligible population, cutoff timezone or measure definitions.

The physical snapshot remains recovery evidence. A modeled periodic fact is separately generated with one order-status row per eligible order at business cutoff, conformed dimensions, missing policy and reconciliation to events.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): keys, transactions, temporal queries and window functions support snapshots and milestone calculations.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): conformed periods, calendars, facts and metrics coordinate state across domains.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): dense grids, incremental backfills and cumulative state create scale challenges.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md): stock–flow balance and process state are system feedback/control concepts.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): retries, event time, ordering, watermarks and atomic publication shape correctness.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): workflow APIs and events need stable process/milestone identity.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): orchestration, backfill controls and observability make snapshot pipelines operable.

## References

1. Kimball Group, [Transaction Fact Tables](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/transaction-fact-table/). Defines event-grain transaction facts and their dimensional context.
2. Kimball Group, [Periodic Snapshot Fact Tables](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/periodic-snapshot-fact-table/). Defines period grain and typically dense periodic rows.
3. Kimball Group, [Accumulating Snapshot Fact Tables](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/accumulating-snapshot-fact-table/). Defines workflow-instance rows, milestone date keys and repeated updates.
4. Kimball Group, [Design Tip 167: Complementary Fact Table Types](https://www.kimballgroup.com/2014/06/design-tip-167-complementary-fact-table-types/). Explains why transaction, periodic and accumulating facts can coexist.
5. Kimball Group, [Design Tip 145: Time-Stamping Accumulating Snapshot Fact Tables](https://www.kimballgroup.com/2012/05/design-tip-145-time-stamping-accumulating-snapshot-fact-tables/). Covers event pairing, periodic snapshots and versioned pipeline history.
6. Microsoft, [Modeling Fact Tables in Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-fact-tables). Provides current guidance on all three fact types and measure additivity.
7. Microsoft, [Load Tables in a Dimensional Model](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-load-tables). Describes incremental fact loading, integrity checks and special-member repair.
8. PostgreSQL Global Development Group, [Window Functions](https://www.postgresql.org/docs/current/functions-window.html). Defines `lag`, `lead` and window behavior useful for event intervals.
9. Google Cloud, [Introduction to Table Snapshots](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro). Defines a physical point-in-time table snapshot, useful for distinguishing storage from analytical snapshots.

## Exercises

### Exercise 1

Design transaction and daily periodic inventory facts for product-location stock. Specify grains, keys, cutoffs, density, measures, late events and exact reconciliation. Explain which monthly aggregations are valid.

### Exercise 2

A loan workflow has applied, verified, approved, funded, canceled and reopened events. Design an accumulating snapshot plus any complementary facts. Address optional stages, repeats, reopening, business-duration clocks and idempotent updates.

### Exercise 3

An account-day snapshot is sparse: rows appear only when balance changes. Define how to answer end-of-day total balance, average daily balance and “accounts with zero balance” without treating absence ambiguously. Compare redesign options.

### Exercise 4

A late shipment movement effective March 5 arrives March 20. Daily snapshots through March 19 are already published. Produce a restatement plan with checkpoints, versions, consumer impact, validation and rollback.

### Exercise 5

Choose fact types for an insurance claims process whose users need every transition, current milestone lags, daily open-claim backlog and quarter-end pipeline as originally reported. Show how tables reconcile without direct atomic fact joins.

## Answers to the Exercises

### Answer 1

The transaction fact has one row per accepted inventory movement with movement ID, product/location/event-date roles, effective timestamp, signed quantity, movement type and unit. The periodic fact has one row per eligible product-location-local-business-day cutoff/version with closing quantity, interval receipt/shipment/adjustment components, source watermark and observation status.

Choose dense eligible combinations when zero/absence must be explicit, or supply a coverage relation for sparse capture. Define exact timezone/cutoff and whether cutoff events enter the closing period. Reconcile per product-location: closing equals prior closing plus complete signed movements/adjustments. Monthly receipt/shipment flows sum; month-end stock uses last valid fresh snapshot; average inventory defines day/duration denominator; summing balances yields unit-days only when that exposure measure is intended.

### Answer 2

Use one accumulating row per loan application/process cycle with applied, first/latest verified, approved, funded, canceled and current-cycle milestones, status, verification count, reopen count and named durations. Future/skipped milestones have explicit states. Keep one transaction fact per immutable workflow event and optionally one cycle fact when reopened cycles require independent SLAs.

Define allowed transitions by workflow version. Funding may skip or require approval by product policy; cancellation is terminal only until governed reopen. Business duration uses a versioned calendar, timezone and paused intervals. Deduplicate by source event identity, deterministically order ties, and compare-and-set/rebuild the row so replay is a no-op. Reconcile each milestone/count/status to the event sequence and publish related values atomically.

### Answer 3

A changed-only row is a state-change event/materialization, not a self-sufficient daily snapshot. To recover end-of-day state, carry the latest valid value per account from a known baseline, respecting closure and freshness; missing complete history makes the answer unprovable. Average daily balance requires generating eligible account-days and duration/day weighting. Zero-balance accounts require coverage because “no change row” includes nonzero unchanged accounts.

Prefer a dense eligible account-day periodic snapshot when these queries are core. Alternatives are a complete effective-dated state table plus calendar expansion at query/materialization time, or sparse snapshots with explicit coverage and carry-forward contract. In every case separate observed zero, carried state, missing and ineligible, and reconcile to source totals.

### Answer 4

Validate the late event's identity, effective time, sign and source sequence. Select the last trusted snapshot before March 5, replay all accepted movements from that checkpoint through March 19, and generate new versions for every affected product-location-day. Compare key sets, event counts/digests, per-key state–flow residuals and authoritative controls.

Publish versions atomically, retain old versions and a restatement manifest listing cause, prior/new digests, affected periods and reports. Refresh dependent aggregates/semantic caches, notify consumers that historical values changed, and monitor reconciliation. Rollback selects the prior snapshot versions and dependent outputs via retained version pointers; never delete the late event or silently post it on March 20.

### Answer 5

Use a transaction fact at one claim-transition event grain for audit and ordering. Use a standard accumulating snapshot at one claim lifecycle/cycle grain for current/final milestones and lags. Generate a daily periodic fact at one eligible claim-day cutoff grain for open backlog. Preserve quarter-end originally reported pipeline either as versioned periodic output or a timespan accumulating fact with valid/system publication evidence.

Each derivative records the source event watermark/digest and workflow-rule version. Reconcile accumulating milestones/status to ordered events; reconcile daily open claims to event-derived state at cutoff; reconcile quarter-end key/status sets to the published daily/timespan version. Compare aggregates only after each fact is independently grouped to conformed status, product and date roles—never join transaction events directly to daily or accumulating rows and sum repeated measures.
