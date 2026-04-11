# Macros, call, and Reuse Without Opaqueness


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Build Architecture Layered Includes Apis"]
  page["Macros, call, and Reuse Without Opaqueness"]
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

Once a Make build has a few repeated rule shapes, the pressure to introduce macros becomes
strong:

- several compile rules look almost the same
- several packaging rules differ only by a name
- several publication steps use the same safety pattern

That pressure is legitimate. Duplication can hide invariants too.

The problem is that macro reuse can go bad in two opposite ways:

- the build stays copy-pasted and drifts inconsistently
- or the build compresses so aggressively that nobody can read the graph anymore

This page is about the middle path: reuse that keeps the graph inspectable.

## The sentence to keep

Before adding a macro, ask:

> is this abstraction making one invariant easier to enforce, or is it mainly hiding the
> graph behind another layer of indirection?

That one question catches a lot of bad macro design.

## Reuse is justified when it protects truth

The strongest reason to use a macro is not "these lines look similar."

The strongest reason is:

> the same correctness rule should be applied the same way every time.

Examples:

- every generated file should publish through a temporary path and final move
- every compile rule should use the same warning flags and include roots
- every bundle rule should produce a manifest alongside the artifact

In those cases, the macro is helping preserve an invariant, not merely reducing typing.

## Reuse is dangerous when it hides the graph

Macros become unhealthy when a reader can no longer answer:

- what target is being defined
- what prerequisites it has
- what recipe it runs

For example:

```make
$(eval $(call define-everything,$(COMPONENTS),$(FLAGS),$(EXTRA)))
```

That may be technically correct, but if the build can only be understood by mentally
executing a meta-language, the architecture is already drifting away from clarity.

This does not mean `call` or `eval` are forbidden. It means the burden of explanation is
higher once you use them.

## A small, healthy macro example

Suppose several generated files should publish atomically.

```make
define publish_file
$1: $2 | $$(@D)/
	@$3 > $$@.tmp
	@mv $$@.tmp $$@
endef
```

Used like:

```make
$(eval $(call publish_file,build/version.txt,data/version.txt,cat data/version.txt))
```

This can be healthy because the macro enforces one repeated safety rule:

- write temporary content first
- then publish the final file

The macro is short, the arguments are explicit, and the resulting target is still easy to
find in `make -p`.

## A copy-paste example where a macro helps

Without reuse:

```make
build/main.o: src/main.c include/app.h
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

build/util.o: src/util.c include/app.h
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@
```

With a bounded macro:

```make
define compile_object
$1: $2 include/app.h | $$(@D)/
	$$(CC) $$(CPPFLAGS) $$(CFLAGS) -c $$< -o $$@
endef

$(eval $(call compile_object,build/main.o,src/main.c))
$(eval $(call compile_object,build/util.o,src/util.c))
```

This may be acceptable because:

- the rule shape is simple
- the expansion is obvious
- the macro reinforces a compile invariant

The important question is not whether the macro is shorter. The important question is
whether the resulting graph is still legible.

## `call` is easier to defend than sprawling ad hoc indirection

If you need reuse in Make, `call` with explicit arguments is often a reasonable tool
because it keeps the interface visible:

- what the macro takes
- what each call site provides
- where the generated rules come from

That is still not automatically good. It is simply easier to review than reuse that hides
its parameters in global mutable variables.

Explicit arguments are one of the strongest habits for keeping Make reuse sane.

## `eval` needs an extra explanation burden

`eval` is powerful because it generates Make syntax during evaluation. That also makes it
easy to overuse.

`eval` is most defensible when:

- the repeated structure is real
- the expanded rules remain inspectable with `make -p`
- the number of generated rule shapes is bounded
- the call sites are easy to locate

`eval` is much less defensible when it becomes the build's real programming language and
the normal files only host a macro engine.

That is when the build starts turning into a framework instead of a system another engineer
can review.

## Macros should not invent a second naming system

One architecture smell is a macro layer that introduces names and conventions unrelated to
the target graph the rest of the repository uses.

For example:

- internal macro names do not resemble published targets
- generated variable names become the only way to trace ownership
- newcomers need to learn the macro dialect before they can understand one target

That is a warning sign. The abstraction is becoming a private language.

## A useful macro review checklist

When you see a macro, ask:

1. what invariant is it enforcing
2. what targets or rules does it generate
3. where are the call sites
4. can the final rules be inspected clearly with `make -p`
5. would two straightforward explicit rules be easier to maintain

If the fifth answer is yes, the macro may not be worth it.

## A healthy boundary for reuse

Macros are most helpful when they stay at one of these levels:

- one repeated rule body
- one repeated publication pattern
- one repeated object or bundle mapping pattern

Macros become much riskier when they try to own:

- whole subsystems
- policy selection
- include layering
- top-level API decisions

Those are usually architecture concerns that deserve clearer, more explicit structure.

## Why `make -p` remains the audit escape hatch

The course does not require every reader to mentally expand macros by hand. It does require
the build to remain inspectable.

That is why `make -p` matters here:

- it shows the final rules after expansion
- it reveals whether the macro generated what the author claims
- it helps verify that reuse did not smuggle in hidden mutation

If the build only makes sense before expansion or only in the macro author's head, the
architecture is already too opaque.

## Failure signatures worth recognizing

### "The Makefile is shorter, but nobody can explain one target"

That often means reuse crossed into opacity.

### "Every bug fix requires editing a macro no one wants to touch"

That usually means too much behavior was centralized in one abstraction.

### "The macro arguments are less clear than the duplicated rules"

That is a strong sign the abstraction is not paying for itself.

### "We need `make -p` just to understand ordinary intent"

It is fine to confirm with `make -p`. It is not fine if it is the only path to basic
understanding.

## A review question that improves reuse decisions

Take one candidate macro and ask:

1. what invariant it is protecting
2. what explicit rules it would replace
3. whether the resulting call sites are easier to read than the original rules
4. whether the expanded graph remains obvious
5. whether the abstraction could be smaller and still useful

If those answers are weak, the macro should probably stay explicit or be redesigned.

## What to practice from this page

Choose one repeated rule family in a Make repository and write two versions:

1. the explicit repeated rules
2. a bounded macro version

Then explain:

- what invariant the macro protects
- what readability cost it introduces
- whether the final design should stay explicit or use the macro

If you can defend that choice in plain language, you understand reuse much better than a
team that automatically abstracts or automatically copy-pastes.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- when a macro improves correctness rather than merely reducing typing
- why explicit arguments matter
- when `eval` is defensible and when it becomes too opaque
- how to tell whether reuse has created a private language
- why `make -p` is the audit backstop for macro-heavy designs
