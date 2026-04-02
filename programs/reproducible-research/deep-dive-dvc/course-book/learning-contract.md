<a id="top"></a>

# Learning Contract

Deep Dive DVC is built around one rule: important claims about reproducibility should be
checkable by inspecting state, running commands, or exercising a recovery path.

This page makes that rule explicit so the learner knows what the course expects and how
to use each module well.

---

## The Teaching Sequence

The strongest sections in this course follow this order:

1. failure mode
2. state model
3. explicit contract
4. proof command
5. capstone corroboration

If a section jumps straight from advice to commands, it is weaker than the course should
be.

[Back to top](#top)

---

## The Learner's Responsibility

Your job is not to memorize DVC commands. Your job is to verify what state the repository
is claiming.

For each module, you should be able to answer:

* what state changed
* where that change was declared
* what evidence makes the change reviewable later
* which command proves the claim instead of only asserting it

[Back to top](#top)

---

## The Instructor's Responsibility

The course material should always provide:

* a clear state question
* an explanation of the failure mode it prevents
* a proof loop the learner can run
* a reason the capstone is or is not the right teaching surface yet

If those are missing, the learner has to reconstruct the pedagogy alone.

[Back to top](#top)

---

## The Proof Tools You Should Use Constantly

These surfaces appear throughout the course because they answer different reproducibility
questions:

| Surface | What it proves |
| --- | --- |
| `dvc.yaml` | the declared pipeline contract |
| `dvc.lock` | the recorded state transition after execution |
| `params.yaml` | the declared control surface |
| tracked metrics | the declared comparison surface |
| publish bundle | the promoted downstream contract |
| recovery drill | whether durability claims survive local loss |

[Back to top](#top)

---

## When To Use The Capstone

Use the capstone when the concept is already legible in a smaller mental or local model
and you want to inspect how it behaves in a realistic DVC repository.

Do not use the capstone:

* as your first exposure to a concept
* as a substitute for understanding state layers
* as evidence that you understand a topic you still cannot explain in plain language

Use [`capstone-map.md`](capstone-map.md) when you need a guided route through the
repository.

[Back to top](#top)

---

## Definition Of Done For A Module

A module is complete only when you can:

* explain the state boundary it teaches
* identify one representative failure mode
* run its core proof loop
* connect the local concept to one capstone surface intentionally

If you can only repeat terms like "reproducibility" or "tracking," the module is not
done yet.

[Back to top](#top)
