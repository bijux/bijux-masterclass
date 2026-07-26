# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Migration Governance Tool Boundaries"]
  page["Exercises"]
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

Use these after reading the five core lessons and the worked example. The goal is to make
your review and migration judgment visible, not to produce generic build advice.

Each exercise asks for three things:

- the stewardship question you are answering
- the evidence or review artifact you would rely on
- the change, rule, or boundary decision that follows from that evidence

For every migration proposal, include a proof bridge:

| Boundary moved | Before evidence | After evidence | Rollback point | New owner |
| --- | --- | --- | --- | --- |

Do not accept “tests pass” unless the named tests protect the contract being moved.

## Exercise 1: Write a first-pass build review

Choose one inherited Make-based repository. Write a short review that covers:

- public target meanings
- trusted outputs and their writers
- hidden inputs or stateful behavior
- one pressure finding from dry-run, trace, or serial/parallel comparison
- the top three risk classes you found

What to hand in:

- one page or less
- at least one concrete command you ran or would run
- the three risk classes in clear language such as graph truth, contract drift, or boundary
  risk

## Exercise 2: Sequence a safe migration

Pick one painful part of the build, such as release packaging, generated metadata, or test
orchestration. Design a migration plan that changes that part without deleting the old proof
surface too early.

What to hand in:

- the current contract in one sentence
- the smallest boundary move you would make first
- one proof surface you would preserve during the migration
- one retirement condition that must be true before the old route disappears

## Exercise 3: Write a governance note that could actually be enforced

Draft a short governance note for the repository. It should define:

- which targets are public
- what review bar applies to public-target changes
- one rule for new include files or macros
- one rule protecting proof surfaces

What to hand in:

- a note of six to ten lines
- wording another maintainer could apply during review
- one sentence explaining which kind of drift the note is meant to prevent

## Exercise 4: Diagnose one recurring antipattern

Pick one of these recurring smells:

- ritual target ordering instead of real edges
- multi-writer outputs
- opaque orchestration through wrappers
- meaningless stamps or manifests
- a release target that does too much

Explain how you would recognize it in a real repository and what the first honest recovery
move would be.

What to hand in:

- the antipattern name
- two signals that would confirm it
- the smallest repair you would try first
- one sentence on why that repair restores truth or ownership clarity

## Exercise 5: Make the tool-boundary argument

Choose one concern from a real build:

- compilation
- code generation
- packaging
- deployment
- release metadata
- remote publication

Argue whether Make should remain the owner, hand it off, or share it through a hybrid
boundary.

What to hand in:

- the concern you chose
- a one-paragraph argument
- the handoff artifact or interface if another tool becomes involved
- one sentence on what evidence would prove the boundary is working

## Exercise 6: Inventory target and output ownership

List every public target, its promised outputs or side effects, and the rule or external
system that owns them. Identify outputs with zero or multiple writers.

What to hand in:

- the inventory table
- the commands used to find callers and writers
- one ownership gap and one multi-writer risk

## Exercise 7: Write characterization checks

Before changing an inherited build, create durable checks for current package layout,
no-op convergence, and serial-versus-parallel agreement.

What to hand in:

- the three checks
- their initial results
- an explanation of which behavior is contractual and which observed defect should not be
  preserved

## Exercise 8: Turn governance prose into verification

Choose two governance rules, such as "CI calls only public targets" or "each trusted
output has one writer," and design automated checks for them.

What to hand in:

- the enforceable rule text
- the check command or test
- one passing and one deliberately failing example
- the review owner for changing the rule

## Exercise 9: Compare Make with a neighboring tool

Choose one real concern and compare Make with a workflow engine, package manager, CI
service, or deployment system. Evaluate file-graph fit, remote state, retries,
observability, and handoff artifacts.

What to hand in:

- a comparison table
- the ownership decision
- the exact interface between tools
- independent verification on both sides of the boundary

## Exercise 10: Produce a stewardship portfolio

Review one real Make-based repository from entrypoint to release boundary. Make one
bounded repair or boundary change while preserving proof and documenting ownership.

What to hand in:

- current-contract and risk review
- durable characterization checks
- the bounded change and its commit rationale
- before-and-after evidence
- governance rules and tool-boundary decision
- a maintainer handoff that states remaining risks honestly

## Mastery standard for this exercise set

Across all ten answers, the module wants the same habits:

- you review behavior before proposing rewrites
- you preserve proof while changing boundaries
- you write governance in enforceable language
- you name antipatterns in terms of truth loss or ownership drift
- you justify tool boundaries by modeling fit, not by novelty

If an answer says only "this build should be cleaned up," keep going.
