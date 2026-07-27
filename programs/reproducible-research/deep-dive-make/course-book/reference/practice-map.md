# Practice Map


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Reference"]
  page["Practice Map"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Use this page when you want the shortest route from a Deep Dive Make module to a local
exercise, proof loop, and capstone follow-up.

## Module practice surfaces

| Module | Exercises 1-5 establish | Exercises 6-10 integrate | Best capstone follow-up |
| --- | --- | --- | --- |
| 01 | targets, prerequisites, convergence | depfiles, deletion recovery, and a tiny project | inspect the capstone `Makefile` after local convergence is clear |
| 02 | parallel graph reasoning | pressure runs, failure classification, and repair | inspect repros and object discovery surfaces |
| 03 | determinism and debugging | negative tests, evidence capture, and selftest design | compare with `capstone/tests/run.sh` |
| 04 | precedence and semantics | include remakes, ambiguity diagnosis, and semantic incidents | inspect public target surfaces and diagnostics |
| 05 | portability and hidden inputs | tool audits, jobserver behavior, and environment convergence | inspect contract and stamp boundaries |
| 06 | generated targets and publication | deletion recovery, failure injection, and complete pipelines | inspect scripts and modeled inputs together |
| 07 | public APIs and include layers | caller audits, macro inspection, and repository growth | inspect the `mk/*.mk` ownership split |
| 08 | artifact and install contracts | reproducible archives, checksum failure, and release rehearsal | inspect package and attestation boundaries |
| 09 | cost layers and incident evidence | repeated baselines, rebuild causality, and response packets | compare with capstone incident evidence |
| 10 | review and migration reasoning | characterization, governance tests, and stewardship portfolio | use the capstone as the final stewardship specimen |

## Reusable proof loops

- truth loop: `make --trace all`, `make all`, `make -q all`
- concurrency loop: compare clean serial and parallel builds
- diagnostics loop: `make -n <target>`, `make --trace <target>`, `make -p`
- public-target loop: `make help`, then the smallest documented target for the current claim

## The 100-exercise ledger

Track every exercise with four fields: command or artifact, observation, explanation, and
remaining question. A module is not complete because its page was read. It is complete
when all ten entries contain evidence you can explain without the answer page open.

## Cumulative evidence portfolio

Do not let each module disappear into a separate directory. Keep these artifacts as one
story of increasing responsibility:

| Module | Portfolio artifact | What it proves about your judgment |
| --- | --- | --- |
| 01 | prediction and observation sheet | you distinguish the graph from recipe side effects |
| 02 | target ownership table | you distinguish safe overlap from shared-state interference |
| 03 | positive and negative selftest claim | you know whether a check can detect the defect it names |
| 04 | semantic event log | you locate a failure in reading, expansion, rule choice, or execution |
| 05 | environment assumption ledger | you separate capabilities, semantic inputs, and diagnostics |
| 06 | generator publication record | you can define when a coupled output set becomes trustworthy |
| 07 | architecture ownership map | you can trace a public target through clear responsibilities |
| 08 | consumer release packet | you can inspect, verify, and install without producer folklore |
| 09 | measured optimization record | you preserve convergence and artifact truth while tuning |
| 10 | migration proof bridge | you preserve evidence and rollback points across ownership change |

Each artifact should fit on one or two pages. The purpose is not administrative weight.
It is to make your reasoning reviewable by someone who did not watch you complete the
exercise.

## Final portfolio review

At the end of Module 10, choose one artifact from the first half and one from the second
half. Explain the connection. For example:

- a Module 01 hidden edge becomes a Module 06 publication defect
- a Module 02 ownership collision becomes a Module 09 incident
- a Module 05 undeclared capability becomes a Module 10 migration constraint

Then give the portfolio to another learner and ask them to reproduce one claim. Repair
any missing command, input description, or interpretation they discover. Reproducibility
applies to learning evidence too.
