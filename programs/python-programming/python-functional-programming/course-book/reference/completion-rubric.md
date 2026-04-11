# Completion Rubric

Use this page when you need to decide whether functional-programming understanding is
actually complete or only familiar.

## Completion standard

You should be able to do all of the following:

- explain which part of a design is pure and which part is an effect boundary
- distinguish value modelling, failure modelling, and orchestration concerns clearly
- justify one choice about laziness, materialization, or retries without hand-waving
- name the proof route that would fail first if a claimed functional boundary drifted
- review a pipeline or capstone change in terms of ownership, dataflow, and proof

## Course outcomes

| Area | Completion signal |
| --- | --- |
| purity and substitution | you can explain what changes when hidden state enters a function and why that matters |
| dataflow and composition | you can read a pipeline and name where transformation, aggregation, and coordination belong |
| failures as values | you can compare explicit failure modelling with exception-shaped ambiguity |
| effect boundaries | you can defend where adapters, resources, and async shells should start |
| sustainment | you can write one review judgment backed by one guide, one file, and one proof route |

## Capstone evidence

Use these as the minimum capstone evidence:

1. `make PROGRAM=python-programming/python-functional-programming capstone-walkthrough`
2. `make PROGRAM=python-programming/python-functional-programming capstone-test`
3. `make PROGRAM=python-programming/python-functional-programming test`

Running them is not enough if you cannot explain what each route proved.

## Reviewer questions

- Which package stays pure here?
- Which boundary owns the effectful part?
- Which failure is represented explicitly rather than hidden?
- Which proof route should another reviewer trust first?
