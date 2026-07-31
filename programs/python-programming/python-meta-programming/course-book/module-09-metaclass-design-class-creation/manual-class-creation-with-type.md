# Manual Class Creation with `type(...)`

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Metaclass Design Class Creation"]
  page["Manual Class Creation with type"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  name["name"]
  bases["bases"]
  namespace["namespace"]
  constructor["type(name, bases, namespace)"]
  class_object["new class object"]
  instance["instance created later"]

  name --> constructor
  bases --> constructor
  namespace --> constructor
  constructor --> class_object --> instance
```
<!-- page-maps:end -->

A class statement is convenient syntax for building a class object. Start Module 09 by
making those construction inputs visible before adding a custom metaclass.

## The problem: assemble one class from explicit data

Imagine a local schema loader has already produced:

- the name `DeliveryNotice`
- the base class `object`
- a `channel` attribute
- a `render` function

The pressure is to create one class from that data. Nothing yet requires a policy over
future subclasses. Calling `type(...)` directly is therefore smaller and more honest than
defining a custom metaclass.

## Run the focused evidence

From the course directory:

```console
python3 -m unittest discover -s tests -p "test_class_creation_manual.py" -v
python3 -m labs.class_creation
```

Inspect:

- `labs/class_creation/manual.py`
- `tests/test_class_creation_manual.py`
- the `manual_construction` object in the JSON packet

Predict the result before opening the JSON:

1. What will `created.__name__` be?
2. What will `created.__bases__` contain?
3. Where will `channel` be stored?
4. When is the first instance created?

## The construction recipe

The lab names the three inputs:

```python
@dataclass(frozen=True, slots=True)
class ClassRecipe:
    name: str
    bases: tuple[type[object], ...]
    namespace: dict[str, object]
```

Then it constructs a class:

```python
def build_class(recipe: ClassRecipe) -> type[object]:
    if not recipe.name.isidentifier():
        raise ValueError(f"class name must be an identifier: {recipe.name!r}")
    namespace = dict(recipe.namespace)
    namespace.setdefault("__module__", __name__)
    return type(recipe.name, recipe.bases, namespace)
```

Trace each input to the result:

| Recipe input | Observable result |
| --- | --- |
| `name="DeliveryNotice"` | `created.__name__ == "DeliveryNotice"` |
| `bases=(object,)` | `created.__bases__ == (object,)` |
| `namespace["channel"]` | `created.channel == "console"` |
| `namespace["render"]` | an instance binds and calls `render` as a method |
| injected `__module__` | introspection identifies the defining module |

The returned object is a class. It is itself an instance of `type`.

```python
created = build_class(recipe)

assert isinstance(created, type)
notice = created()
assert type(notice) is created
```

Class creation happens at the first line. Instance construction happens at the second.
Keeping those events separate prevents later confusion about metaclass timing.

## Why copy the namespace

The lab calls `dict(recipe.namespace)` before passing it to `type`.

That copy creates a boundary:

```python
namespace = {"channel": "console"}
created = build_class(ClassRecipe("Delivery", (), namespace))
namespace["channel"] = "webhook"

assert created.channel == "console"
```

Without the copy, reviewers might incorrectly assume later mutation of the recipe changes
the already-created class. The test makes the intended ownership explicit: construction
consumes the values present at that moment.

This is a shallow copy. Mutable objects inside the mapping would still be shared. The lab
does not claim deep isolation.

## Why `__module__` matters

A class statement normally supplies attributes such as `__module__` and `__qualname__`.
When code creates a class manually, the caller owns enough of that context to keep
introspection understandable.

The lab supplies `__module__` when the recipe does not. It deliberately does not invent a
synthetic `__qualname__` hierarchy or source location. Manual construction can make source
provenance less obvious, which is one reason ordinary class syntax remains preferable for
ordinary classes.

## Failure route: reject invalid construction input

The lab rejects a non-identifier name before calling `type`:

```python
build_class(ClassRecipe("not a class", (), {}))
# ValueError: class name must be an identifier: 'not a class'
```

This proves a local factory can own local input validation. A custom metaclass would add
hierarchy-wide behavior without solving a hierarchy-wide problem.

Other failures remain Python’s responsibility:

- incompatible bases
- invalid metaclass selection derived from those bases
- namespace entries that violate a descriptor or base-class rule

Do not wrap every `TypeError` merely to make the factory appear more complete.

## Where manual construction stops

Direct `type(...)` is a good fit when:

- one explicit call site owns class generation
- the name, bases, and namespace already exist as data
- callers can see when generation happens
- no automatic rule must govern future subclasses

It becomes insufficient when the real invariant is:

- every subclass must be checked automatically
- class-body assignments must be observed while they occur
- one class family needs a consistent construction protocol

Those pressures lead to later sections. They do not retroactively make this factory a
metaclass.

## Capstone comparison

The incident-plugin capstone does not call `type(...)` from application code to create each
plugin. Plugin authors use ordinary class statements because those declarations are the
reader-facing API.

The capstone still reaches the same primitive: `PluginMeta.__new__` delegates to
`type.__new__` through `super()`. Its extra policy is justified only because every plugin
subclass participates in field collection, signature generation, and registration.

That is the transfer:

```text
one explicit generated class
  -> direct type(...) call

one automatic policy over a class family
  -> consider a metaclass after rejecting lower-power owners
```

## Review exercise

For any proposed dynamic class factory, record:

- the exact source of `name`, `bases`, and `namespace`
- who validates those inputs
- when construction happens
- how the class is discoverable in tracebacks and introspection
- why an ordinary class statement is not clearer
- why future subclasses do or do not need automatic policy

If the final answer is only “metaclasses are more flexible,” the ownership analysis is
not complete.

## Exit check

Continue when you can:

- map all three `type(...)` inputs to observable class attributes
- explain why the returned class exists before any instance
- identify the shallow namespace-copy boundary
- name one provenance cost of manual construction
- reject a metaclass for this one-call-site problem

Next: [Metaclass Resolution, Timing, and Conflicts](metaclass-resolution-timing-and-conflicts.md).
