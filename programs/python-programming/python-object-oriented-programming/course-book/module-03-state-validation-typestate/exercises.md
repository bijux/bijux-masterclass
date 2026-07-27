# Exercises

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["State Validation Typestate"]
  page["Exercises"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  legal["name legal and illegal states"] --> validate["choose the validation boundary"]
  validate --> nulls["replace ambiguous null semantics"]
  nulls --> lifecycle["make transitions explicit"]
  lifecycle --> typestate["shape the API around allowed operations"]
```
<!-- page-maps:end -->

Use these exercises as one full lab on state discipline. The goal is not to repeat
phrases such as "invalid states should be unrepresentable." The goal is to prove that a
learner studying alone can take one messy object and turn it into a design with legal
states, explicit transitions, and reviewable boundaries.

## Running lab scenario

Use one object all day so the reasoning compounds instead of resetting every exercise.
If you do not already have a capstone candidate, use this scenario:

`ReportDraft`

- `author_id` must always exist
- `title` may start blank but cannot be blank once the draft is submitted
- `sections` may be empty while drafting but not when ready for review
- `submitted_at` exists only after submission
- `approved_at` exists only after approval
- approved reports cannot be edited
- rejected reports may return to draft with a reason

You may replace the scenario with your own object, but keep the same kind of lifecycle
pressure: drafting, readiness, submission, review, and retirement.

## What to keep open while you work

Maintain one state packet as you go. By the end it should contain:

- one legal-state table
- one illegal-state list
- one validation-boundary note
- one nullability repair
- one transition map
- one API review showing how callers are guided toward legal use

Use these tables directly instead of keeping the reasoning in your head:

| State | Fields that must exist | Fields that must not exist | Allowed operations | Illegal operations |
| --- | --- | --- | --- | --- |

| Ambiguous value today | Meanings currently overloaded | Chosen replacement | Why the replacement is clearer |
| --- | --- | --- | --- |

## Exercise 1: Name the legal states

Using the running scenario, define the smallest honest set of states.

Produce:

- a legal-state table
- one sentence per state explaining what becomes true there
- one sentence naming the most dangerous illegal state

Do not start with field flags. Start with business meaning.

## Exercise 2: Name illegal combinations explicitly

List at least five illegal combinations, such as:

- submitted with no sections
- approved with no submission time
- approved and still editable

For each one, say:

- why the combination is semantically impossible
- where you want the system to reject it

This is the exercise where most weak models stop hand-waving.

## Exercise 3: Choose the construction boundary

Decide what must be true at construction time and what may wait for a later transition.

Write:

- one constructor contract
- one factory or builder alternative if the constructor would become dishonest
- one test that should fail if construction accepts too little or too much

If you need a partially usable object, explain why that is a real state rather than a
shortcut for unfinished design.

## Exercise 4: Repair one overloaded `None`

Find one field whose absence is currently doing too many jobs.

For example:

- `submitted_at is None` might mean draft, rejected, or invalid reset
- `reviewer_id is None` might mean unassigned, not yet loadedd, or no review needed

Replace the ambiguity with one of these:

- a clearer state split
- a dedicated value object
- a sum of explicit fields with sharper meaning

Show the before-and-after representation.

## Exercise 5: Review a property as a contract surface

Pick one attribute-like behavior from the running scenario, such as `is_editable`,
`ready_for_review`, or `approval_status`.

Explain:

- whether it should remain a property
- whether it hides surprising work
- what a caller should infer when reading `object.attr`

If the surface should stay a method, say why attribute syntax would mislead readers.

## Exercise 6: Review a dataclass honestly

Pretend the running scenario is implemented with `@dataclass`.

Decide:

- whether mutability is still honest
- whether default values reflect reality or only convenience
- whether equality should compare content or identity
- whether `frozen`, `slots`, or post-init validation help or distort the design

End with one recommendation: keep the dataclass, narrow it, or replace it.

## Exercise 7: Draw the lifecycle transitions

Create a transition map with:

- allowed moves
- forbidden moves
- the method or boundary that should enforce each move

Minimum transitions to evaluate:

- `draft -> submitted`
- `submitted -> approved`
- `submitted -> rejected`
- `rejected -> draft`

Add one transition you refuse to support and explain why.

## Exercise 8: Narrow the API with typestate pressure

Redesign the public API so illegal operations become harder to express.

Examples:

- editing methods available only on draft or rejected states
- approval method available only on submitted state
- derived read-only view for approved reports

You do not need a fancy static type trick. A runtime-enforced state split is enough if it
removes misleading operations from the obvious path.

## Exercise 9: Place validation libraries at the boundary

Assume external input for the scenario arrives as JSON or a form payload.

Decide:

- what a boundary validator should parse or normalize
- what must remain domain validation inside the object model
- what false confidence appears if library validation is treated as full correctness

Write one short edge-to-domain flow from raw payload to valid object.

## Exercise 10: Produce the full state packet

Finish the lab by writing a short review note that includes:

- legal states
- illegal combinations
- constructor boundary
- nullability repair
- transition map
- one remaining risk
- one reason the model is now safer to maintain

If another learner cannot tell when the object is legal and who enforces transitions, the
packet is not finished yet.

## Done means reviewable, not merely answered

You are done with the exercise day when your packet can survive three review questions:

- "What are the legal states and why?"
- "Where does invalid state get rejected first?"
- "Which operations disappear once the object changes state?"

If those answers are still fuzzy, keep tightening the packet before you open the answer
page.
