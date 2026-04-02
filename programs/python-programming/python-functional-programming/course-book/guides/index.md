# Guides


<!-- page-maps:start -->
## Page Maps

```mermaid
graph TD
  hub["Guides"] --> study["Study guides"]
  hub --> capstone["Capstone guides"]
  study --> modules["Modules 01-10"]
  capstone --> proof["Proof and review routes"]
```

```mermaid
flowchart LR
  choose["Choose what you need"] --> route["Pick the matching guide"]
  route --> read["Read with the module or capstone open"]
  read --> inspect["Inspect the named code or artifact"]
  inspect --> verify["Run the matching command when needed"]
```
<!-- page-maps:end -->

This directory collects the durable learner guides for the course. The course home
explains what the course teaches. The guides explain how to study it, how to compare your
work with the reference states, and how to inspect the capstone without guessing.

## Read These First

- [Start Here](start-here.md) for the shortest honest entry route
- [Course Guide](course-guide.md) for the module arc and support-page roles
- [Foundations Reading Plan](foundations-reading-plan.md) for a lower-density route through Modules 01 to 03
- [FuncPipe RAG Primer](funcpipe-rag-primer.md) for the smallest capstone-domain vocabulary needed to study the course
- [Outcomes and Proof Map](outcomes-and-proof-map.md) for the explicit course alignment between learning goals, activities, and proof
- [Learning Contract](learning-contract.md) for the teaching bar and proof expectations
- [Orientation Overview](../module-00-orientation/index.md) for the full course shape
- [Course Orientation](../module-00-orientation/course-orientation.md) and [How to Study This Course](../module-00-orientation/how-to-study-this-course.md) for the reading rhythm

## Use These For Study Planning

- [Module Dependency Map](module-dependency-map.md) when you need the sequence explained
- [Practice Map](practice-map.md) when you want the rehearsal loop in one place
- [History Guide](history-guide.md) when you want `_history` and module worktree comparisons

## Use These For Commands And Proof

- [Command Guide](command-guide.md) for the executable surface
- [Proof Matrix](proof-matrix.md) for routing a claim to the right evidence
- [Review Checklist](../reference/review-checklist.md) and [Self-Review Prompts](../reference/self-review-prompts.md) when you need a stable review bar

## Use These For Capstone Reading

- [FuncPipe Capstone Guide](capstone.md) for the capstone’s role in the course
- [Capstone Map](capstone-map.md) for the module-to-repository route
- [Capstone File Guide](capstone-file-guide.md) for package-first reading
- [Capstone Test Guide](capstone-test-guide.md) for test-first reading
- [Capstone Review Worksheet](capstone-review-worksheet.md) for review prompts
- [Capstone Architecture Guide](capstone-architecture-guide.md) for boundary ownership
- [Capstone Walkthrough](capstone-walkthrough.md) for the human review story
- [Capstone Proof Guide](capstone-proof-guide.md) for verification depth
- [Capstone Extension Guide](capstone-extension-guide.md) for change placement

## Keep The Layout Stable

- `index.md` stays the course home
- `guides/` stays the learner route and proof shelf
- `reference/` stays the durable standards and checklist shelf
- `module-00-orientation/` plus Modules `01` to `10` stay the teaching arc
