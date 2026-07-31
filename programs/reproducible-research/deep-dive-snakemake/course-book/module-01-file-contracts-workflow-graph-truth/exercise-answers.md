# Exercise Answers

Use this page after you have written your own answers. The value is in comparing reasoning,
not in copying wording.

## How to use the answer page well

Do not read an answer first and then reverse-engineer your exercise around it.

A better sequence is:

1. complete the exercise with your own files and commands
2. write one plain-language explanation
3. compare your reasoning with the model answer
4. revise the explanation if the model answer exposes a gap

The goal is not identical wording. The goal is honest workflow reasoning.

The answers below are model answers. Your filenames and rule names may differ. What should
stay stable is the shape of the explanation:

- start from the target and file contract
- use one piece of workflow evidence
- explain the repair in terms of truth, ownership, or publication

The strongest self-study packets also leave behind six concrete artifacts:

- one prediction note
- one DAG or rulegraph snapshot
- one convergence check
- one wildcard-ownership note
- one publication-safety note
- one meaning-versus-policy review note

If your answers contain only commands and outcomes, the reasoning is still too thin.

## Exercise 1: Explain why one rule does not run

A strong answer sounds like this:

> The requested target is `results/final.txt`. That file is produced by `producer`, so
> Snakemake schedules `producer` and `all`. The extra rule `never_called` publishes
> `results/ghost.txt`, but no requested target depends on that file, so it has no place in
> the current DAG. A dry-run proves this because `never_called` does not appear in the job
> list.

Why this is strong:

- it starts from the requested target
- it names the matching output contract
- it treats the missing rule as irrelevant to the target graph, not as a mystery

Weak answers usually say only "Snakemake skipped the rule."

## Exercise 2: Prove convergence on purpose

A strong answer preserves the command and the second observation:

```console
snakemake --cores 1 results/declared-report.txt
snakemake --cores 1 --dry-run results/declared-report.txt
```

Expected receipt:

```text
Nothing to be done (all requested files are present and up to date).
```

The report should record threshold `10`. The declared facts that stayed unchanged are
`data/source.txt`, `policy/threshold.txt`, the rule implementation, and the requested
target.

A strong explanation is:

> The target converged for the current declared graph because no declared input or tracked
> rule meaning changed after construction. This receipt does not prove that every file
> opened by the renderer appears in the graph.

That final sentence matters. Without it, a learner can mistake planner agreement for a
complete dependency audit.

## Exercise 3: Trigger one selective rebuild

A strong answer keeps the explanation tied to dependency edges.

Example:

> After editing `data/B.txt`, the dry-run schedules only the job that publishes
> `results/B.upper.txt` plus any downstream target that depends on it. `results/A.upper.txt`
> stays untouched because the changed file is not one of its ancestors in the DAG.

Why this is strong:

- it explains the rebuild from the changed input backward
- it avoids the false idea that rule order controls rebuilds

## Exercise 4: Expose and repair an under-rebuild

Before repair, the hidden rule passes `policy/threshold.txt` through `params`. After
building at threshold `10`, changing policy to `20` produces:

```text
Nothing to be done
```

The quiet plan is the symptom. The stronger evidence pair is:

```text
current policy = 20
stored report = 10
```

The contract diff should move the policy path:

```diff
 rule hidden_report:
     input:
-        source="data/source.txt"
+        source="data/source.txt",
+        policy="policy/threshold.txt"
     output:
         "results/hidden-report.txt"
-    params:
-        policy="policy/threshold.txt"
```

The shell command must then use `{input.policy}`. After rebuilding at `10` and changing
policy to `20`, the dry-run should plan `hidden_report`.

`--force` is not a repair because it does not add the missing edge. The next policy
change would be invisible again unless a human remembered the workaround.

## Exercise 5: Diagnose one wildcard ownership problem

A strong answer names the ownership defect directly.

Example:

> The output pattern `results/{x}.txt` is too broad because both `r1` and `r2` can claim
> `results/test.txt`. The issue is not merely a brace problem; it is ambiguous file
> ownership. I would redesign the paths so the rules publish different artifact families,
> such as `results/report/{x}.txt` and `results/qc/{x}.txt`. A dry-run or rule graph then
> shows one clear owner per output family.

Why this is strong:

- it identifies ambiguity as a file-ownership problem
- it fixes the path design instead of hiding the issue with precedence tricks

## Exercise 6: Repair a poison output

The in-place case begins with `trusted`, exits `13`, and leaves:

```text
unsafe-final.txt = PARTIAL
```

The atomic failure begins with another trusted final, exits `17`, and leaves:

```text
atomic-final.txt = trusted
atomic-final.txt.tmp = complete
```

The successful atomic run then leaves:

```text
atomic-final.txt = complete
atomic-final.txt.tmp = absent
```

A useful state table is:

| State | Final | Scratch | Consumer decision |
| --- | --- | --- | --- |
| before replacement | trusted | absent | final may be consumed |
| failed atomic attempt | trusted | complete but unaccepted | final may be consumed; scratch may not |
| successful promotion | complete new value | absent | new final may be consumed |

The claim is limited to same-filesystem rename. A scratch directory mounted elsewhere
does not inherit this guarantee merely because the command is still named `mv`.

## Exercise 7: Separate workflow meaning from execution policy

A strong answer shows one value on each side of the boundary.

Example:

- config value:
  - `samples: [A, B]`
  - reason: changing it changes which outputs the workflow is supposed to build
- profile value:
  - `cores: 4`
  - reason: changing it alters execution behavior, not the meaning of results
- validation example:
  - "a schema would catch a misspelled required key like `samplez` before any job runs"
- review explanation:
  - "the split makes it easier to review whether a change alters workflow meaning or only
    the operating context"

Why this is strong:

- it makes the semantic-versus-policy split explicit
- it shows why early validation is humane, not just formal

## Exercise 8: Compare a plan with execution

After deleting `results/A.upper.txt`, a dry-run should plan only the `uppercase` job for
sample `A` plus the target aggregation. It says what Snakemake *would* do from the current
filesystem state. After execution, `--summary` should report the known outputs as current.
That summary describes file ownership and status; it is not a record that every planned
shell command succeeded in some earlier run.

## Exercise 9: Investigate a missing input

If the requested target is `results/C.upper.txt`, Snakemake can infer `sample=C` and then
requires `data/C.txt`. The error is useful evidence: the output pattern matched, but its
source contract could not be satisfied. Add the source if `C` is a legitimate sample,
remove `C` from semantic configuration if it is not, or correct the path contract if the
source lives elsewhere. Creating an empty file merely to silence the error would hide the
real defect.

## Exercise 10: Complete a trustworthy tiny project

A strong project has three explicit source records, one wildcard transformation family,
one policy file, and one summary rule. `rule all` requests the summary and any
intermediates intended as deliverables. The summary declares both transformed records
and policy as inputs, writes to a sibling scratch path, validates the table, and promotes
only after success. Logs remain separate from published data.

Verification should show:

- the first dry-run plans three transformations and one summary
- the first execution creates all expected files
- the next dry-run converges
- changing one source rebuilds its transformation and the dependent summary
- changing declared policy rebuilds only the dependent summary
- moving policy to `params` reproduces a quiet dry-run with stale output
- restoring policy under `input` repairs the planner
- an injected replacement failure preserves the prior trusted summary

The final review should classify sample membership, transformation parameters, and policy
contents as workflow meaning, while cores and shell-printing behavior remain execution
policy.

A complete acceptance argument has four parts:

> **Intervention:** I changed the declared policy from `10` to `20` and separately forced
> failure before summary promotion. **Observation:** the dry-run planned only the summary,
> and the failed writer left the prior final unchanged while scratch held the new attempt.
> **Decision:** accept the dependency and publication contracts. **Limit:** this proves
> the tested local file influence and same-filesystem rename, not arbitrary hidden inputs
> or cross-filesystem atomicity.

## What all ten answers should have in common

The best Module 01 answers usually do five things:

1. they explain behavior from the target surface backward
2. they point to a concrete evidence route such as `-n`, `--summary`, `--rulegraph`, or a
   per-job log
3. they distinguish tracked meaning from hidden or unstable state
4. they treat wildcard problems as ownership problems
5. they treat final outputs as published artifacts that must be trustworthy

If your answers do those five things, you are learning the module in the right direction.

Weak answer pattern:

- "I ran the commands, the files appeared, so the workflow is probably fine"

That sentence skips convergence, ownership, and publication trust all at once. If your
answers still sound like that, keep revising.
