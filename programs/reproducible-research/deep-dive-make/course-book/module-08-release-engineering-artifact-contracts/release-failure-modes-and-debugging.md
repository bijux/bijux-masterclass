# Release Failure Modes and Debugging

By the time a release goes wrong, the symptoms often sound frustratingly vague:

- "the archive looks wrong"
- "install worked on one machine but not another"
- "the checksum changed for no good reason"
- "the manifest says one thing, the bundle shows another"
- "rerunning `dist` fixed it, somehow"

Those are not helpful explanations. They are the beginning of an investigation.

This page is about turning that investigation into a repeatable release-debugging loop.

## The sentence to keep

When a release breaks, ask:

> did the failure come from build truth, package truth, or publish truth?

That is the question that keeps release debugging from dissolving into shell folklore.

## Three truth boundaries matter here

Release engineering sits on top of earlier modules, so it inherits earlier truths and adds
new ones.

The three boundaries to keep separate are:

1. build truth
2. package truth
3. publish truth

### Build truth

Did the build produce the right outputs in the first place?

Examples:

- the binary is stale
- generated release metadata was wrong before packaging started
- tests never validated the thing that got packaged

### Package truth

Did the release bundle select and arrange the correct files?

Examples:

- the wrong files were copied into `dist/`
- a required file is missing
- the manifest does not match the bundle tree

### Publish truth

Was the bundle or install destination published safely and consistently?

Examples:

- the archive was produced from a half-staged tree
- install mutated the destination in an unsafe order
- checksums or attestations describe something different from what was actually published

These categories are not academic. They tell you where to look first.

## Failure mode 1: wrong bundle contents

Symptom:

- the archive exists
- but a required file is missing or an unexpected file appears inside it

Likely failure class:

- package truth

First questions:

- what files were declared as release inputs
- what did the staging tree actually contain
- did the bundle layout drift from the intended contract

Repair:

- model the package layout explicitly
- stage from declared inputs only
- verify the bundle tree against the manifest or expected layout

## Failure mode 2: checksum or manifest mismatch

Symptom:

- the manifest does not describe the published tree correctly
- or checksums do not match the artifact as published

Likely failure class:

- package truth or publish truth, depending on where the mismatch began

First questions:

- was the manifest generated from the same staged tree that became the artifact
- were checksums computed before or after the final publication boundary
- is unstable metadata being treated as artifact identity

Repair:

- generate verification data from the final intended artifact boundary
- separate unstable evidence from identity
- ensure the manifest job is narrow and stable

## Failure mode 3: unstable release identity

Symptom:

- repeated `make dist` runs change the release artifact even when semantic inputs did not

Likely failure class:

- publish truth or evidence-policy failure

First questions:

- what unstable metadata is entering the bundle
- which files define artifact identity
- which proof files should live beside the artifact instead

Repair:

- move host diagnostics or timestamps out of the core artifact
- keep checksums and manifests scoped to stable identity
- rerun convergence checks on `dist`

## Failure mode 4: unsafe install behavior

Symptom:

- the install tree changes unpredictably on rerun
- partial failures leave mixed old and new state

Likely failure class:

- publish truth

First questions:

- what destination tree does `install` promise
- was the destination staged or mutated in-place
- what is the intended overwrite or idempotence policy

Repair:

- make the destination boundary explicit
- stage or preview when possible
- define and test the rerun behavior

## Failure mode 5: release target meaning drift

Symptom:

- `dist` means one thing to humans and another thing to CI
- or a release target silently accreted validation, install, or deploy behavior

Likely failure class:

- contract drift at the target interface

First questions:

- what does the target name currently promise
- which scripts or systems call it
- what should be split into a different target instead

Repair:

- narrow the target meaning
- make compositions visible through target dependencies
- keep the public release surface small and stable

## The release-debugging loop

When something goes wrong, use this sequence:

1. reproduce the failure with the smallest release route that still shows it
2. identify which truth boundary most likely failed
3. inspect the declared inputs, staging tree, or destination tree that belong to that boundary
4. repair the boundary model
5. rerun convergence and release verification commands

This loop matters because release debugging often tempts teams into rerunning `dist` until
the symptom disappears without ever explaining why.

## Useful evidence commands

Some simple commands keep release debugging grounded:

```sh
make --trace dist
make dist
make -q dist; echo $?
tar -tzf dist/app.tar.gz
make install DESTDIR=/tmp/release-check
find /tmp/release-check -type f | sort
```

Each one answers a different question:

- why did packaging run
- did the release converge
- what is actually inside the archive
- what did install actually publish

That is much stronger than saying "the release step seemed weird."

## A small incident walkthrough

Suppose you see:

```sh
make dist
tar -tzf dist/app.tar.gz
```

and the archive unexpectedly contains:

```text
build.log
host-info.txt
tmp/partial-report.json
```

The right first thought is not "tar is messy." The right thought is:

- bundle content drifted from the intended package contract
- this is a package-truth failure
- the staging or inclusion model is too broad

That classification already narrows the repair a lot.

## Why rerunning is not a diagnosis

Release bugs often feel intermittent because rebuilding or cleaning changes side effects.

That makes it tempting to say:

- rerun `dist`
- delete `dist/`
- try again

Those actions can be useful operationally. They are not explanations.

The explanation has to say which boundary lied:

- build output was wrong
- bundle assembly was wrong
- publication into the archive or destination was wrong

That is the level of clarity Module 08 is aiming for.

## Failure signatures worth recognizing quickly

### "`make dist` passes, but the archive contents are wrong"

That is usually package truth, not build truth.

### "Checksums differ but the source and binary are unchanged"

That often means unstable evidence leaked into artifact identity.

### "Install worked once and failed on rerun"

That usually points to publish-truth problems in the destination contract.

### "The manifest says one thing, but the archive says another"

That means the release verification surface is not tied tightly enough to the final bundle.

## A review question that improves release debugging

Take one release failure and ask:

1. which truth boundary failed first
2. what file tree or artifact belongs to that boundary
3. what command would expose the mismatch
4. what contract or publication repair would make the boundary more honest
5. which rerun or verification command would prove the fix

If those answers are weak, the release investigation is still too vague.

## What to practice from this page

Pick one release failure mode and write a short incident note:

1. the symptom
2. the likely failed truth boundary
3. the first evidence command
4. the likely repair
5. the verification command after the repair

If you can do that cleanly, you are debugging release contracts instead of merely reacting
to them.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- the difference between build truth, package truth, and publish truth
- why wrong bundle contents are usually a package-truth problem
- why unstable release identity often comes from mixing evidence with artifact meaning
- why install failures belong to the same publication discipline as archive releases
- why rerunning `dist` is not the same thing as diagnosing a release defect
