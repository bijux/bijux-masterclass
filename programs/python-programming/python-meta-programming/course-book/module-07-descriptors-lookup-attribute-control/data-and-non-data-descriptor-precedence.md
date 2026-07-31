# Data and Non-Data Descriptor Precedence

<!-- page-maps:start -->
## Page Maps

```mermaid
flowchart TD
  class["Static class value"] --> kind{"Descriptor kind?"}
  kind -->|data| data["Descriptor wins before instance state"]
  kind -->|non-data| state{"Same public name in instance dictionary?"}
  state -->|yes| instance["Instance value wins"]
  state -->|no| nondata["Descriptor __get__ runs"]
```
<!-- page-maps:end -->

The protocol core identified which hooks exist. This core uses that classification to
predict an ordinary instance read before executing it.

The storage owners do not change when lookup precedence changes:

```mermaid
flowchart TD
  class["Delivery class"] --> data["shared data descriptor"]
  class --> nondata["shared non-data descriptor"]
  first["first Delivery instance"] --> firstdict["first instance dictionary"]
  second["second Delivery instance"] --> seconddict["second instance dictionary"]
  data -.reads or writes.-> firstdict
  data -.reads or writes.-> seconddict
  firstdict -.may shadow.-> nondata
  seconddict -.may shadow.-> nondata
```

## The claim

A data descriptor wins over a same-named instance dictionary entry. A non-data descriptor
yields to that entry.

The distinction is not based on the value's purpose:

- `__set__` or `__delete__` makes it a data descriptor
- `__get__` without those hooks makes it a non-data descriptor

## Build the conflict deliberately

The lab creates this class:

```python
class Delivery:
    enforced = StoredField()
    shadowable = ShadowableValue("descriptor-value")
    category = "class-value"
```

Then it places two kinds of state on one instance:

```python
delivery.enforced = "descriptor-storage"
vars(delivery)["enforced"] = "same-name-instance-value"
vars(delivery)["shadowable"] = "instance-value"
```

`StoredField.__set__` wrote the managed value under `_enforced`. The explicit `vars`
assignment added a conflicting public entry named `enforced`. Both values exist, so the
read has to reveal the actual precedence rule.

## Predict without executing

`explain_lookup` first uses `inspect.getattr_static`:

```python
static_value = inspect.getattr_static(Delivery, "enforced")
```

Unlike `getattr`, this does not call `__get__`. The helper can therefore inspect the
owner before producing a prediction:

```python
if protocol.kind == "data":
    winner = "data-descriptor"
elif name in vars(instance):
    winner = "instance-dictionary"
elif protocol.kind == "non-data":
    winner = "non-data-descriptor"
else:
    winner = "class-attribute"
```

Run:

```bash
make descriptor-lookup-lab
```

The `precedence.decisions` packet predicts:

| Name | Static kind | Same public instance name? | Winner |
| --- | --- | --- | --- |
| `enforced` | data descriptor | yes | data descriptor |
| `shadowable` | non-data descriptor | yes | instance dictionary |
| `category` | plain class value | no | class attribute |

The packet then records the actual reads so prediction and execution stay separate.

## Trace the data-descriptor read

For `delivery.enforced`:

1. Python finds `StoredField` through `Delivery`'s MRO.
2. `StoredField`'s type defines `__set__`.
3. The object is therefore a data descriptor.
4. Its `__get__` runs before Python considers `vars(delivery)["enforced"]`.
5. `__get__` reads `_enforced` and returns `"descriptor-storage"`.

The conflicting public instance entry still exists. It simply does not win ordinary
lookup.

## Trace the non-data read

For `delivery.shadowable`:

1. Python finds `ShadowableValue` through the MRO.
2. Its type defines `__get__` but not `__set__` or `__delete__`.
3. The object is a non-data descriptor.
4. Python checks the instance dictionary before calling its `__get__`.
5. The public instance entry returns `"instance-value"`.

Remove that instance entry and `ShadowableValue.__get__` wins again.

## Why a read-only property still wins

A property without a user-defined setter can feel read-only, but the `property` type
still supplies descriptor write machinery. Classification depends on the type's hooks,
not on whether a particular assignment succeeds.

This is why:

```python
vars(obj)["name"] = "attempted shadow"
```

does not normally bypass a read-only property. The property is a data descriptor and is
consulted before the same-named instance entry.

## Why this does not justify subtle APIs

Precedence can explain an outcome without making the design kind.

If users must know that one class attribute is data and another is non-data merely to
assign ordinary values safely, the public API may be too surprising. Use the rule for
prediction and review, not as permission to make shadowing part of an undocumented
contract.

## Limits of the lab predictor

`explain_lookup` deliberately claims only ordinary lookup:

- it assumes the default `object.__getattribute__` model
- it does not execute `__getattr__`
- it does not reproduce a custom `__getattribute__`
- it does not model class lookup controlled by a custom metaclass

The `ordinary_lookup_only` evidence field keeps that limit machine-visible.

## Capstone connection

Every capstone `Field` defines `__get__` and `__set__`, so it is a data descriptor.
Generated initialization uses public assignment:

```python
setattr(plugin, field.name, raw_value)
```

That routes through `Field.__set__`, which coerces and stores under a private name.
Later `plugin.endpoint` reads cannot be replaced by placing a public `endpoint` entry in
the instance dictionary. The data descriptor remains the owner.

This gives the capstone field system a strong invariant, but not an unlimited one:
direct mutation of the private storage name or `object.__setattr__` can still bypass
parts of a public convention.

## Focused proof

Run:

```bash
python3 -m unittest discover -s tests \
  -p "test_descriptor_precedence_lab.py" -v
```

The tests include both sides of the conflict and a no-instance-entry non-data case.

## Exit check

Before continuing, explain all three results without running them:

```python
delivery.enforced
delivery.shadowable
delivery.category
```

Your explanation must name the static class value, its category, whether the public name
exists in the instance dictionary, and the winning layer.

## Continue through Module 07

- Previous: [Descriptor Protocol and `__set_name__`](descriptor-protocol-and-set-name.md)
- Next: [Functions, Binding, and Method Descriptors](functions-binding-and-method-descriptors.md)
