# Exercise Answers

Use this after you have written your own answers. The point is comparison, not copying.

Strong Module 09 answers do not just list commands. They explain:

- what operational question is being asked
- why the chosen evidence surface matches that question
- how the resulting change or response preserves truth

## Exercise 1: Split one "slow build" complaint into layers

A strong answer compares at least:

- a dry-run timing signal such as `/usr/bin/time -p make -n all`
- a full-build timing signal such as `/usr/bin/time -p make all`
- a trace or evidence-size signal such as `make --trace all > build/trace.log && wc -l build/trace.log`

The key reasoning is:

- expensive dry-run suggests parse or evaluation cost
- cheap dry-run plus expensive full build suggests recipe cost
- huge trace output suggests observability overhead as an operational problem

The answer is strongest when it says how the next decision would differ depending on which
layer dominates.

## Exercise 2: Add one bounded observability surface

A strong answer names one explicit question, such as:

> how many lines of trace output does a normal route emit?

and then proposes a bounded route such as:

```make
.PHONY: trace-count

trace-count:
	@make --trace -n all 2>&1 | wc -l
```

The important move is architectural:

- the evidence surface is named
- it answers one question
- it does not mutate normal outputs

A good answer usually removes some ad hoc recipe prints in exchange.

## Exercise 3: Write a triage ladder for one flaky symptom

A strong answer usually includes:

1. confirm the exact symptom
2. reproduce the same target and assumptions
3. preview with `-n` if intent is the question
4. use `--trace` if causality is the question
5. use `-p` if resolved state is the question

The strongest answers explicitly say why editing the Makefile is not the first move:

> editing too early changes the conditions before the failure boundary is understood.

That is the real lesson.

## Exercise 4: Propose one truth-preserving optimization

A good answer might identify repeated parse-time discovery shell-outs and replace them with
a stable manifest or script boundary.

For example:

```make
build/discovery.manifest: scripts/list_sources.py src/ | build/
	@python3 scripts/list_sources.py src > $@.tmp
	@cmp -s $@.tmp $@ 2>/dev/null || mv $@.tmp $@
	@rm -f $@.tmp
```

This is strong because the optimization removes repeated work while preserving:

- explicit inputs
- a convergent boundary
- inspectable build meaning

The post-change proof should usually include both a timing comparison and a truth check such
as `make -q all` or a discovery audit.

## Exercise 5: Write a small operational runbook entry

A strong runbook entry includes:

- one sanity or convergence check
- one command for resolved-state or serial/parallel comparison
- one escalation trigger
- one warning against destructive first moves

For example:

> Run `make all` and `make -q all`. If flakiness is reported, compare serial and `-j`
> behavior before editing the build. Escalate if the symptom cannot be reproduced with a
> stable route. Avoid cleaning first unless the runbook explicitly says the question is about
> clean-state behavior.

That is a real operational note, not just a command list.

## What mastery-level answers sound like

A mastery-level answer set in this module does three things well:

- it separates cost and incident layers instead of using vague words like "slow" or "flaky"
- it treats observability as a designed surface rather than as scattered prints
- it treats performance tuning as valid only when truth and evidence quality survive the change

That is the standard Module 09 is trying to build.
