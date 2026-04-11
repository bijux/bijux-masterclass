# Checksums, Manifests, and Artifact Evidence

Release engineering becomes confusing very quickly when teams mix two different truths:

- what the artifact is
- what evidence we want to keep about it

At first this sounds abstract. In practice it causes very ordinary problems:

- bundles that rebuild every run because timestamps were embedded inside them
- release manifests that mean three different things at once
- host diagnostics getting mistaken for artifact identity
- checksums that no longer match because the bundle includes unstable proof files

This page is about keeping those truths separate enough that both remain useful.

## The sentence to keep

When you add release metadata, ask:

> is this file part of the artifact's identity, or is it supporting evidence about the
> artifact?

That question prevents a lot of unstable release design.

## Identity and evidence are not the same thing

Artifact identity usually means:

- the bundle contents
- the files consumers are meant to receive
- the checksums or manifests that define or verify that bundle according to policy

Supporting evidence usually means:

- toolchain attestation
- host details
- timing reports
- local diagnostic traces
- auxiliary proof artifacts used in validation

Some repositories choose to package more evidence inside the published bundle. That can be
valid. The point is that the choice must be explicit.

Without that explicit choice, release artifacts often become unstable by accident.

## Checksums usually describe identity

Checksums are most useful when they answer:

> which exact bytes make up the published artifact?

That is why checksum files often belong with the released artifact or immediately beside it.

For example:

```make
dist/app.tar.gz.sha256: dist/app.tar.gz
	@sha256sum $< > $@
```

This is a clean relationship:

- the archive is the identity
- the checksum is a verification description of that identity

The trouble starts when the checksum target itself depends on unstable files that should not
have been part of the release identity at all.

## Manifests need a narrower job than "metadata"

"Manifest" is one of those words that can mean almost anything unless you narrow it.

A strong manifest has one clear role, such as:

- listing bundle contents
- recording release version and declared package members
- describing checksums for each payload

A weak manifest is a dumping ground for:

- file list
- build time
- host name
- tool versions
- local user name
- maybe anything else that was easy to print

That kind of manifest quickly stops being trustworthy because nobody can tell which facts
are actually part of the contract.

## A small bundle-manifest example

Suppose the release policy says the bundle should contain:

- `bin/app`
- `LICENSE`
- `share/doc/README.md`

Then a good manifest might say exactly that:

```make
dist/manifest.txt: app LICENSE docs/README.md | dist/
	@printf '%s\n' \
	  'bin/app' \
	  'LICENSE' \
	  'share/doc/README.md' > $@
```

This is useful because it records bundle identity in a stable, inspectable way.

It does not try to become a whole-machine diary.

## Attestation is often better beside the artifact than inside it

Teams often want extra proof about a release:

- compiler version
- platform details
- selected build mode
- validation report

Those may be valuable, but they do not automatically belong inside the artifact's identity.

A healthier pattern is often:

- publish the artifact
- publish checksums and a bundle manifest
- publish attestations beside the artifact or in a verification directory

That way the release remains stable while the proof surface still exists.

## Why timestamps are so dangerous here

Timestamps are one of the fastest ways to confuse identity and evidence.

If you put:

```text
build_time=...
```

inside a manifest that is packaged into the release bundle, then every build creates a new
artifact identity even when nothing semantically changed.

That may be the intended policy. Usually it is not.

This is why Module 08 keeps asking:

- what is identity
- what is evidence
- where should each live

The answers determine whether release artifacts remain stable.

## A sidecar-attestation example

Suppose you want to record compiler and host information for a release:

```make
dist/app.attest.txt: dist/app.tar.gz | dist/
	@printf 'compiler=%s\nhost=%s\n' '$(CC)' "$$(uname -s)" > $@
```

This can be healthy if the attestation file is treated as adjacent evidence rather than as
part of the archive's core identity.

The archive checksum can still describe the artifact itself.

The attestation file can still help operators understand how that artifact was produced.

Those are different jobs, and keeping them separate is usually cleaner.

## Evidence still needs stability where possible

Even when evidence lives beside the artifact, it should still be as stable and meaningful as
possible.

Good evidence files usually:

- record facts people actually use
- avoid redundant noise
- change only when the represented evidence changes

Poor evidence files:

- dump everything available
- include unstable local trivia
- force teams to ignore the file because it changes on every run without teaching anything

This is the same lesson you learned earlier with manifests and stamps. Release proof should
be useful, not merely abundant.

## Failure signatures worth recognizing

### "The release bundle changes every run even when nothing important changed"

That often means evidence was packaged as identity without a clear policy.

### "We have a manifest, but nobody can say what it is for"

That usually means the manifest job is too broad.

### "Checksums do not match because the bundle includes unstable metadata"

That means identity and proof have been mixed carelessly.

### "We lost useful provenance because we were afraid to include anything"

That may mean the repository needs adjacent attestation rather than less evidence overall.

## A review question that improves release evidence design

Take one manifest, checksum set, or attestation file and ask:

1. what exact question this file answers
2. whether that question is about artifact identity or supporting evidence
3. whether the file belongs inside the published bundle or beside it
4. whether its contents are stable enough for that role
5. whether another engineer could verify the policy from the file alone

If those answers are weak, the release evidence model is weak too.

## What to practice from this page

Choose one release artifact and list:

1. the files that define its identity
2. the checksum or manifest files that verify that identity
3. one attestation that should live beside the artifact
4. one unstable diagnostic that should stay out entirely
5. one sentence explaining why the split makes the release easier to trust

If you can do that cleanly, you are treating release evidence as design rather than
afterthought.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why artifact identity and supporting evidence are different
- why checksums usually describe identity rather than ambient machine state
- how manifests become weak when they try to mean everything
- why sidecar attestations are often healthier than stuffing diagnostics into the bundle
- how unstable metadata can accidentally redefine a release artifact
