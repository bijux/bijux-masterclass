# Exercise Answers

Use this page after you have written your own answers. The value is in comparing reasoning,
not in copying sentences.

The answers below are reference-quality examples. Your own repository and target names will
vary. What should stay stable is the reasoning shape:

- start from observable behavior
- classify the finding before recommending a repair
- preserve proof while changing contracts or boundaries

## Answer 1: Write a first-pass build review

A strong answer does not try to solve everything. It makes the current system legible.

Example answer shape:

| Review section | Strong answer example |
| --- | --- |
| public targets | "`all` builds the default outputs, `release` packages and uploads, and `prepare-release` appears to be an accidental semi-public helper because CI calls it directly." |
| trusted outputs | "`dist/report.tar.gz` is treated as trusted, but both `release` and `publish` appear to regenerate inputs on the way there." |
| hidden inputs | "Environment variables choose report mode, but the graph does not model them explicitly." |
| pressure finding | "`make -j8 release` occasionally leaves partial files in `dist/`, which suggests publication is not atomic." |
| risk classes | "Top risks are contract drift, multi-writer output behavior, and boundary confusion between local packaging and remote publication." |

Why this is strong:

- it names behavior instead of insulting structure
- it uses evidence or likely evidence
- it ends with classified findings that can guide migration

Weak answers usually say only "the Makefile is messy" or "we should use a different tool."

## Answer 2: Sequence a safe migration

A strong migration answer changes one boundary and preserves one proof route.

Example:

- current contract: "`release` currently means build, validate, package, and publish."
- first boundary move: "split local package production into `dist` and keep publication
  separate."
- preserved proof: "record the current release layout with `find dist -type f | sort`
  before changing the packaging route."
- retirement condition: "the old `release` implementation can disappear once `dist`
  produces the same declared artifact set and `publish` consumes only that artifact set."

Why this is strong:

- the first change is narrow
- the answer does not remove evidence before the new route is trusted
- retirement is based on proof, not optimism

## Answer 3: Write a governance note that could actually be enforced

A strong answer is short and operational.

Example:

```text
Public targets are all, test, selftest, dist, publish, clean, and help.
Changes to public target names or meanings require maintainer review and docs updates.
CI may call only public targets.
New include files require a one-sentence responsibility statement.
New macros must state whether they compute text, define rules, or both.
Proof routes such as selftest and release audits may not be removed without a documented replacement.
```

Why this is strong:

- another maintainer could apply it in review
- it protects both contracts and proof surfaces
- it addresses the common drift points directly

Weak governance notes use language like "try to keep things simple" because nobody can
enforce that.

## Answer 4: Diagnose one recurring antipattern

Choose one pattern and name the first honest recovery move.

Example:

- antipattern: multi-writer outputs
- confirming signals:
  - "`build/report.html` changes when both `all` and `release` run"
  - "packaging routes invoke the same generator that ordinary build routes invoke"
- first repair: "assign one rule or route as the sole writer of `build/report.html` and
  make packaging depend on that published output instead of regenerating it"
- why this helps: "it restores output ownership and makes incremental behavior easier to
  reason about"

The key is to explain why the repair restores truth or ownership clarity, not just why it
looks cleaner.

## Answer 5: Make the tool-boundary argument

A strong answer focuses on ownership fit.

Example:

- concern: remote publication
- judgment: "Make should not remain the full owner"
- argument: "Make is still a good owner for producing the local artifact and checksum, but
  remote publication depends on authentication, approval, and remote state that Make cannot
  model honestly. A dedicated service should own publication policy and status."
- handoff artifact: "`dist/report.tar.gz` plus its checksum and metadata manifest"
- proving the boundary works: "the build can produce and verify the local artifact without
  talking to the remote system, and publication errors are reported by the owning service
  rather than hidden inside packaging behavior"

Why this is strong:

- it does not replace Make out of fashion
- it keeps Make where it is still honest
- it defines the handoff surface explicitly

## What all five answers have in common

The best answers in this module usually do five things:

1. they describe current behavior before prescribing a redesign
2. they classify findings in terms of truth, contract, or boundary
3. they keep evidence alive during migration
4. they write rules other maintainers could really use
5. they justify tool boundaries by modeling fit and ownership

If your answers do those five things, you are using Module 10 the right way.
