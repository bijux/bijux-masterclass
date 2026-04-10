# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
produce clever Make syntax. The goal is to make your reasoning visible.

## Exercise 1: Draw the graph

Take the tiny C project and draw the dependency graph for `app`, `build/main.o`, and
`build/util.o`. Mark which nodes are real files and which ones are convenience targets.

Focus question: where would a missing edge create a lie?

## Exercise 2: Find a hidden input

Modify the build so that changing `CFLAGS` should matter. Then explain why a plain object
rule does not automatically capture that fact.

Focus question: what evidence would you add so the graph stays truthful?

## Exercise 3: Review rule ownership

Write one explicit rule and one pattern rule for the same build. Compare them and explain
which output path each recipe owns.

Focus question: where would multi-writer confusion start?

## Exercise 4: Explain evaluation timing

Write one example that uses `:=` and one that uses `=`. Predict when each value is
computed and how that changes the graph or recipe behavior.

Focus question: which version is safer for a source-file list?

## Exercise 5: Prove safe publication

Take a compile or link rule and redesign it to publish through a temporary file. Then
state exactly what failure should leave behind.

Focus question: how do you prove the final target path never points at a partial artifact?
