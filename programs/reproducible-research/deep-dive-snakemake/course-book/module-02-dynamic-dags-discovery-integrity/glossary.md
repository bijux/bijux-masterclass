# Glossary

Use this glossary to keep the language of Module 02 stable while you move between the
core lessons, worked example, exercises, and capstone evidence.

The goal is not extra jargon. The goal is to make sure dynamic behavior is described with
clear nouns instead of mystical shortcuts.

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| checkpoint | A controlled point where Snakemake can reevaluate downstream jobs after a declared output has been produced. |
| discovered set | The concrete collection of samples, shards, or units that discovery found for one run. |
| discovery surface | The declared input boundary that decides what the workflow is allowed to discover. |
| dynamic DAG | A workflow graph whose downstream job set depends on data learned during the run. |
| fanout | The expansion from one validated unit list into many concrete per-unit targets. |
| manifest | A declared inventory of files that belong to a publish boundary, often with integrity information. |
| ownership domain | The family of paths a wildcard or rule is allowed to claim. |
| parse-time discovery | Discovery that happens while the Snakefile is being read, before job execution begins. |
| provenance | The run-identity evidence that explains which configuration and software state produced the outputs. |
| publish boundary | The versioned output surface a downstream consumer is allowed to trust. |
| registry | A durable file that records discovery in a structured way, such as `discovered_samples.json`. |
| scheduler cost | The overhead of launching, tracking, and coordinating jobs, apart from the useful work they perform. |
| software boundary | The declared environment or container surface that explains which tools a rule needs. |
| target list | The explicit set of files the workflow is trying to build for a given run. |
| wildcard constraint | A regex restriction that narrows which filename shapes a wildcard may claim. |

## The vocabulary standard for this module

When you explain a Module 02 situation, aim to say things like:

- "the discovered set is recorded in one owned registry"
- "that checkpoint is justified because the downstream target list is not known earlier"
- "this is a fanout-control problem, not just a syntax problem"
- "the publish boundary preserves the discovery fact for later review"
- "the workflow is slow because scheduler cost dominates useful work"

Those sentences are much more useful than saying only "Snakemake gets weird with dynamic workflows."
