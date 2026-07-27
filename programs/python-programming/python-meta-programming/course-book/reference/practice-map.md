# Practice Map


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Reference"]
  page["Practice Map"]
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

Use this page when you finished a module and need to decide what to do next in a way that
actually deepens understanding.

Good practice in this course is not random repetition. It is a loop:

1. practice one mechanism or judgment skill
2. prove one claim concretely
3. cross into one capstone surface only after the module-level loop is stable

## How to use this map

- Start from the module you just finished.
- Choose one primary practice task.
- Choose one proof loop.
- Choose one capstone follow-up only after the first two are clear.

That order stops the capstone from becoming a substitute for learning.

## Module practice map

| Module | Best primary practice | Best proof loop | Best capstone follow-up |
| --- | --- | --- | --- |
| 01 | object-model inspection exercises | explain one runtime fact without changing behavior | inspect manifest and registry outputs |
| 02 | inspection and introspection comparison labs | compare what different tools can observe honestly | inspect public runtime evidence before touching wrappers |
| 03 | signature and provenance exercises | preserve metadata while adding evidence | inspect callable surfaces and saved outputs |
| 04 | thin-wrapper refactors | wrap one function while keeping names, docs, and blame legible | inspect action wrappers and tests |
| 05 | decorator-policy comparisons | compare policy-in-decorator versus explicit composition | inspect decorator seams and review routes |
| 06 | class-customization labs | solve a class problem without escalating to metaclasses yet | inspect framework edges before class-creation hooks |
| 07 | descriptor exercises | give one attribute rule an explicit owner and prove lookup behavior | inspect field descriptors and focused tests |
| 08 | descriptor-system design labs | compare one descriptor to a reusable field framework | inspect validation and constructor behavior |
| 09 | metaclass escalation reviews | write down the lower-power tool that almost worked before using a metaclass | inspect registration and class-creation routes |
| 10 | runtime governance review | justify one mechanism choice against the whole power ladder | use the capstone as the final review specimen |

## Reusable loops

- observation loop: inspect shape first, explain what changed, then decide whether transformation was necessary
- escalation loop: name the lowest honest tool, the invariant it failed to own, and the new risk introduced by the stronger one
- governance loop: explain what another reviewer should still understand one file at a time

## If you are stuck

| If you are stuck on... | Return to... | Before moving on, be able to... |
| --- | --- | --- |
| observation versus execution | Modules 01 and 02 | say what can be inspected without triggering behavior |
| wrapper honesty | Modules 03 through 05 | name which callable facts survived the wrapper |
| attribute ownership | Modules 06 through 08 | explain why the rule belongs on attribute access |
| class-creation escalation | Modules 06 and 09 | name the lower-power tool that almost worked |
| runtime governance | Module 10 and the capstone | defend one mechanism choice with a proof route |

## Good stopping point

Leave this page when you can choose:

- one module-level practice task
- one proof loop
- one capstone follow-up

without defaulting to "just read more" or "just run the whole capstone."
