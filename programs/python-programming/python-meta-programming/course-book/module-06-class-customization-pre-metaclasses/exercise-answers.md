# Exercise Answers: Lower-Power Class Design Studio

<!-- page-maps:start -->
## Page Maps

```mermaid
flowchart LR
  claim["Name the class or attribute claim"] --> owner["Identify the runtime owner"]
  owner --> timing["Place it on the lifecycle"]
  timing --> proof["Connect focused evidence"]
  proof --> boundary["State the unproved boundary"]
```
<!-- page-maps:end -->

Use these answers after attempting the studio. A different implementation can be
defensible, but its timing, ownership, evidence, and limits must be equally explicit.

Keep the lifecycle boundary visible while reviewing every answer:

```mermaid
flowchart LR
  body["Execute class body"] --> create["Create finished class"]
  create --> decorate["Apply class decorators"]
  decorate --> construct["Construct instance"]
  construct --> access["Read or write attribute"]
```

A decorator can change the finished class; a property or descriptor owns the later
attribute operation. None of those lower-power tools sees the namespace while the body
is still executing.

## Answer 1: extend the class-decorator trace

With decorators written as outer, middle, inner, the exact trace is:

```text
factory:outer
factory:middle
factory:inner
body:Delivery
decorate:inner:Delivery
decorate:middle:Delivery
decorate:outer:Delivery
```

The helper expansion is:

```python
outer = tracing_class_decorator("outer", events)
middle = tracing_class_decorator("middle", events)
inner = tracing_class_decorator("inner", events)

class Delivery:
    events.append("body:Delivery")

Delivery = outer(middle(inner(Delivery)))
```

The returned class remains the same object because every tracing decorator mutates and
returns it. Its metaclass remains `type`.

Common wrong turn: listing factory events bottom-up because application is bottom-up.
Expression evaluation and returned-decorator application are different moments.

This proves post-construction order. It does not prove the decorators are independent:
later decorators can rely on state installed by earlier ones.

A requirement to inspect both writes to the same name during the body is already too
early. The finished class retains only the final ordinary value.

## Answer 2: test dataclass claims independently

The claim ledger should look like:

| Evidence | Proves | Does not prove |
| --- | --- | --- |
| generated methods in `vars(cls)` | dataclass installed those methods | the methods enforce domain policy |
| `"three"` stored in `attempts: int` | annotation did not validate at runtime | static tooling would accept the call |
| two list identities differ | factory produced per-instance lists | list contents are valid or immutable |
| `FrozenInstanceError` on assignment | ordinary field rebinding is blocked | nested state is deeply frozen |
| list append succeeds | nested object keeps its own mutation behavior | all nested mutations are desirable |
| no `__dict__` | slots changed ordinary storage | the class is inherently faster in this workload |

Common wrong turn: adding `__post_init__` validation and then claiming the dataclass
annotation enforced the rule. The hook would be the owner.

The standard decorator is preferable to the teaching frozen decorator when generated
fields, slots, equality, and standard frozen behavior form the actual requirement.

## Answer 3: defend one property boundary

The event story is:

1. valid assignment reaches the setter and stores `_endpoint`
2. direct dictionary mutation creates a separate `endpoint` entry
3. normal lookup finds the class data descriptor first
4. invalid later assignment raises before replacing `_endpoint`

After failure, `config.endpoint` must still expose the last valid HTTPS value.

The property remains the best owner for the HTTPS rule because it is domain-specific to
one named boundary. If several attributes repeat only a shallow runtime-class check and
private-storage algorithm, promote that repeated portion to a descriptor. Do not force
the HTTPS meaning into a generic type descriptor.

Common wrong turn: saying the instance dictionary entry was ignored because its name was
private. It was not private; data-descriptor precedence decided normal lookup.

This proves ordinary lookup and assignment behavior. Deliberate mutation of `_endpoint`
can still bypass the property.

## Answer 4: add one reusable typed field

The predicted storage name is:

```text
_TypedField__channel
```

`__set_name__` derives it when class creation assigns the descriptor to `channel`.
`DeliveryConfig.channel` returns the descriptor; `instance.channel` reads the instance
storage.

The necessary evidence is:

- `DeliveryConfig.channel.spec().name == "channel"`
- two instances expose different channel values
- assigning an `int` raises `TypeError`
- reading before assignment raises `AttributeError`

Common wrong turn: storing the current value on `TypedField`. One descriptor object is
shared by every instance, so this leaks state.

Another wrong turn is claiming `TypedField(list)` supports `list[str]`. It checks only
the outer runtime class. Element validation, coercion, aggregated errors, or cross-field
rules require a richer explicit validation owner.

Annotations remain static declarations. The explicit `TypedField(str)` argument is the
runtime contract.

## Answer 5: audit the frozen surface

The state transition is:

```text
class already created
  -> decorator installs hooks
  -> constructor marks boundary open
  -> original initialization and original __setattr__ run
  -> successful return marks boundary closed
  -> ordinary rebinding/deletion raise FrozenSurfaceError
```

The strongest honest claim is:

> `surface_frozen` blocks ordinary top-level attribute rebinding and deletion after
> successful initialization for dictionary-backed instances.

It must also say:

- nested mutable values remain mutable
- `object.__setattr__` can bypass the boundary
- slotted-only instances are refused
- a subclass can override the mutation hook

Common wrong turn: treating those limitations as test gaps. They are tested parts of the
contract.

The decorator becomes the wrong owner when the requirement includes deep immutability,
slots support, sealed subclass behavior, tamper resistance, hash guarantees, or a
standard value-object contract. A standard frozen dataclass or a different explicit
model should be considered before metaclass escalation.

## Answer 6: explain the capstone escalation

The ownership table is:

| Concern | Owner | Timing | Evidence |
| --- | --- | --- | --- |
| action call shape and successful history | `@action` wrapper | call time and successful return | `action-wrapper`, trace, runtime tests |
| configuration value | `Field` descriptor | `__set_name__`, initialization, assignment/access | field manifest and field tests |
| plugin family construction | `PluginMeta` and `DefinitionNamespace` | namespace preparation and `type.__new__` | `class-creation`, registry tests |

`mark_class` can refuse a reserved attribute after it receives the finished class.
`DefinitionNamespace` can refuse a second tracked assignment at the moment of the second
write. After the body completes, the first ordinary value is gone, so a class decorator
cannot reconstruct the collision.

The class-creation report should show:

- `DefinitionNamespace`
- `PluginMeta`
- declared fields and actions
- inherited fields and actions
- whether `__init__` was generated
- visible class signature
- registration
- `constructed: false`
- `executed: false`

Common wrong turn: justifying `PluginMeta` because "plugins need automation." The actual
justification is timing plus family-wide ownership.

This report proves stored provenance agrees with the finished public class. The duplicate
definition test separately proves the prepared namespace observes information that the
finished class cannot expose.

## Final packet review

A strong packet answers six questions for every mechanism:

1. When did it run?
2. Which object owned the behavior?
3. Which public surface changed?
4. How could a reviewer inspect it?
5. Which failure or maintenance cost remained?
6. Why was the next stronger mechanism rejected or accepted?

Reject an answer that says only "the tests passed." The tests are evidence for named
claims, not replacements for the claims.

## Verification ledger

| Changed surface | Smallest first proof |
| --- | --- |
| class-decorator timing or collision | `test_class_customization_transformation.py` |
| dataclass, property, or descriptor packet | named test in `test_class_customization_evidence.py` |
| frozen-surface behavior | `test_frozen_surface_class_decorator.py` |
| capstone class provenance | class-creation runtime and CLI tests |
| saved capstone inspection | bundle-manifest tests |
| website lessons and diagrams | strict program documentation build plus generated HTML inspection |

Escalate to the broad course gate only after the focused route is green.

## Exit check

Before leaving Module 06, confirm you can:

- keep decorator expression timing separate from application timing
- distinguish generated code from runtime invariants
- prove property precedence from a conflicting instance entry
- identify descriptor versus instance storage
- state frozen limitations as contract rather than caveat
- justify the capstone metaclass from creation-time evidence

## Continue

- Previous: [Exercises](exercises.md)
- Return: [Overview](index.md)
- Next module: [Module 07](../module-07-descriptors-lookup-attribute-control/index.md)
- Terms: [Glossary](glossary.md)
