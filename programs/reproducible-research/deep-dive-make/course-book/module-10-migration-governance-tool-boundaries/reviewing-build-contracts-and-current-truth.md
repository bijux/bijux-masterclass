# Reviewing Build Contracts and Current Truth

This page is about the first pass over an inherited build: not how to rewrite it, but how
to understand what it currently promises, what it currently breaks, and what evidence
separates those two things.

The rest of Module 10 depends on this discipline. A migration plan is only as good as the
review that shaped it.

## The first mistake to avoid

Most bad build reviews begin with sentences like these:

- "this Makefile is ugly"
- "we should modernize it"
- "there are too many variables"
- "I would never structure it this way"

Those may or may not be true. They are still weak starting points.

An inherited build is not a style puzzle. It is a contract surface. Before you talk about
beauty, you need to know:

- which targets people rely on
- which outputs the build claims to publish
- which inputs actually control those outputs
- which routes are safe only by accident
- which failures come from truth loss rather than mere inconvenience

That is the difference between criticism and review.

## The sentence to keep

When you open a legacy Make build, ask:

> what does this build currently promise, what evidence supports that promise, and where
> does the promise break under pressure?

That one sentence keeps the review honest.

## Start with public behavior, not file layout

A common beginner move is to start by mapping the file tree:

- top-level `Makefile`
- a few included `.mk` files
- perhaps a `scripts/` directory
- maybe some generated outputs and temp files

That map matters later. It is not the first thing that matters.

The first thing that matters is public behavior. Ask:

- what targets does a developer run on purpose
- what targets does CI call
- what targets are documented in README or helper scripts
- what files or directories are considered trusted outputs
- what commands are used to inspect, clean, publish, or verify the build

Those are the entrypoints into the system. If you do not know them, you do not yet know
what the build is for.

## A practical review order

For a first review, use this order:

1. list the public targets and what each one is supposed to mean
2. list the trusted outputs and who writes them
3. list the obvious sources of hidden state
4. compare serial and parallel behavior
5. classify the top risks before proposing repairs

That order works because it turns a vague build into a legible product surface.

## Step 1: name the public target contract

Take the top-level target surface and write it down in plain language.

Example:

| Target | Likely promise | Questions to ask |
| --- | --- | --- |
| `all` | Build the default artifact set | What artifacts count as complete? |
| `test` | Run ordinary validation | Does it depend on hidden setup or side effects? |
| `clean` | Remove generated outputs | Does it delete source-like or cached inputs too? |
| `release` | Produce publishable outputs | Does it also test, install, or mutate unrelated state? |

This is already more useful than saying "the Makefile is complicated."

Look for contract drift:

- targets with vague names such as `verify-stuff`
- CI depending on helper targets never meant to be public
- one target doing build, test, cleanup, and packaging in one shell ritual
- names that imply one promise but perform another

If the target contract is muddy, the review should say so explicitly.

## Step 2: trace who owns each output

The next review question is simple:

> for each trusted output, who writes it exactly once?

This is where many legacy systems begin to fail.

Suppose you find this:

```make
all: build/app build/version.txt

build/app:
	@./scripts/build-app.sh

package:
	@./scripts/build-app.sh
	@tar -czf dist/app.tar.gz build/app build/version.txt
```

The review issue is not "this uses a script." The issue is output ownership drift:

- `build/app` is written from more than one route
- packaging rebuilds product state as a side effect
- the graph no longer tells the truth about publication

That is a real finding. It predicts flaky releases, confusing reruns, and bad incident
triage later.

## Step 3: look for hidden state on purpose

Many build reviews stop at visible prerequisites. Strong reviews also ask what the build is
quietly depending on.

Common hidden-state sources include:

- environment variables that change recipe meaning
- undeclared tools or config files
- generated files that are read but never modeled
- shell commands that append to shared logs or status files
- directory scans whose result order is unstable

For example:

```make
report.txt:
	@./scripts/render-report.sh $(MODE) > $@
```

The review question is not "does `MODE` exist?" It is:

- where is `MODE` defined
- what happens when it changes
- is that change part of the declared build meaning
- does the current graph know that `report.txt` depends on it

If the answer is no, you have found a semantic input the graph does not model.

## Step 4: compare calm conditions to pressure conditions

A legacy build often looks fine when run one way:

```sh
make all
```

The review should always ask what happens under pressure:

```sh
make -n all
make --trace all
make -j1 all
make -j8 all
```

Those commands help answer different questions:

- `-n` shows intended actions without external mutation
- `--trace` shows why targets are considered
- `-j1` gives a serial baseline
- `-j8` exposes concurrency assumptions and shared-state damage

Many "legacy quirks" are really one of these:

- the build only works serially
- the build only works on a warm machine
- the build only works when outputs from a previous run remain
- the build only works because one accidental order hides the true graph problem

A review that never applies pressure is incomplete.

## Step 5: classify findings before suggesting fixes

Do not jump straight from evidence to edits. First classify the finding.

A simple review rubric is:

| Finding class | What it means |
| --- | --- |
| graph truth risk | the build graph hides a real dependency, writer, or publication event |
| contract drift | target names or output promises no longer match behavior |
| environment risk | the build depends on host state or undeclared tools |
| parallel-safety risk | correctness depends on serial execution or shared mutation |
| observability risk | the build is too opaque to diagnose safely |
| boundary risk | Make owns a concern it cannot model honestly |

That classification matters because each class suggests a different repair path.

For example:

- hidden input: probably a graph truth repair
- release target doing too much: contract repair
- one script maintaining long-lived deployment state: maybe a boundary repair

Without classification, reviews turn into giant wish lists.

## A small example review

Imagine you inherit this build:

```make
.PHONY: all release clean

all:
	@./scripts/build.sh

release:
	@./scripts/build.sh
	@./scripts/test.sh
	@./scripts/package.sh

clean:
	rm -rf build dist
```

A weak review says:

- too script-heavy
- not modular
- should use more make rules

A stronger review says:

1. `all` and `release` both rebuild product state through opaque scripts, so output
   ownership is unclear.
2. `release` mixes build, test, and packaging concerns behind one target, so its contract
   is too broad to audit cleanly.
3. There is no visible way to inspect which files count as trusted outputs before
   packaging.
4. The current structure makes serial/parallel equivalence hard to test because recipe
   meaning is hidden behind shell wrappers.

That second review is actionable because it describes broken promises rather than taste.

## The review artifact you should produce

A good first-pass review can be short. One page is enough if it is specific.

Use five sections:

1. public target contract
2. trusted outputs and writers
3. hidden inputs and stateful behavior
4. pressure findings from dry-run, trace, and serial/parallel comparison
5. top three to five risks, each with a class

If the review cannot fit on one page, the problem is often that the findings are still too
vague.

## What not to promise yet

At review time, avoid sentences like:

- "we should migrate to another tool"
- "we need to rewrite the whole build"
- "this should become a plugin system"

Those may eventually be true. The review has not earned those conclusions yet.

First earn these smaller claims:

- which current contracts are ambiguous
- where truth is already being lost
- which failure surfaces are the most expensive
- which concerns Make is currently modeling poorly

Only then does migration become a design decision instead of a mood.

## Failure signatures worth recognizing

### "The build works, but nobody can say why"

That is usually an observability and contract problem, not merely a documentation problem.

### "We cannot tell if `release` is broken without actually publishing"

That often means the publication boundary is too late or too opaque.

### "Parallel mode exposes random file corruption"

That is a parallel-safety review finding, not a strange CI anecdote.

### "Every engineer describes the build differently"

That usually means the public target contract was never written down.

## The habit this page wants

Strong maintainers do not begin with "how would I have built this?"

They begin with:

> what is the current product surface, what evidence makes it legible, and what exactly is
> broken about the promises it already makes?

That habit is what makes the rest of Module 10 possible.
