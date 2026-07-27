# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning keeps policy and workflow meaning separate.

## How to use the answer page well

Do not read a model answer before you have classified the context change or traced the
storage boundary yourself.

A stronger rhythm is:

1. inspect the profiles, plans, or storage route on your own
2. write one plain-language explanation of what stayed invariant
3. compare that explanation with the model answer
4. revise where the model answer reveals a hidden semantic leak, weak failure model, or
   premature trust boundary you missed

The target is not identical wording. The target is clearer context judgment.

## Exercise 1: Decide whether a profile change is safe

Likely operating policy:

- local: `latency-wait: 60`
- CI: `printshellcmds: false`

Likely semantic leak:

- SLURM: a different `publish_dir`

Why:

Latency waits and shell-command visibility change how the workflow is run and observed.
A different publish directory changes a trusted contract path and therefore changes more
than policy.

Weak answers classify keys by habit instead of by whether they change trusted outputs,
paths, or semantic meaning.

## Exercise 2: Review retries honestly

Why this may be weak:

- it increases policy pressure without first classifying the failure
- it risks hiding deterministic workflow or environment defects

What question should be asked first:

- is this failure plausibly transient, or is it deterministic?

What evidence to request:

- failed logs
- any cluster or storage evidence that explains the intermittence
- confirmation that incomplete outputs are handled explicitly

The main lesson is that retries are not a substitute for diagnosis.

Weak answers jump from "the run failed" to "increase retries" without naming the failure
class first.

## Exercise 3: Diagnose a storage-boundary problem

What trust problem this creates:

- reviewers are inspecting a temporary execution surface as if it were the contract
  surface

When a file should count as trusted:

- once it has been materialized onto the declared workflow or publish path that the
  contract says reviewers and downstream users may trust

What needs clarification:

- the boundary between scratch or staging locations and trusted output locations
- the visibility and promotion model for outputs

Weak answers trust the first visible bytes even when the contract says trust begins only
after promotion onto a declared output path.

## Exercise 4: Compare three contexts

A strong argument would say:

> Side-by-side dry-run comparison matters because all three contexts can "work" while
> still carrying different workflow meaning. Dry-runs help reveal whether profiles changed
> only execution policy or whether one context now plans a different semantic story.

Why:

- successful execution is not enough evidence against semantic drift
- comparison makes hidden context-specific behavior much easier to spot

Weak answers compare only whether the run eventually passed and therefore miss planning or
contract drift.

## Exercise 5: Escalate a semantic profile leak

Why this is not just a profile difference:

- sample filtering changes workflow semantics and published meaning

Which review surface should own that decision:

- visible workflow or config-contract surfaces, not profile policy

What should happen before approval:

- move the semantic setting into an explicit workflow or config boundary
- review the effect on contracts and outputs
- compare contexts again after the change is made honest

Weak answers call this "just a profile preference" even after the setting changes sample
membership, paths, or published meaning.

## Exercise 6: Build a governed policy matrix

Every key belongs to one named policy class. Cores and concurrency are capacity;
printed commands and failed logs are observability; bounded retries are recovery;
latency and scratch roots are filesystem policy; queue and account are executor mapping.
Sample sets, algorithm parameters, and publish paths are semantic leaks. Repeated settings
may remain explicit when readability matters, but their ownership and consistency should
be auditable.

Example matrix headings:

- key
- local value
- CI value
- scheduler value
- policy class
- justified difference or semantic leak

Why this is strong:

- it turns profile review into an auditable inventory
- it makes semantic leaks stand out instead of hiding inside raw YAML

## Exercise 7: Map resources to two executors

The rule declares portable needs with documented units. Local policy caps concurrency and
respects available memory; scheduler policy translates the same values into submission
resources. Queue names and submission syntax never enter the rule. Output paths and
algorithm parameters remain identical when mappings change.

Weak answers move executor-specific syntax into the rule and then claim the workflow is
still portable.

## Exercise 8: Verify scratch promotion

Scratch holds private execution state. After computation, the job validates content,
copies or renames through a temporary destination at the trusted location, and atomically
publishes the final path. Interruption leaves no final output and retains enough logs or
staged evidence for diagnosis. Reviewers never inspect scratch as a substitute for the
declared contract.

Example lifecycle checkpoints:

- scratch allocation
- step-local write
- validation before promotion
- temporary destination at the trusted boundary
- atomic final publication
- cleanup or retained failure evidence

Why this is strong:

- it makes the trust boundary observable
- it prevents reviewers from confusing temporary execution state with final outputs

## Exercise 9: Write an operating-context drift gate

The gate allowlists context-owned differences and compares semantic invariants. It fails
with the profile, key or target, expected value, and observed value. A changed
`publish_dir` or filtering parameter is rejected; cores, executor name, and account may
differ under documented policy. This targeted gate complements execution tests rather
than replacing them.

Weak gates compare everything blindly or ignore semantic dry-run differences completely.

## Exercise 10: Review a policy change like a maintainer

A strong review orders findings by semantic risk: changed trusted path, leaked semantic
config, unclassified retry increase, or unexplained storage assumption. One accepted
policy difference should stay clearly inside observability, capacity, or executor mapping.
Each decision should name the narrowest verification route that supports it, such as a
dry-run comparison, governed key audit, or storage-lifecycle check.

Weak reviews say only "profiles differ by environment" and never decide which difference
is acceptable and which is a leak.

## Self-check

If your answers consistently explain:

- what stays in policy
- what belongs to workflow meaning
- what evidence justifies retry or latency changes
- when storage and path trust become review issues

then you are using the module correctly.
