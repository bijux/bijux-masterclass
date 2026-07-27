# Capstone Glossary

Use this page when the Snakemake capstone routes start sounding interchangeable. The goal
is to keep workflow meaning, operating policy, publish trust, and stewardship review
separate while you are inside the executable repository.

This glossary exists to keep capstone language from flattening into "run something
bigger."

## How to use this glossary

Open this page when two capstone terms sound close enough that your route choice is
getting blurry.

It is most useful when:

- two proof routes sound similar but answer different questions
- policy language starts getting confused with workflow meaning
- publish review language starts drifting into general execution language
- you need to restate a capstone term in plainer words before continuing

Do not read it as a full capstone manual. Read it when vocabulary is blocking route
choice.

## Why this glossary exists

The capstone is larger than the module examples. That makes sloppy vocabulary more
dangerous here.

This glossary keeps a few important distinctions stable:

- orientation route versus execution route
- workflow contract versus operating policy
- publish boundary versus internal run state
- saved evidence versus general repository output
- stewardship review versus ordinary walkthrough

## Terms in this directory

| Term | Meaning here | Use it when... |
| --- | --- | --- |
| walkthrough | the bounded first pass through the workflow repository before stronger executed proof | you need orientation, not full execution |
| tour | one executed workflow story with saved evidence | you need the repository to become concrete without escalating to stewardship |
| rule contract | the explicit input, output, and log relationship a rule is allowed to promise | you are judging workflow meaning rather than helper detail |
| discovery evidence | the durable artifact that records what dynamic discovery found | you need discovery to stay reviewable after execution |
| operating policy | executor, resource, and environment settings that change how the workflow runs without redefining its meaning | you are comparing local, CI, and scheduler contexts |
| semantic drift | a change that alters workflow meaning rather than only execution policy | you suspect a context or profile change is too strong |
| publish boundary | the downstream-facing output surface another person is allowed to trust | you are reasoning from the consumer side |
| saved evidence bundle | an exported artifact set that lets a reviewer inspect the workflow later | you need proof that survives after the run is gone |
| stewardship review | the stronger route used when a maintainer must judge the whole repository, not only one run | the question is about migration, drift, or long-lived trust |

## Three distinctions that matter most

### Walkthrough versus tour

- `walkthrough` is for bounded first understanding
- `tour` is for one executed workflow story

If you need the first story of the repository, start with walkthrough. If you need
execution evidence, move to tour.

### Operating policy versus semantic drift

- operating policy changes how work runs
- semantic drift changes what the workflow means

Confusing those two is one of the fastest ways to misread profiles.

### Publish boundary versus internal run state

- the publish boundary is what downstream users may trust
- internal run state supports execution, debugging, or review but is not itself the
  public contract

This distinction matters every time a learner is tempted to treat `results/` as public.

## Good stopping point

Leave this page when:

- the route terms are distinct again
- you can explain the current capstone question in plainer words
- you know which page or command should come next
