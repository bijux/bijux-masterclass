# Install Flows and Destination Safety

Many repositories treat `install` as a small appendix to the build:

- copy a binary somewhere
- maybe create a directory
- maybe overwrite files
- hope it is fine if run twice

That is a risky habit.

`install` is not a casual copy step. It is a publication act with side effects on a real
destination tree. That means it deserves the same design discipline as `dist`.

This page is about making installation behavior safe enough to trust.

## The sentence to keep

When you define `install`, ask:

> what exact destination tree am I promising to create or update, and what should happen if
> the target is run again?

That question turns installation from shell ritual into contract design.

## Installation has a destination contract

An install step should answer at least four things:

- where files go
- which directories are created
- what overwrite behavior is expected
- whether rerunning the install leaves the same intended result

If those facts are not clear, the install surface is not really designed yet.

This is why `DESTDIR` or other destination-root variables matter. They make the publication
boundary explicit.

## Idempotence matters

One of the healthiest expectations for `install` is idempotence:

> running `make install` twice should not produce a meaningfully different system than
> running it once.

That does not mean timestamps or file metadata can never change. It means the intended
installed tree should settle on the same content and structure.

If the second run:

- duplicates files
- appends to config
- leaves broken intermediate state
- depends on left-over partial results from the first run

then the install contract is lying.

## `DESTDIR` makes install review safer

A classic safe-review pattern is:

```sh
make install DESTDIR=/tmp/release-check
```

This matters because it lets you inspect the resulting layout without mutating a real
system location.

Even if the repository later supports a more privileged install route, `DESTDIR` or a
similar staging root is a very useful discipline:

- it makes the destination explicit
- it helps test idempotence
- it keeps the installation tree inspectable

That is a much safer default than recipes that write straight into `/usr/local` or another
system path during everyday testing.

## A small install contract

Suppose the install policy is:

- binary goes to `$(DESTDIR)/usr/local/bin/app`
- license goes to `$(DESTDIR)/usr/local/share/licenses/app/LICENSE`

Then the build should model that clearly:

```make
PREFIX ?= /usr/local
INSTALL_ROOT := $(DESTDIR)$(PREFIX)

.PHONY: install

install: app LICENSE
	@mkdir -p $(INSTALL_ROOT)/bin
	@mkdir -p $(INSTALL_ROOT)/share/licenses/app
	@cp app $(INSTALL_ROOT)/bin/app
	@cp LICENSE $(INSTALL_ROOT)/share/licenses/app/LICENSE
```

This is not exotic. It is simply explicit enough that another engineer can inspect the
result.

## Stage first when the install flow is more complex

For richer installs, a staging tree is often healthier than copying directly into the final
destination layout piece by piece.

That may look like:

1. assemble install tree in a temporary directory
2. validate it
3. copy or sync it into the destination root in one controlled step

This is the same publication lesson from earlier modules:

- prepare in temporary space
- trust only after the layout is complete

That reduces the chance that a failed install leaves a half-updated destination that looks
finished enough to confuse the next run.

## Overwrite behavior should be deliberate

Install commands often blur three different policies:

- always overwrite
- overwrite only if content changed
- fail if a conflicting file already exists

Any of those can be legitimate depending on the contract.

The mistake is to leave the behavior accidental.

For example, a system-level install might reasonably want stricter conflict handling than a
`DESTDIR` staging install. The important thing is that the build and its docs make that
choice visible.

## A weak install target smells like this

Be suspicious when `install`:

- writes directly into a real system path during everyday testing
- depends on the current working directory or shell state
- mixes package creation and final installation in one recipe without a clear boundary
- cannot be rerun safely

These are not only operational inconveniences. They are contract defects.

## Dry-run and preview help here too

Not every repository can make `install` fully dry-run capable, but preview habits still
matter.

Useful review questions include:

- what files will be copied
- where will they go
- which directories will be created
- what existing paths may be overwritten

Even when the exact preview mechanism differs, the goal is the same: make install side
effects inspectable before they happen.

## A small staged install example

```make
INSTALL_STAGE := build/install-stage
PREFIX ?= /usr/local
INSTALL_ROOT := $(DESTDIR)$(PREFIX)

.PHONY: install

install: app LICENSE
	@rm -rf $(INSTALL_STAGE)
	@mkdir -p $(INSTALL_STAGE)/bin
	@mkdir -p $(INSTALL_STAGE)/share/licenses/app
	@cp app $(INSTALL_STAGE)/bin/app
	@cp LICENSE $(INSTALL_STAGE)/share/licenses/app/LICENSE
	@mkdir -p $(INSTALL_ROOT)
	@cp -R $(INSTALL_STAGE)/* $(INSTALL_ROOT)/
```

This is often easier to review than a longer recipe that mutates the destination tree in
many small steps.

## Install and dist are related but not identical

Teams sometimes blur `dist` and `install`. The healthier distinction is:

- `dist` publishes a portable artifact boundary
- `install` publishes a destination tree side effect

The two may share inputs, but they do not necessarily promise the same result.

That is why each deserves its own contract meaning.

## Failure signatures worth recognizing

### "Running install twice changes the destination unexpectedly"

That means the install route is not idempotent enough for its intended contract.

### "We can only test install by writing into a real machine path"

That usually means the destination boundary is not explicit enough.

### "A failed install leaves half the tree updated"

That means publication into the destination is happening too incrementally or too early.

### "No one can tell whether install overwrites or preserves existing files"

That means overwrite policy is accidental rather than declared.

## A review question that improves install design

Take one install route and ask:

1. what destination tree it promises
2. how that destination is parameterized
3. whether it can be tested under `DESTDIR` or an equivalent staging root
4. what rerunning it should do
5. how it behaves if a partial failure occurs halfway through

If those answers are weak, the install contract is weak too.

## What to practice from this page

Choose one repository install route and write down:

1. the destination root
2. the installed file tree
3. one idempotence expectation
4. one staging or preview improvement
5. one reason the improved design would make release debugging safer

If you can do that cleanly, you are treating installation as contract engineering rather
than as a copy command.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why `install` is a publication act with side effects
- why idempotence matters for installation routes
- why `DESTDIR` or another explicit destination root improves reviewability
- how staged installation can reduce half-updated trees
- why overwrite behavior should be a visible policy decision
