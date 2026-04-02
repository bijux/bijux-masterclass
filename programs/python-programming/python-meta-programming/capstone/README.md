# Python Metaprogramming Capstone


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Metaprogramming"]
  guide["Capstone docs"]
  section["README"]
  page["Python Metaprogramming Capstone"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  orient["Read the guide boundary"] --> inspect["Inspect the named files, targets, or artifacts"]
  inspect --> run["Run the confirm, demo, selftest, or proof command"]
  run --> compare["Compare output with the stated contract"]
  compare --> review["Return to the course claim with evidence"]
```
<!-- page-maps:end -->

This capstone is an executable plugin runtime for incident delivery adapters. It is
small enough to audit line by line and large enough to exercise the core tools of
the course in one place:

- descriptor-backed configuration fields
- decorator-based action instrumentation with preserved signatures
- metaclass-driven registration and generated constructors
- introspection-driven manifest export for tooling and debugging

## What it models

- a `PluginMeta` metaclass that registers concrete plugins by group and stable name
- `Field` descriptors that validate and coerce plugin configuration
- an `@action` decorator that records invocations while preserving signatures
- concrete incident-delivery plugins such as console, webhook, and pager adapters
- a runtime manifest that exposes field schemas and action signatures without
  executing plugin methods

## Run it

From this directory:

```bash
make confirm
```

Or use the saved review routes:

```bash
make inspect
make tour
make verify-report
make proof
```

## Read it in this order

- `PLUGIN_RUNTIME_GUIDE.md` for the vocabulary and timing model
- `SCENARIO_GUIDE.md` for the shipped demo and trace contracts
- `DEFINITION_TIME_GUIDE.md` for the class-definition sequence before runtime invocation
- `FIELD_GUIDE.md` for descriptor-backed configuration ownership
- `ACTION_GUIDE.md` for decorator-backed action ownership
- `ARCHITECTURE.md` for ownership boundaries
- `PLUGIN_CATALOG.md` for the concrete adapters and why each one exists
- `PUBLIC_API_GUIDE.md` for the supported package surface
- `TRACE_GUIDE.md` for the invocation-history review route
- `BUNDLE_GUIDE.md` for the saved review routes and bundle inventory story
- `SCENARIO_SELECTION_GUIDE.md` for choosing the smallest honest capstone route
- `TOUR.md` for a guided file-by-file walk
- `PROOF_GUIDE.md` for the repeatable verification route
- `PACKAGE_GUIDE.md` for the code-reading route
- `TEST_GUIDE.md` for the proof-reading route
- `TARGET_GUIDE.md` and `INSPECTION_GUIDE.md` for the public review surface
- `EXTENSION_GUIDE.md` for the safest change-placement route
- `src/incident_plugins/` for the implementation
- `tests/` for the proof surface

## Read it by course stage

- Observation modules: start with `make manifest`, `make registry`, and `PROOF_GUIDE.md`
- Decorator modules: inspect `src/incident_plugins/actions.py` and the runtime tests
- Descriptor modules: inspect `src/incident_plugins/fields.py` and `tests/test_fields.py`
- Metaclass module: inspect `src/incident_plugins/framework.py` and `tests/test_registry.py`
- Governance and mastery: return to `make inspect`, `make verify-report`, and the saved `artifacts/` bundles

## Why this capstone exists

The course book explains individual mechanisms in isolation. This capstone makes the
integration pressure visible. Class creation, descriptors, wrappers, and inspection
all interact here, so the implementation has to stay honest about:

- which work happens at class-definition time
- what gets validated on assignment versus on invocation
- how signatures survive wrappers
- how registries stay deterministic and resettable in tests

## Layout

- `src/incident_plugins/` contains the framework and built-in plugins.
- `tests/` contains executable verification for descriptors, registration, and runtime manifests.
- `ARCHITECTURE.md`, `TOUR.md`, `PROOF_GUIDE.md`, and the local guide set turn the capstone into a learner-facing review surface.

## Review routes

- `make inspect` writes the learner-facing inspection bundle with manifest and registry evidence.
- `make tour` writes the learner-facing walkthrough bundle with manifest, registry, demo, and trace outputs.
- `make verify-report` writes the executable verification report bundle with pytest output and public-surface evidence.
- `make confirm` runs the strongest local executable confirmation route.
- `make proof` builds the published learner-facing review route.

Read [PLUGIN_RUNTIME_GUIDE.md](PLUGIN_RUNTIME_GUIDE.md) first when the runtime terms still
feel fuzzier than the commands.

## Definition of done

- `make inspect` writes the learner-facing inspection bundle with manifest and registry evidence.
- `make tour` writes the guided walkthrough bundle for file-by-file review.
- `make verify-report` captures pytest output together with the public runtime surface.
- `make confirm` completes the strongest local executable confirmation route.
- `make proof` completes the published learner review route end to end.
