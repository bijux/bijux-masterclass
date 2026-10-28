# Evidence Model

## Claims need the right oracle

The program distinguishes evidence by the property it can actually establish. A strong engineering explanation names the claim, the owner, the cheapest decisive oracle, and the remaining uncertainty.

| Claim type | Decisive evidence | Common false substitute |
|---|---|---|
| Contract structure | standards-aware parse, reference resolution, schema fixtures | rendered documentation |
| Provider conformance | provider-neutral live request/response observation | framework route existence |
| Domain rule | deterministic pure test and state-transition counterexample | database constraint alone |
| Durable effect | database/storage transaction evidence across restart and failure | log line or trace span |
| Security decision | adversarial input and policy test at the enforcement boundary | authentication success or scanner output |
| Operational diagnosis | bounded logs, metrics, and traces correlated with durable truth | telemetry treated as business authority |
| Performance decision | comparable workload/environment identity, complete outcome populations, correctness oracle, repeated runs | one favorable latency number |
| Event effect | source fact, outbox publication, delivery attempt, inbox/effect transaction, acknowledgement/replay evidence | broker publish success |

## Evidence classes

Reports should state whether evidence is:

- **deterministic** — pure logic, parsing, fixtures, canonicalization, or static release rules;
- **local-process** — a real process without representative external dependencies;
- **live-dependency** — PostgreSQL, broker, network, or filesystem behavior in a controlled environment;
- **representative** — workload and topology close enough to support a bounded operational claim;
- **operated** — sustained evidence from a real service context.

A lower evidence class is not worthless. It becomes misleading only when presented as a stronger class.

## The falsification-first loop

For each lab:

1. state the guarantee;
2. plant one controlled defect or pressure condition;
3. predict the first oracle that should fail;
4. capture the smallest failing observation;
5. repair the mechanism, not merely the assertion;
6. retain a regression;
7. rerun broader proof;
8. record what remains untested.

This loop prevents “green test” reasoning. A proof that has never been shown to reject the named defect may be checking the wrong property.

## Negative claims

Some of the most important statements are negative:

- a valid OpenAPI document does not prove runtime conformance;
- a trace does not prove a transaction committed;
- an API key does not establish resource ownership;
- a benchmark does not establish production capacity unless the environment and workload justify that claim;
- at-least-once delivery does not guarantee duplicate business effects;
- a dependency-light audit does not establish live PostgreSQL or broker behavior.

The course checkpoints require these limits because honest boundaries are part of professional competence.

## Evidence retention

Retain small, reviewable artifacts: request/response transcripts, failing fixtures, transaction rows, minimized hostile vectors, trace IDs, metric snapshots, benchmark envelopes, query plans, replay reports, and release decisions. Do not retain secrets, full sensitive payloads, uncontrolled logs, or generated bulk that another reader cannot interpret.
