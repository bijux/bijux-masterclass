# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Build Graph Foundations Truth"]
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

Use these after reading the five core lessons and the worked example. The goal is not to
produce clever Make syntax. The goal is to make your reasoning visible.

## Exercise 1: Draw the graph

Take the tiny C project and draw the dependency graph for `app`, `build/main.o`, and
`build/util.o`. Mark which nodes are real files and which ones are convenience targets.

Focus question: where would a missing edge create a lie?

What to hand in:

- a graph sketch
- one sentence per edge explaining why it matters
- one sentence naming the most dangerous missing edge

## Exercise 2: Find a hidden input

Modify the build so that changing `CFLAGS` should matter. Then explain why a plain object
rule does not automatically capture that fact.

Focus question: what evidence would you add so the graph stays truthful?

What to hand in:

- the changed Makefile fragment
- a plain-language explanation of why the input is hidden
- a proposed stamp, manifest, or other evidence artifact

## Exercise 3: Review rule ownership

Write one explicit rule and one pattern rule for the same build. Compare them and explain
which output path each recipe owns.

Focus question: where would multi-writer confusion start?

What to hand in:

- one explicit rule example
- one pattern or static pattern rule example
- a short comparison of readability and ownership

## Exercise 4: Explain evaluation timing

Write one example that uses `:=` and one that uses `=`. Predict when each value is
computed and how that changes the graph or recipe behavior.

Focus question: which version is safer for a source-file list?

What to hand in:

- one `:=` example
- one `=` example
- one paragraph describing when each value is fixed

## Exercise 5: Prove safe publication

Take a compile or link rule and redesign it to publish through a temporary file. Then
state exactly what failure should leave behind.

Focus question: how do you prove the final target path never points at a partial artifact?

What to hand in:

- the revised rule
- the failure drill you ran
- the observable result after failure and rerun

## Exercise 6: Write the smallest useful Makefile

Create `message.txt` containing one line of text. Write a Makefile that produces
`message.upper.txt` with `tr`, then add a phony `all` target that requests it.

Run the build twice. Change `message.txt` and run it again.

What to hand in:

- the complete Makefile
- the output from all three runs
- one sentence explaining why the second run does no work

## Exercise 7: Predict automatic variables

Without running Make, fill in the values of `$@`, `$<`, and `$^` for this rule:

```make
report.txt: title.txt results.txt
	cat $^ > $@
```

Then create the files, run `make --trace report.txt`, and compare the trace with your
prediction.

What to hand in:

- your prediction written before the run
- the observed command
- a corrected explanation if any value surprised you

## Exercise 8: Remove duplicated compile recipes

Start with two explicit rules that compile `src/alpha.c` and `src/beta.c`. Replace them
with one pattern rule while keeping the object paths under `build/`.

Add a third source file. The new file should require no new compile recipe.

What to hand in:

- the explicit version
- the pattern-rule version
- a trace showing the third object built from the reusable rule

## Exercise 9: Diagnose a stale header build

Create a two-source C project where both source files include `config.h`, but omit the
header from one object rule. Build, change a macro in `config.h`, and observe the stale
object.

Repair the graph and repeat the experiment.

What to hand in:

- the broken rule and the repaired rule
- the trace before and after repair
- an explanation of why `make clean` would hide rather than solve the problem

## Exercise 10: Design and defend a small graph

Design a build for this pipeline:

```text
raw.csv -> cleaned.csv -> summary.txt
                    \-> chart.svg
```

Write rules for all three outputs and a phony `all` target. You may use `cp` and
`printf` instead of real data-analysis tools.

Test these changes separately:

1. change `raw.csv`
2. delete `summary.txt`
3. delete `chart.svg`
4. run the successful build twice

What to hand in:

- the Makefile and a graph diagram
- your predicted rebuild set for each change
- traces confirming or correcting each prediction
- one paragraph defending the ownership of every output path

## Mastery standard for this exercise set

You are aiming for four things across all ten answers:

- you name the evidence Make is using
- you explain why that evidence is sufficient or insufficient
- you prove the claim with a command, a graph sketch, or a failure drill
- you distinguish a file target from a phony action target

If your answer only says "this is best practice" without evidence, keep going.
