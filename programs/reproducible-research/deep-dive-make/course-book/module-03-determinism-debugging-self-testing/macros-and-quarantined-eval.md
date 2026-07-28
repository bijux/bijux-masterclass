# Macros and Quarantined Eval

Make can generate repeated text and rules. That power is useful only when the generated
graph is easier to verify than the duplication it replaces. This lesson builds the
reasoning model first, then gives `eval` a narrow acceptance test.

## Page maps

```mermaid
graph LR
  course["Deep Dive Make"] --> module["Determinism, Debugging, and Self-Testing"]
  module --> page["Macros and Quarantined Eval"]
  page --> proof["Explicit/generated equivalence proof"]
```

```mermaid
flowchart LR
  invariant["repeated invariant"] --> text["macro template"]
  text --> call["call with named input"]
  call --> expand["first expansion"]
  expand --> parse["eval parses generated Make syntax"]
  parse --> graph["inspectable bounded graph"]
```

If you cannot describe the first expansion and the parsed result separately, the
abstraction is not yet reviewable.

## Begin with the explicit rules

Suppose two reports share one rule shape:

```make
build/alpha.txt: src/alpha.txt
	@mkdir -p $(@D)
	cp $< $@

build/bravo.txt: src/bravo.txt
	@mkdir -p $(@D)
	cp $< $@
```

The repeated invariant is clear:

- each output has one corresponding source;
- the output directory exists before copying;
- automatic variables connect the chosen rule to its paths.

Keep explicit rules when the family is small, when members differ materially, or when
generated syntax would cost more review time than duplication.

## Use a macro for text generation

A multi-line recursively expanded variable can hold the rule template:

```make
define copy_rule
build/$(1).txt: src/$(1).txt
	@mkdir -p $$(@D)
	cp $$< $$@
endef
```

`$(call copy_rule,alpha)` binds `$(1)` to `alpha`. The doubled dollar signs preserve
automatic variables through the first expansion so the parsed recipe can evaluate them
when its target runs.

The macro is not a rule by itself. It is text that can become rule syntax.

## Understand the two expansions

This line creates rules:

```make
$(eval $(call copy_rule,alpha))
```

Conceptually:

```text
template text
  -> call expands parameters and one dollar layer
  -> eval parses the expanded text as Makefile syntax
  -> recipe later expands automatic variables for the selected target
```

`eval` expands its argument, parses the result, and expands to an empty string. Dollar
escaping is therefore not cosmetic. Losing one layer can make `$@` or `$<` disappear
before a rule ever runs.

Use a tiny probe when learning:

```make
$(info GENERATED=$(call copy_rule,alpha))
```

Read the emitted text before asking `eval` to parse it. Remove the probe after the model
is clear.

## Generate a finite family

```make
REPORTS := alpha bravo

$(foreach report,$(REPORTS),\
  $(eval $(call copy_rule,$(report))))
```

The family is reviewable because:

- membership comes from one finite, deterministic list;
- each member maps to one predictable target and prerequisite;
- one include can own the template;
- the explicit equivalent is easy to write;
- the resulting targets can be inventoried.

Do not generate target names from ambient shell state or an unbounded workspace scan.
Metaprogramming magnifies discovery defects.

## Compare explicit and generated surfaces

Create two isolated Makefiles: one with the explicit rules and one with the generated
family. For each, capture:

```sh
gmake -pRrq build/alpha.txt > explicit-or-generated.database.txt
gmake -n build/alpha.txt
```

Compare:

| Surface | Expected equivalence |
| --- | --- |
| target name | `build/alpha.txt` |
| prerequisite | `src/alpha.txt` |
| planned recipe | create directory, then copy source to target |
| clean build artifact | same path and content |
| second-run query | exit zero |
| changed-source behavior | only corresponding target becomes stale |

The Make database contains formatting and metadata beyond this table. Compare the
contract, not raw database bytes.

## Keep expansion-time failures attributable

Validate macro inputs near the call:

```make
define copy_rule
$(if $(strip $(1)),,$(error copy_rule requires a report name))
build/$(1).txt: src/$(1).txt
	@mkdir -p $$(@D)
	cp $$< $$@
endef
```

This fails while Make evaluates the generated surface and names the violated invariant.
It is preferable to generating malformed target names that fail later for unclear
reasons.

Other useful invariants include:

- member names contain only the allowed path characters;
- two members cannot produce the same target;
- generated targets stay under one owned output root;
- every generated member has a corresponding declared source;
- the family does not redefine a public target.

Validation is part of the abstraction, not an optional comment.

## Quarantine ownership

A bounded layout might be:

```text
Makefile
mk/
├── core.mk
├── report-rules.mk
└── optional-generated-rules.mk
```

The generated surface should have one obvious owner. In this course, optional
metaprogramming is deliberately separated from the core graph so a learner can inspect
and test the ordinary build first.

An explicit switch makes activation visible:

```make
USE_GENERATED_RULES ?= no

ifeq ($(USE_GENERATED_RULES),yes)
include mk/optional-generated-rules.mk
else ifneq ($(USE_GENERATED_RULES),no)
$(error USE_GENERATED_RULES must be yes or no)
endif
```

The switch needs validation. A typo should not silently select an accidental behavior.

## Define what “optional” means

An optional generated surface must satisfy all of these:

| Claim | Evidence |
| --- | --- |
| core requests work while disabled | normal build and selftest with switch off |
| enabled targets are finite | expected target inventory |
| generated targets are inspectable | bounded database and dry-run evidence |
| enabling does not redefine core meaning | core target comparison |
| disabling removes only the optional surface | absent optional targets and unchanged core artifacts |
| failures name their owner | invalid member/switch rejection |

“The file is in a separate include” proves location, not optionality.

## Test both states

Use independent workspaces when generated and explicit modes could share outputs:

```sh
gmake USE_GENERATED_RULES=no selftest
gmake USE_GENERATED_RULES=yes -n generated-demo
```

For a real migration from explicit to generated rules, compare both implementations over
the same governed fixture:

1. clean build with explicit rules;
2. inventory declared artifacts;
3. clean build with generated rules;
4. compare declared identities and target behavior;
5. mutate one member source;
6. confirm only its corresponding output becomes stale;
7. run the rejection cases for invalid or duplicate members.

A passing happy path is not enough; the abstraction must reject an invalid family.

## Know when a macro is enough

Not every repeated idea needs generated rules. Macros can enforce small invariants:

```make
require_value = $(if $(strip $($(1))),,$(error required variable $(1) is empty))

$(call require_value,PYTHON)
```

Use a macro when it removes repeated policy or validation while leaving rules visible.
Use a generated-rule family only when target repetition is genuinely the owned problem.

## Reject expensive abstraction

Reject or replace the design when:

- a reader must mentally execute nested `foreach`, `call`, and `eval` layers to find one
  prerequisite;
- target membership comes from volatile parse-time state;
- generated rules redefine targets owned elsewhere;
- automatic-variable escaping is unexplained and untested;
- disabling the surface breaks unrelated core targets;
- database inspection produces an unbounded family;
- the abstraction has no invalid-input test;
- ordinary explicit or static pattern rules express the same contract more clearly.

Static pattern rules are often a useful middle ground:

```make
REPORTS := alpha bravo
OUTPUTS := $(addprefix build/,$(addsuffix .txt,$(REPORTS)))

$(OUTPUTS): build/%.txt: src/%.txt
	@mkdir -p $(@D)
	cp $< $@
```

This keeps the finite target set visible without a second parse through `eval`.

## Review record

For one abstraction, preserve:

```text
Repeated invariant:
Explicit equivalent:
Generated member source:
Expected target inventory:
Expansion layers:
Core behavior with surface disabled:
Enabled dry-run/database evidence:
Artifact comparison:
Invalid-input rejection:
Decision and limit:
```

That record lets a later maintainer judge the review cost rather than inheriting a vague
claim that the macro “reduces duplication.”

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain the separate `call`, `eval`, parse, and recipe-expansion moments;
- preserve automatic variables through generated rule text;
- compare a generated family with its explicit equivalent;
- bound membership and output ownership;
- prove that an optional surface does not control the core build;
- choose a macro or static pattern rule when `eval` adds no teaching or maintenance
  value;
- reject generated rules with unclear membership, ownership, or failure evidence.
