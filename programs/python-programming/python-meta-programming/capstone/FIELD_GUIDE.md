# Field Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  declare["Declare Field on class"] --> setname["Descriptor gets __set_name__"]
  setname --> init["Generated constructor initializes field"]
  init --> access["Field validates and exposes value"]
```

```mermaid
flowchart LR
  question["What does this field own?"] --> descriptor["Read the descriptor contract"]
  descriptor --> timing["Ask when coercion or defaults happen"]
  timing --> proof["Choose the matching test or inspection route"]
```
<!-- page-maps:end -->

Use this guide when the capstone's descriptor layer still feels like a clever trick instead
of a clear ownership boundary. The goal is to keep field semantics explicit before you
reason about metaclasses or concrete plugins.

## What a field owns

| Responsibility | Owning surface |
| --- | --- |
| attribute name and storage key | `Field.__set_name__` in `fields.py` |
| required versus defaulted configuration | `Field.required()` and `Field.initialize()` |
| type coercion and validation | concrete field subclasses such as `StringField`, `IntegerField`, `BooleanField`, and `ChoiceField` |
| public schema metadata | `Field.spec()` and `FieldSpec.manifest()` |

## What fields should not own

- plugin registration policy
- action-history recording
- CLI parsing and public command routing
- concrete delivery behavior

## Best code route

1. `Field`
2. `StringField`
3. `IntegerField`
4. `BooleanField`
5. `ChoiceField`

## Best proof surfaces

- `tests/test_fields.py` for coercion, defaults, and per-instance storage
- `manifest` output when the question is about public schema shape
- `DEFINITION_TIME_GUIDE.md` when the question is really about when the field becomes wired into the class

## Best companion guides

- read [PLUGIN_RUNTIME_GUIDE.md](PLUGIN_RUNTIME_GUIDE.md) when the field terms still need wider runtime context
- read [PACKAGE_GUIDE.md](PACKAGE_GUIDE.md) when you want the file route around the descriptor layer
- read [SCENARIO_GUIDE.md](SCENARIO_GUIDE.md) when you want one shipped plugin example using those fields
