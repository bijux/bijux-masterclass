# Package Layouts and Publication Boundaries

Once a release target has a clear name, the next question is obvious:

> what exactly belongs in the published artifact?

This is where teams often start improvising:

- copy the binary
- maybe add docs
- maybe add a license
- maybe add generated metadata
- maybe leave diagnostics in because they seem useful

That approach works until someone asks which of those files are actually part of the
artifact contract.

This page is about answering that question deliberately.

## The sentence to keep

When you design a bundle, ask:

> which files define the published artifact, and where is the moment that this assembled
> tree becomes trustworthy to another system?

That is the core of release modeling.

## Package layout is part of the contract

A release bundle is not just "whatever was convenient to archive." It is a public shape.

If another system, user, or environment is expected to consume:

- `bin/app`
- `LICENSE`
- `share/doc/README.md`
- `manifest.txt`

then that layout is part of the artifact contract.

This means the layout should be:

- intentional
- stable
- explainable

Not merely the side effect of a shell script that copies files in some order.

## Ask what belongs inside the bundle

The strongest package decisions start with a simple separation:

| Category | Typical examples | Should it be inside the published bundle? |
| --- | --- | --- |
| core artifact content | binaries, libraries, required configs, license | usually yes |
| consumer-facing metadata | checksums, manifest of bundle contents | often yes, depending on policy |
| operator diagnostics | host details, timing logs, local paths | usually no |
| build-only intermediates | object files, temp manifests, scratch outputs | no |

The point is not to memorize a table. The point is to stop treating every nearby file as
equally bundle-worthy.

## Bundles need a staging boundary

One of the healthiest habits in release engineering is staging the bundle in a temporary
tree before publishing the final artifact.

For example:

```make
dist/app.tar.gz: app LICENSE docs/README.md dist/manifest.txt | dist/
	@rm -rf dist/tmp
	@mkdir -p dist/tmp/bin dist/tmp/share/doc
	@cp app dist/tmp/bin/app
	@cp LICENSE dist/tmp/LICENSE
	@cp docs/README.md dist/tmp/share/doc/README.md
	@cp dist/manifest.txt dist/tmp/manifest.txt
	@tar -czf $@ -C dist/tmp .
```

This is healthier than archiving files from several unrelated locations directly because:

- the bundle shape becomes visible in one place
- the tree can be inspected before publication
- the archive is produced from one staged boundary

That is easier to reason about and easier to test.

## Publication boundary matters here too

Earlier modules taught publication discipline for generated artifacts. The same logic
applies to release bundles.

The question is:

when may another system trust the release artifact?

Usually the answer is not:

- while files are still being copied
- while the staging tree is still incomplete
- while the manifest is still being rewritten

Usually the answer is:

- after the staging tree is complete
- after the bundle archive is assembled
- after the declared manifest or checksum matches the published tree

That is the publication boundary.

## A package layout should be easy to explain

A strong bundle explanation sounds like this:

> The release archive contains the binary under `bin/`, the license at the root, one README
> under `share/doc/`, and a bundle manifest. Build logs and host attestations are produced
> beside the bundle, not inside it.

That is a good explanation because a consumer can act on it.

A weak explanation sounds like:

> `dist` copies what we usually need.

That is not a contract.

## Derived metadata still needs a policy

Package layout questions are not only about "real files versus fake files." Derived
metadata often matters:

- checksums
- bundle manifests
- version files
- compatibility notes

The architectural question is:

- is this metadata part of the published bundle
- or is it adjacent release evidence

That distinction becomes more explicit in the next core, but you should already start
asking it here whenever you place metadata into a staged release tree.

## A small package-tree example

Suppose the release contract is:

```text
bundle/
  bin/app
  LICENSE
  share/doc/README.md
  manifest.txt
```

Then the Makefile should model that tree on purpose:

```make
DIST_ROOT := dist/tmp

dist/manifest.txt: app LICENSE docs/README.md | dist/
	@printf '%s\n' 'bin/app' 'LICENSE' 'share/doc/README.md' > $@

dist/app.tar.gz: app LICENSE docs/README.md dist/manifest.txt | dist/
	@rm -rf $(DIST_ROOT)
	@mkdir -p $(DIST_ROOT)/bin $(DIST_ROOT)/share/doc
	@cp app $(DIST_ROOT)/bin/app
	@cp LICENSE $(DIST_ROOT)/LICENSE
	@cp docs/README.md $(DIST_ROOT)/share/doc/README.md
	@cp dist/manifest.txt $(DIST_ROOT)/manifest.txt
	@tar -czf $@ -C $(DIST_ROOT) .
```

The important part is that the layout is no longer implicit.

## What should stay outside the bundle

Teams often overstuff bundles with files that are only useful during local debugging:

- host information
- local tool versions
- benchmark logs
- full build traces

Those files may be valuable. That does not automatically make them part of artifact
identity or bundle content.

A healthier pattern is often:

- keep the bundle clean and stable
- publish diagnostics beside it when needed

This keeps release shape understandable.

## Failure signatures worth recognizing

### "The bundle contains files nobody can justify"

That usually means package layout is being assembled by convenience instead of contract.

### "We changed one script and now the archive layout drifted"

That often means the release tree was never modeled explicitly enough.

### "Consumers use files from inside the bundle that are not documented anywhere"

That means the bundle contract is under-specified.

### "We cannot tell whether the staged tree or the final archive is the trusted boundary"

That means publication is not modeled clearly enough.

## A review question that improves package design

Take one release bundle and ask:

1. which files are inside it
2. why each one belongs there
3. which files are kept outside and why
4. where the bundle is staged before publication
5. what exact step makes the finished artifact trustworthy

If those answers are weak, the release boundary is weak too.

## What to practice from this page

Choose one release archive in a repository and write down:

1. the intended directory tree
2. the required files
3. one file currently inside the bundle that should move outside
4. one boundary file or manifest that belongs inside
5. the publication step after which the archive becomes trustworthy

If you can do that cleanly, you are treating bundle layout as a contract instead of a copy
script.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why package layout is part of artifact contract design
- why staging trees improve release clarity
- how to distinguish bundle content from adjacent diagnostics
- why publication boundary matters for archives too
- how to tell whether a bundle contains unjustified files
