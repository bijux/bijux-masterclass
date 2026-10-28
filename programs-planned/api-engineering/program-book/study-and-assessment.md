# Study and Assessment

## Two-week course rhythm

Each course contains orientation plus ten weekday modules. Orientation is required but not counted as a teaching module. The middle weekend introduces no new subject; use it to repair failed checkpoints, consolidate notes, and rerun predecessor and course proofs.

A productive day has four phases:

1. **Understand** — read the chapter and rewrite the central model in your own words.
2. **Transfer** — answer the exercises without the reference answers.
3. **Build and break** — perform the lab, including the named failure or pressure condition.
4. **Defend** — complete the checkpoint, retain evidence, and explain the result without reading the chapter.

## Assessment model

A course score can summarize performance, but certain gates are non-compensable. You cannot offset a broken contract with polished prose, an authorization leak with high test coverage, or a failed correctness oracle with lower latency.

Recommended weighting:

- module exercises and retrieval: 20%;
- ten laboratories: 30%;
- capstone increments and implementation review: 25%;
- final proof and defense: 25%.

Completion requires every module checkpoint and the final course defense.

## Recovery when a checkpoint fails

Do not immediately reread the entire chapter. Use this sequence:

1. restate the failed claim in one sentence;
2. identify its owner and evidence layer;
3. minimize the counterexample;
4. compare the result with the reference answer or implementation;
5. repair the mental model before repairing code;
6. rerun the narrow oracle;
7. rerun the module proof;
8. explain why the previous approach appeared plausible.

If the problem is environmental, record the exact missing dependency and complete all lower evidence classes. Do not mark the live route as passed.

## Notes worth keeping

Keep a decision journal rather than a transcript. For each module record:

- the central question;
- three governing invariants;
- one seductive wrong design;
- one decisive counterexample;
- one Python/TypeScript comparison;
- one proof limitation;
- the capstone state before and after the module.

These notes become the most useful preparation for the final program defense.
