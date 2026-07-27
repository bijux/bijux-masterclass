# Worked Example: Parallel-Safe Build


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Parallel Safety Project Structure"]
  page["Worked Example: Parallel-Safe Build"]
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

This file begins with a tiny scheduling demonstration, then ties the module together
around the real course capstone.

## See parallel scheduling in one minute

Create this Makefile in an empty practice directory:

```make
.PHONY: all alpha beta

all: alpha beta

alpha:
	@printf 'alpha start\n'
	@sleep 2
	@printf 'alpha end\n'

beta:
	@printf 'beta start\n'
	@sleep 2
	@printf 'beta end\n'
```

Compare:

```sh
time make -j1 all
time make -j2 all
```

The serial run takes about four seconds. The parallel run takes about two because `alpha`
and `beta` have no edge between them. Their printed lines may interleave. That is not
automatically a race: the targets do not share output state.

Now add a shared output to both recipes:

```make
alpha:
	@printf 'alpha\n' > combined.txt

beta:
	@printf 'beta\n' > combined.txt
```

Run `make -j2 all` repeatedly. The final file depends on which recipe writes last. The
graph allows concurrent work, but the recipes violate one-writer ownership.

## Layout

```text
capstone/
  Makefile
  mk/
    common.mk
    objects.mk
    rules.mk
  include/
    util.h
    sub.h
  src/
    main.c
    util.c
    sub/sub.c
  repro/
    shared-log-interleaving.mk
    shared-staging-collision.mk
    directory-creation-race.mk
    incremental-edges/
      authored-header/
      generated-producer/
    semantic-faults/
      clock-state/
      order-only-edge/
      pattern-selection/
```

From the repository root, run capstone commands through:

```sh
make PROGRAM=reproducible-research/deep-dive-make capstone-selftest
```

From `programs/reproducible-research/deep-dive-make/capstone/`, use GNU Make directly:

```sh
make selftest
```

On macOS that second command may be `gmake selftest`.

This example matters because it combines three things at once:

- a layered build you want to keep correct
- enough targets that parallel scheduling becomes visible
- several intentionally broken repro files that teach race diagnosis

## A graph view of the simulator

```mermaid
flowchart TD
  all["all"] --> app["app"]
  app --> main["build/main.o"]
  app --> util["build/util.o"]
  app --> sub["build/sub/sub.o"]
  main --> mainc["src/main.c"]
  util --> utilc["src/util.c"]
  sub --> subc["src/sub/sub.c"]
  main --> flags["build/flags.stamp"]
  util --> flags
  sub --> flags
```

This graph matters because it shows the two kinds of parallelism you want:

- object-file targets can become runnable together
- the final link target must wait for all of them

It also shows one hidden-input repair from Module 01 carrying forward: the semantic flags
stamp is now part of the object-file contract.

## What to inspect first

Start with these questions:

1. which targets can become runnable together?
2. which outputs have one clear writer?
3. what would `selftest` need to prove before you trust `-j8`?

This worked example is the concrete home for the rest of the module.

## Layer responsibilities in this build

Read the capstone in this order:

1. `Makefile` for the public interface and selftest entry point
2. `mk/common.mk` for stable policy knobs
3. `mk/objects.mk` for rooted, sorted discovery and output mapping
4. `mk/rules.mk` for atomic publication and dependency edges

That reading order helps you see structure before you see implementation detail.

## Six experiments to run

For every experiment, list the paths each runnable recipe may write. That list is more
useful than a screenshot of interleaved output because it exposes collisions even when a
particular run happens to finish successfully.

### Demonstration 1: Inspect the schedule

Run:

```sh
make -n all
make --trace all
```

The first command shows the candidate work. The second shows why each target is needed.

### Demonstration 2: Prove convergence

Run:

```sh
make clean && make all
make -q all; echo $?
```

You want exit code `0` after the successful build.

### Demonstration 3: Compare serial and parallel

Run:

```sh
make clean && make -j1 all
make clean && make -j8 all
```

The simulator should produce equivalent declared artifacts across both runs.

### Demonstration 4: Use the repro pack as contrast

Run one broken repro, for example:

```sh
make -f repro/shared-staging-collision.mk clean
make -f repro/shared-staging-collision.mk -j8 all
```

Then explain why the healthy capstone does not suffer from the same problem.

### Demonstration 5: Observe an order-only directory

Find a target that uses `| $(BUILD_DIR)/` or another directory prerequisite. Touch the
directory and run the build again. The directory must exist before the recipe runs, but a
directory timestamp change should not force content rebuilds.

### Demonstration 6: Trace one object

Choose one object file, delete only that file, and run:

```sh
make --trace all
```

Explain why that object and its downstream link rebuild while independent objects stay
untouched.

## Diagnose the broken repro without guessing

When a repro fails intermittently, use this order:

1. run `make -n` to identify recipes Make considers independent
2. read those recipes and list every written path, including temporary files and logs
3. run the smallest reproduction repeatedly under `-j8`
4. inspect the shared path after each run
5. redesign the graph so each worker owns one path and one target owns aggregation
6. compare serial and parallel manifests after the repair

Do not begin with `.NOTPARALLEL`, a global lock, or a chain of order-only prerequisites.
Those can suppress overlap without describing the data relationship. The repaired graph
should explain why work waits, not merely force it to wait.

Use this short incident note:

| Question | Evidence |
| --- | --- |
| Which targets were runnable together? | dry-run or trace |
| Which path had multiple writers? | recipe inspection |
| What failure did repeated parallel runs expose? | output transcript or manifest |
| Which ownership change repaired it? | before-and-after graph |
| Why is the result now equivalent under `-j1` and `-j8`? | artifact comparison |

## What this example should teach you

By the time you finish this file, you should be able to point at the simulator and say:

- where runnable targets come from
- where output ownership is enforced
- where hidden semantic state is modeled honestly
- where selftest proves the build instead of merely running it
- why the documented paths and commands correspond to files that actually exist
