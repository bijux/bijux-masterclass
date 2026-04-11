<a id="top"></a>

# Learning Contract

Use this page when you need to reset how to study the course. Deep Dive Make is not built
for passive reading. It is built for learners who can explain what changed, prove it with
one fitting command, and stop before a larger surface hides the point.

## What the course is asking from you

For each module, you should be able to do four things before you call it done:

1. explain the rule or boundary in plain language
2. name the failure it is supposed to prevent
3. choose one command or file that proves the claim
4. say why a heavier proof route would be unnecessary right now

If you can only recognize the wording, the module is not done yet.

[Back to top](#top)

## What the course owes you

The material should make every important idea legible in the same order:

1. a concept with a clear boundary
2. a failure mode that shows why the boundary matters
3. a small example or exercise
4. a proof route that can confirm the claim
5. a capstone surface only after the local idea is clear

When a page skips from slogan to advice, the page is unfinished. You should not have to
reconstruct the lesson design by yourself.

[Back to top](#top)

## How to work a module honestly

Use this loop:

1. Read the module overview and the lesson that matches the current question.
2. Write down one sentence that starts with "This matters because..."
3. Run the smallest proof route that can falsify your understanding.
4. If the proof surface feels bigger than the claim, step back to the module or guide.
5. Move on only when you can explain the idea without copying the page's wording.

The point is not speed. The point is leaving each module with something you can defend.

[Back to top](#top)

## The proof bar for this course

These commands appear often because they answer different classes of question:

| Command | Use it to answer |
| --- | --- |
| `make -n <target>` | what Make intends to do |
| `make --trace <target>` | why a target ran or stayed stale |
| `make -p` | what variables and rules exist after evaluation |
| `make -q <target>` | whether the graph has converged |
| `make -jN <target>` | whether the build stays truthful under concurrency |

Good study means choosing the command that matches the claim instead of jumping straight
to the strongest available route.

[Back to top](#top)

## When the capstone is appropriate

Open the capstone when the local idea is already stable and you want to see it survive a
realer repository shape.

Do not open the capstone yet when:

- you still need a first explanation of the concept
- you cannot name the defect the module is trying to prevent
- you do not know which command would count as proof
- the repository feels bigger than the lesson itself

Use [Capstone Map](../capstone/capstone-map.md) when you know the concept but need the
right repository route.

[Back to top](#top)

## Signs you are fooling yourself

Stop and reset if any of these are true:

- you keep widening the reading surface because one page did not click
- you can quote the rule but cannot give a failure example
- you chose `proof` or `confirm` because it felt safer than thinking
- you can follow the capstone mechanically but cannot say which boundary owns the behavior

Those are not small study gaps. They usually mean the previous page needs a slower, more
bounded pass.

[Back to top](#top)
