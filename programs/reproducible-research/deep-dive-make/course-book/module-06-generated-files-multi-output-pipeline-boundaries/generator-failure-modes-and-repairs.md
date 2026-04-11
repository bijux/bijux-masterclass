# Generator Failure Modes and Repairs

By the time a team reaches generator trouble in a real repository, the failure rarely looks
clean.

It sounds more like this:

- "the header is there, but the code still looks stale"
- "it only breaks under `-j`"
- "the manifest changes every run"
- "the generator failed, but some outputs survived"
- "nobody knows which file the next stage is supposed to trust"

Those are not five unrelated mysteries. They are recurring failure shapes.

This page is about naming those shapes and giving the learner a repair loop that stays
calm under pressure.

## The sentence to keep

When generation misbehaves, ask:

> is the problem a missing semantic input, a dishonest publication unit, an unstable
> boundary file, an early publication bug, or a confused consumer edge?

That question narrows the repair space fast.

## Failure mode 1: stale generated output

Symptom:

- a source schema changed
- the generated file did not rebuild
- or the generated file rebuilt but consumers did not

Usual root cause:

- the generator rule is missing a semantic input
- or a consumer depends on the wrong thing

Example:

```make
build/include/config.h: scripts/gen_config.py
	python3 scripts/gen_config.py data/config.yml > $@
```

If `data/config.yml` changes and the header does not rebuild, the graph is lying.

Repair:

- add the missing semantic input to the generator target
- make consumers depend on the generated header they actually read

This is the simplest generator bug and still one of the most common.

## Failure mode 2: duplicate execution under `-j`

Symptom:

- one generator prints twice
- or coupled outputs get rebuilt inconsistently under parallel execution

Usual root cause:

- a multi-output generation event was modeled too loosely

Example:

```make
api.h api.json: schema/api.yml scripts/gen_api.py
	python3 scripts/gen_api.py
```

Repair:

- use grouped targets if available
- or use a stamp that represents one successful generation event

The important point is not "parallel builds are tricky." The important point is that the
graph failed to name the single publication event clearly enough.

## Failure mode 3: unstable manifest or stamp

Symptom:

- `make -q all` keeps returning `1`
- the manifest rewrites itself every run
- the build never settles even though no semantic input changed

Usual root cause:

- the boundary file records unstable data such as timestamps or host-specific noise

Example:

```make
build/api.manifest:
	@date > $@
```

Repair:

- record only semantic facts
- compare temporary content with the existing file
- publish only when the represented meaning changed

This is usually a convergence bug disguised as provenance.

## Failure mode 4: partial publication after failure

Symptom:

- the generator fails
- some final outputs are still present
- downstream work may now consume half-trusted files

Usual root cause:

- the rule published into final output paths before the whole generation pipeline succeeded

Repair:

- generate in temporary space
- validate before publication
- move into final paths only after the full generation succeeded

This is where publication discipline matters most.

## Failure mode 5: confused consumer edges

Symptom:

- a downstream target depends on the generator script or a stamp
- but the real consumed content is a generated file

Usual root cause:

- producer logic and consumer logic were mixed together

Example:

```make
main.o: main.c gen_api.py
	$(CC) -Ibuild/include -c $< -o $@
```

If the compilation really consumes `build/include/api.h`, then the object file should
depend on the header. A stamp or script dependency may complement that boundary elsewhere,
but it should not replace the direct content edge.

Repair:

- restore the direct output dependency for actual consumers
- keep stamps and manifests only where they represent a real boundary fact

## The repair loop that keeps working

When you hit a generator incident, use the same sequence every time:

1. reproduce it with the smallest command that still shows the failure
2. run `make --trace` to see what Make believed
3. identify which of the five failure shapes fits best
4. repair the graph or publication contract
5. rerun convergence and, when relevant, a parallel build

This loop matters because generator incidents often tempt teams into random shell edits.
The loop keeps the investigation anchored in graph truth.

## A small incident walkthrough

Suppose you see:

```sh
make -j2 all
```

and the log prints:

```text
running api generator
running api generator
```

The clean diagnosis is not "parallelism is broken." It is:

- one logical generation event ran twice
- the likely failure class is duplicate execution under `-j`
- the repair should focus on grouped targets or a stamp boundary

That level of diagnosis is what this page is trying to teach.

## Why `--trace` belongs at the center

Generator incidents often trigger emotional debugging:

- re-run
- delete files manually
- add sleeps
- force serial mode
- blame shell timing

`--trace` pushes the investigation back to the graph. It helps you ask:

- which target was considered stale
- which prerequisite edge triggered the rebuild
- which rule location Make used

That does not solve every generator problem by itself, but it prevents the repair from
drifting into folklore.

## Parallel and convergence checks are the finishing tests

A generator fix is not finished just because one command succeeded once.

You usually want at least these checks:

```sh
make all
make -q all; echo $?
make -j2 all
make -q all; echo $?
```

Why these matter:

- the first pair checks convergence
- the parallel run checks that publication and coupling stay honest under pressure
- the final query checks that the repaired model still settles

This is the same standard the earlier modules built. Module 06 is just applying it to
generation.

## Failure signatures worth recognizing quickly

### "The fix only works after `rm -rf build`"

That often means the incremental graph is still lying.

### "Serial works, parallel flakes"

That often points to coupled publication or early visibility of partial outputs.

### "The manifest proves nothing but still changes every run"

That means the boundary file is unstable noise.

### "Consumers rebuilt, but for the wrong reason"

That usually means the graph is wired through producer internals instead of published
artifacts.

## A review question that improves generator repairs

Take one broken generator incident and ask:

1. which failure class fits best
2. what target or boundary file is mis-modeled
3. what `--trace` line would prove the current behavior
4. what graph change would make the publication contract more honest
5. which post-fix commands would prove convergence and pressure safety

If those answers are strong, the repair is usually on the right path.

## What to practice from this page

Pick one generator failure mode and write a short incident note:

1. the symptom
2. the likely failure class
3. the evidence command
4. the graph or publication repair
5. the verification command after the repair

If you can do that without drifting into vague blame, you have learned the real lesson of
this page.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- the five generator failure classes on this page
- why duplicate execution is a publication-model bug, not just a parallelism annoyance
- why unstable manifests are convergence bugs
- why consumer edges must still point at the content actually read
- why a generator repair is incomplete until convergence and pressure checks pass
