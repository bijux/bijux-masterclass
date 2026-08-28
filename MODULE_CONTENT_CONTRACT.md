# Module Content Contract

Every completed module is exactly one Markdown file at the path declared in `manifests/modules.csv`.

## Required front matter

```yaml
---
module_id: PLS-001
program: Programming Languages & Semantics
level: 1
module_number: 1
title: Programs, Languages, and Observable Behavior
status: complete
last_verified: YYYY-MM-DD
---
```

## Required chapter order

1. **One-Page Review**
2. **Governing Question**
3. **Why This Matters**
4. **Prerequisites and Retrieval**
5. **Learning Objectives**
6. **Core Exposition**
7. **Definitions and Notation**
8. **Mechanisms, Invariants, or Proof Structure**
9. **Alternatives and Trade-Offs**
10. **Failure Modes and Misconceptions**
11. **Ten Worked Examples**
12. **Cross-Program Connections**
13. **References**
14. **Five Exercises**
15. **Answers to the Five Exercises**

The answers must be the final substantive section in the file.

## One-Page Review

The chapter begins with a dense review sheet designed to fit approximately one printed page when rendered compactly.

It must contain:

- the governing question;
- essential definitions;
- the central mechanism or theorem;
- critical invariants;
- common failure modes;
- one compact example;
- links to prerequisite and successor modules.

This review is embedded in the module. It is not a separate file.

## Exposition standard

The exposition must be sufficient for self-study.

It must:

- begin from first principles without becoming childish;
- define every term used as a term of art;
- derive claims rather than merely announce them;
- distinguish model, guarantee, mechanism, implementation, and policy;
- show where assumptions enter;
- explain competing approaches and their consequences;
- connect formal reasoning to real systems;
- identify what has changed in current practice;
- remain useful after the named tools change.

External readings may deepen the module but may not be required to understand it.

## Worked examples

Every module contains exactly **10 numbered worked examples**.

Each example must have:

- a concrete question or situation;
- a fully worked line of reasoning;
- an explicit conclusion;
- a different pedagogical purpose.

Across the ten examples, include an appropriate mix of:

- minimal examples;
- boundary cases;
- counterexamples;
- failure cases;
- implementation traces;
- formal derivations;
- design comparisons;
- production situations.

Renaming ten nearly identical examples does not satisfy the contract.

## Exercises and answers

Every module contains exactly **5 numbered exercises** and exactly **5 corresponding answers**.

The exercises should progress from retrieval to transfer:

1. precise understanding;
2. mechanism tracing or derivation;
3. implementation or diagnosis;
4. comparison or design;
5. unfamiliar transfer problem.

Answers must be complete enough for independent correction. “Answers may vary” is not acceptable without a model answer and evaluation criteria.

## Code and mathematics

When code is relevant:

- use the language most natural to the concept;
- keep examples executable where practical;
- include expected output or behavior;
- test code snippets when a suitable local toolchain exists;
- state when code is intentionally schematic.

Every fenced block must be preceded immediately by a single-line JSON annotation.
Executable Python uses this shape:

````markdown
<!-- bijux-verify: {"id":"sum-values","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"6\n","stderr":""}} -->
```python
print(sum([1, 2, 3]))
```
````

`mode` is `run` or `compile` for executable code. The `expect` object always
declares `exit_code` and may declare exact `stdout` or `stderr`, or
`stdout_contains` or `stderr_contains` checks. Supported execution routes are
explicitly registered; an unknown language or toolchain is unavailable, not an
implicit pass.

Intentionally non-executable blocks use `schematic` or `data`, set `toolchain` to
`none`, and explain why execution is inapplicable:

````markdown
<!-- bijux-verify: {"id":"ownership-graph","mode":"schematic","language":"text","toolchain":"none","reason":"the diagram describes a relationship rather than a program"} -->
```text
owner -> resource -> observer
```
````

The verifier extracts executable snippets and writes source files, commands,
toolchain versions, outputs, expectations, and pass/fail/skipped/unavailable
status under `artifacts/snippets/<MODULE_ID>/`. A skipped schematic or data block
is acceptable only because its reason is explicit; an unavailable executable
route prevents completion.

When mathematics is relevant:

- define notation;
- show intermediate steps;
- distinguish proof, proof sketch, intuition, and empirical evidence.

## Citations and currency

Each module must use:

- authoritative textbooks for durable foundations;
- primary papers for research claims;
- official standards and documentation for current protocols and tools;
- publication or version dates where currency matters.

Current claims must be verified at authoring time.

Do not copy long passages. Explain in original language and cite sources.

## Prohibited content

A module must not be:

- a title and outline;
- a list of links;
- an unedited AI dump;
- a product tutorial without durable concepts;
- a giant lab or capstone;
- a disguised multi-module chapter;
- duplicated from another program;
- padded to a line count;
- dependent on generated images.

ASCII diagrams, tables, equations, and Mermaid diagrams may be used when they clarify the material.

## Completion evidence

A module is complete only when:

- the required sections exist in order;
- all 10 examples are substantive;
- all 5 exercises have complete answers;
- local links resolve;
- code and formulas have been reviewed;
- citations are verified;
- the module passes structural and content review;
- the manifest status changes from `planned` to `complete`;
- the module and manifest update are committed atomically.
