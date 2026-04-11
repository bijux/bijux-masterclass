# Generator Pipelines and Atomic Publication

Generated outputs become much riskier once the generator stops being one clean command and
starts becoming a pipeline:

- generate intermediate data
- transform it
- validate it
- write several final outputs
- maybe update a manifest too

At that point the most important question is no longer "did the script run?" It is:

> when are downstream targets allowed to trust the result?

This page teaches that answer.

## The sentence to keep

For a generator pipeline, ask:

> where is the publication boundary, and what must be true before any downstream target can
> treat the outputs as complete?

That is the heart of pipeline design.

## Pipelines fail differently from simple generators

A simple single-output rule often fails in obvious ways: the file is there or it is not.

Pipelines fail more subtly:

- one stage succeeds, another fails
- partial outputs remain on disk
- one output is fresh, another is stale
- validation should have rejected the result, but publication happened too early

This is why pipelines need an explicit publication contract rather than a casual "the
script writes files" understanding.

## Publication should happen after success, not during hope

Suppose a generator pipeline does:

1. render a header
2. render a JSON schema
3. validate the pair
4. move them into the trusted output directory

That means the publication event is step 4, not step 1.

If the build lets downstream targets see the header before validation completed, the graph
is already trusting partial work.

That is the core lesson: generation and publication are not always the same moment.

## Temporary paths are part of safe publication

One healthy pattern is:

```make
build/api.h build/api.json &: schema/api.yml scripts/gen_api.py | build/
	python3 scripts/gen_api.py --out-dir build/tmp
	python3 scripts/validate_api.py build/tmp/api.h build/tmp/api.json
	mv build/tmp/api.h build/api.h
	mv build/tmp/api.json build/api.json
```

The idea is not "always use `tmp` because it looks professional." The idea is:

- incomplete work stays outside the trusted output paths
- validation happens before final publication
- downstream targets only see the files once the pipeline succeeded

That is a much stronger contract than writing directly into the final paths throughout the
pipeline.

## Atomic publication is about trust

When the module says "atomic publication," the important meaning is not kernel-level
technical perfection in every environment. The important meaning is:

> do not let downstream work observe a half-published result and mistake it for truth.

Often that means:

- write to a temporary file
- validate the full result
- move the file into place

For directory-level or multi-output publication, it may mean staging several outputs and
then moving or touching the final boundary only after all of them are ready.

## A useful single-file example

Single-file generation can still benefit from publication discipline:

```make
build/include/config.h: schema/config.yml scripts/gen_config.py | build/include/
	@python3 scripts/gen_config.py schema/config.yml > $@.tmp
	@python3 scripts/validate_header.py $@.tmp
	@mv $@.tmp $@
```

This rule is easier to trust because:

- an invalid header never becomes the published header
- the published path changes only after validation
- the consumer edge still points at one clean output path

That same pattern scales to larger pipelines.

## Multi-output publication needs one clear finishing point

For coupled outputs, the question becomes:

which step marks the set as complete?

One answer is grouped targets with staged files:

```make
api.h api.json &: schema/api.yml scripts/gen_api.py | build/
	@python3 scripts/gen_api.py --out-dir build/tmp
	@python3 scripts/validate_api.py build/tmp/api.h build/tmp/api.json
	@mv build/tmp/api.h api.h
	@mv build/tmp/api.json api.json
```

Another answer is a stamp or manifest that is touched or published only after both final
outputs are in place.

The important thing is that the build names the finishing point instead of letting
publication leak across multiple partial steps.

## Cleanup on failure matters

Pipelines that fail mid-run need one more discipline:

- remove temporary artifacts that are not trustworthy
- do not leave behind final outputs that were only partially updated

That usually means the recipe should fail before moving temporary outputs into their final
paths, or explicitly remove partial temp state on the way out.

The standard here is not cosmetic tidiness. It is preventing the next build step from
treating garbage as truth.

## A simple pattern with explicit cleanup

```make
build/report.json: data/input.csv scripts/gen_report.py | build/
	@python3 scripts/gen_report.py data/input.csv > $@.tmp
	@python3 scripts/check_report.py $@.tmp
	@mv $@.tmp $@ || { rm -f $@.tmp; exit 1; }
```

In a real shell recipe you may want clearer trap handling, but the design point is
constant:

- invalid or incomplete content should die in temporary space
- the final target path should remain the trustworthy boundary

## Pipelines create stage boundaries on purpose

Some pipelines legitimately need multiple trusted stages:

- raw generated output
- normalized generated output
- packaged generated bundle

That is fine, but each stage must still answer:

- what file or boundary represents completion here
- who consumes this stage
- what validates it before the next stage trusts it

In other words, a pipeline may have several boundaries, but each one still needs the same
honest publication logic.

## Failure signatures worth recognizing

### "The generated file exists, but it was only half-written when the consumer saw it"

That means publication happened too early.

### "Validation failed, but the final output path still changed"

That means the final path stopped being a trustworthy boundary.

### "The pipeline leaves a mix of old and new outputs after failure"

That means coupled publication is being modeled too loosely.

### "Temporary outputs keep leaking into later stages"

That usually means temporary space and trusted space were not separated clearly enough.

## A review question that improves pipeline design

Take one generator pipeline and ask:

1. which step first creates intermediate content
2. which step validates the content
3. which step publishes the trusted outputs
4. what happens on failure before publication
5. which files or boundary nodes downstream targets are allowed to depend on

If those answers are weak, the pipeline contract is weak too.

## What to practice from this page

Choose one multi-stage generator in the capstone or your own build and write down:

1. the temporary paths
2. the validation step
3. the publication step
4. the cleanup behavior on failure
5. the exact output path or boundary file consumers should trust

If you can explain those without hand-waving, the pipeline has a real publication contract.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why pipeline generation and publication are not automatically the same moment
- why temporary paths help keep partial work out of trusted output paths
- what atomic publication means in practical build terms
- why validation should happen before downstream trust
- how to tell whether a pipeline leaves behind untrustworthy partial outputs
