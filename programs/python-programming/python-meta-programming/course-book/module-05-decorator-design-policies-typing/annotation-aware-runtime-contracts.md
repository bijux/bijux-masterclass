# Annotation-Aware Runtime Contracts


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Decorator Design Policies Typing"]
  page["Annotation-Aware Runtime Contracts"]
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

Annotation-aware decorators are one of the easiest places for a course to overpromise.

Type hints can help wrappers make clearer runtime decisions. They do not turn a decorator
into a full type system.

That is the boundary this page keeps explicit.
The page is also where the course needs to stop a common collapse in language: "uses type
hints" is not the same sentence as "enforces the typing story."

## The sentence to keep

When a decorator uses type hints at runtime, ask:

> what limited contract is this wrapper checking, and what part of the typing story is it
> deliberately refusing to claim?

That question keeps runtime validation honest.

Add one more question beside it:

> if this wrapper fails clearly on an unsupported hint, is that failure part of the design or an accidental limitation?

## The basic runtime pipeline

Annotation-aware wrappers typically combine:

- `typing.get_type_hints(func)` to resolve annotations
- `inspect.signature(func)` to understand the callable contract
- `sig.bind(*args, **kwargs)` to match actual arguments to parameter names

That sequence matters because it avoids guesswork:

- hints describe expected shapes
- signatures describe callable structure
- binding tells you what was actually passed

This is much stronger than trying to inspect raw `args` and `kwargs` ad hoc.

It also creates a clean review route:

| Evidence step | What it proves |
| --- | --- |
| `get_type_hints(func)` | what annotation surface the wrapper thinks it is reading |
| `inspect.signature(func)` | what callable structure the wrapper claims to respect |
| `sig.bind(*args, **kwargs)` | what values actually matched which parameters |

If any one of those steps is missing, the contract claim usually gets weaker fast.

## Run the three outcomes before reading the implementation

From `programs/python-programming/python-meta-programming`:

```bash
make decorator-policy-lab
```

Read the `validation` packet as three different contracts:

| Outcome | Timing | Did the wrapped function run? | Meaning |
| --- | --- | --- | --- |
| strict mismatch | call time, before delegation | no | the supported hint did not match |
| warning mismatch | call time, before delegation | yes | the mismatch was observed, not enforced |
| unsupported `list[int]` | decoration time | no callable exists yet | the validator refuses a hint outside its policy |

This table prevents two common mistakes: calling warning mode enforcement, and treating
unsupported annotations as though they had been checked.

## A partial validator is the right review target

For Volume I, the honest approach is a partial checker.

Good supported cases:

- plain runtime classes such as `int` or `str`
- `Union[...]` and `|` of supported types
- `Optional[T]` when `T` itself is supported
- `Any` as an explicit pass-through case

Cases that should be refused or left alone:

- parameterized generics such as `list[int]`
- protocol-heavy typing features
- the full semantics of `Annotated`, `Literal`, or other advanced typing constructs

This is not a weakness in the module. It is a design choice against pretending runtime
checks are broader than they really are.

Use this boundary table when the wrapper starts looking "smart":

| Supported surface | Why it stays in scope |
| --- | --- |
| plain runtime classes | Python can check them directly at runtime |
| `Union` and `Optional` over supported members | the rule is still readable and reviewable |
| `Any` passthrough | the wrapper is explicitly refusing to claim more |

| Refused surface | Why refusal is healthier here |
| --- | --- |
| parameterized generics | runtime semantics get subtle quickly |
| deep `Annotated` enforcement | metadata can become a hidden validation framework |
| advanced typing constructs with structural meaning | the wrapper would start overclaiming what it understands |

## One picture of the validation path

```mermaid
graph TD
  decorate["Decoration time"]
  cache["Cache signature and resolved hints"]
  callSite["Call time"]
  bind["Bind args and kwargs"]
  check["Check supported hints only"]
  delegate["Call original function"]
  decorate --> cache --> callSite --> bind --> check --> delegate
```

Caption: runtime annotation use is strongest when it stays narrow, explicit, and bound to the real call shape.

## Trace the shipped validator

Open `labs/decorator_policy/validation.py`. The public factory is small because three
helpers have separate jobs:

| Owner | Runs when | Responsibility |
| --- | --- | --- |
| `_validate_supported_hint` | decoration | recursively approve only `Any`, runtime classes, `Union`, and `Optional` |
| `_matches_hint` | call | compare a value with an already-approved hint |
| `validated` | factory, decoration, and call | capture policy, resolve hints, bind calls, and choose raise versus warn |

The separation is an invariant. `_matches_hint` is allowed to be compact only because
decoration-time validation has already refused every hint it cannot interpret.

The callable exposes two review surfaces:

- `__validation_policy__` names mismatch mode, return-check choice, and supported forms
- `__validated_hints__` shows the resolved annotations captured for that application

They make the added policy inspectable without reading closure cells. They are teaching
surfaces, not a request to standardize new dunder attributes across Python libraries.

That refusal is a review feature. Silent partial support is one of the fastest ways to
make a validator look more trustworthy than it really is. Refusing during decoration
also means an unsupported contract fails near its declaration instead of surprising the
first production caller.

## Bound arguments matter here too

This page depends directly on Module 03:

- binding gives you the interpreter-faithful mapping of parameter names to values
- defaults can be applied when the validator wants the complete view

Without binding, runtime validation often becomes a brittle mix of tuple indexing and
keyword guessing.

That is exactly the kind of shortcut this course is trying to avoid.

Binding also gives you a stronger answer when a learner asks "which argument failed?" The
validator can answer in parameter language instead of tuple-position folklore.

The strict lab test proves a default is applied before checking: `render("INC-42")`
validates both `incident_id="INC-42"` and `severity="warning"`. A bad
`incident_id=42` is rejected before `render` appends to its call log. This is observable
evidence that binding and validation precede delegation.

## Runtime type checks are not static typing

This module needs to say this plainly:

- runtime checks happen after code is already running
- they see only the values present at the boundary
- they do not provide the same guarantees as static analysis

So the strongest honest claim is:

> this decorator enforces a limited runtime contract at a narrow boundary.

That is a useful claim. It is not the same claim as "this program is type-safe."

Static analysis and this wrapper answer different questions:

| Question | Static checker | This runtime wrapper |
| --- | --- | --- |
| can a known call site pass an incompatible value? | often, before execution | only when that call executes |
| did an untyped external boundary deliver the expected simple runtime class? | not by observing the live value | yes, for the supported subset |
| is every element of `list[int]` an integer? | can reason from declared types | deliberately refuses the hint |
| does `warning` mode stop incompatible work? | not applicable | no |

## Common overclaims to reject

Reject these sentences when they appear in review or teaching notes:

| Overclaim | Better replacement |
| --- | --- |
| "this decorator enforces the type system" | "this decorator checks a narrow supported hint subset at runtime" |
| "unsupported hints are edge cases" | "unsupported hints mark the boundary where the wrapper refuses to pretend" |
| "warning mode is still safe enough" | "warning mode is observability, not enforcement" |
| "the hints already tell us everything we need" | "the wrapper still needs bound-call evidence and a named support policy" |

## `Annotated` and advanced hints need restraint

It is tempting to keep escalating:

- `Annotated` metadata as full validation rules
- parameterized generics as deep structural contracts
- richer typing constructs as runtime policy engines

That is exactly where a small validator starts turning into a separate validation
framework. Sometimes that is justified. Often it is a sign the decorator should stop
growing or hand off to a more explicit tool.

## Return checks happen after side effects

A parameter mismatch can be rejected before the wrapped function runs. A return
mismatch cannot: the value exists only after execution. The focused test
`test_strict_return_validation_runs_after_the_wrapped_function` proves the call counter
is already `1` when the decorator raises.

That timing matters for incident delivery. Rejecting a mislabeled return does not undo a
page that was already sent. Runtime return checking improves evidence; it is not a
transaction boundary.

## Failure modes for annotation-aware decorators

These are the mistakes to catch before approving the design:

| Failure mode | Why it weakens the wrapper | Repair move |
| --- | --- | --- |
| ad hoc inspection of `args` and `kwargs` | the wrapper can misidentify which parameter failed | bind through the signature first |
| half-supporting a hint surface silently | reviewers cannot tell what the contract really covers | refuse unsupported hints clearly |
| using warnings to imply enforcement | callers may believe the function was protected when it was not | describe warning mode as observation only |
| escalating the decorator into a validation framework by accident | the owner becomes too hidden and too broad | move richer rules into an explicit validator component |

## Smallest honest proof route

```bash
python -m unittest discover \
  -s tests \
  -p "test_decorator_policy_validation.py" \
  -v
```

The tests cover default binding, unions, optional values, `Any`, unsupported generics,
strict argument failure, return-check timing, warning behavior, invalid factory
configuration, policy inspection, metadata, and signature preservation. They do not
cover every object recognized by `typing`, nested container contents, protocols,
coercion, or business invariants.

## Capstone transfer: keep checking outside `@action`

Run:

```bash
make capstone-bind-action
make capstone-check-action
make capstone-action-wrapper
```

The capstone separates three responsibilities:

- binding proves call shape
- contract checking reports matches, mismatches, unsupported hints, and missing hints
- wrapper inspection proves which layer owns action metadata and signatures

`check-action` does not construct a plugin or invoke its action. It checks arguments
only, reports unsupported annotations instead of skipping them, and explicitly says
return values are outside its scope. Keeping this as an opt-in framework function avoids
turning every `@action` call into implicit partial type enforcement.

## Review rules for annotation-aware decorators

When reviewing annotation-aware wrappers, keep these questions close:

- what exact hint subset does the wrapper support?
- does the wrapper use `get_type_hints` plus signature binding instead of ad hoc argument guessing?
- is unsupported typing surface rejected clearly instead of half-supported?
- does the review describe the result as a partial runtime contract rather than as full typing?
- has the decorator grown large enough that a dedicated validator object or framework would be clearer?
- can another reviewer name the exact supported hint subset without reading between the lines?

## Exit check for this page

Before moving on, make sure you can do all of these:

- explain why binding is stronger than inspecting raw argument tuples directly
- name one supported hint surface and one refused surface without hedging
- reject one sentence that overstates runtime validation as type safety
- state when the decorator should stop growing and hand validation off to a clearer owner

## What to practice from this page

Try these before moving on:

1. Add `float` to a union already supported by a lab function and prove both the new
   success route and the existing failure route.
2. Add a `dict[str, int]` annotation and predict whether refusal occurs during
   decoration or invocation before running the test.
3. Add an intentionally wrong return and prove the body ran before rejection.
4. Explain one external runtime boundary where this partial validator helps and one
   internal call graph where static analysis should do the heavy lifting.

If those feel ordinary, the next step is cache policy, where wrapper state becomes visible,
inspectable, and operationally significant.

## Continue through Module 05

- Previous: [Resilience and Control-Flow Wrappers](resilience-and-control-flow-wrappers.md)
- Next: [Cache Policy and lru_cache Behavior](cache-policy-and-lru-cache-behavior.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
