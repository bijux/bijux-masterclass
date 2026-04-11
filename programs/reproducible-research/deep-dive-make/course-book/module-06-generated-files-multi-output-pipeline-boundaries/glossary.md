# Glossary

Use this glossary to keep the language of Module 06 stable while you move between the core
lessons, worked example, and exercises.

The goal is not more jargon. The goal is to make sure the same generator fact keeps the
same name whenever you explain staleness, publication, or pipeline trust.

## How to use this glossary

If a discussion starts sliding into vague phrases like "the generator refreshed things" or
"the pipeline mostly finished," stop and look up the term doing the most work in the
argument. Module 06 becomes much clearer once the team agrees on the right nouns.

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| atomic publication | A practical publication discipline where incomplete generation work stays out of trusted output paths until the result is ready. |
| boundary file | A manifest or stamp that represents a real semantic boundary or completion event in the generation pipeline. |
| completion point | The moment or graph node after which downstream targets may treat a generation event as finished. |
| consumer edge | The dependency from a downstream target to the published generated content it actually reads or trusts. |
| coupled outputs | Several files that belong to one logical generation event and therefore need one honest publication model. |
| generated file | A build target produced by a rule or pipeline rather than authored directly as source. |
| grouped targets | GNU Make's `&:` form for saying several outputs are published by one logical recipe execution. |
| manifest | A descriptive boundary file that records stable facts about a generation event, such as schema, mode, or fingerprint. |
| multi-output producer | A generator command or pipeline stage that publishes more than one output as one semantic event. |
| partial publication | A broken state where some outputs become visible as trusted results before the full generation step has succeeded. |
| pipeline boundary | The exact point where one stage of generation hands a trustworthy result to the next stage or to final consumers. |
| publication event | The logical act of making generated outputs or a boundary file trustworthy to downstream targets. |
| semantic input | Any declared file or modeled fact that changes the meaning of a generated output. |
| stamp | A file that represents successful completion of a generation event when no ordinary output alone captures that truth well enough. |
| stale generated output | A generated artifact whose declared inputs changed without an honest rebuild, or whose consumers failed to react correctly. |
| temporary path | A non-trusted workspace used while generation or validation is still in progress. |
| trusted output path | A final published path that downstream targets are allowed to consume as truthful build output. |
| unstable manifest | A boundary file that changes every run because it records noise rather than stable semantic meaning. |

## The vocabulary standard for this module

When you explain a Module 06 incident, aim to say things like:

- "the consumer edge skipped the published header"
- "the coupled outputs need one publication event"
- "that stamp is justified because it represents completion"
- "the manifest is unstable because it records noise"
- "downstream trust begins only after atomic publication"

Those sentences are much more useful than saying only "the generator is weird."
