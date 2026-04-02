# Proof Ladder


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  ladder["Proof ladder"]
  read["Reading proof"]
  inspect["Inspection proof"]
  execute["Executable proof"]

  ladder --> read
  ladder --> inspect
  ladder --> execute
```

```mermaid
flowchart LR
  question["What do I need to prove?"] --> small["Choose the smallest honest proof"]
  small --> inspect["Inspect guides or code"]
  inspect --> execute["Escalate to commands only when needed"]
```
<!-- page-maps:end -->

Use this page when you are deciding how much proof you need. Not every OOP question
needs the strongest capstone command, and using the heaviest route too early often
hides the actual design issue.

## The ladder

| Need | Smallest honest proof | Escalate when |
| --- | --- | --- |
| understand the course promise | [Course Home](../index.md) and [Start Here](start-here.md) | you still cannot place the module you need |
| understand one module promise | [Module Promise Map](module-promise-map.md) and the module overview | the ownership rule is still fuzzy |
| know whether you are ready to move on | [Module Checkpoints](module-checkpoints.md) | you cannot explain the checkpoint in code |
| inspect the capstone shape | [Capstone Map](capstone-map.md) and [Capstone File Guide](capstone-file-guide.md) | you need executable evidence |
| review architecture and boundaries | [Capstone Architecture Guide](capstone-architecture-guide.md) and [Capstone Walkthrough](capstone-walkthrough.md) | you need durable saved evidence |
| review executable evidence | [Capstone Proof Guide](capstone-proof-guide.md) and `make PROGRAM=python-programming/python-object-oriented-programming capstone-confirm` | you need to modify or extend the capstone itself |

## Rules for escalation

- Read before you run when the question is architectural.
- Run before you speculate when the question is behavioral.
- Use the smallest proof that answers the current question.
- Escalate one rung at a time instead of jumping directly to confirmation.

## Common misuse

- using `capstone-confirm` to answer a question that a module overview already settles
- treating saved proof artifacts as if they replace reading the design surfaces
- reading the capstone without knowing what module promise you are trying to confirm

The ladder keeps the proof route proportional. That makes the capstone support the
course instead of overshadowing it.
