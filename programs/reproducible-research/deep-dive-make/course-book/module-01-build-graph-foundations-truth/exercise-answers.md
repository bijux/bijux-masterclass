# Exercise Answers


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Build Graph Foundations Truth"]
  page["Exercise Answers"]
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

Use this file after you have written your own answers. The value is in comparing your
reasoning, not in copying the wording here.

## Exercise 1: Draw the graph

The important answer is that `app`, `build/main.o`, and `build/util.o` are real artifact
targets, while `all` is a convenience target. `include/util.h` is a prerequisite for both
object files because changing the header changes the meaning of both objects.

A strong answer also says why that shared header edge matters: if you omit it, the build
can silently keep stale object files after a header edit.

## Exercise 2: Find a hidden input

`CFLAGS` is a hidden input because it changes the compiler invocation without changing any
file in the prerequisite list. The repair is to turn the semantic value of the flags into
evidence the graph can depend on, such as a stable stamp or manifest.

One acceptable sketch is:

```make
FLAGS_LINE := CFLAGS=$(CFLAGS)
FLAGS_ID := $(shell printf '%s' "$(FLAGS_LINE)" | cksum | awk '{print $$1}')
FLAGS_STAMP := build/flags.$(FLAGS_ID).stamp
```

The key is not the exact hash tool. The key is that the graph now has evidence that moves
when the semantic input moves.

## Exercise 3: Review rule ownership

An explicit rule keeps ownership obvious because the target path is named directly. A
pattern rule is still correct when the mapping is clear, for example `build/%.o:
src/%.c`. The danger starts when multiple rules can publish the same path or when a
multi-output generator is treated as if each file were independent.

The strongest answers mention reviewability, not just correctness. Ownership matters
because another engineer should be able to say where a file comes from without tracing
three alternative paths.

## Exercise 4: Explain evaluation timing

`:=` computes the value when Make reads the file. `=` stores the expansion for later.
For discovered source lists, `:=` is usually the safer Module 01 default because it gives
you one stable value for the whole invocation.

If you add that "`=` is not wrong, but easier to misuse for graph-shaping values,"
that is a strong answer. The important distinction is timing, not moral purity.

## Exercise 5: Prove safe publication

A safe answer writes to `$@.tmp` first and renames only on success. The proof statement is
that a failed recipe leaves either no final target or the previously known-good target,
but never a half-written new target.

A stronger answer also includes the drill:

1. force the rule to fail before the final rename
2. inspect the final target path
3. rerun the build and confirm clean recovery

That turns the answer from principle into evidence.

## Exercise 6: Write the smallest useful Makefile

A complete answer can stay small:

```make
.DEFAULT_GOAL := all
.PHONY: all

all: message.upper.txt

message.upper.txt: message.txt
	tr '[:lower:]' '[:upper:]' < $< > $@
```

The first run creates the target. The second run does nothing because
`message.upper.txt` exists and is newer than `message.txt`. Editing `message.txt` makes
the prerequisite newer, so the recipe runs again.

Check that explanation with:

```sh
make --trace all
make --trace all
printf 'another line\n' >> message.txt
make --trace all
```

## Exercise 7: Predict automatic variables

For the rule shown:

- `$@` expands to `report.txt`
- `$<` expands to `title.txt`
- `$^` expands to `title.txt results.txt`

The resulting shell command is:

```sh
cat title.txt results.txt > report.txt
```

`$<` would be appropriate if the recipe consumed only the first input. `$^` is correct
here because the recipe concatenates every declared prerequisite.

## Exercise 8: Remove duplicated compile recipes

The reusable rule is:

```make
build/%.o: src/%.c | build/
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

build/:
	mkdir -p $@
```

If `build/gamma.o` is a prerequisite of the final target, Make binds `%` to `gamma` and
looks for `src/gamma.c`. The rule reduces duplicated policy; it does not remove the need
to list or discover which object files the final target requires.

A strong answer also checks `make -n` before and after the refactor and confirms that the
compile commands are equivalent.

## Exercise 9: Diagnose a stale header build

The broken shape is:

```make
build/alpha.o: src/alpha.c config.h
build/beta.o: src/beta.c
```

Both recipes may compile successfully, but Make has no evidence connecting `config.h` to
`build/beta.o`. The repair is:

```make
build/beta.o: src/beta.c config.h
```

After changing the header, both objects should rebuild. `make clean` deletes both objects,
so both rebuild even with the edge missing. That proves only that a clean build works; it
does not prove that the incremental graph is truthful.

## Exercise 10: Design and defend a small graph

One valid graph is:

```make
.PHONY: all
all: summary.txt chart.svg

cleaned.csv: raw.csv
	cp $< $@

summary.txt: cleaned.csv
	printf 'summary from %s\n' "$<" > $@

chart.svg: cleaned.csv
	printf '<svg><!-- data from %s --></svg>\n' "$<" > $@
```

Expected rebuilds:

| Change | Rebuilds |
| --- | --- |
| edit `raw.csv` | `cleaned.csv`, `summary.txt`, and `chart.svg` |
| delete `summary.txt` | only `summary.txt` |
| delete `chart.svg` | only `chart.svg` |
| run twice without changes | no recipes on the second run |

`cleaned.csv` has one writer. Each report output also has one writer. The fan-out is
honest because both final outputs name `cleaned.csv` as the input that determines their
contents.

## What a mastery-level answer set looks like

A mastery-level submission does not just contain the right snippets. It shows that you can
move between three levels comfortably:

- graph language: target, prerequisite, ownership, convergence
- command evidence: `--trace`, `-q`, failure drills
- plain-language explanation of why the build is or is not telling the truth
