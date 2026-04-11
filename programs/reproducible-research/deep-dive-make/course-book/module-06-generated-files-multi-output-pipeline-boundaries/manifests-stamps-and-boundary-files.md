# Manifests, Stamps, and Boundary Files

Once a team learns that stamps and manifests can help with generation, a new problem often
appears:

they start using boundary files everywhere, including places where the real issue is simply
a missing edge.

This page is about drawing that line carefully.

A good boundary file makes the build easier to explain. A bad one gives the build another
filename without making the truth any clearer.

## The sentence to keep

Before adding a stamp or manifest, ask:

> what semantic boundary does this file represent that the graph cannot already express
> directly through a normal published output?

If you cannot answer that, you probably do not need the file.

## What a boundary file is for

Boundary files usually serve one of three honest roles:

1. they represent completion of a multi-output generation event
2. they capture a semantic input that has no natural downstream file of its own
3. they declare a contract between one stage of a pipeline and the next

These are real jobs. They are not excuses to avoid modeling content dependencies.

## What a boundary file is not for

Boundary files are a poor fit when they are being used to:

- hide a missing prerequisite on a real source or generated output
- avoid naming the actual file a consumer reads
- make a vague process feel more structured without improving the graph

For example, this is often a smell:

```make
compile.stamp: gen_header.py
	touch $@

main.o: compile.stamp
	$(CC) -Ibuild/include -c main.c -o main.o
```

If `main.o` actually consumes `build/include/config.h`, then the object file should depend
on the header. A stamp here would obscure the real consumer edge.

## The difference between direct content and boundary truth

Use a direct content edge when a target truly reads a file.

Use a boundary file when the target depends on a build event or contract that is not well
represented by one ordinary file.

That distinction sounds abstract until you compare two examples.

### Direct content edge

```make
main.o: main.c build/include/config.h
	$(CC) -Ibuild/include -c $< -o $@
```

This is correct because the compiler really reads the header.

### Boundary file edge

```make
API_GEN_MANIFEST := build/api.manifest

$(API_GEN_MANIFEST): schema/api.yml scripts/gen_api.py | build/
	python3 scripts/gen_api.py
	printf 'schema=api.yml\n' > $@

docs/api-summary.txt: $(API_GEN_MANIFEST)
	python3 scripts/summarize_api.py $< > $@
```

This is plausible if the next stage cares about the completion contract or metadata of the
generation event rather than one single generated file.

## Stamps and manifests are not interchangeable names

The names are close, but the roles often differ:

| File kind | Typical role | Healthy use |
| --- | --- | --- |
| stamp | completion fact | "this generator finished successfully" |
| manifest | descriptive boundary file | "these outputs correspond to this schema, mode, or fingerprint" |

You do not need rigid purity here, but the distinction helps learners think better:

- stamps usually emphasize event completion
- manifests usually emphasize inspectable build meaning

## Convergence still matters

A boundary file should converge just like any other generated artifact.

This is unhealthy:

```make
build/api.manifest:
	@date > $@
```

This is healthier:

```make
build/api.manifest:
	@printf 'schema_hash=%s\n' "$$(sha256sum schema/api.yml | awk '{print $$1}')" > $@.tmp
	@cmp -s $@.tmp $@ 2>/dev/null || mv $@.tmp $@
	@rm -f $@.tmp
```

The difference is simple:

- the first file records entropy
- the second file records a semantic fact and changes only when that fact changes

That is exactly the standard boundary files should meet.

## A useful manifest example

Suppose one generator emits:

- `api.h`
- `api.json`
- `api-types.txt`

and the next pipeline stage needs to know exactly which schema and mode produced that set.

A manifest can make that boundary explicit:

```make
API_MANIFEST := build/api.manifest

$(API_MANIFEST): schema/api.yml scripts/gen_api.py | build/
	@printf 'schema=schema/api.yml\nmode=%s\n' '$(MODE)' > $@.tmp
	@cmp -s $@.tmp $@ 2>/dev/null || mv $@.tmp $@
	@rm -f $@.tmp
```

Now the manifest is doing real work:

- it names the boundary facts
- it gives later stages one inspectable contract file
- it can rebuild honestly when those facts change

## Why this still requires direct output edges

Even with a manifest, do not forget the direct output relationships where they matter.

If a C compilation step reads `api.h`, keep that direct edge:

```make
main.o: main.c api.h
```

The manifest does not replace the header. It complements the generation boundary where that
boundary matters.

This is the subtle lesson of the page: boundary files add clarity only when they sit beside
real output relationships, not when they erase them.

## A stamp example that is justified

Suppose a generator publishes several files atomically and downstream work only needs to
know that generation completed successfully:

```make
GEN_STAMP := build/codegen.stamp

$(GEN_STAMP): schema/api.yml scripts/gen_api.py | build/
	python3 scripts/gen_api.py
	touch $@

tests/generated-contract.txt: $(GEN_STAMP)
	python3 scripts/check_codegen.py > $@
```

This is defensible if `tests/generated-contract.txt` is validating the generation event
itself, not reading one specific generated file directly.

Again, the important thing is that the boundary file represents a truth that would
otherwise be awkward to name.

## Failure signatures worth recognizing

### "We added a stamp and the build still feels mysterious"

That often means the file does not represent a clear semantic boundary.

### "Consumers depend on a stamp, but they really read a generated file"

That usually means the direct content edge has been replaced with something less truthful.

### "The manifest changes every run"

That means the boundary file records unstable data instead of stable build meaning.

### "Nobody can say what this stamp stands for"

That is enough reason to distrust it.

## A review question that improves boundary-file design

Take any stamp or manifest and ask:

1. what exact fact or event does this file represent
2. why can that fact not be expressed better by an ordinary output dependency
3. which targets should depend on this file
4. which targets should still depend on direct generated outputs
5. does the file converge when the represented fact stays the same

If those answers are weak, the boundary file is weak too.

## What to practice from this page

Choose one stamp or manifest in the capstone or your own build and explain:

1. whether it represents completion, meaning, or both
2. why it exists
3. which targets should depend on it
4. which targets should not depend on it
5. how you would tell if it is hiding a missing edge

If you can do that cleanly, you understand the value of boundary files much better than a
team that merely "uses stamps."

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- when a stamp or manifest is justified
- why direct content edges still matter
- how a boundary file can clarify a generation stage
- why convergence is a requirement for boundary files too
- how to spot a stamp that is hiding a real dependency
