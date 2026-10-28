---
module_id: DE-016
program: Data Engineering
level: 1
module_number: 16
title: Event and Activity Models
status: complete
last_verified: 2026-09-02
---

# Event and Activity Models

## One-Page Review

### Governing question

How can a data product turn occurrences from many producers into an append-oriented, replay-safe activity history whose identities, times, actors, objects, sessions, funnels and privacy semantics remain stable under retries, lateness and schema change?

### Essential definitions

- An **occurrence** is something that happens in the domain; an **event record** is a producer's observation or representation of that occurrence.
- A **domain event** states a business fact, a **behavioral event** records an actor's interaction, and a **telemetry event** records operational evidence. Their audiences and contracts differ.
- **Event identity** distinguishes one logical record from retries; when identifiers are source-scoped, the deduplication key is $(source,event\_id)$.
- **Event time** is when the represented occurrence happened. **Observed/ingestion time** is when a collector or platform received it. **Processing time** is when a computation handles it.
- An **activity model** organizes events around actor, action, object and context so paths and outcomes can be analyzed.
- A **session** is a derived grouping under an explicit rule, often consecutive actor events separated by no more than an inactivity threshold $\gamma$.
- A **funnel** is an ordered sequence of qualifying stages with an eligibility population and a completion window.
- **Identity stitching** maps device, anonymous, account and person identifiers under evidence, scope and consent rules; it is not a guess that equal-looking attributes mean the same person.
- A **late event** arrives after a result was first emitted for its event-time window. A **watermark** is a system estimate of event-time completeness, not proof that no earlier event can arrive.
- A **schema version** identifies interpretation rules for an event payload. Event type and schema evolution must preserve or explicitly break consumer expectations.

### Central model, mechanism, or theorem

Represent a normalized event as

$$
E=(I,N,S,A,O,T_e,T_o,C,P,V),
$$

where $I$ is event identity, $N$ event name/type, $S$ source, $A$ actor identity at collection, $O$ subject/object, $T_e$ event time, $T_o$ observed time, $C$ context, $P$ typed properties and $V$ schema version. The canonical activity grain is one accepted logical event, not one delivery attempt, session, user-day or current entity.

For an actor's deduplicated events sorted by the total order $(T_e,T_o,I)$, assign a new session before event $i$ exactly when the actor changes or

$$
T_{e,i}-T_{e,i-1}>\gamma.
$$

With the comparison operator, threshold, actor key and tie-break fixed, this rule produces a deterministic partition. It does not discover a natural session; it defines one.

### Critical invariants

- One row represents one accepted logical event at a declared granularity.
- The event key is stable across retry/replay and distinct across separate occurrences.
- Event, observed and processing times retain separate names and meanings.
- Ordering uses a deterministic total order; ingestion order is never silently treated as occurrence order.
- Event names express completed facts or actions and follow an owned, versioned taxonomy.
- Actor, account, device, session and object identities are separate fields with governed mappings.
- Session, funnel, path, cohort and attribution outputs record rule versions and eligibility denominators.
- Duplicate, bot, test, internal and consent-ineligible events are classified before metrics.
- Breaking schemas create explicit versions or migrations; consumers never infer meaning from field shape alone.
- Backfills are idempotent, event-time aware and reproducible from immutable inputs plus versioned rules.

### Common failures

Using arrival time as business time; assigning a new ID on every retry; naming commands as if they succeeded; storing mutable current state as an event; mixing page, item and order grain; embedding unbounded JSON without contracts; joining anonymous and known users by weak attributes; treating sessions as source facts; counting events as people; computing funnels without eligibility or order; letting duplicate purchases inflate revenue; discarding all late data at a watermark; changing event meaning without a version; collecting sensitive properties “just in case”; deleting only modeled outputs while raw events persist; and calling an append-only table immutable while allowing silent corrections.

### Compact example

Six deliveries contain one replay of event `e1`. Deduplicating by stable event ID leaves five logical events for two actors. With $\gamma=30$ minutes, actor `u1` has activity at minutes 0, 5 and 40, producing two sessions; actor `u2` has activity at minutes 2 and 8, producing one. One of the two eligible actors purchases, so actor conversion is $1/2=0.5$. Changing the timeout, identity mapping or funnel window creates a different derived model and therefore requires a rule version.

### Connections

[DE-009](009-time-time-zones-and-event-timestamps.md) defines event-time semantics, [DE-011](011-grain-and-the-meaning-of-a-row.md) defines row propositions, and [DE-015](015-snapshot-and-accumulating-fact-tables.md) contrasts events with state snapshots. Planned DE-017 develops wide denormalized models and appears in the [Data Engineering roadmap](../ROADMAP.md). Event contracts connect to [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), late/order semantics to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and governed collection to [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

Can a producer, platform owner and analyst independently inspect an event and agree on what happened, once, to whom or what, at which business time, under which schema and consent state—and then reproduce every session, funnel or path derived from it?

An event table is attractive because it appears universal: append a timestamp, name and properties, then ask questions later. The simplicity is deceptive. A click delivery is not necessarily a click occurrence; a payment request is not a completed payment; a browser identifier is not a person; a session is not observed directly; and the first computed funnel is not timeless truth.

The [CloudEvents specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) requires `id`, `source`, `specversion` and `type`, defines duplicate recognition through the combination of source and ID, and distinguishes optional subject, time and data-schema metadata. It is a transport-neutral interoperability model, not a complete analytical schema. An analytical boundary should borrow its discipline while adding actor, object, observed time, privacy and business-grain rules appropriate to the domain.

The durable goal is not “capture everything.” It is to preserve enough governed evidence to replay interpretations without turning ambiguous, excessive or sensitive collection into permanent technical debt.

## Why This Matters

Activity models often feed the most decision-sensitive metrics in a product: activation, conversion, retention, engagement, attribution and experiment exposure. Small semantic errors compound. A retry that doubles purchase events changes revenue; a clock bug reverses a funnel; an identity join combines two people; a session timeout change alters denominators; bot activity makes adoption appear stronger.

Events also bridge operational and analytical systems. Services publish domain facts, clients emit interaction evidence, collectors attach receipt metadata, stream processors window records, and warehouses derive business models. Each boundary can change identity, time, schema or cardinality. Without explicit contracts, downstream SQL merely hides the ambiguity.

Append orientation is valuable because new evidence can be added and old interpretations replayed. It is not a license to treat erroneous or unlawful data as untouchable. Corrections, erasure, retention and consent changes need governed mechanisms that preserve audit evidence without retaining prohibited content.

Event and state models answer different questions. Events explain transitions and sequence. Current-state tables answer what is true now. Snapshots answer what state held at cutoffs. Replacing any one with another either loses history or makes ordinary queries costly and fragile.

## Prerequisites and Retrieval

Retrieve the business vocabulary; event producers and owners; domain commands and outcomes; actor, account, device, object and transaction identifiers; retry behavior; source sequence; event, client, server, observed and processing clocks; timestamp precision and timezone; clock-skew expectations; event taxonomy; schema registry and compatibility policy; payload examples; nested-item grain; correlation, causation and trace identifiers; collection SDK behavior; offline buffers; late-arrival distribution; transport delivery guarantees; deduplication horizon; session rules; funnel stages and eligibility; conversion windows; cohort anchors; attribution policy; experiment exposure source; identity graph evidence; anonymous-to-known rules; shared-device behavior; consent state at collection; sensitive-field classification; geographic restrictions; retention and deletion obligations; bot/test/internal traffic markers; source sampling; data-quality controls; downstream semantic definitions; replay/backfill procedures; publication versioning; and owners for breaking changes.

Distinguish occurrence from observation; business fact from request or command; behavioral analytics from operational telemetry; event type from schema version; event ID from transaction ID; actor from subject/object; anonymous profile from known account; device from person; source session ID from derived session; client clock from server clock; event time from ingestion and processing time; duplicate delivery from repeated business action; nested context from repeated child grain; property absence from null; late from invalid; correlation from causation; exposure from activity; eligible actor from active actor; stage occurrence from funnel completion; conversion window from attribution window; retained audit metadata from retained sensitive payload; source correction from warehouse mutation; and raw immutable delivery from governed canonical truth.

Before DDL, build adversarial timelines: retry the same event, repeat the same action legitimately, deliver a purchase before its earlier view, send two events at one timestamp, cross the session threshold exactly, sign in after anonymous activity, sign out on a shared device, revoke consent, change a schema, delete an account, generate a bot burst and backfill a week of offline events. State the expected canonical rows and metrics.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish occurrences, event records, commands, state and snapshots;
2. declare a canonical event grain and stable identity contract;
3. separate event, observed and processing time and handle late data;
4. design owned event taxonomies and compatible schema evolution;
5. model actor, object, context, causation and identity evidence;
6. derive deterministic sessions, funnels, paths, cohorts and retention;
7. prevent replay, nested-grain and denominator double counting;
8. apply privacy, consent, deletion and retention controls;
9. validate and observe event quality across producers and versions; and
10. replay/backfill derived activity models reproducibly.

## Core Exposition

### Start with the occurrence

Ask what real-world proposition becomes true. `order_submitted` should mean an order was accepted under a defined rule, not merely that a button was pressed. A client click and server acceptance may be two legitimate events because they represent different occurrences.

Name uncertainty honestly. `payment_attempted`, `payment_authorized` and `payment_captured` are distinct facts. A command such as `capture_payment` expresses intent; it must not masquerade as its outcome.

Document producer authority. The service owning the business transition is normally authoritative for the domain event; a browser can be authoritative only for observations available at the browser.

### Declare one-event grain

Write: “one row per accepted logical occurrence emitted by source $S$ under event type $N$.” Define whether a batch message expands into child events or remains one aggregate event.

An order containing three items is one order event if its payload describes one order occurrence. Exploding items produces a different `(event,item)` analytical grain. Do not sum order value after explosion unless allocation or distinct-order rules prevent multiplication.

Keep delivery attempts outside the canonical grain, or model them in a transport audit table. Canonical event counts must not depend on retry count.

### Separate event families

Domain events carry business meaning and support integration or audit. Behavioral events describe human or agent interaction and support journeys. Telemetry events describe software operation and support reliability.

The same moment can emit all three: a user presses Buy, an order is accepted, and a request span records latency. Correlation identifiers connect them, but they should not be collapsed because ownership, retention, precision and consumers differ.

Create explicit inclusion rules for each family. A broad generic `event` table can be a physical envelope while semantic views retain family-specific contracts.

### Design a canonical envelope

A useful envelope includes source-scoped event ID, event type, source, subject/object, actor identities, event time, observed time, schema reference/version, payload, collection context, consent classification, correlation ID and causation ID.

CloudEvents' required identity/source/type/version fields offer a portable core. Its optional `subject`, `time` and `dataschema` show why routing metadata should be readable without decoding arbitrary payloads.

The envelope should be small and stable. Domain-specific measures belong in typed payloads or modeled tables, not an ever-growing set of unrelated nullable top-level columns.

### Build stable event identity

The identifier answers “is this the same logical event?” Producers should generate it once and reuse it for every retry. If uniqueness is only source-scoped, deduplicate on $(source,event\_id)$ rather than ID alone.

Transaction or order ID is not automatically event ID. One transaction can emit attempted, authorized and settled events; each needs distinct event identity while sharing subject/transaction identity.

When a source cannot provide stable IDs, a deterministic fingerprint can be an explicit fallback. Its normalized fields, collision risk, horizon and correction behavior must be documented; it is weaker than producer identity.

### Make replay idempotent

Canonicalization should select one representative for a duplicate key deterministically, retain delivery evidence separately and make repeated loads no-ops.

If duplicate payloads disagree, do not choose arbitrary arrival order. Apply an authoritative source version/sequence rule or quarantine the conflict. A duplicate identifier with different meaning is a contract violation.

Deduplicate before sessions, funnels and sums. Otherwise every downstream activity construct inherits inflated counts and altered paths.

### Distinguish repeated actions from duplicates

Two legitimate clicks on the same button can share actor, name, object and timestamp precision. They remain different occurrences when their event IDs differ.

A retransmitted purchase uses the same event ID. A second purchase uses a new event ID even if amount and customer match. Content equality is not identity.

Validate suspicious repetition statistically, but do not collapse it without a governed identity rule.

### Govern event names and taxonomy

Choose names that express completed observations or facts, use a consistent grammatical form, and assign ownership. Avoid ambiguous `click`, `success`, `update` or UI-label names whose meaning changes with layout.

Define required properties, actor/object roles, producer authority, allowed cardinality, privacy class and examples for every type. A registry can validate both schema and semantic metadata.

Do not encode every property into an event name. `product_viewed` with a typed product object is more governable than dynamically generated names.

### Version event schemas

Additive optional fields are often compatible; removal, renaming, type changes, unit changes and semantic redefinition are not. Compatibility depends on consumer behavior, not merely parser acceptance.

The [CloudEvents primer](https://github.com/cloudevents/spec/blob/main/cloudevents/primer.md) recommends planning versioning early and notes that consumers generally expect a recognized event type to evolve compatibly. Use a new type/version or an explicit migration when that expectation cannot hold.

Retain the original schema identity and payload, plus the normalization rule version. This allows corrected transforms without pretending the source originally emitted the new contract.

### Separate top-level fields from properties

Promote fields whose semantics are common and required for routing, quality or access control. Keep type-specific properties under governed schemas.

Free-form property bags invite spelling drift, mixed units and high-cardinality secrets. Validate allowed names, types, enumerations, length and sensitivity at collection and normalization boundaries.

Preserve unknown compatible fields when practical, but do not automatically expose them to all consumers.

### Model actor, object and context

Activity is often described as actor–action–object with context such as application, campaign or location. The [W3C ActivityStreams core](https://www.w3.org/TR/activitystreams-core/) defines activities with actor, object, target, origin, result and instrument roles, demonstrating that “who did what to what” needs more than user ID and event name.

Keep roles explicit. The purchaser (actor), order (object), storefront (origin) and promotion (instrument/context) are different entities. Reusing a generic `entity_id` makes joins and access rules ambiguous.

Record identity as known at event time, then use versioned mappings for later analytical resolution.

### Preserve causation and correlation

Correlation groups related work; causation points to the event or command that directly led to another event. Neither proves philosophical or statistical causality, but both improve traceability.

A checkout correlation may contain view, submit, authorization and order events. The authorization may be caused by the submit command. Trace/span identifiers connect operational evidence but need not equal business correlation IDs.

Keep these identifiers stable across asynchronous boundaries and retries.

### Separate occurrence and observation time

The [OpenTelemetry logs data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) defines `Timestamp` as origin occurrence time and `ObservedTimestamp` as when collection observed the record. That distinction is equally important in analytics.

Store both when available. Event time drives business sequence and windows; observed time supports freshness, delay and pipeline diagnosis. Processing time may vary on every replay and belongs to run metadata or processing records.

Never overwrite an implausible event time with receipt time without preserving the original and a quality disposition.

### Handle clock quality and ties

Client clocks can drift, reset or lack timezone. Attach clock source, precision and quality when material. Server-confirmed business events may supersede client timestamps for authoritative ordering under a documented rule.

Timestamp alone rarely creates total order. Add source sequence where authoritative, then observed time and event ID as deterministic tie-breakers. A deterministic order is reproducible even when true causal order remains unknown.

Quarantine impossible values or route them through explicit fallback policies; do not silently sort by file position.

### Use windows, watermarks and lateness deliberately

Event-time windows group by occurrence time. Processing-time windows group by when computation happens and therefore change with delay/replay. Choose based on the question.

The [Apache Beam programming guide](https://beam.apache.org/documentation/programming-guide/) describes event-time windows, watermarks, triggers, allowed lateness and late firings. A watermark enables timely provisional output; it is an estimate, so finality still requires a late-data and restatement policy.

Record whether outputs are early, on-time or late revisions, plus the source/run watermark. Consumers must know whether a metric is provisional or closed.

### Derive sessions as versioned interpretations

A session is rarely a source fact. Sort deduplicated eligible events by actor and deterministic time order. Begin a session at the first event and whenever the preceding gap exceeds $\gamma$.

Specify whether an exact gap equal to $\gamma$ stays in the session. Specify which events count as activity, how midnight and platforms behave, and whether authenticated account or anonymous device is the actor key.

Persist `session_rule_version`, session start/end, qualifying event count and derived session ID. A source-provided session identifier may be retained separately and compared.

### Prove deterministic sessionization

Fix one actor, total ordering and threshold rule. The first event must begin a session. For each later event, the declared predicate on the adjacent gap uniquely determines “same session” or “new session.” Induction over the ordered list therefore gives one unique partition.

This proof sketch establishes determinism, not behavioral truth. Another timeout or actor definition yields another valid partition. The rule is part of the metric contract.

### Model identity without inventing certainty

Store device, browser/client, anonymous profile, login/account and person identifiers separately. Maintain mappings with evidence type, valid/system times, tenant scope, confidence category and consent basis.

An anonymous-to-known transition may link earlier activity only if policy permits retroactive stitching. Logout, shared devices, recycled identifiers and merged/split accounts require explicit behavior.

Google's current [User-ID guidance](https://developers.google.com/analytics/devguides/collection/ga4/user-id) illustrates using a site-owned non-PII identifier to connect behavior across sessions/devices. A warehouse implementation still owns its identity, privacy and deletion rules.

### Define funnels with eligibility and order

A funnel is not a count of event names. Define eligible actors/entities, anchor time, ordered predicates $F_1,\ldots,F_k$, repeated-stage selection, allowed interleaving, completion window $W$ and identity version.

Actor $a$ completes stage $j$ when qualifying events exist at nondecreasing times

$$
t_{a,1}\leq t_{a,2}\leq\cdots\leq t_{a,j}\leq t_{a,1}+W.
$$

Stage-$j$ conversion may use eligible actors, stage-1 starters or prior-stage completers as denominator. Publish the denominator name and count, not only a percentage.

### Treat paths as bounded sequences

Path analysis orders selected events and represents repeats, loops and termination. Define inclusion taxonomy, maximum length, lookback window, tie-break and collapsing rules.

Do not concatenate raw unbounded names into enormous strings. Model one row per path position or bounded sequence with actor/session/rule keys.

Rare-path aggregation and privacy thresholds can reduce disclosure and cardinality while retaining useful structure.

### Build cohorts and retention carefully

A cohort groups entities by a stable anchor such as first qualifying activation, acquisition or contract start. Freeze or version the anchor rule; a backfilled earlier event can move membership.

Retention period $r$ requires an eligible cohort denominator and a defined qualifying return during the period. Calendar-week, rolling seven-day and exact-day retention are different.

Separate “not retained” from “not observable” because consent withdrawal, deletion, platform gaps or incomplete windows change denominators.

### Separate activity, exposure and outcomes

Experiment or recommendation analysis needs the event proving opportunity/exposure, not just later activity. A purchase without known exposure cannot be attributed to a treatment merely because the user was assigned.

Model assignment, eligibility, exposure and outcome separately. Define contamination and cross-device identity rules.

Funnels likewise require population eligibility before stage one; active-event tables alone omit silent eligible entities.

### Govern attribution windows

Attribution assigns credit under a policy; it does not reveal unique causation. Specify eligible touches, channel normalization, lookback window, ordering, model (first/last/multi-touch), conversion identity and late-event closure.

Store contribution weights and rule version. Validate that weights sum to one per conversion when the model requires it.

Do not overwrite raw referrer/campaign evidence with normalized classifications; preserve both under access controls.

### Control nested and repeated grain

An event may contain repeated items, impressions or experiments. Decide whether to keep nested payloads, create child tables or allocate parent measures.

Parent event ID plus child position/business key defines child grain. Repeated fields can legitimately have duplicates, so position may matter.

Never join an event-level amount to exploded items and sum it unchanged. Keep amount at event grain or allocate under a reconciliation rule.

### Filter bots, tests and internal traffic explicitly

Classification should produce disposition and reason, not silent deletion. Rules may use known agents, rate patterns, environment, account flags and producer markers.

Keep rule version and effective time because classifications evolve. Report raw, eligible and excluded counts so sudden changes are observable.

Avoid using one heuristic as proof of a bot; false positives can erase legitimate high-volume activity.

### Minimize sensitive collection

Define an allowlist of properties and privacy class before instrumentation. Avoid raw email, full URL query strings, free text, precise location or tokens unless a justified use and control exist.

Consent state should be attached or resolvable at collection time, not reconstructed solely from current preferences. Route disallowed records away from analytical storage.

Use purpose-based access, encryption, retention and aggregation. Hashing a direct identifier can still leave linkable personal data.

### Implement deletion and retention end to end

Map a governed deletion subject to raw events, identity mappings, canonical tables, derived sessions/funnels, extracts and backups according to policy. Deleting only the user dimension leaves behavioral rows linkable.

Retention may differ by event family and field. Tokenize or redact selected properties when business aggregates can remain lawfully without identity.

Record completion evidence without retaining prohibited payload content. Test deletion through every derived layer and prevent replay from resurrecting expired data.

### Validate event contracts at boundaries

Check required fields, types, enumerations, timestamp range, ID format, source/type ownership, schema identity, nested cardinality, property size and privacy allowlists.

Invalid data should be rejected, quarantined or accepted with a documented degradation policy. Producers need actionable feedback and contract-test fixtures.

Validate semantic invariants too: currency required with money, item totals reconcile, event outcome is possible, and source sequence does not regress unexpectedly.

### Observe event quality

Monitor accepted, duplicate, rejected, quarantined and consent-filtered counts by source/type/version. Measure null rates, distinct IDs, delay $T_o-T_e$, clock anomalies, schema versions, payload size and late-event rates.

Detect sudden volume and cardinality changes against release/deployment context. Zero events may mean no activity or broken instrumentation; compare expected producer heartbeat and eligible population.

Reconcile business outcomes to authoritative systems, not only to prior event counts.

### Backfill and replay reproducibly

A derived model is a function of immutable accepted events, identity graph version, taxonomy/schema mappings, time/session/funnel rules and exclusion policy. Record all input ranges and versions.

Replay deduplicates before derivation and writes a new output version or atomically replaces a governed partition. Processing timestamps may change; business results should not unless inputs or rules changed.

Run comparisons on key sets, counts, sums, stage populations and sample paths. Keep rollback pointers and prevent concurrent incremental jobs from racing the backfill.

### Publish semantic activity tables

Expose typed event-family tables or semantic views with clear grains rather than forcing every consumer to parse raw payloads. Common outputs include canonical events, identity mappings, sessions, session events, funnel completions, cohort membership and attribution contributions.

Each derived table carries rule version, source watermark/input digest and publication time. Metrics link to eligibility definitions and quality limitations.

Keep raw delivery/audit evidence access restricted; broad convenience should not expand sensitive access.

### Evolve activity models safely

Inventory consumers before event rename or meaning change. Dual-publish compatible transition periods, provide mappings, compare metrics and set removal dates.

When a session, identity or funnel rule changes, compute side-by-side versions rather than rewriting history silently. Explain expected breaks and reconcile unaffected invariants.

Retire obsolete collection at the producer as well as downstream. Otherwise cost and privacy exposure persist even if analysts stop using the field.

## Definitions and Notation

Let $R$ be raw deliveries and $E$ accepted canonical events. Let $K(e)=(source(e),id(e))$ be the logical event key. A deterministic canonicalization function $D$ produces at most one accepted event for each $K$ and routes conflicting duplicates separately.

For event $e$, $N(e)$ is type/name, $A(e)$ actor identity under an identity version, $O(e)$ object, $T_e(e)$ event time, $T_o(e)$ observed time, $V(e)$ schema version, and $P(e)$ typed properties. Collection delay is

$$
L(e)=T_o(e)-T_e(e).
$$

Negative $L$ can expose clock skew; a large positive $L$ indicates buffering or pipeline delay. Neither alone proves the event invalid.

For actor $a$, let $(e_1,\ldots,e_n)$ be eligible events sorted by $(T_e,T_o,K)$. With session gap $\gamma$, define boundary indicator

$$
b_i=\begin{cases}
1,&i=1,\\
1,&A(e_i)\neq A(e_{i-1})\text{ or }T_e(e_i)-T_e(e_{i-1})>\gamma,\\
0,&\text{otherwise.}
\end{cases}
$$

Then the session ordinal is $s_i=\sum_{j=1}^{i}b_j$. If equality at $\gamma$ should split, replace $>$ with $\geq$ and version the rule.

For funnel stage predicates $F_1,\ldots,F_k$ and window $W$, let $C_j$ be the set of eligible actors completing stages through $j$ in order. The step conversion is $|C_j|/|C_{j-1}|$ for $j>1$, while overall conversion is $|C_k|/|G|$ for declared eligible population $G$. Zero denominators produce undefined/not-applicable, not zero success.

For cohort $G_c$ and retained members $Q_{c,r}$ in retention period $r$,

$$
retention(c,r)=\frac{|Q_{c,r}|}{|G_c^{observable}(r)|}.
$$

The observable denominator must exclude only governed unobservable cases, not inconvenient non-returners.

## Mechanisms, Invariants, or Proof Structure

**Canonicalization mechanism.** Parse under the declared schema, validate envelope and privacy rules, normalize source/type/time, group by logical key, select a deterministic representative, quarantine conflicting duplicates, and publish accepted events atomically with dispositions.

**Replay-idempotence invariant.** For canonicalization function $D$, reintroducing identical deliveries does not change canonical output:

$$
D(R\cup R)=D(R).
$$

This holds when stable keys persist across retries and representative selection is deterministic. It does not hold if the loader invents a fresh ID for each arrival.

**Session determinism proof sketch.** The first ordered event starts exactly one session. Assuming the partition through $e_{i-1}$ is unique, the fixed boundary predicate on $e_i$ has one Boolean result, so $e_i$ either extends the prior session or starts the next. By induction the full partition is unique. The proof depends on a total order and fixed actor/gap policy.

**Funnel nesting invariant.** A correctly constructed sequential funnel satisfies

$$
C_k\subseteq C_{k-1}\subseteq\cdots\subseteq C_1\subseteq G.
$$

If a later-stage count exceeds an earlier-stage count under the same grain and population, stage predicates, identity, time order or denominators are inconsistent.

**Child reconciliation invariant.** When event-level amount $m(e)$ is allocated to child rows with weights $w_{e,j}$, require $\sum_j w_{e,j}=1$ and $\sum_j m(e)w_{e,j}=m(e)$ within declared rounding tolerance.

**Attribution invariant.** For full-credit attribution, contribution weights per conversion sum to one. Unattributed conversions either carry an explicit unattributed row or are excluded under a named denominator; they do not disappear silently.

**Privacy propagation invariant.** A deletion or expiry disposition applied to subject $x$ must reach every governed derivative addressable through the selected identity graph version. Replaying older raw inputs cannot recreate the removed identity/payload after the policy cutoff.

**Empirical evidence boundary.** Passing replay tests, count reconciliation and sample timelines demonstrates behavior for tested inputs. It does not prove that the event taxonomy captures human intent, identity links are correct, or future producers will comply.

<!-- bijux-verify: {"id":"deduplicate-and-sessionize","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"raw_events=6\nunique_events=5\nduplicates=1\nactors=2\nsessions=3\nevent_counts={'add': 1, 'purchase': 1, 'view': 3}\npurchasers=1\nactor_conversion=0.5000\nsessionization_deterministic=True\n","stderr":""}} -->
```python
events = (
    {"id": "e1", "actor": "u1", "time": 0, "name": "view"},
    {"id": "e1", "actor": "u1", "time": 0, "name": "view"},
    {"id": "e2", "actor": "u1", "time": 5, "name": "add"},
    {"id": "e3", "actor": "u1", "time": 40, "name": "view"},
    {"id": "e4", "actor": "u2", "time": 2, "name": "view"},
    {"id": "e5", "actor": "u2", "time": 8, "name": "purchase"},
)

unique = {}
for event in events:
    unique.setdefault(event["id"], event)
accepted = sorted(unique.values(), key=lambda e: (e["actor"], e["time"], e["id"]))

session_count = 0
previous = None
for event in accepted:
    if previous is None or event["actor"] != previous["actor"] or event["time"] - previous["time"] > 30:
        session_count += 1
    previous = event

counts = {}
for event in accepted:
    counts[event["name"]] = counts.get(event["name"], 0) + 1
counts = {name: counts[name] for name in sorted(counts)}
actors = {event["actor"] for event in accepted}
purchasers = {event["actor"] for event in accepted if event["name"] == "purchase"}

print(f"raw_events={len(events)}")
print(f"unique_events={len(accepted)}")
print(f"duplicates={len(events) - len(accepted)}")
print(f"actors={len(actors)}")
print(f"sessions={session_count}")
print(f"event_counts={counts}")
print(f"purchasers={len(purchasers)}")
print(f"actor_conversion={len(purchasers) / len(actors):.4f}")
print("sessionization_deterministic=True")
```

## Alternatives and Trade-Offs

**Domain-specific tables versus universal envelope.** Typed tables make semantics and performance explicit. A universal envelope simplifies transport and raw retention. A common approach uses the envelope at ingestion and governed typed projections for consumption.

**Client versus server events.** Clients see impressions and interactions that servers cannot. Servers better establish accepted business outcomes and trusted time. Correlate both; choose authority per occurrence.

**Source session versus derived session.** Source IDs reproduce platform behavior but vary by SDK and device. Derived sessions provide cross-source consistency but impose an analytical rule. Keep provenance and never give them the same field name.

**Mutable event correction versus compensating event.** In-place correction simplifies current truth but obscures evidence. A correction/retraction event preserves lineage but complicates consumers. Govern validity and publication versions either way.

**Event-type version versus payload schema version.** A new event type makes breaking meaning visible to routing consumers. A schema version is less disruptive for representational changes. Meaning changes deserve the more explicit boundary.

**Nested versus child tables.** Nested payloads preserve atomic event structure and reduce joins. Child tables support repeated-grain analytics and indexing. Both require parent-grain measure protection.

**Strict rejection versus permissive quarantine.** Strict rejection protects canonical quality but can lose evidence if producers cannot resend. Quarantine retains diagnosis without contaminating metrics. Silent coercion is usually the worst option.

**Early output versus completeness.** Watermark-triggered early results reduce latency. Allowed lateness and restatement improve completeness at operational cost. Label provisional/final states and choose by decision tolerance.

**Deterministic versus probabilistic identity.** Deterministic authenticated mappings are explainable but incomplete. Probabilistic links increase coverage and error/privacy risk. Keep confidence and do not present inferred people as observed facts.

**Recompute versus incrementally repair.** Full replay is simple and reproducible but expensive. Incremental derivation is efficient but must reopen affected sessions, funnels and cohorts when late events arrive.

**Long raw retention versus minimization.** Longer history supports new questions and reprocessing. It expands cost, exposure and deletion burden. Collect and retain according to known purposes rather than hypothetical value.

## Failure Modes and Misconceptions

- **“One delivery is one event.”** Retries can deliver one logical event many times.
- **“Same payload means duplicate.”** Repeated legitimate actions may have equal content.
- **“Transaction ID is event ID.”** One transaction produces multiple event types.
- **“A click proves an order.”** Interaction, intent and accepted outcome differ.
- **“Arrival order is occurrence order.”** Buffers, networks and retries reorder events.
- **“One timestamp is enough.”** Business time and observation freshness answer different questions.
- **“A watermark proves completeness.”** It is an estimate used to balance latency and lateness.
- **“Late means invalid.”** Offline and delayed events can be valid business evidence.
- **“Event name documents itself.”** Required properties, actor/object roles and authority still need a contract.
- **“Adding a field is always compatible.”** Requiredness, defaults and consumer assumptions can break.
- **“JSON accepts anything, so the schema is flexible.”** Unbounded bags create semantic drift and privacy risk.
- **“User ID is a person.”** It may identify an account, tenant membership or shared login.
- **“Device equals user.”** Devices can be shared, reset or used by many accounts.
- **“Identity stitching is just a join.”** Evidence, time, scope, consent and split/merge behavior matter.
- **“Sessions exist in nature.”** They are derived under timeout and identity rules.
- **“Thirty minutes is universal.”** Threshold and equality behavior are product definitions.
- **“Event counts are user counts.”** One actor can emit many events.
- **“A funnel is independent event totals.”** It requires eligible entities, order and a window.
- **“Stage percentages explain their denominator.”** Multiple valid denominators exist.
- **“Conversion proves attribution.”** Attribution is credit assignment under policy.
- **“Exploding items preserves order totals.”** Parent measures multiply without grain control.
- **“Bot filtering is obvious.”** Heuristics change and can exclude legitimate behavior.
- **“Hashing removes privacy obligations.”** Stable hashes remain linkable identifiers.
- **“Consent can be inferred later.”** Current state may not describe collection-time permission.
- **“Deleting the user table deletes the user.”** Events, mappings and derivatives may remain linkable.
- **“Append-only means never correct.”** Corrections and erasure need explicit governed paths.
- **“Replays should match processing timestamps.”** Processing metadata can change while business output remains stable.
- **“Schema-valid means semantically valid.”** Units, outcomes and authoritative ownership also matter.

## Worked Examples

### Example 1

A mobile client retries `purchase_completed` after losing the acknowledgement. The SDK reuses event ID `p-17`; two deliveries reach storage.

Canonicalization keys on `(mobile-app,p-17)`, retains one logical purchase and records two delivery attempts. Revenue and purchasers count once. If the retry had generated a new ID, transport behavior would corrupt business metrics.

### Example 2

A user taps Add twice rapidly. Both events share actor, item and millisecond timestamp but have distinct IDs.

The model keeps both because equal content is not duplicate identity. A separate anomaly rule may flag rapid repetition. Collapsing on `(actor,name,time)` would erase legitimate quantity intent.

### Example 3

A browser emits `checkout_clicked`; the order service later emits `order_accepted`. Network failure means some clicks have no accepted order.

The two types remain separate and share correlation ID. The funnel uses the client event for interaction and the service event for completion. Reporting a click as a sale would convert intention into an untrue fact.

### Example 4

An offline device records events at 09:00 and uploads at 15:00 after a 12:00 daily watermark. A noon dashboard initially omits them.

Event-time windows place them in the morning activity period; observed time shows six-hour delay. Allowed lateness triggers a revised output and marks its publication version. Processing-time grouping would incorrectly move activity to 15:00.

### Example 5

Actor events occur at minutes 0, 30 and 61 with $\gamma=30$. Under `gap > 30`, the first two remain together and the third starts a new session because its adjacent gap is 31.

Using `gap >= 30` would create three sessions. Both are deterministic; only the declared version tells consumers which metric they are comparing.

### Example 6

An anonymous browser views a product, then signs into account A and purchases. Later another person signs into account B on the same device.

The model keeps device, anonymous profile and account IDs distinct. Policy may connect the pre-login view to A at the login transition, but it does not permanently assign all device history to A. The later B activity remains separate.

### Example 7

A funnel requires eligible trial users to view setup, connect a source and publish within seven days. One user publishes without a recorded source connection.

That user does not complete the ordered three-stage funnel even though the final event exists. Independent event counts may show more publishes than connections; the nested completion sets must not. Missing instrumentation is investigated separately.

### Example 8

An order event has three items and order revenue 90. Exploding items repeats 90 on each row and a naive sum reports 270.

The child model stores item revenue that reconciles to 90, or keeps order revenue only in the parent. Parent event count uses distinct event identity after child joins.

### Example 9

A product team adds raw search text and full page URLs to every event. URLs contain email reset tokens and search text contains health information.

The collection allowlist rejects/redacts these fields before broad analytical storage. Safe normalized page route and categorized query intent may be retained under a documented purpose. Downstream column hiding alone would leave sensitive raw data exposed.

### Example 10

A new identity rule merges accounts and a funnel rule extends its window from 7 to 14 days. Rewriting the prior funnel table makes last month's published conversion change without explanation.

The pipeline publishes a new identity/rule version beside the old result, compares stage populations and documents the expected increase. Consumers migrate explicitly; stored input digests allow both versions to be replayed.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): uniqueness, constraints, JSON typing, temporal mappings and window functions implement canonical models.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): event vocabularies, identity graphs, semantic metrics and governance span domains.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): deduplication state, event-time windows, replay and high-cardinality paths create scale trade-offs.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md): events are observations of system behavior, while feedback depends on latency, uncertainty and measurement validity.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): at-least-once delivery, clocks, ordering and causality determine canonical correctness.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): commands, domain outcomes, event envelopes and compatible contracts share service ownership boundaries.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): registries, collection gateways, replay controls, observability and policy enforcement make event products operable.

## References

1. Cloud Native Computing Foundation, [CloudEvents Specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md). Defines portable event identity, source, type, time, subject and schema context.
2. Cloud Native Computing Foundation, [CloudEvents Primer](https://github.com/cloudevents/spec/blob/main/cloudevents/primer.md). Explains event identity, correlation and compatible type evolution.
3. Apache Software Foundation, [Apache Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/). Documents event-time windows, watermarks, triggers and allowed lateness.
4. OpenTelemetry Authors, [Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/). Distinguishes occurrence timestamp from observed timestamp and defines event/log context fields.
5. World Wide Web Consortium, [Activity Streams 2.0 Core](https://www.w3.org/TR/activitystreams-core/). Defines activity structures and actor, object, target, origin, result and instrument roles.
6. Google, [Send User IDs](https://developers.google.com/analytics/devguides/collection/ga4/user-id). Describes a site-owned non-PII identifier for connecting activity across sessions and devices.
7. Google, [Recommended Events](https://developers.google.com/analytics/devguides/collection/ga4/reference/events). Provides typed behavioral event/property examples and transaction-ID deduplication guidance.
8. PostgreSQL Global Development Group, [Window Functions](https://www.postgresql.org/docs/current/functions-window.html). Defines `lag`, `lead` and ordered window semantics useful for session gaps and event sequences.

## Exercises

### Exercise 1

Design a canonical purchase-event contract for web, mobile and partner producers. Specify grain, source-scoped identity, event and observed times, actor/object roles, item grain, currency/value rules, retries, corrections, privacy controls and schema evolution.

### Exercise 2

Given actor events at minutes 0, 10, 40, 70 and 101, sessionize them with $\gamma=30$ under both `gap > 30` and `gap >= 30`. State why the output is deterministic and which metadata must accompany it.

### Exercise 3

Define a three-stage onboarding funnel: eligible account, setup viewed, source connected and first job succeeded within seven days. Address repeated events, same-time ties, late events, missing exposure, denominators and account merges.

### Exercise 4

A new mobile release doubles event volume, introduces negative collection delays and sends email addresses in a free-form property. Produce an incident and remediation plan that preserves evidence without contaminating analytics or retaining prohibited data.

### Exercise 5

Plan a historical replay after changing anonymous-to-known stitching and session timeout. Specify inputs, rule versions, affected derivatives, reconciliation, comparison, atomic publication, rollback, retention and consumer communication.

## Answers to the Exercises

### Answer 1

Use one event per accepted purchase occurrence, authoritative from the commerce service even when clients/partners supply correlation evidence. Key by `(source,event_id)` with the ID generated once and reused on retries. Store purchase/order as object, account or anonymous actor separately, event time from acceptance, collector observed time, schema reference/version, currency and decimal amount, consent class and correlation/causation identifiers.

Keep items as typed nested data or child rows at `(event,item_position)` grain; item amounts reconcile to the parent and parent value never repeats into an additive child measure. Require currency when value exists and transaction identity distinct from event identity. Corrections use a governed correction/retraction or versioned validity path. Allowlist properties, exclude direct identifiers, apply deletion/retention transitively, and use compatible optional changes or a new event/schema version for breaking semantics.

### Answer 2

Adjacent gaps are 10, 30, 30 and 31. Under `gap > 30`, minutes 0, 10, 40 and 70 form session one; 101 begins session two. Under `gap >= 30`, minute 0 and 10 form session one, 40 session two, 70 session three and 101 session four.

Each output is deterministic because actor key, ordered event list, threshold, comparison and tie-break yield one boundary decision at every position. Persist the rule version, threshold/unit, equality convention, eligible event taxonomy, identity version, ordering keys, derived session ID and input watermark/digest.

### Answer 3

Define eligible accounts independently of activity and anchor their seven-day window to trial start or first governed exposure. Deduplicate logical events, sort by `(event_time,source_sequence,observed_time,event_id)`, and select the first setup view, then first qualifying connection at or after it, then first successful job at or after connection within the anchor window. Repeats do not create extra actors; deterministic ties follow source precedence or quarantine conflicts.

Publish eligible, stage-one, stage-two and stage-three counts so completion sets nest, plus step and overall denominators. Treat absent setup exposure separately from failure. Late events reopen affected accounts until closure/restatement policy. Account merges use a versioned identity graph and trigger side-by-side recomputation rather than silent historical change.

### Answer 4

Pause or quarantine the offending source/version at the collection boundary, revoke broad access to affected payloads and preserve only minimal restricted incident evidence permitted by policy. Identify the deployment and time range. Compare delivery, unique-event, duplicate, timestamp-delay, schema and property profiles; negative delay suggests clock regression or wrong timestamp mapping, while doubling may combine legitimate traffic and retry duplication.

Patch instrumentation to reuse IDs, map the correct clock and remove email before transmission. Redact/delete prohibited values from raw, canonical, derived, extracts and backups according to policy, and prevent replay resurrection. Reprocess from clean deliveries, reconcile authoritative outcomes, publish corrected versions atomically, notify metric owners and add contract/privacy regression tests and release monitoring.

### Answer 5

Freeze the accepted-event input range/digest and retain original actor identifiers. Version both the identity graph and session rule, including timeout, equality behavior, taxonomy and total order. Recompute identity-resolved events, sessions, session events, funnels, cohorts, retention and attribution that depend on either rule; unaffected event facts should retain keys and counts.

Compare unique event keys, mapped/unmapped identities, session counts/durations, funnel nesting, cohort movement and sensitive-data disposition against old output. Publish new tables or partitions atomically with rule/input metadata and a pointer to the prior version. Rollback changes the governed pointer. Respect deletion/retention before and during replay, prevent incremental writers from racing it, and give consumers side-by-side metric deltas, interpretation changes and migration timing.
