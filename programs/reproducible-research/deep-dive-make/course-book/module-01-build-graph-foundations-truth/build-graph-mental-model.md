# Build Graph Mental Model


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Build Graph Foundations Truth"]
  page["Build Graph Mental Model"]
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

The first habit to build is this one:

> Every time you read a Makefile, ask which files exist, which files depend on which
> other files, and which recipe is trusted to publish each output.

That is the mental model. Everything else in Module 01 hangs off it.

## A small graph

```mermaid
flowchart LR
  all["all"] --> app["app"]
  app --> main["build/main.o"]
  app --> util["build/util.o"]
  main --> mainc["src/main.c"]
  main --> utilh["include/util.h"]
  util --> utilc["src/util.c"]
  util --> utilh
```

This graph is ordinary on purpose. It already gives you the important questions:

- which files are real artifacts
- which files are source inputs
- which targets are conveniences such as `all`
- which edges tell Make that a change matters

## Three parts of a rule

A rule has three jobs:

1. name the target being promised
2. declare the inputs that can change its meaning
3. publish the target through a recipe

For example:

```make
build/main.o: src/main.c include/util.h
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@
```

Read that line in English:

"`build/main.o` is trusted output. Its meaning depends on `src/main.c` and
`include/util.h`. If it is missing or older than one of those prerequisites, run this
compile recipe."

Once you can read rules this way, Make gets calmer.

## A target is a promise, not just a filename

The most useful beginner correction is this one:

- a source leaf normally exists without a producing rule
- a file target may already satisfy its promise when Make starts
- Make checks the declared evidence before deciding whether the promise needs renewal
- the owning recipe is the act that publishes a missing or stale target

That framing helps with review. If a rule claims it owns `build/main.o`, then the recipe
must be the only place that turns that path from "missing" into "published artifact."
The target is not just a string on the left side of a colon. It is a promise about what a
future file means.

## Distinguish node roles

| Role | Example | What Make does |
| --- | --- | --- |
| requested goal | command-line `app` | walks its prerequisite closure |
| aggregate/action target | phony `all` or `clean` | represents a request rather than file freshness |
| file target | `build/main.o` | checks existence and prerequisite freshness |
| generated prerequisite | `build/config.h` | updates it before consumers |
| source leaf | `src/main.c` | requires it to exist; no producer is needed |
| missing unexplained leaf | misspelled `src/mian.c` | fails because no rule can make it |

One path can be a target in one rule and a prerequisite in another. “Target” describes
its position in a rule, not a permanent species of file.

## What Make is actually deciding

Make is not asking, "Did the programmer mean to rebuild?" It is asking, "Given the graph
I was shown, is this target up to date?"

That is a smaller question, and it is why bad builds often feel surprising:

- if an input is missing from the graph, Make cannot consider it
- if a target is written by more than one recipe, ownership becomes ambiguous
- if the published file is broken, later decisions can still treat it as truth

The bug is often not in the command. The bug is in the story the graph tells.

## Walk the update decision

For one file target, Make conceptually asks:

```mermaid
flowchart TD
  needed["target lies in requested closure"] --> prereqs["update prerequisites"]
  prereqs --> exists{"target exists?"}
  exists -->|no| run["run owning recipe"]
  exists -->|yes| newer{"normal prerequisite newer?"}
  newer -->|yes| run
  newer -->|no| skip["target is up to date"]
  run --> result{"recipe and publication succeed?"}
  result -->|yes| promise["target promise renewed"]
  result -->|no| failure["request fails; rejected output must not look valid"]
```

Phony targets follow action semantics and are considered for execution whenever they are
requested in the graph. Order-only prerequisites affect update order but not the
newer-than test; Module 02 develops that distinction.

## Predict from a state table

Before running Make, write:

| Target exists | Prerequisite state | Prediction |
| --- | --- | --- |
| no | prerequisites available | recipe runs |
| yes | all normal prerequisites older | recipe skips |
| yes | one normal prerequisite newer | recipe runs |
| yes | one prerequisite missing with no rule | request fails |
| yes | hidden recipe input changed | Make may skip dishonestly |

The final row is why reading recipes still matters after reading the graph: Make cannot
infer undeclared shell reads.

## A quick contrast: graph thinking vs script thinking

| Script-thinking question | Better graph-thinking question |
| --- | --- |
| "What commands run from top to bottom?" | "What targets become eligible to run when an input changes?" |
| "Where should I insert this shell line?" | "What file or stamp should represent this fact?" |
| "Why does clean fix it?" | "Which dependency was missing or which artifact was published badly?" |

This shift is the difference between a build that feels magical and a build you can
review.

## Read the graph before you read the shell

When a Makefile is unfamiliar, do not start with the longest recipe. Start here:

1. find the requested goal, such as `all` or `app`
2. list the prerequisites of that goal
3. keep walking downward until you reach source leaves
4. only then read the recipes

That reading order keeps you focused on causality. A shell command can be complicated and
still sit in a correct graph. A tiny shell command can sit in a lying graph.

Then compare declared prerequisites with actual recipe observations:

```text
target:
declared normal prerequisites:
declared setup prerequisites:
recipe file reads:
recipe environment/tool inputs:
recipe writes:
```

Every semantic read needs graph evidence or a deliberate documented external contract.
The shell remains opaque to Make.

## A tiny Makefile worth reading slowly

```make
.PHONY: all clean

all: app

app: build/main.o build/util.o
	$(CC) $^ -o $@

build/main.o: src/main.c include/util.h
	$(CC) -Iinclude -c $< -o $@

build/util.o: src/util.c include/util.h
	$(CC) -Iinclude -c $< -o $@

clean:
	rm -rf build app
```

This is not a production Makefile yet. It is just small enough to teach the shape:

- `all` is a convenience target
- `app` is a real artifact
- the object files are intermediate artifacts
- the source and header files are leaves in the graph

If `include/util.h` changes, both object files should rebuild because both depend on it.

## Common reading mistakes

### Mistake 1: treating `.PHONY` like a normal file target

`.PHONY` targets are commands you always want available. They are not evidence about file
state. Put operational actions there, not publish steps for real artifacts.

### Mistake 2: assuming Make watches command text automatically

It does not. If command flags or environment values change build meaning, you have to
model them. That is the next lesson.

### Mistake 3: assuming "it built once" means the graph is correct

A build can succeed while still lying. Hidden inputs, missing edges, and unsafe output
publication often show up only on the next incremental run.

### Mistake 4: assuming the top target is the whole story

Beginners often stare at `all:` and think they understand the build because they
understand the top line. The real understanding usually lives one or two steps lower:

- which file edges feed the object files
- which rule owns the binary
- which prerequisites are shared across multiple outputs

That is where correctness lives.

## A worked reading pass

Take this rule set:

```make
all: app

app: build/main.o build/util.o
	$(CC) $^ -o $@

build/main.o: src/main.c include/util.h
	$(CC) -Iinclude -c $< -o $@
```

Now ask the questions in order:

1. What is the requested goal? `all`.
2. What real artifact does `all` point at? `app`.
3. What evidence does `app` rely on? `build/main.o` and `build/util.o`.
4. What evidence does `build/main.o` rely on? `src/main.c` and `include/util.h`.
5. Which change should rebuild `build/main.o`? either source or header change.

That is the real reading pass. If you start with `$(CC)`, you start too late.

Now challenge it:

1. remove `app` and predict the closure that rebuilds;
2. repeat unchanged and predict no work;
3. change only `src/main.c` and predict one object plus the link;
4. change `include/util.h` and predict both objects plus the link;
5. add an undeclared header read and predict the stale-output failure after changing it.

The fifth challenge tests completeness. A no-op build can be quiet because the graph is
correct or because an edge is missing.

## Commands that make the graph visible

Use these when your picture of the graph is fuzzy:

```sh
make -n all
make --trace all
make -pRrq all > artifacts/learning/deep-dive-make/module-01-graph-truth/database.txt
```

Create the artifact directory before redirecting. Query mode may return `1` when work is
needed, so capture its exit separately rather than assuming the database is absent.

Dry run predicts ordinary recipes; trace explains selected updates; the bounded database
shows evaluated rules and variables. None proves that a recipe produced correct content.

## Default goals and multiple requests

Without `.DEFAULT_GOAL`, GNU Make normally chooses the first ordinary target it reads as
the default. Include reordering can therefore change an accidental default.

Declare intent:

```make
.DEFAULT_GOAL := all
```

A user can also request several goals:

```sh
make app report
```

Make takes the union of their needed graph. Do not design correctness around an assumed
left-to-right shell-script sequence between independent goals.

## End-of-page checkpoint

Before leaving this page, make sure you can do all four:

- point at one rule and name its target, prerequisites, and recipe in plain language
- explain why `.PHONY` does not belong on real artifacts
- describe the object-file graph for the tiny C build without looking at the diagram
- say which command you would run first if you wanted Make to explain a rebuild decision
- distinguish a missing file target, an up-to-date file target, a source leaf, and a
  phony action
- challenge graph completeness with a relevant input mutation

## What to practice on this page

Take any small target in your build and answer these five questions:

1. What file path is the target promising to publish?
2. What files are declared as prerequisites?
3. Which missing prerequisite would cause a silent lie?
4. Is the target real or phony?
5. Which recipe owns that output path?

If you can answer those without hand-waving, you are ready for the next page.
