# Why Git and Scripts Are Not Enough

Module 01 should not leave you with the impression that Git is weak or useless.

Git is excellent at what it owns.

The problem is that teams often ask Git and a few scripts to carry a reproducibility story
that is larger than source control alone.

## What Git does well

Git is strong at:

- versioning text
- showing code history
- supporting branching and review
- preserving deliberate edits to source files and docs

Those are major strengths. Any honest DVC course should say that clearly.

## Where the gap opens

Reproducibility for data and ML work depends on more than source text:

- the exact data identity
- the relationship between stages
- the parameters that shaped a run
- the environment and execution context
- the resulting artifacts someone later wants to recover

Git can record some of that indirectly, but it does not model the full problem by itself.

## A practical contrast

| Workflow question | Git answers well | Git alone struggles with |
| --- | --- | --- |
| who changed the code | yes | not the main issue |
| which data bytes produced this result | not directly | this is a core gap |
| how outputs depend on inputs and stages | only by convention | weak without extra structure |
| how to recover large or derived artifacts cleanly | not Git's core job | teams improvise here |
| how to compare experimental runs beyond source diff | partly | often incomplete |

This is why "we put it in Git" is not the same claim as "we can defend the result."

## Scripts are useful, but they often hide structure

Ad hoc scripts can absolutely be part of a good workflow.

The problem appears when the scripts become the only place where important structure lives:

- which files are inputs
- which outputs are derived
- which parameters were chosen
- which order the steps are meant to run in

At that point, a teammate can read the code and still not recover the whole operational
story without asking the author.

## A small example

Imagine a repo with:

- `train.py`
- `evaluate.py`
- `run_all.sh`
- `README.md`

That may be enough to get work done.

But now ask stronger questions:

- which exact dataset version was used
- which artifacts are intermediate versus trusted outputs
- whether the shell script assumes files already exist
- whether metrics from last month can be recovered exactly

Git history plus shell commands can help, but they do not answer all of those on their
own.

## Why teams reach for memory instead of structure

Git-plus-script workflows often survive for longer than they should because the team has
informal compensations:

- one person remembers the right command
- one folder name is treated as if it were an identity
- one server still has the "real" copy
- one notebook output is accepted as evidence

That is not reproducibility. It is social caching.

## What this means for DVC

DVC is not here to replace Git.

It is here to complement Git by making parts of the workflow story more explicit:

- data and artifact identity
- stage relationships
- experiment and metric context
- recovery paths for non-source artifacts

That only makes sense once the Git boundary is understood honestly.

## The wrong conclusion to avoid

Do not leave this page thinking:

> Git failed us, so we need a different tool for everything.

The better conclusion is:

> Git is solving source history well, but source history is only part of the reproducibility problem.

That is a much more stable foundation for the rest of the course.

## Keep this standard

When evaluating a fragile workflow, ask two separate questions:

1. what is Git already preserving well
2. what important parts of the result story still have no clear owner

That second question is where DVC enters.
