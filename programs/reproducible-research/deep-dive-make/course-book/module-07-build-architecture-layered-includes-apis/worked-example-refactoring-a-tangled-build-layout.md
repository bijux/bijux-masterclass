# Worked Example: Refactoring a Tangled Build Layout


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Build Architecture Layered Includes Apis"]
  page["Worked Example: Refactoring a Tangled Build Layout"]
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

This worked example begins with a build that exits zero in every scenario. Its architecture
is still dishonest in three ways:

- automation depends on a target the help interface does not promise
- a release include changes an ordinary artifact
- two subsystem sources collapse into one output

The goal is not to make the files look modular. The goal is to replace each hidden
dependency with a contract another maintainer can verify.

## Establish the baseline before editing

From `programs/reproducible-research/deep-dive-make/capstone/`, run:

```sh
gmake architecture-contract-audit
```

Copy these six rows from `summary.tsv` into the review note:

| Boundary | Inherited behavior | Control behavior |
| --- | --- | --- |
| caller to build API | `PRIVATE_TARGET_DEPENDENCE_REPRODUCED` | `PUBLIC_TARGET_CONTRACT_HONORED` |
| release to shared policy | `CROSS_LAYER_POLICY_LEAK_REPRODUCED` | `TARGET_SCOPED_POLICY_PRESERVED` |
| source to output | `FLAT_OUTPUT_OWNERSHIP_COLLAPSED` | `SUBSYSTEM_OUTPUT_OWNERSHIP_PRESERVED` |

Do not start by renaming files. First preserve the observations that the refactor must
change:

```text
private caller: application.txt exists; verification.txt absent
global mutation: default.txt and release.txt both contain -DRELEASE
flat output: two sources; one output; owner=cli survives
```

These are the baseline assertions. They prevent a structural rewrite from hiding a
behavioral regression.

## Repair the caller boundary

The inherited Makefile contains both targets:

```make
.PHONY: internal-build verify

internal-build: build/application.txt

verify: internal-build
	@printf 'verified\n' > build/verification.txt
```

Its help output promises only:

```text
help    show the supported build interface
verify  build and verify the application
```

The automation script nevertheless runs:

```sh
gmake internal-build
```

That command is reachable and successful. It is not a supported interface, and it bypasses
the evidence created by `verify`.

Change the caller, not the visibility of every helper:

```sh
gmake verify
```

Then rerun the caller and require both files:

```text
build/application.txt
build/verification.txt
```

Why not add `internal-build` to help? Because that would convert an implementation detail
into a promise merely to avoid repairing one caller. Public API growth is a compatibility
decision, not a documentation shortcut.

```mermaid
flowchart LR
  automation["automation"]
  verify["verify<br/>declared promise"]
  internal["internal-build<br/>implementation"]
  app["application.txt"]
  proof["verification.txt"]

  automation --> verify
  verify --> internal --> app
  verify --> proof
```

The acceptance evidence is:

- help declares `verify`
- the external caller invokes `verify`
- both promised artifacts exist
- the finding is `PUBLIC_TARGET_CONTRACT_HONORED`

## Repair the policy boundary

The inherited include order is readable:

```make
include mk/policy.mk
include mk/release.mk
include mk/artifacts.mk
```

The ownership is not. `policy.mk` establishes:

```make
CFLAGS := -O2
```

Then `release.mk` performs a global mutation:

```make
CFLAGS += -DRELEASE
```

Because includes are parsed before Make updates a goal, merely loading the release layer
changes the value seen by `all`.

Keep the file split and narrow the assignment:

```make
release: CFLAGS += -DRELEASE
```

Now run `all` and `release` independently. Accept the repair only if the artifacts say:

```text
build/default.txt: flags=-O2
build/release.txt: flags=-O2 -DRELEASE
```

Renaming `release.mk` or moving the global append to another include would not satisfy this
test. The repair is about the value’s propagation domain.

## Repair the output boundary

The repository now has two legitimate owners for the basename `util.txt`:

```text
src/cli/util.txt
src/lib/util.txt
```

The inherited mapping strips both ownership directories:

```make
OUTPUTS := $(sort $(addprefix build/,$(notdir $(SOURCES))))
```

Evaluate the graph before inspecting the recipe:

```text
2 source paths -> 2 duplicate output strings -> 1 unique target
```

Replace the lossy transformation with:

```make
OUTPUTS := $(patsubst src/%,build/%,$(SOURCES))
```

Then use pattern rules whose prerequisite roots match the output namespaces:

```make
build/cli/%.txt: src/cli/%.txt | build/cli/
	{ printf 'selected=%s\n' '$<'; cat '$<'; } > $@

build/lib/%.txt: src/lib/%.txt | build/lib/
	{ printf 'selected=%s\n' '$<'; cat '$<'; } > $@
```

Accept the repair only when the map has equal source and unique-output counts and both
artifacts preserve their owners:

```text
build/cli/util.txt: owner=cli
build/lib/util.txt: owner=lib
```

This test catches an error that “the build succeeded” cannot catch.

## Keep abstraction inside the proved boundary

After the three repairs, repeated rules may invite a macro. Extract only the invariant the
evidence already established:

```make
define publish_owned_source
build/$1/%.txt: src/$1/%.txt | build/$1/
	{ printf 'selected=%s\n' '$$<'; cat '$$<'; } > $$@
endef

$(eval $(call publish_owned_source,cli))
$(eval $(call publish_owned_source,lib))
```

The macro has one responsibility: preserve the same owner on both sides of the mapping.
Its call sites still expose the owner set. It does not choose public targets, mutate
policy, or generate unrelated release rules.

Rerun the output checks after extraction. Reduced line count is not proof that the macro
preserved the contract.

## Review the combined architecture

The repaired ownership flow is:

```mermaid
flowchart TD
  caller["external caller"] --> api["declared target"]
  api --> graph["artifact graph"]
  base["shared policy"] --> graph
  release["release target scope"] --> release_graph["release branch"]
  sources["rooted source owners"] --> mapping["namespace-preserving mapping"]
  mapping --> graph
  graph --> evidence["owned artifacts and verification"]
```

Record each boundary in one table:

| Contract | Owner | Consumer | Evidence |
| --- | --- | --- | --- |
| supported build action | top-level help and target | automation | help trace and caller trace |
| base flags | `policy.mk` | ordinary and release graph | `default.txt` |
| release specialization | `release` target | release prerequisites | `release.txt` |
| source-to-output mapping | discovery/mapping layer | artifact rules | map trace and owned files |

If the “Owner” cell says “several includes,” the refactor is not yet reviewable.

## Run the acceptance sequence

Use this order so a later check cannot conceal an earlier contract failure:

1. Run `gmake help` and identify the supported automation target.
2. Run the external caller and require both application and verification evidence.
3. Build ordinary and release artifacts separately and compare their flags.
4. Print the source-to-output map and compare its cardinality.
5. Read both namespaced artifacts and compare their recorded owners.
6. Clean, rerun the same checks, and confirm the observations do not depend on stale state.

For the course specimens, the automated equivalent is:

```sh
gmake architecture-contract-selftest
```

The self-test also mutates disposable copies of the models and confirms that dishonest
evidence is rejected. That matters because an audit that always reports success is only a
demonstration script.

## Write the review conclusion

A defensible conclusion names changed evidence:

> Automation now calls the declared `verify` target and receives both application and
> verification artifacts. Release flags reach only the release target branch. Two sources
> with the same basename map to two owner-identifiable outputs. The audit reports the three
> preserved control findings, and its rejection tests fail when any control is made
> dishonest.

Avoid “the Makefiles are cleaner.” It does not identify a contract, an observation, or a
remaining risk.

## Your turn: refactor without losing the baseline

Use a disposable copy of the three broken specimens.

1. Record the inherited finding and artifact evidence for each defect.
2. Apply the caller repair and rerun only the public-API cases.
3. Apply the target-scoped policy repair and compare the two flag artifacts.
4. Apply the namespace-preserving mapping and add a third colliding owner.
5. Rerun the complete audit and its rejection tests.
6. Write a review table naming each owner, consumer, and evidence path.

The work is complete only when all three repaired contracts are independently observable.
A new directory layout without those observations is still a proposal.
