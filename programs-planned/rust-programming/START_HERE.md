# How to study the ninety-module program

## What completion means

A module is complete when you can do all six of these things without following the chapter line by line:

1. state the mechanism and its boundary in plain language;
2. predict the decisive compiler, runtime, build, platform, or schedule consequence;
3. repair a broken design without deleting the difficult requirement;
4. build the independent laboratory from its contract;
5. integrate the matching capstone increment;
6. transfer the idea to a different product and defend the trade-off.

Reading is necessary but not sufficient. Passing tests is necessary but not sufficient. The finish line is working code plus a causal explanation.

## The daily sequence

### Morning — construct the model

Read the authoritative module chapter in order. Type the central examples. After each example, change one assumption: ownership, lifetime, input shape, receiver, bound, adapter order, generated syntax, byte length, failure path, thread topology, queue capacity, memory ordering, future state, frame boundary, or protocol phase. Predict the consequence before compiling.

Write the module’s reasoning artifact beside the code. That artifact may be an ownership ledger, loan graph, law table, iterator stage map, macro expansion ledger, safety dossier, concurrency protocol map, performance claim ledger, or release manifest. Its purpose is to prevent an API name from replacing an argument.

### Midday — predict and repair

Complete the workbook prediction table before running a specimen. For a repair task, preserve the product contract. A clone, box, trait object, `RefCell`, macro, unsafe block, lock, channel, atomic, or parallel iterator is not automatically wrong. It is wrong when it hides an unexamined requirement or claims a guarantee it does not provide.

For each failed prediction, record:

- what you expected;
- the decisive rule;
- the earliest phase or event that can know the result;
- the smallest principled repair;
- one tempting repair that weakens the product.

### Afternoon — isolate the mechanism

Work from a copy of the lab starter. Run its baseline checks. Write the public contract and first adversarial case before opening the solution. The lab is intentionally smaller than the capstone so the mechanism remains visible.

A good lab result includes:

- observable behavior;
- explicit invalid cases;
- state after failure;
- ownership and cleanup;
- deterministic output where promised;
- a transfer implementation that changes the domain rather than only the names.

### Evening — integrate and explain

Apply the capstone increment. Identify the invariant that changes before touching code. Compare with the reasoned solution only after a serious attempt. End with a short closed-book reconstruction:

```text
one governing invariant
one decisive rule
one rejected shortcut
one failure path
one transfer case
```

## Laboratory method

A laboratory is an independent product, not a fill-in-the-blank copy of the capstone.

1. Copy `starter/` into your own working directory.
2. Run the baseline tests and read the public API.
3. Write the first missing behavior as a test.
4. Implement one invariant at a time.
5. Add adversarial tests before broad refactoring.
6. Complete the independent transfer requirement.
7. Only then inspect `solution/`.

The reference is one defended implementation, not a grading key. Compare accepted inputs, rejected inputs, state after failure, ownership, authority, deterministic behavior, public surface, and cost claims before comparing syntax.

## The course-book hierarchy

Within each course, use this order:

```text
course overview
    → ten-day plan
        → module chapter
            → workbook
                → lab
                    → capstone increment
                        → reasoned solutions
                            → reference desk
                                → final review
```

The module chapter is authoritative. Reference pages compress material for later retrieval; they do not replace the derivation.

## Prediction and boundary records

For every compiler, runtime, build, systems, concurrency, async, or protocol case, record:

- expected outcome category;
- decisive line, token, state transition, synchronization event, or external action;
- governing contract;
- earliest phase or event that establishes the result;
- smallest repair that preserves the requirement;
- tempting repair that merely avoids the difficult proof.

Do not call a runtime panic a compiler failure, a race condition a data race, a platform observation a language guarantee, or a passing stress test a liveness proof.

## When to stop and repair

Do not advance when:

- you make edits you cannot explain;
- three predictions fail for unrelated reasons;
- your design depends on a later-course mechanism to avoid understanding the current one;
- the success path works but failure leaves an unspecified state;
- cleanup, join, or shutdown ownership is unclear;
- a concurrency test relies on sleep duration rather than a causal event;
- an atomic ordering is chosen by habit rather than a publication argument;
- a claim is stronger than the type, test, platform, safety, or schedule evidence behind it.

Reduce the problem to the smallest counterexample, rebuild the model, and return to the lab only when the cause is clear.

## Time and pacing

One course is ten focused days, normally five days per week for two weeks. A dense day is eight to ten focused hours including breaks. The weekend between weeks is for repair, closed-book reconstruction, and rest—not new material.

The suggested day is:

```text
08:30  retrieval from yesterday
09:00  chapter and worked examples
10:45  prediction and diagnostic cases
13:15  focused exercises
15:00  independent laboratory
16:45  capstone increment
19:00  tests, refactoring, and explanation
20:00  closed-book checkpoint
```

## Course-specific records

| Course | Keep this record beside your code |
|---:|---|
| 1 | type/state trace and ownership ledger |
| 2 | place/loan/lifetime graph and cleanup or liveness state machine |
| 3 | contract law table and variation/dispatch map |
| 4 | capture ledger, iterator stage map, failure policy, and cost ledger |
| 5 | source-of-truth, grammar, expansion, and phase ledger |
| 6 | representation, resource-state, boundary, safety, and ABI ledger |
| 7 | ownership, synchronization, exclusion, liveness, failure, determinism, and resource ledgers |
| 8 | future-state, task-tree, framing, protocol, capacity, cancellation, and retry ledgers |
| 9 | performance claim, workload, profile, allocation, byte journey, observability, threat, and release ledgers |

## Concurrent, async, and production practice

For Courses 7 and 8, a passing result under one schedule is weak evidence. Record the execution structure before testing:

- every thread or task and the component that owns its completion;
- every operation that can block or suspend;
- every event that wakes or unblocks it;
- every queue, buffer, permit set, retry loop, and retained result with its bound;
- every cancellation point and the state visible after abandonment;
- every transport, protocol, application, and durability commit boundary;
- every order the product promises to reconstruct.

Use deterministic coordination in tests. Prefer explicit handshakes, paused time, controlled byte chunking, and scripted peers over real sleeps and favorable scheduling. A test that fails only when the machine is busy has revealed a missing protocol, not merely an inconvenient environment.


## Performance and production practice

For Course 9, freeze the claim before using a benchmark, profiler, load generator, security scanner, or release tool. Record:

- the semantic behavior that must remain unchanged;
- the workload, corpus version, and boundary;
- compiler, target, profile, features, dependencies, and host class;
- the resource or risk being investigated;
- the observation that would falsify the preferred explanation;
- displaced CPU, memory, latency, security, or operating cost;
- the release artifact and configuration to which the result applies.

Do not place noisy performance thresholds inside semantic unit tests. Do not call a local observation portable. Do not treat generated dashboards, scanner output, or a green release job as a substitute for interpretation. End each module with a one-paragraph production claim that is precise enough for another reader to challenge.
