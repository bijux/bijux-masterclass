# Glossary

Performance work goes bad when every delay is called "slow" and every surprise is called
"flaky." This glossary gives Module 09 a tighter language so incident handling and tuning
stay evidence-led instead of emotional.

## How to use this glossary

Come back to this page whenever a discussion starts drifting into vague words such as
"slow," "flaky," "noisy," or "optimization."

The glossary is not here to make the writing sound formal. It is here to keep operational
discussion precise enough that two maintainers can mean the same thing.

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

## Confusion pairs worth fixing early

These pairs matter because they decide what you measure, what you tune, and when you stop
calling something "just performance":

- `planning cost` versus `tool runtime`: planning cost happens before jobs do useful work;
  tool runtime is the time spent inside the command or script that performs the step.
- `scheduler overhead` versus `storage drag`: scheduler overhead comes from job management;
  storage drag comes from movement, promotion, or slow filesystem visibility.
- `rule-local evidence` versus `workflow-state evidence`: one explains a bounded job family;
  the other explains behavior of the workflow as a whole.
- `honest tuning` versus `semantic drift`: honest tuning preserves meaning while improving
  execution; semantic drift changes meaning while pretending to be a harmless performance
  tweak.

## Quick self-check

Before you leave Module 09, make sure you can answer these in a full sentence:

- If the DAG takes a long time to build before any real command starts, which cost class
  are you naming?
- If benchmark files show tools are fast but the run is still slow because thousands of
  tiny jobs are launched, which performance surface deserves attention?
- If one failed sample needs inspection, what narrower evidence type should you look at
  before reading the whole run history?
- If a proposed speedup drops checks, logs, or provenance needed for review, what kind of
  tuning has it stopped being?

## Terms you should be able to use by the end of the day

By the end of Module 09, you should be comfortable using these in a full sentence:

- planning cost
- scheduler overhead
- workflow-state evidence
- incident ladder
- incident class
- honest tuning
- escalation trigger
