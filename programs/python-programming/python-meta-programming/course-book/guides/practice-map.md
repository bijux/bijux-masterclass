# Practice Map

<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Metaprogramming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Practice Map"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

Use this page to turn reading into deliberate practice. The course is strongest when
each concept is followed by one small proof, one capstone inspection, and one review
question.

## Practice loops by stage

### Modules 01-03

- print runtime identities, signatures, and namespaces
- explain what the inspection shows and what it does not guarantee

### Modules 04-06

- wrap one function and check whether signature, name, and docstring survive
- compare a function decorator, class decorator, and `@property` solution to the same problem

### Modules 07-08

- trace one attribute from descriptor declaration to per-instance storage
- identify whether validation happens at assignment, at construction, or too late

### Modules 09-10 and Mastery Review

- identify one invariant that truly belongs at class creation time
- reject at least one metaclass idea as better solved by a lower-power mechanism
- review one design choice for debuggability, security, and test isolation

## Capstone checkpoints

- read the manifest before invoking any plugin
- inspect the field schema before reading one descriptor implementation
- inspect the registry before reading the metaclass
- run the proof route after changing one configuration value
