# Module Promise Map


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  promises["Module promises"]
  semantics["Semantics arc"]
  systems["Systems arc"]
  trust["Trust arc"]

  promises --> semantics
  promises --> systems
  promises --> trust
```

```mermaid
flowchart LR
  start["Choose a module"] --> promise["Read its promise first"]
  promise --> study["Study the module pages"]
  study --> checkpoint["Check the module exit bar"]
  checkpoint --> next["Move only when the promise is real"]
```
<!-- page-maps:end -->

Use this page when the table of contents feels wide and you want the exact promise of
each module in one place. A serious course should make clear what each module is for,
what it does not settle yet, and what design pressure it prepares you to handle next.

## The ten-module promise spine

| Module | Main promise | Not promised yet | Prepares you for |
| --- | --- | --- | --- |
| 01 Object Model | you can explain identity, equality, mutation, aliasing, and data-model hooks as contracts | architecture and collaboration boundaries | role assignment and layering |
| 02 Design and Layering | you can place behavior in values, entities, services, policies, adapters, and protocols deliberately | multi-object consistency and persistence | state transitions and lifecycle rules |
| 03 State and Typestate | you can make illegal states and transitions harder to construct | cross-object coordination and event boundaries | aggregates and collaboration |
| 04 Aggregates and Collaboration | you can centralize invariants and coordinate object collaboration without tangling ownership | storage, schema change, and runtime pressure | survivability and persistence |
| 05 Resources and Evolution | you can keep cleanup, retries, errors, and compatibility attached to clear owners | storage mapping and cross-process state | repository and schema boundaries |
| 06 Persistence and Schema Evolution | you can persist aggregates without flattening away domain meaning | concurrency scheduling and async runtime design | time and runtime pressure |
| 07 Time and Concurrency | you can keep clocks, queues, threads, and async boundaries from corrupting ownership | confidence strategy and public governance | tests and public surfaces |
| 08 Testing and Verification | you can design proof routes that match stateful and contract-heavy object systems | extension governance and third-party reuse | public APIs and safe customization |
| 09 Public APIs and Extension Governance | you can expose a stable public surface without letting extension points dissolve the model | operational measurement and hardening | operational review |
| 10 Performance, Observability, and Security | you can review an object system under hot-path, telemetry, trust, and operational pressure | no later module; this is the integrated review pass | capstone mastery and long-term stewardship |

## The three arcs inside the course

### Semantics arc

Modules 01 to 03 answer:

- what does an object mean?
- what role should it play?
- what states is it allowed to inhabit?

If these are weak, the rest of the course feels like architecture theater.

### Systems arc

Modules 04 to 07 answer:

- how do multiple objects preserve one coherent story?
- how do resources, persistence, time, and concurrency change ownership rules?

If these are weak, the system survives only while feature pressure is low.

### Trust arc

Modules 08 to 10 answer:

- what proof should exist?
- what is actually public?
- what breaks under load, visibility, or hostile inputs?

If these are weak, the system may look elegant but still fail under real use.

## How to use this map well

- Read the module promise before reading the module overview.
- Use “not promised yet” to avoid expecting later modules too early.
- Use “prepares you for” to understand why the reading order matters.

The promise map keeps the course from feeling like a pile of advanced topics. It makes
the book read like one argument about ownership, survivability, and trust.
