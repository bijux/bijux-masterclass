# Discovery, Namespacing, and Repository Growth


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Build Architecture Layered Includes Apis"]
  page["Discovery, Namespacing, and Repository Growth"]
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

A flat output directory can appear correct until a second subsystem introduces a familiar
basename such as `util`, `config`, or `summary`. At that point, successful execution is a
weak signal: Make may have built one file while the mapping silently discarded another
owner.

This lesson uses two source roots that deliberately collide:

```text
src/
  cli/util.txt    owner=cli
  lib/util.txt    owner=lib
```

The central architecture invariant is:

> Every selected source that promises its own artifact must map to one distinct,
> owner-identifiable output path.

## Run the collision audit

From `programs/reproducible-research/deep-dive-make/capstone/`, run:

```sh
gmake architecture-contract-audit
```

Open these two rows in the generated `summary.tsv`:

```text
output-ownership	flat-output	...	FLAT_OUTPUT_OWNERSHIP_COLLAPSED	PASS
output-ownership	namespaced-output	...	SUBSYSTEM_OUTPUT_OWNERSHIP_PRESERVED	PASS
```

The first row passes because the audit successfully reproduced a defect. Read the finding,
not just the result column.

## Broken model: erase ownership before building

The flat specimen starts with two sources:

```make
SOURCES := src/cli/util.txt src/lib/util.txt
```

It then discards their parent paths:

```make
OUTPUTS := $(sort $(addprefix build/,$(notdir $(SOURCES))))
```

Evaluate that expression from the inside:

1. `$(notdir ...)` turns both sources into `util.txt util.txt`.
2. `$(addprefix ...)` turns both into `build/util.txt build/util.txt`.
3. `$(sort ...)` removes the duplicate.

Two selected sources have become one target before any recipe runs.

```mermaid
flowchart LR
  cli["src/cli/util.txt<br/>owner=cli"]
  lib["src/lib/util.txt<br/>owner=lib"]
  strip["notdir"]
  output["build/util.txt<br/>one path"]

  cli --> strip
  lib --> strip
  strip --> output
```

The rule makes the loss visible:

```make
build/util.txt: $(SOURCES) | build/
	{ printf 'selected=%s\n' '$<'; cat '$<'; } > $@
```

`$<` is the first prerequisite, so the output records the CLI source. The library source
is listed as a prerequisite, but it never receives an artifact of its own. Make exits zero
because the graph asked for exactly one target and that target was created.

Inspect the evaluated mapping and surviving file:

```sh
cat artifacts/audit/reproducible-research/deep-dive-make/architecture-contracts/traces/output-ownership-flat-output-map.log
cat artifacts/audit/reproducible-research/deep-dive-make/architecture-contracts/workspace/output-ownership/flat-output/build/util.txt
```

The evidence should establish all three facts:

- source count is two
- unique output count is one
- the surviving artifact says `owner=cli`

That is stronger than saying “flat paths might collide.”

## Control model: preserve the source namespace

The control changes one mapping:

```make
OUTPUTS := $(patsubst src/%,build/%,$(SOURCES))
```

The relative path below `src/` survives below `build/`:

| Source | Output |
| --- | --- |
| `src/cli/util.txt` | `build/cli/util.txt` |
| `src/lib/util.txt` | `build/lib/util.txt` |

Separate pattern rules keep each prerequisite binding explicit:

```make
build/cli/%.txt: src/cli/%.txt | build/cli/
	{ printf 'selected=%s\n' '$<'; cat '$<'; } > $@

build/lib/%.txt: src/lib/%.txt | build/lib/
	{ printf 'selected=%s\n' '$<'; cat '$<'; } > $@
```

```mermaid
flowchart LR
  cli["src/cli/util.txt"] --> cli_out["build/cli/util.txt<br/>owner=cli"]
  lib["src/lib/util.txt"] --> lib_out["build/lib/util.txt<br/>owner=lib"]
```

Now source count and unique output count are both two, and each file records the expected
owner. The output path itself also communicates which subsystem owns the artifact.

## Check cardinality before recipe correctness

When each source is supposed to produce one output, review the mapping as a function:

```text
source path -> output path
```

For the selected domain, ask:

1. **Totality:** does every source map to an output?
2. **Uniqueness:** do different sources map to different outputs?
3. **Ownership:** can a reviewer recover the source owner from the output path?
4. **Stability:** does adding an unrelated source leave existing mappings unchanged?

A recipe can be perfectly written and still operate on a graph that failed the second
question.

For a small list, Make can expose a useful diagnostic surface:

```make
show-map:
	@printf 'sources=%s\n' '$(SOURCES)'
	@printf 'outputs=%s\n' '$(OUTPUTS)'
```

For a larger repository, publish a machine-readable source-to-output manifest and reject
duplicate output keys before recipes execute.

## Reject collisions before sorting can hide them

Keep the mapped list and unique list separate:

```make
MAPPED_OUTPUTS := $(patsubst src/%,build/%,$(SOURCES))
UNIQUE_OUTPUTS := $(sort $(MAPPED_OUTPUTS))

ifneq ($(words $(MAPPED_OUTPUTS)),$(words $(UNIQUE_OUTPUTS)))
$(error source-to-output mapping is not injective: $(MAPPED_OUTPUTS))
endif

OUTPUTS := $(UNIQUE_OUTPUTS)
```

The check compares the number of selected mapping results with the number of unique output
keys. Assigning `OUTPUTS := $(sort ...)` first destroys the duplicate evidence and makes
the later count look healthy.

For diagnosis, print the logical pairs rather than only the two lists:

```make
show-owner-map:
	@$(foreach source,$(SOURCES),\
	  printf '%s\t%s\n' \
	    '$(source)' '$(patsubst src/%,build/%,$(source))';)
```

Store this as a TSV artifact in a serious audit. A reviewer should be able to reverse an
output path to the selected source owner without reading the recipe body.

## Prove totality separately

An injective mapping can still ignore sources outside the supported roots:

```make
SELECTED_SOURCES := $(sort $(wildcard src/*/*.c))
OWNED_SOURCES := $(CLI_SOURCES) $(LIB_SOURCES)
UNOWNED_SOURCES := $(filter-out src/cli/% src/lib/%,$(SELECTED_SOURCES))

ifneq ($(strip $(UNOWNED_SOURCES)),)
$(error selected sources lack an ownership root: $(UNOWNED_SOURCES))
endif
```

Totality asks whether every selected source belongs to a declared mapping domain.
Injectivity asks whether two selected sources receive distinct keys. Both are required
for a one-source/one-output contract.

```mermaid
flowchart LR
  selected["selected source"] --> owned{"declared owner root?"}
  owned -- no --> reject_owner["reject unowned source"]
  owned -- yes --> key["derive logical owner key"]
  key --> unique{"key unique?"}
  unique -- no --> reject_collision["reject collision"]
  unique -- yes --> output["publish owner-identifiable output"]
  output --> reverse["manifest reverses output to source"]
```

## Root discovery in declared ownership domains

Namespacing answers where outputs belong. Rooted discovery answers which inputs belong to
the build:

```make
CLI_SOURCES := $(sort $(wildcard src/cli/*.c))
LIB_SOURCES := $(sort $(wildcard src/lib/*.c))
SOURCES := $(CLI_SOURCES) $(LIB_SOURCES)
```

The explicit roots make the ownership domains reviewable. `$(sort ...)` stabilizes the
order used by manifests, link commands, and publication lists.

Do not confuse sorting with collision prevention. Sorting made the broken specimen’s
duplicate disappear predictably; it did not make the mapping injective. Deterministic loss
is still loss.

## Use logical owner keys when roots are deeper

Repositories often grow from:

```text
src/cli/util.c
src/lib/util.c
```

to:

```text
components/cli/src/util.c
components/lib/src/util.c
```

Stripping each root to `util.c` recreates the collision. Define a stable logical key:

| Physical source | Logical key | Output |
| --- | --- | --- |
| `components/cli/src/util.c` | `cli/util.c` | `build/cli/util.o` |
| `components/lib/src/util.c` | `lib/util.c` | `build/lib/util.o` |

The key is owned by the repository contract, not by how many parent directories happen to
exist today. Record it in the mapping manifest so a source move within one component does
not silently transfer output ownership.

## Decide how symlinks and generated sources participate

Path identity and file identity are different:

- two logical source paths may resolve to the same physical file through symlinks
- one generated source may not exist when Make first parses discovery expressions
- an unbounded recursive scan may cross vendored, generated, or mounted directories

Write a policy:

| Case | Decision to make |
| --- | --- |
| symlinked source root | reject, preserve logical alias, or canonicalize with an explicit owner |
| generated source | declare generator output and include it from graph data, not incidental parse-time scan |
| vendored tree | include through a bounded vendor owner or exclude explicitly |
| source move | preserve logical owner key or treat as an intentional artifact identity change |

`$(realpath ...)` can help compare existing physical paths, but it returns nothing for
missing paths and can erase intentional logical ownership. Canonicalization is not a
substitute for an ownership decision.

## Test extension stability

Before accepting a new root, capture the established mapping manifest. Add:

1. one source with a unique basename
2. one source with a colliding basename
3. one unsupported-root source
4. one generated source whose producer has not run

Require:

- established source/output pairs remain unchanged
- both supported additions receive distinct owner-identifiable outputs
- the unsupported source is rejected with its path
- the generated source appears only through its declared generator contract

This checks stability and rejection, not only the happy path.

## Decide whether one DAG still expresses the truth

Colliding basenames do not automatically justify recursive builds such as:

```sh
gmake -C cli
gmake -C lib
```

First ask whether the subsystems share a real dependency graph, tool policy, or final
artifact. If they do, preserving ownership within one DAG keeps cross-subsystem
dependencies visible.

Use separate invocations when the boundary is operationally real and their contracts are
explicit. Do not use them merely to hide a path-model failure that
`build/cli/...` and `build/lib/...` would solve.

## Growth review table

| Review surface | Evidence | Failure signal |
| --- | --- | --- |
| discovery roots | sorted source list or manifest | files join through an unbounded search |
| mapping cardinality | source and unique-output counts | fewer outputs than promised sources |
| path ownership | output-to-subsystem mapping | owner cannot be inferred |
| extension behavior | add one colliding basename | an existing output changes owner |
| total mapping | add unsupported-root source | source is silently omitted |
| physical identity | add symlink alias | duplicate physical input has no declared policy |
| generated membership | start from clean parse | generated source appears only after a warm run |
| graph coherence | dry run or graph view | cross-subsystem dependency is hidden in recursion |

Use this table before a repository adds its next subsystem, not after an artifact has been
silently overwritten.

## Practice: add a third owner

Work in a disposable copy of the namespaced specimen.

1. Add `src/plugin/util.txt` containing `owner=plugin`.
2. Predict the flat model’s source count, output count, and surviving owner.
3. Extend the namespaced model so it publishes `build/plugin/util.txt`.
4. Run `show-map` and `all`.
5. Prove that all three outputs exist and each records its matching owner.
6. Explain why sorting the flat `OUTPUTS` list cannot satisfy the uniqueness invariant.
7. Add one unsupported-root source and require the map check to reject it by name.
8. Preserve the mapping manifest, add the plugin root, and prove established pairs remain
   byte-for-byte identical.

A complete result contains the mapping, the three artifact paths, and their contents. A
directory sketch without executable evidence is not complete.

## End-of-page checkpoint

You are ready to continue when you can explain:

- exactly where the flat model turns two source paths into one output
- why exit status zero does not establish one-output-per-source behavior
- how `patsubst src/%,build/%` preserves subsystem ownership
- why rooted, sorted discovery and collision-free mapping solve different problems
- which evidence supports `SUBSYSTEM_OUTPUT_OWNERSHIP_PRESERVED`
- how totality, injectivity, reverse ownership, and extension stability differ
- why symlink and generated-source handling require explicit ownership policy
