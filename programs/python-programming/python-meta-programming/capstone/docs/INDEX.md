# Capstone Index

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph TD
  guide["INDEX.md"]
  route["Route selection"]
  local["Local capstone guides"]
  code["Source files"]
  proof["Commands and tests"]

  guide --> route --> local
  local --> code
  local --> proof
```

```mermaid
flowchart LR
  question["Pick the question you have"] --> local_guide["Choose the smallest local guide"]
  local_guide --> inspect["Inspect the command, file, or bundle it names"]
  inspect --> answer["Return with one concrete ownership or proof answer"]
```
<!-- page-maps:end -->

Use this page when the capstone root shows many guide files and you need one durable
starting point. It combines the first-session route with the guide index so the doc set
has one stable entry hub instead of two overlapping arrival pages.

## First honest pass

1. Run `make manifest`.
2. Read [README.md](../README.md).
3. Read [ARCHITECTURE.md](ARCHITECTURE.md).
4. Read [PLUGIN_RUNTIME_GUIDE.md](PLUGIN_RUNTIME_GUIDE.md).
5. Open `src/incident_plugins/framework.py`, then `fields.py`, then `actions.py`.
6. Read `tests/test_registry.py` and `tests/test_fields.py`.
7. Stop there unless your current question clearly requires invocation or CLI detail.

## What the first pass should settle

| Step | Main answer |
| --- | --- |
| `make manifest` | what the runtime exposes publicly without invoking plugin behavior |
| `README.md` | what this repository is for and which commands matter |
| `ARCHITECTURE.md` | which file owns each mechanism and why |
| `PLUGIN_RUNTIME_GUIDE.md` | how definition-time, attribute-time, and invocation-time behavior differ |
| `framework.py`, `fields.py`, `actions.py` | where registration, field behavior, and action wrapping actually live |
| `test_registry.py`, `test_fields.py` | what proof already exists for class creation and descriptor ownership |

## Start here by question

### "What is this project, and how should I enter it?"

- [README.md](../README.md)
- [INDEX.md](INDEX.md)
- [PLUGIN_RUNTIME_GUIDE.md](PLUGIN_RUNTIME_GUIDE.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)

### "Which file owns which mechanism?"

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [DESIGN_BOUNDARIES.md](DESIGN_BOUNDARIES.md)
- [PACKAGE_GUIDE.md](PACKAGE_GUIDE.md)
- [SOURCE_GUIDE.md](SOURCE_GUIDE.md)

### "Which command should I run first?"

- [COMMAND_GUIDE.md](COMMAND_GUIDE.md)
- [TARGET_GUIDE.md](TARGET_GUIDE.md)
- [README.md](../README.md)

### "How do I inspect the public runtime shape?"

- [MANIFEST_GUIDE.md](MANIFEST_GUIDE.md)
- [REGISTRY_GUIDE.md](REGISTRY_GUIDE.md)
- [INSPECTION_GUIDE.md](INSPECTION_GUIDE.md)
- [PUBLIC_SURFACE_MAP.md](PUBLIC_SURFACE_MAP.md)

### "How do wrappers, fields, and constructors work?"

- [ACTION_GUIDE.md](ACTION_GUIDE.md)
- [FIELD_GUIDE.md](FIELD_GUIDE.md)
- [CONSTRUCTOR_GUIDE.md](CONSTRUCTOR_GUIDE.md)
- [DEFINITION_TIME_GUIDE.md](DEFINITION_TIME_GUIDE.md)

### "How do I review or extend the project safely?"

- [PROOF_GUIDE.md](PROOF_GUIDE.md)
- [TEST_GUIDE.md](TEST_GUIDE.md)
- [TEST_READING_MAP.md](TEST_READING_MAP.md)
- [EXTENSION_GUIDE.md](EXTENSION_GUIDE.md)
- [MECHANISM_SELECTION_GUIDE.md](MECHANISM_SELECTION_GUIDE.md)
- [SOURCE_TO_PROOF_MAP.md](SOURCE_TO_PROOF_MAP.md)

### "How do I read the saved review bundles?"

- [BUNDLE_GUIDE.md](BUNDLE_GUIDE.md)
- [BUNDLE_MANIFEST_GUIDE.md](BUNDLE_MANIFEST_GUIDE.md)
- [WALKTHROUGH_GUIDE.md](WALKTHROUGH_GUIDE.md)
- [TOUR.md](TOUR.md)
- [REVIEW_ROUTE_MAP.md](REVIEW_ROUTE_MAP.md)

## Escalation rule

Use the smallest guide that answers the current question, then stop.

- Move to source files only after the guide names the owning file.
- Move to tests only after the guide names the claim that still needs proof.
- Move to saved bundles only when another reviewer needs a durable artifact.

## Good stopping point

Stop after the first pass when you can answer:

- what the runtime exports without invocation
- which file owns registration
- which file owns field behavior
- which file owns action wrapping
- which proof file you would open first for registration or field questions
