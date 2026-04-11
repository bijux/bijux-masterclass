# Glossary

This glossary keeps the language of Module 09 stable.

The goal is practical incident and performance clarity: when the same terms keep the same
meaning, review gets faster and less argumentative.

## Terms

| Term | Meaning in this module |
| --- | --- |
| cost class | A named source of workflow time such as planning, scheduler overhead, storage drag, or tool runtime. |
| planning cost | Time spent discovering inputs, expanding targets, resolving wildcards, and building the DAG before jobs really run. |
| scheduler overhead | Time spent launching, tracking, and finalizing jobs rather than performing the scientific or analytic work itself. |
| storage drag | Delay caused by staging, scratch promotion, shared filesystem latency, or slow visibility of files. |
| tool runtime | The time spent inside the script, wrapper, or external tool that performs the real step-local work. |
| evidence surface | A specific artifact or command output used to answer one review question, such as a log, benchmark, summary, or provenance file. |
| rule-local evidence | Evidence tied to one rule or target, usually logs or benchmark files for a specific job family. |
| workflow-state evidence | Evidence about the workflow as a whole, such as dry-run output, summaries, or rerun-cause listings. |
| provenance | The configuration, profile, environment, and runtime identity that explain what produced a given published result. |
| incident ladder | A fixed sequence for moving from symptom to evidence to classification before editing the workflow. |
| incident class | The current boundary where the problem appears to live: workflow semantics, operating context, storage behavior, or tool behavior. |
| noisy evidence | Evidence that exists but does not help answer the actual review question because it is too broad, too vague, or too verbose. |
| semantic drift | A change that alters workflow meaning, file-contract truth, or published meaning while being framed as something smaller. |
| honest tuning | A performance improvement that keeps workflow semantics, declared dependencies, and review evidence intact. |
| runbook | A short operational route that tells maintainers what to run first, what to inspect next, and when to escalate. |
| escalation trigger | A condition that says the issue has crossed a boundary and should move from local debugging into profile review, publish review, or design review. |

## How to use these terms

If a performance or incident discussion starts getting vague, ask which term has become
unclear:

- are we talking about planning cost or tool runtime?
- do we need workflow-state evidence or rule-local evidence?
- is this still honest tuning, or has it crossed into semantic drift?
- is the next move a local repair or an escalation trigger?

Those questions usually expose the real disagreement quickly.
