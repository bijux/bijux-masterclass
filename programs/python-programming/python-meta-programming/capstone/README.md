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

## Start here

Use the smallest honest route for the question you have:

- Want to inspect the public runtime shape without execution? Run `make manifest` or `make registry`.
- Want to inspect one concrete field or action contract? Run `make field` or `make action`.
- Want one full learner-facing review bundle? Run `make PROGRAM=python-programming/python-meta-programming capstone-walkthrough` from the repository root, or `make tour` locally.
- Want executable confirmation? Run `make verify-report`, `make proof`, or `make confirm`.

If you are new to this capstone, the best first route is:

1. Read [INDEX.md](docs/INDEX.md).
2. Run `make manifest`.
3. Read [INDEX.md](docs/INDEX.md).
4. Read [PLUGIN_RUNTIME_GUIDE.md](docs/PLUGIN_RUNTIME_GUIDE.md).
5. Read [ARCHITECTURE.md](docs/ARCHITECTURE.md).
6. Read `src/incident_plugins/framework.py`, then `fields.py`, then `actions.py`.
7. Read the matching tests.

## Start with these defaults

- If you do not know where to begin, read [INDEX.md](docs/INDEX.md).
- If you know the question but not the guide, read [INDEX.md](docs/INDEX.md).
- If you know the guide but not the command, read [COMMAND_GUIDE.md](docs/COMMAND_GUIDE.md).
- If you already have a claim and need evidence, read [PROOF_GUIDE.md](docs/PROOF_GUIDE.md).

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
make manifest
make registry
make plugin
make field
make action
make signatures
make demo
make trace
make inspect
make tour
make verify-report
make proof
```

From the repository root, use the published course-level routes:

```bash
make PROGRAM=python-programming/python-meta-programming capstone-walkthrough
make PROGRAM=python-programming/python-meta-programming capstone-tour
make PROGRAM=python-programming/python-meta-programming capstone-verify-report
make PROGRAM=python-programming/python-meta-programming capstone-confirm
```

## Documentation set

All supporting capstone guides live under `docs/`. Start from the group that matches
your pressure instead of reading the full list in alphabetical order.

### First-pass orientation

- [INDEX.md](docs/INDEX.md)
- [PLUGIN_RUNTIME_GUIDE.md](docs/PLUGIN_RUNTIME_GUIDE.md)
- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [DESIGN_BOUNDARIES.md](docs/DESIGN_BOUNDARIES.md)

### Public surface and command choice

- [COMMAND_GUIDE.md](docs/COMMAND_GUIDE.md)
- [TARGET_GUIDE.md](docs/TARGET_GUIDE.md)
- [MANIFEST_GUIDE.md](docs/MANIFEST_GUIDE.md)
- [REGISTRY_GUIDE.md](docs/REGISTRY_GUIDE.md)
- [PUBLIC_API_GUIDE.md](docs/PUBLIC_API_GUIDE.md)
- [PUBLIC_SURFACE_MAP.md](docs/PUBLIC_SURFACE_MAP.md)

### Mechanism and ownership guides

- [ACTION_GUIDE.md](docs/ACTION_GUIDE.md)
- [CONSTRUCTOR_GUIDE.md](docs/CONSTRUCTOR_GUIDE.md)
- [DEFINITION_TIME_GUIDE.md](docs/DEFINITION_TIME_GUIDE.md)
- [FIELD_GUIDE.md](docs/FIELD_GUIDE.md)
- [MECHANISM_SELECTION_GUIDE.md](docs/MECHANISM_SELECTION_GUIDE.md)
- [PACKAGE_GUIDE.md](docs/PACKAGE_GUIDE.md)
- [SCENARIO_GUIDE.md](docs/SCENARIO_GUIDE.md)
- [SCENARIO_SELECTION_GUIDE.md](docs/SCENARIO_SELECTION_GUIDE.md)
- [SOURCE_GUIDE.md](docs/SOURCE_GUIDE.md)
- [SOURCE_TO_PROOF_MAP.md](docs/SOURCE_TO_PROOF_MAP.md)

### Review, proof, and saved bundles

- [BUNDLE_GUIDE.md](docs/BUNDLE_GUIDE.md)
- [BUNDLE_MANIFEST_GUIDE.md](docs/BUNDLE_MANIFEST_GUIDE.md)
- [INSPECTION_GUIDE.md](docs/INSPECTION_GUIDE.md)
- [PROOF_GUIDE.md](docs/PROOF_GUIDE.md)
- [REVIEW_ROUTE_MAP.md](docs/REVIEW_ROUTE_MAP.md)
- [TEST_GUIDE.md](docs/TEST_GUIDE.md)
- [TEST_READING_MAP.md](docs/TEST_READING_MAP.md)
- [TOUR.md](docs/TOUR.md)
- [TRACE_GUIDE.md](docs/TRACE_GUIDE.md)
- [WALKTHROUGH_GUIDE.md](docs/WALKTHROUGH_GUIDE.md)

### Concrete runtime examples

- [EXTENSION_GUIDE.md](docs/EXTENSION_GUIDE.md)
- [PLUGIN_CATALOG.md](docs/PLUGIN_CATALOG.md)

## Read it by question

### "What can I inspect without running business behavior?"

- `make manifest`
- `make registry`
- [COMMAND_GUIDE.md](docs/COMMAND_GUIDE.md)
- [PUBLIC_SURFACE_MAP.md](docs/PUBLIC_SURFACE_MAP.md)
- [MANIFEST_GUIDE.md](docs/MANIFEST_GUIDE.md)
- [REGISTRY_GUIDE.md](docs/REGISTRY_GUIDE.md)
- [TARGET_GUIDE.md](docs/TARGET_GUIDE.md)

### "Where do wrappers, fields, and class creation live?"

- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [DESIGN_BOUNDARIES.md](docs/DESIGN_BOUNDARIES.md)
- [PACKAGE_GUIDE.md](docs/PACKAGE_GUIDE.md)
- [SOURCE_GUIDE.md](docs/SOURCE_GUIDE.md)
- [SOURCE_TO_PROOF_MAP.md](docs/SOURCE_TO_PROOF_MAP.md)
- `src/incident_plugins/actions.py`
- `src/incident_plugins/fields.py`
- `src/incident_plugins/framework.py`

### "What does one concrete plugin look like?"

- `make plugin`
- `make field`
- `make action`
- `make signatures`
- [PLUGIN_CATALOG.md](docs/PLUGIN_CATALOG.md)
- [CONSTRUCTOR_GUIDE.md](docs/CONSTRUCTOR_GUIDE.md)

### "How do I review the full learner-facing route?"

- [INDEX.md](docs/INDEX.md)
- `make PROGRAM=python-programming/python-meta-programming capstone-walkthrough`
- `make inspect`
- `make tour`
- [INSPECTION_GUIDE.md](docs/INSPECTION_GUIDE.md)
- [REVIEW_ROUTE_MAP.md](docs/REVIEW_ROUTE_MAP.md)
- [WALKTHROUGH_GUIDE.md](docs/WALKTHROUGH_GUIDE.md)
- [TOUR.md](docs/TOUR.md)

### "How do I prove the runtime still works?"

- `make verify-report`
- `make proof`
- `make confirm`
- [TEST_GUIDE.md](docs/TEST_GUIDE.md)
- [TEST_READING_MAP.md](docs/TEST_READING_MAP.md)
- [PROOF_GUIDE.md](docs/PROOF_GUIDE.md)

Use these question routes when you already know the pressure. Otherwise, stay with the
defaults above and escalate only one guide at a time.

## Read it by course stage

- Observation modules: start with `make manifest`, `MANIFEST_GUIDE.md`, `make registry`, and `PROOF_GUIDE.md`
- Decorator modules: inspect `src/incident_plugins/actions.py` and the runtime tests
- Descriptor modules: inspect `src/incident_plugins/fields.py`, `CONSTRUCTOR_GUIDE.md`, and `tests/test_fields.py`
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

## Repository layout

- `src/incident_plugins/` contains the framework and built-in plugins.
- `src/incident_plugins/framework.py` owns registration, generated constructors, and manifest export.
- `src/incident_plugins/fields.py` owns descriptor-backed field contracts.
- `src/incident_plugins/actions.py` owns wrapper-backed action contracts.
- `src/incident_plugins/plugins.py` owns concrete delivery adapters.
- `tests/` contains executable verification for descriptors, registration, and runtime manifests.
- `ARCHITECTURE.md`, `TOUR.md`, `PROOF_GUIDE.md`, and the local guide set turn the capstone into a learner-facing review surface.

## Review routes

- `make manifest` and `make registry` inspect the public runtime shape without invoking plugin behavior.
- `make plugin`, `make field`, `make action`, and `make signatures` isolate one concrete public contract at a time.
- `make demo` and `make trace` inspect one realistic runtime behavior and its recorded history.
- `make inspect` writes the learner-facing inspection bundle with manifest and registry evidence.
- `make tour` writes the learner-facing walkthrough bundle with manifest, registry, demo, and trace outputs.
- `make verify-report` writes the executable verification report bundle with pytest output and public-surface evidence.
- `make confirm` runs the strongest local executable confirmation route.
- `make proof` builds the published learner-facing review route.

Read [PLUGIN_RUNTIME_GUIDE.md](docs/PLUGIN_RUNTIME_GUIDE.md) first when the runtime terms still
feel fuzzier than the commands.

## Best companion guides

- [INDEX.md](docs/INDEX.md) for the smallest honest local route into the doc set
- [COMMAND_GUIDE.md](docs/COMMAND_GUIDE.md) for local command selection and artifact locations
- [PUBLIC_SURFACE_MAP.md](docs/PUBLIC_SURFACE_MAP.md) for connecting commands, outputs, and owning files
- [SOURCE_TO_PROOF_MAP.md](docs/SOURCE_TO_PROOF_MAP.md) for change-to-proof alignment
- [TEST_READING_MAP.md](docs/TEST_READING_MAP.md) for finding the first proof file by question
- [REVIEW_ROUTE_MAP.md](docs/REVIEW_ROUTE_MAP.md) for choosing the right local route, command, and bundle
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) for ownership boundaries
- [DESIGN_BOUNDARIES.md](docs/DESIGN_BOUNDARIES.md) for what each mechanism owns and what it should not own
- [PLUGIN_RUNTIME_GUIDE.md](docs/PLUGIN_RUNTIME_GUIDE.md) for the timing model
- [MECHANISM_SELECTION_GUIDE.md](docs/MECHANISM_SELECTION_GUIDE.md) for change placement
- [SCENARIO_SELECTION_GUIDE.md](docs/SCENARIO_SELECTION_GUIDE.md) for smallest-route selection
- [EXTENSION_GUIDE.md](docs/EXTENSION_GUIDE.md) for safe evolution

## Definition of done

- `make inspect` writes the learner-facing inspection bundle with manifest and registry evidence.
- `make tour` writes the guided walkthrough bundle for file-by-file review.
- `make verify-report` captures pytest output together with the public runtime surface.
- `make confirm` completes the strongest local executable confirmation route.
- `make proof` completes the published learner review route end to end.
