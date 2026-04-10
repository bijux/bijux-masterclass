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

## Directory targets are the classic case

Directories are often setup requirements rather than semantic inputs. That is why a build
directory is usually better handled through `mkdir -p "$(@D)"` inside the recipe or
through a carefully chosen order-only prerequisite.

If you use a normal prerequisite for a directory, you often create rebuild noise rather
than truth.

## Stamps exist to model hidden semantic state

Sometimes a fact matters but is not naturally a file input:

- compiler flags
- configuration mode
- toolchain identity

That is when a stamp or manifest becomes useful. The point is not the filename. The point
is that the graph gets durable evidence about a semantic change.

## Serialization is the last resort

`.NOTPARALLEL` and `.WAIT` are real tools, but they are not first-choice fixes. If you
reach for them before understanding the missing or false edge, you are probably hiding a
lying DAG instead of repairing it.
