# Module 05: Portability, Hermeticity, and Failure Modes


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Portability Hermeticity Failure Modes"]
  page["Module 05: Portability, Hermeticity, and Failure Modes"]
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

Modules 01 to 04 teach graph truth, parallel safety, determinism, and exact Make
semantics. Module 05 asks a harder question:

> what assumptions about the machine, shell, tools, and environment are you willing to
> trust, and which ones must be modeled explicitly?

This is the module where a build stops being "correct on my machine" and starts becoming a
declared contract.

## Plan for the day

| Time | Activity | Evidence you keep |
| --- | --- | --- |
| 45 minutes | Run a toolchain and environment audit | a `doctor` report from two environments |
| 75 minutes | Read the portability and recursion lessons | a written support contract |
| 60 minutes | Build a convergent environment manifest | two identical no-op runs |
| 60 minutes | Separate Make overhead from recipe cost | timings and a trace-line count |
| 90 minutes | Harden the inherited-build example | a repaired graph and boundary decision |
| 90 minutes | Complete the ten exercises | commands, observations, and explanations |

If you have only one hour, run the environment audit in the worked example, read the
portability contract, and complete Exercises 1, 6, and 7. Return for recursion,
measurement, and tool boundaries when you can test them rather than merely read about
them.

## What this module is for

By the end of Module 05, you should be able to explain five things clearly:

- which parts of the toolchain and shell are required, optional, or unsupported
- how recursion stays bounded and jobserver-aware under `-j`
- which non-file inputs change artifact meaning and how to model them honestly
- how to measure Make overhead instead of guessing about performance
- when a failure is a repairable Make problem and when it points to a tool boundary

## Sort assumptions into three contracts

Do not put every environmental fact into one stamp. Classify it first:

| Kind | Example | Build response |
| --- | --- | --- |
| required capability | GNU Make 4.3, `python3`, POSIX shell | detect early and fail with a useful message |
| semantic input | compiler, flags, target architecture | record stable evidence and make outputs depend on it |
| diagnostic context | hostname, current time, terminal color | report separately; do not destabilize artifact identity |

This distinction prevents two opposite mistakes. Ignoring a semantic input creates stale
outputs. Recording every volatile diagnostic as an input creates endless rebuilds.

For one build you know, write at least two facts in each row. If you cannot decide where
a fact belongs, ask: “Could changing this fact change the bytes or meaning of a declared
artifact?” A yes usually indicates a semantic input. A no may still matter for debugging,
but it should not automatically control freshness.

## Study route

```mermaid
flowchart TD
  start["Overview"] --> core1["Portability Contract and Version Gates"]
  core1 --> core2["Jobserver and Controlled Recursion"]
  core2 --> core3["Modeling Non-File Inputs and Stamps"]
  core3 --> core4["Performance Measurement and Make Overhead"]
  core4 --> core5["Failure Modes and Tool Boundaries"]
  core5 --> example["Worked Example: Hardening an Inherited Build"]
  example --> practice["Exercises"]
  practice --> answers["Exercise Answers"]
  answers --> glossary["Glossary"]
```

Read the module in that order the first time. Later, return directly to the page that
matches the incident or design boundary you are facing.

## The ten files in this module

1. Overview (`index.md`)
2. [Portability Contract and Version Gates](portability-contract-and-version-gates.md)
3. [Jobserver and Controlled Recursion](jobserver-and-controlled-recursion.md)
4. [Modeling Non-File Inputs and Stamps](modeling-non-file-inputs-and-stamps.md)
5. [Performance Measurement and Make Overhead](performance-measurement-and-make-overhead.md)
6. [Failure Modes and Tool Boundaries](failure-modes-and-tool-boundaries.md)
7. [Worked Example: Hardening an Inherited Build](worked-example-hardening-an-inherited-build.md)
8. [Exercises](exercises.md)
9. [Exercise Answers](exercise-answers.md)
10. [Glossary](glossary.md)

## How to use the file set

| If you need to... | Start here |
| --- | --- |
| define the minimum supported Make, shell, and tools | [Portability Contract and Version Gates](portability-contract-and-version-gates.md) |
| make recursion behave under parallel execution | [Jobserver and Controlled Recursion](jobserver-and-controlled-recursion.md) |
| model environment facts without lying about reproducibility | [Modeling Non-File Inputs and Stamps](modeling-non-file-inputs-and-stamps.md) |
| understand whether Make overhead is actually the bottleneck | [Performance Measurement and Make Overhead](performance-measurement-and-make-overhead.md) |
| classify a failure and decide whether Make is still the right tool | [Failure Modes and Tool Boundaries](failure-modes-and-tool-boundaries.md) |
| see the whole module in one incident narrative | [Worked Example: Hardening an Inherited Build](worked-example-hardening-an-inherited-build.md) |
| test your own understanding | [Exercises](exercises.md) |
| compare your reasoning against a reference answer | [Exercise Answers](exercise-answers.md) |
| stabilize the module vocabulary | [Glossary](glossary.md) |

## The running question

Carry this question through every page:

> if this build changes behavior on another machine or another run, which assumption moved
> and where is that assumption declared?

Good Module 05 answers usually mention one or more of these:

- an undeclared portability boundary
- recursion that escaped the jobserver budget
- a non-file input that was real but unmodeled
- performance claims made without measurement
- a failure mode that should have forced a tool-boundary decision earlier

## Commands to keep close

These commands form the evidence loop for Module 05:

```sh
make -n all
make --trace all
make -p
make all && make -q all
/usr/bin/time -p make -n all
```

Use them on purpose. Hardening work becomes sloppy when measurement and proof get replaced
with suspicion.

## Learning outcomes

By the end of this module, you should be able to:

- publish a portability contract instead of relying on workstation folklore
- keep recursive Make under the same parallel budget and make that behavior inspectable
- model non-file inputs as explicit build facts without contaminating artifacts
- produce at least one meaningful performance measurement before proposing a performance fix
- explain when Make should remain the orchestrator and when another tool should take over

## Exit standard

Do not move on until all of these are true:

- you can name the required Make and shell features without hedging
- you can explain how a recursive sub-make receives parallel budget
- you can model one non-file input using a convergent stamp or manifest
- you can produce one timing or trace-volume metric and explain what it means
- you can classify one failure as a Make repair, a tool boundary, or a migration trigger
- you can complete all ten exercises and defend each decision with observed evidence

When those feel ordinary, Module 05 has done its job.
