# Performance Measurement and Make Overhead


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Portability Hermeticity Failure Modes"]
  page["Performance Measurement and Make Overhead"]
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

Build-performance conversations go bad quickly when nobody distinguishes between these
different costs:

- the time Make spends parsing and deciding
- the time recipes spend doing actual work
- the time the logs spend burying the evidence
- the time humans waste blaming the wrong layer

That is why this page is not called "performance tricks." The first job is not to trick
Make into looking faster. The first job is to identify which part of the build is
expensive.

## The sentence to keep

When someone says "Make is slow," ask them:

> slow in which layer: parse time, rebuild decision time, recipe execution time, or log
> handling?

Without that question, the rest of the discussion is mostly theater.

## Measure before you optimize

This sounds obvious, but many build changes still skip it. Engineers:

- add `eval`
- split files aggressively
- rewrite rules into generated macros
- introduce recursion
- switch tools entirely

before they can show where the time went.

Module 05 insists on a stricter habit:

1. measure one baseline
2. explain what that measurement includes
3. change one design variable
4. measure again

That is the minimum standard for believable performance claims.

## The main layers to separate

### Parse and evaluation cost

This is the time Make spends reading files, expanding variables, loading includes, and
building its internal model of the world.

Warning signs:

- huge `make -n` time even when no recipes run
- heavy use of `$(shell ...)`, `eval`, or broad wildcard discovery
- many included files with expensive parse-time computation

### Decision cost

This is the time Make spends deciding whether targets are up to date.

Warning signs:

- lots of tiny targets with complex prerequisite graphs
- excessive implicit rule search
- repeated directory scans or unstable discovery patterns

### Recipe cost

This is the actual time spent compiling, archiving, copying, testing, packaging, and so
on.

Warning signs:

- `make -n` is fast, but real builds are slow
- individual tool invocations dominate the wall clock
- parallelism is available but not being exploited

### Log and trace handling cost

This is not always a machine bottleneck, but it is often a human bottleneck. Logs that are
too large or unordered turn diagnosis into a performance problem of their own.

Warning signs:

- `--trace` output is unmanageable
- recursive logs interleave so badly that nobody can follow them
- the team stops using evidence because the output is too painful

## A tiny baseline loop

Start with something simple:

```sh
/usr/bin/time -p make -n all >/dev/null
/usr/bin/time -p make all >/dev/null
make --trace all > build/trace.log
wc -l build/trace.log
```

This already gives you:

- a decision-only baseline from `make -n`
- a full-build baseline from `make all`
- a rough trace-volume metric

That is not a full profiler. It is enough to stop guessing blindly.

## Why `make -n` is useful here

`make -n` is not only a debugging command. It is also a crude performance lens.

If `make -n all` is already slow, the bottleneck is not the compiler. It is probably one
of these:

- parse-time shell calls
- heavy variable expansion
- too much rule or include complexity
- expensive graph discovery

That is a very different diagnosis from "the build needs more cores."

## Trace volume is a legitimate metric

Engineers sometimes dismiss log size as cosmetic. It is not.

If the trace output for a normal build is so large that nobody can inspect it, then the
build's evidence surface has become expensive to use.

This matters because the whole course is built on proof. A build that technically exposes
evidence but practically buries it is harder to operate.

A simple metric such as line count can still be useful:

```sh
make --trace all > build/trace.log
wc -l build/trace.log
```

The goal is not "fewest lines wins." The goal is to notice when changes dramatically
inflate the explanation surface.

## Common parse-time performance traps

### Repeated `$(shell ...)` calls

Each shell escape adds cost and often adds hidden inputs too.

This shape is usually a warning sign:

```make
FILES := $(shell find src -name '*.c')
TOOLS := $(shell command -v python3)
STAMP := $(shell date +%s)
```

Especially when repeated across multiple files.

### Overuse of `eval`

`eval` can be legitimate, but it increases mental and performance cost together. If a rule
set could be expressed clearly without generated makefile text, that simpler shape is often
easier to maintain and faster to reason about.

### Broad implicit rule search

If the build quietly relies on built-in rules and suffix behavior, Make may spend time
searching for patterns you never intended to use.

Sometimes adding explicit rules or using `-rR` during audits clarifies both correctness and
decision cost.

## Common recipe-time traps

Performance work also gets distorted when Make is blamed for slow tools.

Examples:

- a compiler invocation is expensive because of optimization level or dependency scanning
- a packaging step recompresses large assets repeatedly
- a test suite is doing the real work while Make just orchestrates it

In those cases, rewriting Make logic may change almost nothing.

That is why you compare `make -n` and `make all`. They help separate orchestration cost
from tool cost.

## A simple comparison pattern

Imagine these results:

```text
/usr/bin/time -p make -n all   -> 2.8s
/usr/bin/time -p make all      -> 3.0s
```

That suggests most of the cost is in parse and decision work, not recipes.

Now imagine:

```text
/usr/bin/time -p make -n all   -> 0.2s
/usr/bin/time -p make all      -> 18.0s
```

That suggests Make itself is not the main performance problem.

This kind of comparison is basic, but it stops many wrong turns.

## Parallelism is not a universal fix

When a build is slow, people often reach for `-j` first.

That can help, but it does not fix:

- heavy parse-time computation
- needless trace volume
- recursive boundaries that lose the jobserver
- serial bottlenecks inside a single expensive recipe

Parallelism helps when there is real independent work to schedule. It is not a substitute
for understanding the cost structure.

## Performance changes need proof too

The course has been insisting on proof for correctness. The same standard belongs here.

A believable performance change should say:

- the baseline measurement
- what changed
- the after measurement
- which layer improved
- any tradeoff in readability or correctness

Without that, a "performance improvement" is often just a preference with a benchmark-shaped story.

## Failure signatures worth recognizing

### "Nothing is compiling, but `make -n` still feels heavy"

That points at parse, expansion, or discovery cost.

### "The full build is slow, but dry-run is cheap"

That points away from Make orchestration and toward recipe work.

### "The build is technically correct, but nobody can use the trace output anymore"

That means the evidence surface has become operationally expensive.

### "We rewrote the Makefiles and got no measurable speedup"

That usually means the actual bottleneck was elsewhere.

## A review question that improves performance work

Ask anyone proposing a performance fix to answer five things:

1. what exact measurement showed the problem
2. which layer is expensive
3. what change addresses that layer
4. how the new measurement compares
5. what readability or correctness cost the change introduces

This is a very effective way to filter out cargo-cult optimizations.

## What to practice from this page

Take one build route in the capstone or your own repository and produce a short report:

1. `make -n` time
2. full build time
3. trace line count
4. your best guess about which layer dominates
5. one next experiment that would test that guess

If you can produce that report cleanly, you are doing performance engineering instead of
performance folklore.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why build-performance complaints need layer separation
- why `make -n` is a useful performance lens
- why trace volume can be a real operational cost
- why some performance problems are really recipe problems, not Make problems
- why every performance fix needs a before-and-after story
