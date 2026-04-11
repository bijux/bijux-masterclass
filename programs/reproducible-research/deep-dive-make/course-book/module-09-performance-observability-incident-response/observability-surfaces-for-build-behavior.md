# Observability Surfaces for Build Behavior

Teams often discover they have a build observability problem only during an incident.

They already know the build is:

- correct enough most days
- fast enough some of the time
- difficult to explain when something surprising happens

Then the team starts improvising:

- add `echo` lines to recipes
- print variables in random places
- dump timestamps into files
- leave debug scaffolding inside the real build

That is understandable under pressure. It is usually not a good long-term observability
strategy.

This page is about building evidence surfaces that help without mutating the truth you are
trying to observe.

## The sentence to keep

When you add build observability, ask:

> what question does this surface answer, and does it answer it without changing the build's
> semantic outputs?

That question separates observability from accidental instrumentation.

## Observability should answer concrete questions

Good build observability tells you things like:

- what ran
- why it ran
- what Make believed about variables and rules
- which discovery or manifest state was in effect
- how much evidence was emitted

That is why the module treats observability as a set of specific surfaces instead of one
general desire for "more logs."

## `--trace` answers causality questions

If you want to know:

- why a target ran
- which prerequisite edge triggered the rebuild
- where the relevant rule lives

then `--trace` is one of the best built-in tools:

```sh
make --trace all
```

This is valuable because it grounds the incident in graph behavior rather than in stories.

The lesson is not "always dump trace output." The lesson is "use trace when the question is
about causality."

## `-p` answers evaluated-world questions

If the question is:

- what value did a variable really have
- which rule is actually present after includes and expansion
- what does the final Make database look like

then `-p` is more appropriate:

```sh
make -p > build/make.dump
```

This is a different kind of evidence from `--trace`.

That distinction matters because one of the most common observability mistakes is using the
right tool for the wrong question.

## Bounded diagnostic targets are healthier than scattered debug prints

A good repository often grows one or two focused diagnostic targets such as:

- `trace-count`
- `discovery-audit`
- `contract-audit`
- `profile-audit`

These are healthier than ad hoc `echo` statements scattered through normal recipes because
they:

- answer a specific question
- keep the evidence surface discoverable
- avoid changing normal semantic outputs

For example:

```make
.PHONY: trace-count

trace-count:
	@make --trace -n all 2>&1 | wc -l
```

This is much easier to explain and remove than a hundred one-off debug prints.

## Debug prints become dangerous when they leak into artifacts

One easy way to make observability harmful is to let diagnostics become part of semantic
outputs.

Examples:

- writing timestamps into generated files just to see when something ran
- printing local host info into a packaged artifact
- mixing debug status text into manifests that are supposed to be stable

That is not observability anymore. That is output mutation disguised as debugging.

This is why the module keeps insisting that observability should stay beside the artifact or
inside dedicated evidence routes, not inside the meaning of the build itself.

## A small observability toolkit

Here is a practical split:

| Question | Better tool |
| --- | --- |
| why did this rebuild | `make --trace <target>` |
| what is the final variable/rule world | `make -p` |
| how much trace output does a normal route emit | a `trace-count` target or `wc -l` on trace output |
| what did discovery resolve to | a discovery audit target or stable manifest |
| what changed between serial and parallel behavior | a selftest or explicit artifact comparison route |

This table is useful because it prevents the common habit of treating all evidence as one
generic "debug output" category.

## Discovery and manifest audits can be real observability surfaces

Some of the most useful build evidence is not about timing or trace. It is about resolved
state:

- which files discovery found
- what a manifest currently declares
- what a contract file contains

That evidence becomes more valuable when it is exposed through stable, named routes rather
than by asking every maintainer to remember one-off shell commands.

For example, a discovery audit target might produce a stable file list that can be compared
or reviewed.

The architectural point is:

- observable state should have a home
- not merely a memory

## Observability should be bounded

More output is not automatically better observability.

If the build emits:

- too much trace
- too many redundant debug lines
- too many unstable dumps

then the evidence surface becomes expensive to use.

This is why the course prefers bounded diagnostic targets:

- they answer one question
- they keep output size proportional to value
- they make normal build routes easier to live with

That is a much better pattern than sprinkling temporary prints everywhere and never cleaning
them up.

## A useful anti-pattern: "debug by mutation"

One of the clearest observability anti-patterns is debugging by mutation:

- change outputs to prove a step ran
- bake local state into artifacts
- add hidden files inside normal routes just to inspect them later

This is tempting because it produces visible evidence quickly. It is still a bad habit
because it changes the system you are trying to observe.

The healthier move is:

- add a sidecar evidence surface
- add a bounded diagnostic target
- use `--trace` or `-p`

Those choices preserve trust.

## Failure signatures worth recognizing

### "We added more logging, but incidents are still hard to explain"

That often means the output answers no specific question or is too noisy to use.

### "The only way to debug this build is to edit the Makefiles"

That means the repository is missing named observability surfaces.

### "Our manifests or bundles keep changing because of debug info"

That means observability has leaked into semantic outputs.

### "No one knows whether to use `--trace` or `-p`"

That means the team lacks a shared map from questions to tools.

## A review question that improves observability design

Take one evidence surface and ask:

1. what question it answers
2. how a newcomer discovers it
3. whether it mutates normal outputs
4. whether it is bounded enough to use under pressure
5. whether a built-in Make surface would already answer the same question better

If those answers are weak, the observability design is weak too.

## What to practice from this page

Choose one Make-based build and write down:

1. the question `--trace` helps answer
2. the question `-p` helps answer
3. one diagnostic target that would be worth adding
4. one current debug habit that should be removed
5. one reason the improved observability surface would make incidents calmer

If you can do that cleanly, you are treating observability as design instead of as a pile
of prints.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why observability should answer explicit questions
- when `--trace` is the right tool
- when `-p` is the right tool
- why bounded diagnostic targets are healthier than scattered debug prints
- why debug-by-mutation is dangerous in a build system
