# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your graph reasoning visible through artifacts, traces, and repair notes, not through
confident-sounding Make syntax.

## How to work through this set

Treat the ten exercises as one full lab day on graph truth.

Before each answer:

1. name the target or input relationship you are testing
2. predict what Make will do before you run the command
3. keep the smallest artifact that proves whether your prediction was honest

If you skip the prediction, it becomes too easy to write a polished story after the fact.
The whole point of Module 01 is to catch where your mental graph is still weak.

Do the exercises in order. The day is designed as one progression:

- Exercises 1-3 teach you to draw and defend the graph honestly
- Exercises 4-6 move from graph language into concrete build behavior
- Exercises 7-8 teach you to generalize a design without losing ownership
- Exercises 9-10 test whether you can diagnose and defend a small build yourself

Keep one build-truth packet as you go. By the end of the day it should contain:

- one graph sketch that you corrected after running Make
- one hidden-input example and its repair
- one safe-publication rule with a failure drill
- one small Makefile that you can explain target by target
- one stale-output diagnosis where `make clean` would hide the defect
- one final graph you would be willing to defend to another learner

If those six artifacts are missing, you are probably collecting snippets instead of
learning how Make decides what is true.

## Recommended working layout

If you want one lab tree that can support the whole day, use something like:

```text
module01-lab/
├── Makefile
├── src/
├── include/
├── build/
├── data/
├── notes/
└── artifacts/
```

That is intentionally small. Module 01 should feel inspectable. If your lab gets large
enough that you stop seeing the graph directly, shrink it again.

Keep one evidence sheet while you work:

| Before the run | Command | What happened | What the graph means now |
| --- | --- | --- | --- |
| prediction written first | exact `make` command | target-level observation | corrected explanation |

Also keep one ownership list for every multi-target example:

| Target path | Who writes it | Which inputs decide it | What would make it stale |
| --- | --- | --- | --- |

That second table is the fastest way to notice where you are relying on hidden inputs or
implicit assumptions.

```mermaid
flowchart LR
  predict["predict the graph claim"]
  draw["draw targets and prerequisites"]
  run["run the smallest useful command"]
  inspect["inspect the trace or artifact"]
  repair["repair the edge, rule, or ownership"]
  defend["explain why the graph is truthful now"]

  predict --> draw --> run --> inspect --> repair --> defend
```

Use that route on purpose. It keeps the day centered on evidence instead of on folklore
about "how Make usually works."

## Exercise 1: Draw the graph

Take the tiny C project and draw the dependency graph for `app`, `build/main.o`, and
`build/util.o`. Mark which nodes are real files and which ones are convenience targets.

What to hand in:

- a graph sketch
- one sentence per edge explaining why it matters
- one sentence naming the most dangerous missing edge
- one sentence distinguishing a real file target from a phony convenience target

Study note:
If your graph does not name headers, directories, or convenience targets explicitly, it
is probably too vague to teach you anything.

## Exercise 2: Find a hidden input

Modify the build so that changing `CFLAGS` should matter. Then explain why a plain object
rule does not automatically capture that fact.

What to hand in:

- the changed Makefile fragment
- a plain-language explanation of why the input is hidden
- a proposed stamp, manifest, or other evidence artifact
- one sentence explaining how another person would verify the repair

Study note:
Do not answer this as "Make cannot track variables." The better question is: what
artifact could carry the semantic value so the graph has something truthful to depend on?

## Exercise 3: Review rule ownership

Write one explicit rule and one pattern rule for the same build. Compare them and explain
which output path each recipe owns.

What to hand in:

- one explicit rule example
- one pattern or static pattern rule example
- a short comparison of readability and ownership
- one sentence naming where multi-writer confusion would start

Study note:
Ownership is not the same as convenience. A shorter Makefile is not better if another
reader can no longer tell who publishes a path.

## Exercise 4: Explain evaluation timing

Write one example that uses `:=` and one that uses `=`. Predict when each value is
computed and how that changes the graph or recipe behavior.

What to hand in:

- one `:=` example
- one `=` example
- one paragraph describing when each value is fixed
- one sentence explaining which version is safer for a source-file list and why

Study note:
The important distinction is not "simple variables versus recursive variables." The
important distinction is whether the graph-shaping value is stable for the whole run.

## Exercise 5: Prove safe publication

Take a compile or link rule and redesign it to publish through a temporary file. Then
state exactly what failure should leave behind.

What to hand in:

- the revised rule
- the failure drill you ran
- the observable result after failure and rerun
- one sentence explaining why the final target path never points at a partial artifact

Study note:
If your proof is only theoretical, the lesson is incomplete. Force a failure and inspect
what actually remains on disk.

## Midday self-check

Before you move into the smaller design and refactor exercises, make sure your packet can
already answer these questions cleanly:

- which graph edge in your lab is easiest to forget and most dangerous to omit
- which input in your build is still hidden unless you add evidence
- which target path is published atomically and how you proved it
- which value in your Makefile must be fixed at parse time for the graph to stay stable

If you cannot answer those four questions in plain language, return to Exercises 1-5 and
make the packet more explicit before you continue.

## Exercise 6: Write the smallest useful Makefile

Create `message.txt` containing one line of text. Write a Makefile that produces
`message.upper.txt` with `tr`, then add a phony `all` target that requests it.

Run the build twice. Change `message.txt` and run it again.

What to hand in:

- the complete Makefile
- the output from all three runs
- one sentence explaining why the second run does no work
- one sentence naming the exact edge that makes the third run legitimate

Study note:
The point is not to impress anyone with terseness. The point is to feel the smallest
possible truthful graph in your hands.

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
- one sentence explaining why `$<` would be wrong for this recipe

Study note:
Automatic variables become much easier once you tie each one to a graph question instead
of memorizing a table.

## Exercise 8: Remove duplicated compile recipes

Start with two explicit rules that compile `src/alpha.c` and `src/beta.c`. Replace them
with one pattern rule while keeping the object paths under `build/`.

Add a third source file. The new file should require no new compile recipe.

What to hand in:

- the explicit version
- the pattern-rule version
- a trace showing the third object built from the reusable rule
- one sentence explaining what information the final target still needs even after the
  compile recipe is generalized

Study note:
Pattern rules remove duplicated policy. They do not remove the need to declare which
outputs belong in the build.

## Exercise 9: Diagnose a stale header build

Create a two-source C project where both source files include `config.h`, but omit the
header from one object rule. Build, change a macro in `config.h`, and observe the stale
object.

Repair the graph and repeat the experiment.

What to hand in:

- the broken rule and the repaired rule
- the trace before and after repair
- an explanation of why `make clean` would hide rather than solve the problem
- one sentence naming the stale artifact and the missing edge that allowed it

Study note:
This is the exercise where many learners realize they have been proving only that clean
builds work, not that incremental builds tell the truth.

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
- one sentence explaining why the fan-out from `cleaned.csv` is honest

Study note:
The best final answers sound calm and specific. They name the writer of every path and
the input that makes each rebuild legitimate.

## Before you read the answers

Before opening `exercise-answers.md`, make sure you have at least:

- one wrong prediction you can now explain
- one repaired hidden-input example
- one graph diagram you would be willing to show a classmate
- one failure drill that proved atomic publication
- one reason a clean build is not an honest fix for stale outputs

If you do not yet have those five things, the answer page will feel useful but will not
do much teaching.

## Mastery standard for this exercise set

You are aiming for four things across all ten answers:

- you name the evidence Make is using
- you explain why that evidence is sufficient or insufficient
- you prove the claim with a command, a graph sketch, or a failure drill
- you distinguish file targets, convenience targets, and owned output paths clearly

If your answer only says "this is best practice" without evidence, keep going.
