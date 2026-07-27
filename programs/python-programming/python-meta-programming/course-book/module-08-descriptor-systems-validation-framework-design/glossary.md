# Module Glossary

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Descriptor Systems Validation Framework Design"]
  page["Module Glossary"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

This glossary belongs to **Module 08: Descriptor Systems, Validation, and Framework Design**
in **Python Metaprogramming**. It keeps the language of this directory stable so the same
ideas keep the same names across lessons, practice, review, and capstone discussion.

## How to use this glossary

Use the glossary when framework-shaped descriptor discussions start to blur together cache
policy, external sources of truth, wrapper fields, hint-driven validation, and broader
architecture. Module 08 is meant to keep those boundaries explicit.

Use it for one more purpose as well:

to stop answers from sounding correct while staying ownership-vague. If a term cannot help
you identify an owner, a source of truth, a refusal boundary, or an escalation rule, you
are probably using it too loosely.

## Terms in this directory

| Term | Meaning in this directory |
| --- | --- |
| Cache invalidation | The explicit act of clearing or refreshing a cached descriptor value when its dependencies or source data change. |
| Composed field | A descriptor built by wrapping one field descriptor in another so an extra concern can be layered through delegation. |
| Descriptor-system packet | A reviewable packet containing source-of-truth notes, invalidation rules, owner choices, rejected alternatives, and escalation boundaries for one descriptor design. |
| Evidence route | A deliberate sequence of checks a learner uses to prove what a descriptor owns, where truth lives, and how failure or escalation is handled. |
| External source of truth | The backing store outside the instance that ultimately owns a field's persisted value. |
| External-storage descriptor | A descriptor that reads from or writes to backend-managed state rather than relying only on instance-local storage. |
| Field wrapper | A delegating descriptor layer that adds one concern around an inner descriptor, such as validation or logging. |
| Framework boundary | The point where descriptor behavior is no longer just per-field semantics and now requires explicit architectural owners. |
| Honest field claim | A bounded description of what one field descriptor actually guarantees, without implying broader coordination it does not prove. |
| Hidden I/O | The case where ordinary attribute access performs backend reads, writes, or serialization work that is not obvious from the syntax alone. |
| Hint-driven field | A descriptor that reads annotations or `Annotated[...]` metadata as runtime evidence for validation or coercion. |
| Identity map | A broader framework mechanism that keeps one in-memory object per record identity, explicitly outside the scope of a single descriptor. |
| Invalidation owner | The code path, layer, or actor responsible for clearing cached state when it is no longer trustworthy. |
| Layer ledger | A review note listing each wrapper layer, the one concern it owns, and the protocol path it must forward correctly. |
| Lower-power owner | A smaller owner candidate that was considered but rejected because it cannot honestly carry the required contract. |
| Read-through cache | A cache strategy where a descriptor fetches from the authoritative backend on miss, stores the value locally, and returns it. |
| Refusal surface | The set of inputs, hint forms, behaviors, or architectural responsibilities a design intentionally declines to support. |
| Serialization boundary | The conversion point between Python values and stored representations such as JSON strings. |
| Source of truth | The location or system whose value should be treated as authoritative when field state and cached state diverge. |
| Stronger owner | A broader owner candidate such as a service, session, repository, or framework layer that may be required when field scope is no longer enough. |
| Unit of work | A wider framework pattern for coordinating multiple persistence changes together, beyond what one field descriptor should own. |
| Write-through behavior | The strategy of persisting a new field value to the backend immediately when assignment occurs, while also updating local cached state. |
| `Annotated[...]` metadata | Extra runtime metadata attached to a type annotation and often used here for validator-style field behavior. |

## Confusing pairs to keep separate

| Pair | Distinction to keep |
| --- | --- |
| computed access vs cached access | computed recalculates; cached reuses and therefore needs freshness ownership |
| local storage vs external source of truth | local storage may hold a copy; the external source still decides what is authoritative |
| composition vs subclass multiplication | composition layers narrow concerns; subclass multiplication bakes combinations into a growing class tree |
| hint support vs runtime typing comprehensiveness | a supported subset is honest; a vague claim of "runtime typing" is not |
| field ownership vs framework ownership | one field can own attribute semantics; cross-record or lifecycle coordination needs broader architecture |

## Review prompts for vocabulary

If a term appears in your notes, pressure-test it with one of these prompts:

- who owns this?
- where does truth live?
- what does this design refuse?
- what stronger owner would be needed if the blast radius grew?

If the term does not help answer one of those questions, tighten the wording.

## Keep the module connected

- Return to [Module 08 Overview](index.md) for the full learning route.
- Use [Exercises](exercises.md) and [Exercise Answers](exercise-answers.md) to pressure-test the framework-descriptor vocabulary.
- Revisit the [Worked Example](worked-example-building-an-educational-mini-relational-model.md) when a field system starts to look like broader architecture and needs a boundary check.
