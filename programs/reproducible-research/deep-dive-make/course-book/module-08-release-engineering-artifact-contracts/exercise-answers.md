# Exercise Answers

Use this after you have written your own answers. The point is comparison, not copying.

Strong Module 08 answers do not just name files or commands. They explain:

- what release promise is being made
- what evidence would prove that promise
- why the chosen boundary makes publication safer and easier to trust

## Exercise 1: Write a clear `dist` contract

A strong answer explains `dist` in one narrow sentence, such as:

> `dist` produces the publishable release archive and its declared verification files under
> `dist/`.

The strongest answers also say what `dist` does not promise. For example:

- it does not install onto the local machine
- it does not deploy
- it does not silently run unrelated cleanup

That negative clarity matters because narrow targets are easier to trust.

## Exercise 2: Design a publishable bundle tree

A strong answer models the bundle as a deliberate tree, for example:

```text
bundle/
  bin/app
  LICENSE
  share/doc/README.md
  manifest.txt
```

The answer is strongest when it also names something that should stay outside, such as:

- host diagnostics
- build logs
- timing traces

The key idea is that package layout is a contract, not a side effect of copying files from
whatever directory already exists.

## Exercise 3: Separate identity from evidence

A strong answer says something like:

- artifact identity: `app.tar.gz` plus its checksum or bundle manifest
- adjacent evidence: `app.attest.txt` with compiler or host details

The reasoning should sound like:

> if unstable host or timestamp details are packaged into the archive itself, then the
> artifact identity changes even when the release content did not.

That is the central release-engineering lesson of this module.

## Exercise 4: Make `install` safe to rerun

A strong answer introduces an explicit destination boundary, often with `DESTDIR` or a
staging root:

```make
PREFIX ?= /usr/local
INSTALL_ROOT := $(DESTDIR)$(PREFIX)
```

The answer is stronger if it states one idempotence expectation clearly, such as:

> running `make install DESTDIR=/tmp/release-check` twice should produce the same intended
> file tree under that root.

And it should include an inspection command like:

```sh
find /tmp/release-check -type f | sort
```

That turns install from a blind side effect into something reviewable.

## Exercise 5: Diagnose one release failure

A strong answer starts by classifying the failed boundary:

- build truth
- package truth
- publish truth

Then it chooses an evidence command that matches that boundary.

For example:

- wrong bundle contents
  first evidence: `tar -tzf dist/app.tar.gz`
- checksum mismatch
  first evidence: inspect the bundle inputs and the checksum target relationship
- unsafe install behavior
  first evidence: rerun install under a temporary destination root and compare the tree

The strongest answers do not jump straight to "rerun `dist`." They first decide what
boundary likely lied.

## What mastery-level answers sound like

A mastery-level answer set in this module does three things well:

- it treats release targets as interfaces with stable meaning
- it treats bundle layout as a modeled publication boundary
- it separates artifact identity from the surrounding evidence surface

That is the standard Module 08 is trying to build.
