# Public Targets and Build API Design

As soon as a Make build becomes useful, people start calling it from more places:

- developers run it locally
- CI calls it in pipelines
- release scripts invoke it
- one-off maintenance commands get added by whoever needed them last

Without discipline, the top-level `Makefile` turns into an accidental API:

- internal helper targets become public by habit
- CI starts depending on private target names
- local convenience commands quietly become part of the release path
- nobody can say which targets may change safely and which ones are contractual

This page is about replacing that drift with a build API you can actually defend.

## The sentence to keep

When you look at a top-level `Makefile`, ask:

> which targets are promises to other humans or tools, and which targets are only internal
> implementation detail?

That is the core separation.

## A build API is still an API

The word "API" can sound too formal for a Makefile. It is still the right word.

If other humans, scripts, or CI systems depend on:

- `make all`
- `make test`
- `make selftest`
- `make clean`
- `make release`

then those names form a contract. Changing them casually is not just refactoring. It is a
breaking interface change.

This matters because many Make repositories behave as if every target is equally public.
That is usually false.

## Public targets should be few and stable

Healthy public target surfaces are small.

Typical public targets might include:

- `all`
- `test`
- `selftest`
- `clean`
- `help`
- one or two clearly named audit or release targets

That is enough for most users.

The build often contains many other targets, but they should remain implementation detail
unless there is a real reason to promote them.

The point is not minimalism for its own sake. The point is that a small target surface is
easier to document, easier to support, and safer to evolve.

## Internal helper targets are not shameful

Some teams act as if internal helper targets are a problem. They are not. They are useful.

The problem is when the build never says which targets are helpers and which ones are public
entrypoints.

For example:

```make
.PHONY: all test clean help package verify-contract build-objects
```

There may be nothing wrong with all of those existing. The architectural question is:

- which of them should another human rely on
- which of them may change name or shape freely as long as the public surface still works

That is why target lists need design, not just accumulation.

## Help output should reinforce the public surface

A good `help` target does more than print every name it can find. It teaches the user which
entrypoints are for them.

For example:

```make
.PHONY: help

help:
	@printf '%s\n' \
	  'all        Build the default artifact set' \
	  'test       Run project tests' \
	  'selftest   Verify build-system convergence and invariants' \
	  'clean      Remove generated build outputs'
```

This is stronger than dumping dozens of helper names. It makes the public surface visible.

That also means `help` should not pretend internal implementation targets are first-class
commands unless they truly are.

## CI should depend on public targets, not archaeology

One of the clearest signs of build architecture drift is this:

CI starts calling whatever target happened to exist when someone needed a shortcut.

Examples:

- `verify-contract`
- `build-objects`
- `dist-raw`
- `ci-step-3`

Those names may be useful internally, but CI should usually call a documented public target
such as `test`, `selftest`, or `release-check`.

Why? Because CI is a contract consumer. If it depends on internals, architectural cleanup
becomes much more dangerous.

## Public targets should say what they mean

Target naming matters. A good public target name says what a user is allowed to expect.

For example:

- `test` means tests the repository promises to run in normal validation
- `selftest` means build-system or repository invariants beyond ordinary product tests
- `release-check` means release-readiness checks, not "whatever this maintainer runs before tagging"

This is why vague names such as `run-all-things` or `final-check` age badly. They do not
communicate a stable promise.

## A small example of a healthy public surface

Top-level `Makefile`:

```make
.PHONY: all test selftest clean help

all: app

test:
	+$(MAKE) -C tests run

selftest:
	+$(MAKE) -C tests build-invariants

clean:
	rm -rf build dist app

help:
	@printf '%s\n' \
	  'all        Build the application' \
	  'test       Run product tests' \
	  'selftest   Run build-system invariants' \
	  'clean      Remove generated outputs'
```

This does not mean no internal targets exist. It means the public promises are clear.

## Internal targets can still be documented locally

Inside `mk/` files or a maintainer guide, you may still document helper targets such as:

- `build-objects`
- `render-assets`
- `refresh-manifest`

That is useful for maintainers. The important point is that the repository should not force
every user to treat those names as stable public contracts.

This is similar to public versus private functions in code. Private implementation details
can still be explained without becoming part of the external API.

## Public target drift is a real architectural smell

Watch for these symptoms:

- nobody can list the public targets from memory
- CI depends on target names that do not appear in user-facing docs or `help`
- targets exist only because some old script once depended on them
- new features always add top-level targets, even when they are not meant for general use

Those are not documentation issues only. They are interface-design issues.

## A practical promotion test

Before making a target public, ask:

1. will humans or automation rely on this regularly
2. can you explain its meaning in one sentence
3. is the name stable enough to keep
4. does it belong at the top level rather than inside a maintainer-only layer
5. are you willing to treat changes to it as interface changes

If the answer to the last question is no, the target probably should not be public.

## Why this page comes before include layering

Teams often start with include refactors first. That is usually backwards.

If you do not know which targets are public, you cannot make good layering decisions. The
top-level API is one of the main reasons layers exist in the first place.

That is why Module 07 begins here.

## Failure signatures worth recognizing

### "Our CI broke after a harmless refactor"

That often means CI was depending on a private target.

### "We have `help`, but it prints thirty targets and nobody knows which ones matter"

That means the public surface is not actually curated.

### "No one can tell whether `verify` and `selftest` are different"

That means target names or contracts are too vague.

### "Every new script gets its own top-level target"

That usually means the API is expanding by habit rather than design.

## A review question that improves build APIs

Take a top-level Makefile and ask:

1. which targets are public
2. how does a newcomer learn that
3. which of those targets are used by CI or scripts
4. which top-level targets should really be private helpers
5. which names are too vague to survive long-term

If those answers are weak, the build API is weak too.

## What to practice from this page

Choose one Make-based repository and write its public target list in plain language:

1. the public target names
2. one sentence of contract meaning for each
3. one target that should be demoted to internal
4. one improvement to `help`
5. one reason this smaller surface would make future refactors safer

If you can do that cleanly, you are treating the Makefile as an interface rather than a
bucket of commands.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why a Makefile can and should have a public API
- why public target sets should be small and stable
- why CI should call documented public targets rather than private helpers
- how `help` can reinforce the API instead of obscuring it
- how to decide whether a target deserves promotion to the public surface
