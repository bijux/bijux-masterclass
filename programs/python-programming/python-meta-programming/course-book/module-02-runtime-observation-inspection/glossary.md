# Module Glossary

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Runtime Observation Inspection"]
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

This glossary belongs to **Module 02: Safe Runtime Observation and Inspection** in
**Python Metaprogramming**. It keeps the language of this directory stable so the same
ideas keep the same names across lessons, practice, and capstone discussion.

## How to use this glossary

Use the glossary when a discussion starts to blur together discovery, storage, lookup,
and execution. Module 02 is meant to replace vague phrases like "I just inspected it"
with explicit observation language.

When a learner cannot explain which truth they are after, this glossary is the reset
point. Most weak answers in this module happen because someone mixes up one of these
boundaries:

- names that look reachable
- state that is actually stored
- objects attached under a name
- values produced only after runtime lookup executes

## Terms in this directory

| Term | Meaning in this directory |
| --- | --- |
| Attachment truth | What object is attached at a name before normal runtime resolution executes. Static lookup is often the safest first tool for this question. |
| Attribute protocol | The runtime machinery behind attribute access, including `__getattribute__`, descriptors, and `__getattr__`. |
| Best-effort discovery | The fact that `dir(obj)` is a discovery aid rather than a complete contract about what lookup can resolve. |
| Callable category | The concrete callable family involved in an example, such as function, bound method, class, or callable instance. Naming the category keeps `callable(obj)` from sounding more informative than it is. |
| Call protocol | The runtime behavior that makes an object callable. It depends on the object's type-level support for invocation. |
| Callable object | Any object for which `callable(obj)` is true, including functions, classes, bound methods, and callable instances. |
| Diagnostic execution risk | The risk that a debugging or inspection tool runs business behavior while trying to observe runtime structure. |
| Dynamic lookup | Normal attribute resolution through `getattr(obj, name)` or dot syntax, which may execute descriptors and lookup hooks. |
| Exact type check | A check such as `type(obj) is T` that rejects subclasses and asks for one concrete runtime type. |
| Execution truth | What ordinary runtime behavior actually produces when lookup or invocation is allowed to run normally. |
| Inheritance-aware question | A review question that cares whether an object can participate through subclass, ABC, or protocol-style relationships rather than exact identity alone. |
| Least-risk workflow | An inspection order that starts with the safest structural evidence and only moves into execution when earlier evidence cannot answer the real question. |
| Polymorphic type check | A check such as `isinstance(obj, T)` that accepts objects through subclass or ABC relationships. |
| Resolved value truth | The value returned by normal dynamic lookup after descriptors, `__getattribute__`, and fallback hooks have had a chance to run. |
| Reviewable inspection packet | A small bundle of question, tool choice, evidence, and design judgment that another learner can audit without guessing what happened. |
| Subclass rejection rule | The explicit reason an exact-type check refuses subclasses. If you cannot name this rule, the exact check is probably not justified. |
| Static lookup | Observation through `inspect.getattr_static`, which inspects the attached attribute object without normal protocol execution. |
| Stored state | The state physically stored on the object, usually through `__dict__` or slot-backed storage. |
| Visible names | Candidate attribute names discovered through a tool like `dir(obj)`. |
| `__dict__`-backed state | Per-object storage represented by an attribute dictionary. |
| `__slots__` | A class declaration that gives instances a fixed storage layout and often removes the default instance dictionary. |
| `dir(obj)` | A best-effort name discovery tool that may draw from instance, class, MRO, and custom `__dir__` behavior. |
| `getattr(obj, name)` | Dynamic attribute access that runs the normal lookup protocol and may execute code. |
| `getattr(obj, name, default)` ambiguity | The fact that a default result can blur together a truly missing attribute and an internal `AttributeError` raised during lookup. |
| `hasattr(obj, name)` | A convenience wrapper around dynamic lookup that treats `AttributeError` as absence and therefore can still execute code. |
| `inspect.getattr_static` | A tooling-oriented lookup function that returns the raw attached attribute object without normal dynamic resolution. |
| `isinstance(obj, T)` | A polymorphic runtime classification check for objects. |
| `issubclass(C, T)` | A polymorphic runtime classification check for class relationships. |
| `mappingproxy` | A read-only view of a class namespace, commonly exposed through `cls.__dict__` on CPython. |
| `type(obj)` | The exact runtime class of an object. |
| Value resolution | The act of asking what ordinary runtime lookup would produce, not just what names or stored state are present. |

## Common boundary repairs

Use these when your wording starts to drift:

| If you say... | Rewrite it as... |
| --- | --- |
| "I inspected the attribute." | "I used static lookup to inspect the attached object under the attribute name." |
| "I checked whether it exists." | "I used best-effort discovery for candidate names" or "I used dynamic lookup to see whether runtime resolution produced a value." |
| "I used `type` to be precise." | "I used an exact-type check because I needed to reject subclasses that change this behavior." |
| "I know it is callable." | "I know the runtime will permit a call attempt, but I do not yet know whether the call is valid or safe." |

## Keep the module connected

- Return to [Module 02 Overview](index.md) for the full learning route.
- Use [Exercises](exercises.md) and [Exercise Answers](exercise-answers.md) to pressure-test the vocabulary.
- Revisit the [Worked Example](worked-example-building-a-safer-debug-printer.md) when an inspection tool starts to blur observation and execution.
