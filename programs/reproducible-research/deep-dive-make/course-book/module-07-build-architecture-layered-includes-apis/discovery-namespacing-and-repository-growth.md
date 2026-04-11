# Discovery, Namespacing, and Repository Growth

Small Make builds can survive with informal naming and casual discovery.

Larger builds usually cannot.

As a repository grows, the first architectural failures often look like this:

- source discovery order changes unexpectedly
- target names collide across subsystems
- output paths stop communicating ownership
- every component invents its own naming conventions
- the build slowly drifts toward disconnected local truths

This page is about the rules that keep a growing repository from becoming structurally
ambiguous.

## The sentence to keep

When a build starts growing, ask:

> if another component adds files tomorrow, will the current discovery and naming rules keep
> the graph stable and the ownership legible?

That question is what turns growth into architecture instead of improvisation.

## Discovery is an architectural choice

Discovery often begins innocently:

```make
SRCS := $(wildcard src/*.c)
```

That may be enough for a tiny project. As soon as the tree grows, discovery rules become a
policy decision:

- which directories count as source roots
- which file patterns are included
- whether the result order is stable
- how multiple components avoid stepping on each other

This is why Module 07 treats discovery as architecture rather than convenience.

## Rooted discovery beats wandering discovery

One of the healthiest habits for larger repositories is rooted discovery:

```make
APP_SRCS := $(sort $(wildcard src/app/*.c))
LIB_SRCS := $(sort $(wildcard src/lib/*.c))
```

This is better than broad, wandering discovery because it says:

- these directories are part of the build contract
- files outside them do not accidentally become build inputs
- order is stabilized intentionally

That makes the build easier to review and easier to extend.

## Sorting is part of graph stability

Discovery order matters more than many learners expect.

If source lists affect:

- object ordering
- link ordering
- generated manifests
- grouped publication sets

then unstable ordering can change the graph or the artifact shape even when the repository
meaning has not changed.

That is why this module keeps reinforcing the same habit:

```make
SRCS := $(sort $(wildcard src/**/*.c))
```

The sort is not cosmetic. It is a small determinism fence.

## Namespacing prevents target collisions

As repositories grow, collisions become a real risk:

- two components both want `build/main.o`
- two generated reports both want `summary.txt`
- two packages both want `dist.tar.gz`

This is a naming problem before it becomes a runtime problem.

Healthy namespacing often looks like:

```make
APP_OBJS := $(patsubst src/app/%.c,build/app/%.o,$(APP_SRCS))
LIB_OBJS := $(patsubst src/lib/%.c,build/lib/%.o,$(LIB_SRCS))
```

Now the path communicates ownership:

- `build/app/...` belongs to the app component
- `build/lib/...` belongs to the library component

That makes both debugging and code review easier.

## Output paths should tell a story

A good output path often answers one or more of these questions:

- which component owns it
- which stage produced it
- whether it is generated, packaged, or final

For example:

- `build/app/main.o`
- `build/generated/api.h`
- `dist/app-linux.tar.gz`

These names are useful because they communicate structure without extra commentary.

That is a big architectural advantage over flat output directories where every target must
be disambiguated mentally.

## One repository does not require many disconnected DAGs

When growth becomes painful, teams often reach for recursive separation too early:

- `make -C app`
- `make -C lib`
- `make -C tools`

Sometimes that boundary is real. Often it is a way of avoiding the harder work of naming
and discovery discipline inside one coherent DAG.

This page is not saying recursion is always wrong. It is saying:

if the repository still wants one coherent build truth, then namespacing and rooted
discovery are usually safer first moves than splitting reality into disconnected local
graphs.

## A small growth example

Suppose the repository grows from:

```text
src/
  main.c
  util.c
```

to:

```text
src/
  app/main.c
  app/util.c
  lib/main.c
  lib/io.c
```

The old object mapping:

```make
OBJS := $(patsubst src/%.c,build/%.o,$(SRCS))
```

may now create collisions or confusing paths.

A healthier growth-aware mapping is:

```make
APP_SRCS := $(sort $(wildcard src/app/*.c))
LIB_SRCS := $(sort $(wildcard src/lib/*.c))

APP_OBJS := $(patsubst src/app/%.c,build/app/%.o,$(APP_SRCS))
LIB_OBJS := $(patsubst src/lib/%.c,build/lib/%.o,$(LIB_SRCS))
```

The mapping grew with the repository instead of pretending the old flat model still
explains ownership.

## Discovery policy should be visible, not accidental

The build should make it easy to answer:

- where do sources come from
- why are these files included
- how would a new component join the system

If the answer is "search around until you notice the right wildcard pattern," the
architecture is already too implicit.

This is why some repositories keep discovery policy in a dedicated layer such as
`mk/objects.mk` or `mk/discovery.mk`. It gives the rule a home and a review boundary.

## Naming conventions are part of the public architecture

Developers often think namespacing is only a low-level path concern. It also affects the
human-facing architecture:

- target names
- output directories
- bundle names
- generated artifact names

Good conventions reduce explanation cost. Bad conventions create translation work in every
conversation.

For example, a repository is easier to extend if components follow one target naming model
instead of each subsystem inventing its own build vocabulary.

## Failure signatures worth recognizing

### "The same target name means different things in different places"

That usually means the naming system is too flat or too informal.

### "Adding a new component changed the order of unrelated outputs"

That often points to unstable discovery or unsorted lists.

### "We had to split into sub-builds because naming collisions got out of hand"

That may indicate architecture pressure that namespacing could have solved earlier.

### "A newcomer cannot tell where to add files for a new subsystem"

That means discovery policy is not visible enough.

## A review question that improves growth discipline

Take one growing repository and ask:

1. where discovery is rooted
2. whether discovered lists are sorted
3. how output paths communicate ownership
4. which target names might collide as more components are added
5. whether one coherent DAG is still possible with better naming discipline

If those answers are weak, the repository is likely to get harder to reason about quickly.

## What to practice from this page

Choose one Make-based repository that has more than one subsystem and write down:

1. the discovery roots
2. the naming pattern for outputs
3. one likely future collision
4. one namespacing improvement
5. one place where a broad wildcard should become a rooted, sorted rule

If you can do that cleanly, you are thinking about growth as an architectural problem
instead of a cleanup chore.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why discovery rules are part of architecture
- why rooted and sorted discovery protects stability
- how namespacing keeps ownership visible
- why output paths should communicate component or stage identity
- how repository growth can often be handled inside one coherent DAG before jumping to disconnected builds
