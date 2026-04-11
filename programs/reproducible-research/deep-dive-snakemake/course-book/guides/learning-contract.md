<a id="top"></a>

# Learning Contract

Use this page when you need to reset how to study the program. Deep Dive Snakemake is not
built for passive reading. It is built for learners who can explain one workflow
boundary, name the failure it prevents, and point to the command or artifact that proves
the claim.

## What the program is asking from you

For each module, you should be able to do four things before you call it done:

1. explain the workflow or publish boundary in plain language
2. name the failure that would appear if that boundary were false
3. choose one command, artifact, or file that tests the claim
4. say why a heavier proof route would be unnecessary right now

If you can only recognize the vocabulary, the module is not done yet.

[Back to top](#top)

## What the program owes you

The material should present each important idea in an order that a human can actually use:

1. the contract question
2. the failure mode that makes the question matter
3. the repair or design rule
4. the proof route that can confirm the claim
5. the capstone route only after the local idea is clear

When a page jumps from slogan to command list, the learner is doing the course-design
work alone.

[Back to top](#top)

## How to work a module honestly

Use this loop:

1. Read the module overview and the lesson that matches the current question.
2. Write down one sentence that starts with "The contract here is..."
3. Run the smallest proof route that could falsify your understanding.
4. If the evidence surface feels bigger than the claim, step back to the module or guide.
5. Move on only when you can explain the idea without borrowing the page's wording.

The goal is not speed. The goal is leaving each module with something you can defend in
review.

[Back to top](#top)

## The proof surfaces you should keep reaching for

These surfaces recur because they answer different classes of question:

| Surface | Use it to answer |
| --- | --- |
| dry-run output | what Snakemake intends to do before execution |
| `--summary` | what outputs exist and how Snakemake currently sees them |
| `--list-changes` | why code, params, or inputs now justify reruns |
| `FILE_API.md` | what downstream users are allowed to trust |
| publish bundle contents | what the repository promotes as a versioned contract |
| verification and test targets | whether the repository can defend its claims after execution |

Good study means choosing the surface that matches the claim instead of jumping straight
to the biggest route.

[Back to top](#top)

## When the capstone is appropriate

Open the capstone when the local idea is already stable and you want to see it survive a
real repository shape.

Do not open the capstone yet when:

- you still need a first explanation of the concept
- you cannot name the failure the module is trying to prevent
- you do not know which command would count as proof
- the repository still feels larger than the lesson itself

Use [Capstone Map](../capstone/capstone-map.md) when the concept is clear but the right
repository route is not.

[Back to top](#top)

## Signs you are fooling yourself

Stop and reset if any of these are true:

- you keep widening the reading surface because one page did not click
- you can quote the term but cannot give a failure example
- you chose `proof` or `capstone-confirm` because it felt safer than thinking
- you can follow the capstone mechanically but cannot say which boundary owns the behavior

Those are not minor study gaps. They usually mean the previous page needs a slower,
smaller pass.

[Back to top](#top)
