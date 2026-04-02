# Package Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph TD
  framework["framework.py"] --> fields["fields.py"]
  framework --> actions["actions.py"]
  framework --> plugins["plugins.py"]
  plugins --> cli["cli.py"]
  cli --> tests["tests/"]
```

```mermaid
flowchart LR
  question["Learner question"] --> package["Choose the owning package"]
  package --> boundary["Read the boundary and its neighbors"]
  boundary --> proof["Find the matching command or test"]
  proof --> review["Return with a concrete ownership answer"]
```
<!-- page-maps:end -->

Use this guide when the capstone still feels like a pile of Python hooks instead of a
system with named responsibilities. The goal is to know which file owns a kind of
metaprogramming pressure before you start chasing call stacks.

## Recommended reading order

1. `src/incident_plugins/framework.py`
2. `src/incident_plugins/fields.py`
3. `src/incident_plugins/actions.py`
4. `src/incident_plugins/plugins.py`
5. `src/incident_plugins/cli.py`
6. `tests/`

That route keeps definition-time authority first, attribute contracts second, wrapper
discipline third, concrete plugin behavior fourth, and proof surfaces last.

## Package responsibilities

| Surface | What it owns | What it should not own |
| --- | --- | --- |
| `framework.py` | metaclass registration, plugin construction, manifest export, and public runtime helpers | field coercion details or concrete delivery behavior |
| `fields.py` | descriptor-backed validation, coercion, and schema metadata | registry policy or action-history behavior |
| `actions.py` | action decorator metadata, signature preservation, and invocation recording | plugin registration or field storage |
| `plugins.py` | concrete incident-delivery plugins and realistic adapter behavior | framework-wide registry policy |
| `cli.py` | public inspection and invocation commands | hidden business logic not available from the runtime helpers |
| `tests/` | executable proof for import-time, class-definition-time, and invocation behavior | undocumented design authority |

## Best questions by file

- Open `framework.py` when you need to know what happens at class-definition time.
- Open `fields.py` when you need to know who validates configuration and when.
- Open `actions.py` when you need to prove that wrappers keep signatures and history visible.
- Open `plugins.py` when you need the concrete behavior that keeps the framework honest.
- Open `cli.py` when you need to inspect the public surface without importing private internals yourself.

## What this guide prevents

- starting in concrete plugins and mistaking them for the framework contract
- burying descriptor rules inside metaclass machinery
- treating the CLI as if it were the runtime source of truth
- reading tests before you know which file is supposed to own the behavior
