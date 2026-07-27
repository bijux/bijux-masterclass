# Start Here

Use this page when Snakemake is new, when the course feels too large, or when you need
the safest route back to first principles. This page exists to protect beginners from a
common mistake: widening the surface before the first workflow is actually clear.

Deep Dive Snakemake does not begin with clusters, profiles, or a large repository. It
begins with one honest rule, one target, one dry-run, and one explanation you can defend.

## If you are learning this without the live class

Read this page in four passes:

1. confirm you are still at first contact rather than already in capstone pressure
2. complete the first-hour route once without widening the surface
3. write down what the first workflow proved and what it did not prove
4. move into Module 00 and Module 01 only after the local model is stable

If you start opening later shelves before step 2 is honest, the course will feel larger
and weaker at the same time.

## What you need from day one

On your first pass, you do not need:

- the full capstone repository
- checkpoint mechanics
- scheduler policy
- publish versioning
- architecture review

You do need:

- a working `snakemake --version`
- one small local example
- one dry-run you can read
- one rerun you can explain

That is enough to start building the right model.

## The first packet you should keep beside you

Before you widen into the modules, keep one tiny starter packet:

- one command confirming Snakemake is installed
- one small workflow you can run locally
- one dry-run capture
- one explanation of why the second run does no work
- one explanation of why changing one input changes the plan

If that packet feels too small, that is a sign you are still reaching for scale instead
of clarity.

## The first-hour route

If you only have one hour, do this and stop:

1. Confirm `snakemake --version` works.
2. Complete [your first workflow](../module-00-orientation/index.md#your-first-workflow).
3. Run a dry-run and explain why Snakemake wants the planned job.
4. Run the workflow twice and explain why the second run does no work.
5. Edit one input and explain why the target becomes eligible again.

If you can do those five things honestly, you have a real start.

## The sentence to keep in your head

When the course feels bigger than you want, return to this sentence:

> Today I only need to understand why one target ran, why the second run did not, and
> why changing one input changed the plan.

That is not a low standard. That is the core model that everything else in the course
keeps extending.

## A first-contact card you should be able to fill quickly

Use a table like this before you keep reading:

| Question | Short honest answer |
| --- | --- |
| what target did I ask for | one file Snakemake owes me |
| what rule can build it | one visible file contract |
| what did the dry-run prove | what work is planned before any command runs |
| what did the second run prove | the workflow can converge instead of repeating work forever |
| what did changing one input prove | dependency edges, not vibes, drive rebuilds |

If any row still feels vague, stay here longer. That is not falling behind. It is
protecting the model the whole course depends on.

## Read this page in order

1. confirm you are still at first contact
2. complete the first-hour route once
3. stop before you widen the surface
4. move into Module 00 and Module 01 while the example is still fresh

This page is intentionally narrow. If it starts turning into a dashboard, you have
already opened too much.

## Use this page when

- Snakemake still feels unfamiliar
- you opened too many course pages and lost the teaching sequence
- the capstone looks tempting but the local model is still fuzzy
- you need to restart the course without pretending you remember more than you do

## Do not use this page to

- replace the module sequence with support-page browsing
- skip the actual first workflow
- choose the strongest proof route by default
- justify entering the capstone before one local rule is clear

## What beginners often do wrong

The most common early mistake is believing that a larger repository or a more advanced
topic will somehow make the concept clearer.

Usually it does the opposite.

If one small workflow is still fuzzy, then:

- more files create more hiding places
- more profiles create more noise
- more proof routes create more ceremony
- more advanced pages create more vocabulary without more understanding

## What goes wrong when the surface widens too early

Use this card when you feel the urge to jump ahead:

| If you are tempted to... | The likely hidden problem is... | Smaller move instead |
| --- | --- | --- |
| open the capstone first | the local model is still fuzzy | rerun one tiny workflow and explain the plan |
| browse many guide pages at once | sequence anxiety is replacing learning | stay with Start Here, Module 00, and Module 01 |
| choose the strongest proof route immediately | evidence appetite is outrunning the question | keep one dry-run and one rerun explanation |
| jump to late governance or incident pages | advanced vocabulary feels safer than first principles | return to one requested target and one file contract |

If the smaller move feels too humble, that usually means it is the right one.

## The best first pass

Use this route and stop there:

1. [Platform Setup](platform-setup.md)
2. [Module 00](../module-00-orientation/index.md)
3. [Course Map](../module-00-orientation/course-map.md)
4. [Module 01](../module-01-file-contracts-workflow-graph-truth/index.md)

Do not open the capstone or the reference shelf until Module 01 is making sense in your
own words.

## If your pressure is not purely beginner pressure

| If you need... | Read next | Keep nearby |
| --- | --- | --- |
| first contact with Snakemake | [Module 00](../module-00-orientation/index.md), [Module 01](../module-01-file-contracts-workflow-graph-truth/index.md), [Module 02](../module-02-dynamic-dags-discovery-integrity/index.md) | [Module Checkpoints](module-checkpoints.md) |
| repair of an existing workflow | [Pressure Routes](pressure-routes.md), [Module 03](../module-03-production-operations-policy-boundaries/index.md), [Module 04](../module-04-scaling-workflows-interface-boundaries/index.md) | [Boundary Review Prompts](../reference/boundary-review-prompts.md) |
| stewardship of a long-lived repository | [Course Guide](course-guide.md), [Module 06](../module-06-publishing-downstream-contracts/index.md), [Module 07](../module-07-workflow-architecture-file-apis/index.md) | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |

## What to keep open and what to keep closed

Keep open:

- [First-Contact Map](../module-00-orientation/first-contact-map.md)
- [Course Guide](course-guide.md)
- [Module Checkpoints](module-checkpoints.md)

Keep closed for now:

- the larger capstone surfaces
- late-module incident and governance pages
- reference pages you are not yet using to solve a real learning problem

## A five-line beginner note you should be able to write from memory

If this page has done its job, you should be able to write:

1. which target your first workflow requested
2. which rule produced it
3. what the dry-run told you before execution
4. why the second run did no work
5. why the capstone is not your first lesson

If you cannot do that, stay in the starter route a little longer.

## Success signal

You are ready to leave this page when you can explain:

- what makes a workflow contract truthful
- why a target selects the rules Snakemake needs
- why a second run may do no work
- why the capstone is not your first lesson

When you can say those clearly, continue into Module 00 and Module 01.
