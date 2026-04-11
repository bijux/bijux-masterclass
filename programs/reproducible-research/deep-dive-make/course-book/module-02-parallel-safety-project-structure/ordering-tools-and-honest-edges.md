# Ordering Tools and Honest Edges

Make gives you several ways to impose order. The only acceptable ordering is ordering
that tells the truth.

## The core rule

Use the smallest tool that matches the real dependency.

If target `Y` needs the content of `X`, write:

```make
Y: X
```

If `Y` merely needs `X` to exist, but changes to `X` should not trigger rebuilds, use an
order-only prerequisite:

```make
Y: | X
```

The difference is not cosmetic. It changes what Make is allowed to infer from a changed
mtime.

## A small chooser table

| Situation | Correct tool | Reason |
| --- | --- | --- |
| Output meaning changes when `X` changes | real prerequisite | content dependency is real |
| `Y` needs a directory or setup path to exist | order-only prerequisite or `mkdir -p "$(@D)"` | existence matters, not mtime churn |
| Flags or build mode change output meaning | stamp or manifest | semantic input needs durable evidence |
| You cannot yet model a clean boundary | redesign first, serialize last | hidden truth is still hidden under `.NOTPARALLEL` |

## Directory targets are the classic case

Directories are often setup requirements rather than semantic inputs. That is why a build
directory is usually better handled through `mkdir -p "$(@D)"` inside the recipe or
through a carefully chosen order-only prerequisite.

If you use a normal prerequisite for a directory, you often create rebuild noise rather
than truth.

That rebuild noise matters because it trains you to distrust Make for the wrong reason.
The real bug is not "Make is noisy." The real bug is that the graph treated a setup path
as if it were semantic content.

## Stamps exist to model hidden semantic state

Sometimes a fact matters but is not naturally a file input:

- compiler flags
- configuration mode
- toolchain identity

That is when a stamp or manifest becomes useful. The point is not the filename. The point
is that the graph gets durable evidence about a semantic change.

The most common mistake here is an always-changing stamp such as:

```make
stamp:
	date > $@
```

That does model change, but it models change constantly. The result is non-convergence.
The right question is whether the stamp changes when the semantic fact changes, not
whether the stamp changes at all.

## Serialization is the last resort

`.NOTPARALLEL` and `.WAIT` are real tools, but they are not first-choice fixes. If you
reach for them before understanding the missing or false edge, you are probably hiding a
lying DAG instead of repairing it.

## A good review sentence

When you choose an ordering tool, try to say the decision out loud:

- "`Y: X` because `Y` depends on the content of `X`."
- "`Y: | dir/` because `Y` needs the directory to exist, but directory mtimes should not
  force rebuilds."
- "`Y: flags.stamp` because compiler mode changes `Y` even when source files do not."

If the sentence sounds vague, the rule probably is too.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain the difference between a real and order-only prerequisite
- describe one situation where a stamp is the honest tool
- explain why directory mtimes often create noise rather than signal
- say why serialization is not the first repair for a lying graph
