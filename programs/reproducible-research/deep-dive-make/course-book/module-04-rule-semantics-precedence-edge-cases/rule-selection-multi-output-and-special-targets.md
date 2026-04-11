# Rule Selection, Multi-Output, and Special Targets

By the time engineers reach this part of Make, they often know enough syntax to be
dangerous.

They have learned pattern rules, special targets, and maybe a few features from blog
posts or old repositories. The trouble is that advanced Make features are not impressive
because they are obscure. They are useful only when they preserve the same correctness
principles the earlier modules taught:

- one owner per output
- honest edges
- deterministic publication
- convergence under repeated runs
- parallel safety when the graph allows parallelism

This page is about the sharp features that tempt people to cut corners.

## The sentence to keep

When a rule feature feels powerful, ask one question immediately:

> what correctness contract does this feature require me to uphold?

If you cannot answer that, the feature is probably not ready to be used in the build.

## Pattern rules are good until they overlap

Pattern rules are often the first advanced feature people use:

```make
build/%.o: src/%.c
	$(CC) -c $< -o $@
```

This is healthy because it is easy to explain:

- every `build/name.o` comes from `src/name.c`
- the ownership is clear
- the expansion is local and inspectable

Trouble starts when multiple pattern rules can plausibly claim the same target.

Example:

```make
%.o: %.c
	$(CC) -c $< -o $@

%.o: generated/%.c
	$(CC) -c $< -o $@
```

Now a learner has to ask which rule Make will choose and why. If the answer is "I think it
uses the second one," the design is already too murky.

The healthy fix is usually to make the patterns non-overlapping or to use explicit/static
pattern rules for the ambiguous cases.

## Static pattern rules are often clearer than clever generality

Static pattern rules let you define a small controlled set of targets:

```make
OBJECTS := build/main.o build/util.o

$(OBJECTS): build/%.o: src/%.c
	$(CC) -c $< -o $@
```

This is less magical than a very broad implicit rule set. It says exactly which targets are
in scope.

Use static pattern rules when:

- you want the convenience of pattern substitution
- but you do not want the whole tree to become eligible for the rule

That is a good trade when you are teaching or maintaining a repository meant to stay
readable.

## Multi-output generators require one logical publication step

This is where even experienced engineers make avoidable mistakes.

Suppose one generator produces both `api.h` and `api.json`. A naive rule often looks like
this:

```make
api.h api.json: gen_api.py schema.yml
	python3 gen_api.py
```

The intuition is understandable: both files come from the same command, so list them both.

The risk is that Make still needs a correct model of how that generation happens. Under
parallel or incremental operation, naive multi-target rules can produce:

- duplicate generator invocations
- partial publication where one file is newer and the other is stale
- confusion about which output is the true driver of rebuild decisions

The rule is only safe if the semantics guarantee one logical invocation per regeneration.

## Grouped targets are the clean answer when available

GNU Make 4.3 introduced grouped targets with `&:`:

```make
api.h api.json &: gen_api.py schema.yml
	python3 gen_api.py
```

This tells Make that the outputs belong to one grouped update. That is much closer to the
real semantics of the generator.

If your supported Make version includes grouped targets, prefer them for genuine
multi-output generators.

## A stamp fallback is better than pretending

If grouped targets are not available, use a stamp that represents the successful
publication event:

```make
GEN_STAMP := build/api.stamp

$(GEN_STAMP): gen_api.py schema.yml | build/
	python3 gen_api.py
	touch $@

api.h api.json: $(GEN_STAMP)
```

This is not as elegant as grouped targets, but it is honest. It says:

- one recipe owns the generation event
- the outputs are downstream of that event
- the build graph has a stable point to reason about

The stamp is not busywork. It is the missing node that makes the generation explainable.

## `.PHONY` is for orchestration, not real artifacts

One of the most common rule-level mistakes is declaring a real file target as phony.

Example:

```make
.PHONY: app

app:
	$(CC) main.c -o app
```

This guarantees `app` runs every time because `.PHONY` tells Make the target is not a file
truth claim.

That is useful for targets like:

- `clean`
- `test`
- `lint`
- `help`

It is destructive for real artifacts such as binaries, archives, manifests, or generated
headers.

## `.NOTPARALLEL` is a last resort, not a design strategy

`.NOTPARALLEL` can be valid when a tool genuinely cannot be modeled safely for concurrent
execution. But it is often used to hide graph bugs:

- shared temp files
- multi-writer outputs
- missing order relationships
- non-atomic publication

If `-j1` or `.NOTPARALLEL` is the only reason the build behaves, treat that as a report of
missing truth, not as a final repair.

## `.WAIT` is a barrier, not a substitute for real edges

GNU Make 4.4 added `.WAIT` as a way to impose barrier-style ordering in prerequisite
lists. It can be useful, but it should not replace honest prerequisites.

Use a real edge when content or publication truly depends on another artifact.

Use a barrier only when the scheduling relationship is real but not naturally expressed by
a normal file dependency.

That distinction matters because barriers are easier to misuse as ordering folklore.

## `.SECONDARY` and friends can preserve files, but they do not fix semantics

Special targets such as `.SECONDARY`, `.PRECIOUS`, and `.INTERMEDIATE` affect how Make
treats intermediate files. They can be helpful for debugging or for preventing deletion of
useful intermediates.

They do not solve:

- missing prerequisites
- bad output ownership
- multi-output publication bugs
- hidden inputs

In other words, file retention policy is not the same thing as graph truth.

## `.ONESHELL` changes recipe execution shape

`.ONESHELL` makes all lines in a recipe run in one shell instance instead of separate
invocations.

That can be useful for complex shell logic, but it changes failure behavior and state
sharing inside recipes. For example:

- environment exports on one line remain visible to later lines
- `cd` persists within the recipe
- shell error handling needs to be set deliberately

This is not automatically bad. It is a reminder that special targets often change the
semantics more than their short syntax suggests.

## A small broken-generator example

Use this sketch:

```make
.PHONY: clean

api.h api.json: gen_api.py
	@printf 'running generator\n'
	@python3 gen_api.py

clean:
	rm -f api.h api.json
```

Now imagine the generator updates both files. Ask the learner:

- what guarantees one invocation under `-j4`
- what path tells Make the publication completed as one event
- how would you prove the repair with `--trace`

The answer should move them toward grouped targets or a stamp.

## Failure signatures worth recognizing

### "Only one of the generated files updated"

That usually means a multi-output generator was modeled as if each output were independent.

### "This target keeps rebuilding forever"

That often points to `.PHONY` on a real artifact or to publication that never settles.

### "The build passes only when serialized"

That often signals missing edges or shared mutable outputs, not a legitimate need for
`.NOTPARALLEL`.

### "I do not know which rule Make chose"

That means the rule space is too broad or overlapping. Reduce it until the answer becomes
obvious.

## A better way to review advanced rule features

When someone proposes an advanced rule form, ask them to explain five things:

1. which recipe invocation owns the publication event
2. which files are the semantic inputs
3. whether parallel runs can trigger duplicate or competing writers
4. how the rule converges on a second run
5. which Make feature is required and what the fallback is

If those answers are strong, the feature is probably justified.

## What to practice from this page

Take one advanced rule pattern in the capstone or your own repository and rewrite the
explanation in plain language:

1. what outputs does it own
2. why does Make choose this rule
3. how many times should the recipe run per logical regeneration
4. what would break under `-j`
5. which special target, if any, is truly justified

If you can answer those without hiding behind syntax, the rule is probably sound.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why overlapping pattern rules make builds harder to reason about
- why multi-output generation needs one logical publication event
- why grouped targets or a stamp are safer than naive multi-target rules
- why `.PHONY` belongs on orchestration targets, not real artifacts
- why special targets can be useful without being valid substitutes for graph truth
