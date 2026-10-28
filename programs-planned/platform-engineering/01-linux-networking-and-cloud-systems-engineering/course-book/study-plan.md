# Ten-Day Study Plan

The course is designed as ten dense study days plus orientation. A day is approximately eight focused hours, not twelve hours of passive reading. Use a longer schedule when Linux is new to you. The checkpoints, not the calendar, determine progression.

## Daily rhythm

| Phase | Purpose |
|---|---|
| Retrieval, 30 minutes | Reconstruct yesterday's model without notes |
| Chapter, 90 minutes | Read for ownership, transitions, and failure boundaries |
| Worked inspection, 60 minutes | Follow examples and inspect the actual capstone files |
| Exercises, 90 minutes | Solve all twelve before opening answers |
| Break and review, 30 minutes | Identify one uncertain concept to revisit |
| Lab, 150 minutes | Predict, inject, observe, repair, and clean |
| Checkpoint, 60 minutes | Assemble evidence and explain the result aloud |
| Synthesis, 30 minutes | Write the handoff to the next module |

Do not compress the experiment phase to make up for slow reading. The lab is where attractive but incomplete models are falsified.

## Orientation

Classify the host, establish the evidence boundary, run the local capstone tour, and prepare a disposable VM plan. No privileged change is required.

## Day 1 — Processes

Trace Atlas API and worker process identity, descriptors, signals, and exit behavior. Finish with a clean graceful-stop transcript and an explanation of what `SIGKILL` cannot preserve.

## Day 2 — Identity and supervision

Design service users, path ownership, umask, capability policy, systemd lifecycle, and negative authority tests. Finish with verified unit files and a privilege-transition table.

## Day 3 — Resources

Measure CPU, memory, tasks, descriptors, cgroup state, and pressure. Apply a bounded envelope in a disposable environment and distinguish throttling from OOM failure.

## Day 4 — Storage

Trace bytes from userspace buffers to filesystem publication. Exercise atomic write, disk-full handling, backup, empty-destination restore, and crash-point reasoning.

## Day 5 — Networking

Build the listener and route model, observe TCP state, test IPv4/IPv6 and timeouts, and diagnose a deliberately wrong binding without changing multiple layers at once.

## Day 6 — DNS, HTTP, and TLS

Generate and inspect the local PKI, separate DNS from SNI, certificate identity, route, and HTTP authority, and perform a verified request without `-k`.

## Day 7 — Intermediaries

Apply host firewall policy in a disposable namespace or VM, inspect trusted proxy headers, reason about retries and draining, and verify that unsafe writes are not replayed.

## Day 8 — Virtual machines

Build or inspect a disposable VM, classify image/boot/durable state, and conduct a replacement exercise. Record image and instance identity rather than saying only that “the VM restarted.”

## Day 9 — Cloud primitives

Map the same host requirements to AWS, GCP, and Azure concepts without treating similar names as identical semantics. Defend one failure-domain claim and record quota and cost dependencies.

## Day 10 — Production host defense

Run the full local proof, then a bounded VM game day if available. Restore every boundary, verify cleanup, and export the Course 2 handoff.

## Recovery rule

A failed checkpoint is useful evidence. Do not hide it by rerunning until green without preserving the first failure. Record the observation, revise the model, rerun the focused proof, and explain why the repair addresses the mechanism rather than merely suppressing the symptom.

## Completion standard

You complete the course when the dependency-light proof passes, every checkpoint has evidence, the strongest available environment-backed labs are truthfully classified, the final defense is coherent, and the Course 2 handoff describes infrastructure requirements that another engineer could implement without asking what the host actually needs.
